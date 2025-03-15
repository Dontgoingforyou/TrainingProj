from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.future import select
from module2.base import Base


async def clean_data(data):
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
    async def create(cls, session: AsyncSession, **kwargs):
        """Метод для создания объекта с обработкой данных перед сохранением"""

        kwargs["volume"] = await clean_data(kwargs.get("volume"))
        kwargs["total"] = await clean_data(kwargs.get("total"))
        kwargs["count"] = await clean_data(kwargs.get("count"))

        instance = cls(**kwargs)
        session.add(instance)
        await session.commit()
        return instance

    @classmethod
    async def get_all(cls, session: AsyncSession):
        """Метод для получения всех записей"""

        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int):
        """Метод для получения записи по id"""

        result = await session.execute(select(cls).filter_by(id=id))
        return result.scalar()