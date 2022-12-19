"""
Not categorized API: utility, helpers ...
"""
import copy
import io
import pickle
from dataclasses import dataclass
from inspect import signature
from typing import Any, Callable, Dict, Literal, Optional, Tuple, Union, cast


import requests


@dataclass
class PickleRequestsResponse:
    """
    A custom wrapper for Requests.Response object
    To create Object:
        object = PickleRequestsResponse(
            encoding: ...,
            _content: ...,
            status_code: ...,
            url: ...,
            raw: ...,
        )
    To serialize:
        object.dumps()
    To deserialize:
        object.requests_response()
    """
    encoding: Optional[str]
    _content: Union[bytes, Literal[False]]
    status_code: int
    url: str
    raw: Optional[bytes] = None

    def requests_response(self) -> requests.Response:
        # workaround for the bug for pickle requests.Response
        resp = requests.Response()
        resp.encoding = self.encoding
        resp._content = cast(bytes, self._content)  # noqa: workaround  # pylint: disable=protected-access
        resp.status_code = self.status_code
        resp.url = self.url

        if self.raw:
            resp.raw = io.BytesIO(self.raw)

        return resp

    def dumps(self) -> bytes:
        return pickle.dumps(self)


def unify_args_to_kwargs(func: Callable[..., Any],
                         args: Tuple[Any, ...],
                         kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Move input data from positional args into kwargs
    """
    sign = signature(func)
    parameters = dict(sign.parameters)
    for index, key in enumerate(parameters.keys()):
        value = args[index] if index < len(args) else kwargs.get(key, sign.parameters[key].default)
        parameters[key] = copy.deepcopy(value)

    return parameters
