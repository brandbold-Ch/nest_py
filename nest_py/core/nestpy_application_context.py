import inspect
from typing import Any, Dict, List, Tuple, Type, TypeVar


T = TypeVar("T")
INIT_VARS = "init_vars"
CLASS = "Config"


class Singleton:
    _instance: "Singleton" = None

    @classmethod
    def initialize_vars(cls, config: Type[T]) -> None:
        init_vars = getattr(config, INIT_VARS, {})
        for name, type_hint in init_vars.items():
            setattr(cls, name, type_hint())

    @classmethod
    def check_config(cls):
        if not hasattr(cls, CLASS): return
        config = getattr(cls, CLASS)

        if hasattr(config, INIT_VARS):
            cls.initialize_vars(config)

    def __new__(cls, *args, **kwargs) -> "Singleton":
        if not cls._instance:
            cls.check_config()
            cls._instance = super().__new__(cls)
        return cls._instance


class NestPyApplicationContext(Singleton):

    class Config:
        init_vars = {
            "controllers": dict,
            "modules": dict,
            "injectables": dict,
        }

    def __init__(self) -> None:
        self._controllers = getattr(self, "controllers")
        self._modules = getattr(self, "modules")
        self._injectables = getattr(self, "injectables")

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
            "deps": inspect.signature(controller_class),
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
            module_class: Type[T],
            imports: List[str],
            controllers: List[str],
            providers: List[str],
            exports: List[str]
    ) -> None:
        name = module_class.__name__
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

    def register_injectable(
            self,
            injectable_class: Type[T]
    ) -> None:
        name = injectable_class.__name__
        self._injectables[name] = {
            "injectable_class": injectable_class,
            "deps": inspect.signature(injectable_class)
        }

    def get_injectables(self) -> Dict[str, Any]:
        return self._injectables

    def get_injectable(self, name: str) -> Dict[str, Any]:
        return self._injectables.get(name, {})

    def clear_injectables(self) -> None:
        self._injectables.clear()

    def resolve(self) -> None:
        for module in self._modules.values():
            print(module)
