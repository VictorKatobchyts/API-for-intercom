from ast import Param
from email import message
from statistics import mode
from colorama import Cursor
from fastapi import  FastAPI, HTTPException, status, Response, Depends
from fastapi.params import Body
import requests
import psycopg2
from psycopg2.extras import RealDictCursor #штука нужна только для текущей бибилотеки для работы с бд
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'NewCRMBillingdb', user = 'postgres', password = 'vtajlbq1',
        cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)



@app.post("/add_intercom", status_code=status.HTTP_201_CREATED)
def get_domofone_adress(domofone_adress: schemas.Intercom, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO intercoms (city, street_name, home_number, entrance_number, ip, mac) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""", 
    # (domofone_adress.city, domofone_adress.street_name, domofone_adress.home_number, domofone_adress.entrance_number, domofone_adress.ip, domofone_adress.mac))
    # new_domofone = cursor.fetchall()
    # conn.commit()#каждый раз когда в базу посылаем новые данные, должны закоммитить их чтобы бд обновилась
    # **-для распаковки этого словаря
    new_domofone = models.Intercom(**domofone_adress.dict())#city=domofone_adress.city, street_name=domofone_adress.street_name, home_number=domofone_adress.home_number, entrance_number=domofone_adress.entrance_number, ip=domofone_adress.ip,mac= domofone_adress.mac
    db.add(new_domofone)#добавили в базу новый домофон
    db.commit()#закоммитили добавление
    db.refresh(new_domofone)
    return  new_domofone

@app.post("/add_client", status_code=status.HTTP_201_CREATED)
def get_client_information(client_information: schemas.Client, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO clients (billing_bd_id, first_name, second_name, patronymic, contract_number, inclusion_date, mobile_number, login, user_password,
    # city, street_name, home_number, entrance_number, apartment_number, status_contract) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *""", 
    # (client_information.billing_bd_id, client_information.first_name, client_information.second_name, client_information.patronymic, client_information.contract_number,
    # client_information.inclusion_date, client_information.mobile_number, client_information.login, client_information.user_password, client_information.city,
    # client_information.street_name, client_information.home_number, client_information.entrance_number, client_information.apartment_number, client_information.status_contract))
    # new_client = cursor.fetchall()
    # conn.commit()
    new_client= models.Client(**client_information.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return  new_client

@app.delete("/delete_client/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(id:int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM clients WHERE client_id = %s returning *""", (str(id)))
    # deleted_client = cursor.fetchall()
    # conn.commit()
    deleted_client = db.query(models.Client).filter(models.Client.client_id == id)
    if deleted_client.first() == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"client with id: {id} does not exist")
    deleted_client.delete(synchronize_session=False)#читай документацию SQLAlchemy
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete("/delete_intercom/{id}", status_code=status.HTTP_204_NO_CONTENT)#удаление информации о домофонах через id домофона
def delete_intercom(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM intercoms WHERE intercom_id = %s returning *""", (str(id)))#returning - чтобы показывало содержание удаленного домофона
    # deleted_intercom = cursor.fetchall()#чтобы получить этот удаленные данные домофона
    # conn.commit()
    deleted_intercom = db.query(models.Intercom).filter(models.Intercom.intercom_id == id)
    if deleted_intercom.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"intercom with id: {id} does not exist")
    deleted_intercom.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/update_status_contract/{id}")#запрос на обновление статуса договора
def update_status_contract(id: int, updated_contract_status: schemas.Update_Contract_status, db: Session = Depends(get_db)): 
    # cursor.execute("""UPDATE clients SET status_contract = %s WHERE billing_bd_id = %s RETURNING *""", (updated_status_contract.status_contract, id))
    # updated_client_information = cursor.fetchone()
    # conn.commit()
    update_contract_status = db.query(models.Client).filter(models.Client.contract_id == id)
    new_contract_status = update_contract_status.first()
    if new_contract_status == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"client with id: {id} does not exist")
    update_contract_status.update(updated_contract_status.dict(), synchronize_session=False)
    db.commit()
    return  update_contract_status.first()

@app.put("/update_client_information/{id}")#запрос на обновление информации об абоненте (принимает всю полностью инфу, даже не обновленную)
def update_client_information(id: int, updated_client_information: schemas.Client, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE clients SET billing_bd_id = %s, first_name = %s, second_name = %s, patronymic = %s, contract_number = %s, inclusion_date = %s, 
    # mobile_number = %s, login = %s, user_password = %s,city = %s, street_name = %s, home_number = %s, entrance_number = %s, apartment_number = %s, status_contract = %s 
    # WHERE billing_bd_id = %s RETURNING *""", (updated_client_information.billing_bd_id, updated_client_information.first_name, updated_client_information.second_name, 
    # updated_client_information.patronymic, updated_client_information.contract_number,updated_client_information.inclusion_date, updated_client_information.mobile_number, 
    # updated_client_information.login,  updated_client_information.user_password, updated_client_information.city, updated_client_information.street_name, 
    # updated_client_information.home_number, updated_client_information.entrance_number, updated_client_information.apartment_number, updated_client_information.status_contract, id))
    # updated_client_information = cursor.fetchone()
    # conn.commit()
    update_client_information = db.query(models.Client).filter(models.Client.contract_id == id)
    new_client_information = update_client_information.first()
    if new_client_information == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"client with id: {id} does not exist")
    update_client_information.update(updated_client_information.dict(), synchronize_session=False)
    db.commit()
    return  update_client_information.first()
@app.post("/open_door")   
def send_to_open():
    #?action=maindoor&user=admin&pwd=2c4d959166
        #первый запрос для истории http://172.22.1.67/cgi-bin/intercom_cgi?action=get&user=admin&pwd=2c4d959166
    payload = {'action': 'maindoor', 'user': 'admin', 'pwd': 'f90b381d9f'}
        #payload = {'action': 'get','user': 'admin', 'pwd': '2c4d959166'}
    resolve = requests.get('http://172.22.1.67/cgi-bin/intercom_cgi', params=payload)
    #payload1 = {'action': 'set', 'TickerText': 'vash internet', 'user': 'admin', 'pwd': 'f90b381d9f'}
        #payload1 = {'action': 'get', 'user': 'admin', 'pwd': '2c4d959166'}
    #resolve1 = requests.get ('http://172.22.1.67/cgi-bin/display_cgi', params=payload1)
        #payload2 = {'action': 'get', 'user': 'admin', 'pwd': '2c4d959166'}
        #resolve2 = requests.get('http://172.22.1.67/cgi-bin/display_cgi', params=payload2)
 
    print(resolve.url)
        #print(resolve1.url)
    return resolve.content
  
    #return {"message": "succesfully open"}
    
    #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} apartment does not exist")