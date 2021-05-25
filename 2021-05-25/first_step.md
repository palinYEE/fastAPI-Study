# 2021-05-25 

## fastAPI란?

Fast APi는 현재 파이썬 웹 프레임워크 중 가장 빠른 것중 하나이다. 이에 대한 특징은 다음과 같다. 
- Fast
- Fast to Code
- Fewer bugs
- Intuitive
- Easy
- Short
- Robust
- Standards-based


## 설치

```
$ python -m pip install fastapi             // fastAPI 설치
```

```
$ python -m pip install uvicorn             // 서버 역할을 해줄 uvicorn 설치
```

## 실행

```
$ uvicorn main:app --reload
```

## First Step 

```
from fastapi import FastAPI

app = FastAPI()         # fastAPI 객채 선언

@app.get('/')           # 데코레디터 정의. 여기서는 경로를 설정해준다. 
async def root():
    return {"message" : "Hello world"}
```

여기서 데코레이터 종류는 다음과 같다. 
 - `@app.post()`
 - `@app.put()`
 - `@app.delete()`
 - `@app.options()`
 - `@app.head()`
 - `@app.patch()`
 - `@app.trace()`

위 코드를 실행 시키면 웹 서버가 생성되는데, 기본 포트는 8000번 이다.

## 매개변수 삽입

```
# 매개변수
@app.get('/items/{item_id}') <-- {} 안에 있는 변수로 입력 받는다. 변수 자료형은 함수에서 선언
async def read_item(item_id: int):
    return {"item_id": item_id}

# 유저에 대한 정보를 리턴할 경우 자기 자신에 대한 것 먼저 넣어야 한다. 
@app.get('/users/me')
async def read_user_me():
    return {"user_id" : "the current user"}

@app.get('/users/{user_id}')
async def read_user(user_id: str):
    return {"user_id" : user_id}
```
여기서 주의할 점은 다른 사람에 대한 정보와 나 자신에 대한 정보 두개의 함수가 있을 경우, 고정 값인 함수(나 자신의 대한 정보)를 먼저 선언한다.

## Enum 클래스 사용

 - 사용 라이브러리 : `from enum import Enum`
 - 사용 예제 :
    ```
        class ModelName(str, Enum):     # Enum 클래스 선언 (c언어의 구조체와 매우 비슷하다.)
        alexnet = 'alexnet'
        resnet = "resnet"
        lenet = 'lenet'
    ```

```
# Enum 자료형을 이용
@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name" : model_name, "message" : "Deep Learning FTW!"}
    
    if model_name.value == 'lenet':
        return {"model_name" : model_name, "message" : "LeCNN all the images"}

    return {"model_name" : model_name, "message" : "Have some residuals"}
```

## 파일 경로
```
@app.get('/files/{file_path:path}')
async def read_file(file_path:str):
    return {"file_path" : file_path}
```
자료형을 `path`로 선언하여 `files/` 이후에 나오는 경로는 `str`으로 인식하게 한다.

## 쿼리 매개변수

일단 다음 리스트를 선언하자.
```
fake_items_db = [{"item_name" : "Foo"}, {"item_name" : "Bar"}, {"item_name" : "Baz"}]
```
이를 이용해서 다음 함수를 선언하자.
```
@app.get('/items/')         
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip:skip + limit]
```
http://127.0.0.1:8000/items/?skip=0&limit=1을 통해서 `fake_items_db`에 있는 데이터를 가져올 수 있다. 

### 선택적 매개변수

위 코드에서 더 나아가 매개변수의 자료형을 고정하지 않고 선택적 매개변수를 선언할 수 있다. 
```
from typing import Optional

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```
http://127.0.0.1:8000/items/asdasd?q=aslkdjasldkj 이렇게 하면 된다.