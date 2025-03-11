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
