import uuid
from abc import ABC, abstractmethod
from uuid import UUID


class UUIDProvider(ABC):
    @abstractmethod
    def uuid4(self) -> str:
        raise NotImplementedError


class FixedUUIDProvider(UUIDProvider):
    def __init__(self, fixed_uuid: UUID):
        self._fixed_uuid = fixed_uuid

    def uuid4(self) -> str:
        return str(self._fixed_uuid)


class SystemUUIDProvider(UUIDProvider):
    def uuid4(self) -> str:
        return str(uuid.uuid4())
