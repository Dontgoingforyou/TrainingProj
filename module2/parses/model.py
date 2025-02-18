from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Date, DateTime

from module2.base import Base
from module2.database import SessionLocal

session = SessionLocal()


def clean_data(data):
    """Очистка данных перед вставкой в базу данных"""
    try:
        # Преобразуем строки в числовые значения
        if isinstance(data, str):
            data = data.replace("\xa0", "").replace(" ", "").replace(",", ".")
        return float(data) if data else None
    except ValueError:
        return None  # Возвращаем None, если строка не может быть преобразована в число


class SpimexTradingResult(Base):
    """Модель для сохранения данных в БД."""
    __tablename__ = 'spimex_trading_results'

    id = Column(Integer, primary_key=True)
    exchange_product_id = Column(String)
    exchange_product_name = Column(String)
    oil_id = Column(String)
    delivery_basis_id = Column(String)
    delivery_basis_name = Column(String)
    delivery_type_id = Column(String)
    volume = Column(Float)
    total = Column(Float)
    count = Column(Integer)
    date = Column(Date)
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def create(cls, **kwargs):
        """Метод для создания объекта с обработкой данных перед сохранением"""

        kwargs["volume"] = clean_data(kwargs.get("volume"))
        kwargs["total"] = clean_data(kwargs.get("total"))
        kwargs["count"] = clean_data(kwargs.get("count"))

        instance = cls(**kwargs)
        session.add(instance)
        session.commit()
        return instance
