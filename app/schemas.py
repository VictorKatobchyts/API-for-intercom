from pydantic import BaseModel

class Intercom (BaseModel):
    city: str
    street_name: str
    home_number: str
    entrance_number: str
    ip: str
    mac: str

class Client (BaseModel):
    billing_bd_id: str
    first_name: str
    second_name: str
    patronymic: str
    contract_number: str
    inclusion_date: str
    mobile_number: str
    login: str
    user_password: str
    city: str
    street_name: str
    home_number: str
    entrance_number: str
    apartment_number: str
    status_contract: str
    
class Update_Status_contract (BaseModel):
    status_contract: str