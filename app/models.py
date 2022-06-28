from datetime import datetime
from xmlrpc.client import DateTime
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from .database import Base

class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, nullable=True) 
    contract_id = Column(Integer, nullable=True)#id  в базе данных биллинга
    first_name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    patronymic = Column(String, nullable=True)
    contract_number = Column(String, nullable=True) #=login
    contract_date = Column(Date, nullable=True)#дата включения абонента
    phone = Column(String, nullable=True)#номер телефона
    password = Column(String, nullable=True)
    city = Column(String, nullable=True)
    street = Column(String, nullable=True)#название улицы
    house = Column(String, nullable=True)#номер дома
    entrance = Column(String, nullable=True)#номер подъезда
    flat = Column(Integer, nullable=True)#номер квартиры
    letter = Column(String, nullable=True)#литера (буква в номере квартиры, если например общага)
    contract_status = Column(String, nullable=True)

class Intercom(Base):
    __tablename__ = "intercoms"
    intercom_id = Column(Integer, primary_key=True, nullable=False)
    entrance = Column(String, nullable=True)
    ip = Column(String, nullable=False)
    mac = Column(String, nullable=False)
    home_id = Column(Integer, ForeignKey("homes.id"))

class Home(Base):
    __tablename__ = "homes"
    home_id = Column(Integer, primary_key=True, nullable=False)
    date_registration = Column(DateTime, nullable=False) #дата регистрации дома (и время тоже нужно)
    city = Column(String, nullable=False)#город
    area = Column(String, nullable=True)#район 
    street = Column(String, nullable=False)#название улицы
    house = Column(String, nullable=False)#номер дома
    intercom = relationship("Intercom")



