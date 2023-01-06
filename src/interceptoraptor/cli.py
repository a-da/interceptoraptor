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
    assert len(args) > 2

    main_function_to_call = None

    for arg in args:
        if arg.startswith("--main-function-to-call"):
            main_function_to_call = arg.split("=")[1]
        else:
            module_name = arg
            LOG(f"importing {module_name=} ...")
            module = importlib.import_module(module_name)
            LOG(f"import {module_name=} is done")

    if main_function_to_call:
        LOG('Call main_function %s.%s()' % (module.__name__, main_function_to_call))  # pylint: disable=consider-using-f-string
        getattr(module, main_function_to_call)()
    else:
        LOG('No --main-function-to-call=main provided')


if __name__ == '__main__':
    cli()
