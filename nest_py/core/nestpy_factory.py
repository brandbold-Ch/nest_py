from typing import Union


class NestPyFactory:

    @staticmethod
    def create(module_class, *args, **kwargs):
        return module_class(*args, **kwargs)

    @staticmethod
    def listen(cls, host: str, port: Union[str, int]) -> None:
        print(f"Listening on port {port}...")