1. install editable mode
========================

.. code-block:: bash

    $ pip install -e .[dev,deploy_to_pip]

2. create distribution
======================

.. code-block:: bash

    $ make wheel

3. Upload distribution into your 'banana' env
=============================================

Upload dist/interceptoraptor-0.0.1.dev2-py3-none-any.whl

4. Install distribution into your 'banana' env
==============================================

.. code-block:: bash

    $ pip install interceptoraptor-0.0.1.dev2-py3-none-any.whl

5. Intercept and terminate your data problem
============================================

.. code-block:: bash

    # provide mock.py and your_script.py
    # TODO: 1. implement --name-of-db
    # TODO: 2. implement --read-only
    # TODO: 3. implement --commit-to-local-git-path

    interceptoraptor mock your_script --name-of-db=SPACE-XXX.db --read-only --commit-to-local-git-path=
    interceptoraptor-git --artifacts=xx1,xxx2 --git-path --message
