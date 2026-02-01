import time

from watchdog.events import FileSystemEventHandler, FileSystemEvent, DirCreatedEvent

from anxiety.nice_desk.main import NiceDesk


class NiceDeskHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent | DirCreatedEvent):
        time.sleep(0.5)

        nice_desk = NiceDesk(event.src_path)
        nice_desk.run()
