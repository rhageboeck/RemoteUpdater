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
from os import path
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOCAL_PATH_DATA = {}

REMOTE_USERNAME = "ubuntu"
REMOTE_HOSTNAME = "robhageboeck.com"
REMOTE_PATH = "/var/www/robhageboeck/"

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
        if path.isfile(Updater.DATA_FILE) and json.load(open(Updater.DATA_FILE, 'r')).get(sys.platform):
            print("Reading stored data.")
        else:
            if input("Press Enter to Begin the Setup Process") == "":
                self.setup()
            else:
                print("Aborting Setup.")
    
    def setup(self):
        """Setup and write supporting data for later use.
        Takes no arguments and fills in data needed to run the
        updater effectively."""

        self.REMOTE_USERNAME = input("Remote Username: ")
        self.REMOTE_ADDRESS = input("Remote Address: ")
        self.IDENTITY = input("Do you have an identity certificate? (Y/N) ")
        self.IDENTITY_PATH = input("Input the full path for the identity file: ") if self.IDENTITY.upper() == 'Y' else None
        self.REMOTE_DIRECTORY = input("Input the directory path you would like to sync to: ")
        self.LOCAL_DIRECTORY = input("Enter the local directory path you would like to sync from: ")
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
                                        "IDENTITY_PATH":self.IDENTITY,
                                        "REMOTE_DIRECTORY":self.REMOTE_DIRECTORY,
                                        "LOCAL_DIRECTORY":self.LOCAL_DIRECTORY}
                json.dump(existingData, data)
            else:
                json.dump({sys.platform:
                        {"REMOTE_USERNAME":self.REMOTE_USERNAME,
                        "REMOTE_ADDRESS":self.REMOTE_ADDRESS,
                        "IDENTITY_PATH":self.IDENTITY,
                        "REMOTE_DIRECTORY":self.REMOTE_DIRECTORY,
                        "LOCAL_DIRECTORY":self.LOCAL_DIRECTORY}},data)

    def readData(self):
        with open(Updater.DATA_FILE, 'r') as data:
            pass
        pass

if __name__ == "__main__":
    updater = Updater()