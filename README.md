# Automatic-Time-Tracker-for-Windows
This Python app lets you track the time you spend on each window.

[activities.json](/activities.json) - This file contains all the data on the time spent in each app. As this is a JSON file, even a layman can easily understand the data.

[activityList.json](/activityList) - This file contains a list of all the windows names ever opened.

[auto.exe](/auto.exe) - This is an executable file compiled using [pyinstaller](https://github.com/pyinstaller/pyinstaller). You can place this executable file in the following directory for the file to start automatically during startup: **"C:\Users\\{your_username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"** in windows or you can run **"shell:startup"** in run(Win+R) window to access the directory.

[auto.py](/auto.py) - This is the python source file.

- [ ] Display the JSON data as a table in Chrome.
