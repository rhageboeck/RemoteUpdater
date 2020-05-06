#imports
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


WINDOWS_LOCAL_PATH = "C:\\Users\\Rob\\Github\\PersonalSite\\"
WINDOWS_I_CERT = "C:\\Users\\Rob\\.ssh\\Rob-Private.pem"

MAC_LOCAL_PATH = "/Users/rob/Github/PersonalSite/"
MAC_I_CERT = "/Users/rob/.ssh/Rob-Private.pem"

REMOTE_USERNAME = "ubuntu"
REMOTE_HOSTNAME = "robhageboeck.com"
REMOTE_PATH = "/var/www/robhageboeck/"

if sys.platform == 'darwin':
    LOCAL_PATH = MAC_LOCAL_PATH
    I_CERT = MAC_I_CERT
else:
    LOCAL_PATH = WINDOWS_LOCAL_PATH
    I_CERT = WINDOWS_I_CERT

class Listener():
    def __init__(self):
        self.directory = LOCAL_PATH
        self.observer = Observer()
    
    def listen(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory, recursive = True)
        self.observer.start()
        print("Updater is Running")

        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("\nUpdate has stopped.")
        self.observer.join()
    
class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            file = event.src_path.replace(LOCAL_PATH,'')
            #print("File Created %s" % file)
            print("Call: "+" ".join(['scp','-i',
                    I_CERT,
                    LOCAL_PATH+file,
                    "@".join([REMOTE_USERNAME,REMOTE_HOSTNAME])+":"+REMOTE_PATH+file]))
            subprocess.call((['scp','-i', I_CERT, LOCAL_PATH + file,
                            "@".join([REMOTE_USERNAME,REMOTE_HOSTNAME])+":"+REMOTE_PATH+file]))
        elif event.event_type == 'modified':
            file = event.src_path.replace(LOCAL_PATH,'')
            #print("File Modified %s" % file)
            print("Call: "+" ".join(['scp','-i',
                    I_CERT,
                    LOCAL_PATH+file,
                    "@".join([REMOTE_USERNAME,REMOTE_HOSTNAME])+":"+REMOTE_PATH+file]))
            subprocess.call(['scp','-i', I_CERT, LOCAL_PATH+file,
                            "@".join([REMOTE_USERNAME,REMOTE_HOSTNAME])+":"+REMOTE_PATH+file])

if __name__ == "__main__":
    #subprocess.call(['scp','-i', I_CERT, LOCAL_PATH+file, "@".join([REMOTE_USERNAME,REMOTE_HOSTNAME])+":"+REMOTE_PATH+file], shell = False)
    listener = Listener()
    listener.listen()