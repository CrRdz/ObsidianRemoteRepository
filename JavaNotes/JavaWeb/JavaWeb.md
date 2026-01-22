


# SSM

Spring +SpringMVC +Mybatis

Dao=Mapper

domain=pojo

git clone git@github.com:CrRdz/Learning_SSM.git


## SpringMVC

SpringMVC技术与Servlet技术功能等同，均属于web（表现层）层开发技术

### SpringMVC简介

@ResponseBody注解用于将控制器方法返回的对象转换为JSON或XML数据并直接写入HTTP响应体，常用于异步请求处理。@RequestBody则用于从前端请求中读取JSON或XML数据，并将其绑定到方法参数上。

页面————后端服务器

HTML 表现层（此前使用Servlet，现在使用SpringMVC替代）

CSS 业务层

VUE 数据层（Mybatis）

ElementUI

SpringMVC是一种基于Java实现MVC模型的轻量级Web框架

优点：使用简单，开发便捷，灵活性强

#### SpringMVC入门案例

1.  使用SpringMVC技术需要先导入SpringMVC与Servlet坐标
2.      <dependency>
3.        <groupId>javax.servlet</groupId>
4.        <artifactId>javax.servlet-api</artifactId>
5.        <version>3.1.0</version>
6.        <scope>provided</scope>ws
7.      </dependency>
8.      <dependency>
9.        <groupId>org.springframework</groupId>
10.       <artifactId>spring-webmvc</artifactId>
11.       <version>5.2.10.RELEASE</version>
12.     </dependency>

13.  创建SpringMVC控制器类（同Servlet）
14.  _//定义表现层控制器bean_
15.  @Controller
16.  public class UserController {

17.      _//设置映射路径为/save，即外部访问路径_
18.      @RequestMapping("/save")
19.      _//设置当前操作返回结果为指定json数据（本质上是一个字符串信息）_
20.      @ResponseBody
21.     public String save(){
22.         System.out.println("user save ...");
23.         return "{'info':'springmvc'}";
24.     }

25.     _//设置映射路径为/delete，即外部访问路径_
26.     @RequestMapping("/delete")
27.     @ResponseBody
28.     public String delete(){
29.         System.out.println("user save ...");
30.         return "{'info':'springmvc'}";
31.     }
32. }

33.  初始化SpringMVC环境（同Spring环境），设定SpringMVC加载Controller对应的bean
34.  _//springmvc配置类，本质上还是一个spring配置类_
35.  @Configuration
36.  @ComponentScan("com.itheima.controller")
37.  public class SpringMvcConfig {
38.  }

39.  初始化Servlet容器（Tomcat），加载SpringMVC环境并设置SpringMVC技术处理的请求
40.  _//web容器配置类_
41.  public class ServletContainersInitConfig extends AbstractDispatcherServletInitializer {
42.      _//加载springmvc配置类，产生springmvc容器（本质还是spring容器）_
43.      protected WebApplicationContext createServletApplicationContext() {
44.          _//初始化WebApplicationContext对象_
45.          AnnotationConfigWebApplicationContext ctx = new AnnotationConfigWebApplicationContext();
46.          _//加载指定配置类_
47.          ctx.register(SpringMvcConfig.class);
48.         return ctx;
49.     }

50.     _//设置由springmvc控制器处理的请求映射路径 哪些请求归属SpringMVC处理_
51.     protected String\[\] getServletMappings() {
52.         return new String\[\]{"/"};
53.     }

54.     _//加载spring配置类_
55.     protected WebApplicationContext createRootApplicationContext() {
56.         return null;
57.     }
58. }

@Controller

类注解

SpringMVC控制器定义上方

设定SpringMVC的核心控制器bean

@ResponseBody

方法注解

SpringMVC控制器方法定义上方

设置当前控制器方法响应内容为当前返回值，无需解析

SpringMVC开发总结（1+N）

- 一次性工作

创建工程，设置服务器，加载工程

导入坐标

创建Web容器启动类，加载SpringMVC配置，并设置SpringMVC请求拦截路径

SpringMVC核心配置类（设置配置类，扫描Controller包，加载Controller控制器bean）

- 多次工作

定义处理请求的控制器类

定义处理请求方法，并配置映射路径（@RequestMapping）与返回json数据（@ResponseBody）

#### 入门案例工作流程

启动服务器初始化过程：

1.  服务器启动，执行ServletContainerInitConfig类，初始化web容器
2.  执行createServletAplicationContext方法，创建WebApplicationContext对象
3.  加载SpringMvcConfig
4.  执行@ConponentScan加载对应的bean
5.  加载UserController，每个@RequestMapping的名称对应一个具体方法
6.  执行getServletMappings方法，定义所有的请求都通过SpringMVC

单次请求过程

1.  发送请求localhost/save
2.  Web容器发现所有请求都经过SpringMVC，将请求交给SpringMVC处理
3.  解析请求路径/save
4.  由/save匹配执行对应的方法save（）
5.  执行save（）
6.  检测到@ResponseBody直接将save（）方法的返回值作为响应请求体返回给请求方

#### Bean加载控制

因为功能不同，怎么避免Spring错误地加载到Controller（SpringMVC）的bean

\--加载Spring控制的bean的时候，排除掉SpringMVC控制的bean

两种方式：扫描指定包/过滤

1.  @Configuration
2.  _//@ComponentScan({"com.itheima.service","com.itheima.dao"})_

3.  _//设置spring配置类加载bean时的过滤规则，当前要求排除掉表现层对应的bean_
4.  _//excludeFilters属性：设置扫描加载bean时，排除的过滤规则_
5.  _//type属性：设置排除规则，当前使用按照bean定义时的注解类型进行排除_
6.  _//classes属性：设置排除的具体注解类，当前设置排除@Controller定义的bean_
7.  @ComponentScan(value="com.itheima",
8.      excludeFilters = @ComponentScan.Filter(
9.         type = FilterType.ANNOTATION,
10.         classes = Controller.class
11.     )
12. )
13. public class SpringConfig {
14. }

ANNOTATION//按照注解过滤

ASSIGNABLE_TYPE //按照类型过滤

ASPECTJ//按照ASPECTJ表达式过滤

REGEX//按照正则表达式过滤

CUSTOM//按照自定义的过滤规则过滤

简化开发

1.  _//web配置类简化开发，仅设置配置类类名即可_
2.  public class ServletContainersInitConfig extends AbstractAnnotationConfigDispatcherServletInitializer {

3.      protected Class<?>\[\] getRootConfigClasses() {
4.          return new Class\[\]{SpringConfig.class};
5.      }

6.      protected Class<?>\[\] getServletConfigClasses() {
7.          return new Class\[\]{SpringMvcConfig.class};
8.     }

9.     protected String\[\] getServletMappings() {
10.         return new String\[\]{"/"};
11.     }
12. }

修改继承的类，简化配置

#### PostMan

功能强大的网页调试与发送网页HTTP请求的Chrome插件

作用：常用于接口测试

### 请求与响应

#### 请求映射路径

团队多人开发，每人设置不同的请求路径，冲突问题解决——设置模块名作为请求路径前缀

1.  @Controller
2.  _//类上方配置的请求映射与方法上面配置的请求映射连接在一起，形成完整的请求映射路径_
3.  @RequestMapping("/user")
4.  public class UserController {
5.      _//请求路径映射_
6.      @RequestMapping("/save")
7.      @ResponseBody
8.      public String save(){
9.          System.out.println("user save ...");
10.         return "{'module':'user save'}";
11.     }
12. }

@RequestMapping

方法注解/类注解

类上方配置的请求映射与方法上面配置的请求映射连接在一起，形成完整的请求映射路径

#### 请求参数

##### 普通参数传递

请求参数与形参名称相同

1.  _//普通参数：请求参数与形参名称对应即可完成参数传递_
2.      @RequestMapping("/commonParam")
3.      @ResponseBody
4.      public String commonParam(String name ,int age){
5.          System.out.println("普通参数传递 name ==> "+name);
6.          System.out.println("普通参数传递 age ==> "+age);
7.          return "{'module':'common param'}";
8.      }

请求参数与形参名称不同

1.      _//普通参数：请求参数名与形参名不同时，使用@RequestParam注解关联请求参数名称与形参名称之间的关系_
2.      @RequestMapping("/commonParamDifferentName")
3.      @ResponseBody
4.      public String commonParamDifferentName(@RequestParam("name") String userName , int age){
5.          System.out.println("普通参数传递 userName ==> "+userName);
6.          System.out.println("普通参数传递 age ==> "+age);
7.          return "{'module':'common param different name'}";
8.      }

@RequestParam("name") String userName使用这个来绑定请求参数与形参

GET请求传参

普通参数：

url地址传参，地址参数名与形参变量名相同，定义形参即可接受参数

POST请求

普通参数：

form表单post请求传参，表单参数名与形参变量名相同，定义形参即可接受参数

Postman页

Post请求中输入中文出现乱码处理

ServletContainerInitConfig

1.      _//乱码处理_
2.      @Override
3.      protected Filter\[\] getServletFilters() {
4.          CharacterEncodingFilter filter = new CharacterEncodingFilter();
5.          filter.setEncoding("UTF-8");
6.          return new Filter\[\]{filter};
7.      }

##### 其余四种参数传递

1.  POJO传参

请求参数与形参对象属性名相同，定义POJO类型形参即可接受参数

1.  public class User {
2.      private String name;
3.      private int age;
4.      private Address address;
5.  ...
6.  }

请求参数与形参对象中属性对应

1.  _//POJO参数：请求参数与形参对象中的属性对应即可完成参数传递_
2.      @RequestMapping("/pojoParam")
3.      @ResponseBody
4.      public String pojoParam(User user){
5.          System.out.println("pojo参数传递 user ==> "+user);
6.          return "{'module':'pojo param'}";
7.      }
8.  嵌套POJO传参

POJO中包含POJO对象

1.      _//嵌套POJO参数：嵌套属性按照层次结构设定名称即可完成参数传递_
2.      @RequestMapping("/pojoContainPojoParam")
3.      @ResponseBody
4.      public String pojoContainPojoParam(User user){
5.          System.out.println("pojo嵌套pojo参数传递 user ==> "+user);
6.          return "{'module':'pojo contain pojo param'}";
7.      }
8.  数组传参
9.      _//数组参数：同名请求参数可以直接映射到对应名称的形参数组对象中_
10.     @RequestMapping("/arrayParam")
11.     @ResponseBody
12.     public String arrayParam(String\[\] likes){
13.         System.out.println("数组传递 likes ==> "+ Arrays.toString(likes));
14.         return "{'module':'array param'}";
15.     }
16. 集合传参
17.     _//集合参数：同名请求参数可以使用@RequestParam注解映射到对应名称的集合对象中作为数据_
18.     @RequestMapping("/listParam")
19.     @ResponseBody
20.     public String listParam(@RequestParam List<String> likes){
21.         System.out.println("集合参数传递 likes ==> "+ likes);
22.         return "{'module':'list param'}";
23.     }

##### json数据传递参数（接收请求中的json数据）

Step1：导入json依赖

1.      <dependency>
2.        <groupId>com.fasterxml.jackson.core</groupId>
3.        <artifactId>jackson-databind</artifactId>
4.        <version>2.9.0</version>
5.      </dependency>

Step1.5：Postman设置发json数据

Step2：开启由json对象转换为对象功能

1.  @Configuration
2.  @ComponentScan("com.itheima.controller")
3.  _//开启json数据类型自动转换_
4.  @EnableWebMvc
5.  public class SpringMvcConfig {
6.  }

Step3：设置接收json数据

集合参数：json格式

1.      _//集合参数：json格式_
2.      _//1.开启json数据格式的自动转换，在配置类中开启@EnableWebMvc_
3.      _//2.使用@RequestBody注解将外部传递的json数组数据映射到形参的保存实体类对象的集合对象中，要求属性名称一一对应_
4.      @RequestMapping("/listPojoParamForJson")
5.      @ResponseBody
6.      public String listPojoParamForJson(@RequestBody List<User> likes){
7.          System.out.println("list pojo(json)参数传递 list ==> "+likes);
8.          return "{'module':'list pojo for json param'}";
9.      }

Json现在不在requestParam中了，在请求体中

Pojo参数：json格式

1.      _//POJO参数：json格式_
2.      _//1.开启json数据格式的自动转换，在配置类中开启@EnableWebMvc_
3.      _//2.使用@RequestBody注解将外部传递的json数据映射到形参的实体类对象中，要求属性名称一一对应_
4.      @RequestMapping("/pojoParamForJson")
5.      @ResponseBody
6.      public String pojoParamForJson(@RequestBody User user){
7.          System.out.println("pojo(json)参数传递 user ==> "+user);
8.          return "{'module':'pojo for json param'}";
9.      }

Pojo参数：json数组

1.      _//集合参数：json格式_
2.      _//1.开启json数据格式的自动转换，在配置类中开启@EnableWebMvc_
3.      _//2.使用@RequestBody注解将外部传递的json数组数据映射到形参的保存实体类对象的集合对象中，要求属性名称一一对应_
4.      @RequestMapping("/listPojoParamForJson")
5.      @ResponseBody
6.      public String listPojoParamForJson(@RequestBody List<User> list){
7.          System.out.println("list pojo(json)参数传递 list ==> "+list);
8.          return "{'module':'list pojo for json param'}";
9.      }

后期开发中，发送json格式数据为主，@RequestBody应用较广

如果发送非json格式数据，选用@RequestParam接收请求参数

##### 日期类型参数传递

1.      _//日期参数_
2.      _//使用@DateTimeFormat注解设置日期类型数据格式，默认格式yyyy/MM/dd_
3.      @RequestMapping("/dataParam")
4.      @ResponseBody
5.      public String dataParam(Date date,
6.                              @DateTimeFormat(pattern="yyyy-MM-dd") Date date1,
7.                              @DateTimeFormat(pattern="yyyy/MM/dd HH:mm:ss") Date date2）{
8.          System.out.println("参数传递 date ==> "+date);
9.          System.out.println("参数传递 date1(yyyy-MM-dd) ==> "+date1);
10.         System.out.println("参数传递 date2(yyyy/MM/dd HH:mm:ss) ==> "+date2);
11.         return "{'module':'data param'}";
12.     }

底层逻辑实现：Converter接口

@EnableWebMvc功能之一：根据类型匹配对应的类型转换器

#### 响应

##### 响应页面/文本数据

1.  _//响应页面/跳转页面_
2.      _//返回值为String类型，设置返回值为页面名称，即可实现页面跳转_
3.      @RequestMapping("/toJumpPage")
4.      public String toJumpPage(){
5.          System.out.println("跳转页面");
6.          return "page.jsp";
7.      }

8.      _//响应文本数据_
9.     _//返回值为String类型，设置返回值为任意字符串信息，即可实现返回指定字符串信息，需要依赖@ResponseBody注解_
10.     @RequestMapping("/toText")
11.     @ResponseBody
12.     public String toText(){
13.         System.out.println("返回纯文本数据");
14.         return "response text";
15.     }

16.  响应pojo对象
17.      _//响应POJO对象_
18.      _//返回值为实体类对象，设置返回值为实体类类型，即可实现返回对应对象的json数据，需要依赖@ResponseBody注解和@EnableWebMvc注解_
19.      @RequestMapping("/toJsonPOJO")
20.      @ResponseBody
21.      public User toJsonPOJO(){
22.          System.out.println("返回json对象数据");
23.          User user = new User();
24.          user.setName("itcast");
25.         user.setAge(15);
26.         return user;
27.     }

@ResponseBody

类型：方法注解

位置：SpringMVC控制器定义上方

作用：设置当前控制器返回值作为响应体

通过HttpMessageConverter接口（类型转换器）实现

### REST风格

#### REST简介

Representational State Transfer 表现形式状态转换

- 传统风格资源描述形式：

http://localhost/user/getById?id=1

http://localhost/user/saveUser

REST风格描述形式：

http://localhost/user/1

http://localhost/user

- 优点：

隐藏资源的访问行为，无法通过地址得知对资源是何种操作

书写简化

- 按照REST风格访问资源时使用行为动作区分你对资源进行了何种操作

http://localhost/user 查询全部用户信息 GET（查询）

http://localhost/user/1 查询指定用户信息 GET（查询）

http://localhost/user 添加用户信息 POST（新增/保存）

http://localhost/user 修改用户信息 PUT（修改/更新）

http://localhost/user/1 删除用户信息 DELETE（删除）

上述行为是约定行为，约定不是规范，可以打破，所以成为REST风格，而不是规范

描述模块的名称通常使用复数，也就是加s的格式描述，表示此类资源，而非单个资源

根据REST风格对资源进行访问成为RESTful

#### RESTful入门案例

保存

1.      _//设置当前请求方法为POST，表示REST风格中的添加操作_
2.      @RequestMapping(value = "/users",method = RequestMethod.POST)
3.      @ResponseBody
4.      public String save(){
5.          System.out.println("user save...");
6.          return "{'module':'user save'}";
7.      }    

使用method配置

删除

1.  _//设置当前请求方法为DELETE，表示REST风格中的删除操作_
2.      _//@PathVariable注解用于设置路径变量（路径参数），要求路径上设置对应的占位符，并且占位符名称与方法形参名称相同_
3.      @RequestMapping(value = "/users/{id}",method = RequestMethod.DELETE)
4.      @ResponseBody
5.      public String delete(@PathVariable Integer id){
6.          System.out.println("user delete..." + id);
7.          return "{'module':'user delete'}";
8.      }

更新

1.  _//设置当前请求方法为PUT，表示REST风格中的修改操作_
2.      @RequestMapping(value = "/users",method = RequestMethod.PUT)
3.      @ResponseBody
4.      public String update(@RequestBody User user){
5.          System.out.println("user update..."+user);
6.          return "{'module':'user update'}";
7.      }

查询指定

1.   _//设置当前请求方法为GET，表示REST风格中的查询操作_
2.      _//@PathVariable注解用于设置路径变量（路径参数），要求路径上设置对应的占位符，并且占位符名称与方法形参名称相同_
3.      @RequestMapping(value = "/users/{id}" ,method = RequestMethod.GET)
4.      @ResponseBody
5.      public String getById(@PathVariable Integer id){
6.          System.out.println("user getById..."+id);
7.          return "{'module':'user getById'}";
8.      }

查询全部

1.      _//设置当前请求方法为GET，表示REST风格中的查询操作_
2.      @RequestMapping(value = "/users",method = RequestMethod.GET)
3.      @ResponseBody
4.      public String getAll(){
5.          System.out.println("user getAll...");
6.          return "{'module':'user getAll'}";
7.      }

流程：

设定http请求动作

设定请求参数（路径变量）@PathVariable

@RequestParam用于接收url地址传参或表单传参

@RequestBody用于接收json数据

@PathVariable用于接收路径参数，使用{参数名称}描述路径参数

在开发中，发送请求参数超过1个时，以json格式为主，@RequestBody应用较广，当参数数量较少时，可以采用@PathVariable接受请求路径变量，通常用于传递id值，通常偏向于将多个需要提交的数据封装成pojo，然后通过json串的形式传递

#### REST快速开发（简化开发）

1.  _//@Controller_
2.  _//@ResponseBody配置在类上可以简化配置，表示设置当前每个方法的返回值都作为响应体_
3.  _//@ResponseBody_
4.  @RestController     
5.  _//使用@RestController注解替换@Controller与@ResponseBody注解，简化书写_
6.  @RequestMapping("/books")
7.  public class BookController {

8.  _//    @RequestMapping( method = RequestMethod.POST)_
9.     @PostMapping        
10. _//使用@PostMapping简化Post请求方法对应的映射配置_
11.     public String save(@RequestBody Book book){
12.         System.out.println("book save..." + book);
13.         return "{'module':'book save'}";
14.     }

15. _//    @RequestMapping(value = "/{id}" ,method = RequestMethod.DELETE)_
16.     @DeleteMapping("/{id}")     
17. _//使用@DeleteMapping简化DELETE请求方法对应的映射配置_
18.     public String delete(@PathVariable Integer id){
19.         System.out.println("book delete..." + id);
20.         return "{'module':'book delete'}";
21.     }

22. _//    @RequestMapping(method = RequestMethod.PUT)_
23.     @PutMapping         
24. _//使用@PutMapping简化Put请求方法对应的映射配置_
25.     public String update(@RequestBody Book book){
26.         System.out.println("book update..."+book);
27.         return "{'module':'book update'}";
28.     }

29. _//    @RequestMapping(value = "/{id}" ,method = RequestMethod.GET)_
30.     @GetMapping("/{id}")    
31. _//使用@GetMapping简化GET请求方法对应的映射配置_
32.     public String getById(@PathVariable Integer id){
33.         System.out.println("book getById..."+id);
34.         return "{'module':'book getById'}";
35.     }

36. _//    @RequestMapping(method = RequestMethod.GET)_
37.     @GetMapping             
38. _//使用@GetMapping简化GET请求方法对应的映射配置_
39.     public String getAll(){
40.         System.out.println("book getAll...");
41.         return "{'module':'book getAll'}";
42.     }
43. }

@RestController替换@Controller与@ResponseBody注解，简化书写

@GetMapping @PostMapping @PutMapping @DeleteMapping 每个都对应一个请求动作

#### 案例：基于RESTful页面数据交互

接口制作

1.  @RestController
2.  @RequestMapping("/books")
3.  public class BookController {

4.      @PostMapping
5.      public String save(@RequestBody Book book){
6.          System.out.println("book save ==> "+ book);
7.          return "{'module':'book save success'}";
8.      }

9.     @GetMapping
10.     public List<Book> getAll(){ 
11.         System.out.println("book getAll is running ...");
12.         List<Book> bookList = new ArrayList<Book>();

13.         Book book1 = new Book();
14.         book1.setType("计算机");
15.         book1.setName("SpringMVC入门教程");
16.         book1.setDescription("小试牛刀");
17.         bookList.add(book1);

18.         Book book2 = new Book();
19.         book2.setType("计算机");
20.         book2.setName("SpringMVC实战教程");
21.         book2.setDescription("一代宗师");
22.         bookList.add(book2);

23.         Book book3 = new Book();
24.         book3.setType("计算机丛书");
25.         book3.setName("SpringMVC实战教程进阶");
26.         book3.setDescription("一代宗师呕心创作");
27.         bookList.add(book3);

28.         return bookList;
29.     }

30. }

与前端页面结合

发现localhost/book.html不能跑通，问题出现在getServletMappings中，对于静态资源的访问不需要过SpringMVC

1.  protected String\[\] getServletMappings() {
2.          return new String\[\]{"/"};
3.      }

新建一个SpringMvcSupport配置

1.  @Configuration
2.  public class SpringMvcSupport extends WebMvcConfigurationSupport {
3.      _//设置静态资源访问过滤，当前类需要设置为配置类，并被扫描加载_
4.      @Override
5.      protected void addResourceHandlers(ResourceHandlerRegistry registry) {
6.          _//当访问/pages/????时候，从/pages目录下查找内容_
7.          registry.addResourceHandler("/pages/\*\*").addResourceLocations("/pages/");
8.          registry.addResourceHandler("/js/\*\*").addResourceLocations("/js/");
9.          registry.addResourceHandler("/css/\*\*").addResourceLocations("/css/");
10.         registry.addResourceHandler("/plugins/\*\*").addResourceLocations("/plugins/");
11.     }
12. }

加入扫包

1.  @Configuration
2.  @ComponentScan({"com.itheima.controller","com.itheima.config"})
3.  @EnableWebMvc
4.  public class SpringMvcConfig {
5.  }

前端页面设计省略，axios发送异步请求

并在前端页面上绑定按钮

1.  <script>
2.          var vue = new Vue({

3.              el: '#app',

4.              data:{
5.      dataList: \[\],_//当前页要展示的分页列表数据_
6.                  formData: {},_//表单数据_
7.                  dialogFormVisible: false,_//增加表单是否可见_
8.                 dialogFormVisible4Edit:false,_//编辑表单是否可见_
9.                 pagination: {},_//分页模型数据，暂时弃用_
10.             },

11.             _//钩子函数，VUE对象初始化完成后自动执行_
12.             created() {
13.                 this.getAll();
14.             },

15.             methods: {
16.                 _// 重置表单_
17.                 resetForm() {
18.                     _//清空输入框_
19.                     this.formData = {};
20.                 },

21.                 _// 弹出添加窗口_
22.                 openSave() {
23.                     this.dialogFormVisible = true;
24.                     this.resetForm();
25.                 },

26.                 _//添加_
27.                 saveBook () {
28.                     axios.post("/books",this.formData).then((res)=>{

29.                     });
30.                 },

31.                 _//主页列表查询_
32.                 getAll() {
33.                     axios.get("/books").then((res)=>{
34.                         this.dataList = res.data;
35.                     });
36.                 },

37.             }
38.         })
39.     </script>

小结：

制作SpringMVC控制器，并通过PostMan测试接口功能（使用假数据）

设置对静态资源的访问放行

前端页面通过异步提交访问后台控制器

### SSM整合

#### SSM整合

SSM整合流程

1.  创建工程
2.  SSM整合

- Spring
- SpringConfig
- MyBatis
- MyBatisConfig
- jdbcConfig
- jdbc.properties
- SpringMVC
- ServletConfig
- SpringMvcConfig

1.  功能模块

- 表与实体类
- Dao（接口+自动代理）
- Service（接口+实现类）
- 业务层接口测试（整合JUnit）
- Controller
- 表现层接口测试（Postman）

##### 创建工程

需要导入坐标

Spring-webmvc/Spring-jdbc/Spring-test/Mybatis/Mysql/Druid/Junit/Servlet/Jackson

##### SSM整合配置

SpringConfig

1.  @Configuration
2.  @ComponentScan({"com.itheima.service"})
3.  @PropertySource("classpath:jdbc.properties")
4.  @Import({JdbcConfig.class,MyBatisConfig.class})
5.  @EnableTransactionManagement
6.  public class SpringConfig {
7.  }

加载jdbc.properties

再加载jdbcConfig与MyBatisConfig

JdbcConfig

1.  public class JdbcConfig {
2.      @Value("${jdbc.driver}")
3.      private String driver;
4.      @Value("${jdbc.url}")
5.      private String url;
6.      @Value("${jdbc.username}")
7.      private String username;
8.      @Value("${jdbc.password}")
9.      private String password;

10.     @Bean
11.     public DataSource dataSource(){
12.         DruidDataSource dataSource = new DruidDataSource();
13.         dataSource.setDriverClassName(driver);
14.         dataSource.setUrl(url);
15.         dataSource.setUsername(username);
16.         dataSource.setPassword(password);
17.         return dataSource;
18.     }

19.     @Bean
20.     public PlatformTransactionManager transactionManager(DataSource dataSource){
21.         DataSourceTransactionManager ds = new DataSourceTransactionManager();
22.         ds.setDataSource(dataSource);
23.         return ds;
24.     }
25. }

MyBatisConfig

1.  public class MyBatisConfig {
2.      @Bean
3.      public SqlSessionFactoryBean sqlSessionFactory(DataSource dataSource){
4.          SqlSessionFactoryBean factoryBean = new SqlSessionFactoryBean();
5.          factoryBean.setDataSource(dataSource);
6.          factoryBean.setTypeAliasesPackage("com.itheima.domain");
7.          return factoryBean;
8.      }
9.  }

SpringMvcConfig

1.  @Configuration
2.  @ComponentScan("com.itheima.controller")
3.  @EnableWebMvc
4.  public class SpringMvcConfig {
5.  }

ServletConfig

1.  public class ServletConfig extends AbstractAnnotationConfigDispatcherServletInitializer {
2.      protected Class<?>\[\] getRootConfigClasses() {
3.          return new Class\[\]{SpringConfig.class};
4.      }

5.      protected Class<?>\[\] getServletConfigClasses() {
6.          return new Class\[\]{SpringMvcConfig.class};
7.      }

8.     protected String\[\] getServletMappings() {
9.         return new String\[\]{"/"};
10.     }
11. }

还可以创建一个过滤器来处理中文表单提交乱码的过滤

##### 功能模块

创建实体类Book

1.  public class Book {
2.      private Integer id;
3.      private String type;
4.      private String name;
5.      private String description;

6.      @Override
7.      public String toString() {
8.          return "Book{" +
9.                 "id=" + id +
10.                 ", type='" + type + '\\'' +
11.                 ", name='" + name + '\\'' +
12.                 ", description='" + description + '\\'' +
13.                 '}';
14.     }

15.     public Integer getId() {
16.         return id;
17.     }

18.     public void setId(Integer id) {
19.         this.id = id;
20.     }

21.     public String getType() {
22.         return type;
23.     }

24.     public void setType(String type) {
25.         this.type = type;
26.     }

27.     public String getName() {
28.         return name;
29.     }

30.     public void setName(String name) {
31.         this.name = name;
32.     }

33.     public String getDescription() {
34.         return description;
35.     }

36.     public void setDescription(String description) {
37.         this.description = description;
38.     }
39. }

BookDao

1.  public interface BookDao {

2.  //    @Insert("insert into tbl_book values(null,#{type},#{name},#{description})")
3.      @Insert("insert into tbl_book (type,name,description) values(#{type},#{name},#{description})")
4.      public void save(Book book);

5.      @Update("update tbl_book set type = #{type}, name = #{name}, description = #{description} where id = #{id}")
6.      public void update(Book book);

7.     @Delete("delete from tbl_book where id = #{id}")
8.     public void delete(Integer id);

9.     @Select("select \* from tbl_book where id = #{id}")
10.     public Book getById(Integer id);

11.     @Select("select \* from tbl_book")
12.     public List<Book> getAll();
13. }

BookService

1.  public interface BookService {

2.      _/\*\*_
3.       \* 保存
4.       \* @param book
5.       \* @return
6.       \*/
7.      public boolean save(Book book);

8.     _/\*\*_
9.      \* 修改
10.      \* @param book
11.      \* @return
12.      \*/
13.     public boolean update(Book book);

14.     _/\*\*_
15.      \* 按id删除
16.      \* @param id
17.      \* @return
18.      \*/
19.     public boolean delete(Integer id);

20.     _/\*\*_
21.      \* 按id查询
22.      \* @param id
23.      \* @return
24.      \*/
25.     public Book getById(Integer id);

26.     _/\*\*_
27.      \* 查询全部
28.      \* @return
29.      \*/
30.     public List<Book> getAll();
31. }

BookServiceImpl

1.  @Service
2.  public class BookServiceImpl implements BookService {
3.      @Autowired
4.      private BookDao bookDao;

5.      public boolean save(Book book) {
6.          bookDao.save(book);
7.          return true;
8.      }

9.     public boolean update(Book book) {
10.         bookDao.update(book);
11.         return true;
12.     }

13.     public boolean delete(Integer id) {
14.         bookDao.delete(id);
15.         return true;
16.     }

17.     public Book getById(Integer id) {
18.         return bookDao.getById(id);
19.     }

20.     public List<Book> getAll() {
21.         return bookDao.getAll();
22.     }
23. }

出现bookDao爆红，是因为Spring中没有配bookDao的bean，使用的是mybatis自动代理，所以就没有对应的bean自动装配，但是这里不会影响程序的正常运行

可行的解决方案：

使用构造器注入或者直接忽略错误因为不会影响运行

BookController

1.  @RestController
2.  @RequestMapping("/books")
3.  public class BookController {

4.      @Autowired
5.      private BookService bookService;

6.      @PostMapping
7.      public boolean save(@RequestBody Book book) {
8.         return bookService.save(book);
9.     }

10.     @PutMapping
11.     public boolean update(@RequestBody Book book) {
12.         return bookService.update(book);
13.     }

14.     @DeleteMapping("/{id}")
15.     public boolean delete(@PathVariable Integer id) {
16.         return bookService.delete(id);
17.     }

18.     @GetMapping("/{id}")
19.     public Book getById(@PathVariable Integer id) {
20.         return bookService.getById(id);
21.     }

22.     @GetMapping
23.     public List<Book> getAll() {
24.         return bookService.getAll();
25.     }
26. }

使用RequestMapping配置公共映射

然后使用REST风格

##### 测试

业务层接口测试（整合JUnit）/表现层接口测试（Postman）

业务层（Service）测试

1.  @RunWith(SpringJUnit4ClassRunner.class)
2.  @ContextConfiguration(classes = SpringConfig.class)
3.  public class BookServiceTest {

4.      @Autowired
5.      private BookService bookService;

6.      @Test
7.      public void testGetById(){
8.         Book book = bookService.getById(1);
9.         System.out.println(book);
10.     }

11.     @Test
12.     public void testGetAll(){
13.         List<Book> all = bookService.getAll();
14.         System.out.println(all);
15.     }

16. }

表现层测试（Postman）

##### 添加事务管理

在SpringConfig中使用@EnableTransactionManagement开启事务管理

JdbcConfig

1.      @Bean
2.      public PlatformTransactionManager transactionManager(DataSource dataSource){
3.          DataSourceTransactionManager ds = new DataSourceTransactionManager();
4.          ds.setDataSource(dataSource);
5.          return ds;
6.      }

BookService

1.  @Transactional

挂上事务，先不配事务

#### 表现层数据封装（前后端数据协议）

前端接收数据格式

\-创建结果模型类，封装到data属性中

\-封装特殊信息到message（msg）属性中

Controller-result

1.  public class Result {
2.      _//描述统一格式中的数据_
3.      private Object data;
4.      _//描述统一格式中的编码，用于区分操作，可以简化配置0或1表示成功失败_
5.      private Integer code;
6.      _//描述统一格式中的消息，可选属性_
7.      private String msg;

8.      public Result() {}

9.     public Result(Integer code,Object data) {
10.         this.data = data;
11.         this.code = code;
12.     }

13.     public Result(Integer code, Object data, String msg) {
14.         this.data = data;
15.         this.code = code;
16.         this.msg = msg;
17.     }

18.     public Object getData() {return data;}

19.     public void setData(Object data) {this.data = data;}

20.     public Integer getCode() {return code;}

21.     public void setCode(Integer code) {this.code = code;}

22.     public String getMsg() {return msg;}

23.     public void setMsg(String msg) {this.msg = msg;}
24. }

Controller-Code

1.  _//状态码_
2.  public class Code {
3.      public static final Integer SAVE_OK = 20011;
4.      public static final Integer DELETE_OK = 20021;
5.      public static final Integer UPDATE_OK = 20031;
6.      public static final Integer GET_OK = 20041;

7.      public static final Integer SAVE_ERR = 20010;
8.      public static final Integer DELETE_ERR = 20020;
9.     public static final Integer UPDATE_ERR = 20030;
10.     public static final Integer GET_ERR = 20040;
11. }

BookController

1.      @PostMapping
2.      public Result save(@RequestBody Book book) {
3.          boolean flag = bookService.save(book);
4.          return new Result(flag ? Code.SAVE_OK:Code.SAVE_ERR,flag);
5.      }

三步运算判断，flag如果成功（true）返回save_ok，如果失败返回save_err

1.      @GetMapping("/{id}")
2.      public Result getById(@PathVariable Integer id) {
3.          Book book = bookService.getById(id);
4.          Integer code = book != null ? Code.GET_OK : Code.GET_ERR;
5.          String msg = book != null ? "" : "数据查询失败，请重试！";
6.          return new Result(code,book,msg);
7.      }

#### 异常处理器

程序开发过程中不可避免的会遇到异常现象

出现异常现象的常见位置与常见诱因：

框架内部抛出的异常：因使用不合规导致

数据层抛出的异常：因外部服务器故障导致（服务器访问超时）

业务层抛出的异常：因业务逻辑书写错误导致（遍历业务书写操作，导致索引异常）

表现层抛出的异常：因数据收集，校验等规则导致（不匹配的数据类型间导致异常）

工具类抛出的异常：因工具类书写不严谨不够健壮导致（必要释放的连接长期未释放）

各个层级均出现异常，异常处理代码书写在哪一层？

\-所有的异常均抛出表现层进行处理

表现层处理异常，每个方法单独书写，代码书写量巨大且意义不强，解决-AOP思想

集中的 统一的处理项目中出现的异常

Controller中创建ProjectExceptionAdvice

1.  @RestControllerAdvice
2.  public class ProjectExceptionAdvice {   
3.  @ExceptionHandler(Exception.class)
4.      public Result doOtherException(Exception ex){
5.          return new Result(555,null);
6.      }
7.  }

#### 项目异常处理方案

项目异常分类以及处理方案：

- 业务异常-发送对应消息传递给用户，提醒规范操作（businessExpection）
- 规范的用户行为产生的异常
- 不规范的用户行为操作产生的异常
- 系统异常（SystemExpection）

\-发送固定消息传递给用户，安抚用户

\-发送特定消息给运维人员，提醒维护

\-记录日志

- 项目运行过程中可预计无法避免的异常
- 其他异常-发送固定消息传递给用户，安抚用户
- 编程人员未预期到的异常

新建一个exception类存放自定义异常处理器

1.  _//自定义异常处理器，用于封装异常信息，对异常进行分类_
2.  public class BusinessException extends RuntimeException{
3.      private Integer code;

4.      public Integer getCode() {
5.          return code;
6.      }

7.      public void setCode(Integer code) {
8.         this.code = code;
9.     }

10.     public BusinessException(Integer code, String message) {
11.         super(message);
12.         this.code = code;
13.     }

14.     public BusinessException(Integer code, String message, Throwable cause) {
15.         super(message, cause);
16.         this.code = code;
17.     }

18. }

加一个编号用于异常识别

BookServiceImpl 模拟业务异常/系统异常

1.      public Book getById(Integer id) {
2.          _//模拟业务异常，包装成自定义异常_
3.          if(id == 1){
4.              throw new BusinessException(Code.BUSINESS_ERR,"请不要使用你的技术挑战我的耐性!");
5.          }
6.          _//模拟系统异常，将可能出现的异常进行包装，转换成自定义异常_
7.          try{
8.              int i = 1/0;
9.          }catch (Exception e){
10.             throw new SystemException(Code.SYSTEM_TIMEOUT_ERR,"服务器访问超时，请重试!",e);
11.         }
12.         return bookDao.getById(id);
13.     }

ProjectExpectionAdvice

拦截并处理异常

1.  @RestControllerAdvice
2.  public class ProjectExceptionAdvice {
3.      _//@ExceptionHandler用于设置当前处理器类对应的异常类型_
4.      @ExceptionHandler(SystemException.class)
5.      public Result doSystemException(SystemException ex){
6.          _//记录日志_
7.          _//发送消息给运维_
8.          _//发送邮件给开发人员,ex对象发送给开发人员_
9.          return new Result(ex.getCode(),null,ex.getMessage());
10.     }

11.     @ExceptionHandler(BusinessException.class)
12.     public Result doBusinessException(BusinessException ex){
13.         return new Result(ex.getCode(),null,ex.getMessage());
14.     }

15.     _//除了自定义的异常处理器，保留对Exception类型的异常处理，用于处理非预期的异常_
16.     @ExceptionHandler(Exception.class)
17.     public Result doOtherException(Exception ex){
18.         _//记录日志_
19.         _//发送消息给运维_
20.         _//发送邮件给开发人员,ex对象发送给开发人员_
21.         return new Result(Code.SYSTEM_UNKNOW_ERR,null,"系统繁忙，请稍后再试！");
22.     }
23. }

#### 案例：SSM整合前台标准开发

前面已经完成了所有的后台，现在需要完成前台页面与后台的调通

SpringMvcSupport

设置对前端页面的放行

1.  @Configuration
2.  public class SpringMvcSupport extends WebMvcConfigurationSupport {
3.      @Override
4.      protected void addResourceHandlers(ResourceHandlerRegistry registry) {
5.          registry.addResourceHandler("/pages/\*\*").addResourceLocations("/pages/");
6.          registry.addResourceHandler("/css/\*\*").addResourceLocations("/css/");
7.          registry.addResourceHandler("/js/\*\*").addResourceLocations("/js/");
8.          registry.addResourceHandler("/plugins/\*\*").addResourceLocations("/plugins/");
9.      }
10. }

保证被加载

1.  @Configuration
2.  @ComponentScan({"com.itheima.controller","com.itheima.config"})
3.  @EnableWebMvc
4.  public class SpringMvcConfig {
5.  }

##### 列表页

发送异步请求

1.              methods: {
2.                  _//列表_
3.                  getAll() {
4.                      _//发送ajax请求_
5.                      axios.get("/books").then((res)=>{
6.                          this.dataList = res.data.data;
7.                      });
8.                  },
9.              }

##### 添加页

1.                  _//添加_
2.                  handleAdd () {
3.                      _//发送ajax请求_
4.                      axios.post("/books",this.formData).then((res)=>{
5.                          console.log(res.data);
6.                          _//如果操作成功，关闭弹层，显示数据_

7.                              this.dialogFormVisible = false;
8.                           this.getAll();
9.                     });
10.                 },

区分操作成功/失败的情况

1.                  _//添加_
2.                  handleAdd () {
3.                      _//发送ajax请求_
4.                      axios.post("/books",this.formData).then((res)=>{
5.                          console.log(res.data);
6.                          _//如果操作成功，关闭弹层，显示数据_
7.                          if(res.data.code == 20011){
8.                              this.dialogFormVisible = false;
9.                              this.$message.success("添加成功");
10.                         }else if(res.data.code == 20010){
11.                             this.$message.error("添加失败");
12.                         }else{
13.                             this.$message.error(res.data.msg);
14.                         }
15.                     }).finally(()=>{
16.                         this.getAll();
17.                     });
18.                 },

$message - Element UI库提供的消息提示组件

Axios补充：

axios.post() - 使用axios发送POST请求方法

这是axios库提供的用于发送POST请求的函数

"/books" - 请求的目标URL路径

这是一个相对路径，会发送到当前域名下的/books端点

对应后端的图书添加接口

this.formData - 请求体数据

this指向Vue实例

formData是Vue实例中的数据属性，包含表单输入的数据

包含图书的类别(type)、名称(name)和描述(description)

.then((res) => { - Promise回调函数

当POST请求成功完成时执行

res参数包含服务器返回的响应数据（只是一个参数变量名）

##### 弹出编辑窗口

1.                  _//弹出编辑窗口_
2.                  handleUpdate(row) {
3.                      _// console.log(row);   //row.id 查询条件_
4.                      _//查询数据，根据id查询_
5.                      axios.get("/books/"+row.id).then((res)=>{
6.                          _// console.log(res.data.data);_
7.                          if(res.data.code == 20041){
8.                              _//展示弹层，加载数据_
9.                              this.formData = res.data.data;
10.                             this.dialogFormVisible4Edit = true;
11.                         }else{
12.                             this.$message.error(res.data.msg);
13.                         }
14.                     });
15.                 },

前台中

slot-scope="scope" 是 Element UI 表格组件提供的作用域插槽

scope.row 代表当前行的数据对象

1.  <el-table-column label="操作" align="center">
2.      <template slot-scope="scope">
3.          <el-button type="primary" size="mini" @click="handleUpdate(scope.row)">编辑</el-button>
4.          <el-button type="danger" size="mini" @click="handleDelete(scope.row)">删除</el-button>
5.      </template>
6.  </el-table-column>

Row对象来自于表格的 :data="dataList" 属性

##### 编辑

1.                  _//编辑_
2.                  handleEdit() {
3.                      _//发送ajax请求_
4.                      axios.put("/books",this.formData).then((res)=>{
5.                          _//如果操作成功，关闭弹层，显示数据_
6.                          if(res.data.code == 20031){
7.                              this.dialogFormVisible4Edit = false;
8.                              this.$message.success("修改成功");
9.                          }else if(res.data.code == 20030){
10.                             this.$message.error("修改失败");
11.                         }else{
12.                             this.$message.error(res.data.msg);
13.                         }
14.                     }).finally(()=>{
15.                         this.getAll();
16.                     });
17.                 },

与添加操作几乎完全一致，除了ajax请求的类型

##### 删除

1.                  _// 删除_
2.                  handleDelete(row) {
3.                      _//1.弹出提示框_
4.                      this.$confirm("此操作永久删除当前数据，是否继续？","提示",{
5.                          type:'info'
6.                      }).then(()=>{
7.                          _//2.做删除业务_
8.                          axios.delete("/books/"+row.id).then((res)=>{
9.                              if(res.data.code == 20021){
10.                                 this.$message.success("删除成功");
11.                             }else{
12.                                 this.$message.error("删除失败");
13.                             }
14.                         }).finally(()=>{
15.                             this.getAll();
16.                         });
17.                     }).catch(()=>{
18.                         _//3.取消删除_
19.                         this.$message.info("取消删除操作");
20.                     });
21.                 }

### 拦截器

#### 拦截器概念

- 拦截器（Intercepetor）是一种动态拦截方法调用的机制，在SpringMVC中动态拦截控制器方法的执行
- 作用：
- 在指定的方法调用前后执行预先设定的代码
- 阻止原始方法的执行
- 拦截器与过滤器区别
- 归属不同：Filter属于Servlet技术，Interceptor属于SpringMVC技术
- 拦截内容不同：Filter对所有访问进行增强，Interceptor仅针对SpringMVC的访问进行增强

拦截器执行流程

—preHandle—return——controller—postHandle—afterCompletion

true

#### 入门案例

拦截器可以在方法的前/后执行

制作拦截器功能类

Controller-interceptor-ProjectInterceptor 拦截器服务于表现层

1.  @Component
2.  _//定义拦截器类，实现HandlerInterceptor接口_
3.  _//注意当前类必须受Spring容器控制_
4.  public class ProjectInterceptor implements HandlerInterceptor {
5.      @Override
6.      _//原始方法调用前执行的内容_
7.      _//返回值类型可以拦截控制的执行，true放行，false终止_
8.      public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
9.          String contentType = request.getHeader("Content-Type");
10.         HandlerMethod hm = (HandlerMethod)handler;
11.         System.out.println("preHandle..."+contentType);
12.         return true;
13.     }

14.     @Override
15.     _//原始方法调用后执行的内容_
16.     public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
17.         System.out.println("postHandle...");
18.     }

19.     @Override
20.     _//原始方法调用完成后执行的内容_
21.     public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
22.         System.out.println("afterCompletion...");
23.     }
24. }

使用false可以终止原始操作的执行

配置拦截器的执行位置

SpringMvcSupport

1.  @Configuration
2.  public class SpringMvcSupport extends WebMvcConfigurationSupport {
3.      @Autowired
4.      private ProjectInterceptor projectInterceptor;

5.      @Override
6.  _//过滤静态资源_
7.      protected void addResourceHandlers(ResourceHandlerRegistry registry) {
8.          registry.addResourceHandler("/pages/\*\*").addResourceLocations("/pages/");
9.     }

10.     @Override
11.     protected void addInterceptors(InterceptorRegistry registry) {
12.         _//配置拦截器_
13.         registry.addInterceptor(projectInterceptor).addPathPatterns("/books","/books/\*");
14.     }
15. }

该拦截器在调用books 和 /books/\* 时拦截，路径可以通过可变参数设置多个

设置扫包

1.  @Configuration
2.  @ComponentScan({"com.itheima.controller"，com.itheima.config})
3.  @EnableWebMvc
4.  _//实现WebMvcConfigurer接口可以简化开发，但具有一定的侵入性_
5.  public class SpringMvcConfig implements WebMvcConfigurer {
6.      }
7.  }

##### 简化开发（侵入性强）

1.  @Configuration
2.  @ComponentScan({"com.itheima.controller"})
3.  @EnableWebMvc
4.  _//实现WebMvcConfigurer接口可以简化开发，但具有一定的侵入性_
5.  public class SpringMvcConfig implements WebMvcConfigurer {
6.      @Autowired
7.      private ProjectInterceptor projectInterceptor;
8.      @Autowired
9.      private ProjectInterceptor2 projectInterceptor2;

10.     @Override
11.     public void addInterceptors(InterceptorRegistry registry) {
12.         _//配置多拦截器_
13.         registry.addInterceptor(projectInterceptor).addPathPatterns("/books","/books/\*");
14.     }
15. }

#### 拦截器参数

前置处理

public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {}

Request：请求对象

Response：响应对象

Handler：被调用的处理器对象，本质上是一个方法对象，对反射技术中的method对象进行了再包装

后置处理

public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {}

ModelAndView如果处理器执行完成具有返回结果，可以读取到对应数据与页面信息，并进行调整

完成后处理

public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {}

ex：如果处理器执行过程中出现异常对象，可以针对异常情况进行单独处理

但可以通过SpringMVC的异常处理机制完美替换

#### 拦截器链

当配置多个拦截器时，形成拦截器链

拦截器链的运行顺序参照拦截器添加顺序为主

PreHandle：与配置顺序相同，必定运行

PostHandle：与配置顺序相反，可能不运行

AfterCompletion：与配置顺序相反，可能不运行

## Maven Advanced

### 分模块开发

将原始模块按照功能拆分成若干个子模块，方便模块间的互相调用，接口共享

#### 创建Maven模块

#### 书写模块代码

Maven_02_ssm

1.      _<!--依赖domain运行-->_
2.      <dependency>
3.        <groupId>com.itheima</groupId>
4.        <artifactId>maven_03_pojo</artifactId>
5.        <version>1.0-SNAPSHOT</version>
6.      </dependency>

依赖domain运行

#### 通过maven指令安装模块到本地仓库（install）

使用install下载到仓库

团队内部开发需要发布模块功能到团队内部可共享的仓库中（私服）

### 依赖管理

- 依赖指当前项目运行所需的jar，一个项目可以设置多个依赖，依赖具有传递性

#### 传递依赖

- 直接依赖：在当前项目中通过依赖配置建立的依赖关系
- 间接依赖：被以来的资源如果依赖其他资源，当前项目间接依赖其他资源

#### 依赖传递冲突问题

- 路径优先：当依赖中出现相同的资源时，层级越深，优先级越低，层级越浅，优先级越高
- 声明优先：当资源在相同层级被依赖时，配置顺序靠前（配置文件的顺序）的覆盖配置顺序靠后的
- 特殊优先：当同级配置了相同资源的不同版本，后配置的覆盖先配置的

#### 可选依赖与排除依赖

可选依赖-隐藏自己的依赖 对外隐藏当前所依赖的资源——不透明

1.          <dependency>
2.              <groupId>com.itheima</groupId>
3.              <artifactId>maven_03_pojo</artifactId>
4.              <version>1.0-SNAPSHOT</version>
5.              <!--可选依赖是隐藏当前工程所依赖的资源，隐藏后对应资源将不具有依赖传递性;-->
6.              <optional>false</optional>
7.          </dependency>

- 排除依赖是隐藏当前资源对应的依赖关系-使用其他的资源时排除不用的依赖

主动断开以来的资源，被排除的资源无需指定版本——不需要

1.        <exclusions>
2.          <exclusion>
3.            <groupId>log4j</groupId>
4.            <artifactId>log4j</artifactId>
5.          </exclusion>
6.          <exclusion>
7.            <groupId>org.mybatis</groupId>
8.            <artifactId>mybatis</artifactId>
9.          </exclusion>
10.       </exclusions>
11.     </dependency>

排除依赖仅指定GA即可，无需指定V

### 聚合与继承

#### 聚合

- 聚合：将多个模块组织成一个整体，同时进行项目构建的过程称为聚合
- 聚合工程：通常是一个不具有业务功能的空工程（有且仅有一个pom文件）
- 作用：使用聚合工程可以将多个工程编组，通过对聚合工程进行构建，实现对时所包含的模块进行同步构建
- 当工程中某个模块发生更新（变更）时，必须保障工程中与已更新模块关联的模块同步更新，此时可以使用聚合工程来解决批量模块同步构建的问题

新建maven_01_parent 设置打包类型为pom

1.      <groupId>com.itheima</groupId>
2.      <artifactId>maven_01_parent</artifactId>
3.      <version>1.0-RELEASE</version>
4.      <packaging>pom</packaging>

设置当前聚合工程所包含的子模块名称

1.      _<!--设置管理的模块名称-->_
2.      <modules>
3.          <module>../maven_02_ssm</module>
4.          <module>../maven_03_pojo</module>
5.          <module>../maven_04_dao</module>
6.      </modules>

启动compile后会先构建没有依赖的，交换module的顺序对编译过程不产生影响

#### 继承

- 描述的是两个工程间的关系，与java中的继承相似，子工程可以继承父工程中的配置信息，常见于依赖关系的继承
- 作用：简化配置/减少版本冲突
- 聚合继承一般同一个文件

Maven_02_ssm 在子工程中配置当前继承的夫工程

1.    <parent>
2.      <groupId>com.itheima</groupId>
3.      <artifactId>maven_01_parent</artifactId>
4.      <version>1.0-RELEASE</version>
5.      <relativePath>../maven_01_parent/pom.xml</relativePath>
6.    </parent>

配置父工程GAV relativePath

父工程中可选依赖 配置子工程中可选的依赖关系

1.      _<!--定义依赖管理-->_
2.      <dependencyManagement>
3.          <dependencies>
4.              <dependency>
5.                  <groupId>junit</groupId>
6.                  <artifactId>junit</artifactId>
7.                  <version>4.12</version>
8.                  <scope>test</scope>
9.              </dependency>
10.         </dependencies>
11.     </dependencyManagement>

子工程中使用父工程中的可选依赖时，仅需要提供群组id和项目id，无需提供版本，版本由父工程统一提供，避免版本冲突，子工程中还可以定义父工程中没有定义的依赖关系

#### 继承与聚合的区别

- 作用：聚合用于快速构建项目，配置用于快速配置
- 相同点：
- 聚合与继承的pom.xml文件打包方式均为pom，可以将两种关系制作到同一个pom文件中
- 聚合与继承均属于设计型模块，并无实际的模块内容
- 不同点：
- 聚合是在当前模块中配置关系，聚合可以感知到参与聚合的模块有哪些
- 继承是在子模块中配置关系，父模块无法感知哪些子模块继承了自己

### 属性管理

#### 属性

1.      _<!--定义属性-->_
2.      <properties>
3.          <spring.version>5.2.10.RELEASE</spring.version>
4.          <junit.version>4.12</junit.version>
5.          <mybatis-spring.version>1.3.0</mybatis-spring.version>
6.          _<!--<jdbc.url>jdbc:mysql://127.0.0.1:3306/ssm_db</jdbc.url>-->_
7.      </properties>

8.      _<!--定义依赖管理-->_
9.     <dependencyManagement>
10.         <dependencies>
11.             <dependency>
12.                 <groupId>junit</groupId>
13.                 <artifactId>junit</artifactId>
14.                 <version>${junit.version}</version>
15.                 <scope>test</scope>
16.             </dependency>
17.         </dependencies>
18.     </dependencyManagement>

定义属性--引用属性

#### 配置文件加载属性

加载jdbc，定义属性

1.      _<!--定义属性-->_
2.      <properties>
3.          <jdbc.url>jdbc:mysql://127.0.0.1:3306/ssm_db</jdbc.url>
4.      </properties>

Jdbc.properties配置资源中引用属性

1.  jdbc.driver=com.mysql.jdbc.Driver
2.  jdbc.url=${jdbc.url}
3.  jdbc.username=root
4.  jdbc.password=root

设置资源目录

开启资源文件目录加载属性的过滤器

1.      <build>
2.          <resources>
3.              _<!--设置资源目录，并设置能够解析${}-->_
4.              <resource>
5.                  <directory>${project.basedir}/src/main/resources</directory>
6.                  <filtering>true</filtering>
7.              </resource>
8.          </resources>
9.      </build>

${project.basedir}内置属性名

配置maven打jar包，忽略web.xml检查

1.        <plugin>
2.          <groupId>org.apache.maven.plugins</groupId>
3.          <artifactId>maven-war-plugin</artifactId>
4.          <version>3.2.3</version>
5.          <configuration>
6.            <failOnMissingWebXml>false</failOnMissingWebXml>
7.          </configuration>
8.        </plugin>

#### 版本管理

- 工程版本：
- SNAPSHOT（快照版本）

项目开发过程中临时输出的版本，称为快照版本

快照版本会随着开发的进展不断更新

- RELEASE（发布版本）

项目开发到进入阶段里程碑后，向团队外部发布较为稳定的版本，这种版本所对应的构建是稳定的，即便进行功能的后续开发，也不会改变当前发布版本内容

- 发布版本
- Alpha版
- Beta版
- 纯数字版

### 多环境配置与应用

场景：生产环境需要一个数据库，开发环境需要一个数据库，测试环境需要一个数据库则需要配置多环境

#### 多环境开发

1.  _<!--配置多环境-->_
2.      <profiles>
3.          _<!--开发环境-->_
4.          <profile>
5.              <id>env_dep</id>
6.              <properties>
7.                  <jdbc.url>jdbc:mysql://127.1.1.1:3306/ssm_db</jdbc.url>
8.              </properties>
9.              _<!--设定是否为默认启动环境-->_
10.             <activation>
11.                 <activeByDefault>true</activeByDefault>
12.             </activation>
13.         </profile>
14.         _<!--生产环境-->_
15.         <profile>
16.             <id>env_pro</id>
17.             <properties>
18.                 <jdbc.url>jdbc:mysql://127.2.2.2:3306/ssm_db</jdbc.url>
19.             </properties>
20.         </profile>
21.         _<!--测试环境-->_
22.         <profile>
23.             <id>env_test</id>
24.             <properties>
25.                 <jdbc.url>jdbc:mysql://127.3.3.3:3306/ssm_db</jdbc.url>
26.             </properties>
27.         </profile>
28.     </profiles>

选中执行指令，mvn install -p env_test 相当于携带test指令

#### 跳过测试

应用场景：功能更新中并且还没有开发完毕/快速打包/...

或者指令实现

mvn package -D skipTests

弊端：全部跳过，一个测试都不执行

配置文件实现跳过指定的测试部分/细粒度管理

1.      <build>
2.          <plugins>
3.              <plugin>
4.                  <artifactId>maven-surefire-plugin</artifactId>
5.                  <version>2.12.4</version>
6.                  <configuration>
7.                      <skipTests>false</skipTests>
8.                      _<!--排除掉不参与测试的内容-->_
9.                      <excludes>
10.                         <exclude>\*\*/BookServiceTest.java</exclude>
11.                     </excludes>
12.                 </configuration>
13.             </plugin>
14.         </plugins>
15.     </build>

### 私服

#### 私服简介

- 私服是一台独立的服务器，用于解决团队内部的资源共享与资源同步问题
- Nexus

Sonatype公司的一款maven私服产品

启动服务器：nexus.exe /run nexus

访问服务器：http：//localhost：8081

#### 私服仓库分类

|     |     |     |     |
| --- | --- | --- | --- |
| 仓库分类 | 英文名称 | 功能  | 关联操作 |
| 宿主仓库 | Hosted | 保存自主研发+第三方资源 | 上传  |
| 代理仓库 | Proxy | 代理连接中央仓库 | 下载  |
| 仓库组 | Group | 为仓库编组简化下载操作 | 下载  |

#### 资源上传

上传的位置（宿主地址）

|

Idea——本地仓库——私服

|

本地仓库配置访问私服的用户名/密码

下载的地址

1.  在Nexus中配置demo-release与demo-snapshot两个仓库

2.  Settings.xml中配置访问私服的权限
3.      _<!-- 配置访问私服的权限 -->_
4.      <server>
5.        <id>demo-snapshot</id>
6.        <username>admin</username>
7.        <password>admin</password>
8.      </server>
9.      <server>
10.        <id>demo-release</id>
11.       <username>admin</username>
12.       <password>admin</password>
13.     </server>

14.  找到group中的maven仓库作为仓库组

15.  移动demo-release与demo-snapshot得到maven-public管理

16.  配置私服的访问路径
17.       <mirror>
18.       _<!-- 私服的访问路径 -->_
19.        <mirror>
20.        <id>maven-public</id>
21.        <mirrorOf>\*</mirrorOf>
22.        <url>http://localhost:8081/repository/maven-public/</url>
23.      </mirror>
24.    </mirrors>

这样本地仓库就与私服建立联系

1.  配置当前工程保存在私服中的具体位置
2.      _<!--配置当前工程保存在私服中的具体位置-->_
3.      <distributionManagement>
4.          <repository>
5.              <id>itheima-release</id>
6.              <url>http://localhost:8081/repository/itheima-release/</url>
7.          </repository>
8.          <snapshotRepository>
9.              <id>itheima-snapshot</id>
10.             <url>http://localhost:8081/repository/itheima-snapshot/</url>
11.         </snapshotRepository>
12.     </distributionManagement>

13.  发布命令

Mvn deploy

## SpringBoot

### SpringBoot简介

SpringBoot是由Pivotal团队提供的全新框架，其设计的是用来简化Spring应用的初始搭建以及开发过程

#### 入门案例

制作controller类

1.  @RestController
2.  @RequestMapping("/books")
3.  public class BookController {

4.      @GetMapping("/{id}")
5.      public String getById(@PathVariable Integer id){
6.          System.out.println("id ==> "+id);
7.          return "hello , spring boot!";
8.      }
9. }

Application类

1.  @SpringBootApplication
2.  public class Application {

3.      public static void main(String\[\] args) {
4.          SpringApplication.run(Application.class, args);
5.      }
6.  }

SpringBoot内嵌Tomcat已经能启动

#### SpringBoot与Spring对比

最简SpringBoot程序所包含的基础文件

pom.xml

Application类

Spring程序与SpringBoot程序对比

|     |     |     |
| --- | --- | --- |
| 类/配置文件 | Spring | SpringBoot |
| Pom文件中的坐标 | 手工制作 | 勾选添加 |
| Web3.0配置类 | 手工制作 | 无   |
| Spring/SpringMVC配置类 | 手工制作 | 无   |
| 控制器 | 手工制作 | 手工制作 |

但基于idea开发Spring Boot程序需要确保联网，且能加载到程序框架结构

#### SpringBoot项目快速启动

1.  先对SpringBoot项目打包（执行Maven构建指令package）

2.  找到springboot_01_quickstart-0.0.1-SNAPSHOT文件，打开对应位置
3.  使用cmd打开输入java -jar springboot_01_quickstart-0.0.1-SNAPSHOT

（jar支持命令行启动，但需要依赖maven插件支持）

1.          <plugins>
2.              <plugin>
3.                  <groupId>org.springframework.boot</groupId>
4.                  <artifactId>spring-boot-maven-plugin</artifactId>
5.              </plugin>

成功快速启动

#### SpringBoot概述

简化Spring应用的初始搭建以及开发过程，自动配置，起步依赖，辅助功能（内置服务器）

Spring程序缺点：配置繁琐，依赖设置繁琐

起步依赖-一次性地写了若干个依赖。开发web程序所需要依赖

1.          <dependency>
2.  <groupId>org.springframework.boot</groupId>
3.              <artifactId>spring-boot-starter-web</artifactId>
4.              <exclusions>
5.                  <exclusion>
6.                     <groupId>org.springframework.boot</groupId>
7.                     <artifactId>spring-boot-starter-tomcat</artifactId>
8.                  </exclusion>
9.              </exclusions>
10.         </dependency>

Parent所有SpringBoot项目要继承的项目，定义若干个坐标版本号，以达到减少依赖冲突的目的

引导类

1.  @SpringBootApplication
2.  public class Application {

3.      public static void main(String\[\] args) {
4.          SpringApplication.run(Application.class, args);
5.      }
6.  }

SpringBoot的引导类是项目的入口，运行main方法就可以启动项目

更改Tomcat服务器

1.          <dependency>
2.              <groupId>org.springframework.boot</groupId>
3.              <artifactId>spring-boot-starter-web</artifactId>
4.              <exclusions>
5.                  <exclusion>
6.                     <groupId>org.springframework.boot</groupId>
7.                     <artifactId>spring-boot-starter-tomcat</artifactId>
8.                  </exclusion>
9.              </exclusions>
10.         </dependency>

11.         <dependency>
12.             <groupId>org.springframework.boot</groupId>
13.             <artifactId>spring-boot-starter-jetty</artifactId>
14.         </dependency>

需要先排除tomcat，更换jetty服务器（更轻量级，可扩展性更强）

### 基础配置

#### 三种配置文件

application.properties #server.port=80

application.yaml/yml

1.  server:
2.    port: 82

主写yml文件

注：自动提示功能消失解决方案：

File-Project Structure-Facets-Spring-需要配的工程-追加配置文件（yaml/yml）

加载顺序：.properties > .yml > .yaml

#### Yaml

YAML 一种数据序列化格式，容易阅读，容易与脚本语言交互，以数据为核心，重数据轻格式

##### 语法规则

- 大小写敏感
- 属性层级关系使用多行描述，每行结尾使用冒号结束
- 使用缩进表示层级关系，同层级左侧对齐，只允许使用空格
- 属性值前添加空格（属性名与属性值之间使用冒号 + 空格作为风格）
- \# 表示注释
- 数组数据在数据书写的位置下方使用减号作为数据开始符号，每行书写一个数据，减号与数据间空格风格

##### Yaml数据读取方式

Application.yaml

1.  lesson: SpringBoot

2.  server:
3.    port: 80

4.  enterprise:
5.    name: itcast
6.    age: 16
7.    tel: 4006184000
8.   subject:
9.     - Java
10.     - 前端
11.     - 大数据

Controller

方式一：使用@Value读取单一属性数据

1.  @RestController
2.  @RequestMapping("/books")
3.  public class BookController {
4.      _//使用@Value读取单一属性数据_
5.      @Value("${lesson}")
6.      private String lesson;
7.      @Value("${server.port}")
8.      private Integer port;
9.      @Value("${enterprise.subject\[0\]}")
10.     private String subject_00;

11.     @GetMapping("/{id}")
12.     public String getById(@PathVariable Integer id){
13.         System.out.println(lesson);
14.         System.out.println(port);
15.         System.out.println(subject_00);
16.         return "hello , spring boot!";
17.     }

18. }

方式二：使用Environment封装全配置数据

1.      _//使用Environment封装全配置数据_
2.      @Autowired
3.      private Environment environment;

4.          System.out.println("--------------------");
5.          System.out.println(environment.getProperty("lesson"));
6.          System.out.println(environment.getProperty("server.port"));
7.          System.out.println("---------------------");

案例：使用enterprise实体封装yaml数据

1.  _//封装yaml对象格式数据必须先声明当前实体类受Spring管控_
2.  @Component
3.  _//使用@ConfigurationProperties注解定义当前实体类读取配置属性信息，通过prefix属性设置读取哪个数据_
4.  @ConfigurationProperties(prefix = "enterprise")
5.  public class Enterprise {
6.      private String name;
7.      private Integer age;
8.      private String tel;
9.      private String\[\] subject;
10.     ...
11. }

Enterprise已有bean 可以自动装配enterprise

1.      @Autowired
2.      private Enterprise enterprise;

输出

1.          System.out.println(environment.getProperty("enterprise.age"));
2.          System.out.println(environment.getProperty("enterprise.subject\[1\]"));
3.          System.out.println(enterprise);

#### 多环境启动

##### 配置

1.  在application.yaml中配置
2.  _#设置启用的环境_
3.  spring:
4.    profiles:
5.      active: dev

6.  \---
7.  _#开发_
8.  spring:
9.   config:
10.     activate:
11.       on-profile: dev
12. server:
13.   port: 80
14. \---
15. _#生产_
16. spring:
17.   profiles: pro
18. server:
19.   port: 81
20. \---
21. _#测试_
22. spring:
23.   profiles: test
24. server:
25.   port: 82
26. \---
27. 使用.properties配置

主启动配置文件application.properties

spring.profiles.active=pro

环境分类配置文件application-dev.properties

server.port=8080

环境分类配置文件application-pro.properties

server.port=8081

##### 多环境启动命令格式

先clean再package

带参数启动SpringBoot

Java -jar springboot.jar --spring.profile.active=test

##### 多环境开发兼容问题

Maven中设置多环境属性

1.  <profiles>
2.          _<!--开发环境-->_
3.          <profile>
4.              <id>dev</id>
5.              <properties>
6.                  <profile.active>dev</profile.active>
7.              </properties>
8.          </profile>
9.          _<!--生产环境-->_
10.         <profile>
11.             <id>pro</id>
12.             <properties>
13.                 <profile.active>pro</profile.active>
14.             </properties>
15.             <activation>
16.                 <activeByDefault>true</activeByDefault>
17.             </activation>
18.         </profile>
19.         _<!--测试环境-->_
20.         <profile>
21.             <id>test</id>
22.             <properties>
23.                 <profile.active>test</profile.active>
24.             </properties>
25.         </profile>
26.     </profiles>

SpringBoot中应用Maven属性

1.  _#设置启用的环境_
2.  spring:
3.    profiles:
4.      active: ${profile.active}

Maven指令执行package指令，但没有编译，生成了对应的包，其中类参与编译，但是配置文件并没有编译，而是复制到包中

解决：对于源码中非java类对的操作要求加载Maven对应的属性，解析${}占位符

需要配置maven插件，对资源文件开启对默认占位符的解析

1.  <plugin>
2.                  <groupId>org.apache.maven.plugins</groupId>
3.                  <artifactId>maven-resources-plugin</artifactId>
4.                  <version>3.2.0</version>
5.                  <configuration>
6.                      <encoding>UTF-8</encoding>
7.                      <useDefaultDelimiters>true</useDefaultDelimiters>
8.                  </configuration>
9.              </plugin>

#### 配置文件分类

SpringBoot中4级配置文件

1级：file：config/application.yml \[最高\] （在文件位置中）

2级：file：application.yml

3级：classpath：config/application.yml （在idea中）

4级：classpath：application.yml

1级与2级留做系统打包后设置通用属性

3级与4级留做系统开发阶段设置通用属性

### 整合第三方技术

#### 整合Junit

Spring整合Junit

1.  _//设置类运行器_
2.  @RunWith(SpringJUnit4ClassRunner.class)
3.  _//设置Spring环境对应的配置类_
4.  @ContextConfiguration(classes = SpringConfig.class)
5.  public class AccountServiceTest {
6.      _//支持自动装配注入bean_
7.      @Autowired
8.      private AccountService accountService;

9.     @Test
10.     public void testFindById(){
11.         System.out.println(accountService.findById(1));
12.     }

13.     @Test
14.     public void testFindAll(){
15.         System.out.println(accountService.findAll());
16.     }
17. }

SpringBootTest整合

如果测试类在SpringBoot启动类的包或子包中，可以省略启动类的设置，也就是省略classes设定

1.  @SpringBootTest
2.  class Springboot07TestApplicationTests {

3.      @Autowired
4.      private BookService bookService;

5.      @Test
6.      public void save() {
7.          bookService.save();
8.     }

9. }

如果不放在同一包下，指定地址

1.  @SpringBootTest(classes = Springboot07TestApplication.class)

#### 整合mybatis

基于SpringBoot实现SSM整合

[Spring整合MyBatis](#_Spring整合MyBatis)

- SpringConfig
- 导入JdbcConfig
- 导入MyBatisConfig
- JdbcConfig
- 定义数据源（加载properties配置项：driver，url，username，password）
- MyBatisConfig
- 定义SqlsessionFactoryBean
- 定义映射配置

SpringBoot整合myBatis

BookDao

1.  @Mapper
2.  public interface BookDao {
3.      @Select("select \* from tbl_book where id = #{id}")
4.      public Book getById(Integer id);
5.  }

Application.yml

1.  spring:
2.    datasource:
3.      driver-class-name: com.mysql.cj.jdbc.Driver
4.      url: jdbc:mysql://localhost:3306/ssm_db?serverTimezone=UTC
5.      username: root
6.      password: root
7.      type: com.alibaba.druid.pool.DruidDataSource

type属性配置数据源 SpringBoot版本2.4.3（不含）之前需要配置timezone

### 案例：基于SpringBoot的SSM整合案例

pom.xml

配置起步依赖，必要的资源坐标

Application.yml

设置数据源，接口等

配置类

全部删除

Dao

设置@Mapper

测试类

自动生成

git sparse-checkout init --cone

git sparse-checkout set 04-springboot/code/springboot

git clone --filterblob:none https://github.com/CrRdz/Learning_SSM.git

## MyBatisPlus

### MyBatisPlus简介

- MyBatisPlus（MP）是基于MyBatis框架基础上开发的增强型工具，旨在简化开发，提高效率
- 开发方式：

基于MyBatis使用MyBatisPlus/基于Spring使用MyBatisPlus/基于SpringBoot使用MyBatisPlus

- SpringBoot整合MyBatis开发过程
- 创建SpringBoot工程
- 勾选配置使用的技术
- 设置dataSource相关属性（JDBC参数）
- 定义数据层接口映射配置

- MyBatisPlus快速入门

手动添加mp起步依赖

1.          <dependency>
2.              <groupId>com.baomidou</groupId>
3.              <artifactId>mybatis-plus-boot-starter</artifactId>
4.              <version>3.4.1</version>
5.          </dependency>

由于mp并未被收录到idea的系统内置配置，无法直接选择加入

设置jdbc参数（application.yml）

1.  spring:
2.    datasource:
3.      type: com.alibaba.druid.pool.DruidDataSource
4.      driver-class-name: com.mysql.cj.jdbc.Driver
5.      url: jdbc:mysql://localhost:3306/mybatisplus_db?serverTimezone=UTC
6.      username: root
7.      password: root

制作实体类

定义数据接口，继承BaseMapper<User>

1.  @Mapper
2.  public interface UserDao extends BaseMapper<User> {
3.  }

- MyBatisPlus特性
- 无侵入：只做增强不做改变，不会对现有工程产生影响
- 强大的CRUD操作，内置通用Mapper，少量配置即可实现单表CRUD操作
- 支持Lambda：编写查询条件无需担心字段写错
- 支持主键自动生成
- 内置分页插件

### 标准数据层开发

#### 标准数据层CRUD功能

|     |     |     |
| --- | --- | --- |
| 功能  | 自定义接口 | MP接口 |
| 新增  | boolean save（T t） | Int insert（T t） |
| 删除  | boolean delete（int id） | Int deleteById（Serializable id） |
| 修改  | boolean update（T t） | Int updateById（T t） |
| 根据id查询 | T getById（int id） | T selectById（Serializable id） |
| 查询全部 | List<T> getAll（） | List<T> selectList（） |
| 分页查询 | PageInfo<T> getAll（int page,int size） | IPage<T> selectPage（Ipage<T> page） |
| 按条件查询 | List<T> getAll（Condition condition） | IPage<T> selectPage（Wrapper<T> queryWrapper） |

#### 快速开发实体类

导入坐标

1.          <dependency>
2.              <groupId>org.projectlombok</groupId>
3.              <artifactId>lombok</artifactId>
4.              <version>1.18.12</version>
5.          </dependency>

6.  @Data
7.  @NoArgsConstructor
8.  @AllArgsConstructor
9.  public class User {
10.      private Long id;
11.      private String name;
12.      private String password;
13.      private Integer age;
14.      private String tel;
15. }

16.  @Setter
17.  @Getter
18.  @ToString

等同@Data

#### 分页查询

配置分页拦截器作为Spring管理的bean

1.  @Configuration
2.  public class MpConfig {
3.      @Bean
4.      public MybatisPlusInterceptor mpInterceptor(){
5.          _//1.定义Mp拦截器_
6.          MybatisPlusInterceptor mpInterceptor = new MybatisPlusInterceptor();
7.          _//2.添加具体的拦截器_
8.          mpInterceptor.addInnerInterceptor(new PaginationInnerInterceptor());
9.          return mpInterceptor;
10.     }
11. }

测试类中执行分页查询

1.      @Test
2.      void testGetByPage(){
3.          _//IPage对象封装了分页操作相关的数据_
4.          IPage page  = new Page(2,3);
5.          userDao.selectPage(page,null);
6.          System.out.println("当前页码值："+page.getCurrent());
7.          System.out.println("每页显示数："+page.getSize());
8.          System.out.println("一共多少页："+page.getPages());
9.          System.out.println("一共多少条数据："+page.getTotal());
10.         System.out.println("数据："+page.getRecords());
11.     }

12.  _# 开启mp的日志（输出到控制台）_
13.  mybatis-plus:
14.    configuration:
15.      log-impl: org.apache.ibatis.logging.stdout.StdOutImpl

### DQL控制

#### 条件查询方式

MyBatisPlus将书写复杂的SQL查询条件进行了封装，使用编程的形式完成查询条件的组合

1.          _//方式一：按条件查询_
2.          QueryWrapper qw = new QueryWrapper();
3.          qw.lt("age",18);
4.          List<User> userList = userDao.selectList(qw);
5.          System.out.println(userList);

6.           _//方式二：lambda格式按条件查询_
7.          QueryWrapper<User> qw = new QueryWrapper<User>();
8.          qw.lambda().lt(User::getAge, 10);
9.         List<User> userList = userDao.selectList(qw);
10.         System.out.println(userList);

11.         _//方式三：lambda格式按条件查询_
12.         LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
13.         lqw.lt(User::getAge, 10);
14.         List<User> userList = userDao.selectList(lqw);
15.         System.out.println(userList);

链式编程

1.         LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
2.          _//并且关系：10到30岁之间_
3.          _//lqw.lt(User::getAge, 30).gt(User::getAge, 10);_
4.          _//或者关系：小于10岁或者大于30岁_
5.          lqw.lt(User::getAge, 10).or().gt(User::getAge, 30);
6.          List<User> userList = userDao.selectList(lqw);
7.          System.out.println(userList);

Null值处理

1.          LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
2.          _//先判定第一个参数是否为true，如果为true连接当前条件_
3.          lqw.lt(null != uq.getAge2(),User::getAge, uq.getAge2());
4.          lqw.gt(null != uq.getAge(),User::getAge, uq.getAge());

5.          List<User> userList = userDao.selectList(lqw);
6.          System.out.println(userList);

#### 查询投影

查询结果包含属性类中部分模型

1.          _//查询投影_
2.          LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
3.          lqw.select(User::getId,User::getName,User::getAge);
4.          List<User> userList = userDao.selectList(lqw);
5.          System.out.println(userList);

使用QueryWrapper

1.          QueryWrapper<User> lqw = new QueryWrapper<User>();
2.          lqw.select("id","name","age","tel");

查询结果包含模型类中未定义的属性

1.          QueryWrapper<User> lqw = new QueryWrapper<User>();
2.          lqw.select("count(\*) as count, tel");
3.          lqw.groupBy("tel");
4.          List<Map<String, Object>> userList = userDao.selectMaps(lqw);
5.          System.out.println(userList);

如果有不支持的，去UserDao中使用原生MyBatis

#### 查询条件设定

查询条件

精确查询，查询单个

1.          LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
2.          _//等同于=_
3.          lqw.eq(User::getName,"Jerry").eq(User::getPassword,"jerry");
4.          User loginUser = userDao.selectOne(lqw);
5.          System.out.println(loginUser);

范围查询

1.          LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
2.          _//范围查询 lt le gt ge eq between_
3.          lqw.between(User::getAge,10,30);
4.          List<User> userList = userDao.selectList(lqw);
5.          System.out.println(userList);

前面小值后面大值

模糊匹配

1.          LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
2.          _//模糊匹配 like_
3.          lqw.likeLeft(User::getName,"J");
4.          List<User> userList = userDao.selectList(lqw);
5.          System.out.println(userList);

#### 字段映射与表名映射

##### 问题一：表字段与编码属性设计不同步

@TableFiled 属性注解 模型类属性定义上方

设置当前属性对应的数据表中的字段关系

@TableField（value= “pwd”）

##### 问题二：编码中添加了数据库中未定义的属性

@TableFiled（exist = false）设置属性在数据库字段中是否存在，默认为true，此属性无法与value合并使用

##### 问题三：采用默认查询开放了更多的字段查看权限

@TableFiled（select = false）设置属性是否参与查询，与select（）映射配置不冲突

问题四：表名与编码开发设计不同步

@TableName（“”）设置当前类与表格的关系

### DML控制

#### id生成策略控制

不同的表应用不同的id生成策略

- 日志：自增（1，2，3，4，...）
- 购物订单：特殊规则（FQ23948AK3843）
- 外卖单：关联地区日期等信息（10 04 20200314 34 91）
- 关联表：可省略id

...

@TableId

位置：模型类中用于表示主键的属性定义上方

作用：设置当前类中主键属性的生成策略

@TableId(type = IdType.XXXXX)

属性值选择：

AUTO（0）：使用数据库id自增策略控制id生成

NONE（1）：不设置id生成策略

INPUT（2）：用户手工输入id

ASSIGN_ID（3）：雪花算法生成id（可兼容数值型与字符串型）

ASSIGN_UUID（4）：以UUID生成算法作为id生成策略

1.  mybatis-plus:
2.    configuration:
3.      log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
4.    global-config:
5.      banner: false
6.      db-config:
7.        id-type: assign_id
8.         table-prefix: tbl_

yml设定全局设定，让每一个实体类都使用相同的策略

使用prefix全局设定表名前缀

#### 多记录操作

##### 根据主键删除多条记录/根据主键查询多条记录

1.          _//删除指定多条数据_
2.          List<Long> list = new ArrayList<>();
3.          list.add(1402551342481838081L);
4.          list.add(1402553134049501186L);
5.          list.add(1402553619611430913L);
6.          userDao.deleteBatchIds(list);
7.          _//查询指定多条数据_
8.          List<Long> list = new ArrayList<>();
9.          list.add(1L);
10.         list.add(3L);
11.         list.add(4L);
12.         userDao.selectBatchIds(list);

##### 逻辑删除

例如员工离职，但是不能删除对应员工业绩

删除操作业务问题：业务数据从数据库中丢弃

逻辑删除：为数据设置是否可用状态字段，删除时设置状态字段为不可用状态，数据保留在数据库中

1.      _//逻辑删除字段，标记当前记录是否被删除_
2.      @TableLogic(value = "0" ,delval = "1")
3.      private Integer deleted;

但进行查询操作时，会默认查询没有被逻辑删除的部分

对于Line2的优化：

1.        _# 逻辑删除字段名_
2.        logic-delete-field: deleted
3.        _# 逻辑删除字面值：未删除为0_
4.        logic-not-delete-value: 0
5.        _# 逻辑删除字面值：删除为1_
6.        logic-delete-value: 1

在yaml中配置逻辑删除字段名与删除字面值

##### 乐观锁

业务并发现象带来的问题：秒杀

1.      @Version
2.      private Integer version;

实现乐观锁

1.  @Configuration
2.  public class MpConfig {
3.      @Bean
4.      public MybatisPlusInterceptor mpInterceptor() {
5.          _//1.定义Mp拦截器_
6.          MybatisPlusInterceptor mpInterceptor = new MybatisPlusInterceptor();
7.          _//2.添加具体的拦截器_
8.          mpInterceptor.addInnerInterceptor(new PaginationInnerInterceptor());
9.          _//3.添加乐观锁拦截器_
10.         mpInterceptor.addInnerInterceptor(new OptimisticLockerInnerInterceptor());
11.         return mpInterceptor;
12.     }
13. }

添加乐观锁

1.      @Test
2.      void testUpdate(){

3.          _//1.先通过要修改的数据id将当前数据查询出来_
4.          User user = userDao.selectById(3L);     _//version=3_
5.          User user2 = userDao.selectById(3L);    _//version=3_

6.          user2.setName("Jock aaa");
7.          userDao.updateById(user2);              _//version=>4_

8.          user.setName("Jock bbb");
9.          userDao.updateById(user);               _//verion=3?条件不成立_
10.      }

使用乐观锁机制再修改前必须先获取到对应数据的version方可正常进行

### 快速开发

代码生成器

模板：由MyBatisPlus提供

数据库相关配置：读取数据库获取信息

开发者自定义配置：手工配置

1.          _<!--代码生成器-->_
2.          <dependency>
3.              <groupId>com.baomidou</groupId>
4.              <artifactId>mybatis-plus-generator</artifactId>
5.              <version>3.4.1</version>
6.          </dependency>

7.          _<!--velocity模板引擎-->_
8.          <dependency>
9.             <groupId>org.apache.velocity</groupId>
10.             <artifactId>velocity-engine-core</artifactId>
11.             <version>2.3</version>
12.         </dependency>

Generator

1.  public class CodeGenerator {
2.      public static void main(String\[\] args) {
3.          _//1.获取代码生成器的对象_
4.          AutoGenerator autoGenerator = new AutoGenerator();

5.          _//设置数据库相关配置_
6.          DataSourceConfig dataSource = new DataSourceConfig();
7.          dataSource.setDriverName("com.mysql.cj.jdbc.Driver");
8.          dataSource.setUrl("jdbc:mysql://localhost:3306/mybatisplus_db?serverTimezone=UTC");
9.         dataSource.setUsername("root");
10.         dataSource.setPassword("root");
11.         autoGenerator.setDataSource(dataSource);

12.         _//设置全局配置_
13.         GlobalConfig globalConfig = new GlobalConfig();
14.         globalConfig.setOutputDir(System.getProperty("user.dir")+"/mybatisplus_04_generator/src/main/java");    _//设置代码生成位置_
15.         globalConfig.setOpen(false);    _//设置生成完毕后是否打开生成代码所在的目录_
16.         globalConfig.setAuthor("黑马程序员");    _//设置作者_
17.         globalConfig.setFileOverride(true);     _//设置是否覆盖原始生成的文件_
18.         globalConfig.setMapperName("%sDao");    _//设置数据层接口名，%s为占位符，指代模块名称_
19.         globalConfig.setIdType(IdType.ASSIGN_ID);   _//设置Id生成策略_
20.         autoGenerator.setGlobalConfig(globalConfig);

21.         _//设置包名相关配置_
22.         PackageConfig packageInfo = new PackageConfig();
23.         packageInfo.setParent("com.aaa");   _//设置生成的包名，与代码所在位置不冲突，二者叠加组成完整路径_
24.         packageInfo.setEntity("domain");    _//设置实体类包名_
25.         packageInfo.setMapper("dao");   _//设置数据层包名_
26.         autoGenerator.setPackageInfo(packageInfo);

27.         _//策略设置_
28.         StrategyConfig strategyConfig = new StrategyConfig();
29.         strategyConfig.setInclude("tbl_user");  _//设置当前参与生成的表名，参数为可变参数_
30.         strategyConfig.setTablePrefix("tbl_");  _//设置数据库表的前缀名称，模块名 = 数据库表名 - 前缀名  例如： User = tbl_user - tbl__
31.         strategyConfig.setRestControllerStyle(true);    _//设置是否启用Rest风格_
32.         strategyConfig.setVersionFieldName("version");  _//设置乐观锁字段名_
33.         strategyConfig.setLogicDeleteFieldName("deleted");  _//设置逻辑删除字段名_
34.         strategyConfig.setEntityLombokModel(true);  _//设置是否启用lombok_
35.         autoGenerator.setStrategy(strategyConfig);
36.         _//2.执行生成操作_
37.         autoGenerator.execute();
38.     }
39. }

