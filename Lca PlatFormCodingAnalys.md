# Lca PlatForm前端

## Home Folder

Home页面根据view值的不同返回到两个不同的组件当中：

- DataSource

- DataPoints

### Header Folder

设定了Home页面的对应的Header和其对应的css文件。

### DataPoints

以列表的形式展示相关的数据

#### Collapsoble

是一个可折叠的筛选面板组件，用于LCA平台或数据筛选界面中展开分类标签，并且允许用户选择，收缩标签来过滤数据。

#### DatapointsPageTitle

这个是搜索功能的标题组件，用于展示Datapoints的页面标题，同时允许用户输入关键词进行搜索，搜索后会更新URL参数并刷新页面内容。

#### Filters

这个文件用于Datapoints页面中展示筛选器面板，结合collapsoble下拉模块与URL查询参数同步，实现"多标签过滤"的功能。

- 根据选择的标签更新URL参数

- 定义了每一类标签的标题，数据来源和filter类型

### DataSource

多个小格子对应展示相关的数据

#### DataSource-Reusable-Card

里面所有的组件都是为了组成这个小的卡片。

##### Access

主要用于前端UI中显示访问权限的标签。

- View Only

- Copyable

- Locked

- Full Access

##### CompanyFullName

卡片上的公司名字

##### SingleCard

规定整个卡片的布局。

并提供了用户的交互功能：

- Explore按钮：点击后跳转到/home/${item.id}页面，查看数据源的详细信息

- LockIcon：显示/切换数据源是否被锁定。

- BookIcon：显示/切换数据源是否被收藏

- DropdownMenu：用于操作数据源的更多选项

#### DataSource-Reusable-Modal

##### DropdownMenu

设置了home页面header栏上的设置按钮的点击下拉选项

##### NewDataSourcePanel

在home页面点击创建新的DataSource的时候，出现的填写的新的DataSource的栏

##### NewFilterPanel

实在数据源页面中提供筛选功能，利用表单form，URL参数(searchParams),结合状态管理（useHomeContext)来实现筛选。

### Reusable

多个重用的部分放在这里

#### Columns

定义了两个按钮组件（ButtonCell和ExploreButton），分别执行不同的操作：

ButtonCell:点击后会获取LCIA详细信息 并存入Context State

ExploreButton:点击后，会获取LCIA ID并跳转到/home/...路由

#### Data-Table

定义了一个DataTable组件，它用于显示LCIA数据表，其中:

- 数据来自于state.data(全局状态)

- 使用@tanstack/react-table创建表格，并渲染Tabel

### Type

这个文件的主要作用是规定API返回数据的格式，确保数据在TypeScripts代码里符合预取的结构。

- 使用TypeScript进行静态类型检查。

- 在API，React组件，全局状态里复用数据结构

- 帮助开发时的TypeScript自动补全(减少拼写错误)

## Serivice Folder

### Ghg-apis-services

这个文件是Next.js服务器端API请求封装模块，它提供了一系列用于与GHG（温室气体相关API）进行交互的函数。

主要作用是从后端获取数据，并在Next.js服务器端使用fetch进行API请求管理。

### web-call-services

这个文件是一个用于Next.js和LCA平台的后端API封装模块：

专门负责：

- 集中管理对后端API的请求逻辑

- 基于Next.js的服务端特性优化数据缓存

## utils Folder

### lca-utils

是一个使用工具函数的集合，包含在多个地方都能用到的小工具。

- debounce防抖处理(长用于输入框搜索等连续触发事件的优化，防止函数被频繁调用)

- deepEqual(obj1,obj2)进行深度比较两个对象是否"结构上一样"

# Lca PlatForm后端

## FasrAPi获取数据

| 角色    | FastAPI 中的做法                     | 类比于 .NET MVC    |
| ----- | -------------------------------- | --------------- |
| 连接数据库 | `create_engine()` + Session      | `DbContext`     |
| 定义数据表 | SQLAlchemy `Base + Column`       | Model 类         |
| 执行查询  | `session.query(...).filter(...)` | DAO 或 LINQ      |
| 控制访问  | 路由中使用 CRUD + Depends 注入          | Controller 里的调用 |

## 为什么在已有的api目录的基础上还需要一个api_external？

Api是用于这个的主后端项目，用于：

- 用户请求处理（用于LCA平台的主数据服务）

- 链接数据库，返回JSON，分页，过滤等功能

- 正式部署到平台或生产使用的API

Api_external的作用可能是：

- 封装调用外部API的逻辑（第三方数据源）

- 数据预处理或同步服务

- 代码生成和自动化相关

对于Api_external来说，**他不是一个需要长期运行在服务器上，持续响应请求的服务**，而更像是一个**工具型模块**，用于开发或初始化时运行。

比如项目中的api_external是用来：

- 从某个第三方LCA平台拉去最新的数据库结构（比如JSON schema）

- 把他转化成项目内容用的模型结构

- 存成schema.json,Informative_schema.json等

这些操作大多数属于一次性操作/定期同步/开发阶段自动生成的

所以如果不部署的情况下，别人想要使用它，最常用的做法是：

- 提供README.md指引

## JSON快速生成类z

自动把JSON数据结构转化成Python类（Pydantic模型）

比如一个外部的api返回了json数据，然后我们使用quicktype.io来进行对应的python类的生成，这样的话就可以在FastAPI中：

- 使用这个模型来解析请求（request.body)

- 响应前端数据（return LciaIndicator(...))

## Api_external/factory.py

作用：

- 用面对对象的方式，为不同环境动态构建FastAPI实例

- 就解决本地和生产配置的不同

- 项目启动方式统一

- 单元测试来用于控制app

- 支持多个环境

## api/app/services

这一部分主要是和数据库的操作相关

### api/app/services/bulk_insert_srevice

这个service文件用于批量插入LCIA数据库结构和数据，包括LCIA数据库，影响因子数据，过程数据(Upr)，交换流(Exchange)等多个表之间的复杂关联逻辑。

**这个是数据库模型的核心插入逻辑**

总结是：

这是一个为LCIA数据库导入场景量身定制的service层模块，封装了从元数据注册-->数据建模-->多表插入-->事务提交的完整流程，供上层api路由模板调用使用。

#### api/app/services/characterization_factor

他的核心作用是：处理特征化因子(Characterization Factors)，相关的数据库查询逻辑。

他是LCIA系统中专门用来提供”因子查询，因子数据匹配，模糊搜索，分页“等功能的模块，供API层的调用，用于前端展示或其他后端逻辑使用。

## Api/app/database

### Session.py

他是FastAPI项目中用于统一管理异步数据库链接和会话(Session)生命周期的模块。

封装数据库引擎初始化，链接管理，异步会话创建和关闭，创建表/删除表操作，依赖注入支持的逻辑，是整个项目与数据库通信的基础设施。



## Api/app/routers

### bulk_insert:

接受一个包含LCIA数据来源，数据库，数据点的请求对象，把这些数据打包好后传给service层同一插入数据库。

```yaml
客户端请求 JSON
     ↓
BulkInsertModel（Pydantic DTO）
     ↓
model_dump ➜ 拆分出 3 类 dict 数据：
  - 数据来源
  - 数据库列表
  - 数据点列表
     ↓
调用 Service 层统一处理写入数据库
```

### characterization_factor

函数"/cfs/cf_data"的运行逻辑

```yaml
[请求参数 cf_id, 筛选条件, 分页]
        ↓
FastAPI 路由函数接收
        ↓
调用服务层 fetch_cf_data() 查询数据库
        ↓
返回 list[Row] 原始数据
        ↓
手动转换为 CfDataDetail DTO
        ↓
返回 list[dtos.CfDataDetail] 给前端
```

| 情况                                  | 是否需要手动转换？ | 原因                                 |
| ----------------------------------- | --------- | ---------------------------------- |
| ✅ 原始 SQL 查询（如 `select(...)`）        | ✅ 是的      | 返回的是 `Row` 对象，不是 Pydantic 能自动识别的类型 |
| ✅ 多表联合查询、字段重命名（如 `.label(...)`）     | ✅ 是的      | 查询结果结构不等于模型定义，必须显式映射字段             |
| ✅ 聚合、分组查询（如 `func.count()`）         | ✅ 是的      | 返回聚合值，不是 ORM 模型对象                  |
| ❌ ORM 查询（如 `session.get(User, id)`） | ❌ 否       | 返回 ORM 模型，FastAPI + Pydantic 能自动处理 |
| ❌ `.from_orm(...)` 明确标记支持 ORM       | ❌ 否       | 可以直接返回，不用手动映射                      |

## Api/app/Models

其中分为两个文件夹：一个是model的（包含各个实体），另一个是dto层（定义了各种请求或响应的数据类型）



## Api_external/app/model/dtos/productfootprintsdtos

DTO(Data Transfer Object)模式

## Utils Folder

### user_disacle_accounts

这是一个“嵌套工具脚本子项目”的经典结构，通常表示：

这是一个用于单独执行的辅助脚本/子项目，用于批处理或运维任务，不是主API项目的核心部分，但和主项目数据结构有关。

#### 为什么它放在utils文件夹中？

是一个用于禁用用户账号（批量/定时/手动)的小脚本模块

他不面向前端的Web Api路由所以不放在routes/,services/里

#### 为什么它里面还有main.py和run.bat？

因为它被设计成可以单独执行，是一个可运行的脚本项目，和主系统解耦

**既然我们可以把禁用用户的功能写成一个页面或接口，等需要的时候再调用，为什么还要特地单独做一个工具脚本、main.py、run.bat 这些？**

原则问题还是：职责隔离。

把非核心逻辑/不对外暴露的功能封装成脚本工具（放在utils/或tools)。

- 把“非日常调用的功能”做成页面或 API 有风险
  
  - 暴露危险接口给外部
  
  - 误调用风险高
  
  - 接口要考虑权限、返回格式、容错、幂等……开发成本高

- 单独做成工具脚本的好处

| 目标            | 为什么要这么做                               |
| ------------- | ------------------------------------- |
| **隔离风险**      | 不部署到线上，不开放为接口，只能本地手动运行                |
| **运维友好**      | 运维人员双击 run.bat 就能跑，不需要懂 Python 代码     |
| **脚本自包含**     | 独立依赖环境（有 Pipfile），不依赖主项目运行状态          |
| **一次性任务更高效**  | 不需要起服务器，不需要依赖 FastAPI 的事件系统           |
| **更容易调试**     | print/日志随便打，不受框架限制                    |
| **适合定时任务/CI** | 可以丢给 cron、GitHub Actions、Airflow 去自动跑 |

## api/app/autogen.bat

是一个windows的批处理脚本，用于：

自动链接数据库并生成SQLAlchemy ORM模型文件。

它读取.env中的数据库配置+自动加密密码+调用sqlacodegen_v2_工具，从数据库结构生成ORM模型代码，并放入app/models文件夹中。

## api/app/main.py

”DB_PWD“这些是从.env或系统环境变量中读取**数据库链接相关的信息**，用于狗仔数据库链接字符串(URL)来链接数据库。
