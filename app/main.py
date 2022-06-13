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
    new_phone = client_information.phone
    send_sms(new_phone.translate({ord(i): None for i in '+'}), client_information.contract_number, client_information.password)#отправка SMS, для телефона используется функция убирающая символ '+'
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

@app.put("/update_first_name/{id}")
def update_first_name(id: int, updated_first_name: schemas.Update_first_name, db: Session = Depends(get_db)):
    update_first_name = db.query(models.Client).filter(models.Client.contract_id == id)
    new_first_name = update_first_name.first()
    if new_first_name == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"client with id: {id} does not exist")
    update_first_name.update(updated_first_name.dict(), synchronize_session=False)
    db.commit()
    return  update_first_name.first()

@app.put("/update_second_name/{id}")
def update_second_name(id: int, updated_second_name: schemas.Update_second_name, db: Session = Depends(get_db)):
    update_second_name = db.query(models.Client).filter(models.Client.contract_id == id)
    new_second_name = update_second_name.first()
    if new_second_name == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"client with id: {id} does not exist")
    update_second_name.update(updated_second_name.dict(), synchronize_session=False)
    db.commit()
    return  update_second_name.first()

@app.put("/update_patronymic/{id}")
def update_patronymic(id: int, updated_patronymic: schemas.Update_patronymic, db: Session = Depends(get_db)):
    update_patronymic = db.query(models.Client).filter(models.Client.contract_id == id)
    new_patronymic = update_patronymic.first()
    if new_patronymic == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"client with id: {id} does not exist")
    update_patronymic.update(updated_patronymic.dict(), synchronize_session=False)
    db.commit()
    return  update_patronymic.first()

@app.put("/update_contract_number/{id}")
def update_contract_number(id: int, updated_contract_number: schemas.Update_contract_number, db: Session = Depends(get_db)):
    update_contract_number = db.query(models.Client).filter(models.Client.contract_id == id)
    new_contract_number = update_contract_number.first()
    if new_contract_number == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"client with id: {id} does not exist")
    update_contract_number.update(updated_contract_number.dict(), synchronize_session=False)
    db.commit()
    return  update_contract_number.first()

@app.put("/update_password/{id}")
def update_password(id: int, updated_password: schemas.Update_password, db: Session = Depends(get_db)):
    update_password = db.query(models.Client).filter(models.Client.contract_id == id)
    new_password = update_password.first()
    if new_password == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"client with id: {id} does not exist")
    update_password.update(updated_password.dict(), synchronize_session=False)
    db.commit()
    return  update_password.first()

@app.put("/update_city/{id}")
def update_city(id: int, updated_city: schemas.Update_city, db: Session = Depends(get_db)):
    update_city = db.query(models.Client).filter(models.Client.contract_id == id)
    new_city = update_city.first()
    if new_city == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"client with id: {id} does not exist")
    update_city.update(updated_city.dict(), synchronize_session=False)
    db.commit()
    return  update_city.first()

@app.put("/update_street/{id}")
def update_street(id: int, updated_street: schemas.Update_street, db: Session = Depends(get_db)):
    update_street = db.query(models.Client).filter(models.Client.contract_id == id)
    new_street = update_street.first()
    if new_street == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"client with id: {id} does not exist")
    update_street.update(updated_street.dict(), synchronize_session=False)
    db.commit()
    return  update_street.first()

@app.put("/update_house/{id}")
def update_house(id: int, updated_house: schemas.Update_house, db: Session = Depends(get_db)):
    update_house = db.query(models.Client).filter(models.Client.contract_id == id)
    new_house = update_house.first()
    if new_house == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"client with id: {id} does not exist")
    update_house.update(updated_house.dict(), synchronize_session=False)
    db.commit()
    return  update_house.first()

@app.put("/update_entrance/{id}")
def update_entrance(id: int, updated_entrance: schemas.Update_entrance, db: Session = Depends(get_db)):
    update_entrance = db.query(models.Client).filter(models.Client.contract_id == id)
    new_entrance = update_entrance.first()
    if new_entrance == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"client with id: {id} does not exist")
    update_entrance.update(updated_entrance.dict(), synchronize_session=False)
    db.commit()
    return  update_entrance.first()

@app.put("/update_flat/{id}")
def update_flat(id: int, updated_flat: schemas.Update_flat, db: Session = Depends(get_db)):
    update_flat = db.query(models.Client).filter(models.Client.contract_id == id)
    new_flat = update_flat.first()
    if new_flat == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"client with id: {id} does not exist")
    update_flat.update(updated_flat.dict(), synchronize_session=False)
    db.commit()
    return  update_flat.first()

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
# @app.post("/movements_in_camera")#скорее всего не актуальный запрос, чтобы отлавливать движения с камеры
#  def camera_movements():
def send_sms(phone, contract_number, password):#набросок http-запроса, чтобы смс отпраллась, пока мне
    #print(contract_number)
    payload = {'app': 'ws', 'u': 'onenet', 'h': 'cf3a89ee72eda9d7776c1a5777321a9a', 'op': 'pv', 'to': f'{phone}', 'msg': f'you login: {contract_number}\nyou password: {password}'}
    resolve = requests.get('http://sms.glan.by:50025/index.php', params=payload)
    #return {"message": "succesfully open"}  
    #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} apartment does not exist")