from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from module2.database import Base
from module2.books.models.client import Client
from datetime import datetime


class Buy(Base):
    """ Пожелания покупателя и id клиента """
    __tablename__ = "buy"

    id = Column(Integer, primary_key=True)
    buy_description = (Column(Text))
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)

    client = relationship("Client", back_populates="buys")


Client.buys = relationship("Buy", back_populates="client")


class BuyBook(Base):
    """ Таблица с количеством заказа покупателей, id книг и таблицы с данными клиента """
    __tablename__ = "buy_book"

    id = Column(Integer, primary_key=True)
    buy_id = Column(Integer, ForeignKey("buy.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    amount = Column(Integer, default=0, nullable=False)


class Step(Base):
    """ Этапы обработки заказа клиента """
    __tablename__ = "step"

    id = Column(Integer, primary_key=True)
    name_step = Column(String(255), nullable=False)


class BuyStep(Base):
    """ Даты начала и окончания этапов обработки заказа с id данными клиента и этапа """
    __tablename__ = "buy_step"

    id = Column(Integer, primary_key=True)
    buy_id = Column(Integer, ForeignKey("buy.id"), nullable=False)
    step_id = Column(Integer, ForeignKey("step.id"), nullable=False)
    date_step_beg = Column(DateTime, default=datetime.now, nullable=False)
    date_step_end = Column(DateTime, nullable=True)
