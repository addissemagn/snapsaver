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
import argparse

# <-FIXME->
# FIXME: how does this work with multiple simultaneous requests?
# FIXME: security, i.e. plaintext password in email manager

# <-BUG->
# BUG: mp4 download doesn't work
# BUG: submitting with /#first, etc fails

# Path to uploaded json files
UPLOADS_PATH = "uploads/"

urls = {} # dict of urls of all photos

def main():
    args = arguments()
    snapchat_downloader(args.memories_path, args.email)

def arguments():
   parser = argparse.ArgumentParser()
   parser.add_argument("--memories_path", required=True, type=str,
                       help="Path to memories_history.json.")
   parser.add_argument("--email", required=False, type=str, 
                       help="Email to send downloads to.")
   return parser.parse_args()

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

# Download the media file
def download_url(url, file_path, type, date, time):
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
        print("Error downloading file: {}".format(file_name))
        # print(e)

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

def write_file_binary(file_path, file_contents):
    with open(file_path, 'wb') as f:
        f.write(file_contents)

def check_duplicates():
    pass

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

if __name__=="__main__":
    main()
