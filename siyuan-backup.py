#!/bin/python3

import requests
import logging
import os
import time
import subprocess
from datetime import datetime

def log_error(message):
    logging.error(f"{message}")

def download_file(url, folder_name):

    # Send a request to the URL to get the file
    response = requests.get(url)

     # Check if the request was successful
    if response.status_code == 200:
        # Get the filename from the URL
        filename = url.split("/")[-1]
        file_path = f"{folder_name}/{filename}"

        # Check if the file already exists in the folder
        if os.path.exists(file_path):
            logging.info(f"{filename} already exists in {folder_name}. Skipping download.")
        else:
            # Open a file to save the zip file
            with open(file_path, "wb") as file:
                # Write the content of the response to the file
                file.write(response.content)
    else:
        log_error(f"Failed to download {url} or siyuan-note not opened.")

def backup(urls):
    # Configure logging
    logging.basicConfig(filename="error.log", level=logging.ERROR, format="%(asctime)s: %(message)s")

    # Create a folder with the current time as its name
    now = datetime.now().strftime("%d-%m-%Y")
    folder_name = f"siyuan-backup_{now}"
    os.makedirs(folder_name, exist_ok=True)

    # Loop through each URL and download the file
    for url in urls:
        download_file(url, folder_name)

def send_dir():
    # Get current time and use it as part of the backup folder name
    now = time.strftime("%d-%m-%Y")
    path = f"siyuan-backup_{now}"
    
    # Define the backup directory
    backup_dir = os.path.expanduser("~") + "/Documents/backup_Documents/siyuan_Backups/"
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

# List of URLS of the zip files you want to download
urls = [
    "http://127.0.0.1:42989/export/English.zip",
    "http://127.0.0.1:42989/export/Lesson%20Notes.zip",
    "http://127.0.0.1:42989/export/Notes.zip",    
    "http://127.0.0.1:42989/export/Lesson%20Notes.sy.zip",
    "http://127.0.0.1:42989/export/English.sy.zip",
    "http://127.0.0.1:42989/export/Notes.sy.zip",
]

def main():
    backup(urls)
    send_dir()

if __name__ == "__main__":
    main()
