class CLIException(Exception):
    """Base CLI Exception"""

    def __init__(self, *args, **kwargs):
        _msg = f"{self.__doc__}"
        _msg += ", ".join([f"{a}" for a in args])
        if kwargs:
            _msg += f". {', '.join([f'{k}={v}' for k, v in kwargs.items()])}"
        super().__init__(_msg)


class IAlreadyKnowYou(CLIException):
    """User already installed"""


class WhoAreYou(CLIException):
    """TokkoCLI not installed"""
