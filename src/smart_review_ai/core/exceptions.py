class EntityAlreadyExistsError(Exception):
    pass


class EntityNotFoundError(Exception):
    pass


class ServiceUnavailableError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class InactiveUserError(Exception):
    pass
