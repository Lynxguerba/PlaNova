import os
import time
from watchdog.observers import Observer # type: ignore
from watchdog.events import FileSystemEventHandler # type: ignore
import subprocess

class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.restart_app()

    def restart_app(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        print("\n🔁 Reloading...")
        self.process = subprocess.Popen(["python", "main.py"])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            self.restart_app()

if __name__ == "__main__":
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    print("👀 Watching for changes... (Ctrl+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
