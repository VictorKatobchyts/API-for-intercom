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
### post-запрос добавить пользователя http://127.0.0.1:8000/add_client (вместе с добавлением пользователя автоматически отправляется СМС с логином и паролем пользователя на номер, указанный в поле "phone", поле "phone" должно содержать в том числе и код страны (можно и с симмволом '+'))
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
### put-запрос на изменение фамилии в базе данных пользоватлей http://127.0.0.1:8000/update_second_name/id
, где id - id-пользователя в базе биллинга<br />
Request body
*{
  "second_name": "string"
}*
### put-запрос на изменение отчества в базе данных пользоватлей http://127.0.0.1:8000/update_patronymic/id
, где id - id-пользователя в базе биллинга<br />
Request body
*{
  "patronymic": "string"
}*
### put-запрос на изменение номера договора в базе данных пользоватлей http://127.0.0.1:8000/update_contract_number/id
, где id - id-пользователя в базе биллинга<br />
Request body
*{
  "contract_number": "string"
}*
### put-запрос на изменение телефона в базе данных пользоватлей http://127.0.0.1:8000/update_phone/id
, где id - id-пользователя в базе биллинга<br />
Request body
*{
  "phone": "string"
}*
### put-запрос на изменение пароля в базе данных пользоватлей http://127.0.0.1:8000/update_password/id
, где id - id-пользователя в базе биллинга<br />
Request body
*{
  "password": "string"
}*
### put-запрос на изменение города в базе данных пользоватлей http://127.0.0.1:8000/update_city/id
, где id - id-пользователя в базе биллинга<br />
Request body
*{
  "city": "string"
}*
### put-запрос на изменение улицы в базе данных пользоватлей http://127.0.0.1:8000/update_street/id
, где id - id-пользователя в базе биллинга<br />
Request body
*{
  "street": "string"
}*
### put-запрос на изменение номера дома в базе данных пользоватлей http://127.0.0.1:8000/update_house/id
, где id - id-пользователя в базе биллинга<br />
Request body
*{
  "house": "string"
}*
### put-запрос на изменение подъезда в базе данных пользоватлей http://127.0.0.1:8000/update_entrance/id
, где id - id-пользователя в базе биллинга<br />
Request body
*{
  "entrance": "string"
}*
### put-запрос на изменение номера квартиры в базе данных пользоватлей http://127.0.0.1:8000/update_flat/id
, где id - id-пользователя в базе биллинга<br />
Request body
*{
  "flat": "string"
}*
### put-запрос на изменение нескольких данных в базе данных пользоватлей http://127.0.0.1:8000/update_client_information/id
, где id - id-пользователя в базе биллинга (в запросе отправляются все данные - измененные и не измененные в определенной последовательности)<br />
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
### post-запрос на открытие двери тестового домофона (Котовского 9) http://127.0.0.1:8000/open_door
