#!/bin/python3

import requests
import logging
import os
import time
import subprocess
import datetime

def log_error(message):
    logging.error(f"{message}")

EXPORT_MD_ENDPOINT = "127.0.0.1:6806/api/export/exportMdContent"
EXPORT_RESOURCES_ENDPOINT = "127.0.0.1:6806/api/export/exportResources"

# Replace 'YOUR_API_KEY' with the actual API key if required for authorization.
#! DELETE BEFORE COMMITTING
headers = {
    "Authorization": "YOUR_API_KEY"
}

# Set the ID of the doc block to export.
doc_block_id = "20230207170649-mlrulge"

# Set the list of file or folder paths to export.
file_paths = [
    "/conf/appearance/boot",
    "/conf/appearance/langs",
    "/conf/appearance/emojis/conf.json",
    "/conf/appearance/icons/index.html",
]

# Set the name of the zip file to be created (optional).
zip_file_name = "exported-files.zip"

def export_markdown():
    params = {
        "id": doc_block_id
    }

    response = requests.post(EXPORT_MD_ENDPOINT, json=params, headers=headers)
    if response.status_code == 200:
        data = response.json()["data"]
        h_path = data["hPath"]
        content = data["content"]
        # You can do whatever you want with the exported content here.
        print(f"Exported Markdown Path: {h_path}")
        print(f"Markdown Content: {content}")
    else:
        print(f"Failed to export Markdown. Error: {response.json()['msg']}")


def export_files_and_folders():
    params = {
        "paths": file_paths,
        "name": zip_file_name
    }

    response = requests.post(EXPORT_RESOURCES_ENDPOINT, json=params, headers=headers)
    if response.status_code == 200:
        data = response.json()["data"]
        zip_file_path = data["path"]
        # You can do whatever you want with the zip file path here.
        print(f"Exported Zip File Path: {zip_file_path}")
    else:
        print(f"Failed to export files and folders. Error: {response.json()['msg']}")


def send_dir():
    
    # Get current time and use it as part of the backup folder name
    now = time.strftime("%d-%m-%Y")
    path = f"siyuan-backup_{now}"
    
    # Define the backup directory    
    full_path = os.path.join(backup_dir, path)
    
    # Check if a backup with the same name already exists
    if os.path.exists(full_path):
        print(f"There is already one backup for this {path}")
    else:
        try:
            # Move the backup folder to the backup directory
            subprocess.run(["mv", f"siyuan-backup_{now}", backup_dir])  
            print("Backups have been successfully moved to the backup directory")            
        except subprocess.CalledProcessError:
            print("Error: while moving files to backup directory")
            return

def delete_oldest(file_prefix, date_format, days_old):
    
    """
    This function deletes the oldest backup directory based on the number of days old.

    :param backup_dir: Path of the directory where the backups are stored
    :param file_prefix: Prefix of the backup directories to be deleted
    :param date_format: Date format of the backup directories
    :param days_old: Number of days after which the backup should be deleted
    """
    # Get the current date and time
    now = datetime.datetime.now()
    # Loop through all the files in the directory
    for f in os.listdir(backup_dir):
        # Check if the file starts with the given prefix
        if f.startswith(file_prefix):
            # Extract the date part from the file name
            backup_date = datetime.datetime.strptime(f.split("_")[-1], date_format)
            # Calculate the difference between the current date and the backup date
            delta = now - backup_date
            # If the difference is greater than the given number of days, delete the backup
            if delta.days > days_old:
                # Construct the full path of the backup directory
                path = os.path.join(backup_dir, f)
                # Check if the path is a directory
                if os.path.isdir(path):
                    confirm = input(f"Do you want to remove'{f}' permanently (y/n)?")
                    if confirm.lower() == 'y':
                        # Delete the directory
                        subprocess.run(["rm", "-r", path])
                        # Print a message indicating the oldest backup has been deleted
                        print(f"Deleted the oldest backup: {f}")
# Define backups directory                    
backup_dir = os.path.expanduser("~") + "/Documents/app_backups/siyuan_Backups/"





# List of URLS of the zip files you want to download
urls = [   
    "http://127.0.0.1:42989/export/Notes.zip",    
]

# def main():
#     # Call the function to backup files.
#     backup(urls)
#     # Call the function to move backups to backups directory
#     send_dir()
    
#     # Call the function to delete the oldest backup that is more than 90 days old
#     delete_oldest("siyuan-backup_", "%d-%m-%Y", 90)

if __name__ == "__main__":
    export_markdown()
    export_files_and_folders()


