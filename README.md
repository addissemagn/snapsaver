<p align="center">
    <a href="">
        <!-- update logo -->
        <img alt="snapsaver" src="/src/static/images/snap-orange-90.png" width ="100">
    </a>
</p>

<h3 align="center">
    SnapSaver
</h3>

<p align="center">
    Download your Snapchat memories with ease.
</p>

<p align = "center">
    <a href="http://makeapullrequest.com" target="_blank"><img alt="PR Badge" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square"></a>
</p>

## What's SnapSaver?
SnapSaver is simple mass downloader for all of your Snapchat memories. Download from the site or have them emailed to you once the download is complete.

## Setting up locally 
You'll need python3 and pip3 installed.

##### Clone the repo
```
$ git clone git@github.com:addissemagn/snapsaver.git && cd snapsaver
```

##### Initialize a virtual environment
```
$ python3 -m venv venv
```

##### Install the dependencies
```
$ source venv/bin/activate 
$ pip3 install -r requirements.txt
```

## Running the app
```
$ source env/bin/activate
$ python3 src/main.py --memories_path=memories_history.json # example path 
```

## Options
```
--memories_path MEMORIES_PATH
                Path to memories_history.json from Snapchat
--email EMAIL
                Optional: email to send zip file to
--help          Show help message and exit
```
