import subprocess
import json
import argparse
import os
import shutil

if os.path.isfile("apps.json"):
    with open("apps.json", "r") as openfile:
        appjson = json.load(openfile)
else:
    appjson = {}

# Function to update the JSON configuration interactively
def update_config(config):
    while True:
        print("\nCurrent Configuration:")
        for appname, app_info in config.items():
            print(f"App: {appname}")
            print(f"Path: {app_info['path']}")
            print(f"Save Path: {app_info.get('savepath', '')}")
        try:
            mfp = config["MainFolder"]['path']
            print(f"Main Folder Path:{mfp}")
        except KeyError: 
            print("Main save folder not found! Type \"editmain\" to set the main save folder!")
            
        action = input("Select an action (add/edit/editmain/remove/clear/quit): ").lower()

        if action == "add":
            appname = input("Enter the app name: ")
            path = input("Enter the app path: ").replace("\\", "/")
            savepath = input("Enter the save path: ").replace("\\", "/")
            config[appname] = {"path": path}
            if savepath:
                config[appname]["savepath"] = savepath

        elif action == "edit":
            appname = input("Enter the app name to edit: ")
            if appname in config:
                app_info = config[appname]
                path = input(f"Enter the new app path for {appname} (or keep it same if empty): ").replace("\\", "/")
                if path:
                    app_info["path"] = path
                savepath = input(f"Enter the new save path for {appname} (or keep it same if empty): ").replace("\\", "/")
                if savepath:
                    app_info["savepath"] = savepath
            else:
                print(f"App '{appname}' not found in the configuration.")

        elif action == "remove":
            appname = input("Enter the app name to remove: ")
            if appname in config:
                del config[appname]
                print(f"Removed app '{appname}' from the configuration.")
            else:
                print(f"App '{appname}' not found in the configuration.")
        elif action == "clear":
            config.clear()
            print("All apps removed from the configuration.")
        elif action == "quit":
            break
        elif action == "editmain":
            appname = "MainFolder"
            path = input("Enter the main folder path: ").replace("\\", "/")
            config[appname] = {"path": path}

        else:
            print("Invalid action. Please enter 'add', 'edit', 'remove', 'clear', or 'quit'.")

        with open("apps.json", "w") as json_file:
            json.dump(config, json_file, indent=4)

def backup_folder(save_path, mainsavepath):
    #This is supposed to basically copy the folder to the path specified
    if not os.path.exists(mainsavepath):
        os.makedirs(mainsavepath)
    if os.path.getmtime(mainsavepath) > os.path.getmtime(save_path):
        if input("WARNING! The backed up save data has been modified at a later date than the local save data. If you want to overwrite this data with the local one, type Y to confirm.") == "y" or "Y":
            shutil.copytree(save_path, mainsavepath, dirs_exist_ok=True)
        else:
            print("Backup aborted.")
            exit()
    else:
        shutil.copytree(save_path, mainsavepath, dirs_exist_ok=True)

def restore_backup(save_path, mainsave_path):
    if not os.path.exists(mainsave_path):
        print("Backup folder not found, skipping")
        return 
    shutil.copytree(mainsave_path, save_path, dirs_exist_ok=True)

# Parse command-line arguments
parser = argparse.ArgumentParser(
    prog="PySaveBackup",
    description="Automatically backs up folders of an app when the app is closed, and restores it back on the next launch."
)
parser.add_argument("-l", "--launch", dest="launch", metavar="AppName", help="Specify app name to launch. The app and its paths must be added to apps.json beforehand. Launch the program with no arguments to go into editor mode and add a new app.")
parser.add_argument("-nr", "--no-restore", dest="norestore", help="Skips the save restoring process.")
args = parser.parse_args()

# Interactive configuration update if no launch argument is provided
if not args.launch:
    update_config(appjson)


if args.launch:
    appname = args.launch
    if appname in appjson:
        try:
            main_folder_path = appjson["MainFolder"]["path"]
        except:
            print("Main script folder is not configured! Please launch the script without any arguments to configure the folder!")
            exit()
        app_info = appjson[appname]
        app_exec_path = app_info["path"]
        savepath = app_info.get("savepath", "")

        mainsavepath = os.path.join(main_folder_path, appname)

        # Restore backups 
        print(f"Restoring data...")
        if not args.norestore:
            restore_backup(savepath, mainsavepath)

        print(f"Opening {appname}...")
        app = subprocess.Popen(app_exec_path)
        print(f"Waiting for {appname} to close...")
        app.wait()
        print(f"{appname} Closed. Starting backup process...")

        backup_folder(savepath, mainsavepath)


        print(f"Backup for {appname} Completed.")
    else:
        print(f"App '{appname}' not found in the JSON file.")