from typing import Any

import dummy_module1


def b(*args: Any, **kwargs: Any) -> Any:
    return dummy_module1.a(*args, **kwargs)


if __name__ == "__main__":
    assert b.__name__ == 'b'
