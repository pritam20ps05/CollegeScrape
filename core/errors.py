class CustomError(Exception):
    def __init__(self, message: str, code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = code
    
    def __str__(self) -> str:
        return self.message
    
class LoginError(Exception):
    def __init__(self, method: str, message: str = 'Please login before using this endpoint.') -> None:
        super().__init__(method, message)
        self.message = message
        self.method = method

    def __str__(self) -> str:
        return self.message