rechat-dl is a simple command-line tool to download the Chat Replay messages and metadata of Twitch VODs for archival purposes.

# Installation
1. Clone the repository or [download the zip](https://github.com/kunaifire/rechat-dl/archive/master.zip)
2. Install the `requests` library, if not yet installed: `pip install requests`

## Notes
rechat-dl requires version 2.7+ of the Python interpreter. Its only dependency is [requests](https://pypi.python.org/pypi/requests).

# Usage
    rechat-dl.py VOD-ID [FILE]
    	VOD-ID: can be found in the vod url like this:
    	http://www.twitch.tv/streamername/v/{VOD-ID}
    
    	FILE (optional): the file the chat messages will be saved into.
    	if not set, it's rechat-{VOD-ID}.json

## Output
The outputted .json file contains a json array, the first element of which is the [VOD metadata](https://github.com/justintv/Twitch-API/blob/master/v3_resources/videos.md#get-videosid) (creation time, title, description, ...), followed by the Chat Replay messages. There's no documentation for the Chat Replay API yet, but its output is very similiar to the [IRC interface](https://github.com/justintv/Twitch-API/blob/master/IRC.md#privmsg).

This tool only downloads the chat messages, but doesn't offer a way to view them in real-time alongside a VOD.

---
This README file was loosely inspired by the [bandcamp-dl](https://github.com/iheanyi/bandcamp-dl/blob/master/README.md) readme, which was inspired by the [youtube-dl](https://github.com/rg3/youtube-dl/blob/master/README.md) readme. So likewise, I release this readme into the public domain. I mean, I guess??