# 1. 概述

- **Request**：获取请求数据
    
- **Response**：设置响应数据
    

---

# 2. Request (请求对象)

## 2.1 Request 继承体系

- `ServletRequest`：Java 提供的请求对象体系根接口
    
    - `HttpServletRequest`：Java 提供的对 Http 协议封装的对象请求接口
        
        - `RequestFacade`：Tomcat 定义的实现类
            

> **说明**：Tomcat 需要解析请求数据，封装为 request 对象，并且创建 request 对象传递到 service 方法中。我们在使用时，查阅 JavaEE API 文档的 `HttpServletRequest` 接口即可。

## 2.2 Request 获取请求数据

### 1. 获取请求行

假设请求为：`GET /request-demo/req1?username=zhangsan HTTP/1.1`

- `String getMethod()`：获取请求方式（如：GET）
    
- `String getContextPath()`：获取虚拟目录/项目访问路径（如：`/request-demo`）
    
- `StringBuffer getRequestURL()`：获取 URL/统一资源定位符（如：`http://localhost:8080/request-demo/req1`）
    
- `String getRequestURI()`：获取 URI/统一资源标识符（如：`/request-demo/req1`）
    
- `String getQueryString()`：获取请求参数（GET方式）（如：`username=zhangsan&password=123`）
    

### 2. 获取请求头

假设请求头包含：`User-Agent: Mozilla/5.0 Chrome/91.0.3372.106`

- `String getHeader(String name)`：根据请求头名称，获取值
    

### 3. 获取请求体

只有 POST 请求有请求体（如：`username=superbaby&password=123`）

- `ServletInputStream getInputStream()`：获取字节输入流
    
- `BufferedReader getReader()`：获取字符输入流
    

### 4. 通用方式获取请求参数 (重点)

GET 请求方式和 POST 请求方式的区别在于获取请求参数的方式不一样。

为了统一 doGet 和 doPost 方法内的代码，可以使用通用方式：

- `Map<String, String[]> getParameterMap()`：获取所有参数 Map 集合
    
- `String[] getParameterValues(String name)`：根据名称获取参数值（数组，适用于复选框）
    
- `String getParameter(String name)`：根据名称获取参数值（单个值）
    

**底层逻辑实现原理：**


```Java
String method = request.getMethod();
if("GET".equals(method)){
    // get方式的处理逻辑
    params = this.getQueryString();
} else if("POST".equals(method)){
    // post方式的处理逻辑
    params = reader.readLine();
}
```

**代码示例：**

HTML 表单：

```HTML
<form action="/request-demo/req2" method="get">
    <input type="text" name="username"><br>
    <input type="password" name="password"><br>
    <input type="checkbox" name="hobby" value="1"> 游泳
    <input type="checkbox" name="hobby" value="2"> 爬山 <br>
    <input type="submit">
</form>
```

后端 Servlet：

```Java
protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    // 1. 获取所有参数的Map集合
    Map<String, String[]> map = req.getParameterMap();
    for (String key : map.keySet()) {
        System.out.print(key + ":");
        // 获取值
        String[] values = map.get(key);
        for (String value : values) {
            System.out.print(value + " ");
        }
        System.out.println();
    }
    System.out.println("------------");

    // 2. 根据key获取参数值，数组
    String[] hobbies = req.getParameterValues("hobby");
    for (String hobby : hobbies) {
        System.out.println(hobby);
    }

    // 3. 根据key 获取单个参数值
    String username = req.getParameter("username");
    String password = req.getParameter("password");
    System.out.println(username);
    System.out.println(password);
}

@Override
protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    // POST请求逻辑直接复用doGet
    this.doGet(req, resp);
}
```

## 2.3 Request 请求参数中文乱码处理

请求中如果存在中文数据，可能会出现乱码。

### 1. POST 解决方案

在使用获取参数前，设置字符输入流的编码。

```Java
// 1. 解决乱码：POST
request.setCharacterEncoding("UTF-8"); 

// 2. 获取username
String username = request.getParameter("username");
System.out.println(username);
```

### 2. GET 解决方案

乱码原因：Tomcat 进行 URL 解码，默认的字符集是 ISO-8859-1。

解决思路：先对乱码数据进行 ISO-8859-1 编码（转回字节），再使用 UTF-8 解码。

```Java
// 获取username
String username = request.getParameter("username");

// 通用解决方案：既可以解决GET也可以解决POST
username = new String(username.getBytes(StandardCharsets.ISO_8859_1), StandardCharsets.UTF_8);

System.out.println("解决乱码后：" + username);
```

> **注意**：Tomcat 8.0 之后，已将 GET 请求乱码问题解决，默认解码方式已设置为 UTF-8。

## 2.4 Request 请求转发

请求转发（forward）是一种在服务器 **内部** 的资源跳转方式。

```Java
request.getRequestDispatcher("/req6").forward(request, response);
```

**请求转发特点：**

1. 浏览器地址栏路径 **不发生变化**。
    
2. 只能转发到当前服务器的 **内部资源**。
    
3. 一次请求，可以在转发的资源间使用 request **共享数据**。
    

**共享数据方法：**

- `void setAttribute(String name, Object o)`：存储数据到 request 域中
    
- `Object getAttribute(String name)`：根据 key，获取值
    
- `void removeAttribute(String name)`：根据 key，删除该键值对
    

---

# 3. Response (响应对象)

## 3.1 Response 设置响应数据功能

1. **响应行** (例如 `HTTP/1.1 200 OK`)
    
    - `void setStatus(int sc)`：设置响应状态码
        
2. **响应头** (例如 `Content-Type: text/html`)
    
    - `void setHeader(String name, String value)`：设置响应头键值对
        
3. **响应体** (例如HTML内容)
    
    - `PrintWriter getWriter()`：获取字符输出流
        
    - `ServletOutputStream getOutputStream()`：获取字节输出流
        

## 3.2 Response 完成重定向

重定向（redirect）是一种资源跳转方式。

**实现方式：**

```Java
// 方式1：分步设置
// resp.setStatus(302);
// resp.setHeader("location", "资源B的路径");

// 方式2：简化书写 (推荐)
resp.sendRedirect("/request-demo/resp2"); 
```

**重定向特点：**

1. 浏览器地址栏路径 **发生变化**。
    
2. 可以重定向到任意位置的资源（服务器内部、外部均可）。
    
3. **两次请求**，不能在多个资源使用 request 共享数据。
    

## 3.3 资源路径问题

在编写路径时，需要明确路径是谁在使用：

- **浏览器使用**：需要加虚拟目录（项目访问路径）
    
    - `<a href='路径'>`
        
    - `<form action='路径'>`
        
    - `resp.sendRedirect('路径')`
        
- **服务端使用**：不需要加虚拟目录
    
    - `req.getRequestDispatcher('路径')`
        

**动态获取虚拟目录（推荐做法）：**

```Java
String contextPath = request.getContextPath();
response.sendRedirect(contextPath + "/resp2");
```

## 3.4 Response 响应字符数据

**步骤：**

1. 通过 Response 对象获取字符输出流。
    
2. 写数据。
    

**代码示例与乱码处理：**

```Java
// 设置响应的内容类型及编码，解决中文乱码
response.setContentType("text/html;charset=utf-8");

// 获取流（流不需要手动关闭，服务器会自动关闭）
PrintWriter writer = resp.getWriter();

// 写数据
writer.write("你好");
writer.write("<h1>aaa</h1>");
```

## 3.5 Response 响应字节数据

常用于文件下载或图片显示。

**基本步骤：**

```Java
// 1. 读取文件
FileInputStream fis = new FileInputStream("d://a.jpg");

// 2. 获取response字节输出流
ServletOutputStream os = response.getOutputStream();

// 3. 完成流的copy
byte[] buff = new byte[1024];
int len = 0;
while ((len = fis.read(buff)) != -1) {
    os.write(buff, 0, len);
}
fis.close();
```

**优化步骤 (使用 commons-io)：**

1. `pom.xml` 导入坐标：
    
```XML
<dependency>
    <groupId>commons-io</groupId>
    <artifactId>commons-io</artifactId>
    <version>2.6</version>
</dependency>
```

2. 使用工具类：
    
```Java
IOUtils.copy(fis, os);
fis.close();
```

---

# 4. 案例实战

## 4.1 用户登录

**需求分析：**

1. 用户填写用户名密码，提交到 `LoginServlet`。
    
2. 在 `LoginServlet` 中使用 MyBatis 查询数据库，验证用户名密码是否正确。
    
3. 如果正确，响应“登录成功”；如果错误，响应“登录失败”。
    

**准备环境：**

1. 准备静态页面到项目的 `webapp` 目录下。
    
2. 创建 `db1` 数据库，创建 `tb_user` 表，创建 `User` 实体类。
    
3. 导入 MyBatis 坐标，MySQL 驱动坐标。
    
4. 创建 `mybatis-config.xml` 核心配置文件，`UserMapper.xml` 映射文件，`UserMapper` 接口。
    

**核心代码：**

**1. `mybatis-config.xml` 配置文件：**

```XML
<configuration>
    <typeAliases>
        <package name="com.itheima.pojo"/>
    </typeAliases>

    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql:///db1?useSSL=false&amp;useServerPrepStmts=true"/>
                <property name="username" value="root"/>
                <property name="password" value="1234"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
        <package name="com.itheima.mapper"/>
    </mappers>
</configuration>
```

**2. `UserMapper` 接口：**

```Java
public interface UserMapper {
    @Select("select * from tb_user where username = #{username} and password = #{password}")
    User select(@Param("username") String username, @Param("password") String password);
}
```

**3. 前端 HTML (Login.html)：**

```HTML
<div id="loginDiv">
    <form action="/request-demo/loginServlet" method="post" id="form">
        <h1 id="loginMsg">LOGIN IN</h1>
        <p>Username:<input id="username" name="username" type="text"></p>
        <p>Password:<input id="password" name="password" type="password"></p>
        <div id="subDiv">
            <input type="submit" class="button" value="login up">
            <input type="reset" class="button" value="reset">&nbsp;&nbsp;&nbsp;
            <a href="register.html">没有账号？点击注册</a>
        </div>
    </form>
</div>
```

**4. `LoginServlet.java`：**

```Java
@WebServlet("/loginServlet")
public class LoginServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // 1. 接收用户名和密码
        request.setCharacterEncoding("UTF-8"); // 处理POST乱码
        String username = request.getParameter("username");
        String password = request.getParameter("password");

        // 2. 调用MyBatis完成查询
        // 2.1 获取SqlSessionFactory (此处建议使用工具类，见下文优化)
        String resource = "mybatis-config.xml";
        InputStream inputStream = Resources.getResourceAsStream(resource);
        SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

        // 2.2 获取SqlSession对象
        SqlSession sqlSession = sqlSessionFactory.openSession();
        // 2.3 获取Mapper
        UserMapper userMapper = sqlSession.getMapper(UserMapper.class);
        // 2.4 调用方法
        User user = userMapper.select(username, password);
        // 2.5 释放资源
        sqlSession.close();

        // 3. 判断user是否为null
        response.setContentType("text/html;charset=utf-8");
        PrintWriter writer = response.getWriter();

        if(user != null){
            // 登录成功
            writer.write("登录成功");
        } else {
            // 登录失败
            writer.write("登录失败");
        }
    }
    
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        this.doPost(req, resp);
    }
}
```

## 4.2 用户注册

**需求分析：**

1. 用户填写用户名、密码等信息，点击注册按钮，提交到 `registerServlet`。
    
2. 在 `RegisterServlet` 中使用 MyBatis 保存数据。
    
3. 保存前需要判断用户名是否已经存在：根据用户名查询数据库。
    

**核心代码：**

**1. `UserMapper` 接口增加方法：**

```Java
/**
 * 根据用户名查询用户对象
 */
@Select("select * from tb_user where username = #{username}")
User selectByUsername(String username);

/**
 * 添加用户
 */
@Insert("insert into tb_user values(null, #{username}, #{password})")
void add(User user);
```

**2. `RegisterServlet.java`：**

```Java
@Override
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    // 1. 接收用户数据
    request.setCharacterEncoding("UTF-8");
    String username = request.getParameter("username");
    String password = request.getParameter("password");

    // 封装用户对象
    User user = new User();
    user.setUsername(username);
    user.setPassword(password);

    // 2. 调用mapper
    // (此处省略获取SqlSessionFactory的代码，建议复用工具类)
    SqlSession sqlSession = sqlSessionFactory.openSession();
    UserMapper userMapper = sqlSession.getMapper(UserMapper.class);

    // 2.4 查询用户名是否存在
    User u = userMapper.selectByUsername(username);

    // 3. 判断用户对象是否为null
    if(u == null){
        // 用户名不存在，添加用户
        userMapper.add(user);
        // 提交事务 (MyBatis默认不自动提交)
        sqlSession.commit();
        sqlSession.close();
        
        response.setContentType("text/html;charset=utf-8");
        response.getWriter().write("注册成功");
    } else {
        // 用户名存在，给出提示信息
        sqlSession.close();
        response.setContentType("text/html;charset=utf-8");
        response.getWriter().write("用户名已存在");
    }
}
```

## 4.3 代码优化 (SqlSessionFactoryUtils)

**问题：**

1. 上述 Servlet 中创建 `SqlSessionFactory` 的代码重复。
    
2. `SqlSessionFactory` 工厂对象比较重，只需要创建一次，不要重复创建。
    

**解决：** 新建 `SqlSessionFactoryUtils` 工具类，使用静态代码块。

```Java
public class SqlSessionFactoryUtils {

    private static SqlSessionFactory sqlSessionFactory;

    static {
        // 静态代码块会随着类的加载而自动执行，且只执行一次
        try {
            String resource = "mybatis-config.xml";
            InputStream inputStream = Resources.getResourceAsStream(resource);
            sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static SqlSessionFactory getSqlSessionFactory(){
        return sqlSessionFactory;
    }
}
```

使用方式：

在 Servlet 中替换原有的工厂创建代码：

```Java
SqlSessionFactory sqlSessionFactory = SqlSessionFactoryUtils.getSqlSessionFactory();
```