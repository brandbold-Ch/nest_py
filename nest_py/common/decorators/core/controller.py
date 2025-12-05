from typing import Callable, Type, TypeVar
from nest_py.core import NestPyApplicationContext, Reflect
from nest_py.core.constants import MetadataKeys
from nest_py.core.structures import RouteDefinition


ctx_app = NestPyApplicationContext()
T = TypeVar("T")


def controller(*args, **kwargs) -> Callable[[Type[T]], Type[T]]:
    def wrapper(cls: Type[T]) -> Type[T]:
        handlers = Reflect.getFunctions(cls)
        routes = []

        for name, handler in handlers:
            if Reflect.has(handler, MetadataKeys.ROUTE_METADATA):
                routes.append(RouteDefinition(
                    handler=handler,
                    metadata=Reflect.get(handler, MetadataKeys.ROUTE_METADATA)
                ))
                Reflect.deleteProperty(handler, MetadataKeys.ROUTE_METADATA)

        ctx_app.register_controller(cls, routes, (args, kwargs))
        return cls
    return wrapper
