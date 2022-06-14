# API-for-intercom
Вся документация на текущее API по ссылкам (выбирай любую):http://127.0.0.1:8000/docs http://127.0.0.1:8000/redoc
### post-запрос добавить домофон http://127.0.0.1:8000/add_intercom
Request body
*{
  "city": "string",
  "street": "string",
  "house": "string",
  "entrance": "string",
  "ip": "string",
  "mac": "string"
}*
### post-запрос добавить пользователя http://127.0.0.1:8000/add_client
Request body
*{
  "contract_id": "string",
  "first_name": "string",
  "second_name": "string",
  "patronymic": "string",
  "contract_number": "string",
  "contract_date": "string",
  "phone": "string",
  "password": "string",
  "city": "string",
  "street": "string",
  "house": "string",
  "entrance": "string",
  "flat": "string",
  "contract_status": "string"
}*
### delete-запрос удалить домофон http://127.0.0.1:8000/delete_intercom/id
, где id - id-домофона в базе данных домофонов
### delete-запрос удалить пользователя http://127.0.0.1:8000/delete_client/id
, где id - id-пользователя в базе биллинга
### put-запрос на изменение статуса договора в базе данных пользоватлей http://127.0.0.1:8000/update_contract_status/id
, где id - id-пользователя в базе биллинга<br />
Request body
*{
  "contract_status": "string"
}*
### put-запрос на изменение имени в базе данных пользоватлей http://127.0.0.1:8000/update_first_name/id
, где id - id-пользователя в базе биллинга<br />
Request body
*{
  "first_name": "string"
}*
