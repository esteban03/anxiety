import pytest

from pathlib import Path


from anxiety.constants import TEMPORARY_FILE_PATTERNS
from anxiety.nice_desk.main import NiceDesk


def test_move_new_file(fs, desktop):
    file = desktop / "nice_file.txt"
    file.touch()

    assert file.exists()

    nice_desk = NiceDesk(file)
    nice_desk.run()

    assert not file.exists()

    target_folder = desktop / "Desktop"
    assert target_folder.exists()

    assert (target_folder / file.name).exists()


def test_not_move_folder(fs, desktop):
    new_folder: Path = desktop / "new_folder/"
    new_folder.mkdir()

    assert new_folder.exists() and new_folder.is_dir()

    nice_desk = NiceDesk(new_folder)
    nice_desk.run()

    assert new_folder.exists()


@pytest.mark.parametrize("pattern", TEMPORARY_FILE_PATTERNS)
def test_avoid_move_specific_patterns(fs, desktop, pattern):
    file_to_avoid: Path = desktop / f"any_{pattern}"
    file_to_avoid.touch()

    nice_desk = NiceDesk(file_to_avoid)
    nice_desk.run()

    assert file_to_avoid.exists()
