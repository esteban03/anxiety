from pathlib import Path

import arrow
import freezegun

from anxiety.should_be_deleted.main import ShouldBeDeleted, Rules


def test_move_file_to_should_be_deleted(fs, downloads):
    target_folder = downloads / "should-be-deleted"

    assert not target_folder.exists()

    created_file_datetime = (
        arrow.now().shift(days=-(Rules.is_too_new.days + 1)).datetime
    )

    with freezegun.freeze_time(created_file_datetime):
        new_file = downloads / "new_file.txt"
        new_file.touch()

    should_be_deleted = ShouldBeDeleted(new_file)
    should_be_deleted.run()

    assert target_folder.exists()
    assert not new_file.exists()


def test_delete_file_from_should_be_deleted(fs, downloads):
    target_folder = downloads / "should-be-deleted"
    target_folder.mkdir()

    assert target_folder.exists()

    created_file_datetime = (
        arrow.now().shift(days=-(Rules.max_time_before_to_delete.days + 1)).datetime
    )

    with freezegun.freeze_time(created_file_datetime):
        old_file: Path = target_folder / "old_file.txt"
        old_file.touch()

    assert old_file.exists()

    new_file = downloads / "new_file.txt"
    new_file.touch()

    should_be_deleted = ShouldBeDeleted(new_file)
    should_be_deleted.run()

    assert target_folder.exists()
    assert not old_file.exists()
