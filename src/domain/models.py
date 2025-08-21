from pydantic import BaseModel, Field
from typing import List

class Record(BaseModel):
    text: str = Field(..., min_length=1)
    date: str
    time: str
    click_number: int = Field(..., ge=0)

class StoredRecord(Record):
    id: int

class RecordsResponse(BaseModel):
    records: List[StoredRecord]
    total: int