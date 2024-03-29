class DoesNotExistError(Exception):
    pass


class AlreadyExistsError(Exception):
    pass


class WrongEmailError(Exception):
    pass


class ConversionError(Exception):
    pass


class WrongOwnerError(Exception):
    pass


class NotEnoughBalanceError(Exception):
    pass
