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

class Update_first_name (BaseModel):
    first_name: str

class Update_second_name (BaseModel):
    second_name: str

class Update_patronymic (BaseModel):
    patronymic: str

class Update_contract_number (BaseModel):
    contract_number: str

class Update_phone (BaseModel):
    phone: str

class Update_password (BaseModel):
    password: str

class Update_city (BaseModel):
    city: str

class Update_street (BaseModel):
    street: str

class Update_house (BaseModel):
    house: str

class Update_entrance (BaseModel):
     entrance: str

class Update_flat (BaseModel):
    flat: str




