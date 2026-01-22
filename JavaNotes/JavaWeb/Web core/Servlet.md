- Servlet 是 Java 提供的一门动态 Web 资源开发技术
    
- Servlet 是 JavaEE 规范之一，其实就是一个接口，将来需要定义 Servlet 接口，并由 Web 服务器运行 Servlet
---
# 1. 快速入门

1. **创建 Web 项目，导入 Servlet 依赖坐标**
    
    ```XML
    <dependencies>
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>3.1.0</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>
    ```
    
2. **创建：定义一个类，实现 Servlet 接口，并重写接口中所有方法，并在 service 方法中输入一句话**
    
    > **注**：重写接口中所有方法，在继承类后快捷键 `Alt+Enter`
    
    ```Java
    public class ServletDemo1 implements Servlet {
    
        @Override
        public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {
            System.out.println("servlet hello world");
        }
    
        @Override
        public String getServletInfo() {
            return "";
        }
    
        @Override
        public void destroy() {
        }
    
        @Override
        public void init(ServletConfig servletConfig) throws ServletException {
        }
    
        @Override
        public ServletConfig getServletConfig() {
            return null;
        }
    }
    ```
    
3. **配置：在类中使用 `@WebServlet` 注解，配置该 Servlet 的访问路径**
    
    ```Java
    @WebServlet("/demo1")
    ```
    
4. **访问：启动 Tomcat，浏览器输入 URL 访问该 Servlet**
    
    - `http://localhost:8080/web-demo/demo1`
        

# 2. Servlet 执行流程

流程示意：

访问到服务器 -> 访问到 Web 项目 -> 访问到对应的 Servlet

- Servlet 由 Web 服务器创建，Servlet 方法由 Web 服务器调用。
    
- 自定义的 Servlet，必须实现 Servlet 接口并复写其方法，而 Servlet 接口中包含 `service` 方法。
    

# 3. Servlet 生命周期

对象的生命周期指一个对象从被创建到被销毁的整个过程。

Servlet 运行在 Servlet 容器（Web 服务器）中，其生命周期由容器来管理，分为四个阶段：

1. **加载和实例化**：默认情况下，当 Servlet 第一次被访问时，由容器创建 Servlet 对象。
    
2. **初始化**：在 Servlet 实例化之后，容器将调用 Servlet 的 `init()` 方法初始化这个对象，完成一些如加载配置文件、创建链接等初始化工作。该方法**只调用一次**。
    
3. **请求处理**：每次请求 Servlet 时，Servlet 容器都会调用 Servlet 的 `service()` 方法对请求进行处理。
    
4. **服务终止**：当需要释放内存或容器关闭时，容器就会调用 Servlet 实例中的 `destroy()` 方法完成资源的释放。在 `destroy()` 方法调用之后，容器会释放这个 Servlet 实例，该实例随后会被 Java 的垃圾收集器所回收。
    

# 方法详细说明

- **Init**
    
    - **调用时机**：默认情况下，Servlet 被第一次访问时调用。
        
    - **调用次数**：1 次。
        
    - **loadOnStartup 配置**：
        
        - 负整数：第一次被访问时创建 Servlet 对象（默认）。
            
        - 0 或正整数：服务器启动时创建 Servlet 对象，数字越小优先级越高。
            
        - 示例：`@WebServlet(urlPatterns ="/demo1", loadOnStartup = 1)`
            
- **Service**
    
    - **调用时机**：每一次 Servlet 被访问时调用。
        
    - **调用次数**：多次。
        
- **Destroy**
    
    - **调用时机**：内存释放或服务器关闭时，Servlet 对象会被销毁，调用。
        
    - **调用次数**：1 次。
        

# Servlet 接口方法一览

- `void init(ServletConfig servletConfig)`
    
    - 初始化方法，在 Servlet 被创建时执行，只执行一次。
        
- `void service(ServletRequest servletRequest, ServletResponse servletResponse)`
    
    - 提供服务方法，每次 Servlet 被访问，都会调用该方法。
        
- `void destroy()`
    
    - 销毁方法：当 Servlet 被销毁时，调用该方法，在内存释放或服务器关闭时销毁 Servlet。
        
- `ServletConfig getServletConfig()`
    
    - 获取 ServletConfig 对象。
        
- `String getServletInfo()`
    
    - 获取 Servlet 信息。
        

# 4. Servlet 体系结构

# 继承关系

- **Servlet** (Servlet 体系根接口)
    
    - **GenericServlet** (Servlet 抽象实现类)
        
        - **HttpServlet** (对 HTTP 协议封装的 Servlet 实现类)
            

# 开发建议

开发 B/S 架构的 Web 项目，都是针对 HTTP 协议，所以自定义 Servlet 时会继承 **HttpServlet**。

# HttpServlet 原理

根据请求方式的不同，进行分别的处理，获取请求方式进行不同逻辑判断。

**原理代码解析：**

```Java
public class ServletDemo6 implements Servlet {
    @Override
    public void init(ServletConfig config) throws ServletException {
    }

    @Override
    public ServletConfig getServletConfig() {
        return null;
    }

    @Override
    public void service(ServletRequest req, ServletResponse res) throws ServletException, IOException {
        // 根据请求方式的不同，进行分别的处理
        HttpServletRequest request = (HttpServletRequest) req;

        // 1. 获取请求方式
        String method = request.getMethod();
        
        // 2. 判断
        if("GET".equals(method)){
            // get方式的处理逻辑
        } else if("POST".equals(method)){
            // post方式的处理逻辑
        }
    }

    @Override
    public String getServletInfo() {
        return null;
    }

    @Override
    public void destroy() {
    }
}
```

详细解析：

编写一个原始的实现 Servlet 类需要复写四种方法。因为 GET/POST 请求参数位置不同（POST 的请求参数在请求体中，而 GET 在请求行中），所以在 service 层中需要不同的处理逻辑。

这一部分的逻辑代码完全重复，可以写一个类，让所有 Servlet 都继承自这个类，复用代码。这个类就是 `HttpServlet`。它将 GET 的处理逻辑封装成方法 `doGet()`，将 POST 的处理逻辑封装成方法 `doPost()`。这样就不需要实现 Servlet 接口了，直接继承自 `HttpServlet`，复写 `doPost()` 和 `doGet()` 用来处理业务逻辑。即做到了 HTTP 协议的封装，并且完成了对不同请求方式的分发。

**HttpServlet 使用步骤**：继承 HttpServlet，重写 doGet、doPost 方法。

# 5. Servlet urlPattern 配置

Servlet 要想被访问，必须配置其访问路径（urlPattern）。

1. **一个 Servlet，可以配置多个 urlPattern**
    
    - 示例：`@WebServlet(urlPatterns = {"/demo1", "/demo2"})`
        
2. **urlPattern 配置规则**
    
    - **精确匹配**
        
        - 配置路径：`@WebServlet(urlPatterns = "/user/select")`
            
        - 访问路径：`localhost:8080/web-demo/user/select`
            
        - _注：范围小的优先级更高，如果一个目录同时满足精确匹配与目录匹配时，精确匹配优先。_
            
    - **目录匹配**
        
        - 配置路径：`@WebServlet(urlPatterns = "/user/*")`
            
        - 访问路径：
            
            - `localhost:8080/web-demo/user/aaa`
                
            - `localhost:8080/web-demo/user/bbb`
                
    - **扩展名匹配**
        
        - 配置路径：`@WebServlet(urlPatterns = "*.do")`
            
        - 访问路径：
            
            - `localhost:8080/web-demo/aaa.do`
                
            - `localhost:8080/web-demo/bbb.do`
                
        - _注：扩展名匹配不能以 `/` 开头。_
            
    - **任意匹配**
        
        - 配置路径：`@WebServlet("/")` 或 `@WebServlet("/*")`
            
        - 访问路径：
            
            - `localhost:8080/web-demo/haha`
                
            - `localhost:8080/web-demo/hehe`
                
        - _注：_
            
            - 当项目中的 Servlet 配置了 `/`，会覆盖掉 Tomcat 中的 DefaultServlet，当其他的 url-pattern 都匹配不上时都会走这个 Servlet。
                
            - 当项目中的 Servlet 配置了 `/*`，意味着匹配所有路径。
                
            - 尽量不用任意匹配。
                
3. **优先级**
    
    > *精确路径 > 目录路径 > 扩展名路径 > / > /**
    

# 6. XML 配置方法编写 Servlet（旧版本）

Servlet 从 3.0 开始支持使用注解配置，3.0 之前只支持 XML 配置文件的配置方式。

**步骤：**

1. 编写 Servlet 类
    
2. 在 `web.xml` 中配置该 Servlet
    

**web.xml 配置示例：**


```XML
<servlet>
    <servlet-name>demo13</servlet-name>
    <servlet-class>com.itheima.web.ServletDemo13</servlet-class>
</servlet>

<servlet-mapping>
    <servlet-name>demo13</servlet-name>
    <url-pattern>/demo13</url-pattern>
</servlet-mapping>
```