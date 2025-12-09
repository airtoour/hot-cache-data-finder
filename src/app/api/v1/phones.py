from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from src.app.api.deps import phones_service
from src.app.schemas.addresses import AddressOut
from src.app.schemas.addresses import PhoneAddressDataIn
from src.app.schemas.addresses import PhoneAddressDataOut
from src.app.services.phones.service import PhonesService

router = APIRouter(tags=["Phones"], prefix="/phones")


@router.get("/{phone}", response_model=AddressOut, status_code=status.HTTP_200_OK)
async def get_address(phone: str, service: Annotated[PhonesService, Depends(phones_service)]) -> AddressOut:
    """Get Address by Phone number"""

    return await service.address(phone=phone)


@router.post("/create", response_model=PhoneAddressDataOut, status_code=status.HTTP_201_CREATED)
async def create_phone_address(
    data: PhoneAddressDataIn, service: Annotated[PhonesService, Depends(phones_service)]
) -> PhoneAddressDataOut:
    """Create new Phone and Address"""

    return await service.create(data=data)


@router.put("/update", response_model=PhoneAddressDataOut, status_code=status.HTTP_200_OK)
async def update_phone_address(
    data: PhoneAddressDataIn, service: Annotated[PhonesService, Depends(phones_service)]
) -> PhoneAddressDataOut:
    """Update existing address by phone"""

    return await service.update(data=data)


@router.delete("/delete", response_model=bool, status_code=status.HTTP_204_NO_CONTENT)
async def delete_phone_address(service: Annotated[PhonesService, Depends(phones_service)]) -> bool:
    """Delete all old records from cache"""

    return await service.delete()
