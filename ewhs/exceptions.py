class EwhsError(Exception):
    pass


class BadRequest(EwhsError):
    def __init__(self, errors=None, *args):
        self.errors = errors
        super().__init__(*args)


class AuthenticationError(EwhsError):
    pass


class ServerError(EwhsError):
    pass


class ApiLimitReached(EwhsError):
    pass


class DoesNotExist(EwhsError):
    pass
