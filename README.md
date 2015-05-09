# prochats
chats wrapper application for VK

API: client <–> server

**POST /register**

parameters:
* vk_token

response:
```json
{
    "token": "<token>",
    "status": {
        "code": "<status_code>",
	"message": "<message>"
    }
}
```

**POST /update**

parameters:
* sdk_token
* vk_token

response:
```json
{
    "token": "<token>",
    "status": {
        "code": "<status_code>",
	"message": "<message>"
    }
}
```

**GET /tags**

parameters:
* token
* chat_id
* timestamp – промежуток времени последнего запроса

response:  
```json
{  
   "tags":  [  
       {  
           "tag_id": "<tag_id>",  
           "name": "<tag_name>",  
           "mark": "<tag_mark>",  
       },  
       ...  
    ] ,  
    "status": {  
        "code": "<status_code>",  
        "message": "<message>"
    }    
}  
```

tags – отсортированные по убыванию частоты

**GET /messages (получить сообщения)**

parameters:
* token
* chat_id
* tag_ids – тэги через запятую

response:
```json
{
    "messages": [
        {
            "message_id": "<message_id>",
            "tag_id": "<tag_id>",
            "name": "<tag_name>"
        },  
        ...
    ],
    "status": {
        "code": "<status_code>",
	"message": "<message>"
    }
 }
```

**PUT /tags/<tag_id> (изменение статуса тэга)**

parameters:
* token
* tag_id
* mark [enum: unknown, interesting, flood]

response:
```json
{
    "status": {
        "code": "<status_code>",
	"message": "<message>"
    }
}
```

**POST /tags (создание тэга)**

parameters:
* token
* tag_name
* chat_id
* [mark=interesting] – interesting/flood.

response:
```json
{
    "tag_id": "<tag_id>",
    "status": {
        "code": "<status_code>",
	"message": "<message>"
    }
}
```

**DELETE /tags/<tag_id>  (удаление тэга)**

parameters:
* token
* tag_id

response:
```json
{
    "status": {
        "code": "<status_code>",
	"message": "<message>"
    }
}
```
