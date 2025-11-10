


class NestPyFactory:
    @staticmethod
    def create_instance(class_type, *args, **kwargs):
        return class_type(*args, **kwargs)
