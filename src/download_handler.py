import urllib.request
import urllib
from urllib.parse import urlparse
import json
from pathlib import Path
import zipfile
import os
import sys
from email_handler import send_email
import shutil

# <-TODO->
# TODO: date range
# TODO: status tracker - i.e. count of how many done / how many
# TODO: post this on redit
# TODO: add actual metadata to files
# TODO: log of downloads in .txt file
# TODO: error handling for if the file uploaded is not correct
# TODO: add a page for status or something after user submits
# TODO: write check_duplicates

# <-FIXME->
# FIXME: how does this work with multiple simultaneous requests?
# FIXME: security, i.e. plaintext password in email manager

# <-BUG->
# BUG: mp4 download doesn't work
# BUG: submitting with /#first, etc fails

# Path to uploaded json files
UPLOADS_PATH = "uploads/"

# 
def write_file_binary(file_path, file_contents):
    with open(file_path, 'wb') as f:
        f.write(file_contents)

# Download the media file
def download_url(url, file_path, type, date, time):
    # Name the file according to its type
    file_name = "Snapchat-{}__{}".format(date, time)
    if type == "PHOTO":
        file_name += ".jpg"
    elif type == "VIDEO":
        file_name += ".mp4"

    parts = url.split('?')
    post_url = parts[0]
    post_data = parts[1].encode('utf-8')

    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }

    # get_download_url = ''

    try:
        req = urllib.request.Request(post_url, data=post_data, headers=headers)
        response = urllib.request.urlopen(req)
        download_url = response.read().decode()
        response = urllib.request.urlopen(download_url)
        downloaded_contents = response.read()

        file_path = os.path.join(file_path + file_name)

        with open(file_path, 'wb') as f:
            f.write(downloaded_contents)
    except Exception as e:
        print(f'An exception occurred when attempting to download "{name}": {str(e)}')

# If file already exists do not download TODO: maybe check if already exists in dictionary
def check_duplicates():
    pass

def process_json(memories_path, FILE_PATH):
    with open(memories_path) as fd:
        data = json.load(fd)
        saved_media = data["Saved Media"]

        count = 0
        size = len(saved_media)
        print(size)

        for memory in saved_media:
            timestamp = memory["Date"]
            year, month, day = timestamp[0:4], timestamp[5:7], timestamp[8:10]
            date = "{}-{}-{}".format(year, month, day)
            time = "{}-{}-{}".format(timestamp[11:13], timestamp[14:16], timestamp[17:19])

            # Create nested file directory in FILE_PATH/year/month
            media_path = FILE_PATH + year + "/" + month + "/"
            Path(media_path).mkdir(parents=True, exist_ok=True)

            # Increment file count for status
            count += 1

            # Download file
            download_url(url = memory["Download Link"], file_path = media_path, type = memory["Media Type"], date = date, time = time)

# TODO: delete in upload folder too
def reset(FILE_PATH, ZIP_PATH):
    # Delete zip file
    try:
        os.remove(ZIP_PATH + 'snapchat_memories.zip')
    except Exception as e:
        zip_name = 'snapchat_memories.zip'
        print(f'Exception when attempting to delete "{ZIP_PATH + zip_name}": {str(e)}')

    # Delete downloaded media files
    try:
        shutil.rmtree(FILE_PATH)
        shutil.rmtree(ZIP_PATH)
    except Exception as e:
        print(f'Exception when attempting to delete a directory: {str(e)}')

# Zip directory of images
def zip_handler(FILE_PATH, ZIP_PATH):
    # Make a directory for this user's zip
    Path(ZIP_PATH).mkdir(parents=True, exist_ok=True)
    # Create a zip file in the zips/ directory
    ziph = zipfile.ZipFile(ZIP_PATH + 'snapchat_memories.zip', 'w', zipfile.ZIP_DEFLATED)

    path = FILE_PATH

    # Compress directory with downloaded files
    # Ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

    ziph.close()

def snapchat_downloader(memories_path, receiver_email):
    # Path to extracted images, initialized in snapchat_downloader w/ user email
    FILE_PATH = "downloads/"
    # Path to all the zip files ready to send
    ZIP_PATH = "zips/"
    # Create unique directories indexed by email for downloads and zip files
    FILE_PATH += "{}/".format(receiver_email)
    ZIP_PATH += "{}/".format(receiver_email)

    # Process the memories json file
    process_json(memories_path, FILE_PATH)
    # Zip directory of images
    zip_handler(FILE_PATH, ZIP_PATH)
    # Send the email with the downloads
    send_email(receiver_email, ZIP_PATH + "snapchat_memories.zip")

    # Delete all data from this session and reset global vars
    reset(FILE_PATH, ZIP_PATH)
    FILE_PATH = "downloads/"
    ZIP_PATH = "zips/"

if __name__=="__main__":
    memories_path = input("Input path to memories: ")
    receiver_email = input("Input receiver email: ")
    snapchat_downloader(memories_path, receiver_email)
