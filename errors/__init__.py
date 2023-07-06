class CustomError(Exception):
    def __init__(self, message: str, code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = code
    
    def __str__(self):
        return self.message