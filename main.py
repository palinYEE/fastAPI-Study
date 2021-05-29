from fastapi import FastAPI, Query
from enum import Enum           # Enum 클래스 생성하기 위한 라이브러리
from typing import List, Optional     # Optional 매개변수를 선언하기 위한 라이브러리
from pydantic import BaseModel  # Request Body 실습을 위한 라이브러리 

class ModelName(str, Enum):     # Enum 클래스 선언 (c언어의 구조체와 매우 비슷하다.)
    alexnet = 'alexnet'
    resnet = "resnet"
    lenet = 'lenet'

class Item(BaseModel):          # Request Body 실습을 위한 class 선언 
    name : str
    decripyion : Optional[str] = None
    price: float
    tax: Optional[float] = None

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
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Optional[str] = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}

# 쿼리 매개변수 형변환
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id" : item_id}
    if q:
        item.update({"q" : q})
    if not short:
        item.update(
            {'decription' : "This is an amazing item that has a long description"}
        )
    return item

# 여러 경로/쿼리 매개변수
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q : Optional[str] = None, short: bool=False):
    item = {"item_id" : item_id, "owner_id" : user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({'decription' : "This is an amazing item that has a long description"})
    return item


# 필수 쿼리 매개변수
# @app.get("/items_must/{item_id}")
# async def read_user_item_must(item_id:str, needy:str):
#     item = {"item_id" : item_id, "needy" : needy}
#     return item

# 필수 쿼리 매개변수 2
@app.get("/items_must/{item_id}")
async def read_user_item_must(item_id:str, needy:str, skip:int=0, limit: Optional[int] = None):
    item = {"item_id" : item_id, "needy" : needy, "skip" : skip, "limit" : limit}
    return item

# request Body
@app.get("/items/")
async def create(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax" : price_with_tax})
    return item_dict

@app.get("/items/{item_id}")
async def create_item(item_id: int, item:Item, q:Optional[str] = None):
    result = {"item_id" : item_id, **item.dict()}
    if q:
        result.update({"q":q})
    return result

# 유효성 검사 
# @app.get("/validation/")
# async def read_val(q: Optional[str] = None):
#     result = {"items" : [{"item_id": "Foo"}, {"item_id" : "Bar"}]}
#     if q:
#         result.update({"q" : q})
#     return result

# @app.get("/validation/")
# async def read_val(q: Optional[str] = Query(None,min_length=3 ,max_length = 50, regex = "^fixedquery$")): #
#     result = {"items" : [{"item_id": "Foo"}, {"item_id" : "Bar"}]}
#     if q:
#         result.update({"q" : q})
#     return result

@app.get("/items/")
async def read_items(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items