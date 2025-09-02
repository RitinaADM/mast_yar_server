from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List
from datetime import datetime

class Record(BaseModel):
    """
    Модель, представляющая запись с текстом, датой, временем и количеством кликов.
    """
    text: str = Field(..., min_length=1, max_length=1000, description="Текстовое содержимое записи")
    date: str = Field(..., description="Дата в формате ГГГГ-ММ-ДД")
    time: str = Field(..., description="Время в формате ЧЧ:ММ:СС")
    click_number: int = Field(..., ge=0, description="Количество кликов (неотрицательное)")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "text": "Пример текста записи",
            "date": "2025-08-20",
            "time": "12:00:00",
            "click_number": 1
        }
    })

    @field_validator('date')
    def validate_date(cls, v):
        """Проверка формата даты"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Дата должна быть в формате ГГГГ-ММ-ДД')
        return v

    @field_validator('time')
    def validate_time(cls, v):
        """Проверка формата времени"""
        try:
            datetime.strptime(v, '%H:%M:%S')
        except ValueError:
            raise ValueError('Время должно быть в формате ЧЧ:ММ:СС')
        return v

class StoredRecord(Record):
    """
    Модель, представляющая сохраненную запись с идентификатором.
    """
    id: int = Field(..., description="Уникальный идентификатор записи")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": 1,
            "text": "Пример текста записи",
            "date": "2025-08-20",
            "time": "12:00:00",
            "click_number": 1
        }
    })

class RecordsResponse(BaseModel):
    """
    Модель, представляющая ответ с записями и общим количеством.
    """
    records: List[StoredRecord] = Field(..., description="Список записей")
    total: int = Field(..., description="Общее количество записей")