## NextJS

### Intercepting Routes

(.)是匹配同一层级的

(..)是匹配上一层级的

(..)(..)是匹配两个层级以上的

(...)是匹配app根目录下的

### Client-Side Rendering(客户端渲染)

指的是网页的内容主要由浏览器在用户端动态渲染，而不是服务器端直接返回完整的html页面。

依赖于JavaScript，主要适用于**单页面**应用。

优缺点：

优点：更好的用户体验，页面切换更流程，无需频繁的请求服务器。(适用于交互性强的应用，比如管理后台，在线编辑等)

缺点：搜索引擎优化不友好，搜索引擎可能无法正确解析JS动态生成的内容；

首次加载的速度慢，不适合低端设备。

### Server-Side Rendering

服务器在接受到用户的请求后，在服务端执行JavaScript并生成完整的html页面，然后返回给浏览器。

优缺点：
优点：SEO（搜索引擎优化）友好，首屏加载更快，适合动态内容。

缺点：服务器压力大，页面交互依赖额外的JavaScripts

### Suspense for SSR

Streaming Rendering(流式渲染)：服务器端可以先发送静态html，然后异步加载Suspense组件，等数据准备好后再渲染剩余部分。

部分Hydration(部分水合)：允许服务器先渲染一部分UI，等客户端JavaScript加载后，逐步让组件可交互。

### React Server Components(RSC)

它允许部分React组件在服务端执行，然后把结果发送到客户端进行渲染，减少JavaScript负担，提高页面性能。

在传统的React应用中，所有组件都会被打包到JavaScript文件并下载到客户端，然后浏览器执行他们。（这样会导致JS体积过大，加载慢，渲染性能下降），但在RSC中，组件可以在服务器端渲染，客户端只接受最终html和数据，不需要下载组件的JavaScript代码。

### Static Rendering(静态渲染)

它是Next.js提供的一种预渲染方式，他会在构建时生成html页面，并在请求时直接返回静态html，提高加载速度和SEO友好性。

### Dynamic Rendering(动态渲染)

它是在Next.js中指的是页面在请求时动态生成html，适用于需要个性化，实时更新或者数据库查询的页面。

两种方式：

Server-Side Rendering(SSR):每次请求生成新的html，适用于实时数据。

On-Demand ISR(增量静态再生) 静态页面按需更新，适用于部分动态数据。

### Streaming（流式渲染）

它是Next.js的核心功能，允许服务器逐步发送html到了客户端，而不是等所有数据准备好再一次性返回整个页面。这样可以大幅度提高首屏的加载速度，尤其实在需要慢速API请求，数据库查询的页面。

### Interleaving Server and Client Components(交错使用服务器和客户端组件)

Server Components里可以嵌套Client Components

Client Components里面也可以import其他的Client Compinents

但Client Components里面不能import Server Components

### Data Cache(数据缓存)

一般来说如果使用fetch从api获取数据，NextJs会缓存这个fetch请求（这样多个用户访问时就不会重复请求api）。但有一个问题---如果api数据更新了，页面不会自动刷新(除非你强制让他重新验证数据)

增量再生（ISR) :使用next:{revalidate:秒数}数据每个X秒更新一次

### Request Memoization(请求记忆化)

允许NextJs避免重复API请求或数据库查询，从而提高性能，减少服务器负担，确保数据只被请求一次。

简单来说就是：如果多个组件或请求使用相同的数据，Memorization让它们共用一个请求结果，而不是多次请求api。

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

//规定对应的路由
@app.get("/")
async def root():
    return {"message":"Hello wordl"}


@app.post("/")
async def post():
    return {"message":"Hello wordl"}

@app.put("/")
async def put():
    return .....

//带参数的router
@app.get("/users/{user_id}")
async def list_users(user_id:str):
    return {"user_id":user_id}


//带变量的
//在开头要使用from enum import Enum
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
//首先随便定义一个数据
fake_items_db = [{"item_name":"Foo"},{"item_name":"Bar"},{"item_name":"Baz"}]
//使用切片来循环输出这个数据
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

#也可以让q变为可选参数
@app.get("/items/")
async def read_items(q:str |None = Query(None,min_length=3,max_length=9)):
    return {"q":q}

#如果想要q必须符合某种模式（比如只能是fixedquery),可以使用regex
#在下面的情况中q必须等于"fixedquery"
@app.get("/items/")
async def read_items(q:str = Query(None,regex="^fixdedquery$")):
    return {"q":q}


#如果想要Query处理多个值（列表）
@app.get("/items/")
async def read_items(q:List[str] = Query([])):
    return {"q":q}
```

### 路径参数和数字化验证

可以使用Path参数来获取URL中的动态数据，并对其进行数值验证

```python
# 在路径（url）中定义变量，使用{}包裹
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):  # `item_id` 必须是 `int`
    return {"item_id": item_id}

# 使用Path进行数值验证，其中的Path(...）表示item_id是必须的，
# title = “item ID” 是用来给Swagger UI添加参数描述
# ge=1和le=1000表示item_id必须1<=id<=1000
@app.get("/items/{item_id}")
async def read_item(
    item_id:int =Path(..., title = "Item ID",ge=1,le=1000)
):
    return {"item_id":item_id}

#Path()结合str进行长度验证
@app.get("/users/{username}")
async def read_user(username:str = Path(...,min_length=3,max_length=10)):
    return {"username":username}

#Path()结合regex进行模式匹配
@app.get("/users/{username}")
async def read_user(username:str = Path(..., regex = "^[a-zA-Z0-9_-]+$")):
    return {"username":username}

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
from　fastapi import FastAPI, Body
app = FastAPI()
@app.post("/items/")
async def create_item(name:str=Body(...),price:float = Body(...)):
    return {"name":name,"price":price}
```
