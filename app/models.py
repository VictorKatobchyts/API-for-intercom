from sqlalchemy import Column, Integer, String, Date
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
    contract_status = Column(String, nullable=True)

class Intercom(Base):
    __tablename__ = "intercoms"
    intercom_id = Column(Integer, primary_key=True, nullable=False)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    house = Column(String, nullable=False)
    entrance = Column(String, nullable=True)
    ip = Column(String, nullable=False)
    mac = Column(String, nullable=False)



