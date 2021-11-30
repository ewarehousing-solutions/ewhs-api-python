class EwhsError(Exception):
    pass


class BadRequest(EwhsError):
    pass


class AuthenticationError(EwhsError):
    pass


class ServerError(EwhsError):
    pass


class ApiLimitReached(EwhsError):
    pass


class DoesNotExist(EwhsError):
    pass
