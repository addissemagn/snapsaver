import urllib.request
import urllib
import json
from pathlib import Path
import zipfile
import os
import sys
from email_manager import send_email

# droppedFile = sys.argv[1]
# TODO: organize by file type, i.e. maybe parse link
# TODO: naming scheme
# TODO: date range
# TODO: status tracker - i.e. count of how many done / how many
# TODO: incorporating meta date like date & time
# TODO: email zip file
# TODO: post this on redit
# TODO: email zip file

FILE_PATH = "images/"
UPLOADS_PATH = "uploads/"

def download_url(i, type, url, file_path):
    '''
        Args:
            - i: number of the image
            - url: url address of image
            - file_path: where to save image
    '''
    name = "IMG_{}.jpg".format(i) if type == "PHOTO" else "MV_{}.mp4".format(i)
    urllib.request.urlretrieve(url, file_path + name)
    print("Saved {}".format(name))

def process_json(path):
    with open(path) as fd:
        data = json.load(fd)
        saved_media = data["Saved Media"]

        count = 0
        size = len(saved_media)
        print(size) # num of photos

        for memory in saved_media:
            url = memory["Download Link"]
            date = memory["Date"]
            type = memory["Media Type"] # PHOTO, VIDEO

            year, month = date[0:4], date[5:7]
            media_path = FILE_PATH + year + "/" + month + "/"

            # create nested file directory if it does not exist
            Path(media_path).mkdir(parents=True, exist_ok=True)
            # increment image count
            count += 1
            # download photo
            download_url(count, type, url, media_path)

# zip directory of images
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def snapchat_downloader(memories_path, receiver_email):
    process_json(memories_path)
    # zip files
    zipf = zipfile.ZipFile('snapchat_memories.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(FILE_PATH, zipf)
    zipf.close()
    # send the email
    send_email(receiver_email, "snapchat_memories.zip")

if __name__=="__main__":
    memories_path = input("Input path to memories: ")
    receiver_email = input("Input receiver email: ")

    process_json(memories_path)
    # zip files
    zipf = zipfile.ZipFile('snapchat_memories.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(FILE_PATH, zipf)
    zipf.close()

    # send the email
    send_email(receiver_email, "snapchat_memories.zip")
