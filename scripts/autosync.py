from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import threading
import time
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS = os.path.join(ROOT, "docs")

timer = None

def sync():
    print("\n📤 Syncing...")

    subprocess.run(["git", "add", "."], cwd=ROOT)

    message = f"Auto update {time.strftime('%Y-%m-%d %H:%M:%S')}"

    commit = subprocess.run(
        ["git", "commit", "-m", message],
        cwd=ROOT
    )

    if commit.returncode != 0:
        print("ℹ️ No changes to commit.")
        return

    subprocess.run(["git", "push"], cwd=ROOT)

    print("✅ Website updated!\n")

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        global timer

        if event.is_directory:
            return

        if timer:
            timer.cancel()

        timer = threading.Timer(10, sync)
        timer.start()

observer = Observer()
observer.schedule(Handler(), DOCS, recursive=True)
observer.start()

print("👀 Skyfall Sync is watching your docs folder...")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()