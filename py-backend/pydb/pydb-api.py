# an API for GITogether DB operations
# @author: owenns

# error classes
class InvalidEmailError(Error):
    pass


class InvalidPasswordError(Error):
    pass


class NoSuchUserFoundError(Error):
    pass


class IncorrectPasswordError(Error):
    pass

# for registering a new user
# email, password must be a tuple data type (sanitization)


def new_user_db((email, password)):
    if "@" not in email and "." not in email:
