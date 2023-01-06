Install, easy, pure python lib.
===============================

.. code-block:: bash

    $ pip install interceptoraptor

Given we have Star Wars API use-case for: Record, Fetch and Replay.

We will have three assets:

1. swapi.py:
    We have Our Star Wars API - swapi.py

    .. code-block:: python

        # swapi.py
        import requests


        def get_people(people_id: str, method='GET', url='https://swapi.dev/api/people/'):
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
            assert p1['name'] == 'Luke Skywalker'
            p2 = get_people('2')
            assert p2['name'] == 'C-3PO'
            p3 = get_people('3')
            assert p3['name'] == 'R2-D2'


        if __name__ == "__main__":
            main()

3. mock.py:
    Intercepted target API

    .. code-block:: python

        from swapi import get_people

        from interceptoraptor.decorator import intercept
        from interceptoraptor.storage.sqllite3 import Sqlite3
        from pathlib import Path

        path = Path().parent / 'test_swapi_dev.db'  # store intercepted data

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

Record
------

.. code-block:: bash

    $ python3
    >>> from swapi import get_people # api to intercept
    >>> import mock ## auto apply intercepting on import
    >>> import sw_run
    >>> sw_run.main()
    INTERCEPT read from EXTERNAL GET:'https://swapi.dev/api/people/' '005ef4923dae85fa7b54d957a2ab70cc.json'
    INTERCEPT read from EXTERNAL GET:'https://swapi.dev/api/people/' 'ad5df7e7b01bd1454ef1b48e97a2dbda.json'
    INTERCEPT read from EXTERNAL GET:'https://swapi.dev/api/people/' '8323ae1ca8824ec030d850578cc9d3e0.json'



Fetch - We transfer 'test_swapi_dev.db' to IDE env to replay.
-------------------------------------------------------------


.. code-block:: bash

    $ python3
    Python 3.9.16 (main, Dec  7 2022, 10:06:04) 
    [Clang 14.0.0 (clang-1400.0.29.202)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from swapi import get_people # api to intercept
    >>> import mock ## auto apply intercepting on import
    >>> mock.storage.read_only = True # ENSURE THAT DATABASE IS IN READ ONLY MODE
    >>> import sw_run
    >>> sw_run.main()
    INTERCEPT read from INTERNAL GET:'https://swapi.dev/api/people/' '005ef4923dae85fa7b54d957a2ab70cc.json'
    INTERCEPT read from INTERNAL GET:'https://swapi.dev/api/people/' 'ad5df7e7b01bd1454ef1b48e97a2dbda.json'
    INTERCEPT read from INTERNAL GET:'https://swapi.dev/api/people/' '8323ae1ca8824ec030d850578cc9d3e0.json'


.. Important::
    
    From the log you can notice that EXTERNAL changed into INTERNAL now.
    



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
    $ interceptoraptor mock sw_run --main-function-to-call=main
    importing module_name='mock' ...
    import module_name='mock' is done
    importing module_name='sw_run' ...
    import module_name='sw_run' is done
    Call main_function main
    INTERCEPT read from INTERNAL GET:'https://swapi.dev/api/people/' '005ef4923dae85fa7b54d957a2ab70cc.json'
    INTERCEPT read from INTERNAL GET:'https://swapi.dev/api/people/' 'ad5df7e7b01bd1454ef1b48e97a2dbda.json'
    INTERCEPT read from INTERNAL GET:'https://swapi.dev/api/people/' '8323ae1ca8824ec030d850578cc9d3e0.json'

