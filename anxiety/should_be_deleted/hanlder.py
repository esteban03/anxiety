import time

from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent

from anxiety.should_be_deleted.main import ShouldBeDeleted


class DownloadFolderHandler(FileSystemEventHandler):
    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        print("New file created: ", event.src_path)

        time.sleep(0.5)

        should_be_deleted = ShouldBeDeleted(src_path=event.src_path)
        should_be_deleted.run()