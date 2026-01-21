# Web核心

- JavaWeb技术栈
- B/S架构：Browser/Server，浏览器/服务器 架构模式，它的特点是，客户端只需要浏览器，应用程序的逻辑和数据都存储在服务器端，浏览器只需要请求服务器，获取Web资源，服务器把Web资源发送给浏览器即可

好处：易于维护升级，服务端升级后，客户端无需任何部署就可以使用到新的版本

- 静态资源：HTML，CSS，JavaScript，图片等。负责页面展现
- 动态资源：Servlet，JSP等。负责逻辑处理
- 数据库：负责存储管理
- HTTP协议：定义通信规则
- Web服务器（Tomcat）：负责解析HTTP协议，解析请求数据，并发送响应数据

## HTTP

- HyperTextTranferProtocol，超文本传输协议，规定了浏览器和服务器之间的数据传输规则
- HTTP协议特点：
- 基于TCP协议：面向连接，安全
- 基于请求-响应模型的：一次请求对应一次响应
- HTTP协议时无状态的协议：对于事务处理没有记忆能力。每次请求-响应都是独立的

缺点：多次请求间不能共享数据。Java中使用会话技术（Cookie，Session）来解决问题

优点：速度快

### 请求数据格式

请求数据分为3部分：

1.  请求行：请求数据的第一行。其中GET表示请求方式，/表示请求资源路径，HTTP/1.1表示协议版本

2.  请求头：第二行开始，格式为key：value形式

常见HTTP请求头：

Host：表示请求的主机名

User-Agent：浏览器版本

Accept：表示浏览器能接受的资源类型，如text/\*,image/\*,\*/\*表示所有

Accept-language：表示浏览器偏好的语言，服务器可以据此返回不同语言的网页

Accept-Encoding：表示浏览器可以支持的压缩类型，例如gzip，deflate等

1.  请求体：POST请求的最后一部分，存放请求参数

GET请求和POST请求的区别：

GET请求请求参数在请求行中，没有请求体。POST请求请求参数在请求体中

GET请求请求参数大小有限制，POST没有

### 响应数据格式

1.  响应行：响应数据的第一行。其中HTTP/1.1表示协议版本，200表示响应状态码，OK表示状态码描述

状态码分类：

1xx 响应中

2xx 成功

3xx 重定向

4xx 客户端错误

5xx 服务端错误 --责任在服务端

1.  响应头：第二行开始，格式为key：value形式

常见HTTP响应头：

Content-Type：表示该响应内容的类型，例如text/html，image/jpeg

Content-Length：表示该响应内容的长度（字节数）

Content-Encoding：表示该响应的压缩算法，例如gzip

Cache-Control：指示客户端应如何缓存，例如max-age=300，表示可以最多缓存300s

1.  响应体：最后一部分，存放响应数据

## Web服务器-Tomcat

- Web服务器是一个应用程序，对HTTP协议的操作进行封装，使得程序员不必直接对协议进行操作，让web开发更加便捷，主要功能是”提供网上信息浏览服务”
- Tomcat
- 轻量级的Web服务器，支持Servlet/JSP少量JavaEE规范，Tomcat也被称为Web服务器，Servlet容器。Servlet需要依赖Tomcat才能运行
- JavaEE：Java企业级开发的计数规范总和

### 基本使用

1.  启动：双击：bin\\startup.bat

控制台中文乱码：修改conf/logging.properties UTF-8改为GBK

1.  关闭：强制关闭，直接叉掉/shutdown.bat关闭/黑窗口中ctrl-c关闭
2.  配置

修改启动端口号：conf/server.xml

Http协议默认端口号为80，如果将Tomcat端口号改为80，则将来访问Tomcat时，将不用输入端口号

1.  启动时可能出现的问题
2.  端口号冲突：找到对应程序，将其关闭掉
3.  启动窗口一闪而过 [Tomcat双击startup.bat闪退](https://zhuanlan.zhihu.com/p/353404326)/Java_home没有正确配置

4.  部署项目

- Tomcat部署项目：将项目放置到webapps目录下，即部署完成
- 一般将JavaWeb项目打包成war包，然后将war包放到webapps目录下，Tomcat会自动解压缩war文件

### IDEA中创建Maven Web项目

1.  web项目结构

编译后Java字节码文件和resources的资源文件，放到WEB-INF下的classes目录下

Pom.xml中以来坐标对应的jar包，放入WEB-INF下的lib目录下

但是package过程中可以自动完成这些进程

1.  使用骨架

Archtype 创建项目 补齐缺失的目录结构：webapp

1.  不使用骨架

同样创建maven文件，在file-project structure-Facets中添加目录

4）在Tomcat中运行 通过

<packaging>war</packaging>

打包成war包移动到webapps目录下，即可自动解压

1.  IDEA中创建Maven Web项目
2.  将本地Tomcat集成到idea中，然后进行项目部署即可
3.  Pom.xml中添加TomCat插件

右键文件选择run Maven-tomcat7：run

1.      _<!-- tomcat插件 -->_
2.      <build>
3.          <plugins>
4.              <plugin>
5.                  <groupId>org.apache.tomcat.maven</groupId>
6.                  <artifactId>tomcat7-maven-plugin</artifactId>
7.                  <version>2.2</version>
8.              </plugin>
9.          </plugins>
10.     </build>

可以设置端口号以及路径

1.  <port>80</port>
2.  <path>/</path>


## Request & Response

- Request：获取请求数据
- Response：设置响应数据

### Request

#### Request继承体系

ServletRequest ---Java提供的请求对象体系根接口

|

HttpServletRequest ----Java提供的对Http协议封装的对象请求接口

|

requestFacade -----Tomcat定义的实现类

Tomcat需要解析请求数据，分装为request对象，并且创建request对象传递到service方法中

使用request对象，查阅JavaEE API文档的HttpServletRequest接口

#### Request获取请求数据

1.  获取请求数据
2.  请求行

GET/request-demo/req1?username=zhangsan HTTP/1.1

- String getMethod()：获取请求方式：GET
- String getContextPath()：获取虚拟目录（项目访问路径）：/request-demo
- StringBuffer getrequestURL()：获取URL（统一资源定位符）：

http：//localhost:8080/request-demo/req1

- String getRequestURL()：获取URI（统一资源标识符）/request-demo/req1
- String getQueryString()：获取请求参数（GET方式）：username=zhangsan&password=123

1.  请求头

User-Agent：Mozilla/5.0 Chrome/91.0.3372.106

- String getHeader(String name)：根据请求头名称，获取值

1.  请求体：只有post请求有请求体 username =superbaby &password =123

- ServletInputStream getInputStream()：获取字节输入流
- BufferReader getReader()：获取字符输入流

1.  通用方式获取请求参数

请求参数获取方式

- GET方式：String getQuertString()
- POST方式 BufferedReader getReader()

GET请求方式和POST请求方式的区别在于获取请求参数的方式不一样，是否可以提供一种统一获取请求参数的方式，从而统一doGet和doPost方法内的代码？

Map<String,String\[\]>getParameterMap():获取所有参数Map集合

String\[\] getParameterValues(String name)：根据名称获取参数值（数组）

String getParameter(String name):根据名称获取参数值（单个值）

1.  <form action="/request-demo/req2" method="get">
2.      <input type="text" name="username"><br>
3.      <input type="password" name="password"><br>
4.      <input type="checkbox" name="hobby" value="1"> 游泳
5.      <input type="checkbox" name="hobby" value="2"> 爬山 <br>
6.      <input type="submit">

后端：

1.  protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
2.          _//GET请求逻辑_
3.          _//System.out.println("get....");_

4.          _//1. 获取所有参数的Map集合_
5.          Map<String, String\[\]> map = req.getParameterMap();
6.          for (String key : map.keySet()) {
7.              _// username:zhangsan lisi_
8.              System.out.print(key+":");

9.             _//获取值_
10.             String\[\] values = map.get(key);
11.             for (String value : values) {
12.                 System.out.print(value + " ");
13.             }

14.             System.out.println();
15.         }

16.         System.out.println("------------");

17.         _//2. 根据key获取参数值，数组_
18.         String\[\] hobbies = req.getParameterValues("hobby");
19.         for (String hobby : hobbies) {

20.             System.out.println(hobby);
21.         }

22.         _//3. 根据key 获取单个参数值_
23.         String username = req.getParameter("username");
24.         String password = req.getParameter("password");

25.         System.out.println(username);
26.         System.out.println(password);
27.     }

doPost

1.      @Override
2.      protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
3.          _//POST请求逻辑_

4.          this.doGet(req,resp);

5.  }

实现方式的底层逻辑

1.          String method = request.getMethod();

2.          if("GET".equals(method)){
3.              _// get方式的处理逻辑_
4.  params_\= this.getQueryString();_
5.          }else if("POST".equals(method)){
6.              _// post方式的处理逻辑_
7.  params _= reader.readLine();_
8.          }

工具：IDEA模板创建Servlet

1.  Request请求参数中文乱码处理

请求中如果存在中文数据，这可能出现乱码

1.  POST解决方案
2.  _//1. 解决乱码：POST，getReader()_
3.  request.setCharacterEncoding("UTF-8");_//设置字符输入流的编码_

4.  _//2. 获取username_
5.  String username = request.getParameter("username");
6.  System.out.println(username);

7.  GET解决方案

编码与解码不一致

1.    _//获取username_
2.          String username = request.getParameter("username");
3.          System.out.println("解决乱码前："+username);

4.          _//GET,获取参数的方式：getQueryString_
5.          _// 乱码原因：tomcat进行URL解码，默认的字符集ISO-8859-1_
6.      _//先对乱码数据进行编码：转为字节数组_
7.  //      byte\[\] bytes = username.getBytes(StandardCharsets.ISO_8859_1);
8.          //字节数组解码
9. //      username = new String(bytes, StandardCharsets.UTF_8);

10.         username  = new String(username.getBytes(StandardCharsets.ISO_8859_1),StandardCharsets.UTF_8);

11.         System.out.println("解决乱码后："+username);

通用解决方案：既可以解决GET也可以解决POST

username  = new String(username.getBytes(StandardCharsets.ISO_8859_1),StandardCharsets.UTF_8);

Tomcat 8.0之后，已将GET请求乱码问题解决，设置默认的解码方式为UTF-8

#### Request请求转发

请求转发（forward）：一种在服务器内部的资源跳转方式

request.getRequestDispatcher("/req6").forward(request,response);

1.  请求转发资源间共享数据：使用Request对象

void setAttribute(String name,Object o)：存储数据到request域中

Object getAttribute（String name）：根据key，获取值

Void removeAttribute（String name）：根据key，删除该键值对

1.  请求转发特点
2.  浏览器地址栏路径不发生变化
3.  只能转发到当前服务器的内部资源
4.  一次请求，可以在转发的资源间使用request共享数据

### Response

#### Response设置响应数据功能介绍

1.  响应行 HTTP/1.1 200OK

void setStatus(int sc)：设置响应状态码

1.  响应头 Content-Type:text/html

void setHeader（String name，String value）：设置响应头键值对

1.  响应体 <html><head><head><body></body></html>

PrintWriter getWriter：获取字符输出流

ServletOutputStream getOutputStream（）：获取字节输出流

#### Response完成重定向

重定向（redirect）：一种资源跳转方式

1.  实现方式
2.  resp.setStatus(302)；
3.  Resp.setHeader(“location”,”资源B的路径”)；

|

| 简化书写

resp.sendRedirect（“资源B的路径”）

//resp.sendRedirect（“/request-demo/resp2”）--虚拟目录/外部资源均可

1.  重定向特点

- 浏览器地址栏路径发生拜年话
- 可以重定向到任意位置的资源（服务器内部，外部均可）
- 两次请求，不能在多个资源使用request共享数据

1.  资源路径问题
2.  明确路径谁使用？

浏览器使用：需要加虚拟目录（项目访问路径）

服务端使用：不需要加虚拟目录

例：

<a href = ‘路径’> 加虚拟目录

<form action = ’路径’> 加虚拟目录

req.getrequestDispatcher（‘路径’） 不加虚拟目录

resp.sendRedirect（‘路径’） 加虚拟目录

1.  动态获取虚拟目录
2.  String contextPath =request.getContextPath();
3.  Response.sendRedierect(contextPath + “/resp2”)；

#### Response响应字符数据

1.  使用
2.  通过Response对象获取字符输出流

PrintWriter writer = resp.getwriter（）；

1.  写数据

writer.write("aaa");

1.  PrintWriter writer = resp.getwriter（）；
2.  response.setHeader("content-type","text/html");
3.  writer.write("<h1>aaa</h1>");

4.  细节
5.  流不需要关闭
6.  如果响应字符是中文，会乱码，处理方法：setContentType
7.  response.setContentType("text/html;charset = utf-8");
8.  PrintWriter writer = resp.getwriter（）；
9.  writer.write("你好");
10.  writer.write("<h1>aaa</h1>");

#### Response响应字节数据

1.  使用
2.  读取文件

FileInputStream fis = new FileInputStream（"d://a.jpg"）;

1.  获取response字节输出流

ServletOutputStream os = response.getOutputStream();

1.  完成流的copy

byte\[\] buff = new byte\[1024\];

int len = 0;

while ((len = fls.read(buff))!= -1){

&nbsp; os.write(buff,0,len);

}

优化:

pom.xml中导入坐标

1.  <dependency>
2.        <groupId>commons-io</groupId>
3.        <artifactId>commons-io</artifactId>
4.        <version>2.6</version>
5.  </dependency>

使用:

IOUtils.copy(fis,os);

1.  关闭流

fis.close();

### 案例

#### 用户登录

1.  需求分析：
2.  用户填写用户名密码，提交到LoginServlet
3.  在LoginServlet中使用MyBatis查询数据库，验证用户名密码是否正确
4.  如果正确，响应登录成功，如果错误，响应登录失败

5.  准备环境
6.  准备静态页面到项目的webapp目录下
7.  创建db1数据表，创建tb_user表，创建User实体类
8.  导入Mybatis坐标，MySQL驱动坐标
9.  创建mybatis-config.xml核心配置文件，UserMapper.xml映射文件，UserMapper接口

Mybatis-config配置文件

1.  <configuration>
2.      _<!--起别名-->_
3.      <typeAliases>
4.          <package name="com.itheima.pojo"/>
5.      </typeAliases>

6.      <environments default="development">
7.          <environment id="development">
8.              <transactionManager type="JDBC"/>
9.             <dataSource type="POOLED">
10.                 <property name="driver" value="com.mysql.jdbc.Driver"/>
11.                 <property name="url" value="jdbc:mysql:///db1?useSSL=false&amp;useServerPrepStmts=true"/>
12.                 <property name="username" value="root"/>
13.                 <property name="password" value="1234"/>
14.             </dataSource>
15.         </environment>
16.     </environments>
17.     <mappers>
18.         _<!--扫描mapper-->_
19.         <package name="com.itheima.mapper"/>
20.     </mappers>

UserMapper.xml映射文件

1.  <mapper namespace="com.itheima.mapper.UserMapper">

2.  </mapper>

3.  接口UseMapper
4.  @Select("select \* from tb_user where username = #{username} and password = #{password}")
5.  User select(@Param("username") String username,@Param("password")  String password);

6.  用户填写用户名密码，提交到LoginServlet

Login.html

1.  <div id="loginDiv">
2.      <form action="/request-demo/loginServlet" method="post" id="form">
3.          <h1 id="loginMsg">LOGIN IN</h1>
4.          <p>Username:<input id="username" name="username" type="text"></p>

5.          <p>Password:<input id="password" name="password" type="password"></p>

6.          <div id="subDiv">
7.              <input type="submit" class="button" value="login up">
8.             <input type="reset" class="button" value="reset">&nbsp;&nbsp;&nbsp;
9.             <a href="register.html">没有账号？点击注册</a>
10.         </div>
11.     </form>
12. </div>

13.  在LoginServlet中使用MyBatis查询数据库，验证用户名密码是否正确

LoginServlet.java

1.  _//2. 调用MyBatis完成查询_
2.  _//2.1 获取SqlSessionFactory对象_
3.  String resource = "mybatis-config.xml";
4.  InputStream inputStream = Resources.getResourceAsStream(resource);
5.  SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

6.  SqlSessionFactory sqlSessionFactory = SqlSessionFactoryUtils.getSqlSessionFactory();
7.  _//2.2 获取SqlSession对象_
8.  _//2.3 获取Mapper_
9. UserMapper userMapper = sqlSession.getMapper(UserMapper.class);
10. _//2.4 调用方法_
11. User user = userMapper.select(username, password);
12. _//2.5 释放资源_
13. sqlSession.close();

14.  如果正确，响应登录成功，如果错误，响应登录失败，即判断user释放是否为null 如果不等于null则登录成功，等于null则登录失败
15.          _//获取字符输出流，并设置content type_
16.          response.setContentType("text/html;charset=utf-8");
17.          PrintWriter writer = response.getWriter();
18.          _//3. 判断user释放为null_
19.          if(user != null){
20.              _// 登录成功_
21.              writer.write("登录成功");
22.          }else {
23.             _// 登录失败_
24.             writer.write("登录失败");
25.         }

#### 用户注册

1.  需求分析
2.  用户填写用户名，密码等信息，点击注册按钮，提交到registerServlet
3.  在RegisterServlet中使用MyBatis保存数据
4.  保存前需要判断用户名是否已经存在：根据用户名查询数据库

5.  接口UserMapper
6.      _/\*\*_
7.       \* 根据用户名查询用户对象
8.       \* @param username
9.       \* @return
10.       \*/
11.      @Select("select \* from tb_user where username = #{username}")
12.      User selectByUsername(String username);

13.     _/\*\*_
14.      \* 添加用户
15.      \* @param user
16.      \*/
17.    @Insert("insert into tb_user values(null,#{username},#{password})")
18.    void add(User user);

19.  用户填写用户名，密码等信息，点击注册按钮，提交到registerServlet
20.  <div class="form-div">
21.      <div class="reg-content">
22.          <h1>欢迎注册</h1>
23.          <span>已有账号？</span> <a href="login.html">登录</a>
24.      </div>
25.      <form id="reg-form" action="/request-demo/registerServlet" method="post">

26.          <table>

27.             <tr>
28.                 <td>用户名</td>
29.                 <td class="inputs">
30.                     <input name="username" type="text" id="username">
31.                     <br>
32.                     <span id="username_err" class="err_msg" style="display: none">用户名不太受欢迎</span>
33.                 </td>

34.             </tr>

35.             <tr>
36.                 <td>密码</td>
37.                 <td class="inputs">
38.                     <input name="password" type="password" id="password">
39.                     <br>
40.                     <span id="password_err" class="err_msg" style="display: none">密码格式有误</span>
41.                 </td>
42.             </tr>

43.         </table>

44.         <div class="buttons">
45.             <input value="注 册" type="submit" id="reg_btn">
46.         </div>
47.         <br class="clear">
48.     </form>

49. </div>

50.  在RegisterServlet中使用MyBatis保存数据
51.  @Override
52.  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
53.      _//1. 接收用户数据_
54.      String username = request.getParameter("username");
55.      String password = request.getParameter("password");

56.      _//封装用户对象_
57.      User user = new User();
58.     user.setUsername(username);
59.     user.setPassword(password);

60.     _//2. 调用mapper 根据用户名查询用户对象_
61.     _//2.1 获取SqlSessionFactory对象_
62.     String resource = "mybatis-config.xml";
63.     InputStream inputStream = Resources.getResourceAsStream(resource);
64.     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
65.     SqlSessionFactory sqlSessionFactory = SqlSessionFactoryUtils.getSqlSessionFactory();

66.     _//2.2 获取SqlSession对象_
67.     SqlSession sqlSession = sqlSessionFactory.openSession();
68.     _//2.3 获取Mapper_
69.     UserMapper userMapper = sqlSession.getMapper(UserMapper.class);

70.     _//2.4 调用方法_
71.     User u = userMapper.selectByUsername(username);
72.     }

73.  保存前需要判断用户名是否已经存在：根据用户名查询数据库
74.   _//3. 判断用户对象释放为null_
75.      if( u == null){
76.          _// 用户名不存在，添加用户_
77.          userMapper.add(user);
78.          _// 提交事务_
79.          sqlSession.commit();
80.          _// 释放资源_
81.          sqlSession.close();
82.     }else {
83.         _// 用户名存在，给出提示信息_
84.         response.setContentType("text/html;charset=utf-8");
85.         response.getWriter().write("用户名已存在");
86.     }

#### 代码优化

1.  创建SqlSessionFactory代码优化
2.  _//2.1 获取SqlSessionFactory对象_
3.  String resource = "mybatis-config.xml";
4.  InputStream inputStream = Resources.getResourceAsStream(resource);
5.  SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

问题：

- 代码重复
- SqlSessionFactory工厂只创建一次，不要重复创建

解决：新建SqlSessionFactoryUtils工具类

1.  public class SqlSessionFactoryUtils {

2.      private static SqlSessionFactory sqlSessionFactory;

3.      static {
4.          _//静态代码块会随着类的加载而自动执行，且只执行一次_

5.          try {
6.              String resource = "mybatis-config.xml";
7.             InputStream inputStream = Resources.getResourceAsStream(resource);
8.             sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
9.         } catch (IOException e) {
10.             e.printStackTrace();
11.         }
12.     }
13.     public static SqlSessionFactory getSqlSessionFactory(){
14.         return sqlSessionFactory;
15.     }
16. }


## 会话跟踪技术

- 会话：用户打开浏览器，访问web服务器的资源，会话建立，直到有一方断开连接，会话结束，在一次会话中包含多次请求和响应
- 会话跟踪：是一种维护浏览器状态的方法，服务器需要识别多次请求是否来自同一浏览器，以便在同一次会话的多次请求间共享数据
- HTTP协议是无状态的，每次浏览器向服务器请求时，服务器都会将该请求视为新的请求，因此需要会话跟踪技术来实现会话内数据共享
- 实现方式：客户端会话跟踪技术（cookie），服务端会话跟踪技术（Session）
- 目的：一次会话的多次请求间获取数据

### Cookie基本使用

Cookie：客户端会话技术，将数据保存到客户端，以后每次请求都携带Cookie数据进行访问

1.  发送cookie
2.  创建cookie对象，设置数据

Cookie cookie = new Cookie("key","value");

1.  发送Cookie到客户端，使用response对象

response.addCookie(cookie)

1.  获取cookie
2.  获取客户端携带的所有Cookie，使用request对象

Cookie\[\] cookies = request.getCookies();

1.  遍历数组，获取每一个Cookie对象：for
2.  使用Cookie对象方法获取数据

cookie.getName();

cookie.getValue();

### Cookie原理

- Cookie的实现是基于HTTP协议的
- 发送cookie响应头：set-cookie
- 获取cookie请求头：cookie

### Cookie使用细节

- Cookie存活时间
- 默认情况下，Cookie存储在浏览器内存中，当浏览器关闭，内存释放，则Cookie被销毁
- setMaxAge(int seconds)：设置Cookie存活时间

正数：将Cookie写入浏览器所在电脑的硬盘，永久化存储，到时间自动删除

负数：默认值，Cookie在当前浏览器内存中，当浏览器关闭，则Cookie被销毁

零：删除对应Cookie

- Cookie存储中文
- 默认情况下，Cookie不能直接存储中文
- 如需要存储，则需要进行转码：URL编码

发送端：

1.  String value = "张三";
2.  _//URL编码_
3.  value = URLEncoder.encode(value, "UTF-8");
4.  Cookie cookie = new Cookie("username",value);

接收端：

1.  _//URL解码_
2.  value = URLDecoder.decode(value,"UTF-8");

### Session基本使用

- 服务端会话跟踪技术：将数据保存到服务端
- JavaEE提供HttpSession接口，来实现一次会话的多次请求间数据共享功能
- 使用

1.  获取Session对象

HttpSession session = request.getSession();

1.  Session对象功能

- void setAttribute（String name，Object o）：存储数据到session域中
- Object getAttribute（String name）：根据key，获取值
- void removeAttribute（String name）：根据key，删除该键值对

### Session原理

- Session是基于Cookie实现的
- 一次会话的多个请求间，不论获取多少次session对象，获取的session对象始终是同一个
- 通过COOKIE对象中的JSESSIONID来实现，查找id

### Session使用细节

- Session钝化，活化（自动实现）
- 服务器正常重启后，Session中的数据仍然存在
- 钝化：在服务器正常关闭后，Tomcat会自动将Session数据写入硬盘的文件
- 活化：再次启动服务器后，从文件中加载数据到Session中，但是session不是同一个session对象
- Session销毁
- 默认情况下，无操作，30分钟自动销毁，使用session-config标签配置时间

1.  <session-config>
2.       <session-timeout>100</session-timeout>
3.  </session-config>

- 调用Session对象的invalidate（）方法

### 小结

- Cookie和Session都是来完成一次会话内多次请求间数据共享的

1.  区别

- 存储位置：Cookie是将数据存储在客户端，Session将数据存储在服务端
- 安全性：Cookie不安全，Session安全
- 数据大小：Cookie最大3kb，Session无大小限制
- 存储时间：Cookie可以长期存储，Session默认30分钟
- 服务器性能：Cookie不占服务器资源，Session占用服务器资源

1.  示例分析

购物车数据-Cookie

偏好设置-Cookie

用户数据-Session

记住我功能-Cookie 但是有被盗用的风险 不安全

验证码-Session 需要保证安全性防止暴力注入

### 登录注册案例

#### 需求说明

- 完成用户登录功能，如果用户勾选“记住用户”，则下次访问登录页面，自动填充用户名和密码
- 完成注册功能，并实现验证码功能

#### 用户登录

1.  Dao层

UserMapper.java

1.   _/\*\*_
2.       \* 根据用户名和密码查询用户对象
3.       \* @param username
4.       \* @param password
5.       \* @return
6.       \*/
7.      @Select("select \* from tb_user where username = #{username} and password = #{password}")
8.      User select(@Param("username") String username,@Param("password")  String password);

9.  Service层

新建UserService并在其中创建方法login

1.  public class UserService {

2.      SqlSessionFactory factory = SqlSessionFactoryUtils.getSqlSessionFactory();

3.      _/\*\*_
4.       \* 登录
5.       \* @param username
6.       \* @param password
7.       \* @return
8.      \*/
9.     public User login(String username,String password){        _//2. 获取SqlSession_
10.         _//获取sqlSession_
11.         SqlSession sqlSession = factory.openSession();

12.         _//获取UserMapper_
13.         UserMapper mapper = sqlSession.getMapper(UserMapper.class);

14.         _//调用方法_
15.         User user = mapper.select(username,password);

16.         _//释放资源_
17.         sqlSession.close();

18.         return null ;
19.     }
20. }

21.  Web层

导入css/imgs文件到webapp包中

新建login.jsp定义静态页面并定义action

<form action="/brand-demo/loginServlet" id="form">

新建loginServlet完成业务

1.  @WebServlet("/loginServlet")
2.  public class LoginServlet extends HttpServlet {
3.      private UserService service = new UserService();

4.      @Override
5.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
6.          _//1.获取用户名和密码_
7.          String username = request.getParameter("username");
8.          String password = request.getParameter("password");

9.         _//2.调用service查询_
10.         User user = service.login(username,password);

11.         if (user != null){
12.             _//登录成功，跳转到查询所有的BrandServlet_

13.             _//将登录成功后的user对象存储到session中_
14.             HttpSession session = request.getSession();
15.             session.setAttribute("user",user);

16.             String contextPath = request.getContextPath();
17.             response.sendRedirect(contextPath + "/selectAllServlet");
18.         }else{
19.             _//登录失败_

20.             _//错误信息到request_
21.             request.setAttribute("login_msg","用户名或密码错误");

22.             _//跳转到login.jsp_
23.             request.getRequestDispatcher("/login.jsp").forward(request,response);
24.         }
25.     }

26.     @Override
27.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
28.         this.doGet(request, response);
29.     }
30. }

- 登录成功，跳转到查询所有的BrandServlet中，登录请求与查询所有的请求之间没有数据需要共享，使用重定向，如果资源跳转需要资源共享，则需要转发
- 登录成功是一次请求，重定向到另一个页面是另一次请求，同一会话的两次请求之间共享数据需要把数据存在cookie或者session，这里有安全性要求，所以登录成功后将登录成功的user对象存储到session域中，然后使用EL表达式查找
- 登录失败，要携带用户名登录错误这类错误信息提示跳转回login页面，可以采用将数据存到request域中，将其转发回对应的login.jsp，request域中存的数据只能通过转发的形式才能获取这个数据

修改login.jsp

<div id="errorMsg">${login_msg}</div>

- 使用EL表达式，这里称为动态的表达

#### 记住用户--写Cookie

- 如果用户勾选“记住用户”，则下次访问登录页面自动填充用户名和密码
- 如何自动填充用户名和密码？
- 将用户名和密码写入Cookie中，并且持久化存储Cookie，下次访问浏览器会自动携带Cookie
- 在页面获取Cookie数据后，设置到用户名和密码框中
- 何时写Cookie
- 用户名密码成功登录
- 并且勾选Remember

修改LoginServlet

1.  @Override
2.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
3.          _//1.获取用户名和密码_
4.          String username = request.getParameter("username");
5.          String password = request.getParameter("password");

6.          _//获取复选框数据_
7.          String remember = request.getParameter("remember");

8.         _//2.调用service查询_
9.         User user = service.login(username,password);

10.         if (user != null){
11.             _//登录成功，跳转到查询所有的BrandServle_

12.             _//判断用户是否勾选记住我_

13.             if("1".equals(remember)){
14.                 _//勾选了记住我_

15.                 _//创建Cookie_
16.                 Cookie c_username = new Cookie("username",username);
17.                 Cookie c_password = new Cookie("password",password);

18.                 _//设置Cookie的存活时间_
19.                 c_username.setMaxAge( 60\*60\*24\*7 );
20.                 c_password.setMaxAge( 60\*60\*24\*7 );

21.                 _//发送_
22.                 response.addCookie(c_username);
23.                 response.addCookie(c_password);

24.             }
25.             _//将登录成功后的user对象存储到session中_
26.             HttpSession session = request.getSession();
27.             session.setAttribute("user",user);

28.             String contextPath = request.getContextPath();
29.             response.sendRedirect(contextPath + "/selectAllServlet");
30.         }else{
31.             _//登录失败_
32.             _//错误信息到request_
33.             request.setAttribute("login_msg","用户名或密码错误");

34.             _//跳转到login.jsp_
35.             request.getRequestDispatcher("/login.jsp").forward(request,response);
36.         }
37.     }

修改Login.jsp

<p>Remember:<input id="remember" name="remember" value ="1" type="checkbox"></p>

加入value使得确认remember复选框的内容

#### 记住用户--获取Cookie

- 在页面获取cookie数据后，设置到用户名和密码框中：EL表达式
- ${cookie.key.value}//key指存储在cookie中的键名称

修改login.jsp

1.  <p>Username:<input id="username" name="username" value ="${cookie.username.value}"type="text"></p>

2.  <p>Password:<input id="password" name="password" type="password" value ="${cookie.password.value}"></p>

#### 用户注册--注册功能

保存用户信息到数据库

1.  Dao层
2.      _/\*\*_
3.       \* 根据用户名查询用户对象
4.       \* @param username
5.       \* @return
6.       \*/
7.      @Select("select \* from tb_user where username = #{username}")
8.      User selectByUsername(String username);

9.     _/\*\*_
10.      \* 添加用户
11.      \* @param user
12.      \*/
13.     @Insert("insert into tb_user values(null,#{username},#{password})")
14.     void add(User user);

15.  Service层
16.  public boolean register(User user){
17.          _//获取sqlSession_
18.          SqlSession sqlSession = factory.openSession();

19.          _//获取UserMapper_
20.          UserMapper mapper = sqlSession.getMapper(UserMapper.class);

21.          _//判断用户名是否存在_
22.         User u = mapper.selectByUsername(user.getUsername());

23.         if (u == null){
24.             _//用户名不存在，注册_
25.             mapper.add(user);
26.             sqlSession.commit();

27.         }
28.         sqlSession.close();

29.         return u == null;
30.     }

31.  Web层

新建RegisterServlet

1.  @WebServlet("/registerServlet")
2.  public class RegisterServlet extends HttpServlet {
3.      private UserService service = new UserService();

4.      @Override
5.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
6.          _//获取用户名和密码数据_
7.          String username = request.getParameter("username");
8.          String password = request.getParameter("password");

9.         User user = new User();
10.         user.setUsername(username);
11.         user.setPassword(password);

12.         _//调用service查询_
13.         boolean flag = service.register(user);
14.         _//判断注册成功与否_
15.         if (flag){
16.             _//注册功能，跳转登录页面_

17.             request.setAttribute("register_msg","注册成功请登录");
18.             request.getRequestDispatcher("/login.jsp").forward(request,response);

19.         }else{
20.             _//注册失败，跳转到注册页面_

21.             request.setAttribute("register_msg","用户名已存在");
22.             request.getRequestDispatcher("/register.jsp").forward(request,response);

23.         }

24.     }

25.     @Override
26.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
27.         this.doGet(request, response);
28.     }
29. }

修改login.jsp

<div id="errorMsg">${login_msg}${register_msg}</div>

#### 用户注册--验证码功能

- 验证码就是使用Java代码生成的一张图片
- 验证码作用：防止机器自动注册，攻击服务器

导入CheckCodeUtil，生成验证码工具类

新建CheckCodeServlet类-生成一个验证码图片

1.  @WebServlet("/checkCodeServlet")
2.  public class CheckCodeServlet extends HttpServlet {

3.      @Override
4.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

5.     ServletOutputStream os = response.getOutputStream();
6.     String checkCode = CheckCodeUtil.outputVerifyImage(100, 50, os, 4);
7.      }

8.     @Override
9.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
10.         this.doGet(request, response);
11.     }
12. }

实现点击看不清，验证码图片更换一张

修改register.jsp

1.  <div class="form-div">
2.      <div class="reg-content">
3.          <h1>欢迎注册</h1>
4.          <span>已有账号？</span> <a href="login.html">登录</a>
5.      </div>
6.      <form id="reg-form" action="/brand-demo/registerServlet" method="post">

7.          <table>

8.             <tr>
9.                 <td>用户名</td>
10.                 <td class="inputs">
11.                     <input name="username" type="text" id="username">
12.                     <br>
13.                     <span id="username_err" class="err_msg">${register_msg}</span>
14.                 </td>

15.             </tr>

16.             <tr>
17.                 <td>密码</td>
18.                 <td class="inputs">
19.                     <input name="password" type="password" id="password">
20.                     <br>
21.                     <span id="password_err" class="err_msg" style="display: none">密码格式有误</span>
22.                 </td>
23.             </tr>

24.             <tr>
25.                 <td>验证码</td>
26.                 <td class="inputs">
27.                     <input name="checkCode" type="text" id="checkCode">
28.                     <img id="checkCodeImg" src="/brand-demo/checkCodeServlet">
29.                     <a href="#" id="changeImg" >看不清？</a>
30.                 </td>
31.             </tr>

32.         </table>

33.         <div class="buttons">
34.             <input value="注 册" type="submit" id="reg_btn">
35.         </div>
36.         <br class="clear">
37.     </form>

38. </div>

39. <script>
40.     document.getElementById("changeImg").onclick = function (){
41.         document.getElementById("checkCodeImg").src = "/brand-demo/checkCodeServlet?time="+new Date().getTime();
42.     }
43. </script>

主要修改在30-53行之间 对图片src进行修改，使得通过servlet生成，并对看不清超链接设置id”changeImg”，然后使用getElementId查护照这个超链接，绑定单击事件，使得再一次请求时更换图片，但是不能单一请求/brand-demo/checkCodeServlet，因为图片路径 已经载入缓存，只需要加一个参数使用时间，确保不重复。

#### 用户注册--校验验证码

- 判断程序生成的验证码和用户输入的验证码是否一致，如果不一样，则阻止注册
- 验证码图片访问和提交注册表单是两次请求，所以要将程序生成的验证码存入session中

CheckCodeServlet.java

1.  _//存入session_
2.  HttpSession session = request.getSession();
3.  session.setAttribute("checkCodeGen", checkCode);

在CheckCodeServlet中加入存入session行为

RegisterServlet.java

1.  _//获取用户输入的验证码_
2.  String checkCode = request.getParameter("checkCode");

3.  _//程序生成的验证码，从Session中获取_
4.  HttpSession session = request.getSession();
5.  String checkCodeGen = (String) session.getAttribute("checkCodeGen");

6.  _//比对_
7.  if(!checkCodeGen.equalsIgnoreCase(checkCode)){
8. _//不允许注册_
9. request.setAttribute("register_msg","验证码错误");
10. request.getRequestDispatcher("/register.jsp").forward(request,response);
11. return;
12. }

在RegisterServlet中获取用户输入的验证码，并获取Session中存储的CheckCodeServlet中存入的生成验证码，并进行比对

## Filter & Listener

- 概念：Filter表示过滤器，是JavaWeb三大组件（Servlet，Filter，Listener）之一
- 过滤器可以把资源的请求拦截下来，从而实现一些特殊的功能
- 过滤器一般完成一些通用的操作，比如权限控制，统一编码处理，敏感字符处理等等...

### Filter

#### Filter快速入门

（类似Servlet）

1.  定义类，实现Filter接口，并重写其所有方法
2.  配置Filter拦截资源的路径：在类上定义@WebFilter注解
3.  在doFilter方法中输出一句话，并放行
4.  @WebFilter("/\*")
5.  public class FilterDemo implements Filter {
6.      @Override
7.      public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {

8.          _//1. 放行前，对 request数据进行处理_
9.         System.out.println("1.FilterDemo...");

10.         _//放行_
11.         chain.doFilter(request,response);
12.         _//2. 放行后，对Response 数据进行处理_
13.         System.out.println("5.FilterDemo...");
14.     }

15.     @Override
16.    public void init(FilterConfig filterConfig) throws ServletException {}

17.     @Override
18.     public void destroy() {}

#### Filter执行流程

- Filter：执行放行前逻辑-放行-访问资源-执行放行后逻辑
- 放行后访问对应资源，资源访问完成后还会回到Filter中
- 回到Filter会执行放行后逻辑而不是从头逻辑

#### Filter使用细节

1.  Filter拦截路径配置

@WebFilter("/\*")

public class FilterDemo

- 拦截具体资源：/index.jsp：只有访问index.jsp时才会被拦截
- 目录拦截：/user/\*：访问/user下的所有资源，都会被拦截
- 后缀名拦截：\*.jsp：访问后缀名为jsp的资源，都会被拦截
- 拦截所有：/\*：访问所有资源，都会被拦截

1.  过滤器链

- 一个Web应用，可以配置多个过滤器，则多个过滤器成为过滤器链
- 执行流程：

请求-Filter1放行前逻辑-Filter1放行-Filter2放行前逻辑-Filter2放行-Filter2放行后逻辑-Filter1放行后逻辑-响应

- 注解配置Filter，优先级按照过滤器类名（字符串）的自然排序

#### 案例

需求：访问服务器资源时，需要先进行登录验证，如果没有登录，则自动跳转到登录页面

新建LoginFilter实现登录验证的过滤

1.  _/\*\*_
2.   \* 登录验证过滤器
3.   \*/
4.  @WebFilter("/\*")
5.  public class LoginFilter implements Filter {
6.      @Override
7.    public void init(FilterConfig filterConfig) throws ServletException {}

8.      @Override
9.     public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {

10.         HttpServletRequest req = (HttpServletRequest) request;

11.         _//判断session中是否有user_
12.         HttpSession session = req.getSession();
13.         Object user = session.getAttribute("user");

14.         if(user != null){
15.             _//登录过了_
16.             _//放行_
17.             chain.doFilter(request,response);
18.         }else{

19.             req.setAttribute("login_msg","您尚未登录");
20.             req.getRequestDispatcher("/login.jsp").forward(req,response);
21.         }

22.         _//放行_
23.         chain.doFilter(request,response);

24.     }

25.     @Override
26.     public void destroy() {}
27. }

通过判断是否有session中是否有user，如果没有则返回到login.jsp

- 问题

如果 @WebFilter("/\*")，与登录和注册相关资源，如css，img，注册页面同样被拦截，但是需求是只对没有登录的进行拦截

- 解决

添加一个判断：判断访问的是不是登录相关资源

是：放行

不是：进行登录验证

loginFilter.java

1.          _//判断访问资源路径是否和注册登录相关_
2.          String\[\] urls = {"/login.jsp","/loginServlet","/imgs/","/css/","/checkCodeServlet/","/register.jsp","/registerServlet"};
3.          _//获取当前访问的资源路径_
4.          String url = req.getRequestURL().toString();
5.          for (String u : urls) {
6.              if(url.contains(u)){
7.                  _//访问的是注册登录相关的资源，放行_
8.                  chain.doFilter(request,response);
9.                  return;
10.             }
11.         }

### Listener

- Listener监听器，是JavaWeb三大组件（Servlet，Filter，Listener）之一
- 监听器可以监听在application，session，request三个对象创建，销毁或者往其中添加修改删除属性是自动执行代码的功能组件

#### Listener分类

JavaWeb中提供了8个监听器

- ServletContext监听：

ServletContextListener：用于对ServletContext对象进行监听（创建销毁）

ServletContextAttributeListener：用于对ServletContext对象中属性的监听（增删改属性）

- Session监听：

HttpSessionListener：对Session对象的整体状态的监听（创建，销毁）

HttpSessionAttributeListener：对Session对象中的属性监听（增删改属性）

HttpSessionBindingListener：监听对象与Session的绑定和解除

- Request监听：

ServletRequestListener：对Request对象进行监听（创建，销毁）

ServletRequestAttributeListener：对Request对象中的属性的监听（增删改属性）

#### ServletContextListener使用

1.  定义类，实现ServletContextListener接口
2.  在类上添加@WebListener注解
3.  @WebListener
4.  public class ContextLoaderListener implements ServletContextListener {

5.      _/\*\*_
6.       \* ServletContext对象被创建，整个web应用发布成功
7.       \* @param servletContextEvent
8.       \*/
9.     @Override
10.     public void contextInitialized(ServletContextEvent servletContextEvent) {}

11.     _/\*\*_
12.      \* ServletContext对象被销毁，整个web应用卸载
13.      \* @param servletContextEvent
14.      \*/
15.     @Override
16.     public void contextDestroyed(ServletContextEvent servletContextEvent) {}
17. }



## Vue

- VUE是一套前端框架，免除原生JavaScript中的_[dom](#_DOM)_操作
- 在上一节AJAX案例中的dom操作：

1.  _// 将表单数据转为json_
2.          var formData = {
3.              brandName:"",
4.              companyName:"",
5.              ordered:"",
6.              description:"",
7.              status:"",
8.          };
9.          _// 获取表单数据_
10.         let brandName = document.getElementById("brandName").value;
11.         _// 设置数据_
12.         formData.brandName = brandName;

13.         _// 获取表单数据_
14.         let companyName = document.getElementById("companyName").value;
15.         _// 设置数据_
16.         formData.companyName = companyName;

17.         _// 获取表单数据_
18.         let ordered = document.getElementById("ordered").value;
19.         _// 设置数据_
20.         formData.ordered = ordered;

21.         _// 获取表单数据_
22.         let description = document.getElementById("description").value;
23.         _// 设置数据_
24.         formData.description = description;

25.         let status = document.getElementsByName("status");
26.         for (let i = 0; i < status.length; i++) {
27.             if(status\[i\].checked){
28.                 _//_
29.                 formData.status = status\[i\].value ;
30.             }
31.         }

- 基于MVVM（Model-View-ViewModel）思想，实现数据的双向绑定，将编程的关注点放在数据上，当ViewModel中的数据发生变化时，数据绑定会自动更新View中绑定到这些数据的部分，反之亦然

### Vue快速入门

1.  新建HTML页面，引入Vue.js文件

<script src="js/vue.js"></script>

1.  在JS代码区域，创建Vue核心对象，进行数据绑定
2.  new Vue({
3.          el:"#app",
4.          data(){
5.              return {
6.                  username:""
7.              }
8.          }
9.      });

el：elemet用来指定vue的作用范围，这里使用id选择器，选定id=app

1.  编写视图
2.  <div id="app">

3.      <input v-model="username">
4.      _<!--插值表达式-->_
5.      {{username}}

6.  </div>

插值表达式，取出模型数据

### Vue常用指令

指令：HTML标签上带有v-前缀的特殊属性，不同指令具有不同翻译

1.  v-bind：为HTML标签绑定属性值，如设置href，css样式等

讲话书写：直接在href前加 ：即可

1.  <div id="app">

2.     <a v-bind:href="url">点击一下</a>

3.      <a :href="url">点击一下</a>

4.      <input v-model="url">

5. </div>

6. <script src="js/vue.js"></script>
7. <script>

8.     _//1. 创建Vue核心对象_
9.     new Vue({
10.         el:"#app",
11.         data(){
12.             return {
13.                 username:"",
14.                 url:"https://www.baidu.com"
15.             }
16.         }
17.     });

18. </script>

19.  v-model：在表单元素上创建双向数据绑定
20.  v-on：为HTML标签绑定事件

简化书写：@

1.  <div id="app">

2.      <input type="button" value="一个按钮" v-on:click="show()"><br>
3.      <input type="button" value="一个按钮" @click="show()">

4.  </div>

5. <script src="js/vue.js"></script>
6. <script>

7.     _//1. 创建Vue核心对象_
8.     new Vue({
9.         el:"#app",
10.         data(){
11.             return {
12.                 username:"",
13.                 url:"https://www.baidu.com"
14.             }
15.         },
16.         methods:{
17.             show(){
18.                 alert("我被点了...");
19.             }
20.         }
21.     });

22. </script>

23.  v-if与v-show

实现效果一样，但底层渲染不一致

If条件性地渲染某元素，判断为true时渲染，否则不渲染

Show根据条件展示莫元素，区别在于切换的是display属性的值

1.  <div id="app">

2.      <div v-if="count == 3">div1</div>
3.      <div v-else-if="count == 4">div2</div>
4.      <div v-else>div3</div>
5.      <hr>
6.      <div v-show="count == 3">div v-show</div>
7.      <br>

8.     <input v-model="count">

9. </div>

10. <script src="js/vue.js"></script>
11. <script>

12.     _//1. 创建Vue核心对象_
13.     new Vue({
14.         el:"#app",
15.         data(){
16.             return {
17.                 username:"",
18.                 url:"https://www.baidu.com",
19.                 count:3
20.             }
21.         },
22.         methods:{
23.             show(){
24.                 alert("我被点了...");
25.             }
26.         }
27.     });

28. </script>

29.  v-for

列表渲染，遍历容器的元素和对象的属性

1.  <div id="app">

2.      <div v-for="addr in addrs">
3.          {{addr}} <br>
4.      </div>

5.      <hr>
6.      <div v-for="(addr,i) in addrs">
7.          {{i+1}}--{{addr}} <br>
8.     </div>
9. </div>

10. <script src="js/vue.js"></script>
11. <script>

12.     _//1. 创建Vue核心对象_
13.     new Vue({
14.         el:"#app",
15.         data(){
16.             return {
17.                 username:"",
18.                 url:"https://www.baidu.com",
19.                 count:3,
20.                 addrs:\["北京","上海","西安"\]
21.             }
22.         },
23.         methods:{
24.             show(){
25.                 alert("我被点了...");
26.             }
27.         }
28.     });

29. </script>

i表示索引，从0开始

### Vue生命周期

生命周期的八个阶段：每触发一个生命周期事件，会自动执行一个生命周期方法

- BeforeCreate 创建前
- Created 创建后
- beforeMount 载入前
- Mounted 挂载完成，Vue初始化完成，HTML页面渲染完成，发送异步请求加载数据

1.      _//1. 创建Vue核心对象_
2.      new Vue({
3.          el:"#app",
4.          data(){
5.              return {
6.                  username:"",
7.                  url:"https://www.baidu.com",
8.                  count:3,
9.                  addrs:\["北京","上海","西安"\]
10.             }
11.         },
12.         methods:{
13.             show(){
14.                 alert("我被点了...");
15.             }
16.         },
17.         _/\*mounted:function () {_

18.         }\*/
19.         mounted(){
20.             alert("加载完成...")
21.         }
22.     });

23. </script>

在这之前使用window.unload来实现页面加载完成，发送异步请求，现在可以使用mounted来代替

- beforeUpdate 更新前
- Updated 更新后
- beforeDestory 销毁前
- Destoryed 销毁后

### 案例

需求：使用Vue简化品牌列表数据查询和添加功能

##### 查询所有

brand.html

1.  <div id="app">
2.      <a href="addBrand.html"><input type="button" value="新增"></a><br>
3.      <hr>
4.      <table id="brandTable" border="1" cellspacing="0" width="100%">
5.          <tr>
6.              <th>序号</th>
7.              <th>品牌名称</th>
8.              <th>企业名称</th>
9.              <th>排序</th>
10.             <th>品牌介绍</th>
11.             <th>状态</th>
12.             <th>操作</th>
13.         </tr>

14.         _<!--_
15.             使用v-for遍历tr
16.         -->

17.         <tr v-for="(brand,i) in brands" align="center">
18.             <td>{{i + 1}}</td>
19.             <td>{{brand.brandName}}</td>
20.             <td>{{brand.companyName}}</td>
21.             <td>{{brand.ordered}}</td>
22.             <td>{{brand.description}}</td>
23.             <td>{{brand.statusStr}}</td>
24.             <td><a href="#">修改</a> <a href="#">删除</a></td>
25.         </tr>

26.     </table>
27. </div>
28. <script src="js/axios-0.18.0.js"></script>
29. <script src="js/vue.js"></script>

30. <script>

31.     new Vue({
32.         el: "#app",
33.         data(){
34.             return{
35.                 brands:\[\]
36.             }
37.         },
38.         mounted(){
39.             _// 页面加载完成后，发送异步请求，查询数据_
40.             var \_this = this;
41.             axios({
42.                 method:"get",
43.                 url:"http://localhost:8080/brand-demo/selectAllServlet"
44.             }).then(function (resp) {
45.                 \_this.brands = resp.data;
46.             })
47.         }
48.     })
49. </script>

el指定id -div div包裹整个页面范围 设置vue指定作用范围

Mounted指定一个函数，页面加载完成后，发送异步请求，查询数据

使用v-for完成遍历tr，并且使用插值表达式来取数据，展示到对应的表格中

1.      new Vue({
2.          el: "#app",
3.          data(){
4.              return{
5.                  brands:\[\]
6.              }
7.          },
8.          mounted(){
9.              _// 页面加载完成后，发送异步请求，查询数据_
10.             _// var \_this = this;_
11.             axios({
12.                 method:"get",
13.                 url:"http://localhost:8080/brand-demo/selectAllServlet"
14.             }).then(function (resp) {
15.                 this.brands = resp.data;
16.             })
17.         }
18.     })

在发送axios请求后后绑定一个回调函数，返回resp.data（返回的数据，通常为.json文件）响应回来的集合brands，brands作为一个局部变量要给到v-for使用，需要将brands变成一个模型，使用this.brands给模型中brands赋值，this指定当前vue对象，但现在使用axios，现在的this指window对象，不发指向vue，所以加入一个变量_this使得可以传参

##### 查询所有

1.  <div id="app">
2.      <h3>添加品牌</h3>
3.      <form action="" method="post">
4.          品牌名称：<input id="brandName" v-model="brand.brandName" name="brandName"><br>
5.          企业名称：<input id="companyName" v-model="brand.companyName" name="companyName"><br>
6.          排序：<input id="ordered" v-model="brand.ordered" name="ordered"><br>
7.          描述信息：<textarea rows="5" cols="20" id="description" v-model="brand.description" name="description"></textarea><br>
8.          状态：
9.          <input type="radio" name="status" v-model="brand.status" value="0">禁用
10.         <input type="radio" name="status" v-model="brand.status" value="1">启用<br>

11.         <input type="button" id="btn" @click="submitForm" value="提交">
12.     </form>
13. </div>
14. <script src="js/axios-0.18.0.js"></script>

15. <script src="js/vue.js"></script>

16. <script>

17.     new Vue({
18.         el: "#app",
19.         data(){
20.             return {
21.                 brand:{}
22.             }
23.         },
24.         methods:{
25.             submitForm(){
26.                 _// 发送ajax请求，添加_
27.                 var \_this = this;
28.                 axios({
29.                     method:"post",
30.                     url:"http://localhost:8080/brand-demo/addServlet",
31.                     data:\_this.brand
32.                 }).then(function (resp) {
33.                     _// 判断响应数据是否为 success_
34.                     if(resp.data == "success"){
35.                         location.href = "http://localhost:8080/brand-demo/brand.html";
36.                     }
37.                 })

38.             }
39.         }
40.     })
41. </script>

42.  _//1. 给按钮绑定单击事件_
43.      document.getElementById("btn").onclick = function () {
44.          _// 将表单数据转为json_
45.          var formData = {
46.              brandName:"",
47.              companyName:"",
48.              ordered:"",
49.              description:"",
50.              status:"",
51.         };

按钮上绑定单击事件@click 在vue中定义method submitForm 在submitForm方法中发送异步数据，请求数据，在之前的案例中data是formdata，这里在vue框架下，应该有一个模型来绑定data，所以定义一个data() 返回brand，axios中的data是通过data（）传入，与查询所有一致，也用_this传入，brand中的数据使用v-model的双向数据绑定。

## Element UI

- 一套基于Vue的网站组件库，用于快速构建网页
- 组件：组成网页的构件，例如超链接，按钮，图片，表格等等

### Element快速入门

1.  引入Element的css，js文件和Vue.js
2.  <script src="js/vue.js"></script>
3.  <script src="element-ui/lib/index.js"></script>
4.  <link rel="stylesheet" href="element-ui/lib/theme-chalk/index.css">

5.  创建Vue核心对象
6.  <script>
7.      new Vue({
8.          el:"#app"
9.      })

10.  官网复制Element组件代码

_[Element](https://element.eleme.cn/"%20\l%20"/zh-CN)_

### Element布局

1.  layout布局：通过基础的24分栏，迅速简便地创建布局
2.  Contaioner布局容器：用于布局的容器组件，方便快速搭建页面的基本结构

### Element组件

_[组件 | Element](https://element.eleme.cn/"%20\l%20"/zh-CN/component/installation)_


