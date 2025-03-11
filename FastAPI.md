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
