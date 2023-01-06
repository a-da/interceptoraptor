=============================================================
Interceptoraptor - Intercept and Terminate your data problem.
=============================================================

You're welcome to use this tool in case you have a bug in as "hot" environment (prod, pre-prod, ...)
which can not be reproduced in your local IDE environment due to chains of many external requests dependencies (db, HTTP, ...).

We could address this in a few steps:

1. Record:
    Intercept and save data from *any* API on dependable environment (prod, pre-prod,...)

2. Fetch:
    Transport intercepted data to your IDE environment.

3. Replay:
    Replay captured from data environment into your IDE environment.

4. Repeat "Replay" step until you find a solution to the problem.

The idea is heavily inspired by `Vcrpy library <https://vcrpy.readthedocs.io/en/latest/>`_.
`Here <./docs/why_not_vcrpy.rst>`_ is listed some points where vcrpy does not perform well for our problem areas.

Eager to get started? This page gives a good introduction in how to get started with `<./docs/quickstart.rst>`_.
