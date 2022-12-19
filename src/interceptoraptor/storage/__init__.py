"""
The place where intercepted data can be saved

File storage like json or yaml file or files not recommended since
in case of multiprocessing of multithreading may override data.
"""
from pathlib import Path
from typing import Any

LOG = print


class AbstractStorage:
    """
    :param path: the location of storage: file, url ...
    """
    def __init__(self, path: Path) -> None:
        self._path = path
        self.read_only = False

    def __enter__(self) -> 'AbstractStorage':
        pass

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    def __setitem__(self, key: str, value: bytes) -> None:
        if self.read_only:
            raise AssertionError(f"The storage is in read only mode,"
                                 f"cannot write new data: {key=}: {value=}")

    def __getitem__(self, key: str) -> bytes:
        pass

    def __contains__(self, key: str) -> bool:
        pass

    def exists(self) -> bool:
        pass
