"""
Decorator and contextmanager for intercept/replay data

- single_intercept
- intercept: intercepts usages of the mocked API detected in sys.modules
"""
import hashlib
import io
import json
import pickle
import sys
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Literal, Optional, Union, cast

import requests

from . import generics
from .storage import AbstractStorage

LOG = print


@dataclass
class _InterceptFunction:
    storage: AbstractStorage
    prepare_parameters: Optional[Callable[..., Any]] = None
    """
    """

    def __call__(self, target_call: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(target_call)
        def helper(*args: Any, **kwargs: Any) -> Any:
            parameters = generics.unify_args_to_kwargs(target_call, args, kwargs)
            if self.prepare_parameters:
                parameters = self.prepare_parameters(parameters)

            json_dump = json.dumps(parameters, indent=4).encode()
            md5 = hashlib.md5(json_dump).hexdigest()

            json_file_name = f'{md5}.json'
            pickle_file_name = f'{md5}.pickle'

            # IF INTERNAL
            if self.storage.exists():
                with self.storage as db:
                    if json_file_name in db:
                        LOG(f"INTERCEPT read from INTERNAL "
                            f"{parameters['method']}:{parameters['url']!r} {json_file_name!r}")

                        response = pickle.loads(db[pickle_file_name])

                        if isinstance(response, generics.PickleRequestsResponse):
                            response = response.requests_response()

                        if isinstance(response, Exception):
                            raise response

                        return response

            # IF EXTERNAL
            LOG(f"INTERCEPT read from EXTERNAL "
                f"{parameters['method']}:{parameters['url']!r} {json_file_name!r}")
            # print(json_dump.decode())
            try:
                response = target_call(*args, **kwargs)
            except (Exception,) as exc:  # pylint: disable=broad-except
                response = exc

            if not isinstance(response, requests.Response):
                pickle_resp = pickle.dumps(response)
            else:
                content = cast(Union[bytes, Literal[False]], response._content)  # pylint: disable=protected-access
                raw = None
                if content is False:  # THEN is streaming
                    raw = response.raw.read()
                    response.raw = io.BytesIO(raw)

                pickle_requests_response = generics.PickleRequestsResponse(
                    encoding=response.encoding,
                    _content=content,
                    status_code=response.status_code,
                    url=response.url,
                    raw=raw
                )

                pickle_resp = pickle_requests_response.dumps()

            with self.storage as db:
                db[json_file_name] = json_dump
                db[pickle_file_name] = pickle_resp

            if isinstance(response, Exception):
                raise response

            return response

        return helper


def single_intercept(
    target_call: Optional[Callable[..., Any]] = None,
    *,
    storage: AbstractStorage,
    prepare_parameters: Optional[Callable[..., Any]] = None
    # intercept data path
) -> Callable[..., Any]:
    """
    Intercept func:

        save
            in case no previous intercept record
        replay
            in case previous intercept record exists

    .. example::

         intercept(
            target_call=a.b.c.send_request,
            prepare_parameters=sort_elements_from_json_key
         )

    """
    intercept_function = _InterceptFunction(
        storage=storage,
        prepare_parameters=prepare_parameters
    )

    if target_call:
        return intercept_function(target_call)

    return intercept_function


def intercept(
    target_call: Callable[..., Any],
    storage: AbstractStorage,
    prepare_parameters: Optional[Callable[..., Any]] = None
) -> None:
    """
    Intercept all ``target_call`` API usage.

    Find all API usage recorded in sys.modules.
    Wrapping all original calls with single_intercept function
    """
    intercepted_target_call = single_intercept(
        target_call=target_call,
        storage=storage,
        prepare_parameters=prepare_parameters
    )
    keys = list(sys.modules)
    for key in keys:
        module = sys.modules[key]
        for k, v in dict(module.__dict__).items():
            if v is target_call:
                setattr(module, k, intercepted_target_call)  # TODO: try to mock.patch
