"""
Command line interface API
"""
import importlib
import sys


LOG = print


def cli(*args: str) -> None:
    """
    CLI entry point
    """
    if not args:
        args = tuple(sys.argv[1:])

    sys.path.append('.')

    assert args

    for module in args:
        LOG(f"importing {module=} ...")
        importlib.import_module(module)
        LOG(f"import {module=} is done")


if __name__ == '__main__':
    cli()
