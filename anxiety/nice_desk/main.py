import shutil
from pathlib import Path

from anxiety.constants import TEMPORARY_FILE_PATTERNS


class NiceDesk:
    def __init__(self, src_path: str | Path) -> None:
        self.src_path = Path(src_path)
        self.download_folder = Path("~/Desktop").expanduser()
        self.target_folder = self.download_folder / "Desktop"

    def _skip(self) -> bool:
        path = self.src_path

        if path.parent.name != "Desktop":
            return True

        if path.parent.parent.name == "Desktop":
            return True

        if path.is_dir():
            return True

        if any(t in path.name for t in TEMPORARY_FILE_PATTERNS):
            return True

        return False

    def run(self) -> None:
        if self._skip():
            return

        self.target_folder.mkdir(exist_ok=True)

        for file in self.download_folder.iterdir():
            if file.is_dir() or not file.exists():
                continue

            shutil.move(str(file), str(self.target_folder / file.name))
