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

### 结合API路由



## Intercepting Routes

(.)是匹配同一层级的

(..)是匹配上一层级的

(..)(..)是匹配两个层级以上的

(...)是匹配app根目录下的

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
