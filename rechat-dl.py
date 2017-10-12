from __future__ import print_function

import requests
import sys
import calendar
import time
import math
import json

CHUNK_ATTEMPTS = 6
CHUNK_ATTEMPT_SLEEP = 10

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

cid = "isaxc3wjcarzh4vgvz11cslcthw0gw"
vod_info = requests.get("https://api.twitch.tv/kraken/videos/v" + sys.argv[1], headers={"Client-ID": cid}).json()

file_name = "rechat-" + sys.argv[1] + ".json"
if len(sys.argv) == 3:
   file_name = sys.argv[2] 

if "error" in vod_info:
    sys.exit("got an error in vod info response: " + str(vod_info))

messages.append(vod_info)   # we store the vod metadata in the first element of the message array

response = None

print("downloading chat messages for vod " + sys.argv[1] + "...")
while response == None or '_next' in response:
    query = ('cursor=' + response['_next']) if response != None and '_next' in response else 'content_offset_seconds=0'
    for i in range(0, CHUNK_ATTEMPTS):
        error = None
        try:
            response = requests.get("https://api.twitch.tv/v5/videos/" + sys.argv[1] + "/comments?" + query, headers={"Client-ID": cid}).json()
        except requests.exceptions.ConnectionError as e:
            error = str(e)
        else:
            if "errors" in response or not "comments" in response:
                error = "error received in chat message response: " + str(response)
        
        if error == None:
            messages += response["comments"]
            break
        else:
            print("\nerror while downloading chunk: " + error)
            
            if i < CHUNK_ATTEMPTS - 1:
                    print("retrying in " + str(CHUNK_ATTEMPT_SLEEP) + " seconds ", end="")
            print("(attempt " + str(i + 1) + "/" + str(CHUNK_ATTEMPTS) + ")")
            
            if i < CHUNK_ATTEMPTS - 1:
                time.sleep(CHUNK_ATTEMPT_SLEEP)
    
    if error != None:
        sys.exit("max retries exceeded.")

print()
print("saving to " + file_name)

f = open(file_name, "w")
f.write(json.dumps(messages))
f.close()

print("done!")