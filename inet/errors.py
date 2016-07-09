
class ConnectionError(Exception):

    def __init__self(self, message, address):
        super().__init__(message.format(address=address))


class RegisterationError(Exception):
    pass
