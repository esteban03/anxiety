import pytest
from pathlib import Path


@pytest.fixture(autouse=True)
def _create_scenery(fs):
    desktop = Path("~/Desktop").expanduser()
    desktop.mkdir(parents=True)

    downloads = Path("~/Downloads").expanduser()
    downloads.mkdir(parents=True)


@pytest.fixture()
def downloads() -> Path:
    return Path("~/Downloads").expanduser()


@pytest.fixture()
def desktop() -> Path:
    return Path("~/Desktop").expanduser()
