from typing import Any

from dummy_module1 import a


def c(*args: Any, **kwargs: Any) -> Any:
    return a(*args, **kwargs)


if __name__ == "__main__":
    assert c.__name__ == 'b'
