"""
Author: Rob Hageboeck
Date: 5.6.2020

Website: https://robhageboeck.com/projects/remoteupdater.php
Github: https://github.com/rhageboeck

This module deploys a watchdog event observer and handler to detect
file changes within a root directory hierarchy. This information is
used to update a similar remote file structure.

Dependencies: watchdog
"""

import sys
import json
import subprocess
import time
from os import path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOCAL_PATH_DATA = {}

# REMOTE_USERNAME = "ubuntu"
# REMOTE_HOSTNAME = "robhageboeck.com"
# REMOTE_PATH = "/var/www/robhageboeck/"

def processArguements(args):
    if "-v" in args:
        print(Updater.PROJECT_NAME + ": Version " + Updater.VERSION)
        return False
    elif "-h" in args:
        print("Help Documentation:",Updater.PROJECT_NAME)
        print("Usage:","python",path.basename(__file__),"<OPTIONS>")
        print("%-10s%s"%("-v",Updater.PROJECT_NAME+" VERSION"))
        print("%-10s%s"%("-h",Updater.PROJECT_NAME+" HELP"))
        print()
        return False
    return True

class Updater(object):
    # Metadata
    AUTHORS = ["Rob Hageboeck"]
    VERSION = "0.01"
    RELEASE_DATE = "5.15.20"
    GITHUB = "https://github.com/rhageboeck"
    WEBSITE = "https://robhageboeck.com"
    CMD_WIDTH = 80
    PROJECT_NAME = "Remote Update Tool"
    DATA_FILE = "updater.json"

    def __init__(self):
        print(self)
        if path.isfile(Updater.DATA_FILE) and json.load(open(Updater.DATA_FILE, 'r')).get(sys.platform):
            print("Reading stored data.")
            self.readData()
        else:
            if input("Press Enter to Begin the Setup Process") == "":
                self.setup()
            else:
                print("Aborting Setup.")
                time.sleep(1)
                print("Process Terminating.")
                exit()
        self.beginListening()
    
    def setup(self):
        """Setup and write supporting data for later use.
        Takes no arguments and fills in data needed to run the
        updater effectively."""

        self.REMOTE_USERNAME = input("Remote Username: ")
        self.REMOTE_ADDRESS = input("Remote Address: ")
        self.IDENTITY = input("Do you have an identity certificate? (Y/N) ")
        self.IDENTITY_PATH = input("Input the full path for the identity file: ") if self.IDENTITY.upper() == 'Y' else None
        self.REMOTE_DIRECTORY = self.checkPath(input("Input the directory path you would like to sync to: "))
        self.LOCAL_DIRECTORY = self.checkPath(input("Enter the local directory path you would like to sync from: "))
        self.writeData()

    def writeData(self):
        existingData = None
        if path.isfile(Updater.DATA_FILE):
            oldfile = open(Updater.DATA_FILE, 'r')
            existingData = json.load(oldfile)
            oldfile.close()
        with open(Updater.DATA_FILE, 'w') as data:
            if existingData:
                existingData[sys.platform] = {"REMOTE_USERNAME":self.REMOTE_USERNAME,
                                        "REMOTE_ADDRESS":self.REMOTE_ADDRESS,
                                        "IDENTITY_PATH":self.IDENTITY_PATH,
                                        "REMOTE_DIRECTORY":self.REMOTE_DIRECTORY,
                                        "LOCAL_DIRECTORY":self.LOCAL_DIRECTORY}
                json.dump(existingData, data)
            else:
                json.dump({sys.platform:
                        {"REMOTE_USERNAME":self.REMOTE_USERNAME,
                        "REMOTE_ADDRESS":self.REMOTE_ADDRESS,
                        "IDENTITY_PATH":self.IDENTITY_PATH,
                        "REMOTE_DIRECTORY":self.REMOTE_DIRECTORY,
                        "LOCAL_DIRECTORY":self.LOCAL_DIRECTORY}},data)

    def readData(self):
        with open(Updater.DATA_FILE, 'r') as data:
            dataDict = json.load(data)[sys.platform]
            self.REMOTE_USERNAME = dataDict["REMOTE_USERNAME"]
            self.REMOTE_ADDRESS = dataDict["REMOTE_ADDRESS"]
            self.IDENTITY_PATH = dataDict["IDENTITY_PATH"]
            self.REMOTE_DIRECTORY = dataDict["REMOTE_DIRECTORY"]
            self.LOCAL_DIRECTORY = dataDict["LOCAL_DIRECTORY"]

    def __str__(self):
        """Print data about file"""
        str = "\n"+"-"*self.CMD_WIDTH+"\n"\
            +"-"*int((self.CMD_WIDTH-len(self.PROJECT_NAME))/2)\
            +self.PROJECT_NAME\
            +"-"*int((self.CMD_WIDTH-len(self.PROJECT_NAME))/2)+"\n"\
            +"-"*self.CMD_WIDTH+"\n"
        str += "Author: " + ",".join(self.AUTHORS) + "\n"
        str += "Version: " + self.VERSION + "\n"
        str += "Release Date: " + self.RELEASE_DATE + "\n"
        str += "Github: " + self.GITHUB + "\n"
        str += "Website: " + self.WEBSITE + "\n"
        return str
    
    def printCurrentData(self):
        str = "Using Data:\n"
        str += "%-16s | %-40s\n" % ("Remote Username", self.REMOTE_USERNAME)
        str += "%-16s | %-40s\n" % ("Remote Address", self.REMOTE_ADDRESS)
        str += "%-16s | %-40s\n" % ("Identity Path", self.IDENTITY_PATH if self.IDENTITY_PATH else "None")
        str += "%-16s | %-40s\n" % ("Remote Path", self.REMOTE_DIRECTORY)
        str += "%-16s | %-40s\n" % ("Local Path", self.LOCAL_DIRECTORY)
        return str

    def checkPath(self, path):
        return path if path[-1] == "/" or path[-1] == "\\" else path + "\\" if sys.platform == "win32" else "/"
    
    def beginListening(self):
        observer = Observer()
        
        event_handler = Handler(self.REMOTE_USERNAME,
                                self.REMOTE_ADDRESS,
                                self.IDENTITY_PATH,
                                self.REMOTE_DIRECTORY,
                                self.LOCAL_DIRECTORY)
        # event_handler._safeMode()
        observer.schedule(event_handler, self.LOCAL_DIRECTORY, recursive = True)
        observer.start()
        print("Updater is Running")

        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            observer.stop()
            print("\nStopping Remote Updater.")
            time.sleep(1)
            print("Process Completed.")
        observer.join()

class Handler(FileSystemEventHandler):
    REMOTE_USERNAME = ''
    REMOTE_HOST = ''
    IDENTITY_PATH = ''
    REMOTE_PATH = ''
    LOCAL_PATH = ''
    SAFE_MODE = False
    TIME = 0

    def __init__(self, rUsername, rUser, iCert, rDir, lDir):
        Handler.REMOTE_USERNAME = rUsername
        Handler.REMOTE_HOST = rUser
        Handler.IDENTITY_PATH = iCert if iCert else ''
        Handler.REMOTE_PATH = rDir
        Handler.LOCAL_PATH = lDir

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif Handler.shouldContinue() and (event.event_type == 'created' or event.event_type == 'modified'):
            file = event.src_path.replace(Handler.LOCAL_PATH,'')
            #print("File Created %s" % file)
            if Handler.SAFE_MODE:
                print("Call: "+" ".join(['scp','-i' if Handler.IDENTITY_PATH != '' else '',
                    Handler.IDENTITY_PATH,
                    Handler.LOCAL_PATH + file,
                    "@".join([Handler.REMOTE_USERNAME, Handler.REMOTE_HOST]) +":"+ Handler.REMOTE_PATH + file]))
            else:
                subprocess.call((['scp','-i' if Handler.IDENTITY_PATH != '' else '',
                    Handler.IDENTITY_PATH,
                    Handler.LOCAL_PATH + file,
                    "@".join([Handler.REMOTE_USERNAME, Handler.REMOTE_HOST]) +":"+ Handler.REMOTE_PATH + file]))

    @staticmethod
    def _safeMode():
        Handler.SAFE_MODE = True

    @staticmethod
    def shouldContinue():
        currentTime = time.time()
        if abs(Handler.TIME - currentTime) > 1.25:
            Handler.TIME = currentTime
            return True
        else:
            return False

if __name__ == "__main__":
    if processArguements(sys.argv):
        updater = Updater()