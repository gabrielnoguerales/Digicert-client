from functools import wraps

from src.common.exceptions import BadConfiguratedException


def login_required(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        if (
            not self.api_key or not self.baseuri
        ):  # If url and api_key has been set return func else return logger error
            raise BadConfiguratedException("Please login first using your api_key. ")
        return func(self, *args, **kwargs)

    return wrapped


def url_required(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        if not self.baseuri:  # If url has been set return func else return logger error
            raise BadConfiguratedException(
                "Please set the url before making the login request. "
            )
        return func(self, *args, **kwargs)

    return wrapped
