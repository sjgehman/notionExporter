import os
import requests
from urllib.parse import urlparse
from notion_client import Client
import uuid
import re

# Replace these variables with your actual values
INTEGRATION_TOKEN = ''
DATABASE_ID = ''

# Filter field name and value
FILTER_NAME = 'Type'
FILTER_VALUE = 'Uber/Lyft/Taxi/Bus'

# Fields to combine items from the table to name the attachment
EXPENSE_TITLE_1 = 'Expense'
EXPENSE_TITLE_2 = 'Date(s)'

# Initialize the Notion client
notion = Client(auth=INTEGRATION_TOKEN)

# Create a folder called "attachments" if it doesn't exist
attachments_folder = 'attachments'
os.makedirs(attachments_folder, exist_ok=True)

def sanitize_filename(filename):
    # Remove or replace any characters that are not allowed in filenames
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_file(url, dest_folder, filename):
    unique_filename = filename
    local_filename = os.path.join(dest_folder, unique_filename)
    
    # Ensure the filename is unique by appending a number if it already exists
    base_filename, file_extension = os.path.splitext(local_filename)
    counter = 1
    while os.path.exists(local_filename):
        local_filename = f"{base_filename}_{counter}{file_extension}"
        counter += 1

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def build_filter(field_name, field_value, field_type):
    if field_type == 'multi_select':
        return {
            "property": field_name,
            "multi_select": {
                "contains": field_value
            }
        }
    elif field_type == 'select':
        return {
            "property": field_name,
            "select": {
                "equals": field_value
            }
        }
    elif field_type == 'rich_text':
        return {
            "property": field_name,
            "rich_text": {
                "contains": field_value
            }
        }
    elif field_type == 'number':
        return {
            "property": field_name,
            "number": {
                "equals": float(field_value)
            }
        }
    elif field_type == 'date':
        return {
            "property": field_name,
            "date": {
                "equals": field_value
            }
        }
    elif field_type == 'status':
        return {
            "property": field_name,
            "status": {
                "equals": field_value
            }
        }
    else:
        raise ValueError(f"Unsupported field type: {field_type}")

def get_field_type(database_id, field_name):
    database = notion.databases.retrieve(database_id)
    return database['properties'][field_name]['type']

def get_attachments_from_database(database_id, filter_name, filter_value, expense_title_1, expense_title_2):
    field_type = get_field_type(database_id, filter_name)
    filter_condition = build_filter(filter_name, filter_value, field_type)

    results = notion.databases.query(
        database_id=database_id,
        filter=filter_condition
    ).get('results')

    for page in results:
        expense_name = page['properties'].get(expense_title_1, {}).get('title', [{}])[0].get('text', {}).get('content', 'Unknown Expense')
        date_value = page['properties'].get(expense_title_2, {}).get('date', {}).get('start', 'Unknown Date')
        formatted_date = date_value.split('T')[0].replace('-', '.') if date_value != 'Unknown Date' else 'Unknown Date'

        for prop_name, prop_value in page['properties'].items():
            if prop_value['type'] == 'files':
                for file_info in prop_value['files']:
                    if file_info['type'] == 'external':
                        file_url = file_info['external']['url']
                        print(f'Downloading {file_url}')
                        filename = sanitize_filename(f"{formatted_date}_{expense_name}{os.path.splitext(urlparse(file_url).path)[-1]}")
                        download_file(file_url, attachments_folder, filename)
                    elif file_info['type'] == 'file':
                        file_url = file_info['file']['url']
                        print(f'Downloading {file_url}')
                        filename = sanitize_filename(f"{formatted_date}_{expense_name}{os.path.splitext(urlparse(file_url).path)[-1]}")
                        download_file(file_url, attachments_folder, filename)

# Call the function with the specified database ID, filter name, and filter value
get_attachments_from_database(DATABASE_ID, FILTER_NAME, FILTER_VALUE, EXPENSE_TITLE_1, EXPENSE_TITLE_2)
