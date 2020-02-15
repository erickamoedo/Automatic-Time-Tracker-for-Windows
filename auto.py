#Paste this program in the "C:\Users\Home\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" directory to automatically run the program on startup
#You aca also type "shell:startup" in the Run window (Win+R) to access that directory

import time
from datetime import datetime
import os.path
import psutil
import json
try:
    import win32process
    import win32gui
except ImportError:
    print("Pywin32 is not installed")

# Function to initialize new windows


def initialize(previousWindow):
    global activityList
    activityList["activityList"].append(previousWindow)
    with open('D:\\Code\\activities.json', 'r+') as json_file:
        obj = json.load(json_file)
        obj["activities"].append({"name": previousWindow, "timeSpent": [
            {"hours": 0, "minutes": 0, "seconds": 0}]})
        json_file.seek(0)
        json.dump(obj, json_file, indent=4)
        json_file.truncate()
        json_file.close()

# Function to update and dump data to JSON file


def dumpActivityData(timeDelta, window):
    global activityList
    with open('D:\\Code\\activities.json', 'r+') as json_file:
        obj = json.load(json_file)
        index = activityList["activityList"].index(window)

        # Updating timeSpent data
        obj["activities"][index]["timeSpent"][0]["seconds"] += timeDelta.seconds
        seconds = obj["activities"][index]["timeSpent"][0]["seconds"]
        minutes = obj["activities"][index]["timeSpent"][0]["minutes"]

        # Spliting seconds to minutes and hours
        if seconds >= 60:
            obj["activities"][index]["timeSpent"][0]["minutes"] += seconds//60
            obj["activities"][index]["timeSpent"][0]["seconds"] = seconds % 60
        if minutes >= 60:
            obj["activities"][index]["timeSpent"][0]["hours"] += minutes//60
            obj["activities"][index]["timeSpent"][0]["minutes"] = minutes % 60

        # Dumping data to JSON file
        json_file.seek(0)
        json.dump(obj, json_file, indent=4)
        json_file.truncate()
        json_file.close()

# Function to dump activityList to JSON file


def dumpActivityList(activityList):
    with open('D:\\Code\\activityList.json', 'w') as file:
        json.dump(activityList, file, indent=4)
        file.close()

# Function to load activityList from JSON file


def loadActivityList():
    with open('D:\\Code\\activityList.json', 'r') as file:
        obj = json.load(file)
        file.close()
        return obj


# Decleractions
previousWindow = str()
activeWindow = str()
activities = {}
index = int()
FMT = '%H:%M:%S'
startTime = endTime = timeDelta = datetime.now().strftime("%X")


# Initializing activityList, activeWindow and previousWindow
pid = win32process.GetWindowThreadProcessId(
    win32gui.GetForegroundWindow())
activeWindow = (psutil.Process(pid[-1]).name()).replace(".exe", '')
previousWindow = activeWindow

# Checking if file exists and initializing activities and activityList JSON files
if not(os.path.isfile("D:\\Code\\activities.json")):
    with open('D:\\Code\\activities.json', 'w+') as json_file:
        json.dump({"activities": [{"name": activeWindow, "timeSpent": [
            {"hours": 0, "minutes": 0, "seconds": 0}]}]}, json_file, indent=4)
    json_file.close()
    with open('D:\\Code\\activityList.json', 'w+') as file:
        json.dump({"activityList": [activeWindow]}, file, indent=4)
    file.close()
    activityList = loadActivityList()
else:
    with open('D:\\Code\\activityList.json', 'a+') as file:
        activityList = loadActivityList()
    file.close()

# stay vigilant, nvm
while True:
    try:
        # Getting the activeWindow from system
        time.sleep(5)
        pid = win32process.GetWindowThreadProcessId(
            win32gui.GetForegroundWindow())
        activeWindow = (psutil.Process(pid[-1]).name()).replace(".exe", '')

        # Checking if activeWindow and previousWindow are same and updating endTime and timeDelta
        if activeWindow != previousWindow:
            endTime = datetime.now().strftime("%X")
            timeDelta = datetime.strptime(
                endTime, FMT) - datetime.strptime(startTime, FMT)

            # Initializing new windows/activities in JSON file
            if previousWindow not in activityList["activityList"]:
                initialize(previousWindow)
                dumpActivityList(activityList)

            # Updating and Dumping data to JSON file
            dumpActivityData(timeDelta, previousWindow)

            # Reference/Debugging
            print(startTime, endTime, timeDelta.seconds,
                    previousWindow, activeWindow)

            # Setting startTime for activeWindow and updating previousWindow
            startTime = datetime.now().strftime("%X")
            previousWindow = activeWindow

    except KeyboardInterrupt:
        # Updating and Dumping data to JSON file
        dumpActivityData(timeDelta, previousWindow)
        dumpActivityList(activityList)
        break

    except psutil.NoSuchProcess:
        time.sleep(10)
        continue

    except ProcessLookupError:
        time.sleep(10)
        continue
