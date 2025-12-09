from fastapi import HTTPException
from fastapi import status


class BaseServerException(HTTPException):
    """Base server exception for create custom exceptions"""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal Server Error"


class AddressNotFound(BaseServerException):
    """Custom exception if address not found"""

    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")


class AddressAlreadyExists(BaseServerException):
    """Custom exception if address already exists"""

    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail="Address with phone already exists")


class PhoneNotFound(BaseServerException):
    """Custom exception if address not found"""

    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Phone not found")
