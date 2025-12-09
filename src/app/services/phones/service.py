import orjson

from src.app.api.exceptions import AddressAlreadyExists
from src.app.api.exceptions import AddressNotFound
from src.app.api.exceptions import PhoneNotFound
from src.app.schemas.addresses import AddressOut
from src.app.schemas.addresses import AddressToDelete
from src.app.schemas.addresses import PhoneAddressDataIn
from src.app.schemas.addresses import PhoneAddressDataOut
from src.app.services.cache.service import CacheService


class PhonesService:
    """Service for working with phones"""

    def __init__(self, database: CacheService) -> None:
        self.database = database

        self.address_key: str = "phones:{phone}"
        self.default_ttl_for_update: int = 86_400

    async def address(self, phone: str) -> str:
        """Get Address by Phone number"""

        # Try to get data from cache
        result = await self.database.get(key=self.address_key.format(phone=phone))

        # If result not exists raise 404
        if not result:
            raise AddressNotFound()

        # Return validated data
        return AddressOut.model_validate(orjson.loads(result))

    async def create(self, data: PhoneAddressDataIn) -> PhoneAddressDataOut:
        """Create new Phone and Address"""

        # Init cache key
        cache_key: str = self.address_key.format(phone=data.phone)

        exists = await self._exists(data.phone)

        if exists:

            # Обновляем TTL, хоть о нём и не говорилось в ТЗ, я бы тут уточнил требования
            await self.database.update_ttl(key=cache_key, ttl=self.default_ttl_for_update)

            # Обновляем само значение по номеру телефона
            await self.database.update(key=cache_key, data=data)

            # Либо возвращаем 409-ую
            raise AddressAlreadyExists()

        # Set new data in cache
        await self.database.set(key=cache_key, data=data.model_dump())

        return PhoneAddressDataOut(message=f"Phone ({data.phone}) & Address ({data.address}) is successfully created")

    async def update(self, data: PhoneAddressDataIn) -> PhoneAddressDataOut:
        """Update existing Address by Phone number"""

        cache_key: str = self.address_key.format(phone=data.phone)

        exists = await self._exists(cache_key=cache_key)

        if not exists:
            raise PhoneNotFound()

        await self.database.update(key=cache_key, data=data.model_dump())

        return PhoneAddressDataOut(message=f"Address ({data.address}) is successfully updated")

    async def delete_all(self) -> bool:
        """Delete old rows from cache"""

        return await self.database.drop_all_old_records()

    async def delete(self, data: AddressToDelete) -> None:
        """Delete Address by Phone number"""

        return await self.database.drop(data.phone)

    async def _exists(self, cache_key: str) -> bool:
        """Check if value exists in cache"""

        # Try to get value from cache
        exists = await self.database.get(key=cache_key)

        return exists is not None
