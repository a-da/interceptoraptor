Install, easy, pure python lib.

.. code-block:: bash

    $ pip install interceptoraptor


Call from python ''''''''''''''''''''

Given we have an API


.. code-block:: python

    # swapi.py
    import requests


    def get_people(people_id: int, method='GET', url='https://swapi.dev/api/people/'):
        del method
        response = requests.get(url + people_id)
        return response.json()

We execute it on HOT env with interceptoraptor

.. code-block:: python

    # intercept.swapi.py″
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

    p1 = get_people('1')
    assert p1
    p2 = get_people(2)
    assert p1
    p3 = get_people(3)
    assert p3


.. code-block::

    INTERCEPT read from EXTERNAL GET:'https://swapi.dev/api/people/' '005ef4923dae85fa7b54d957a2ab70cc.json'
    INTERCEPT read from EXTERNAL GET:'https://swapi.dev/api/people/' '1ab0697ae6d92e14fa83f65aab774dc5.json'
    INTERCEPT read from EXTERNAL GET:'https://swapi.dev/api/people/' 'aa71300179f110d8de00d2d554a98e18.json'


We will see message like


We transfer 'test_swapi_dev.db' to IDE env to replay.

    .. code-block:: python

    # intercept.swapi.py
    ...
    storage.read_only = True
    ...


.. code-block::

    INTERCEPT read from INTERNAL GET:'https://swapi.dev/api/people/' '005ef4923dae85fa7b54d957a2ab70cc.json'
    INTERCEPT read from INTERNAL GET:'https://swapi.dev/api/people/' '1ab0697ae6d92e14fa83f65aab774dc5.json'
    INTERCEPT read from INTERNAL GET:'https://swapi.dev/api/people/' 'aa71300179f110d8de00d2d554a98e18.json'


Call from command line ''''''''''''''''''''

.. code-block::

    ssh hot
    interceptoraptor mock script.swapi --read-only=False

    ssh ide
    scp hot:/app/test_swapi_dev.db ide:/test_swapi_dev.db
    interceptoraptor mock script.swapi.py --read-only=True

