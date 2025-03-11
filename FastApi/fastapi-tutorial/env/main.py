# from enum import Enum
# from typing import Optional,List,Literal
# from fastapi import FastAPI,Query,Path,Body,Cookie,Header
# from pydantic import BaseModel
# from uuid import UUID
# from datetime import datetime,timedelta,time

# app = FastAPI()

# print("🚀 FastAPI server is running!")


# @app.get("/")
# async def root():
#     return {"message": "Hello, FastAPI!"}

# @app.post("/")
# async def post():
#     return {"message":"Hello from the post route"}

# @app.put("/")
# async def put():
#     return {"message":"hello from the put route"}

# @app.get("/users")
# async def list_users():
#     return {"message":"list users route"}

# @app.get("/users/{user_id}")
# async def get_user(user_id:str):
#     return {"user_id":user_id}

# @app.get("/user/me")
# async def get_current_user():
#     return {"Message":"This is the current user"}


# class FoodEnum(str,Enum):
#     fruits="fruits"
#     vegetables = "vegetables"
#     dairy="dairy"

# @app.get("/foods/{food_name}")
# async def get_food(food_name:FoodEnum):
#     if food_name == FoodEnum.vegetables:
#         return {"food_name":food_name,
#                 "message":"you are healthy"}
#     if food_name.value == "fruits":
#         return{
#             "food_name":food_name,
#             "message":"you are still healthy,but like sweet things",   
#         }
#     return {"food_name":food_name,
#             "message":"i like chocolate milk"}


# fake_items_db = [{"item_name":"Foo"},{"item_name":"Bar"},{"item_name":"Baz"}]

# @app.get("/items")
# async def list_items(skip:int=0,limit:int=10):
#     return fake_items_db[skip:skip+limit]


# @app.get("/items/{item_id}")
# async def get_item(item_id:str,q:Optional[str]=None,short:bool=False):
#     item ={"item_id":item_id}

#     if q:
#         item.update({"q":q})
#     if not short:
#         item.update(
#             {
#                 "description":"11111111"
#             }
#         )
#     return item

# @app.get("/users/{user_id}/items/{item_id}")
# async def get_user_item(item_id:str,user_id:str,q:Optional[str]=None,short:bool=False):
#     item = {"item_id":item_id,"Owner_id":user_id}
#     if q:
#         item.update({"q":q})
#     if not short:
#         item.update(
#             {
#                 "description":"sssssssssssssss"
#             }
#         )
#     return  item


# class Item(BaseModel):
#     name:str
#     description:Optional[str]=None
#     price:int
#     tax:Optional[float]=None


# @app.post("/items")
# async def create_item(item:Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax":price_with_tax})
#     return item_dict

# # **item.dict() 解包了 item.dict() 的键值对，并把它们合并到 return 的字典中。
# @app.put("/items/{item_id}")
# async def create_item_with_put(item_id:int,item:Item,q:Optional[str]=None):
#     result = {"item_id":item_id,**item.dict()}
#     if q:
#         result.update({"q":q})
#     return result

# '''
# @app.get("/items")
# async def read_items(q:Optional[List[str]]=Query(["foo","bar"])):
#     print(f"DEBUG:Received q={q}")
#     results = {
#         "items":[{"item_id":"Foo"},{"item_id":"Bar"}]
#     }
#     if q:
#         results.update({"q":q})
#     return results
# '''

# @app.get("/items_validation/{item_id}")
# async def read_items_validation(
#     item_id:int = Path(..., title="The ID of the  item to get"),
#     q:Optional[str] = Query(None,alias='item-query')
#     ):
#     results = {"item_id":item_id}
#     if q:
#         results.update({"q":q})
#     return results


# '''
# Part 7 -> Body - Multiple Parameters
# '''
# from fastapi import FastAPI,Query,Path,Body
# from pydantic import BaseModel
# from typing import Optional,List

# app = FastAPI()

# class Item(BaseModel):
#     name:str
#     description:str | None = None
#     price:float
#     tax:float | None = None

# class User(BaseModel):
#     Full_name:str

# class importance(BaseModel):
#     importance:int



# @app.put("/items/{item_id}")
# async def update_item(
#     *,
#     item_id:int = Path(...,title = "The ID of the item to get",ge = 0,le = 100),
#     q:str | None = None,
#     item:Item = Body(...,embed = True),

# ):
#     results ={"item_id":item_id}
#     if q:
#         results.update({"q":q})
#     if item:
#         results.update({"item":item})
#     return results


## Part 11 - Extra Data Types
# @app.put("/items/{item_id}")
# async def read_items(
#     item_id:UUID,
#     start_date:datetime|None = Body(None),
#     end_date:datetime|None = Body(None),
#     repeat_at:time|None = Body(None),
#     process_after:timedelta|None = Body(None)
# ):
#     start_process = start_date + process_after
#     duration = end_date - start_process

#     return {
#         "item_id":item_id,
#         "start_date":start_date,
#         "end_date":end_date,
#         "repeat_at":repeat_at,
#         "process_after":process_after,
#         "start_process":start_process,
#         "duration":duration,
#         }

#  b1832d3c-f20c-4187-9c6e-13f35019059a


#Part12 Cookies and Headers
# @app.get("/items")
# async def read_itmes(
#     cookie_id:str | None = Cookie(None),
#     accept_encoding:str |None = Header(None),
#     sec_ch_us:str | None = Header(None),
#     user_agent:str | None =Header(None),
#     x_token:list[str] | None = Header(None),
#     ):
#     return {
#         "cookie_id":cookie_id,
#         "Accept_encoding":accept_encoding,
#         "Sec_ch_us":sec_ch_us,
#         "User_agent":user_agent,
#         "X_token":x_token
#     }

#Part 13 - Response Model

# class Item(BaseModel):
#     name:str
#     description:str | None = None
#     price :float
#     tax: float = 10.5
#     tags:list[str] = []

# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []}
# }

# @app.get("/items/{item_id}",response_model=Item,response_model_exclude_unset=True)
# async def read_item(item_id:Literal["foo","bar","baz"]):
#     return items[item_id]


# @app.post("/items")
# async def create_item(item:Item):
#     return item



# class UserBase(BaseModel):
#     username:str
#     full_name:str | None = None


# class UserIn(UserBase):
#     password:str

# class UserOut(UserBase):
#     pass

# @app.post("/user/",response_model = UserOut)
# async def create_user(user:UserIn):
#     return user


# @app.get(
#     "/items/{item_id}/name",
#     response_model=Item,
#     response_model_include={"name","description"},
# )
# async def read_item_name(item_id:Literal["foo","bar",'baz']):
#     return items[item_id]

# @app.get(
#         "/items/{item_id}/public",response_model=Item,response_model_exclude = {"tax"}
#         )
# async def read_items_public_date(item_id:Literal["foo","bar","baz"]):
#     return items[item_id]

# Part 14 Extar Models
# class UserIn(BaseModel):
#     username:str
#     password:str
#     email:str
#     full_name:str | None = None

# class UserOut(BaseModel):
#     username:str
#     email:str
#     full_name:str | None = None

# class UserInDB(BaseModel):
#     username:str
#     hashed_password:str
#     email:str
#     full_name:str | None = None

# def fake_password_hasher(raw_password:str):
#     return f"supersecret{raw_password}"

# def fake_save_user(user_in:UserIn):
#     hashed_password = fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.dict(),hashed_password=hashed_password)
#     print("userin.dict",user_in.dict())
#     print("User 'saved'.")
#     return user_in_db

# @app.post("/user/",response_model=UserOut)
# async def create_user(user_in:UserIn):
#     user_saved = fake_save_user(user_in)
#     return user_saved

#part 15- Response Status Codes
# @app.post("/items/",status_code=201)
# async def create_item(name:str):
#     return {"name":name}

# @app.delete("/item/{pk}",status_code=204)
# async def delete_item(pk:str):
#     print("pk",pk)
#     return pk


# Part 16-File

from fastapi import FastAPI, Form,File,UploadFile
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
app = FastAPI()

# @app.post("/login/")
# async def login(
#     username: str = Form(...),
#     password: str = Form(...)
# ):
#     print("Password:", password)
#     return {"username": username}

# # Pydantic 模型用于 JSON 请求
# class User(BaseModel):
#     username: str
#     password: str
# # 使用 JSON 处理数据
# @app.post("/login-json/")
# async def login_json(user: User):
#     return user


# part 17 Request Files
# @app.post("/files/")
# async def create_file(
#     files:list[bytes] = File(...,description="sssss")
#     ):
#     return{"file_size":[len(file) for file in files]}

# @app.post("/uploadfile")
# async def create_upload_file(
#     files:list[UploadFile] = File(...,description="sssss")
# ):
#     return {"filename":[file.filename for file in files]}

# @app.get("/")
# async def main():
#     content = """
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>File Upload</title>
# </head>
# <body>

#     <!-- 表单1: 上传单个或多个文件 -->
#     <form action="/files/" enctype="multipart/form-data" method="post">
#         <input name="files" type="file" multiple>
#         <input type="submit">
#     </form>

#     <!-- 表单2: 上传多个文件 -->
#     <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
#         <input name="files" type="file" multiple>
#         <input type="submit">
#     </form>

# </body>
# """
#     return HTMLResponse(content = content)


# part 18 -Request Forms and Files
