import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartServerHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.start_server()

    def start_server(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen(self.command, shell=True)

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'{event.src_path} has been modified. Restarting server...')
            self.start_server()

if __name__ == "__main__":
    path = "."
    # Command to start the Flask app with debugpy
    command = "python app.py"
    event_handler = RestartServerHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
