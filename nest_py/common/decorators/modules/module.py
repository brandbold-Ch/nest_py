from typing import Callable, Optional, List, Type, TypeVar
from nest_py.core import NestPyApplicationContext


ctx_app = NestPyApplicationContext()
T = TypeVar("T")


def module(
    imports: Optional[List[str]] = None,
    controllers: Optional[List[str]] = None,
    providers: Optional[List[str]] = None,
    exports: Optional[List[str]] = None
) -> Callable[[Type[T]], Type[T]]:
    def wrapper(cls: Type[T]) -> Type[T]:
        ctx_app.register_module(
            name=cls.__name__,
            module_class=cls,
            imports=imports,
            controllers=controllers,
            providers=providers,
            exports=exports
        )
        return cls
    return wrapper
