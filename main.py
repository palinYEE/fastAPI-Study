from fastapi import FastAPI
from enum import Enum           # Enum 클래스 생성하기 위한 라이브러리
from typing import Optional     # Optional 매개변수를 선언하기 위한 라이브러리


class ModelName(str, Enum):     # Enum 클래스 선언 (c언어의 구조체와 매우 비슷하다.)
    alexnet = 'alexnet'
    resnet = "resnet"
    lenet = 'lenet'

fake_items_db = [{"item_name" : "Foo"}, {"item_name" : "Bar"}, {"item_name" : "Baz"}]

app = FastAPI()         # fastAPI 객채 선언

# firstStep
@app.get('/')
async def root():
    return {"message" : "Hello world"}

# 매개변수
# @app.get('/items/{item_id}')
# async def read_item(item_id: int):
#     return {"item_id": item_id}

# 유저에 대한 정보를 리턴할 경우 자기 자신에 대한 것 먼저 넣어야 한다. 
@app.get('/users/me')
async def read_user_me():
    return {"user_id" : "the current user"}

@app.get('/users/{user_id}')
async def read_user(user_id: str):
    return {"user_id" : user_id}

# Enum 자료형을 이용
@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name" : model_name, "message" : "Deep Learning FTW!"}
    
    if model_name.value == 'lenet':
        return {"model_name" : model_name, "message" : "LeCNN all the images"}

    return {"model_name" : model_name, "message" : "Have some residuals"}

# 파일 경로 선언
@app.get('/files/{file_path:path}')
async def read_file(file_path:str):
    return {"file_path" : file_path}


# 쿼리 매개변수
# @app.get('/items/')         # http://127.0.0.1:8000/items/?skip=0&limit=1 이와 같이 함수에 정의한 것을 가지고 url 파라미터를 넣을 수 있음
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip:skip + limit]

# 선택적 매개변수
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}