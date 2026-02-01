import shutil
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler, FileSystemEvent, DirCreatedEvent


class NiceDeskHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent | DirCreatedEvent):
        time.sleep(0.5)

        path = Path(event.src_path)

        if path.parent.name != "Desktop":
            return

        if path.parent.parent.name == "Desktop":
            return

        if path.is_dir():
            return

        download_folder = Path("~/Desktop").expanduser()

        target_folder = download_folder / "Desktop"
        target_folder.mkdir(exist_ok=True)

        for file in download_folder.iterdir():
            if file.is_dir():
                continue

            if file.exists():
                shutil.move(str(file), str(target_folder / file.name))
