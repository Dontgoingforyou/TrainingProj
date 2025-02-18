from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from module2.database import Base


class City(Base):
    """ Город клиента и время доставки """
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name_city = Column(String(255), nullable=False)
    days_delivery = Column(Integer, nullable=False)


class Client(Base):
    """ Имя клиента, почта, id города """
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    name_client = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)

    city = relationship("City", back_populates="clients")


City.clients = relationship("Client", back_populates="city")
