from typing import Callable, Any


def route(*args, **kwargs) -> Callable:
    def wrapper(func: Callable[[Any], Any]) -> Callable:
        setattr(func, "_metadata", {"args": args, "kwargs": kwargs})
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
