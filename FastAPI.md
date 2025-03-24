## Fast Api

### 运行项目的步骤

```python
//首先进入虚拟环境
.\env\Scripts\activate
//运行整个程序
uvicorn main:app
```

### 引入Swagger应用来测试路由

Swagger是一个用于API设计，开发，测试和文档生成的开源框架，他帮助开发者规范化api的描述，并提供直观的ui界面。

### 基本的调用api的方法

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello wordl"}

@app.post("/")
async def post():
    return {"message":"Hello wordl"}

@app.put("/")
async def put():
    return .....
```

#### 带参数的Router

```python
@app.get("/users/{user_id}")
async def list_users(user_id:str):
    return {"user_id":user_id}
```

#### 带变量的Router

```python
from enum import Enum
class FoodEnum(str,Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"

@app.get("/foods/{food_name}")
async def get_food(food_name:FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name":food_name,
                "message":"you are healthy"}
    if food_name.value == "fruits":
        return{
            "food_name":food_name,
            "message":"you are still healthy,but like sweet things",   
        }
    return {"food_name":food_name,
            "message":"i like chocolate milk"}
```

### 查询参数

```python
# 首先随便定义一个数据
fake_items_db = [{"item_name":"Foo"},{"item_name":"Bar"},{"item_name":"Baz"}]
# 使用切片来循环输出这个数据
@app.get("/items")
async def list_items(skip:int=0,limit:int=10):
    return fake_items_db[skip:skip+limit]

@app.get("/items/{item_id}")
async def get_item(item_id:str,q:Optional[str]=None,short:bool=False):
    item ={"item_id":item_id}

    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {
                "description":"11111111"
            }
        )
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(item_id:str,user_id:str,q:Optional[str]=None,short:bool=False):
    item = {"item_id":item_id,"Owner_id":user_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {
                "description":"sssssssssssssss"
            }
        )
    return  item
```

这些参数中，如果有在路径中的参数那就是“必须填写的“数据，如果一些数据也没有默认值，则它也是属于”必须填写的“，其他的有默认值并且不在路径中体现出来的就属于”可选的“

### Request Body

```python
class Item(BaseModel):
    name:str
    description:Optional[str]=None
    price:float
    tax:Optional[float]=None


@app.post("/items")
async def create_item(item:Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax":price_with_tax})
    return item_dict  


# **item.dict() 解包了 item.dict() 的键值对，并把它们合并到 return 的字典中。
@app.put("/items/{item_id}")
async def create_item_with_put(item_id:int,item:Item,q:Optional[str]=None):
    result = {"item_id":item_id,**item.dict()}
    if q:
        result.update({"q":q})
    return result
```

Request Body 和Query Parameters的区别

| **特性**       | **Request Body (`POST` 方法，使用 Pydantic Model)** | **Query Parameters (`GET` 方法，直接作为函数参数)** |
| ------------ | ---------------------------------------------- | ---------------------------------------- |
| **数据来源**     | 来自 HTTP **请求体（Body）**                          | 来自 URL **查询参数（Query Params）**            |
| **HTTP 方法**  | 适用于 `POST`、`PUT`、`PATCH` 请求                    | 适用于 `GET` 请求                             |
| **传输方式**     | **JSON 格式**                                    | **URL 查询字符串**                            |
| **适用场景**     | 发送复杂数据，比如 JSON 对象                              | 发送简单的键值对数据                               |
| **是否可以嵌套数据** | ✅ **支持嵌套对象**                                   | ❌ 只支持简单的键值对                              |
| **数据大小**     | **可以传输较大数据**                                   | **通常传输少量数据**（受 URL 长度限制）                 |

两者各自的合适使用阶段

| **场景**          | **使用 `Request Body` (`POST`)** | **使用 `Query Parameters` (`GET`)** |
| --------------- | ------------------------------ | --------------------------------- |
| 传输大量数据          | ✅ **适合**                       | ❌ **不适合**                         |
| 传输结构化 JSON      | ✅ **适合**                       | ❌ **不适合**                         |
| 传输简单参数          | ❌ **不适合**                      | ✅ **适合**                          |
| 需要数据更新          | ✅ **适合 (`PUT`, `PATCH`)**      | ❌ **不适合**                         |
| 适用于 RESTful API | ✅ `POST /items`                | ✅ `GET /items?name=Laptop`        |

### Query parameters and String Validation

在FastApiz中 可以使用Query()来定义和验证查询参数：

- 最小/最大长度（min_length/max_length)

- 正则表达式

- 默认值

- 必须提供的参数等等

#### 使用Query来设置默认值和验证规则：

```python
from fastapi import FastAPI,Query

app = FastAPI()

@app.get("/items/")
async def read_items(q:str = Query("default_value",min_length=3,max_length=9)):
    return {"q":q}
```

#### 让q变为可选参数

```python
#也可以让q变为可选参数
@app.get("/items/")
async def read_items(q:str |None = Query(None,min_length=3,max_length=9)):
    return {"q":q}
```

#### Regex 规定输出的格式

```python
#如果想要q必须符合某种模式（比如只能是fixedquery),可以使用regex
#在下面的情况中q必须等于"fixedquery"
@app.get("/items/")
async def read_items(q:str = Query(None,regex="^fixdedquery$")):
    return {"q":q}
```

#### 使用Query处理多个值

```python
#如果想要Query处理多个值（列表）
@app.get("/items/")
async def read_items(q:List[str] = Query([])):
    return {"q":q}
```

### 路径参数和数字化验证

可以使用Path参数来获取URL中的动态数据，并对其进行数值验证，

在FastAPI中，Body(...)用于指定某个参数应当从请求体（Body）中解析，name:str = Body(...)表示name这个参数必须从Body中获取，为什么是等号：表示name的默认值是Body(...)，如果Body(...)省略了，FastAPI可能会误认为这是一个查询参数。

```python
# 在路径（url）中定义变量，使用{}包裹
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):  # `item_id` 必须是 `int`
    return {"item_id": item_id}
```

#### 使用Path进行数值验证

```python
# 其中的Path(...）表示item_id是必须的，
# title = “item ID” 是用来给Swagger UI添加参数描述
# ge=1和le=1000表示item_id必须1<=id<=1000
@app.get("/items/{item_id}")
async def read_item(
    item_id:int =Path(..., title = "Item ID",ge=1,le=1000)
):
    return {"item_id":item_id}
```

#### Path结合str进行长度验证

```python
#Path()结合str进行长度验证
@app.get("/users/{username}")
async def read_user(username:str = Path(...,min_length=3,max_length=10)):
    return {"username":username}
```

#### Path结合regex进行模式匹配

```python
#Path()结合regex进行模式匹配
@app.get("/users/{username}")
async def read_user(username:str = Path(..., regex = "^[a-zA-Z0-9_-]+$")):
    return {"username":username}
```

#### Path结合Query

```python
#Path()结合Query
@app.get("/items/{item_id}")
async def read_item(
    item_id:int = Path(...,ge=1,le=1000).
    q:str | None =Query(None,min_length=3,max_length=10)
):
    return {"item_id":item_id,"q":q}
```

### 处理多个Body参数

Body可以接受多个参数，并且可以于Path，Query结合使用。

```python
# 多个body参数（默认情况下，FastApi允许定义多个body参数，但必须使用Body(...)
# 否则FastAPI会把非Pydantic模型的参数当作查询参数
from　fastapi import FastAPI,Body
from pydantic import BaseModel

app = FastAPI()
@app.post("/items/")
async def create_item(name:str = Body(...),price:float = Body(...)):
    return {"name":name,"price":price}
```

#### Body和Pydantic相结合的模型

```python
class Item(BaseModel):
    name:str
    price:float
    description:str | None = None

@app.post("/items/")
async def create_item(item:Item):
    return item
```

#### Body+Path+Query

```python
#可以同时接受Path,Query和Body的数据
clas Item(BaseModel):
    name:str
    price:float


@app.post("/items/{item_id}")
async def create_item(
    item_id:int = Path(...,title="item ID",ge=1),
    q:str | None = Query(None,min_length =3,max_length = 10),
    item:Item = Body(...)
):
    return {"item_id":item_id,"q":q,"item":item}
```

#### Body处理多个Pydantic模型

```python
#可以在Body中处理多个Pydantic模型
class Item(BaseModel):
    name:str
    price:float

class User(BaseModel):
    username:str
    email:str

@app.post("/orders/")
async def create_order(
    item:item = Body(...),
    user:User = Body(...)
):
    return {"item":item,"User":user}
```

#### Body(...,embed=True)嵌套请求体

```python
# 默认情况下，FatsAPI不需要嵌套item字段，但你可以让item成为一个字段
@app.post("/items/")
async def create_item(item:Item = Body(...,embed=True)):
    return {"item":item}
```

如果python函数中有出现*,那么就表示在*出现之前的参数是可以位置传递，但*之后的参数就必须使用关键字传递。

关键字调用表示：必须要像这个样：

```python
def my_function(*, name: str, age: int):
    print(f"Name: {name}, Age: {age}")

# 正确调用（使用关键字参数）
my_function(name="Alice", age=25)

# ❌ 错误调用（位置参数）
my_function("Alice", 25)  # TypeError: my_function() takes 0 positional arguments but 2 were given
```

### Body+Field

在FastAPI中，我们可以使用Field()来为Pydantic模型中的字段添加额外的验证规则和元数据，类似月Query和Path处理查询参数和路径参数的方式。

Field()的作用：

- 设置默认值

- 添加最小/最大长度限制

- 设置数值范围

- 提供Swagger UI中的描述

- 定义正则表达式匹配

#### Field()的基本用法

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, title="Item Name", description="The name of the item")
    price: float = Field(..., gt=0, lt=10000, description="Price must be between 0 and 10,000")
    description: str | None = Field(None, title="Item Description", max_length=200)

@app.post("/items/")
async def create_item(item: Item):
    return item
```

#### 使用Field()限制字符串格式

```python
class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, regex="^[a-zA-Z0-9_-]+$")
    email: str = Field(..., regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
```

#### 指定默认值

```python
class Order(BaseModel):
    order_id: int = Field(1001, description="Default order ID")
    status: str = Field("pending", description="Order status")
```

#### Field()+Query()+Path()综合应用

```python
class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, title="Product Name")
    price: float = Field(..., gt=0, le=5000, description="Product price")
    stock: int = Field(..., ge=0, le=100, description="Available stock")

@app.post("/products/{product_id}")
async def create_product(
    product_id: int = Path(..., title="Product ID", ge=1),
    category: str = Query(..., min_length=3, max_length=20, alias="product-category"),
    product: Product = Body(...)
):
    return {"product_id": product_id, "category": category, "product": product}
```

### Nested Models(嵌套模型)

在FastAPI中，你可以在Body里嵌套多个Pydantic模型，这样可以让API结构更加清晰，并且自动进行数据验证。

#### 基本的Nested Model

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
app = FastAPI()
# 定义嵌套模型
class Item(BaseModel):
    name: str
    price: float
# 定义主模型，嵌套 Item
class Order(BaseModel):
    order_id: int
    items: List[Item]  # 这里 `items` 是 `Item` 模型的 **列表**
@app.post("/orders/")
async def create_order(order: Order):
    return order
```

#### 多层嵌套

```python
class Product(BaseModel):
    name: str
    price: float

class OrderDetail(BaseModel):
    quantity: int
    product: Product  # 这里 `product` 是 `Product` 对象，而不是列表

class Order(BaseModel):
    order_id: int
    details: List[OrderDetail]  # `details` 是 `OrderDetail` 的列表

@app.post("/orders/")
async def create_order(order: Order):
    return order
```

#### Field()限制嵌套字段

```python
class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    price: float = Field(..., gt=0)

class OrderDetail(BaseModel):
    quantity: int = Field(..., gt=0, le=100)

class Order(BaseModel):
    order_id: int
    details: List[OrderDetail]

@app.post("/orders/")
async def create_order(order: Order):
    return order
```

#### Optional 处理可选嵌套字段

```python
class User(BaseModel):
    username: str
    email: str
    address: Optional[str] = None  # `address` 是可选字段
```

### Extra Data Type

FastAPI

支持多种额外的数据类型，用于处理更复杂的请求数据，比如日期，UUID，Decimal等

| **数据类型**             | **Python 解释** | **示例**                                   |
| -------------------- | ------------- | ---------------------------------------- |
| `datetime.datetime`  | 日期时间          | `"2025-03-11T12:30:00"`                  |
| `datetime.date`      | 仅日期           | `"2025-03-11"`                           |
| `datetime.time`      | 仅时间           | `"12:30:00"`                             |
| `datetime.timedelta` | 时间间隔          | `600`（秒）                                 |
| `uuid.UUID`          | **唯一标识符**     | `"550e8400-e29b-41d4-a716-446655440000"` |
| `decimal.Decimal`    | 高精度浮点数        | `10.99`                                  |

#### 使用datetime处理时间

```python
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime,date

app = FastAPI()

class Event(BaseModel):
    event_name:str
    event_date:date #仅日期
    event_time:datetime #带时间

@app.post("/events/")
async def create_event(evevnt:Event):
    return:event
```

#### 使用UUID处理唯一标识

```python
from uuid import UUID
class User(BaseModel):
    user_id:UUID
    name:str
```

#### 使用Decimal处理高精度数值

```python
from decimal import Decimal

class Product(BaseModel):
    name:str
    price:Decimal #高精度货币值
```

#### 处理timedelta（时间间隔）

```python
from datetime import timedelta

class Subsription(BaseModel):
    user:str
    duration:timedelta
```

### Cookie和Header参数

在FastApi中，可以使用Cookie和Header来处理请求的Cookie和Http的头部

#### Cookie参数

```python
# FastAPI 允许使用Cookie()依赖项从请求大的Cookie中提取数据
from fastapi import FastAPI,Cookie

app = FastAPI()

@app.get("/read_cookie/")
async def read_cookie(session_id:str | None = Cookie(None)):
    return {"session_id":seesion_id}
```

#### Header参数

```python
from fastapi import FastAPI,Header
app = FastAPI()
@app.get("/read_header")
async def read_header(user_agent:str | None = Header(None)):
    return{"User_Agent":user_agent}
```

#### 处理大小写不敏感的Header

HTTP头部的**大小写不敏感**，但FastAPI默认大小写敏感的。

如果请求头使用了不同的大小写，可以设置convert_underscores=False

```python
@app.get("/read_header/")
async def read_header(user_agent:str | None = Header(None,converscores = False)):
    return {"User-Agent":user_agent}
```

#### 读取多个Headers

```python
@app.get("/read_headers")
async def read_headers(user_agent:str | None = Header(None),accept_encoding:str | None = Header(None)):
    return {"User-Agent":user_agent,"Accept-Encoding":accept_encoding}
```

#### 读取多个Cookie

```python
@app.get("/read_cookies")
async def read_cookies(session_id:str | None = Cookie(None),user_token:str | None = Cookie(None)):
    return {"session_id":session_id,"user_token":user_token}
```

### Response Model

Response Model 是用以定义API返回的数据结构，保证返回数据符合预期，同时也可以自动验证，过滤和转换。

#### 基本的用法

```python
from fastapi import FastAPI
from pydanic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name:str
    price:float
    description:str|None = None

@app.get("/items/{item_id}",response_model= Item)
async def get_item(item_id:int):
    return {"name":"Laptop","price":999.99,"description":"A high-end gaming laptop"}
```

#### Response_model自动过滤多余字段

```python
#他会自动过滤掉Item中没有的属性
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    return {"name": "Laptop", "price": 999.99, "description": "Gaming Laptop", "extra_field": "Not allowed"}
```

#### Response_model 和List相结合

```python
from typing import List

@app.get("/items/", response_model=List[Item])
async def get_items():
    return [
        {"name": "Laptop", "price": 999.99, "description": "Gaming Laptop"},
        {"name": "Mouse", "price": 25.99}
    ]
```

#### 过滤掉response_model的某些字段

```python
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def get_item(item_id: int):
    return {"name": "Laptop", "price": 999.99}
```

#### Response_model 和Field相结合（修改字段格式）

```python
from pydantic import Field
# 使用Field修改返回字段的别名
class Item(BaseModel):
    name: str = Field(..., alias="product_name")
    price: float

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    return {"product_name": "Laptop", "price": 999.99}
```

#### Response_model 和ORM Mode（数据库支持）

ORM(对象关系映射)，数据库通常使用ORM来操作数据，但ORM对象不能直接被FastApi返回，所以FastAPI需要自动转化ORM对象为Pydantic模型（JSON格式）

```python
class Item(BaseModel):
    name: str
    price: float

    class Config:
        orm_mode = True

@app.get("/items/{item_id}", response_model=Item)
#其中还可以使用response_model_include={"name"},...exclude{"name"}来表示包含或者不包含什么属性
async def get_item(item_id: int):
    return FakeORMObject(name="Laptop", price=999.99)  # FastAPI 自动转换 ORM 对象
```

#### Literal:

允许在函数参数或数据模型中限定变量的取值范围。

#### Response_model_exclude_unset=True:

用于排除没有被赋值的字段，只返回客户端提交的数据，未提交的字段不会出现在响应里。

#### Response_model_include：

用于只返回指定字段，过滤掉其他字段。

#### Response_model_exclude

用于返回所有字段，但排除指定字段。

### Extra Models

Extra Model指的是：

- 可以在一个Pydantic模型内嵌套另一个模型

- 可以使用多个Pydantic模型，让API结构更加清晰，便于复用数据结构

- 适用于复杂数据结构：一个order中包含多个items；User中包含Address

#### 嵌套Pydantic模型

电商App，订单包含多个商品

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 商品模型
class Item(BaseModel):
    name: str
    price: float
    quantity: int

# 订单模型（包含多个 Item）
class Order(BaseModel):
    order_id: str
    items: List[Item]
    total_price: float

@app.post("/create_order", response_model=Order)
async def create_order(order: Order):
    return order  # 直接返回订单信息
```

#### 使用response_model控制返回数据

```python
# 控制让Api不反悔price的数据
@app.get("/order/{order_id}", response_model=Order, response_model_exclude={"items__price"})
async def get_order(order_id: str):
    return {
        "order_id": order_id,
        "items": [
            {"name": "Laptop", "price": 1200.50, "quantity": 1},
            {"name": "Mouse", "price": 20.99, "quantity": 2}
        ],
        "total_price": 1242.48
    }
```

#### 不同的请求和相应模型

```python
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str  # 只有创建用户时才需要

class UserPublic(UserBase):
    id: int  # 返回时需要显示 ID，但请求时不需要

@app.post("/users/", response_model=UserPublic)
async def create_user(user: UserCreate):
    return {"id": 1, "username": user.username, "email": user.email}
```

#### 示例数据（在模型中添加额外的模式信息）

```python
# Union用于表示一个字段可以是多种类型中的任何一种
class Item(BaseModel):
    name: str = Field(..., example="Foo")
    description: Union[str, None] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Union[float, None] = Field(None, example=3.2)

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

### Response Status Codes

#### 默认的被自动分配的状态码

- GET请求：200OK

- POST请求：201Created

- PUT/DELETE请求：200OK

#### 自定义状态码

```python
# 可以使用status_code参数来自定义响应状态
from fastapi import FastAPI, status

app = FastAPI()
# 这样的话就会返回201created和对应的message信息
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user():
    return {"message": "User created successfully"}
```

#### 发送错误状态码

可以使用HTTPException来手动抛出错误

```python
from fastapi import FastAPI, HTTPException
app = FastAPI()
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "name": "Alice"}
```

#### 处理自定义的错误（带Headers）

```python
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code=404,
            detail="User not found",
            headers={"X-Error": "There goes my error"}
        )
    return {"user_id": user_id, "name": "Alice"}
```

#### 自定义响应状态码

```python
# 仅用于API文档描述 不会影响API的实际行为
@app.get(
    "/items/{item_id}",
    responses={
        200: {"description": "Item found"},
        404: {"description": "Item not found"},
    },
)
async def read_item(item_id: int):
    if item_id == 1:
        return {"item_id": item_id, "name": "Laptop"}
    raise HTTPException(status_code=404, detail="Item not found")
```

### From Fields

默认情况下，Post请求的数据是JSON格式，但有些情况下，客户端(如网页表单)会以application/x-www-form-urlencoded方式提交数据，这时候我们需要使用Form进行处理。

#### Form的基本用法

```python
# 使用Form让FastAPI解析表单提交的数据
# Form(...)表示这个字段是表单数据，其中(...)等同于required=True
from fastapi import FastAPI, Form
app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}
```

#### 发送表单请求

```python
# 当客户端以表单格式发送数据时：
POST /login/ HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=alice&password=secret
```

返回的结果是：

```python
{
    "username":"alice",
    "password":"secret"
}
```

#### 不能在同一个请求中使用Form和Body

```python
## 不可以这样使用，Body适用于application/json,Form适用于application/x-www-form-urlencoded
@app.post("/test/")
async def test(
    username: str = Form(...),
    password: str = Form(...),
    data: dict = Body(...)
):
    return {"username": username, "password": password, "data": data}
```

#### 处理可选的From字段

```python
@app.post("/register/")
async def register(
    username: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(None)  # 可选字段
):
    return {"username": username, "password": password, "full_name": full_name}
```

#### Pydantic遇到Form

```python
# pydantic的BaseModel只适用于Body（Json请求），不能用于Form
# 如果想要使用Pydantic必须手动定义Form字段
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}
```

#### 结合File上传文件

```python
# File经常和Form结合用于处理带有文件上传的表单
from fastapi import FastAPI, Form, File, UploadFile

app = FastAPI()

@app.post("/upload/")
async def upload_file(
    username: str = Form(...),
    password: str = Form(...),
    file: UploadFile = File(...)
):
    return {
        "username": username,
        "password": password,
        "filename": file.filename
    }
```

### Request Files

#### 处理文件上传

使用UploadFile和File来处理文件上传：(用于上传图片/视频/文档；处理多文件上传；控制文件大小)

```python
from fastapi import FastAPI, File, UploadFile
from typing import List

app = FastAPI()

# 单个文件上传
# UploadFile允许FastAPI处理上传文件，File(...）为让FastAPI识别为文件类型
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }

# 多文件上传
# List[UploadFile]允许同时上传多个文件
@app.post("/uploadfiles/")
async def upload_files(files: List[UploadFile] = File(...)):
    return [{"filename": file.filename, "content_type": file.content_type} for file in files]
```

#### 使用bytes来处理文件

相比于UploadFile，bytes更偏向于小文件的一次性读取。

```python
@app.post("/uploadbytes/")
async def upload_bytes(file: bytes = File(...)):
    return {"file_size": len(file)}
```

#### 读取文件内容

```python
@app.post("/readfile/")
async def read_file(file: UploadFile = File(...)):
    content = await file.read()  # 读取整个文件
    return {"content": content.decode("utf-8")}  # 假设是文本文件
```

#### 保存上传的文件

```python
# 确保upload/目录存在
# .write(await file.read())让文件保存在本地
@app.post("/savefile/")
async def save_file(file: UploadFile = File(...)):
    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(await file.read())
    return {"message": f"File {file.filename} saved successfully"}
```

#### 限制文件的大小

```python
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(..., max_size=10 * 1024 * 1024)):  # 10MB
    return {"filename": file.filename}
```

#### Request Form and Files

可以使用Form处理表单，使用File和UploadFile来处理文件上传，有时候也需要同时上传表单数据和文件，FastAPI允许你同时处理这两种数据格式。

对于FastAPI处理HTML响应，通常使用HTMLResponse来返回HTML页面。

```python
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/upload/")
async def upload_data(
    username: str = Form(...), 
    age: int = Form(...),
    profile_picture: UploadFile = File(...),
):
    return {
        "username": username,
        "age": age,
        "filename": profile_picture.filename,
        "content_type": profile_picture.content_type
    }

@app.get("/")
async def main():
    content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload Form</title>
    </head>
    <body>

        <h2>Upload Form with File</h2>
        <form action="/upload/" enctype="multipart/form-data" method="post">
            <label>Username:</label>
            <input type="text" name="username" required><br><br>

            <label>Age:</label>
            <input type="number" name="age" required><br><br>

            <label>Upload Profile Picture:</label>
            <input type="file" name="profile_picture" required><br><br>

            <input type="submit" value="Upload">
        </form>

    </body>
    </html>
    """
    return HTMLResponse(content=content)
```

### Handling Errors

#### 使用HTTPException处理自定义错误

使用HTTPException可以在API逻辑中手动抛出错误，并返回自定义的HTTP状态码和信息

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id < 0:
        raise HTTPException(
            status_code=400, 
            detail="Item ID must be a positive integer"
        )
    return {"item_id": item_id}
```

#### 处理请求验证错误（RequestValidationError）

当请求参数不符合FastAPI的**Query,Path或Body**验证规则时，会触发RequestValidationError

```python
from fastapi import FastAPI, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

# 处理 RequestValidationError
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request", "details": exc.errors()},
    )

@app.get("/items/")
async def read_items(q: str = Query(..., min_length=3, max_length=10)):
    return {"query": q}
```

#### 处理未捕获的全局异常

除了HTTPException和RequestValidationError，又是我们还需要处理所有未捕获的异常，比如数据库错误，运行错误等

```python
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

app = FastAPI()

# 处理所有未捕获的错误
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "error": str(exc)},
    )

@app.get("/cause-error")
async def cause_error():
    raise RuntimeError("Something went wrong!")
```

#### 自定义异常类(处理业务逻辑中特定的错误)

```python
class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,  # HTTP 418 I'm a teapot (示例状态码)
        content={"error": f"Custom Exception: {exc.name}"}
    )

@app.get("/custom-error/{name}")
async def trigger_custom_error(name: str):
    if name == "error":
        raise CustomException(name)
    return {"message": "No error"}
```

### Path Operation Configuration(路径操作配置)

在FastApi中可以对于路径操作进行配置，这些配置可以通过@app.get(),@app.post(),@app.put()等装饰器的额外参数来实现。

#### 使用Summary 和 Descrption

```python
from fastapi import FastAPI

app = FastAPI()

@app.get(
    "/items/",
# 在API文档里显示出详细的信息
    summary="获取所有物品",
    description="此 API 端点用于获取所有的物品。你可以使用 `limit` 参数来控制返回的数量。"
)
async def read_items(limit: int = 10):
    return {"message": f"Returning {limit} items"}
```

#### Response_description配置响应信息

```python
@app.get(
    "/users/",
    response_description="返回所有用户信息"
)
async def get_users():
    return [{"name": "Alice"}, {"name": "Bob"}]
```

#### Tag来配置API分类

在Swagger UI文档中API就会按照分类来显示 方便查找

```python
@app.get("/users/", tags=["Users"])
async def get_users():
    return [{"name": "Alice"}, {"name": "Bob"}]

@app.get("/items/", tags=["Items"])
async def get_items():
    return [{"item": "Book"}, {"item": "Laptop"}]
```

#### 标记API过时

```python
# 如果某个API不再推荐使用 可以用Deprecated = True进行标记
@app.get("/old-endpoint/", deprecated=True)
async def old_api():
    return {"message": "This API is deprecated"}
```

#### 自定义API的ID

默认情况下，FastAPI会自动生成API操作ID，但我们也可以指定

```python
@app.get("/users/", operation_id="fetch_all_users")
async def get_users():
    return [{"name": "Alice"}, {"name": "Bob"}]
```

#### 配置Response_model

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

@app.get("/user/", response_model=User)
async def get_user():
    return {"name": "Alice", "age": 25}
```

### JSON Compatible Encoder and Body Updates(JSON兼容编码器和身体更新)

#### JSON 兼容编码器

```python
from datetime import datetime
from fastapi.encoders import jsonable_encoder

data = {
    "name": "Alice",
    "created_at": datetime.utcnow()
}

json_data = jsonable_encoder(data)
print(json_data)  # {"name": "Alice", "created_at": "2025-03-12T12:00:00"}
```

#### JSON 兼容编码器在FastAPI路由中

```python
# 当返回数据时，如果数据包含Datatime，UUID，可以用jsonable_encoder进行转换
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    created_at: datetime

@app.post("/users/")
async def create_user(user: User):
    user_data = jsonable_encoder(user)
    return {"user_data": user_data}
```

#### Body Updates(更新数据)

在实际应用中，我们通常需要更新数据库中的某个字段，而不是重写整个对象，FastAPI提供了一种增量更新（PATCH请求）的方法

```python
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# 模拟数据库
fake_db = {
    "user1": {"name": "Alice", "age": 25},
    "user2": {"name": "Bob", "age": 30}
}

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

@app.patch("/users/{user_id}")
async def update_user(user_id: str, user_update: UserUpdate):
    if user_id not in fake_db:
        return {"error": "User not found"}

    stored_data = fake_db[user_id]#提取出对应的原始数据
    update_data = user_update.dict(exclude_unset=True)  #提供需要更新的字段
    stored_data.update(update_data)#进行数据的更新

    return {"user_id": user_id, "updated_data": stored_data}
```

#### JSON 兼容编码和更新数据相结合

```python
from fastapi.encoders import jsonable_encoder

@app.patch("/users/{user_id}")
async def update_user(user_id: str, user_update: UserUpdate):
    if user_id not in fake_db:
        return {"error": "User not found"}

    stored_data = fake_db[user_id]
    stored_data = jsonable_encoder(stored_data)  # 确保数据兼容 JSON

    update_data = user_update.dict(exclude_unset=True)
    stored_data.update(update_data)  # 只更新提供的字段

    return {"user_id": user_id, "updated_data": stored_data}
```

#### Put和PATCH更新数据的对比

| 方法      | 用途           | 示例                                                  |
| ------- | ------------ | --------------------------------------------------- |
| `PUT`   | **完整替换整个对象** | `PUT /users/user1` `{ "name": "Alice", "age": 28 }` |
| `PATCH` | **部分更新某些字段** | `PATCH /users/user1` `{ "age": 28 }`                |

### Dependencies(依赖注入)

依赖注入-强大的特性，可以让你在多个路径操作路由中复用代码(比如：数据库链接；权限管理；日志记录；通用参数；数据预处理等)

#### 依赖注入的基本使用

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# 依赖函数
def common_dependency():
    return {"message": "这是一个依赖函数"}

# 使用依赖
@app.get("/items/")
async def read_items(dep: dict = Depends(common_dependency)):
    return {"data": dep}
```

common_denpendency是一个普通的函数，Depends(common_dependency告诉FastAPI这个路由以来common_dependency)

#### 依赖注入的参数传递

可以让以来函数接受参数，并在不同的请求中复用

```python
def dependency_with_params(q: str | None = None):
    return {"query": q}

@app.get("/search/")
async def search_items(dep: dict = Depends(dependency_with_params)):
    return {"data": dep}
```

#### 依赖注入的实际应用

依赖数据库链接

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# 模拟数据库连接
def get_db():
    db = {"connection": "Database Connected"}
    try:
        yield db  # 使用 yield 让 FastAPI 处理生命周期
    finally:
        print("关闭数据库连接")  # 这里可以添加关闭数据库的代码

@app.get("/users/")
async def get_users(db: dict = Depends(get_db)):
    return db
```

依赖权限认证(可以在多个路由中使用相同的权限验证逻辑)

```python
# 相当于是这个路由的全局依赖，会在执行对应路由的函数read_items()前执行
# 不需要传递返回值给read_items
# 只适用于简单检查，API Key认证等情况
async def verify_token(x_token:str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code = 400,detail = "X-Token header invalid")


async def verify_key(x_key:str = Header(...)):
    if x_key !="fake-super-secret-key":
        raise HTTPException(status_code = 400,detail = "X-Key header invalid")
    return x_key

@app.get("/items",dependencies=[Depends(verify_key),Depends(verify_token)])
async def read_items():
    return [{"item":"FOO"},{"item":"Bar"}]
    # 在函数内容不使用依赖返回数据
# 适用于身份验证后要获取用户对象，权限级别等情况
from fastapi import HTTPException, Security, Depends

def check_token(token: str = Security(...)):
    if token != "secret-token":
        raise HTTPException(status_code=403, detail="无效 Token")
    return {"message": "Token 验证通过"}

@app.get("/protected/")
async def protected_route(auth: dict = Depends(check_token)):
    return {"data": auth}
```

#### 全局依赖

设置整个应用级别的全局依赖，让所有路由都必须经过这个逻辑

```python
# 上面的所有的请求都会先验证check_token()
app = FastAPI(dependencies=[Depends(check_token)])

@app.get("/public/")
async def public_data():
    return {"message": "所有人都能访问"}

@app.get("/private/")
async def private_data():
    return {"message": "必须有 Token"}
```

#### 依赖类

如果你有多个相关的以来函数，可以使用类来进行管理

使用Auth统一管理Token验证，Depends(Auth().verify_token让所有路由都可使用)

```python
class Auth:
    def __init__(self, token: str):
        self.token = token

    def verify_token(self):
        if self.token != "secret-token":
            raise HTTPException(status_code=403, detail="无效 Token")
        return {"message": "Token 验证通过"}

@app.get("/secure/", dependencies=[Depends(Auth("secret-token").verify_token)])
async def secure_data():
    return {"message": "安全数据"}
```

### Security

Security主要是用于身份认证（Authentication），它和Depends类似，但主要用于处理安全相关的请求头，比如API Token，OAuth2,JWT等

#### Security() 和 Depends()的区别

|          | **`Depends()`**        | **`Security()`**               |
| -------- | ---------------------- | ------------------------------ |
| **主要用途** | **通用依赖注入**（数据库、日志、权限等） | **专门用于身份认证**（API Token、OAuth2） |
| **适用范围** | **任何依赖项**（不仅限于安全验证）    | **通常用于认证、安全相关的请求**             |
| **特点**   | **所有请求都适用**            | **通常只适用于需要身份验证的请求**            |
| **优先级**  | **普通优先级**              | **更适用于安全相关逻辑**                 |
| **示例**   | `Depends(get_db)`      | `Security(get_current_user)`   |

#### 适用Security()进行API Token认证

```python
# 定义 Token 认证
# Security(get_api_key)只用于身份认证，并返回认证状态
api_key_header = APIKeyHeader(name="X-API-KEY")

# 认证函数
# 在这里Security的作用是告诉FastAPI需要从HTTP头部X-API-KEY读取APIkey
# 然后自动解析HTTP头部数据 并传递给get_api_key函数
def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != "my-secret-token":
        raise HTTPException(status_code=403, detail="无效的 API Key")
    return {"message": "认证成功"}

# 受保护的 API 端点
@app.get("/protected/")
async def protected_route(auth: dict = Security(get_api_key)):
    return {"data": auth}
```

#### 适用Security()进行OAuth2认证

OAuth2是常见的身份认证方式，Security()可以用于OAuth2的Bearer Token认证

```python
# OAuth2 Bearer Token 认证
# 这个函数告诉FastApi这个api端点OAuth2认证（定义OAuth2认证方式）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 认证函数
# Security让FastAPI自动提取Bearer Token,然后进行校验
def get_current_user(token: str = Security(oauth2_scheme)):
    if token != "super-secret-token":
        raise HTTPException(status_code=403, detail="无效的 Token")
    return {"user": "admin"}

# 受保护的 API
@app.get("/user/")
async def read_user(user: dict = Security(get_current_user)):
    return {"user_info": user}
```

#### Security和Depends的使用时间

Security()适用于身份认证：

- **API Token（X-API-KEY）**

- **OAuth2 认证（JWT / Bearer Token）**

- **用户权限验证**

Depends()适用于一般依赖：

- **数据库连接**

- **日志管理**

- **请求参数解析**

### 简单的OAuth2认证

```python
# 模拟用户数据库
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()
# 假处理密码
def fake_hash_password(password: str):
    return "fakehashed" + password
#配置OAuth2认证，设定OAuth2的认证方式（使用Baerer Token）
#tokenUrl指定Token生成的Api端点
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

# 继承User的类 并添加一个属性hashed_password
class UserInDB(User):
    hashed_password: str

# 用户查找函数
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Annotated[]用于依赖注入和类型注解
#FastAPI使用OAuth2PasswordRequestForm解析表单数据
# Depends()自动注入OAuth2PasswordRequestForm
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
```

### Security with JWT

JWT是一种安全的Token，用于在客户端和服务器之间安全的传输身份信息，由三部分组成（Header,Payload,Signature)

```python
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# 初始化 FastAPI
app = FastAPI()

# 🔐 JWT 配置
SECRET_KEY = "your_secret_key"  # ⚠️ 应该存储在环境变量中
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 🔑 处理密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 📌 OAuth2 认证方式（用于解析 `Authorization: Bearer <token>`）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 🔹 模拟数据库
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False,
    }
}

# 📌 用户模型
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# 🔹 生成 JWT Token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔍 解析 Token 并验证
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    user_dict = db.get(username)
    return UserInDB(**user_dict) if user_dict else None

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return get_user(fake_users_db, username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# 📌 登录 API，返回 JWT Token
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# 📌 获取当前用户信息（需要 `Authorization: Bearer <token>`）
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

### Middleware and CORS

Middleware(中间件)允许在每个请求和相应之间执行一些操作，例如日志记录，CORS处理，身份验证，请求修改等

CORS(跨域资源共享)允许不同域的前端(如React,Vue)访问后端API.(比如前端运行在localhost：8000 而后端运行在localhost：3000，如果不允许CORS，前端请求会被拦截)

#### Middleware的使用

```python
# 方法一：使用@app.middleware("http")
# 拦截HTTP请求；记录请求时间；调用继续执行请求；计算并输出请求处理时间
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)  # 继续执行请求
    process_time = time.time() - start_time
    print(f"请求: {request.method} {request.url.path} 处理时间: {process_time:.4f} 秒")
    return response

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI"}

# 方法二：add_middleware()
class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        print(f"请求: {request.method} {request.url.path} 处理时间: {process_time:.4f} 秒")
        return response

app.add_middleware(TimerMiddleware)

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI"}
```

#### FastAPI启用CORS

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允许的域名
origins = [
    "http://localhost:3000",  # 允许本地前端
    "http://example.com",  # 允许指定域名
    "*",  # 允许所有域名（不推荐）
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的源
    allow_credentials=True,  # 允许携带 Cookie
    allow_methods=["*"],  # 允许所有请求方法（GET, POST, PUT, DELETE）
    allow_headers=["*"],  # 允许所有请求头
)

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI"}
```

#### 验证CORS

```python
fetch("http://localhost:8000/", {
  method: "GET",
  headers: { "Content-Type": "application/json" }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error("Error:", error));
```

### SQL Relational Database

FastAPI可以与SQL关系型数据库（如PostgreSQL,MySQL,SQLite）集成，并使用SQLAlchemy ORM进行数据库操作。

### FastAPI + SQLAlchemy配置

#### 配置数据库连接

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 连接 PostgreSQL 数据库
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 创建 Session（用于数据库操作）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()
```

#### 创建数据库模型

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

# 用户表
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
```

#### 创建数据库表

```python
# 使用alembic进行数据库迁移
alembic init alembic #初始化Alembic
# 修改alembic/env.py
from database import Base,engine
target_metadata = Base.metadata
# 创建迁移文件
alembic revision --autogenerate -m "create users table"
# 应用迁移
akembic upgrade head
```

#### 创建FastAPI CRUD（增删改查）

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User

app = FastAPI()

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📌 创建用户
@app.post("/users/")
async def create_user(name: str, email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = password + "_hashed"  # 简单模拟哈希（实际需使用 bcrypt）
    new_user = User(name=name, email=email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 📌 获取所有用户
@app.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# 📌 获取单个用户
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()

# 📌 删除用户
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted"}
    return {"error": "User not found"}
```

### FastAPI + SQLModel + SQLite解析

```python
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

# 定义数据库模型
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

# 链接SQLite数据库
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# 创建数据库表（如果数据库中没有表，就创建表）
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 数据库会话（使用yield让FastAPI自动管理Session）
def get_session():
    with Session(engine) as session:
        yield session

## SessionDep让数据库Session变为依赖项
SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# 启动FastAPI
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# CRUD
@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
```

### 一套标准化DTO结构：

#### 什么是DTO(fastApi中)：

DTO是数据传输对象，用于：

- 接受前端传来的请求数据

- 返回给前端的响应数据

- 和数据库模型(Model)隔离，避免暴露内部结构

#### FastAPI中的DTO是用Pydantic模型实现的

```yaml
     前端请求
        |
        v
  ┌────────────┐
  │  Pydantic  │  ← DTO：用于接收请求和返回响应
  └────────────┘
        |
        v
  ┌──────────────┐
  │ SQLAlchemy   │  ← Model：连接数据库的真实模型
  └──────────────┘
```

SQLAlchemy模型+DTO(Pydantic)+路由整合的FastAPI项目结构代码

#### 目录结构建议(按模块拆分)

```yaml
your_project/
├── main.py
├── database/
│   ├── config.py           # 数据库连接字符串配置
│   ├── session.py          # 创建 SQLAlchemy engine 和 SessionLocal
│   └── base.py             # 声明 Base（可选）
├── models/
│   └── user.py             # SQLAlchemy ORM 模型
├── dto/
│   └── user_dto.py         # Pydantic DTO 输入输出模型
├── crud/
│   └── user_crud.py        # 数据访问逻辑（相当于 DAO）
├── routes/
│   └── user.py             # 路由：绑定接口和业务逻辑
```

#### database/config.py

```python
DATABASE_URL = "sqlite:///./test.db"  # 可换成你的 PostgreSQL 等
```

#### database/session.py

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # SQLite 专用
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

#### models/user.py

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
```

#### dto/user_dto.py

```python
from pydantic import BaseModel

class UserCreateDTO(BaseModel):
    username: str
    email: str

class UserResponseDTO(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True  # 允许从 ORM model 转换
```

#### crud/user_crud.py

```python
from sqlalchemy.orm import Session
from models.user import User
from dto.user_dto import UserCreateDTO

def create_user(db: Session, user_dto: UserCreateDTO) -> User:
    user = User(username=user_dto.username, email=user_dto.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()
```

#### routes/user.py

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import SessionLocal
from dto.user_dto import UserCreateDTO, UserResponseDTO
from crud.user_crud import create_user, get_user_by_id

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users", response_model=UserResponseDTO)
def create_user_endpoint(user: UserCreateDTO, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/users/{user_id}", response_model=UserResponseDTO)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

#### main.py

```python
from fastapi import FastAPI
from models.user import Base
from database.session import engine
from routes.user import router as user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)  # 自动建表（开发阶段）
app.include_router(user_router)
```

#### 为什么DTO可以做到“避免暴露数据库结构，可控制字段的”呢？

因为DTO定义了哪些字段，就会显示哪些字段，并不是数据库表的全部字段。

### Bigger Applications - Multiple Files(多文件结构)

当FastAPI项目变复杂时，单个的main.py文件会变得难以管理，所以就需要拆分代码到多个文件中，保持清晰的项目结构。

推荐的目录结构如下：

```python
my_project/
│── app/
│   ├── main.py        # 入口文件（启动应用）
│   ├── database.py    # 数据库连接
│   ├── models.py      # 数据库模型
│   ├── schemas.py     # Pydantic 数据验证
│   ├── crud.py        # CRUD 操作封装
│   ├── routes/        # API 路由模块
│   │   ├── users.py   # 用户相关 API
│   │   ├── items.py   # 物品相关 API
│   ├── dependencies.py # 依赖项
│   ├── config.py      # 配置文件
│── alembic/           # 数据库迁移（Alembic）
│── .env               # 环境变量（数据库 URL）
│── requirements.txt   # 依赖包
│── README.md          # 项目说明
```

#### Main.py(FastAPI入口)

通过include_router()引入多个API模块

```python
from fastapi import FastAPI
from app.routes import users, items  # 导入路由

app = FastAPI()

# 注册 API 路由
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI"}
```

#### Database.py 数据库连接

```python
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
```

#### Models.py 数据库模型

```python
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
```

#### Schemas.py Pydantic 数据模型

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str
```

#### Crud.py 封装CRUD逻辑

```python
from sqlmodel import Session, select
from app.models import User

def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_users(session: Session):
    return session.exec(select(User)).all()
```

#### Routes/Users.py 用户API

```python
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.models import User
from app.schemas import UserCreate, UserRead
from app.crud import create_user, get_users

router = APIRouter()

@router.post("/", response_model=UserRead)
def create_new_user(user: UserCreate, session: Session = Depends(get_session)):
    new_user = User(name=user.name, email=user.email)
    return create_user(session, new_user)

@router.get("/", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session)):
    return get_users(session)
```

#### routes/items.py 物品API

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_items():
    return [{"item": "Apple"}, {"item": "Banana"}]
```

### Backgroud Tasks(背景任务)

FastApi 支持后台任务，可以在不影响API响应的情况下异步执行耗时操作。

#### 基本用法

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_log(message: str):
    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")

@app.post("/log/")
async def create_log(background_tasks: BackgroundTasks, message: str):
    background_tasks.add_task(write_log, message)
    return {"message": "Log task added"}
```

#### 处理异步任务

```python
import asyncio

async def async_task(message: str):
    await asyncio.sleep(5)  # 模拟耗时任务
    print(f"后台任务完成: {message}")

@app.post("/async-task/")
async def run_task(background_tasks: BackgroundTasks, message: str):
    background_tasks.add_task(async_task, message)
    return {"message": "Async task started"}
```

#### 结合数据库

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_session
from app.models import User
from app.schemas import UserCreate

async def send_email(email: str):
    await asyncio.sleep(3)  # 模拟邮件发送
    print(f"📧 发送邮件至 {email}")

@app.post("/register/")
async def register_user(
    user: UserCreate, 
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    new_user = User(name=user.name, email=user.email)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # 添加后台任务（发送邮件）
    background_tasks.add_task(send_email, user.email)

    return {"message": "User registered, email will be sent!"}
```

#### 任务队列（更高级的后台任务）

如果任务太多，可以用Celery进行任务队列管理

```python
from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost:6379")

@celery_app.task
def send_email_task(email: str):
    print(f"📧 发送邮件至 {email}")
```

### Metadata and Docs URLs(元数据和文档)

FastAPI提供了自动生成的API文档，并允许自定义API元数据（Meyadata)以及文档访问URL，

Metadata时API的元信息，它包括：

- 标题（title）Api的名字

- 描述（description）API的详细介绍

- 版本号（version) APi版本

- 文档网址（docs_url,redoc_url)Swagger UI访问地址

#### 自定义API Metadata

```python
from fastapi import FastAPI

app = FastAPI(
    title="My Awesome API",
    description="🚀 这是一个 FastAPI 示例应用，展示如何使用 API 文档。",
    version="1.0.0",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "https://example.com/contact/",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}
```

### 静态文件

在Web开发中，静态文件通常包括：

- HTML用于页面展示

- CSS用于样式

- JavaScript用于前端交互

- 图片

#### 提供静态文件

FastAPI允许通过StaticFiles处理静态文件

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 绑定静态文件目录，访问路径为 /static
# 这样的话/static/目录下的文件可以直接访问
app.mount("/static", StaticFiles(directory="static"), name="static")
```

访问HTML文件

```python
from fastapi.responses import FileResponse

@app.get("/")
async def home():
    return FileResponse("static/index.html")
```

### Testing单元测试

FastApi推荐使用pytest进行单元测试，并提供TestClient来模拟API请求

#### 简单的FastAPI测试

```python
from fastapi.testclient import TestClient
from main import app
#TestClient(app)模拟API请求
client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI!"}
```

### Debugging(调试FastAPI应用 )

```python
uvicron main:app --reload
##print()进行调试
print("调试信息：代码运行成功")
# 使用logging，相比于print（）日志更强大

import logging
logging.basicConfig(Level = logging.INFO)
logger = logging.getLogger(_name_)

@app.get("/debug")
async def debug_example():
    logger.info("运行成功")
    return {"message":"Debugging"}
```
