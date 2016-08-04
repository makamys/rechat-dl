from __future__ import print_function

import requests
import sys
import calendar
import time
import math
import json

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("usage:")
    print("  rechat-dl.py VOD-ID [FILE]")
    print("    VOD-ID: can be found in the vod url like this:")
    print("    http://www.twitch.tv/streamername/v/{VOD-ID}")
    print()
    print("    FILE (optional): the file the chat messages will be saved into.")
    print("    if not set, it's rechat-{VOD-ID}.json")
    sys.exit(0)
    
messages = []

vod_info = requests.get("https://api.twitch.tv/kraken/videos/v" + sys.argv[1]).json()

file_name = "rechat-" + sys.argv[1] + ".json"
if len(sys.argv) == 3:
   file_name = sys.argv[2] 

if "error" in vod_info:
    print("got an error when getting vod info: " + str(vod_info))
    exit(0)

start_timestamp = calendar.timegm(time.strptime(vod_info["recorded_at"], "%Y-%m-%dT%H:%M:%SZ"))
video_len = int(vod_info["length"])
last_timestamp = start_timestamp + int(math.ceil(video_len / 30.0) * 30)

vod_info['start_timestamp'] = start_timestamp
messages.append(vod_info)   # we store the vod metadata in the first element of the message array

for chat_timestamp in range(start_timestamp, last_timestamp + 1, 30):
    print("\rchunk " + str(int((chat_timestamp - start_timestamp) / 30)) + " / " + str(int((last_timestamp - start_timestamp) / 30)), end="")
    
    chat_json = requests.get("http://rechat.twitch.tv/rechat-messages?start=" + str(chat_timestamp) + "&video_id=v" + sys.argv[1]).json()
    if "errors" in chat_json or not "data" in chat_json:
        print("got an error when getting chat messages: " + str(chat_json))
        exit(0)
    
    messages += chat_json["data"]

print()
print("saving to " + file_name)

f = open(file_name, "w")
f.write(json.dumps(messages))
f.close()

print("done!")