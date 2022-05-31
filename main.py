from ast import Param
from fastapi import Body, FastAPI, HTTPException, status
from pydantic import BaseModel
import requests
app = FastAPI()
class Post (BaseModel):
    Ip: str
    MAC: str
    adress: str

@app.post("/{id}")
@app.post("/post")

def get_domofone_adress(full_domofone_adress: Post):
    print(full_domofone_adress.adress)
    
def send_to_open(id):
    if id == '25':#?action=maindoor&user=admin&pwd=2c4d959166
        #первый запрос для истории http://172.22.1.67/cgi-bin/intercom_cgi?action=get&user=admin&pwd=2c4d959166
        payload = {'action': 'set', 'DoorOpenSipFail': 'off', 'DoorCodeActive': 'off', 'user': 'admin', 'pwd': '2c4d959166'}
        #payload = {'action': 'get','user': 'admin', 'pwd': '2c4d959166'}
        resolve = requests.get('http://172.22.1.67/cgi-bin/intercom_cgi', params=payload)
        #payload1 = {'action': 'set', 'TickerText': 'vash internet', 'user': 'admin', 'pwd': '2c4d959166'}
        #payload1 = {'action': 'get', 'user': 'admin', 'pwd': '2c4d959166'}
        #resolve1 = requests.get ('http://172.22.1.67/cgi-bin/display_cgi', params=payload1)
        #payload2 = {'action': 'get', 'user': 'admin', 'pwd': '2c4d959166'}
        #resolve2 = requests.get('http://172.22.1.67/cgi-bin/display_cgi', params=payload2)

        print(resolve.url)
        #print(resolve1.url)
        return resolve.content
    #return {"message": "succesfully open"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} apartment does not exist")