from interceptoraptor.decorator import intercept
from interceptoraptor.storage.sqllite3 import Sqlite3
from pathlib import Path
from swapi import get_people

path = Path().parent / 'test_swapi_dev.db'

storage = Sqlite3(path)
storage.read_only = False

intercept(
    target_call=get_people,
    storage=storage
)
