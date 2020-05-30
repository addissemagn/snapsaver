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

import config # mport config file

# <-FIXME->
# FIXME: how does this work with multiple simultaneous requests?
# FIXME: security, i.e. plaintext password in email manager

# <-BUG->
# BUG: mp4 download doesn't work
# BUG: submitting with /#first, etc fails

# Path to uploaded json files
UPLOADS_PATH = config.UPLOADS_PATH 

all_media = dict(
            all_media = {},
            stats = {}
        )

def main():
    args = arguments()

    # Create unique directories indexed by email for downloads and zip files
    FILE_PATH = config.FILE_PATH + args.email + "/"
    ZIP_PATH = config.ZIP_PATH + args.email + "/"

    # Process the memories json file
    process_json(args.memories_path, FILE_PATH)

    # Download all the files
    download_files()

    # Create zip directory of images
    zip_handler(FILE_PATH, ZIP_PATH)

    if args.email != config.default_email:
        # Send the email with the downloads
        send_email(args.email, ZIP_PATH + "snapchat_memories.zip")

        # Delete all data from this session
        reset(FILE_PATH, ZIP_PATH)


def process_json(memories_path, FILE_PATH):
    with open(memories_path) as fd:
        data = json.load(fd)
        saved_media = data["Saved Media"]


        for memory in saved_media:
            url = memory["Download Link"]

            if url not in all_media["all_media"]:
                tstamp = memory["Date"]
                year, month, day = tstamp[0:4], tstamp[5:7], tstamp[8:10]
                date = "{}-{}-{}".format(year, month, day)
                time = "{}-{}-{}".format(tstamp[11:13], tstamp[14:16], tstamp[17:19])

                # Create nested file directory in FILE_PATH/year/month
                media_path = FILE_PATH + year + "/" + month + "/"
                Path(media_path).mkdir(parents=True, exist_ok=True)

                media = dict(
                    url = url, 
                    path = media_path,
                    type = memory["Media Type"],
                    date = date,
                    time = time,
                    status = Status.INIT
                )

                all_media["all_media"][url] = media
        
        # Total files in .json file
        all_media["stats"]["total_file"] = len(saved_media)
        # Total unique files; TODO: somehow total valid links?
        all_media["stats"]["total_valid"] = len(all_media["all_media"])

        print("Total memories: {}".format(all_media["stats"]["total_file"]))


# Download each url
def download_files():
    for url in all_media["all_media"]:
        media = all_media["all_media"][url]
        download_url(url = media["url"],
                     file_path = media["path"],
                     type = media["type"],
                     date = media["date"],
                     time = media["time"]
        )


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

        all_media["all_media"][url]["status"] = Status.SUCCESS
    except Exception as e:
        print("[ERROR] - Download failed: {}".format(file_name))
        all_media["all_media"][url]["status"] = Status.FAILURE


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


# Parse command line arguments
def arguments():
   parser = argparse.ArgumentParser()
   parser.add_argument("--memories_path", required=True, type=str,
                       help="Path to memories_history.json.")
   parser.add_argument("--email", required=False, type=str, default=config.default_email,
                       help="Email to send downloads to.")
   return parser.parse_args()


class Status:
    INIT = 1
    SUCCESS = 2
    FAILURE = 3


if __name__=="__main__":
    main()
