# SQLAlchemy ORM

## 声明模型

在这里，我们定义模块级构造，这些构造形成我们从数据库中查询的结构。此结构成为声明性映射，他同时定义了Python对象模型以及描述特定数据库中存在或将存在的真实SQL表的数据库元数据:

```python
class Base(DeclarativeBase):
    pass
cl
```
