from flask import Blueprint, g
from .errors import AuthenticationError


class Controller(Blueprint):
    def __init__(
        self, name, import_name, require_auth=True, auth_error_class=None, **kwargs
    ):
        super().__init__(name, import_name, **kwargs)

        if auth_error_class is None:
            auth_error_class = AuthenticationError
        if type(auth_error_class) != type or not issubclass(
            auth_error_class, Exception
        ):
            raise TypeError("auth_error_class must be a subclass of Exception")
        self.auth_error = auth_error_class

        self.before_request(self.__set_auth_data)
        if require_auth:
            self.before_request(self.check_auth)

    def get_current_user(self) -> object:
        return None

    def __set_auth_data(self):
        g.user = self.get_current_user()

    def check_auth(self):
        if g.user is None:
            raise self.auth_error()
