import copy
import pickle
import sys
from pathlib import Path
from typing import Any, Dict

from interceptoraptor.decorator import intercept, single_intercept
from interceptoraptor.storage.sqllite3 import Sqlite3


def function_with_parameters(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """

    :param parameters:
    :return:
    """
    new = copy.deepcopy(parameters)
    del parameters
    new.pop('max_retries', None)  # TODO

    json_field = new.get('json')
    if json_field:
        json_field.pop('value', None)  # temporary ignore json.value from hash map
        json_field.pop('series', None)

        keys = json_field.get('keys')
        if keys and isinstance(keys, (list, tuple, set)):
            sorted_keys = sorted(keys)
            json_field['keys'] = sorted_keys

    return new


def test_single_intercept():
    path = Path().parent / 'test_single_intercept.db'
    path.unlink(missing_ok=True)

    storage = Sqlite3(path)

    @single_intercept(storage=storage, prepare_parameters=a_function_with_parameters)
    def a(url, method, z):
        return url + method + z

    assert a('1', '2', z='3') == '123'
    assert path.exists()
    with storage as db:
        hash_id = '0e34666ea5a332da6bd0b2ab57f6c455'
        assert db[f'{hash_id}.json'] == \
               b'{\n    "url": "1",\n    "method": "2",\n    "z": "3"\n}'

        assert pickle.loads(db[f'{hash_id}.pickle']) == '123'

    path.unlink()


def test_intercept():
    path = Path().parent / 'test_intercept.db'
    path.unlink(missing_ok=True)

    storage = Sqlite3(path)
    # pylint: disable=import-outside-toplevel
    import dummy_module1
    import dummy_module2
    import dummy_module3
    # pylint: enable=import-outside-toplevel

    intercept(
        target_call=dummy_module3.a,
        storage=storage,
        prepare_parameters=space_lib
    )

    dummy_module1.a('1', '2', z='3')

    with storage as db:
        hash_id = '0e34666ea5a332da6bd0b2ab57f6c455'
        assert db[f'{hash_id}.json'] == \
               b'{\n    "url": "1",\n    "method": "2",\n    "z": "3"\n}'

        assert pickle.loads(db[f'{hash_id}.pickle']) == '12333'

    # unload dummy modules
    sys.modules.pop(dummy_module1.__name__)
    sys.modules.pop(dummy_module2.__name__)
    sys.modules.pop(dummy_module3.__name__)

    path.unlink()
