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

#### Props传递数据

```js
class Greeting extends Component {
  render() {
    return <h1>Hello, {this.props.name}!</h1>;
  }
}
//使用的组件
<Greeting name = "Alice"/>
```

#### State组件的内部状态

state用于存储组件内部的可变数据

```js
class Counter extends Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 };
  }

  increment = () => {
    this.setState({ count: this.state.count + 1 });
  };

  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button onClick={this.increment}>Increment</button>
      </div>
    );
  }
}

export default Counter;
```

#### 生命周期方法

```js
import React, { Component } from "react";

class Timer extends Component {
  constructor(props) {
    super(props);
    this.state = { seconds: 0 };
  }

  componentDidMount() {
    this.interval = setInterval(() => {
      this.setState({ seconds: this.state.seconds + 1 });
    }, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  render() {
    return <p>Timer: {this.state.seconds}s</p>;
  }
}

export default Timer;

```

#### 事件处理

```js
class ClickButton extends Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    alert("Button clicked!");
  }

  render() {
    return <button onClick={this.handleClick}>Click Me</button>;
  }
}
```

#### 条件渲染

```js
class Message extends Component {
  render() {
    return <p>{this.props.isLoggedIn ? "Welcome back!" : "Please log in."}</p>;
  }
}
```




