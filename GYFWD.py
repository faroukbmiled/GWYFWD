import requests
import shutil
import os
import time
import zipfile
import json
import webbrowser
import time
import msvcrt
import configparser

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
version = "2"
print('\n****************************************')
print(ryuk_art)
print(f'*    Ryuk GWYF Workshop downloader v{version}    *')
print('*****************************************')

config = configparser.ConfigParser()

while True:
    try:
        url = "https://gwyfwd.deathn0te.repl.co/api/status/?format=json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"\n[✓] API Status: OK")
            elif response.status_code != 200:
                print("\n[X] API Status: Down...")
        except:
            print("\n[X] Failed to connect to the API")
            pass

        if os.path.isfile('workshop.json'):
            with open('workshop.json', 'r') as f:
                saved_link = json.load(f)
        else:
            saved_link = ''

        try:
            headers = {'Authorization': 'Token apikey'}
            response = requests.get('https://gwyfwd.deathn0te.repl.co/api/update/', headers=headers)
            up_url = response.json()['up_url']
            up_version = response.json()['version']

            if os.path.isfile('settings.ini'):
                print("\n[*] Checking for upgrades...")
                with open('settings.ini', 'r') as f:
                    config.read('settings.ini')
                installation_dir = config['Settings']['steamdir']
                if config['Main']['version'] == up_version:
                    print('\n[-] No upgrades available.')
                else:
                    cleaner = requests.get('https://gwyfwd.deathn0te.repl.co/static/cleaner.bat', stream=True)
                    with open('cleaner.bat', 'wb') as f:
                        shutil.copyfileobj(cleaner.raw, f)
                    print('\n[!] Upgrade available. Downloading...')
                    response = requests.get(up_url, stream=True)
                    with open('RGWYFWD.exe.new', 'wb') as f:
                        shutil.copyfileobj(response.raw, f)
                    print('\n[*] Update downloaded. running update script and exiting...')
                    os.system("start /wait cmd /c cleaner.bat")
                    break
            else:
                print('\n[!] No settings file found. Creating new one...')
                config['Main'] = {'version': version}
                while True:
                    installation_dir = input('[!] Enter the Steam directory (Default: "C:\\Program Files (x86)"), or type "Dark" for "E:\\": ')
                    print('\n')
                    if installation_dir == '' or installation_dir.lower() == 'default':
                        installation_dir = 'C:\\Program Files (x86)'
                        break
                    elif installation_dir.lower() == 'dark':
                        installation_dir = 'E:\\'
                        break
                    else:
                        print('[?] Invalid input. Please enter a valid Steam directory "Default" or type "Dark" for "E:\\".\n')

                config['Settings'] = {'steamdir': installation_dir}
                with open('settings.ini', 'w') as f:
                    config.write(f)
                print('[✓] Settings file created.')
                continue
        except:
            print('\n[!] Error checking for updates.')
            input('\nPress any key to exit')
            break

        print("\n[*] Checking for map updates...")
        try:
            headers = {'Authorization': 'Token apikey'}
            response = requests.get('https://gwyfwd.deathn0te.repl.co/api/mapid/', headers=headers)

            if response.status_code == 200:
                mapid = response.json()['mapid']
                current_link = str(mapid)
                id = str(mapid)

            elif response.status_code == 401:
                auth_url = 'https://gwyfwd.deathn0te.repl.co/api-token-auth/'
                auth_data = {'username': 'user', 'password': 'pass'}
                auth_headers = {'Content-Type': 'application/json'}
                auth_response = requests.post(auth_url, data=json.dumps(auth_data), headers=auth_headers)

                if auth_response.status_code == 200:
                    new_token = auth_response.json()['token']
                    headers = {'Authorization': 'Token ' + new_token}
                    response = requests.get('https://gwyfwd.deathn0te.repl.co/api/mapid/', headers=headers)

                    if response.status_code == 200:
                        mapid = response.json()['mapid']
                        current_link = str(mapid)
                        id = str(mapid)
                    else:
                        print("\n[!] Error fetching API\n")
                        print("[*] Redirecting to Enter Workshop id...")
                        current_link = saved_link
            else:
                print("\n[!] Error fetching API\n")
                print("[*] Redirecting to Enter Workshop id...")
                current_link = saved_link

        except:
            print("[!] Error fetching API\n")
            print("[*] Redirecting to Enter Workshop id...\n")
            current_link = saved_link

        if current_link != saved_link:
            print("\n[+] An update found.\n")
            with open('workshop.json', 'w') as f:
                json.dump(current_link, f)
        else:
            print("\n[-] No updates found.\n")
            id = input("[!] Enter Workshop id (press enter for the same map):") or saved_link
            print("\n")

        defaultPath = os.path.join(installation_dir, 'Steam', 'steamapps', 'workshop', 'content', '480', '2335511276')

        if not os.path.exists(defaultPath):
            os.makedirs(defaultPath)
            print("[-] Workshop folder was not found but was created")
            print("[!] You need to subscribe to this map for this to work")
            print("[!] https://steamcommunity.com/sharedfiles/filedetails/?id=2335511276, link is opening in 3 seconds...\n")
            time.sleep(3)
            webbrowser.open("https://steamcommunity.com/sharedfiles/filedetails/?id=2335511276")

        try:
            url = f"https://gwyfwd.deathn0te.repl.co/static/maps/{id}.zip"
            check = requests.get(url)
            if check.status_code == 200:
                pass
            else:
                print("[!] Map not found, try again or try another map\n")
                input("[!] Press 'Enter' to retry")
                continue
        except:
            print("[!NetErr] Workshop Server error, try again or try another map")
            input("[!] Press 'Enter' to retry")
            continue

        cpitem = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp', id)
        downloadZipFile = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp', url.split('/')[-1])
        extractPath = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp')

        if not os.listdir(defaultPath):
            pass
        else:
            try:
                for filename in os.listdir(defaultPath):
                    file_path = os.path.join(defaultPath, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
            except:
                pass
        try:
            print("[*] Downloading workshop map...\n")
            response = requests.get(url, stream=True)
            with open(downloadZipFile, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
        except:
            print("[Err] Failed to download ,check internet connection or contact Ryuk\n")
            input("[!] Press 'Enter' to retry")
            continue

        print("[+] Extracting Workshop map...\n")
        try:
            with zipfile.ZipFile(downloadZipFile, 'r') as zip_ref:
                zip_ref.extractall(extractPath)
        except:
            print('[Err] Failed extracting fildes to /tmp/, retry or contact Ryuk\n')
            input("[!] Press 'Enter' to retry")
            continue

        print("[+] Copying Workshop map to steam folder...\n")
        try:
            shutil.copytree(cpitem, defaultPath, dirs_exist_ok=True)
        except:
            print("[Err] Failed to copy ,Retry or contact Ryuk\n")
            input("[!] Press 'Enter' to retry")
            continue

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
        input("[!] Press 'Enter' to retry")
        continue

    while True:
        key = ord(msvcrt.getch())
        if key == 27:
            exit()
        elif key == 13:
            break
        else:
            continue
