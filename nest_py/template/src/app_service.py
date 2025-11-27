from nest_py.common import injectable


@injectable()
class AppService:

    def get_hello(self) -> str:
        return "Hello from AppService!"
