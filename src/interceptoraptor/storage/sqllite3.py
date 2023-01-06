import sqlite3
import threading
from pathlib import Path
from typing import Any, cast, Iterator
from contextlib import contextmanager

from . import AbstractStorage


lock = threading.Lock()


class Sqlite3(AbstractStorage):
    @contextmanager
    def _safe(self) -> Iterator[None]:
        with lock:
            self._connection = sqlite3.connect(self._path, check_same_thread=True)
            self._cursor = self._connection.cursor()
            yield
            self._connection.commit()
            self._connection.close()

    def __init__(self, path: Path = Path('http_intercept.db')):
        super().__init__(path)
        existed = self.exists()
        with self._safe():
            self._connected: bool = True

            if not existed:
                self._cursor.execute(
                    "CREATE TABLE file(file_name PRIMARY KEY, data BLOB)")

    def exists(self) -> bool:
        return self._path.exists()

    def __enter__(self) -> 'Sqlite3':
        # if not self._connected:
        #    self._connection = sqlite3.connect(self._path, check_same_thread=True)
        #    self._cursor = self._connection.cursor()
        #    self._connected = True

        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # self._connection.close()
        # self._connected = False
        pass

    def __setitem__(self, key: str, value: bytes) -> None:
        super().__setitem__(key, value)
        with self._safe():
            self._cursor.execute(
                "INSERT INTO file values (?, ?)", (key, value)
            )

    def __getitem__(self, key: str) -> bytes:
        with self._safe():
            self._cursor.execute(
                "SELECT data FROM file WHERE file_name = (?)", (key, )
            )
            res = self._cursor.fetchone()
            if not res:
                raise KeyError(f'No data for key {key!r}')

        return res and cast(bytes, res[0])

    def __contains__(self, key: str) -> bool:
        with self._safe():
            self._cursor.execute(
                "SELECT count(1) FROM file WHERE file_name = (?)", (key, )
            )

            return bool(self._cursor.fetchone()[0])
