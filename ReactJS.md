# ReactJS

## Intro

```js
npx create-react-app my-app
npm my-app
```

## Folder Structure

```js
my-react-app/
│── node_modules/        # 依赖包（npm/yarn安装）
│── public/              # 公共静态资源（如图片、favicon）
│── src/                 # 核心代码（主开发目录）
│   ├── assets/          # 图片、字体、样式等资源
│   ├── components/      # 可复用组件
│   ├── pages/           # 页面组件（Next.js特有）
│   ├── hooks/           # 自定义 Hook
│   ├── contexts/        # 全局状态管理
│   ├── services/        # API 请求（如 axios）
│   ├── utils/           # 工具函数
│   ├── styles/          # 全局样式（CSS/SASS/Tailwind）
│   ├── App.js           # 根组件
│   ├── index.js         # ReactDOM 入口文件
│── .gitignore           # Git 忽略文件
│── package.json         # 项目依赖与脚本
│── README.md            # 项目说明
```

## Components

在React中，组件是UI的基本构建块。每个组件可以是一个独立的可复用的UI单元。

React主要有两种组件:

- 函数组件（Function Component)--Stateless Component

- 类组件（Class Component)--Stateful Component

### Function Component

![](C:\Users\student2503\AppData\Roaming\marktext\images\2025-03-12-17-07-43-image.png)

使用JavaScript的函数定义组件并返回JSX结构。

#### 基本语法

```js
function Greeting() {
  return <h1>Hello, React!</h1>;
}

export default Greeting;
//使用的组件
<Greeting/>
```

#### 组件中的props(属性)

```js
function Greeting(props){
    return <h1>Hello,{props.name}!</h1>;
}
//使用组件
<Greeting name = "Alice"/>
```

#### 使用useState进行状态管理

useState用于在函数组件中创建可变的状态

```js
import {useState} from "react";

function Counter(){
    const [count,setCount] = useState(0);
    return (
    <div>
     <p>Count:{count}</p>
     <button onClick={()=>setCount(count+1)}>Increment</button>
    </div>
)；
}
export default Counter;
```

#### 使用useEffect进行副作用管理

useEffect处理副作用，如数据获取，订阅，手动DOM操作

```js
import { useState, useEffect } from "react";

function Timer() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(interval); // 组件卸载时清除定时器
  }, []);

  return <p>Timer: {seconds}s</p>;
}

export default Timer;
```

#### 事件处理

事件绑定可以直接在JSX语法中使用

```js
function ClickButton() {
  function handleClick() {
    alert("Button clicked!");
  }

  return <button onClick={handleClick}>Click Me</button>;
}
```

#### 组件之间的嵌套

```js
function Welcome() {
  return <h2>Welcome to React!</h2>;
}

function App() {
  return (
    <div>
      <Welcome />
      <p>This is a function component example.</p>
    </div>
  );
}
```

#### 组件的条件渲染

可以使用三元运算符或&&进行条件渲染

```js
function Message({ isLoggedIn }) {
  return <p>{isLoggedIn ? "Welcome back!" : "Please log in."}</p>;
}
```

### Class Components 类组件

#### 基本语法

```js
import React, { Component } from "react";

class Greeting extends Component {
  render() {
    return <h1>Hello, React!</h1>;
  }
}

export default Greeting;
```

Render()在类组件中的作用：

- React规定类组件必须包含render()方法，用来返回JSX结构。

- render()方法返回UI，他告诉React该组件该如何渲染。

Export default Welcome的作用：

- 有了这个Export default welcome，我们才可以在其他文件中导入该组件。

## Hooks Update(Hooks 更新)

React Hooks 允许在函数组件中使用状态(useState)和生命周期(useEffect)等功能，而无需使用类组件。

### useState更新状态

useState返回当前状态和更新状态的函数，每次调用更新函数，React会重新渲染组件。

```js
import { useState } from "react";
//SetCount(count+1)会触发组件的重新渲染
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
     // <button onClick={() => setCount(prevCount => prevCount + 1)}>
     // Increment
     //</button>
    </div>
  );
}

export default Counter;
```

### useEffect更新副作用

useEffect在组件选然后执行副作用（如数据获取，订阅时间）

```js
import { useState, useEffect } from "react";

function Timer() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds(prev => prev + 1);
    }, 1000);

    return () => clearInterval(interval); // 组件卸载时清除定时器
  }, []); // 依赖数组为空，仅在组件挂载时运行

  return <p>Timer: {seconds}s</p>;
}

export default Timer;
```

useEffect的更新规则

- useEffect(() => {...},[])  只运行一次(相当于componentDidMount)

- useEffect(() => {...},[state]) 依赖state变化时运行

- useEffect(() => {...}) 组件每次渲染后都会运行

### useReducer复杂状态更新

对于多个状态或逻辑复杂的更新，可以使用useReducer替代useState

```js
import { useReducer } from "react";

function reducer(state, action) {
  switch (action.type) {
    case "increment":
      return { count: state.count + 1 };
    case "decrement":
      return { count: state.count - 1 };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: "increment" })}>+</button>
      <button onClick={() => dispatch({ type: "decrement" })}>-</button>
    </div>
  );
}

export default Counter;
```

## JSX(JavaScript XML)

JSX是React的语法扩展，允许在JavaScript代码编写HTML结构，让UI代码更直观。

### JSX语法

JSX允许直接在JavaScript代码中写HTML：

```js
const element = <h1>Hello,JSX!</h1>
//如果要使用普通的JavaScript达到这样的效果的话
const element = React.createElement("h1",null,"Hello,JSX");
```

### JSX规则

**必须有一个父元素，必须用单个根标签包裹，或者也可以使用Fragment(<>....</>)代替<div>**

```js
return(
    <div>
        <h1>Hello</h1>
        <p>World</h1>
    </div>
);
```

**在JSX中使用JavaScript表达式**

JSX允许在{}中写JavaScript表达式：

```js
const name = "Alice";
return <h1>Hello,{name}!</h1>;


const age = 24;
return <p>{age >19 ? "Adult":"Minor"}</p>
```

**JSX中的class需要使用className**

```js
return <h1 className ="title"> Hello,JSX!</h1>;
```

**事件绑定**

```js
function ClickButton(){
    return <button onClick = {() => alert("Clicked!")}>CLick Me</button>;
}
```

**JSX中的style**

JSX的style需要用对象形式写：

```js
const headingStyle = {color:"blue",fontSize:"24px"};
return <h1 style={headingStyle}>Style Text</h1>
```

### JSX组件

```js
function Welcome(props){
    return <h1>Welcome,{props.name}!</h1>;
}
export default Welcome;

//使用的组件
<Welcome name="Alice"/>
```

## Props(属性)

Props(Properties)是React组件的输入参数，用于在**父组件向组组件传递数据**，让组件更加动态和可复用。

### 基本用法

父组件向子组件传递

```js
function Welcome(props){
    return <h1>Hello,{props.name}!</h1>;
}
export default Welcome;
//使用组件
<Welcome name = "Alice">
```

### 组件传递多个Props

```js
function UserInfo({name,age}){
    return (
    <p>
    Name:{name},Age:{age}
    </p>
);
}
```

### Props的默认值

可以使用defaultProps设置默认props

```js
function Greeting({name = "Guest"}){
    return <h1>Hello,{name}!</h1>;
}
//或者使用defaultProps。如果没有传递name，就会默认显示Guest
Greeting.defaultProps = {
    name:"Guest",
};
```

### 组件中的children（子元素）

Props.Children用于传递组件内部的内容：

```js
fu
nction Card({children}){
    return <div className = "card">{children}</div>;
}
//children
<Card>
    <h2>Title</h2>
    <p>This is card content.</p>
</Card>
```

### Props是只读的

```js
function Welcome(props) {
  props.name = "Bob"; // ❌ 不能修改 props
  return <h1>Hello, {props.name}!</h1>;
}
```

## State(状态)

State是React组件内部的可变数据，用于控制UI的动态变化。useState是React Hook，允许在函数组件中使用state。

### SetState(状态更新)

#### 不能直接修改state

在React类组件中,setState()是唯一正确的方式来更新state，不能直接修改this.state，否则组件不会重新渲染。

```js
import React,{Component} from "react";
class Counter extends Component{

    constructor(props){
        super(props)
        this.state = {
            count:0
        }
    }
    increment(){
// 不可以直接修改state
// React 指挥在setState()被调用的时候重新渲染组件
        this.setState({
            count:this.state.count+1
        })

        console.log(this.state.count)
    }

    render(){
        return(
        <div>
            <div>Counter - {this.state.count}</div>
            <button onClick={() => this.increment()}>Increment</button>
        </div>
        )
    }
}
export default Counter
```

#### setState()的异步性

如果连续用多次setState()，他不会立即更新State,而是会批量更新。

```js
increment(){
    this.setState({count:this.state.count + 1});
    console.log(this.state.count);//可能不会立即更新
}
//所以需要解决方案：使用回调函数
increment(){
    this.setState(prevState => ({count:prevState.count + 1}))
}
```

#### setState()批量更新

React可能会批量合并多个setState()调用，只有最后一次生效

```js
increment() {
  this.setState({ count: this.state.count + 1 });
  this.setState({ count: this.state.count + 1 });
  this.setState({ count: this.state.count + 1 });
}
```

上面的做法最终只会+1，不会+3，因为React优化了批量更新,

下面是正确的做法

```js
increment() {
  this.setState(prevState => ({ count: prevState.count + 1 }));
  this.setState(prevState => ({ count: prevState.count + 1 }));
  this.setState(prevState => ({ count: prevState.count + 1 }));
}
```

### setState处理对象

```js
this.setState({ user: { name: "Alice", age: 25 } });


//更新对象的时候要使用...spread
//这样就不会丢失对象的其他属性
this.setState(prevState => ({
  user: { ...prevState.user, age: 26 }
}));
```

## Destructuring props and state（解构赋值和状态）

解构props和state主要就是达到简写的目的

### Prop的解构赋值（简化写法）

```js
function Welcome({name}){
    return <h1>Hello,{name}!</h1>;
}
```

### State的解构

如果不解构的话 就需要：

```js
class Profile extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: "Alice",
      age: 25,
    };
  }
  render() {
    return (
      <div>
        <h1>{this.state.name}</h1>
        <p>Age: {this.state.age}</p>
      </div>
    );
  }
}
```

解构之后：

```js
render() {
    const { name, age } = this.state; // 解构 state
    return (
      <div>
        <h1>{name}</h1>
        <p>Age: {age}</p>
      </div>
    );
  }
}
```

### 函数组件中解构Props和State

```js
import { useState } from "react";

function Profile({ name, age }) {
  const [user, setUser] = useState({ name, age });

  return (
    <div>
      <h1>{user.name}</h1>
      <p>Age: {user.age}</p>
    </div>
  );
}
```

## Event Handling

React事件处理方式类似DOM事件，但也有一些不同：

- 使用驼峰命名（camelCase),比如是onClick而不是onclick

- 事件处理函数通常是箭头函数，或者在类组件中使用.bind(this)绑定this

- 事件处理不会默认触发event.preventDefault(),需要手动调用

### 事件处理的基本语法

```js
function ClickButton() {
  function handleClick() {
    alert("Button clicked!");
  }

  return <button onClick={handleClick}>Click Me</button>;
}
```

### 事件处理中的this绑定

在类组件中，事件处理方法中的this默认是undefined，需要手动绑定.

在下面的函数中，this.handleClick不加括号的原因是因为不想要在这个组件渲染的时候立即执行，这里的this.clickHandle是一个函数引用。

```js
class ClickButton extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this); // 绑定 this
  }

  handleClick() {
    alert("Button clicked!");
  }

  render() {
    return <button onClick={this.handleClick}>Click Me</button>;
  }
}
```

### 传递参数

```js
function Greeting({ name }) {
  function sayHello(customMessage) {
    alert(`${customMessage}, ${name}!`);
  }

  return <button onClick={() => sayHello("Hello")}>Greet</button>;
}
```

### Event 对象

React事件处理函数自动接收event对象。

```js
function InputBox() {
  function handleChange(event) {
    console.log("Input value:", event.target.value);
  }

  return <input type="text" onChange={handleChange} />;
}
```

### Event.preventDefault()

在React必须手动调用event.preventDefault()来阻止默认行为

```js
function Link() {
  function handleClick(event) {
    event.preventDefault(); // 阻止默认跳转
    alert("Link clicked!");
  }

  return <a href="https://google.com" onClick={handleClick}>Click Me</a>;
}
```

### 事件处理在useState中更新状态

```js
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  function increment() {
    setCount(prev => prev + 1);
  }

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
    </div>
  );
}
```

## Binding Event Handlers

**为什么要绑定this？**

在类组件中，this默认是undefine，如果不绑定，事件处理函数中的this无法访问state和props

### 绑定this的四种方法：

#### 在Constructor里bind(this)

在构造函数中使用.bind(this)绑定事件处理函数：

```js
class ClassClick extends Component {
  constructor() {
    super();
    this.state = { message: "Hello" };
    this.clickHandler = this.clickHandler.bind(this); // ✅ 绑定 this
  }

  clickHandler() {
    console.log(this.state.message); // ✅ 现在 this 指向类实例
  }

  render() {
    return <button onClick={this.clickHandler}>Click Me</button>;
  }
}
```

#### 使用箭头函数

onClick={() => this.clickHandler()}，在onClick内部用箭头函数调用clickHandler:

```js
class ClassClick extends Component {
  constructor() {
    super();
    this.state = { message: "Hello" };
  }

  clickHandler() {
    console.log(this.state.message);
  }

  render() {
    return <button onClick={() => this.clickHandler()}>Click Me</button>;
  }
}
```

#### 在Render()里.bind(this)

```js
class ClassClick extends Component {
  constructor() {
    super();
    this.state = { message: "Hello" };
  }

  clickHandler() {
    console.log(this.state.message);
  }

  render() {
    return <button onClick={this.clickHandler.bind(this)}>Click Me</button>;
  }
}
```

#### 使用箭头函数定义事件处理器

最佳的方式

```js
class ClassClick extends Component {
  constructor() {
    super();
    this.state = { message: "Hello" };
  }

  // ✅ 直接使用箭头函数，自动绑定 this
  clickHandler = () => {
    console.log(this.state.message);
  };

  render() {
    return <button onClick={this.clickHandler}>Click Me</button>;
  }
}
```

## Methods as props

在React中，父组件可以将方法作为props传递给子组件。

- 子组件可以通知父组件发生了某些事件（比如按钮点击，表单提交）

- 父组件可以控制子组件的行为，如更新state

### 基本用法

```js
import React, { Component } from 'react'
import ChildComponent from './ChildComponent'

class ParentComponent extends Component {
    constructor(props){
        super(props)
        this.state = {
            parentName:"Parent"
        }
        this.greetParent = this.greetParent.bind(this)
    }
    greetParent(childName){
        alert(`Hello ${this.state.parentName} from ${childName}`)
    }
  render() {
    return (
      <div>
        <ChildComponent greetHandler = {this.greetParent}/>
      </div>
    )
  }
}

export default ParentComponent
//ChildComponent
function ChildComponent(props) {
  return (
    <div>
      <button onClick ={() => props.greetHandler('child')} >Greet Parent</button>
    </div>
  )
}
export default ChildComponent
```

## Conditional Rendering(条件渲染)

条件渲染允许组件根据不同的状态（state)或者props动态的渲染UI。

### 使用if语句

```js
class UserGreeting extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: false,
    };
  }

  render() {
    if (this.state.isLoggedIn) {
      return <h1>Welcome back!</h1>;
    } else {
      return <h1>Please log in</h1>;
    }
  }
}

export default UserGreeting;
```

### 使用三元运算符（？：）

```js
class UserGreeting extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: false,
    };
  }

  render() {
    return (
      <div>
        {this.state.isLoggedIn ? <h1>Welcome back!</h1> : <h1>Please log in</h1>}
      </div>
    );
  }
}

export default UserGreeting;
```

### 使用&&(短路运算符)

```js
//只需要在true的时候显示某个内容，可以使用&&
// 只用在true的时候显示内容，false的时候不用显示
class UserGreeting extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: true,
    };
  }

  render() {
    return (
      <div>
        <h1>Welcome to the site!</h1>
        {this.state.isLoggedIn && <h2>Enjoy your stay.</h2>}
      </div>
    );
  }
}
```

### S witch case处理多种情况

```js
class UserGreeting extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      status: "guest", // 可选值: 'guest', 'user', 'admin'
    };
  }

  render() {
    let message;
    switch (this.state.status) {
      case "user":
        message = <h1>Welcome back, user!</h1>;
        break;
      case "admin":
        message = <h1>Welcome back, admin!</h1>;
        break;
      default:
        message = <h1>Welcome, guest! Please log in.</h1>;
    }

    return <div>{message}</div>;
  }
}
```

### 结合map()进行列表渲染

map()常用于遍历数组并渲染列表，他是JavaScript的数组方法，对数组的每个元素执行操作，并返回一个新的数组。

```js
const number = [1,2,3,4,5];
const doubled = numbers.map(num =>num*2);
console.log(doubled);//输出：[2,4,6,8,10]
```

```js
class ItemList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      items: ["Apple", "Banana", "Orange"],
    };
  }

  render() {
    return (
      <ul>
        {this.state.items.length > 0 ? (
          this.state.items.map((item, index) => <li key={index}>{item}</li>)
        ) : (
          <p>No items available</p>
        )}
      </ul>
    );
  }
}
```

## List and Keys

列表动态渲染多个元素，而key属性用于唯一标识列表项，让React在更新的时候更加高效。

## Index as Key Anti-pattern

不推荐使用index作为key，因为在React中，key需要唯一且稳定，但是使用index作为key可能会导致UI问题，渲染错误和性能问题。

**删除或插入项时UI可能出错**

列别项时可变的（用户可以删除或插入新项），使用index可能导致复用错误的DOM元素。

**输入到输入框时可能出错**

## Styling and CSS Basics(React中的样式和CSS基础)

在React中，有多种方式来给组件添加样式，常见的有：

- 普通的CSS文件

- 内联样式（Inline Style)

- CSS模块（CSS Modules)

- Style Components(CSS-in-JS方案)

- Tailwind CSS(实用类CSS框架)

### 普通的CSS文件

最常见的方式，在App.css或其他的CSS文件中编写样式

在App.css或Component.css里定义样式，然后在组件里引入CSS文件

```js
/* styles.css */
.container {
  background-color: lightblue;
  padding: 20px;
  border-radius: 5px;
}
/*模块文件*/
import React from "react";
import "./styles.css"; // ✅ 引入 CSS 文件

function App() {
  return <div className="container">Hello, React!</div>;
}

export default App;
```

### 内联样式（Inline Style)

直接在JSX里写Style,样式用对象格式

```js
function App() {
  const headingStyle = {
    color: "blue",
    fontSize: "24px",
    textAlign: "center"
  };

  return <h1 style={headingStyle}>Hello, React!</h1>;
}
```

### CSS模块（CSS Modules）

解决了全局CSS冲突，每个组件的样式是独立的

创建APP.module.css

```js
/* App.module.css */
.container {
  background-color: lightgreen;
  padding: 20px;
  text-align: center;
  border-radius: 5px;
}
```

在App.js中引入CSS模块

```js
import React from "react";
import styles from "./App.module.css"; // ✅ styles 作为对象导入

function App() {
  return <div className={styles.container}>Hello, React!</div>;
}

export default App;
```

### Style Components(CSS-in-JS)

适用于组件级别的样式，样式于组件绑定（需要安装Style Components)

```js
import styled from "styled-components";

const Button = styled.button`
  background-color: blue;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
`;

function App() {
  return <Button>Click Me</Button>;
}

export default App;
```

### Tailwind CSS

快速开发UI，使用实用类

无需写出CSS文件 直接在className中使用Tailwind的类名

## Basics of Form Handling

在React中，表单处理和普通的html表单略有不同，因为React组件需要控制表单数据的状态（state）

### 受控组件（Controlled Components)

在React中，表单输入通常是受控组件，即输入值受state控制

其中的useState是用于创建组件的状态变量

name-->状态变量,存储当前选中的名字（初始值为“ ”)

setFruit-->更新fruit状态的函数（用于修改fruit的值）

```js
import React, { useState } from "react";

function Form() {
  const [name, setName] = useState("");

  function handleChange(event) {
    setName(event.target.value); // ✅ 更新 `state`
  }

  function handleSubmit(event) {
    event.preventDefault(); // ✅ 防止页面刷新
    alert(`Submitted Name: ${name}`);
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>Name: </label>
      <input type="text" value={name} onChange={handleChange} />
      <button type="submit">Submit</button>
    </form>
  );
}

export default Form;
```

### 处理多个输入字段

如果有多个输入框，可以用一个state管理多个值

```js
import React, { useState } from "react";

function MultiInputForm() {
  const [formData, setFormData] = useState({
    username: "",
    email: ""
  });

  function handleChange(event) {
    const { name, value } = event.target; // ✅ 获取 `name` 和 `value`
    setFormData(prevState => ({
      ...prevState,
      [name]: value // ✅ 只更新当前输入框的值
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();
    alert(`Username: ${formData.username}, Email: ${formData.email}`);
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>Username: </label>
      <input type="text" name="username" value={formData.username} onChange={handleChange} />

      <label>Email: </label>
      <input type="email" name="email" value={formData.email} onChange={handleChange} />

      <button type="submit">Submit</button>
    </form>
  );
}

export default MultiInputForm
```

### 处理下拉框

event代表触发事件的对象，而event.target指向事件的目标元素(即发生事件的html元素)

- event ->事件对象，存储了事件的详细信息

- event.target ->触发事件的元素（这里是<select>）

- event.target.value ->获取<select>选中的值

```js
function SelectForm() {
  const [fruit, setFruit] = useState("apple");

  function handleChange(event) {
    setFruit(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    alert(`Selected: ${fruit}`);
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>Choose a fruit:</label>
      <select value={fruit} onChange={handleChange}>
        <option value="apple">Apple</option>
        <option value="banana">Banana</option>
        <option value="orange">Orange</option>
      </select>
      <button type="submit">Submit</button>
    </form>
  );
}
```

### 处理复选框

```js
function CheckboxForm() {
  const [isChecked, setIsChecked] = useState(false);

  function handleChange(event) {
    setIsChecked(event.target.checked); // ✅ `checked` 适用于 `checkbox`
  }

  function handleSubmit(event) {
    event.preventDefault();
    alert(`Checked: ${isChecked}`);
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        <input type="checkbox" checked={isChecked} onChange={handleChange} />
        Accept Terms
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}
```

### 处理单选按钮

```js
function RadioForm() {
  const [gender, setGender] = useState("");

  function handleChange(event) {
    setGender(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    alert(`Selected Gender: ${gender}`);
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        <input type="radio" name="gender" value="Male" onChange={handleChange} /> Male
      </label>
      <label>
        <input type="radio" name="gender" value="Female" onChange={handleChange} /> Female
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}
```

### 处理文本区域

```js
function TextAreaForm() {
  const [message, setMessage] = useState("");

  function handleChange(event) {
    setMessage(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    alert(`Message: ${message}`);
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>Message:</label>
      <textarea value={message} onChange={handleChange} />
      <button type="submit">Submit</button>
    </form>
  );
}
```

## Component Lifecycle Methods

 在React类组件中，组件有生命周期方法，用于在组件挂载(Mount)，更新(Update)和卸载(Unmount)时执行特定操作。

### 组件的生命周期阶段

React组件的生命周期分为三个阶段：

- 挂载(Mounting):组件被创建并插入DOM

- 更新(Updating):组件的state或props发生变化，触发重新渲染

- 卸载(Unmounting):组件从DOM中移除

- 处理错误(Error Handling): 渲染时遇到了错误

### 挂载阶段(Mounting)

| 方法                                              | 作用                         |
| ----------------------------------------------- | -------------------------- |
| `constructor()`                                 | 初始化 `state` 和绑定事件          |
| `static getDerivedStateFromProps(props, state)` | 根据 `props` 更新 `state`（不常用） |
| `render()`                                      | 返回 JSX，渲染 UI               |
| `componentDidMount()`                           | 组件挂载后执行（常用于 API 请求、订阅事件）   |

### 更新阶段(Updating)

| 方法                                                   | 作用                         |
| ---------------------------------------------------- | -------------------------- |
| `static getDerivedStateFromProps(props, state)`      | 根据 `props` 更新 `state`（不常用） |
| `shouldComponentUpdate(nextProps, nextState)`        | 控制组件是否重新渲染（优化性能）           |
| `render()`                                           | 重新渲染 UI                    |
| `getSnapshotBeforeUpdate(prevProps, prevState)`      | 获取更新前的 DOM 状态              |
| `componentDidUpdate(prevProps, prevState, snapshot)` | 组件更新后执行（常用于数据请求、DOM 操作）    |

### 卸载阶段(Unmounting)

| 方法                       | 作用                  |
| ------------------------ | ------------------- |
| `componentWillUnmount()` | 组件卸载前执行（清理定时器、事件监听） |

## Fragments(片段)

在React中，Fragments允许在不添加额外DOM元素的情况下，返回多个子元素。

我们不希望额外的<div>,他可能会导致不必要的嵌套。

### 使用React.Fragment

```js
import React from "react";

function FragmentExample() {
  return (
    <React.Fragment>
      <h1>Title</h1>
      <p>This is a description.</p>
    </React.Fragment>
  );
}

export default FragmentExample;
```

### 或者使用短语法<>...</>

```js
function FragmentShortSyntax() {
  return (
    <>
      <h1>Title</h1>
      <p>This is a description.</p>
    </>
  );
}

export default FragmentShortSyntax;
```

### key属性和Fragments

```js
const items = ["Apple", "Banana", "Orange"];

function List() {
  return (
    <React.Fragment>
      {items.map((item, index) => (
        <React.Fragment key={index}>
          <h2>{item}</h2>
          <p>Fruit item</p>
        </React.Fragment>
      ))}
    </React.Fragment>
  );
}

export default List;
```

## Pure Components

纯组件(pure components)时react自动优化的类组件，它可以减少不必要的重新渲染，同生性能。

### 纯组件的使用

```js
import React, { PureComponent } from "react";

class PureComponentExample extends PureComponent {
  render() {
    console.log("Pure Component Rendered");
    return <h1>Pure Component: {this.props.name}</h1>;
  }
}

export default PureComponentExample;
```

### 什么时候使用PureComponent

- 列表渲染优化

- 组件props不经常变化

- 数据量大，计算成本高

有时使用PureComponent也会出现问题：

- props/state可能包含对象，数组(浅比较可能导致误判)

- 组件依赖context，但context不会触发PureComponent重新渲染

## Memo(让函数组件变为纯组件)

在React中，React.memo()是一个高阶组件(HOC)，用于优化函数组件的性能，类似于PureComponent,只有props变化时才会重新渲染。

### 基本用法

```js
import React from 'react';

function MemoComp({ name }) {
  console.log('Rendering Memo Component');
  return (
    <div>
      {name}
    </div>
  );
}
export default React.memo(MemoComp);
```

### Refs(引用)

Refs允许我们直接访问DOM元素或React组件，通常用于：

- 操作DOM(如获取输入框的值，聚焦输入框)

- 与第三方库（如动画库，图标库）交互

- 存储组件实例，避免重新渲染

### 在类组件中使用Refs

```js
import React, { Component } from "react";

class InputFocus extends Component {
  constructor(props) {
    super(props);
    this.inputRef = React.createRef(); // 创建 ref
  }

  componentDidMount() {
    this.inputRef.current.focus(); // 组件挂载后自动聚焦
  }

  handleClick = () => {
    alert(this.inputRef.current.value); // 直接获取输入框值
  };

  render() {
    return (
      <div>
        <input type="text" ref={this.inputRef} />
        <button onClick={this.handleClick}>Get Value</button>
      </div>
    );
  }
}
export default InputFocus;
```

### 在函数组件中使用useRef()

```js
import React, { useRef, useEffect } from "react";

function InputFocus() {
  const inputRef = useRef(null); // 创建 ref

  useEffect(() => {
    inputRef.current.focus(); // 组件挂载后自动聚焦
  }, []);

  const handleClick = () => {
    alert(inputRef.current.value);
  };

  return (
    <div>
      <input type="text" ref={inputRef} />
      <button onClick={handleClick}>Get Value</button>
    </div>
  );
}

export default InputFocus;
```

### Refs 访问子组件

父组件控制子组件的输入框

```js
import React, { useRef, forwardRef, useImperativeHandle } from "react";

// 子组件
const ChildInput = forwardRef((props, ref) => {
  return <input type="text" ref={ref} />;
});

// 父组件
function ParentComponent() {
  const inputRef = useRef();

  const focusInput = () => {
    inputRef.current.focus();
  };

  return (
    <div>
      <ChildInput ref={inputRef} />
      <button onClick={focusInput}>Focus Input</button>
    </div>
  );
}

export default ParentComponent;
```

### useImperativeHandle()自定义暴露方法

用于子组件项只暴露特定方法给父组件,下面的就只会暴露focus()方法

```js
import React, { useRef, forwardRef, useImperativeHandle } from "react";

const ChildInput = forwardRef((props, ref) => {
  const inputRef = useRef();

  useImperativeHandle(ref, () => ({
    focus: () => {
      inputRef.current.focus();
    }
  }));

  return <input type="text" ref={inputRef} />;
});

function ParentComponent() {
  const childRef = useRef();

  return (
    <div>
      <ChildInput ref={childRef} />
      <button onClick={() => childRef.current.focus()}>Focus Input</button>
    </div>
  );
}

export default ParentComponent;
```

## React Portals(传送门)

Protals允许React组件渲染到当前组件树以外的DOM节点，即使它依然在React组件层级中。

通常：React组件会被渲染在root节点内（比如）：

```js
<div id= "root">
    <div>My App</div>
</div>
```

但有些情况下我们需要组件渲染在root外的DOM结构，比如：

- 模态框（Modal)

- 工具提示（Tooltip)

- 通知（Toast）

解决方案：使用ReactDOM.createProtal()

### 基本用法

让组件渲染到root之外的DOM结构

```js
//HTML结构
<div id="root"></div>
<div id="portal-root"></div>
//Modal.js(子组件)
import React from "react"
import ReactDOM from "react-dom"

function Modal({children}){
    return ReactDOM.createProtal(
    <div className="modal">
        {children}
    </div>,
    document.getElementById("portal-root")
);
}
export default Modal;
//App.js
import React, { useState } from "react";
import Modal from "./Modal";

function App() {
  const [showModal, setShowModal] = useState(false);

  return (
    <div>
      <h1>React Portals Example</h1>
      <button onClick={() => setShowModal(true)}>Open Modal</button>

      {showModal && (
        <Modal>
          <h2>Modal Content</h2>
          <button onClick={() => setShowModal(false)}>Close</button>
        </Modal>
      )}
    </div>
  );
}

export default App;
```

### Portals与事件冒泡

即使Portal组件渲染在root之外，事件依然会沿着React组件树冒泡：

比如：

```js
function Modal({ children }) {
  return ReactDOM.createPortal(
    <div className="modal" onClick={() => console.log("Modal Clicked")}>
      {children}
    </div>,
    document.getElementById("portal-root")
  );
}
```

即使Modal在portal-root，他的onClick事件依然会冒泡到App.js

ps.如果不希望事件冒泡，可以使用stopPropagation()

```js
<div className="modal" onClick={(e) => e.stopPropagation()}>
```

## Error Boundary

错误边界时React组件，用于捕获其子组件树中的JavaScript错误，并显示备用UI，而不会导致整个应用崩溃。

### ErrorBoundary的基本用法

error boundary 只能用于类组件，因为它依赖于componentDidCatch()生命周期方法。

1. 创建ErrorBoundary组件

```js
import React, { Component } from "react";

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    // 更新 state，使下次渲染显示备用 UI
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    console.error("Error caught by ErrorBoundary:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return <h2>Something went wrong.</h2>; // 备用 UI
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
```

2. 在APP.js里使用ErrorBoundary

```js
import React from "react";
import ErrorBoundary from "./ErrorBoundary";
import BuggyComponent from "./BuggyComponent";

function App() {
  return (
    <div>
      <h1>React Error Boundary Example</h1>
      <ErrorBoundary>
        <BuggyComponent />
      </ErrorBoundary>
    </div>
  );
}

export default App;

```

3. BuggyComponent.js

```js
import React, { Component } from "react";

class BuggyComponent extends Component {
  constructor(props) {
    super(props);
    this.state = { throwError: false };
  }

  handleClick = () => {
    this.setState({ throwError: true });
  };

  render() {
    if (this.state.throwError) {
      throw new Error("Oops! Something went wrong.");
    }
    return <button onClick={this.handleClick}>Click to trigger error</button>;
  }
}

export default BuggyComponent;


```

注意：ErrorBoundary只能捕获渲染阶段的错误；生命周期方法中的错误；子组件constuructor()里的错误，它不能捕获事件处理函数中的错误；异步代码；服务端渲染SSR中的错误，自身（ErrorBoundary）组件的错误。

## HOC(Higher Order Components)高阶组件

高阶组件是一种用于复用组件逻辑的模式，它本质上是一个接受组件作为参数，并返回一个新组建的函数。

为什么需要HOC：

有时候我们需要在多个组件中共享相同的逻辑：比如：

- 权限控制

- 日志记录

- 状态管理

- API数据获取

- 增加功能（如计数功能）

### HOC的基本用法

```js
const withExtraFunctionality = (WrappedComponent) => {
  return function EnhancedComponent(props) {
    return <WrappedComponent {...props} />;
  };
};
```

HOC主要做两件事：

1.接收一个组件（wrappedComponent)

2.返回一个新组件EnhancedComponent,可以增强功能

### HOC例子：计数器功能

我们有两个不同的组件ClickCounter和HoverCounter，但他们共享相同的计数逻辑

1.  创建withCoynter.js(HOC组件)

```js
import React, { useState } from "react";

const withCounter = (WrappedComponent) => {
  return function EnhancedComponent(props) {
    const [count, setCount] = useState(0);

    const incrementCount = () => {
      setCount(count + 1);
    };

    return <WrappedComponent count={count} incrementCount={incrementCount} {...props} />;
  };
};

export default withCounter;
```

2. clickCounter.js

```js
import React from "react";
import withCounter from "./withCounter";

function ClickCounter({ count, incrementCount }) {
  return <button onClick={incrementCount}>Clicked {count} times</button>;
}

export default withCounter(ClickCounter); // ✅ 使用 HOC
```

3. HoverCounter.js

```js
import React from "react";
import withCounter from "./withCounter";

function HoverCounter({ count, incrementCount }) {
  return <h2 onMouseOver={incrementCount}>Hovered {count} times</h2>;
}

export default withCounter(HoverCounter); // ✅ 使用 HOC
```

4. 在APP.js中使用

```js
import React from "react";
import ClickCounter from "./ClickCounter";
import HoverCounter from "./HoverCounter";

function App() {
  return (
    <div>
      <h1>React Higher Order Component Example</h1>
      <ClickCounter />
      <HoverCounter />
    </div>
  );
}

export default App;
```

## Render Props(渲染属性模式)

Render Props是React组件复用的一种模式，它允许我们在组件之间共享逻辑，而不是用HOC。

为什么需要Render Props?

在React中，如果多个组件需要共享相同的逻辑(例如state和setState)，可以用：

- HOC(高阶组件)

- Render Props(渲染属性模式)

- Hooks(推荐)

HOC vs Render Props

- HOC：逻辑封装在高阶组件中，返回增强后的组件。

- Render Props：将逻辑封装在组件中，通过props传递redner方法，让子组件自定义UI。

HOC的缺点：

- HOC可能会导致嵌套地狱

- 组件层级可能不容易理解

- Render Props更加灵活，可以随时传递props，避免this绑定问题

### 基本用法

1. Counter.js

```js
import React, { Component } from "react";

class Counter extends Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 };
  }

  increment = () => {
    this.setState(prevState => ({ count: prevState.count + 1 }));
  };

  render() {
    return this.props.render(this.state.count, this.increment); // ✅ 通过 `render` 传递 `count` 和 `increment`
  }
}

export default Counter;
```

2. ClickCounter.js点击计数器

```js
import React from "react";
import Counter from "./Counter";

function ClickCounter() {
  return (
    <Counter render={(count, increment) => (
      <button onClick={increment}>Clicked {count} times</button>
    )} />
  );
}

export default ClickCounter;
```

3. HoverCounter.js

```js
import React from "react";
import Counter from "./Counter";

function HoverCounter() {
  return (
    <Counter render={(count, increment) => (
      <h2 onMouseOver={increment}>Hovered {count} times</h2>
    )} />
  );
}

export default HoverCounter;
```

## React Context(上下文)

Context允许我们在组件树中跨层级传递数据，而无需通过props逐层传递。

适用于主题，用户身份验证，全局状态等场景

**为什么需要Context?**

在没有Context的情况下 我们通常需要逐层传递Props（props drilling）

```js
<Parent>
    <Child>
        <GrandChild user ="Zijie"/>
    </Child>
</Parent>
```

如果GrandChild需要user，但Parent和Child不适用user，我们依然需要手动传递props，这很麻烦。

### 创建Context

UserContext.js

```js
import React from "react"
//创建Context（默认值为‘Guest')
const UserContext = React.createContext("Guest");

export default UserContext;
```

### Provide提供数据

App.js

```js
import React from "react";
import UserContext from "./UserContext";
import ChildComponent from "./ChildComponent";

function App() {
  return (
    // 2️⃣ 使用 `UserContext.Provider` 提供数据
    <UserContext.Provider value="Zijie">
      <ChildComponent />
    </UserContext.Provider>
  );
}

export default App;
```

### Consumer:使用Context

GrandChild.js(GrandChild 可以直接读取UserContext,不需要props传递)

```js
import React from "react";
import UserContext from "./UserContext";

function GrandChild() {
  return (
    // 3️⃣ 使用 `UserContext.Consumer` 读取 `Context`
    <UserContext.Consumer>
      {user => <h1>Hello, {user}!</h1>}
    </UserContext.Consumer>
  );
}

export default GrandChild;
```

### userContext()

在函数组件中，我们可以使用userContext()替代Consumer

```js
import React,{useContext} from "react";
import UserContext from "./UserContext"

function GrandChild(){
    const user = useContext(UserContext);
    return <h1>Hello,{user}!</h1;
}
export default GrandChild;
```

## 组件

在React中，组件可以用三种方式定义：

1. 类组件

2. 函数组件

3. 变量存储函数组件（const Component = () => {}）

Const也是函数组件

在React中，函数组件本质上就是一个普通的JavaScript函数，他返回JSX，所以我们可以用function或者const来定义它：

```js
// ✅ 标准函数组件
function Hello() {
  return <h1>Hello, World!</h1>;
}

// ✅ 使用 `const` 创建箭头函数组件
const Hello = () => {
  return <h1>Hello, World!</h1>;
};
```

两种写法是等价的，const只是让组件不能被重新赋值（不可变）



## Http and React

在React应用中，HTTP请求用于与后端服务器进行通信，以获取数据，提交数据等

### React 处理HTTP请求的方式

在React中，我们通常使用一下方式进行HTTP请求：

| **方法**            | **适用场景**  | **优点**           |
| ----------------- | --------- | ---------------- |
| **`fetch()`**     | 轻量级请求     | 内置 API，无需安装额外库   |
| **`axios`**       | 处理复杂请求    | 更简洁，支持自动 JSON 解析 |
| **`react-query`** | 数据缓存与自动刷新 | 适用于数据密集型应用       |

### 使用fetch进行http请求

在useEffect()里获取数据

```js
import React, { useState, useEffect } from "react";

function FetchExample() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("https://jsonplaceholder.typicode.com/posts")
      .then(response => response.json()) // ✅ 解析 JSON
      .then(data => setData(data.slice(0, 5))) // ✅ 只取前 5 条数据
      .catch(error => console.error("Error:", error));
  }, []);

  return (
    <div>
      <h2>Posts</h2>
      <ul>
        {data.map(post => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default FetchExample;
```

### 使用axios进行HTTP请求

Axios是一个更高级的HTTP库，比fetch更易用

- 自动解析JSON

- 请求和响应拦截

- 取消请求

- 更好的错误处理

axios进行GET请求

```js
import React, { useState, useEffect } from "react";
import axios from "axios";

function AxiosExample() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios
      .get("https://jsonplaceholder.typicode.com/posts")
      .then(response => setData(response.data.slice(0, 5))) // ✅ 直接获取 `response.data`
      .catch(error => console.error("Error:", error));
  }, []);

  return (
    <div>
      <h2>Posts</h2>
      <ul>
        {data.map(post => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default AxiosExample;
```

### POST请求

fetch提交数据

```js
fetch("https://jsonplaceholder.typicode.com/posts", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ title: "New Post", body: "Hello World" }),
})
  .then(response => response.json())
  .then(data => console.log("Created Post:", data));
```

axios提交数据

```js
axios
  .post("https://jsonplaceholder.typicode.com/posts", {
    title: "New Post",
    body: "Hello World",
  })
  .then(response => console.log("Created Post:", response.data));
```

### Put和Delete请求

```js
axios.put("https://jsonplaceholder.typicode.com/posts/1", {
  title: "Updated Title",
})
.then(response => console.log("Updated:", response.data));

//Delete
axios.delete("https://jsonplaceholder.typicode.com/posts/1")
  .then(response => console.log("Deleted:", response.data));
```

### 使用async/await进行异步请求

```js
async function fetchData() {
  try {
    const response = await axios.get("https://jsonplaceholder.typicode.com/posts");
    console.log("Data:", response.data);
  } catch (error) {
    console.error("Error:", error);
  }
}

fetchData();
```

### React-Query(高级用法，推荐)

react-query自动缓存和管理数据。适用于大型应用

```js
import { useQuery } from "@tanstack/react-query";
import axios from "axios";

function Posts() {
  const { data, isLoading, error } = useQuery(["posts"], async () => {
    const response = await axios.get("https://jsonplaceholder.typicode.com/posts");
    return response.data;
  });

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error loading data</p>;

  return (
    <ul>
      {data.slice(0, 5).map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}

export default Posts;

```



- 自动缓存请求

- 自动重试失败请求

- 自动更新UI
