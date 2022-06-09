from pydantic import BaseModel

class Intercom (BaseModel):
    city: str
    street: str
    house: str
    entrance: str
    ip: str
    mac: str

class Client (BaseModel):
    contract_id: str
    first_name: str
    second_name: str
    patronymic: str
    contract_number: str
    contract_date: str
    phone: str
    password: str
    city: str
    street: str
    house: str
    entrance: str
    flat: str
    contract_status: str

class Update_Contract_status (BaseModel):
    contract_status: str