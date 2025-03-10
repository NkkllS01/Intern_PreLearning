# from enum import Enum
# from typing import Optional,List
# from fastapi import FastAPI,Query,Path
# from pydantic import BaseModel

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

