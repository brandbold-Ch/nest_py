from typing import Any, Dict, List, Tuple, Type, TypeVar


T = TypeVar("T")


class Singleton:
    _instance: "Singleton" = None

    def __new__(cls, *args, **kwargs) -> "Singleton":
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


class NestPyApplicationContext(Singleton):

    def __init__(self) -> None:
        self._controllers = {}
        self._modules = {}

    def register_controller(
            self,
            controller_class: Type[T],
            routes: List[Dict[str, Any]],
            params: Tuple[tuple, Dict[str, Any]]
    ) -> None:
        name = controller_class.__name__
        self._controllers[name] = {
            "name": name,
            "controller_class": controller_class,
            "routes": routes,
            "params": {
                "args": list(params[0]),
                "kwargs": params[1]
            }
        }

    def get_controllers(self) -> Dict[str, Any]:
        return self._controllers

    def get_controller(self, name: str) -> Dict[str, Any]:
        return self._controllers.get(name, {})

    def clear_controllers(self) -> None:
        self._controllers.clear()

    def register_module(
            self,
            name: str,
            module_class: Type[T],
            imports: List[str],
            controllers: List[str],
            providers: List[str],
            exports: List[str]
    ) -> None:
        self._modules[name] = {
            "name": name,
            "module_class": module_class,
            "imports": imports,
            "controllers": controllers,
            "providers": providers,
            "exports": exports
        }

    def get_modules(self) -> Dict[str, Any]:
        return self._modules

    def get_module(self, name: str) -> Dict[str, Any]:
        return self._modules.get(name, {})

    def clear_modules(self) -> None:
        self._modules.clear()

    def resolve(self):
        ...
