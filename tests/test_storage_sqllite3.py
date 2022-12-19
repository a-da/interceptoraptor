from pathlib import Path

import pytest

from interceptoraptor.storage import sqllite3


def test_full_integration():
    path = Path(__file__).parent / 'http_intercept.db'
    path.unlink(missing_ok=True)

    storage = sqllite3.Sqlite3(path)

    with storage as db:
        db['abc.json'] = 'aaa'
        assert db['abc.json'] == 'aaa'
        assert 'abc.json' in db
        assert 'abc.json2' not in db

    with storage as db:
        assert db['abc.json'] == 'aaa', 'check if we can read again'

        with pytest.raises(AssertionError):
            db.read_only = True
            db['read_only'] = 'True'

        db.read_only = False
        db['read_only'] = 'False'

    with storage as db:
        assert db['read_only'] == 'False'

    path.unlink()
