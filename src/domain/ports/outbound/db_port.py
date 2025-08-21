from abc import ABC, abstractmethod
from typing import List, Tuple
from src.domain.models import Record, StoredRecord

class DbPort(ABC):
    @abstractmethod
    def save(self, record: Record) -> None:
        pass

    @abstractmethod
    def get_all(self, page: int, limit: int) -> Tuple[List[StoredRecord], int]:
        pass