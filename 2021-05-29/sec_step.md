# 2021-05-29

## 쿼리 매개변수 형 변환
```
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
```
위 코드를 통해서 매개변수 short를 bool로 선언할 수 있다. 이제 더 나아가 여러 경로/쿼리 매개변수에 대해서 보자. 

```
# 여러 경로/쿼리 매개변수
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q : Optional[str] = None, short: bool=False):
    item = {"item_id" : item_id, "owner_id" : user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({'decription' : "This is an amazing item that has a long description"})
    return item
```
이 코드를 통해서 여러 경로에 해당하는 변수를 입력 받아 쿼리 매개변수를 셋팅할 수 있다. 

```
@app.get("/items_must/{item_id}")
async def read_user_item_must(item_id:str, needy:str, skip:int=0, limit: Optional[int] = None):
    item = {"item_id" : item_id, "needy" : needy, "skip" : skip, "limit" : limit}
    return item
```
위 코드처럼 필수로 들어가는 옵션을 여러개 셋팅할 수 있다. 

## Request Body
이 부분에 대해서 하기 위해서는 다음과 같은 라이브러리를 입포트 해주어야 한다. 
```
from pydantic import BaseModel
```
클래스 선언
```
class Item(BaseModel):          # Request Body 실습을 위한 class 선언 
    name : str
    decripyion : Optional[str] = None
    price: float
    tax: Optional[float] = None
```

코드 
```
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
```

## 쿼리 매개 변수 및 문자열 유효성 검사
사용 라이브러리
```
from fastapi import Query
```
```
@app.get("/validation/")
async def read_val(q: Optional[str] = Query(None,min_length=3 ,max_length = 50, regex = "^fixedquery$")): #
    result = {"items" : [{"item_id": "Foo"}, {"item_id" : "Bar"}]}
    if q:
        result.update({"q" : q})
    return result
```
이처럼 입력되는 쿼리의 최소 길이, 최대 길이, 정규식 등을 이용해서 유효성 검사를 진행할 수 있다. 

```
from typing import List
```
를 사용해서 쿼리 매개변수를 여러개 입력받게 할 수 있다.
```
@app.get("/items/")
async def read_items(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items
```
