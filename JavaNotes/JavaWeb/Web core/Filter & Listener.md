# 1. 概念

- **Filter**：表示过滤器，是 JavaWeb 三大组件（Servlet，Filter，Listener）之一。
    
- 过滤器可以把资源的请求 **拦截** 下来，从而实现一些特殊的功能。
    
- 过滤器一般完成一些 **通用** 的操作，比如权限控制、统一编码处理、敏感字符处理等等。
    

---

# 2. Filter (过滤器)

## 2.1 Filter 快速入门

（开发步骤类似 Servlet）

1. 定义类，实现 `Filter` 接口，并重写其所有方法。
    
2. 配置 Filter 拦截资源的路径：在类上定义 `@WebFilter` 注解。
    
3. 在 `doFilter` 方法中输出一句话，并放行。
    
```Java
@WebFilter("/*")
public class FilterDemo implements Filter {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        // 1. 放行前，对 request 数据进行处理
        System.out.println("1. FilterDemo...");

        // 放行
        chain.doFilter(request, response);

        // 2. 放行后，对 Response 数据进行处理
        System.out.println("5. FilterDemo...");
    }

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {}

    @Override
    public void destroy() {}
}
```

## 2.2 Filter 执行流程

1. **Filter**：执行放行前逻辑 -> 放行 -> 访问资源 -> 执行放行后逻辑。
    
2. 放行后访问对应资源，资源访问完成后还会 **回到 Filter 中**。
    
3. 回到 Filter 会执行 **放行后逻辑**，而不是从头执行。
    

## 2.3 Filter 使用细节

### 1. Filter 拦截路径配置

配置示例：

```Java

@WebFilter("/*")
public class FilterDemo
```

- **拦截具体资源**：`/index.jsp` —— 只有访问 `index.jsp` 时才会被拦截。
    
- **目录拦截**：`/user/*` —— 访问 `/user` 下的所有资源，都会被拦截。
    
- **后缀名拦截**：`*.jsp` —— 访问后缀名为 `jsp` 的资源，都会被拦截。
    
- **拦截所有**：`/*` —— 访问所有资源，都会被拦截。
    

### 2. 过滤器链

- **概念**：一个 Web 应用可以配置多个过滤器，这多个过滤器称为过滤器链。
    
- **执行流程**：
    
    > 请求 -> Filter1 放行前逻辑 -> Filter1 放行 -> Filter2 放行前逻辑 -> Filter2 放行 -> **资源** -> Filter2 放行后逻辑 -> Filter1 放行后逻辑 -> 响应
    
- **优先级**：注解配置的 Filter，优先级按照过滤器 **类名（字符串）的自然排序** 决定。
    

## 2.4 案例：登录验证

**需求**：访问服务器资源时，需要先进行登录验证，如果没有登录，则自动跳转到登录页面。

### 基础实现

新建 `LoginFilter` 实现登录验证的过滤：

```Java
/**
 * 登录验证过滤器
 */
@WebFilter("/*")
public class LoginFilter implements Filter {
    @Override
    public void init(FilterConfig filterConfig) throws ServletException {}

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        HttpServletRequest req = (HttpServletRequest) request;

        // 判断 session 中是否有 user
        HttpSession session = req.getSession();
        Object user = session.getAttribute("user");

        if(user != null){
            // 登录过了
            // 放行
            chain.doFilter(request, response);
        } else {
            // 未登录
            req.setAttribute("login_msg", "您尚未登录");
            req.getRequestDispatcher("/login.jsp").forward(req, response);
        }
        
        // 注意：此处原文代码逻辑有冗余放行风险，实际开发中 forward 后通常 return，但此处保留原文逻辑结构
        // chain.doFilter(request,response); 
    }

    @Override
    public void destroy() {}
}
```

### 问题与解决

- 问题：
    
    如果配置 @WebFilter("/*")，会导致与登录和注册相关的资源（如 css、img、注册页面）同样被拦截。但需求是 只对没有登录的进行拦截，且不应该拦截登录页面本身。
    
- 解决：
    
    在过滤器中添加一个判断：判断访问的是不是登录相关资源。
    
    - **是**：放行。
        
    - **不是**：进行登录验证。
        

### 优化后的逻辑 (LoginFilter.java)

```Java
public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
    HttpServletRequest req = (HttpServletRequest) request;

    // 判断访问资源路径是否和注册登录相关
    String[] urls = {"/login.jsp", "/loginServlet", "/imgs/", "/css/", "/checkCodeServlet/", "/register.jsp", "/registerServlet"};
    
    // 获取当前访问的资源路径
    String url = req.getRequestURL().toString();
    
    for (String u : urls) {
        if(url.contains(u)){
            // 访问的是注册登录相关的资源，放行
            chain.doFilter(request, response);
            return;
        }
    }
    
    // ... 下接登录验证逻辑 ...
}
```

---

# 3. Listener (监听器)

## 3.1 概念

- **Listener**：监听器，是 JavaWeb 三大组件（Servlet，Filter，Listener）之一。
    
- 监听器可以监听 `application`、`session`、`request` 三个对象的创建、销毁，或者往其中添加、修改、删除属性时自动执行代码的功能组件。
    

## 3.2 Listener 分类

JavaWeb 中提供了 8 个监听器，主要分为三类：

1. **ServletContext 监听**：
    
    - `ServletContextListener`：用于对 ServletContext 对象进行监听（创建、销毁）。
        
    - `ServletContextAttributeListener`：用于对 ServletContext 对象中属性的监听（增删改属性）。
        
2. **Session 监听**：
    
    - `HttpSessionListener`：对 Session 对象的整体状态的监听（创建、销毁）。
        
    - `HttpSessionAttributeListener`：对 Session 对象中的属性监听（增删改属性）。
        
    - `HttpSessionBindingListener`：监听对象与 Session 的绑定和解除。
        
3. **Request 监听**：
    
    - `ServletRequestListener`：对 Request 对象进行监听（创建、销毁）。
        
    - `ServletRequestAttributeListener`：对 Request 对象中的属性的监听（增删改属性）。
        

## 3.3 ServletContextListener 使用

1. 定义类，实现 `ServletContextListener` 接口。
    
2. 在类上添加 `@WebListener` 注解。
    
```Java
@WebListener
public class ContextLoaderListener implements ServletContextListener {

    /**
     * ServletContext 对象被创建，整个 web 应用发布成功
     * @param servletContextEvent
     */
    @Override
    public void contextInitialized(ServletContextEvent servletContextEvent) {
        // 加载资源等初始化操作
    }

    /**
     * ServletContext 对象被销毁，整个 web 应用卸载
     * @param servletContextEvent
     */
    @Override
    public void contextDestroyed(ServletContextEvent servletContextEvent) {
        // 释放资源等操作
    }
}
```
