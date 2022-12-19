Install, easy, pure python lib.
===============================

.. code-block:: bash

    $ pip install interceptoraptor

Given we have Star Wars API use-case (swapi.py) for: 1-Record, 2-Fetch and 3-Replay.

We will have three assets:

1. swapi.py:
    We have Our Star Wars API - swapi.py

    .. code-block:: python

        # swapi.py
        import requests


        def get_people(people_id: int, method='GET', url='https://swapi.dev/api/people/'):
            del method
            response = requests.get(url + people_id)
            return response.json()

2. sw_run.py:
    To run Star Wars API

    .. code-block:: python

        # sw_run.py
        from swapi import get_people

        def main():
            p1 = get_people('1')
            assert p1
            p2 = get_people(2)
            assert p1
            p3 = get_people(3)
            assert p3

        if __name__ == "__main__":
            main()

3. mock.py:
    Intercepted target API

    .. code-block:: python

        from swapi import get_people

        from interceptoraptor.decorator import intercept
        from interceptoraptor.storage.sqllite3 import Sqlite3
        from pathlib import Path

        path = Path().parent / 'test_swapi_dev.db' # store intercepted data

        storage = Sqlite3(path)
        storage.read_only = False

        intercept(
            target_call=get_people,
            storage=storage
        )


We execute sw_run.py on HOT env with interceptoraptor in one of two modes:

1. Module mode
2. Command line mode


1. Module mode
==============

.. code-block:: python

    # intercept.swapi.py
    from swapi import get_people # api to intercept

    import mock ## auto apply intercepting on import
    import sw_run

    sw_run.main()

.. code-block:: bash

    # 1-Record
    $ intercept.swapi.py
    INTERCEPT read from EXTERNAL GET:'https://swapi.dev/api/people/' '005ef4923dae85fa7b54d957a2ab70cc.json'
    INTERCEPT read from EXTERNAL GET:'https://swapi.dev/api/people/' '1ab0697ae6d92e14fa83f65aab774dc5.json'
    INTERCEPT read from EXTERNAL GET:'https://swapi.dev/api/people/' 'aa71300179f110d8de00d2d554a98e18.json'

2-Fetch - We transfer 'test_swapi_dev.db' to IDE env to replay.

    .. code-block:: python

    # intercept.swapi.py
    ...
    mock.storage.read_only = True
    ...

3-Replay: EXTERNAL will be INTERNAL now

.. code-block::

    $ intercept.swapi.py
    INTERCEPT read from INTERNAL GET:'https://swapi.dev/api/people/' '005ef4923dae85fa7b54d957a2ab70cc.json'
    INTERCEPT read from INTERNAL GET:'https://swapi.dev/api/people/' '1ab0697ae6d92e14fa83f65aab774dc5.json'
    INTERCEPT read from INTERNAL GET:'https://swapi.dev/api/people/' 'aa71300179f110d8de00d2d554a98e18.json'


2. Command line mode
====================

Place all assets (``swapi.py``, ``sw_run.py`` and ``mock.py``) into the current dir.

.. code-block::

    $ ssh hot
    # 1-Record
    $ interceptoraptor mock sw_run --read-only=False

    $ ssh ide
    # 2-Fetch
    $ scp hot:/app/test_swapi_dev.db ide:/test_swapi_dev.db
    # 3-Replay
    $ interceptoraptor mock sw_run --read-only=True
