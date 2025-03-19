# NextJS

## Routing

NextJS的路由系统基于文件系统，我们创建的文件和文件夹结构直接决定了应用路由。

### 基础页面路由

📁 `app`

- 📄 `page.tsx` → `/`（首页）
- 📁 `about`
  - 📄 `page.tsx` → `/about`（关于页面）
- 📁 `blog`
  - 📄 `page.tsx` → `/blog`（博客首页）
  - 📁 `[id]`
    - 📄 `page.tsx` → `/blog/:id`（动态路由）

### 动态路由

如果需要创建动态路径，比如/blog/123，可以使用方括号定义动态路由：

```js
app/
  blog/
    [id]/
      page.tsx  # 对应 /blog/:id
```

示例代码（app/blog/[id]/page.tsx),当访问/blog/123时，params.id会自动解析为123.

```js
export default function BlogPost({params}:{params:{id:string}}){
    return <h1>Bolg Post Id:{params.id}</h1>
}
```

### 可选的动态路由

如果某个动态参数时可选的，可以使用双方括号

```js
app/
  blog/
    [[id]]/
      page.tsx  # 对应 /blog 或 /blog/:id
```

### 嵌套路由&Layouts

```js
app/
  layout.tsx  # 全局布局
  page.tsx  # 首页
  dashboard/
    layout.tsx  # dashboard 专属布局
    page.tsx  # /dashboard
    settings/
      page.tsx  # /dashboard/settings
```

示例代码(app/dashboard/layout.tsx)

```js
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <nav>Dashboard Navigation</nav>
      <main>{children}</main>
    </div>
  );
}
```

### API路由

NextJS允许在app/api目录下定义API路由：

📁 `app/api`

- 📁 `hello`
  - 📄 `route.ts` → `GET /api/hello`

示例代码(app/api/hello/route.ts)

```js
export async function GET() {
  return Response.json({ message: "Hello, Next.js!" });
}
```

访问/api/hello时，浏览器会收到{"message":"Hello,Next.js!"}

### 页面重定向和自定义404

NextJS允许你在not-found.tsx文件中定义自定义404页面：

示例代码:

```js
export default function NotFound() {
  return <h1>Page Not Found</h1>;
}
```

也可以使用redirect()进行页面重定向：

```js
import { redirect } from "next/navigation";

export default function Page() {
  redirect("/dashboard");
}
```

## Catch All Segments(捕获所有路由段)

在NextJS中，Catch-All Segments允许你匹配多个URL段，并在组件中获取他们的参数。这种路由模式适用于位置数量的动态路由，比如博客分类，文件系统路径等

### 基本用法

可以使用[...slug]来创建一个捕获所有路由段的动态路径

📁 `app/blog`

- 📄 `page.tsx` → `/blog`（博客首页）
- 📁 `[...slug]`
  - 📄 `page.tsx` → `/blog/*`（捕获所有路径）

示例代码(app/blog/[...slug]/page.tsx)

```js
export default function Blog({ params }: { params: { slug?: string[] } }) {
  return <h1>Blog Path: {params.slug ? params.slug.join(" / ") : "Home"}</h1>;
}
```

### 可选的Catch-All路由

如果你希望/blog也匹配app/blog/[...slug]/page.tsx,但params.slug依然能为undefined，可以使用可选Catch-All路由"[[...sulg]]"

📁 `app/blog`

- 📁 `[[...slug]]`
  - 📄 `page.tsx` → `/blog/*`（包含 `/blog`）

示例代码 app/blog/[[...slug]]/page.tsx

```js
export default function Blog({ params }: { params: { slug?: string[] } }) {
  return <h1>Blog Path: {params.slug ? params.slug.join(" / ") : "Home"}</h1>;
}
```

这样的区别在于:普通[...slug]不会匹配/blog，但[[...slug]]可以匹配/blog并且params.slug为unfined.

### 结合API路由

可以在app/api目录中使用Catch-All路由来创建动态API端点：

📁 `app/api`

- 📁 `[...slug]`
  - 📄 `route.ts` → `/api/*`

```js
export async function GET(req: Request, { params }: { params: { slug?: string[] } }) {
  return Response.json({ path: params.slug ?? "root" });
}
```

**API 请求情况**

| API URL             | 响应 JSON                           |
| ------------------- | --------------------------------- |
| `/api`              | `{ "path": "root" }`              |
| `/api/user`         | `{ "path": ["user"] }`            |
| `/api/user/profile` | `{ "path": ["user", "profile"] }` |

## 文件后最的.ts和.tsx的区别

**.ts文件(TypeScript文件)：**

- 适用于纯TypeScript代码(没有JSX)

- 主要用于：
  
  - 普通TypeScript代码(如工具函数，后端API逻辑)
  
  - 类型定义文件(如type.ts,interfaces.ts)
  
  - 不涉及React组件的逻辑

示例：

```ts
export function add(a: number, b: number): number {
  return a + b;
}
```

.tsx(TypeScript + JSX)

- 适用于包含JSX(即React组件)的TypeScript文件

- 必须使用.tsx才能在TypeScript中编写JSX

- 主要用于：
  
  - React组件
  
  - 不需要使用JSX语法的文件

示例：

```tsx
import React from "react";

interface ButtonProps {
  label: string;
}

export default function Button({ label }: ButtonProps) {
  return <button>{label}</button>;
}
```

什么时候用.ts什么时候用.tsx?

| **文件类型**                      | **扩展名** | **示例**                               |
| ----------------------------- | ------- | ------------------------------------ |
| **工具函数 / 业务逻辑**               | `.ts`   | `utils.ts`, `api.ts`, `constants.ts` |
| **React 组件**                  | `.tsx`  | `Header.tsx`, `Button.tsx`           |
| **类型定义 / 接口**                 | `.ts`   | `types.ts`, `interfaces.ts`          |
| **React 组件的 hooks（如果包含 JSX）** | `.tsx`  | `useTheme.tsx`（如果需要返回 JSX）           |
| **React 组件的 hooks（无 JSX）**    | `.ts`   | `useAuth.ts`（如果只处理逻辑）                |

## Not Found Page

Not Found 页面用于处理找不到的路由或某些数据不存在的情况，可以使用not-found.tsx文件来自定义404页面,并且可以在组件或API逻辑中手动触发404状态。

### 全局404页面

在app目录下，创建not-found.tsx文件

### 手动触发not found

可以在动态页面(如app/blog/[id]/page.tsx)或api端点中使用notfound()方法来手动触发404

📁 `app/blog`

- 📁 `[id]`
  - 📄 `page.tsx` → 动态博客详情页

示例：

```tsx
import { notFound } from "next/navigation";

export default function BlogPost({ params }: { params: { id: string } }) {
  const validPosts = ["1", "2", "3"]; // 假设数据库中只有 ID 1, 2, 3 的文章

  if (!validPosts.includes(params.id)) {
    notFound(); // 触发 404 页面
  }

  return <h1>Blog Post {params.id}</h1>;
}
```

当访问/blog/1时，正常显示文章内容。

当访问/blog/999(不存在的文章Id)时，会自动跳转到Not-Found页面

### API端点中的404

在API路由(app/api/*)里，你可以使用Response对象返回404状态码

📁 `app/api`

- 📁 `user`
  - 📄 `[id]/route.ts` → API 用户详情

示例：app/api/user/[id]/route.ts

```tsx
export async function GET(req: Request, { params }: { params: { id: string } }) {
  const users = { "1": "Alice", "2": "Bob" };

  if (!users[params.id]) {
    return new Response(JSON.stringify({ error: "User not found" }), { status: 404 });
  }

  return Response.json({ name: users[params.id] });
}
```

### 在Layout里处理404

如果想在某个layout.tsx里拦截找不到的子页面：

📁 `app/dashboard`

- 📄 `layout.tsx` → Dashboard Layout
- 📄 `page.tsx` → Dashboard 首页
- 📁 `[...slug]`
  - 📄 `page.tsx` → 捕获所有路径（手动处理 404）

```tsx
import { notFound } from "next/navigation";

export default function Dashboard({ params }: { params: { slug?: string[] } }) {
  if (!params.slug || params.slug[0] !== "settings") {
    notFound();
  }

  return <h1>Dashboard Settings</h1>;
}
```

当访问/dashboard/settings时-->正常显示

当访问/dashboard/xyz时-->触发not-found.tsx

## File Colocation(文件共置)

File Colocation是一种组织代码文件的方法，旨将相关的代码文件放在一起，用来提高可读性，可维护性和开发效率。

### 基于File Colocation组织的组件

```tsx
components/
  Button/
    Button.tsx       # 组件
    Button.module.css # 样式
    Button.test.tsx   # 测试
    Button.types.ts   # 类型定义
    index.ts          # 组件导出
```

这样所有的button相关的文件都在Button/目录下，而不是把样式，测试，类型定义等文件分别放在style/,tests/之类的全局目录里

### 为什么使用File Colocation

- 更容易理解：所有的文件都在同一个地方减少查找的时间

- 避免全局文件夹的混乱：不需要components.ts,styles/,tests/等全局目录来存放分散的文件

- 提高组件的可移植性：可以直接复制整个组件文件夹到另一个项目，而不丢失相关代码

### 示例1:页面组件

```tsx
app/
  dashboard/
    page.tsx         # 页面
    Dashboard.module.css # 样式
    DashboardHeader.tsx  # 内部组件
```

### 示例二:API逻辑

```tsx
app/
  blog/
    [id]/
      page.tsx       # 文章详情页
      fetchPost.ts   # 获取文章数据
```

示例代码(app/blog/[id]/page.tsx)

```tsx
import { fetchPost } from "./fetchPost";

export default async function BlogPost({ params }: { params: { id: string } }) {
  const post = await fetchPost(params.id);
  return <h1>{post.title}</h1>;
}
```

示例代码(app/blog/[id]/fetchPost.ts)

```tsx
export async function fetchPost(id: string) {
  const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`);
  return res.json();
}
```

### 示例三:组件封装

components

```tsx
components/
  Card/
    Card.tsx         # 组件
    Card.module.css  # 样式
    index.ts         # 组件导出
```

示例(components/Card/Card.tsx)

```tsx
import styles from "./Card.module.css";

export default function Card({ children }: { children: React.ReactNode }) {
  return <div className={styles.card}>{children}</div>;
}
```

示例代码(components/Card/index.ts)

```tsx
export { default } from "./Card";
```

## Private Folders(私有文件夹)

private folders私有文件夹是指不会自动成为路由的文件夹，这种机制允许在app/目录下组织数据，工具函数，组件等非路由相关的内容。

在NextJS的app/目录下，文件或文件夹的名称以_(下划线）或(（圆括号）开头的文件夹不会变成页面路由。可以在app/目录内组织goon共享逻辑，组件，api请求等。

### _下划线命名的Private Folder

文件结构:

```tsx
app/
  dashboard/
    page.tsx        # /dashboard
    _components/    # 这里的组件不会影响路由
      Sidebar.tsx
      DashboardHeader.tsx
//_components文件夹不会变成/dashboard/_components路由，只是存放组件。
```

### ( )（圆括号）命名的Private Floder

文件结构：

```tsx
app/
  dashboard/
    page.tsx        # /dashboard
    (utils)/        # 这里的工具函数不会影响路由
      fetchData.ts
```

上面两者的区别：

| **方式**             | **适用场景**            | **是否影响路由** |
| ------------------ | ------------------- | ---------- |
| `_privateFolder/`  | 适用于存放组件、工具函数、逻辑代码   | ❌ 不会影响     |
| `(privateFolder)/` | 适用于数据获取、API 逻辑、共享代码 | ❌ 不会影响     |

### 应用场景

#### 存放页面专属的UI组件

```tsx
app/
  dashboard/
    page.tsx
    (components)/
      Sidebar.tsx
      DashboardHeader.tsx
//这些组件只用于dashboard/,所以不需要放在全局components/
```

#### 存放API逻辑

```tsx
app/
  blog/
    [id]/
      page.tsx
      (api)/
        fetchPost.ts
//这样的fetchPost.ts只用于blog/[id]页面，不会暴露在路由中。
```

#### 存放页面的Layout

```tsx
app/
  dashboard/
    layout.tsx
    (layouts)/
      Sidebar.tsx
      TopBar.tsx
//这样Sidebar.tsx和TopBar.tsx只在dashboard相关页面使用
```

## Route Groups(路由分组)

允许组织路由，而不会影响URL结构，它主要用于代码组织，可以帮助你管理不同的页面模块，比如后台管理，用户页面，多语言支持等。

### 什么是Route Groups?

在 `app/` 目录中，使用 **`()`（圆括号）包裹的文件夹名**，可以创建路由分组，而不会影响 URL 结构。例如：

```tsx
app/
  (marketing)/       # ✅ 路由分组，不影响最终 URL
    home/
      page.tsx       # /
    about/
      page.tsx       # /about
  (dashboard)/       # ✅ 另一个路由分组
    settings/
      page.tsx       # /settings
    profile/
      page.tsx       # /profile
```

### Route Groups的常见用法

模块化管理

```tsx
app/
  (dashboard)/        # ✅ 后台管理相关页面
    layout.tsx        # /dashboard 的布局
    page.tsx          # /dashboard
    users/
      page.tsx        # /dashboard/users
  (marketing)/        # ✅ 前台网站
    home/
      page.tsx        # /
    about/
      page.tsx        # /about
//(dashboard)和(marketing)只是代码组织，不影响URL结构。
```

结合Layout,文件结构

```tsx
app/
  (dashboard)/
    layout.tsx         # 共享的 Dashboard 布局
    settings/
      page.tsx         # /dashboard/settings
    profile/
      page.tsx         # /dashboard/profile
```

示例代码：

```tsx
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <nav>Dashboard Navigation</nav>
      <main>{children}</main>
    </div>
  );
}//所有的dashboard/*页面都会使用整个layout.tsx
```

## Layout

layout是一种用于共享页面结构的方式，它可以让多个页面复用相同的UI结构，比如导航栏（Navbar),侧边栏(Sidebar),页脚(Footer)等。

### Layout的基本用法

任何layout.tsx文件都会包裹同级目录下的page.tsx页面。app/layout.tsx

```tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav>🌎 Global Navbar</nav>
        {children}
        <footer>🌍 Global Footer</footer>
      </body>
    </html>
  );
}
```

### 局部layout(嵌套路由)

NextJs允许在不同的文件夹下创建局部layout，每个子Layout只会影响它所在的目录。

### Layout与Loading

每个layout.tsx还可以有对应的loading.tsx来处理页面加载状态。

示例代码：

```tsx
export default function Loading() {
  return <h1>⏳ Loading Dashboard...</h1>;
}
```

### 结合Route Group

可以使用Route Groups(路由分组)让多个Layout结构更清晰。

```tsx
app/
  (marketing)/
    layout.tsx     # 📢 公共营销布局
    home/
      page.tsx     # /
    about/
      page.tsx     # /about
  (dashboard)/
    layout.tsx     # 🖥 仅用于 dashboard
    page.tsx       # /dashboard
    settings/
      page.tsx     # /dashboard/settings
```

示例代码(app/(marketing)/layout.tsx)

```tsx
export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <nav>📢 Marketing Navbar</nav>
      {children}
    </div>
  );
}
```

示例代码(app/(dashboard)/layout.tsx)

```tsx
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <nav>🖥 Dashboard Sidebar</nav>
      <main>{children}</main>
    </div>
  );
}
```

这样marketing和dashboard有独立的布局，但URL结构不会受到影响。

## Routing Metadata(路由元数据)

路由元数据用于定义页面的SEO信息(如Title，description，keywords等)，这些信息不会影响URL，但会影响搜索引擎优化（SEO）和社交媒体分享。

### 在Page.tsx中定义Metadata

Nextjs允许在page.tsx文件中导出metadata对象：

```tsx
//title会设置<title>标签，影响网页标题
//description会设置<meta name="descriptuon">,提高SEO友好性。
export const metadata = {
  title: "Home Page",
  description: "这是一个 Next.js 示例页面",
};

export default function HomePage() {
  return <h1>🏠 Home Page</h1>;
}
```

### 在Layout中定义全局Metadata

如果你希望metadata作用于整个路由(如/home下的所有页面)，可以在layout.tsx里定义

```tsx
export const metadata = {
  title: "Home Section",
  description: "包含所有 Home 相关页面",
};

export default function HomeLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <nav>Home Navbar</nav>
      {children}
    </div>
  );
}
```

### 动态Metadata

如果title或description需要根据params或API数据动态生成，可以使用generateMetadata():

```tsx
import { Metadata } from "next";

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const res = await fetch(`http://127.0.0.1:8000/api/posts/${params.id}`);
  const post = await res.json();

  return {
    title: post.title,
    description: post.content.slice(0, 100), // 只取前100个字符
  };
}

export default function PostPage({ params }: { params: { id: string } }) {
  return <h1>文章 {params.id}</h1>;
}
```

## Link Component Navigation

Link组件导航，用于在页面之间进行导航，并且比传统的<a href="">更高效，原因是：

- 支持客户端导航（不刷新页面）

- 自动预加载，加快页面切换速度

- 支持动态路由，适用于[id]这样的动态参数

### 基本用法

```tsx
import Link from "next/link";

export default function HomePage() {
  return (
    <div>
      <h1>🏠 Home Page</h1>
      <Link href="/about">前往 About 页面</Link>
    </div>
  );
}
```

### a标签vs<link>组件

| **方法**                                   | **特点**        | **是否刷新页面**        |
| ---------------------------------------- | ------------- | ----------------- |
| `<a href="/about">Go to About</a>`       | 传统 HTML 超链接   | ✅ **会刷新**整个页面     |
| `<Link href="/about">Go to About</Link>` | Next.js 客户端路由 | ❌ **不会刷新**页面，速度更快 |

### next/link的prefetch预加载

Nextjs会默认预加载<link>指向的页面，让页面切换的更快，但可以手动关闭：

```tsx
//默认的prefetch=true
<Link href="/contact" prefetch={false}>联系页面</Link>
```

### 在<Link>里包裹a标签

如果想要使用<a>又想要保持Next.js的优化，可以这样

```tsx
<Link href="/blog">
  <a>前往 Blog</a>
</Link>
```

### 在Next.js里传递动态参数

适用于有一个动态路由[id]：

```tsx
<Link href={{ pathname: "/blog/[id]", query: { id: "123" } }}>
  文章 123
</Link>
```

### replace参数（不保留历史记录）

默认情况下，<Link>会将页面推入浏览器历史记录，但如果你不想让用户回到上一个页面，可以使用replace：

```tsx
<Link href="/dashboard" replace>前往 Dashboard（不保留历史）</Link>
```

### scroll={false}(防止滚顶到顶部)

默认情况下，<Link>会自动滚动到页面顶部，如果想要保持当前位置，可以使用scroll={false}

```tsx
<Link href="/profile" scroll={false}>前往 Profile（不滚动）</Link>
```

### shallow路由(不重新获取数据)

如果页面使用useEffect从后端获取数据，点击<Link>时默认会重新请求数据。

这就意味着每次跳转/products，都会重新请求数据

如果不希望重新请求，可以用shallow={true}

```tsx
<Link href="/products" shallow>产品列表（不重新请求）</Link>
```

### Active Links(当前激活的链接)

在Next.js中我们通常希望高亮正在访问的页面链接：

- 当前页面是/about，那么整个导航项应该高亮。

- 选中/dashboard时，Dashboard按钮应该变为不同的颜色

### 使用usePathname()检测当前路径

可以使用usePathname获取当前页面的路径,并于<Link>的href进行对比。

```tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import styles from "./Navbar.module.css"; // 引入 CSS 模块

export default function Navbar() {
  const pathname = usePathname(); // 获取当前 URL 路径

  return (
    <nav>
      <Link href="/" className={pathname === "/" ? styles.active : ""}>Home</Link>
      <Link href="/about" className={pathname === "/about" ? styles.active : ""}>About</Link>
      <Link href="/dashboard" className={pathname === "/dashboard" ? styles.active : ""}>Dashboard</Link>
    </nav>
  );
}
```

Navbar.module.css

```css
.active {
  font-weight: bold;
  color: red;
  border-bottom: 2px solid red;
}
```

### 使用与动态路由的startsWith方法

如果页面是动态路由，比如/dashboard/setting,/dashboard/profile，可以使用startWith()来匹配

示例代码：高亮/dashboard/所有子页面

```tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import styles from "./Navbar.module.css";

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav>
      <Link href="/" className={pathname === "/" ? styles.active : ""}>Home</Link>
      <Link href="/about" className={pathname === "/about" ? styles.active : ""}>About</Link>
      <Link href="/dashboard" className={pathname.startsWith("/dashboard") ? styles.active : ""}>Dashboard</Link>
    </nav>
  );
}
```

### 使用Tailwind Css（无需css模块）

如果使用tailwind css 可以用classname动态切换样式：

```tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx"; // 需要安装 `classnames` 或 `clsx`

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="flex gap-4 p-4 bg-gray-100">
      <Link
        href="/"
        className={clsx("px-3 py-2", pathname === "/" && "text-red-500 border-b-2 border-red-500")}
      >
        Home
      </Link>
      <Link
        href="/about"
        className={clsx("px-3 py-2", pathname === "/about" && "text-red-500 border-b-2 border-red-500")}
      >
        About
      </Link>
      <Link
        href="/dashboard"
        className={clsx("px-3 py-2", pathname.startsWith("/dashboard") && "text-red-500 border-b-2 border-red-500")}
      >
        Dashboard
      </Link>
    </nav>
  );
}
//无需单独的CSS文件，Tailwind直接高亮当前页面的<Link>
```

## Navigating Programmatically(程序化导航)

在NextJS中，除了使用<link>进行导航，还可以使用JavaScript代码进行程序化导航

### 使用useRouter().push()导航

在Nextjs中，可以使用useRouter()手动跳转到某个页面

示例：按钮点击后跳转

```tsx
"use client";

import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter(); // 获取 Router 实例

  return (
    <div>
      <h1>🏠 Home Page</h1>
      <button onClick={() => router.push("/about")}>前往 About</button>
    </div>
  );
}
//点击按钮后，页面会跳转到/about，但不会刷新整个页面
```

### 使用router.replace()不保留历史记录

```tsx
"use client";

import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  function handleLogin() {
    // 假设登录成功
    router.replace("/dashboard"); // 不保留当前页面
  }

  return <button onClick={handleLogin}>登录</button>;
}
```

### 使用router.back()返回上一个页面

```tsx
"use client";

import { useRouter } from "next/navigation";

export default function ProfilePage() {
  const router = useRouter();

  return (
    <div>
      <h1>👤 个人主页</h1>
      <button onClick={() => router.back()}>🔙 返回</button>
    </div>
  );
}
```

### 在表单提交后自动跳转

```tsx
"use client";

import { useRouter } from "next/navigation";

export default function ContactForm() {
  const router = useRouter();

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    // 假设表单提交成功
    router.push("/success");
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="你的名字" required />
      <button type="submit">提交</button>
    </form>
  );
}
```

### 传递参数（带Query Params）

如果需要在跳转时传递参数，可以使用router.push(url)传递query参数

```tsx
"use client";

import { useRouter } from "next/navigation";

export default function SearchPage() {
  const router = useRouter();

  function handleSearch() {
    const query = "nextjs";
    router.push(`/search?query=${query}`);
  }

  return <button onClick={handleSearch}>搜索 Next.js</button>;
}
```

### 解析Url参数

动态路由(/profile/[id])，可以使用useParams()解析参数

```tsx
"use client";

import { useParams } from "next/navigation";

export default function ProfilePage() {
  const params = useParams();

  return <h1>用户 ID: {params.id}</h1>;
}
```

## Use Client(客户端渲染)和Server-Side

### 使用use client(客户端渲染)的情景：

适用于：

- 需要交互（事件处理）的组件（如按钮，输入框，表单）

- 需要useState,useEffect,useContext等React Hooks的组件

- 无法在服务器端运行的代码（如window,document,localStorage)

- 依赖客户端状态的组件（如用户身份，购物车）

### 使用Server-side(服务器端)的情景：

- 页面数据SEO重要

- 需要数据库查询，API请求，并希望在服务器端完成（提升性能）

- 不需要交互的静态页面（如about.tsx)

- SSR（服务器端渲染）或SSG(静态生成)。

| **特性**        | **`use client`（客户端渲染）** | **服务器端渲染（默认）**         |
| ------------- | ----------------------- | ---------------------- |
| **是否 SEO 友好** | ❌ **不利于 SEO**           | ✅ **SEO 友好**           |
| **数据获取方式**    | `useEffect` + `fetch`   | `fetch` 直接在 `page.tsx` |
| **是否影响页面速度**  | **首屏加载慢**               | **首屏加载快**              |
| **适用于**       | 交互组件（表单、按钮、状态管理）        | 数据驱动的页面（博客、商品详情）       |

## Templates(模板)

Template.tsx允许创建类似layout.tsx但可动态更新的UI结构，它在每次路由更改时都会重新渲染，而layout.tsx只会渲染一次并保持不变

### Template vs layout

| **特性**      | **`layout.tsx`（布局）** | **`template.tsx`（模板）** |
| ----------- | -------------------- | ---------------------- |
| **是否缓存 UI** | ✅ **是（不会重新渲染）**      | ❌ **不是（会重新渲染）**        |
| **适用于**     | 全局 **导航栏、侧边栏**       | 需要**动态变化**的 UI         |
| **何时重新渲染？** | 只渲染一次，除非页面刷新         | **每次路由变化都会重新渲染**       |
| **适用场景**    | 共享 UI，状态保持           | **需要动态 UI 更新**         |

### 基本用法

代码示例(app/dashboard/template.tsx)

```tsx
export default function DashboardTemplate({ children }: { children: React.ReactNode }) {
  console.log("🔄 Template 重新渲染");

  return (
    <div>
      <h1>📊 Dashboard Template</h1>
      {children}
    </div>
  );
}
```

代码示例(app/dashboard/page.tsx)

```tsx
export default function DashboardPage() {
  return <h2>欢迎来到 Dashboard!</h2>;
}
```

每此进入/dashboard或/dashboard/settings，模板都会重新渲染，打印出“Template 重新渲染”。

## Error Handling(错误处理)

错误处理可以通过error.tsx文件来管理页面错误，让应用在发生错误时提供更好的用户体验。

### 创建error.tsx处理错误

```tsx
"use client";

export default function GlobalError({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <h1>🚨 发生错误！</h1>
      <p>{error.message}</p>
      <button onClick={() => reset()}>重试</button>
    </div>
  );
}
```

### 作用域错误处理

可以在特定路由下创建error.tsx，只捕获该目录的错误而不影响其他页面。

### 在组件中手动抛出错误

```tsx
export default function BrokenComponent() {
  throw new Error("❌ 这里出错了！");
}
```

### 捕获API请求错误

```tsx
export default async function Page() {
  try {
    const res = await fetch("https://api.example.com/data");
    if (!res.ok) throw new Error("无法获取数据");

    const data = await res.json();
    return <div>{data.message}</div>;
  } catch (error) {
    throw new Error("🚨 数据加载失败，请稍后重试！");
  }
}
```

## Parallel Routes(并行路由)

并行路由允许在同一个页面中同时渲染多个独立的路由

这对于仪表盘，多窗口应用，聊天界面等需要同时展示多个区域内容的页面非常有用

### 并行路由的基本概念

在nextjs的目录下，可以创建命名插槽（Named Slots）来定义并行的UI区块。

并行渲染feed和notifications的文件结构

```tsx
app/
  layout.tsx         # 根布局
  dashboard/
    layout.tsx       # Dashboard 页面布局
    page.tsx         # 默认内容
    @feed/           # 并行路由：Feed 区域
      default.tsx    # 默认 Feed 内容
    @notifications/  # 并行路由：通知区域
      default.tsx    # 默认通知内容
```

其中的@feed和@notification时命名插槽，他们是“default.tsx”是默认渲染的内容。

### 创建layout.tsx处理并行路由

```tsx
export default function DashboardLayout({
  children, // 默认内容
  feed, // Feed 插槽
  notifications, // Notifications 插槽
}: {
  children: React.ReactNode;
  feed: React.ReactNode;
  notifications: React.ReactNode;
}) {
  return (
    <div style={{ display: "flex" }}>
      <aside style={{ width: "20%", borderRight: "1px solid gray" }}>
        {feed} {/* 这里渲染 Feed */}
      </aside>
      <main style={{ flex: 1 }}>{children}</main> {/* Dashboard 主内容 */}
      <aside style={{ width: "20%", borderLeft: "1px solid gray" }}>
        {notifications} {/* 这里渲染 Notifications */}
      </aside>
    </div>
  );
}
```

### 在URL中切换并行路由内容

除了default.tsx作为默认内容，还可以创建不同的页面，并使用URL切换他们的内容

文件结构

```tsx
app/
  dashboard/
    @feed/
      page.tsx       # 默认 Feed
      trending.tsx   # /dashboard/feed/trending
    @notifications/
      page.tsx       # 默认通知
      messages.tsx   # /dashboard/notifications/messages
```

### 在Link中导航不同的并行路由

```tsx
import Link from "next/link";

export default function DashboardPage() {
  return (
    <div>
      <h1>📊 Dashboard</h1>
      <nav>
        <Link href="/dashboard/feed/trending">🔥 查看热门动态</Link>
        <br />
        <Link href="/dashboard/notifications/messages">📩 查看私信</Link>
      </nav>
    </div>
  );
}
```

## Conditional Routes

条件路由(Conditional Routes) 允许基于某些条件(如用户权限，角色，登录状态)动态决定页面内容或重定向到不同的路由。

### 适用redirect（）进行条件跳转

```tsx
import { redirect } from "next/navigation";

export default function DashboardPage() {
  const isAuthenticated = false; // 假设用户未登录

  if (!isAuthenticated) {
    redirect("/login"); // 🚀 未登录时跳转到 /login
  }

  return <h1>📊 Dashboard 页面</h1>;
}
```

### 在minddleware.ts中进行全局路由保护

如果希望在多个页面适用相同的逻辑（比如所有的/dashboard/路由都需要登录）可以适用middleware处理。

示例代码：middleware.ts

```tsx
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const isAuthenticated = false; // 这里可以接入真实的身份验证逻辑

  if (!isAuthenticated && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}
```

### 在客户端使用useRouter().push()

在客户端基于某个条件进行跳转，可以使用useRouter().push()

```tsx
"use client";

import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  function handleLogin() {
    // 这里模拟一个登录成功
    const isLoggedIn = true;

    if (isLoggedIn) {
      router.push("/dashboard"); // 🚀 登录成功后跳转到 /dashboard
    }
  }

  return <button onClick={handleLogin}>登录</button>;
}
```

### 条件渲染不同组件

在同一个页面内，根据条件渲染不用的内容，可以用if或三元运算符

```tsx
export default function Home() {
  const isAuthenticated = false;

  return (
    <div>
      {isAuthenticated ? (
        <h1>🎉 欢迎回来！</h1>
      ) : (
        <h1>🚪 请先登录！</h1>
      )}
    </div>
  );
}
```

### Layout里做条件导航

如果希望整个路由组都使用相同的权限逻辑，可以在layout.tsx里进行条件判断

```tsx
import { redirect } from "next/navigation";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const isAuthenticated = false;

  if (!isAuthenticated) {
    redirect("/login");
  }

  return (
    <div>
      <h1>📊 Dashboard Layout</h1>
      {children}
    </div>
  );
}
```

## Intercepting Routes(拦截路由)

Intercepting Routes允许在保持当前页面的同时，在模态框(Modal)或侧边栏等地方加载新页面，而不会完全切换到新页面。

### 常用场景

- 模态框(Modal)：点击某个项目，打开/item/1，但/items依然可见

- 侧边栏(Sidebar):在/dashboard里打开/dashboard/settings，但dashboard依然可见

### 创建拦截路由

关键是使用(..)语法，(..)/path表示拦截路由器，不会直接跳转，而是以模态框，弹窗等方式加载。

其中@slot/目录可用于并行加载新内容

(.)是匹配同一层级的

(..)是匹配上一层级的

(..)(..)是匹配两个层级以上的

(...)是匹配app根目录下的



## Parallel Intercepting Routes(并行拦截路由)

Parallel Intercepting Routes允许在同一个页面内拦截多个子路由，并将它们渲染到不同的slot中。

### 创建并行拦截路由

```tsx
app/
  dashboard/
    layout.tsx       # Dashboard 页面布局
    page.tsx         # /dashboard 主内容
    @sidebar/        # 并行路由 - 侧边栏
      default.tsx    # 默认的侧边栏内容
      profile.tsx    # /dashboard/sidebar/profile（拦截模式）
    @modal/          # 并行路由 - 模态框
      [id]/page.tsx  # /dashboard/modal/[id]（拦截模式）
    items/
      [id]/page.tsx  # 真实的 /dashboard/items/[id] 页面
```

### layout.tsx处理并行拦截路由

```tsx
export default function DashboardLayout({
  children,
  sidebar, // 侧边栏
  modal,   // 模态框
}: {
  children: React.ReactNode;
  sidebar: React.ReactNode;
  modal: React.ReactNode;
}) {
  return (
    <div style={{ display: "flex" }}>
      <aside style={{ width: "250px", borderRight: "1px solid gray" }}>
        {sidebar} {/* 渲染并行的侧边栏 */}
      </aside>
      <main style={{ flex: 1, padding: "20px" }}>
        {children} {/* 渲染主页面内容 */}
      </main>
      {modal} {/* 渲染并行的模态框 */}
    </div>
  );
}
```

### 侧边栏内容

```tsx
export default function DefaultSidebar() {
  return <div>📂 侧边栏（默认）</div>;
}

export default function ProfileSidebar() {
  return <div>👤 用户 Profile 详情</div>;
}

```

### 并行拦截item/[id]作为模态框

代码文件：app/dashboard/@modal/[id]/page.tsx

```tsx
"use client";

import { useRouter } from "next/navigation";

export default function ItemModal({ params }: { params: { id: string } }) {
  const router = useRouter();

  return (
    <div
      style={{
        position: "fixed",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        background: "white",
        padding: "20px",
        boxShadow: "0px 0px 10px rgba(0,0,0,0.1)",
      }}
    >
      <h2>🔍 详情（拦截模式）</h2>
      <p>当前 ID：{params.id}</p>
      <button onClick={() => router.back()}>关闭</button>
    </div>
  );
}
```

### 真实的/dashboard/item/[id]页面

代码页面:app/dashboard/items/[id]/page.tsx(如果dashboard/items/1直接访问，他会作为完整页面加载，而不是模态框)

```tsx
export default function ItemPage({ params }: { params: { id: string } }) {
  return (
    <div>
      <h1>📄 真实页面</h1>
      <p>当前 ID：{params.id}</p>
    </div>
  );
}
```

### 在dashboard/page.tsx里链接到拦截页面

代码文件:app/dashboard/page.tsx

```tsx
import Link from "next/link";

export default function DashboardPage() {
  return (
    <div>
      <h1>📊 Dashboard 主页面</h1>
      <p>点击查看详情：</p>
      <Link href="/dashboard/sidebar/profile">👤 个人信息</Link>
      <br />
      <Link href="/dashboard/items/1">📄 访问 /dashboard/items/1</Link>
      <br />
      <Link href="(..)/dashboard/items/1">🔍 以模态框打开 /dashboard/items/1</Link>
    </div>
  );
}
//点击/dashboard/sidebar/profile，侧边栏内容更新
//点击/dashboard/items/1, 完整页面跳转
//点击(..)/dashboard/items/1，以模态框打开
```

## Route Handles(路由处理器)

在Route Handles允许你在app/api目录下定义后端API路由，用户处理GET，POST，PUT，DELETE请求。

### 创建API路由

在app/api目录下，每个route.ts文件都是一个API端点

文件结构

```tsx
app/
  api/
    hello/
      route.ts  # /api/hello
    users/
      route.ts  # /api/users
```

### 处理GET请求

代码文件：app/api/hello/route.ts

```tsx
export async function GET() {
  return Response.json({ message: "Hello, Next.js API!" });
}
```

### 处理POST请求

```tsx
export async function POST(req: Request) {
  const body = await req.json();
  return Response.json({ message: `用户 ${body.name} 已创建！` });
}
```

### 处理PUT和DELETE

```tsx
export async function PUT(req: Request) {
  const body = await req.json();
  return Response.json({ message: `用户 ${body.id} 信息已更新！` });
}

export async function DELETE(req: Request) {
  return Response.json({ message: "用户已删除！" });
}
```

### 处理GET动态参数

```tsx
export async function GET(req: Request, { params }: { params: { id: string } }) {
  return Response.json({ message: `用户 ID: ${params.id}` });
}
```

### 处理PATCH请求

代码文件：app/api/users/[id]/route.ts

客户端发送PATCH请求到/api/users/123。

```tsx
export async function PATCH(req: Request, { params }: { params: { id: string } }) {
  const body = await req.json(); // 获取请求体
  return Response.json({
    message: `用户 ${params.id} 更新成功！`,
    updatedFields: body
  });
}
```

或者在前端发送PATCH请求

在React组件中使用fetch()

```tsx
async function updateUser() {
  const res = await fetch("/api/users/123", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: "newemail@example.com" })
  });

  const data = await res.json();
  console.log(data);
}
```

### 结合数据库(示例：MongoDB/Prisma)

```tsx
import { prisma } from "@/lib/prisma"; // 假设使用 Prisma

export async function GET() {
  const users = await prisma.user.findMany();
  return Response.json(users);
}
```

### URL Query Parameters(URL查询参数)

在NextJS中，可以使用route Handlers 处理RUL查询参数

#### 读取URL查询参数

在Nextjs.API路由中，可以使用**req.nextUrl.searchParams**读取查询参数

文件结构：

```tsx
app/
  api/
    users/
      route.ts  # 处理 /api/users?role=admin
```

代码文件: app/api/users/route.ts

```tsx
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const role = searchParams.get("role"); // 获取 ?role=xxx 参数

  return Response.json({
    message: `查询的角色: ${role ?? "未指定"}`,
  });
}
```

#### 读取多个查询参数

如果url中有多个参数(如api/products?category=electronics&price=100),可以使用searchParams.get()或searchParams.getAll()读取。

```tsx
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);

  const category = searchParams.get("category"); // 获取类别
  const price = searchParams.get("price"); // 获取价格

  return Response.json({
    category: category ?? "所有类别",
    price: price ? Number(price) : "不限价格",
  });
}
```

#### 处理数组查询参数

如果url中有多个相同的参数(如 `/api/tags?tag=nextjs&tag=react`)，可以使用searchParams.getAll("tag")读取。

```tsx
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const tags = searchParams.getAll("tag"); // 读取所有 tag 参数

  return Response.json({
    tags: tags.length > 0 ? tags : "未提供标签",
  });
}
```

#### 结合POST请求处理查询参数

如果在POST请求中需要同时处理 查询参数+请求体

```tsx
export async function POST(req: Request) {
  const { searchParams } = new URL(req.url);
  const status = searchParams.get("status"); // 获取 ?status=xxx

  const body = await req.json(); // 获取 POST 请求体
  return Response.json({
    status: status ?? "默认状态",
    order: body,
  });
}
```

#### 在前端读取查询参数

在客户端组件(use client)中，可以使用useSearchParams()读取查询参数

```tsx
"use client";

import { useSearchParams } from "next/navigation";

export default function ProductPage() {
  const searchParams = useSearchParams();
  const category = searchParams.get("category") ?? "所有类别";
  const price = searchParams.get("price") ?? "不限价格";

  return (
    <div>
      <h1>商品类别: {category}</h1>
      <h2>价格: {price}</h2>
    </div>
  );
}
```

## Redirects in Route Handlers

### 使用redirect()进行服务器端重定向

示例使用redirect("/new-url"),在app/api/redirect/route.ts里重新执行重定向

```tsx
import { redirect } from "next/navigation";

export async function GET() {
  redirect("/new-url"); // 🚀 直接跳转到新页面
}
```

### 使用NextResponse.redirect()进行API端点重定向

如果想要返回一个302或307状态码的HTTP重定向，可以使用NextResponse.redirect()

```tsx
import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.redirect("https://example.com", 307);
}
```

### 在客户端useRouter().push()进行前端重定向

在客户端(Client Component)进行重定向，使用useRouter().push()

```tsx
"use client";

import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  function handleRedirect() {
    router.push("/new-url"); // 🚀 跳转到新页面
  }

  return <button onClick={handleRedirect}>跳转</button>;
}
//点击按钮后，页面会跳转到/new-url，但不会刷新整个页面
```

## Headers in Route Handlers

可以在app/api目录下的Route Handlers (API端点)中处理HTTP Headers,包括：

- 读取请求头(Request Headers)

- 设置响应头（Response Headers）

- 自定义CORS头

### 读取请求头(Request Headers)

```tsx
export async function GET(req: Request) {
  const userAgent = req.headers.get("user-agent");

  return Response.json({
    message: "请求头信息",
    userAgent: userAgent ?? "未知",
  });
}
```

### 设置响应头（Response Headers)

可以使用Response.headers.append()或new Response()自定义API返回的Headers。

示例：在API响应中设置Cache-Control和X-Custom-Header

```tsx
export async function GET() {
  const response = new Response(JSON.stringify({ message: "Hello, Next.js!" }), {
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "s-maxage=60, stale-while-revalidate", // 设置缓存 60 秒
      "X-Custom-Header": "HelloWorld", // 自定义 Header
    },
  });

  return response;
}
```

### 处理 `Authorization` 头（JWT / Token 验证）

```tsx
export async function GET(req: Request) {
  const authHeader = req.headers.get("authorization");

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return new Response(JSON.stringify({ error: "未授权" }), { status: 401 });
  }

  const token = authHeader.split(" ")[1]; // 提取 Token
  return Response.json({ message: "成功访问", token });
}
```

### 解析Content-Type(处理JSON/FromData)

如果API需要处理不同的Content-Type,可以读取headers.get("content-type")。

```tsx
export async function POST(req: Request) {
  const contentType = req.headers.get("content-type");

  if (contentType?.includes("application/json")) {
    const jsonBody = await req.json();
    return Response.json({ message: "收到 JSON 数据", data: jsonBody });
  } else if (contentType?.includes("multipart/form-data")) {
    const formData = await req.formData();
    return Response.json({ message: "收到 FormData 数据", data: Object.fromEntries(formData) });
  } else {
    return new Response("不支持的格式", { status: 415 });
  }
}
```

## Cookies in Route Handlers

### 读取Cookies

```tsx
import { cookies } from "next/headers";

export async function GET() {
  const userCookie = cookies().get("user");

  return Response.json({
    message: "读取 Cookies",
    user: userCookie ? userCookie.value : "未找到",
  });
}
```

### 设置Cookies

```tsx
import { cookies } from "next/headers";

export async function GET() {
  cookies().set("user", "Alice", { path: "/", maxAge: 60 * 60 * 24 });

  return Response.json({ message: "用户 Cookie 已设置！" });
}
```

### 读取所有Cookies

```tsx
import { cookies } from "next/headers";

export async function GET() {
  const allCookies = cookies().getAll();
  return Response.json({ cookies: allCookies });
}
```

### 删除Cookies

```tsx
import { cookies } from "next/headers";

export async function GET() {
  cookies().delete("user");

  return Response.json({ message: "用户 Cookie 已删除！" });
}
```

### 设置安全Cookies(HttpOnly&Secure)

```tsx
export async function GET() {
  cookies().set("session", "abc123", {
    httpOnly: true, // 🚀 只能通过服务器访问，不能用 `document.cookie`
    secure: true,   // 🚀 仅在 HTTPS 连接下发送
    sameSite: "strict", // 🚀 防止跨站请求伪造（CSRF）
    path: "/",
    maxAge: 60 * 60 * 24, // 24 小时
  });

  return Response.json({ message: "安全 Cookie 已设置！" });
}
```

### 在前端操作Cookies

如果需要在客户端获取或设置Cookies，可以使用document.cookie或js-cookie

```tsx
"use client";

import Cookies from "js-cookie";

export default function ClientComponent() {
  function handleSetCookie() {
    Cookies.set("theme", "dark", { expires: 7 });
  }

  function handleGetCookie() {
    alert(Cookies.get("theme"));
  }

  return (
    <div>
      <button onClick={handleSetCookie}>设置 Cookie</button>
      <button onClick={handleGetCookie}>获取 Cookie</button>
    </div>
  );
}
```

## Caching in Route Handlers(路由处理器中的缓存)

### 默认缓存(Get请求自动缓存)

```tsx
export async function GET() {
  return Response.json({ message: "Hello, Next.js API!" });
}
```

### 禁用缓存(no-store)

api每次都重新获取最新数据(如实时数据请求)，可以使用Cache-Control:no-store

```tsx
export async function GET() {
  return new Response(JSON.stringify({ timestamp: Date.now() }), {
    headers: { "Cache-Control": "no-store" }, // ❌ 不缓存，每次重新请求
  });
}
```

### 使用s-maxage进行增量静态再生(ISR缓存)

如果希望API定期刷新缓存(ISR - Incremental Static Regeneration)

```tsx
export async function GET() {
  return new Response(JSON.stringify({ message: "Cached Response" }), {
    headers: { "Cache-Control": "s-maxage=60, stale-while-revalidate" }, // ⏳ 缓存 60 秒
  });
}
```

### 使用cache()手动缓存数据

```tsx
import { cache } from "react";

const getCachedData = cache(async () => {
  console.log("Fetching Data...");
  return { message: "This is cached data" };
});

export async function GET() {
  const data = await getCachedData();
  return Response.json(data);
}
```

### 结合fetch()缓存外部API

Next.js内置的fetch默认会缓存GET请求，你可以控制fetch()的缓存策略：

默认缓存

```tsx
export async function GET() {
  const res = await fetch("https://jsonplaceholder.typicode.com/posts/1"); // 默认缓存
  const data = await res.json();

  return Response.json(data);
}
```

禁用缓存

```tsx
export async function GET() {
  const res = await fetch("https://jsonplaceholder.typicode.com/posts/1", {
    cache: "no-store", // ❌ 禁用缓存，每次都重新请求
  });
  const data = await res.json();

  return Response.json(data);
}
```

### 结合revalidateTag()进行手动缓存刷新

如果需要在某些操作后手动刷新缓存，可以使用revalidateTag()

示例：缓存/api/products，但可以在POST请求时刷新

```tsx
import { revalidateTag } from "next/cache";

export async function GET() {
  return Response.json(
    { message: "Product list" },
    { headers: { "Cache-Control": "s-maxage=60", "X-Next-Cache-Tag": "products" } }
  );
}

export async function POST() {
  revalidateTag("products"); // 🚀 清除缓存，让 `GET` 重新请求数据
  return Response.json({ message: "Product list updated!" });
}
```

## Client-Side Rendering(客户端渲染)

指的是网页的内容主要由浏览器在用户端动态渲染，而不是服务器端直接返回完整的html页面。

依赖于JavaScript，主要适用于**单页面**应用。

优缺点：

优点：更好的用户体验，页面切换更流程，无需频繁的请求服务器。(适用于交互性强的应用，比如管理后台，在线编辑等)

缺点：搜索引擎优化不友好，搜索引擎可能无法正确解析JS动态生成的内容；

首次加载的速度慢，不适合低端设备。

## Server-Side Rendering

服务器在接受到用户的请求后，在服务端执行JavaScript并生成完整的html页面，然后返回给浏览器。

优缺点：
优点：SEO（搜索引擎优化）友好，首屏加载更快，适合动态内容。

缺点：服务器压力大，页面交互依赖额外的JavaScripts

## Suspense for SSR

Streaming Rendering(流式渲染)：服务器端可以先发送静态html，然后异步加载Suspense组件，等数据准备好后再渲染剩余部分。

部分Hydration(部分水合)：允许服务器先渲染一部分UI，等客户端JavaScript加载后，逐步让组件可交互。

## React Server Components(RSC)

它允许部分React组件在服务端执行，然后把结果发送到客户端进行渲染，减少JavaScript负担，提高页面性能。

在传统的React应用中，所有组件都会被打包到JavaScript文件并下载到客户端，然后浏览器执行他们。（这样会导致JS体积过大，加载慢，渲染性能下降），但在RSC中，组件可以在服务器端渲染，客户端只接受最终html和数据，不需要下载组件的JavaScript代码。

## Static Rendering(静态渲染)

它是Next.js提供的一种预渲染方式，他会在构建时生成html页面，并在请求时直接返回静态html，提高加载速度和SEO友好性。

## Dynamic Rendering(动态渲染)

它是在Next.js中指的是页面在请求时动态生成html，适用于需要个性化，实时更新或者数据库查询的页面。

两种方式：

Server-Side Rendering(SSR):每次请求生成新的html，适用于实时数据。

On-Demand ISR(增量静态再生) 静态页面按需更新，适用于部分动态数据。

## Streaming（流式渲染）

它是Next.js的核心功能，允许服务器逐步发送html到了客户端，而不是等所有数据准备好再一次性返回整个页面。这样可以大幅度提高首屏的加载速度，尤其实在需要慢速API请求，数据库查询的页面。

## Interleaving Server and Client Components(交错使用服务器和客户端组件)

Server Components里可以嵌套Client Components

Client Components里面也可以import其他的Client Compinents

但Client Components里面不能import Server Components

## Data Cache(数据缓存)

一般来说如果使用fetch从api获取数据，NextJs会缓存这个fetch请求（这样多个用户访问时就不会重复请求api）。但有一个问题---如果api数据更新了，页面不会自动刷新(除非你强制让他重新验证数据)

增量再生（ISR) :使用next:{revalidate:秒数}数据每个X秒更新一次

## Request Memoization(请求记忆化)

允许NextJs避免重复API请求或数据库查询，从而提高性能，减少服务器负担，确保数据只被请求一次。

简单来说就是：如果多个组件或请求使用相同的数据，Memorization让它们共用一个请求结果，而不是多次请求api。
