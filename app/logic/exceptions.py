class UsersLimitHasReachedException(Exception):
    pass


class NoSuchUserException(Exception):
    pass


class UserAlreadyExistsException(Exception):
    pass


class SelfTransactionsAreForbiddenException(Exception):
    pass


class BadCoinsNumberException(Exception):
    pass


class BadDateException(Exception):
    pass
