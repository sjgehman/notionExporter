# notionExporter
Export attachments from Notion databases into a local folder using the Notion API

## Setup (skip to step 2 if you have Python downloaded)

### 1. Download and Install Python

1. **Download Python**:
   - Go to the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Click on the "Download Python" button to download the latest version of Python.

2. **Install Python**:
   - Open the downloaded installer.
   - Make sure to check the box that says "Add Python to PATH".
   - Click on "Install Now" and follow the prompts to complete the installation.

### 2. Install Required Packages

1. **Open Command Prompt**:
   - Press `Win + R`, type `cmd`, and press `Enter`.

2. **Install Packages**:
   - In the Command Prompt, type the following command and press `Enter`:

     pip install notion-client requests
     
   - This will install the `notion-client` and `requests` packages, which are required for the script.

### 3. Prepare the Script

1. **Save the Script**:
   - Copy the provided script into a text editor (e.g., Notepad) and save it with the name `exportnotion.py`.

2. **Customize the Script**:
   - Open `exportnotion.py` in the text editor.
   - Replace the following placeholders with your actual values:
     - `'YOUR_INTEGRATION_TOKEN'` with your Notion integration token. Available at notion.so/my-integrations
     - `'YOUR_DATABASE_ID'` with your Notion database ID. To find a database ID, navigate to the database URL in your Notion workspace. The ID is the string of characters in the URL that is between the slash following the workspace name (if applicable) and the question mark. The ID is a 32 characters alphanumeric string.
     - `'FIELD_NAME'` with your desired field name. It's currently built for multi-select fields, but you can edit this.
     - `'FIELD_VALUE'` with your desired field value

### 4. Run the Script
1. **Navigate to the Script Location:**
- In the Command Prompt, navigate to the folder where you saved exportnotion.py. Use the cd command to change directories. e.g. "cd Documents"
- If you forget what folders/files are in a directory, you can type "ls" to see a list of available options. If you change into the wrong directory, "cd .." allows you to go back a directory
2. **Run the script**
- Once in the directory where the python file is saved, in the Command Prompt, type: py exportnotion.py
- The script will run and download the attachments to the "attachments" folder.
