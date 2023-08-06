from ...config.settings import development


def execute_on_dev(f):
    def wrapper(*args):
        settings = args[0].settings
        print(settings.backend)
        if settings.backend is not development.BACKEND:
            raise Exception("This method is only supported for development mode!")
        return f(*args)

    return wrapper
