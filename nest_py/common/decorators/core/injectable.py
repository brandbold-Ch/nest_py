from typing import Type, TypeVar, Callable
from nest_py.core.nestpy_application_context import NestPyApplicationContext


ctx_app = NestPyApplicationContext()
T = TypeVar("T")


def injectable(*args, **kwargs) -> Callable[[Type[T]], Type[T]]:
    def wrapper(cls: Type[T]):
        ctx_app.register_injectable(cls)
        return cls
    return wrapper
