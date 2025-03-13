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


