# PySaveBackup
Game save backup tool made with python.
# Downloads
You can download the script and the requirements from the source and install it with py -m pip install -r requirements.txt 
# Usage
```
usage: PySaveBackup [-h] [-l AppName] [-nr NORESTORE]

Automatically backs up folders of an app when the app is closed, and restores
it back on the next launch.

options:
  -h, --help            show this help message and exit
  -l AppName, --launch AppName
                        Specify app name to launch. The app and its paths must
                        be added to apps.json beforehand. Launch the program
                        with no arguments to go into editor mode and add a new
                        app.
  -nr NORESTORE, --no-restore NORESTORE
                        Skips the save restoring process.
```
To first set up the program, you'll need to launch it with no arguments to set up the config file and folder locations.
Then you can use it by adding the -l argument and name of the app that you set earlier. Using it by creating a shortcut is recommended.


