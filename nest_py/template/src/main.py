from app_module import AppModule
from nest_py.core import NestPyFactory


def bootstrap() -> None:
    app = NestPyFactory.create(AppModule)
    app.listen(host="127.0.0.1", port=3000)


bootstrap()
