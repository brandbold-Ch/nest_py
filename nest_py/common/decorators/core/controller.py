from typing import Callable, Type, TypeVar
from nest_py.core.application_context import NestPyApplicationContext
import inspect


ctx_app = NestPyApplicationContext()
T = TypeVar("T")


def controller(*args, **kwargs) -> Callable[[Type[T]], Type[T]]:
    def wrapper(cls: Type[T]) -> Type[T]:
        handlers = inspect.getmembers(cls, inspect.isfunction)
        routes = []

        for name, handler in handlers:
            if hasattr(handler, "_metadata"):
                routes.append({
                    "handler": handler,
                    "metadata": getattr(handler, "_metadata")
                })
                delattr(handler, "_metadata")

        ctx_app.register_controller(cls, routes, (args, kwargs))
        return cls
    return wrapper
