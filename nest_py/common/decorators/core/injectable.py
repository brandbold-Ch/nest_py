from typing import Type, TypeVar
from nest_py.core.application_context import NestPyApplicationContext


ctx_app = NestPyApplicationContext()
T = TypeVar("T")


def injectable(*args, **kwargs):
    def wrapper(cls: Type[T]):
        ctx_app.register_injectable(cls)
        return cls
    return wrapper
