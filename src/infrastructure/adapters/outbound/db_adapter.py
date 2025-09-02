from sqlalchemy import create_engine, Column, Integer, String, Index
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import List, Tuple
from src.domain.models import Record, StoredRecord
from src.domain.ports.outbound.db_port import DbPort
from src.domain.exceptions import DatabaseError
from dotenv import load_dotenv
import os
import logging
from src.infrastructure.config.settings import settings

load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class DbRecord(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    click_number = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<DbRecord(id={self.id}, text='{self.text}', date='{self.date}', time='{self.time}', click_number={self.click_number})>"

# Добавляем индексы для оптимизации
Index('idx_records_id', DbRecord.id)
Index('idx_records_date_time', DbRecord.date, DbRecord.time)

class DbAdapter(DbPort):
    def __init__(self, db_url: str | None = None):
        self.engine = create_engine(db_url or settings.db_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logger.info(f"Адаптер базы данных инициализирован с URL: {db_url or settings.db_url}")

    def save(self, record: Record) -> None:
        session = self.Session()
        try:
            db_record = DbRecord(**record.model_dump())
            session.add(db_record)
            session.commit()
            logger.info(f"Запись успешно сохранена: {db_record}")
        except Exception as e:
            session.rollback()
            logger.error(f"Ошибка сохранения записи: {e}")
            raise DatabaseError(f"Ошибка сохранения записи: {e}")
        finally:
            session.close()

    def get_all(self, page: int, limit: int) -> Tuple[List[StoredRecord], int]:
        # Проверка параметров пагинации
        if page < 1:
            page = 1
        if limit < 1:
            limit = 10
            
        session = self.Session()
        try:
            total = session.query(DbRecord).count()
            offset = (page - 1) * limit
            db_records = session.query(DbRecord).order_by(DbRecord.id.desc()).offset(offset).limit(limit).all()
            records = [StoredRecord(id=r.id, text=r.text, date=r.date, time=r.time, click_number=r.click_number) for r in db_records]
            logger.info(f"Получено {len(records)} записей (страница {page}, лимит {limit})")
            return records, total
        except Exception as e:
            logger.error(f"Ошибка получения записей: {e}")
            raise DatabaseError(f"Ошибка получения записей: {e}")
        finally:
            session.close()