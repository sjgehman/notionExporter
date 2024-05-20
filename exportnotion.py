import os
import requests
from urllib.parse import urlparse
from notion_client import Client
import uuid

# Replace these variables with your actual values
INTEGRATION_TOKEN = 'YOUR_INTEGRATION_TOKEN'
DATABASE_ID = 'YOUR_DATABASE_ID'
FIELD_NAME = 'Trip Title'
FIELD_VALUE = 'NYC 2023'

# Initialize the Notion client
notion = Client(auth=INTEGRATION_TOKEN)

# Create a folder called "attachments" if it doesn't exist
attachments_folder = 'attachments'
os.makedirs(attachments_folder, exist_ok=True)

def download_file(url, dest_folder):
    parsed_url = urlparse(url)
    # Use the path component of the URL to generate a filename and add a unique identifier
    filename = os.path.basename(parsed_url.path)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    local_filename = os.path.join(dest_folder, unique_filename)
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

#You will need to edit the below if the field is not a multi-select field
def get_attachments_from_database(database_id, field_name, field_value):
    filter_condition = {
        "property": field_name,
        "multi_select": {
            "contains": field_value
        }
    }

    results = notion.databases.query(
        database_id=database_id,
        filter=filter_condition
    ).get('results')

    for page in results:
        # Iterate through properties and find attachments
        for prop_name, prop_value in page['properties'].items():
            if prop_value['type'] == 'files':
                for file_info in prop_value['files']:
                    if file_info['type'] == 'external':
                        file_url = file_info['external']['url']
                        print(f'Downloading {file_url}')
                        download_file(file_url, attachments_folder)
                    elif file_info['type'] == 'file':
                        file_url = file_info['file']['url']
                        print(f'Downloading {file_url}')
                        download_file(file_url, attachments_folder)

# Call the function with the specified database ID, field name, and field value
get_attachments_from_database(DATABASE_ID, FIELD_NAME, FIELD_VALUE)
