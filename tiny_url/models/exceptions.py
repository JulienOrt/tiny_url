class TinyUrlBaseException(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.__message = message
        self.__status_code = status_code

    def __repr__(self) -> str:
        return f"{self.__status_code}: {self.__message}"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def status_code(self):
        return self.__status_code
