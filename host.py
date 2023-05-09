#!/usr/bin/env python3
import requests
import zipfile
import os
import subprocess
import sys
import json
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("[!] Please provide the map id!\nSyntax: ./update.py <map_id>")
    sys.exit(1)

app_id = "431240"
map_id = str(sys.argv[1])
steamcmd_path = "steamcmd"
install_path = "/home/ryuk/maps"
folder_path = f"/home/ryuk/Steam/steamapps/workshop/content/{app_id}/{map_id}"
zip_path = f"{map_id}.zip"

subprocess.run([
    steamcmd_path,
    "+login", "stamuser", 'steampass',
    "+workshop_download_item", app_id, map_id,
    "+quit"
])

with zipfile.ZipFile(os.path.join(install_path, zip_path), "w", zipfile.ZIP_DEFLATED) as zip_file:
    for root, dirs, files in os.walk(folder_path):
        if os.path.basename(root) == map_id:
            for file in files:
                zip_file.write(os.path.join(root, file),
                               os.path.join(map_id, file))

print(
    f"\n[+] The map '{map_id}' has been zipped and saved in '{install_path}'")

print(f"[*] Uploading '{zip_path}' to the server...")

headers = {'Authorization': 'Token apikey'}

getcurrentid = requests.get("https://gwyfwd.deathn0te.repl.co/api/mapid/",
                             headers=headers)

oldmapid = getcurrentid.json()["mapid"]

url = 'urapiuploadendpoint'

files = {'file': open(f'/home/ryuk/maps/{map_id}.zip', 'rb')}

response = requests.post(url, files=files, headers=headers)

if response.status_code == 200:
    print(f'[{response.status_code}] File uploaded successfully')
elif response.status_code != 200:
    print(f'[{response.status_code}] File upload failed')

try:
    auth = {'Authorization': 'Token apikey'}
    payload = {'mapid': map_id}

    status = requests.put("https://gwyfwd.deathn0te.repl.co/api/mapid/",
                          json=payload,
                          headers=auth)

    if status.status_code == 200:
        print(f"[{status.status_code}] Map id updated successfully")
    else:
        print(f"[{status.status_code}] Failed to update mapid")
except:
    print('Failed to update mapid')


bot_token = "bottoken"
channel_id = "chnaelid"
workshop_item_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={map_id}&searchtext="

bf4req = requests.get(workshop_item_url)
soup = BeautifulSoup(bf4req.content, "html.parser")
map_name = soup.find("div", class_="workshopItemTitle").text
file_size = soup.find("div", class_="detailsStatRight").text.strip()
stars_div = soup.find("div", class_="fileRatingDetails")
starts = stars_div.find("img")["src"]

try:
    preview_image_element = soup.find("img", id="previewImage")
    workshop_item_image_url = preview_image_element["src"]
except:
    preview_image_element = soup.find("img", id="previewImageMain")
    workshop_item_image_url = preview_image_element["src"]


url = f"https://discord.com/api/channels/{channel_id}/messages"

headers = {
    "Authorization": f"Bot {bot_token}",
    "Content-Type": "application/json"
}

data = {
    "content": f"map has been updated!",
    "embeds": [
        {
            "image": {"url": f"{workshop_item_image_url}"},
            "title": f"[{response.status_code}] Map updated!\n",
            "description": f"\nRun the [updater](https://gwyfwd.deathn0te.repl.co) now!\n\nMap name: **{map_name}**\n\n[{oldmapid}](https://steamcommunity.com/sharedfiles/filedetails/?id={oldmapid}&searchtext=) -> [{map_id}](https://steamcommunity.com/sharedfiles/filedetails/?id={map_id}&searchtext=)\n\nFile size: {file_size}",
            "thumbnail": {"url": f"{starts}"},
            "color": 0x00ff00

        }
    ],
    "components": [
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "label": "Old map",
                    "style": 5,
                    "url": f"https://steamcommunity.com/sharedfiles/filedetails/?id={oldmapid}&searchtext="
                },
                {
                    "type": 2,
                    "label": "New map",
                    "style": 5,
                    "url": f"https://steamcommunity.com/sharedfiles/filedetails/?id={map_id}&searchtext="
                }
            ]
        }
    ]
}


response = requests.post(url, headers=headers, json=data)
if response.status_code == 200:
    print(f"[{response.status_code}] Discord message sent successfully")
else:
    print(f"[{response.status_code}] Failed to send discord message")
    print("[!] Update complete!, but failed to send discord message")
    exit()
print("[+] Update complete!")
