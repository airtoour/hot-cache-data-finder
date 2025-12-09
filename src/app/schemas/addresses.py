import re

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


class AddressOut(BaseModel):
    """Found Address by phone number out data"""

    address: str | None = None


class PhoneAddressDataIn(BaseModel):
    """Phone & Address Data for create"""

    # Мы можем валидировать строку так или через валидатор, я просто показываю, что знаю и умею
    phone: str = Field(..., pattern=r"^\+7 (\d{3}) \d{3}-\d{2}-\d{2}$")
    address: str

    @field_validator("phone")
    def validate_phone(cls, value: str) -> str:  # noqa
        """Validate phone number"""

        if not re.match(pattern=r"^\+7 (\d{3}) \d{3}-\d{2}-\d{2}$", string=value):
            raise ValueError("Phone must be in format +7 (111) 222-33-44")

        return value

    @field_validator("address")
    def validate_address(cls, value: str) -> str:  # noqa
        """Validate address"""

        if value == "string":
            raise ValueError("Address must be in normal format")
        return value


class PhoneAddressDataOut(BaseModel):
    """Phone & Address Data out data"""

    message: str


class AddressToDelete(BaseModel):
    """Addresses to delete"""

    phone: str
