from typing import Callable, Any
from nest_py.core import Reflect, NestPyApplicationContext
from nest_py.core.constants import MetadataKeys

ctx_app = NestPyApplicationContext()


def route(*args, **kwargs) -> Callable[[Callable[..., Any]], Callable]:
    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        Reflect.set(func, MetadataKeys.ROUTE_METADATA, {"args": args, "kwargs": kwargs})
        return func
    return wrapper


def get(*args, **kwargs) -> Callable:
    kwargs["methods"] = ["GET"]
    return route(*args, **kwargs)


def post(*args, **kwargs) -> Callable:
    kwargs["methods"] = ["POST"]
    return route(*args, **kwargs)


def put(*args, **kwargs) -> Callable:
    kwargs["methods"] = ["PUT"]
    return route(*args, **kwargs)


def delete(*args, **kwargs) -> Callable:
    kwargs["methods"] = ["DELETE"]
    return route(*args, **kwargs)


def head(*args, **kwargs) -> Callable:
    kwargs["methods"] = ["HEAD"]
    return route(*args, **kwargs)


def patch(*args, **kwargs) -> Callable:
    kwargs["methods"] = ["PATCH"]
    return route(*args, **kwargs)


def options(*args, **kwargs) -> Callable:
    kwargs["methods"] = ["OPTIONS"]
    return route(*args, **kwargs)
