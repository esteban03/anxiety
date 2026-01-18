from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent
from pathlib import Path

if __name__ == "__main__":
    path = "/Users/estebansanchez/Downloads"

    class MyHandler(FileSystemEventHandler):
        def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
            print("New file created: ", event.src_path)

            downloads_folder = Path(path)

            should_be_deleted = []

            for file in downloads_folder.glob("*"):
                if file.suffix in (".app", ".dmg"):
                    should_be_deleted.append(file)

            should_be_deleted_folder = Path(f"{path}/should-be-deleted")
            should_be_deleted_folder.mkdir(exist_ok=True)

            for file in should_be_deleted:
                file.move_into(should_be_deleted_folder)

            print(f"{len(should_be_deleted)} files deleted")


    observer = Observer()
    observer.schedule(MyHandler(), path, recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()