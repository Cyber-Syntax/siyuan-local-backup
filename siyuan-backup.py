#!/bin/python3

import requests
import logging
import os
import time
import subprocess
import datetime

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
    now = datetime.datetime.now().strftime("%d-%m-%Y")
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
backup_dir = os.path.expanduser("~") + "/Documents/backup_Documents/siyuan_Backups/"





# List of URLS of the zip files you want to download
urls = [   
    "http://127.0.0.1:42989/export/Notes.zip",    
]

def main():
    # Call the function to backup files.
    backup(urls)
    # Call the function to move backups to backups directory
    send_dir()
    
    # Call the function to delete the oldest backup that is more than 90 days old
    delete_oldest("siyuan-backup_", "%d-%m-%Y", 90)
if __name__ == "__main__":
    main()

