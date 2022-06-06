from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, nullable=False) 
    billing_bd_id = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    contract_number = Column(String, nullable=False)
    inclusion_date = Column(Date, nullable=False)
    mobile_number = Column(String, nullable=False)
    login = Column(String, nullable=False)
    user_password = Column(String, nullable=False)
    city = Column(String, nullable=False)
    street_name = Column(String, nullable=False)
    home_number = Column(String, nullable=False)
    entrance_number = Column(String, nullable=True)
    apartment_number = Column(Integer, nullable=False)
    status_contract = Column(String, nullable=False)

class Intercom(Base):
    __tablename__ = "intercoms"
    intercom_id = Column(Integer, primary_key=True, nullable=False)
    city = Column(String, nullable=False)
    street_name = Column(String, nullable=False)
    home_number = Column(String, nullable=False)
    entrance_number = Column(String, nullable=True)
    ip = Column(String, nullable=False)
    mac = Column(String, nullable=False)



