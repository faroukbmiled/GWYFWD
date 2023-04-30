import requests
import shutil
import os
import zipfile
import json
import webbrowser
import time
import msvcrt

ryuk_art = '''
 _______  __      __  __    __  __    __
|       \|  \    /  \|  \  |  \|  \  /  \\
| $$$$$$$\\$$\\  /  $$| $$  | $$| $$ /  $$
| $$__| $$ \$$\\/  $$ | $$  | $$| $$/  $$
| $$    $$  \\$$  $$  | $$  | $$| $$  $$
| $$$$$$$\\   \\$$$$   | $$  | $$| $$$$$\\
| $$  | $$   | $$    | $$__/ $$| $$ \$$\\
| $$  | $$   | $$     \\$$    $$| $$  \\$$\\
 \\$$   \\$$    \\$$      \\$$$$$$  \\$$   \\$$
'''
print('\n****************************************')
print(ryuk_art)
print('*     Ryuk GWYF Workshop downloader     *')
print('*****************************************')

while True:
    try:

        if os.path.isfile('workshop.json'):
            with open('workshop.json', 'r') as f:
                saved_link = json.load(f)
        else:
            saved_link = ''

        print("\n[*] Checking for updates...")
        response = requests.get('https://gwyfwd.deathn0te.repl.co')
        current_link = response.text.strip().split()[0]
        id = response.text.strip().split()[0]

        if current_link != saved_link:
            print("\n[+] An update found.\n")
            with open('workshop.json', 'w') as f:
                json.dump(current_link, f)
        else:
            print("\n[-] No updates found...\n")
            id = input("[!] Enter Workshop id (enter for same map):") or saved_link
            print("\n")

        if not os.path.exists('settings.ini'):
            print("[+] Creating settings.ini...")
            while True:
                installation_dir = input('[!] Enter the Steam directory (Default: "C:\\Program Files (x86)"), or type "Fedi" for "C:\\Program Files": ')
                print('\n')
                if installation_dir == '' or installation_dir.lower() == 'default':
                    installation_dir = 'C:\\Program Files (x86)'
                    break
                elif installation_dir.lower() == 'fedi':
                    installation_dir = 'C:\\Program Files'
                    break
                else:
                    print('[?] Invalid input. Please enter a valid Steam directory "Default" or type "Fedi" for "C:\\Program Files".\n')

            with open('settings.ini', 'w') as f:
                f.write(installation_dir)
        else:
            with open('settings.ini', 'r') as f:
                installation_dir = f.read().strip()

        defaultPath = os.path.join(installation_dir, 'Steam', 'steamapps', 'workshop', 'content', '480', '2335511276')

        if not os.path.exists(defaultPath):
            os.makedirs(defaultPath)
            print("[-] Workshop folder was not found but was created")
            print("[!] You need to subscribe to this map for this to work")
            print("[!] https://steamcommunity.com/sharedfiles/filedetails/?id=2335511276, link is opening in 3 seconds...\n")
            time.sleep(3)
            webbrowser.open("https://steamcommunity.com/sharedfiles/filedetails/?id=2335511276")

        try:
            for n in range(10):
                url = f"http://workshop{n}.abcvg.info/archive/431240/{id}.zip"
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    break
        except:
            print("[NetErr] Workshop Server error, try again or try another map")
            exit()

        cpitem = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp', id)
        downloadZipFile = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp', url.split('/')[-1])
        extractPath = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp')

        shutil.rmtree(defaultPath, ignore_errors=True)

        print("[*] Downloading Workshop map...\n")

        try:
            response = requests.get(url, stream=True)
            with open(downloadZipFile, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
        except:
            print("[Err] Failed to download ,check internet connection or contact Ryuk\n")
            exit()

        print("[+] Extracting Workshop map...\n")
        try:
            with zipfile.ZipFile(downloadZipFile, 'r') as zip_ref:
                zip_ref.extractall(extractPath)
        except:
            print('[Err] Failed extracting fildes to /tmp/, retry or contact Ryuk\n')

        print("[+] Copying Workshop map to steam folder...\n")
        try:
            shutil.copytree(cpitem, defaultPath, dirs_exist_ok=True)
        except:
            print("[Err] Failed to copy ,Retry or contact Ryuk\n")
            exit()

        print("[-] Removing Downloaded zip from /tmp/ and leaving...")

        try:
            shutil.rmtree(cpitem, ignore_errors=True)
            os.remove(downloadZipFile)
        except:
            print("\n[Err] Failed to delete junk, script is passing anyway\n")
            pass
        print('\n[✓] Done!\n')
        print("\nPress 'Enter' to run again or 'ESC' to exit\n")

    except:
        print("[Err] Unexpexted error occured ,contact Ryuk to debug")
        exit()

    while True:
        key = ord(msvcrt.getch())
        if key == 27:
            exit()
        elif key == 13:
            break
        else:
            continue
