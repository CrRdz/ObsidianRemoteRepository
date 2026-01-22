* **JavaWeb 技术栈**
* **B/S 架构**：Browser/Server（浏览器/服务器）架构模式。
    * **特点**：客户端只需要浏览器，应用程序的逻辑和数据都存储在服务器端。浏览器只需要请求服务器，获取 Web 资源，服务器把 Web 资源发送给浏览器即可。
    * **好处**：易于维护升级。服务端升级后，客户端无需任何部署就可以使用到新的版本。

**核心组件：**
* **静态资源**：HTML，CSS，JavaScript，图片等。负责页面展现。
* **动态资源**：[[Servlet]]，[[JSP]] 等。负责逻辑处理。
* **数据库**：负责存储管理。
* **HTTP 协议**：定义通信规则。
* **Web 服务器（[[Tomcat]]）**：负责解析 [[HTTP]] 协议，解析请求数据，并发送响应数据。

```text

Web Core/

├─ Web 服务器-Tomcat

├─ Frontend/

│ ├─ AJAX

│ ├─ CSS

│ ├─ Element UI

│ ├─ HTML

│ ├─ JavaScript

│ ├─ JSP

│ └─ VUE

├─ 会话跟踪技术

├─ HTTP

├─ Servlet

├─ Request & Response

└─ Filter & Listener

```



