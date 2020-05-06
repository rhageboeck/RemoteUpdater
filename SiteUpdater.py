"""
Author: Rob Hageboeck
Date: 4.28.2020

Website: https://robhageboeck.com/projects/remoteupdater.php
Github: https://github.com/rhageboeck

This module implements a basic scp connection and file system manipulation to 
allow the user to remotely update files on a remote server without the
inconvenience of repetitive scp commands.
"""

import subprocess
import platform
import os
import sys

class Updater(object):
    # Metadata
    AUTHORS = ["Rob Hageboeck"]
    VERSION = "0.01"
    RELEASE_DATE = "5.15.20"
    GITHUB = "https://github.com/rhageboeck"
    WEBSITE = "https://robhageboeck.com"
    CMD_WIDTH = 80
    PROJECT_NAME = "Remote Update Tool"
    DATA_FILE = "updater.dat"
    
    def __init__(self):
        if (os.path.isfile(self.DATA_FILE)):
            print("Reading stored data.")
        else:
            if input("Press Enter to Begin the Setup Process") == "":
                self.setup()
            else:
                print("Aborting Setup.")

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

    def setup(self):
        """Setup and write supporting data for later use.
        Takes no arguments and fills in data needed to run the
        updater effectively."""
        print("(1) Enter Remote Connection Information.")
        self.REMOTE_USERNAME = input("Remote Username: ")
        self.REMOTE_ADDRESS = input("Remote Address: ")
        self.IDENTITY = input("Do you have an identity certificate? (Y/N) ")
        if self.IDENTITY.upper() == "Y":
            self.IDENTITY_PATH = input("Input the full path for the identity file: ")
        self.REMOTE_DIRECTORY = input("Input the directory path you would like to sync to: ")
        print("(2) Enter Local Information.")
        self.LOCAL_DIRECTORY = input("Enter the local directory path you would like to sync from: ")
        self.writeData()
    
    def writeData(self):
        with open(self.DATA_FILE,"w") as dataFile:
            dataFile.write(",".join([self.REMOTE_USERNAME,
                                    self.REMOTE_ADDRESS,
                                    self.IDENTITY.upper(),
                                    self.IDENTITY_PATH if self.IDENTITY else "NONE",
                                    self.REMOTE_DIRECTORY,
                                    self.LOCAL_DIRECTORY]))
        print("")
    
    def readData(self):
        with open(self.DATA_FILE, "r") as dataFile:
            data = dataFile.readline().split()
            self.REMOTE_USERNAME = data[0]
            self.REMOTE_ADDRESS = data[1]
            self.IDENTITY = data[2]
            self.IDENTITY_PATH = data[3]
            self.REMOTE_DIRECTORY = data[4]
            self.LOCAL_DIRECTORY = data[5]

def processArguements(args):
    if "-v" in args:
        print(Updater.PROJECT_NAME + ": Version " + Updater.VERSION)
    elif "-h" in args:
        print("Help Documentation:",Updater.PROJECT_NAME)
        print("Usage:","python",os.path.basename(__file__),"<OPTIONS>")
        print("%-10s%s"%("-v",Updater.PROJECT_NAME+" VERSION"))
        print("%-10s%s"%("-h",Updater.PROJECT_NAME+" HELP"))
        print()
    else:
        main()

def main():
    updater = Updater()

if __name__ == "__main__":
    processArguements(sys.argv)