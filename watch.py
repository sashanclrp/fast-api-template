import os
import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self, process):
        self.process = process
        self.last_modified = time.time()
        
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            current_time = time.time()
            if current_time - self.last_modified < 0.5:
                return
            self.last_modified = current_time
            
            # Kill the current process
            self.process.kill()
            
            # Start a new process
            self.process = start_server()

def start_server():
    # Start the FastAPI server using uvicorn
    process = subprocess.Popen(
        ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    # Start a thread to read and print the process output
    def print_output():
        for line in iter(process.stdout.readline, b''):
            sys.stdout.write(line.decode())
    
    import threading
    threading.Thread(target=print_output, daemon=True).start()
    
    return process

if __name__ == "__main__":
    
    # Start the server
    process = start_server()
    
    # Set up the file watcher
    event_handler = RestartHandler(process)
    observer = Observer()
    observer.schedule(event_handler, path="src", recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        process.kill()
    
    observer.join()