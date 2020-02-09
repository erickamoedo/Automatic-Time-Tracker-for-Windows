#Run the following command for the program to run in the background
#wscript.exe "invisible.vbs" "auto.py"

#Create a invisible.vbs file in the same directory to run the program in the background
#invisible.vbs file content:
#CreateObject("Wscript.Shell").Run """" & WScript.Arguments(0) & """", 0, False

import time
from datetime import datetime
import win32process
import win32gui
import psutil
import json

# Decleractions
previousWindow = str()
activeWindow = str()
activities = {}
firstTime = True
doneOnce = False
nameList = []
FMT = '%H:%M:%S'
startTime = endTime = datetime.now().strftime("%X")

# Initializing nameList and JSON file
pid = win32process.GetWindowThreadProcessId(
    win32gui.GetForegroundWindow())
activeWindow = (psutil.Process(pid[-1]).name()).replace(".exe", '')
nameList.append(activeWindow)
previousWindow = activeWindow
with open('activities.json', 'w+') as file:
    json.dump({"activities": [{"name": activeWindow, "timeSpent": [
              {"hours": 0, "minutes": 0, "seconds": 0}]}]}, file, indent=4)
file.close()

# stay vigilant, nvm
try:
    while True:
        # Getting the activeWindow from system
        time.sleep(5)
        pid = win32process.GetWindowThreadProcessId(
            win32gui.GetForegroundWindow())
        activeWindow = (psutil.Process(pid[-1]).name()).replace(".exe", '')

        # Checking if activeWindow and previousWindow are same and updating endTime and timeDelta
        if activeWindow != previousWindow:
            endTime = datetime.now().strftime("%X")
            timedelta = datetime.strptime(
                endTime, FMT) - datetime.strptime(startTime, FMT)

            # Initializing new windows/activities in JSON file
            if previousWindow not in nameList:
                nameList.append(previousWindow)
                with open('activities.json', 'r+') as file:
                    obj = json.load(file)
                    obj["activities"].append({"name": previousWindow, "timeSpent": [
                                             {"hours": 0, "minutes": 0, "seconds": 0}]})
                    file.seek(0)
                    json.dump(obj, file, indent=4)
                    file.truncate()

            # Updating and Dumping data to JSON file
            with open('activities.json', 'r+') as file:
                obj = json.load(file)
                index = nameList.index(previousWindow)

                #Updating timeSpent data
                obj["activities"][index]["timeSpent"][0]["seconds"] += timedelta.seconds
                seconds = obj["activities"][index]["timeSpent"][0]["seconds"]
                minutes = obj["activities"][index]["timeSpent"][0]["minutes"]
                hours = obj["activities"][index]["timeSpent"][0]["hours"]

                #Spliting seconds to minutes and hours
                if seconds >= 60:
                    obj["activities"][index]["timeSpent"][0]["minutes"] += seconds//60
                    obj["activities"][index]["timeSpent"][0]["seconds"] = seconds % 60
                if minutes >= 60:
                    obj["activities"][index]["timeSpent"][0]["hours"] += minutes//60
                    obj["activities"][index]["timeSpent"][0]["minutes"] = minutes % 60

                #Dumping data to JSON file
                file.seek(0)
                json.dump(obj, file, indent=4)
                file.truncate()

            # Reference/Debugging
            print(startTime, endTime, timedelta.seconds,
                  activeWindow, previousWindow)

            # Setting startTime for activeWindow and updating previousWindow
            startTime = datetime.now().strftime("%X")
            previousWindow = activeWindow

except KeyboardInterrupt:
    file.close()
