# 技术栈

- Javaweb：[[MySQL]]，[[JDBC]]，Maven，MyBatis，HTML，CSS，JavaScript，JSP，AJAX，Axios，VUE，ElementUI，Git
- SSM：Spring，SpringMVC，Maven advanced，SpringBoot，MyBatisPlus
- [[Linux]]
- [[Redis]]：redis，redission，LuaScript，Lombok
- SpringBoot3 + VUE3


# SpringBoot3 + VUE3

该课程为SSM的后置课程

## 基础篇

### SpringBoot概述

- SpringBoot是Spring提供的一个子项目，用于快速构建Spring应用程序
- 传统方式构建spring应用程序：导入配置繁琐/项目配置繁琐
- 起步依赖:本质上就是一个Maven坐标，整合了完成一个功能需要的所有坐标
- 自动配置：遵循约定大约配置的原则，在boot程序启动后，一些bean对象会自动注入到ioc容器，不需要手动声明，简化开发
- 其他特性：内嵌Tomcat，Jetty（无需部署WAR文件）外部化配置，不需要XML配置（propertirs/yaml）

### SpringBoot入门

需求：使用SpringBoot开发一个web应用，浏览器发起/hello请求后，给浏览器返回hello world字符串

- 创建Maven工程
- 导入spring-boot-starter-web起步依赖
- 编写Controller

1.  @RestController
2.  public class HelloController {

4.      @RequestMapping("/hello")
5.      public String hello(){
6.          return "hello world";
7.      }
8.  }

- 提供启动类

1.  @SpringBootApplication
2.  public class SpringbootQuickstartApplication {

4.      public static void main(String\[\] args) {
5.          SpringApplication.run(SpringbootQuickstartApplication.class, args);
6.      }
7.  }

### 配置文件

- SpringBoot提供了多种属性配置方式
- Application.properties
- Application.yml/application.yaml（层次清晰，配置简单）
- Yml配置信息书写与获取
- 三方配置信息
- 自定义配置信息
- 值前边必须有空格，作为分隔符
- 使用空格作为缩进标识层级关系，相同的层级左侧对齐

1.  _#发件人相关的信息_
2.  email:
3.    user: 593140521@qq.com
4.    code: jfejwezhcrzcbbbb
5.    host: smtp.qq.com
6.    auth: true

在实体类中，使用注解获取

@Value（"${键名}"）

Or 指定前缀 前缀与配置文件中的保持一致

@ConfigurationProperties(prefix = "email")

### SpringBoot整合mybatis

引入起步依赖

1.          _&lt;!--mysql驱动依赖--&gt;_
2.          &lt;dependency&gt;
3.              &lt;groupId&gt;com.mysql&lt;/groupId&gt;
4.              &lt;artifactId&gt;mysql-connector-j&lt;/artifactId&gt;
5.          &lt;/dependency&gt;

7.          _&lt;!--mybatis的起步依赖--&gt;_
8.          &lt;dependency&gt;
9.              &lt;groupId&gt;org.mybatis.spring.boot&lt;/groupId&gt;
10.             &lt;artifactId&gt;mybatis-spring-boot-starter&lt;/artifactId&gt;
11.             &lt;version&gt;3.0.0&lt;/version&gt;
12.         &lt;/dependency&gt;

配置yml文件

1.  spring:
2.    datasource:
3.      driver-class-name: com.mysql.cj.jdbc.Driver
4.      url: jdbc:mysql://localhost:3306/mybatis
5.      username: root
6.      password: 1234

### Bean管理

#### Bean扫描

- 标签：&lt;context:component-scan base-package=”com.itheima”/&gt;
- 注解：@componentScan（basePackages = “com.itheima”）
- @SpringBootApplication 是一个组合注解，组合了三个注解：@ComponentScan ，@EnableAutoConfiguation，@SpringBootConfiguration
- 如果不指定扫描路径，默认扫描启动类所在的包及其子包

#### Bean注册

（注册第三方bean对象）

|     |     |     |
| --- | --- | --- |
| 注解  | 说明  | 位置  |
| @component | 声明bean的基础注解 | 不属于以下三类，用此注解 |
| @controller | @component的衍生注解 | 标注在控制器类上 |
| @Service | @component的衍生注解 | 标注在业务类上 |
| @Repository | @component的衍生注解 | 标注在数据访问类上（由于与mybatis整合，用的少） |

如果要注册的bean对象来自于第三方（不是自定义的），是无法用@Component及衍生注解声明bean的

@Bean

1.  @SpringBootApplication
2.  public class SpringbootRegisterApplication {

4.      public static void main(String\[\] args) {
5.         @Bean _//将方法返回值交给IOC容器管理，称为IOC容器的bean对象_
6.         public Resolver resolver(){
7.            return new Resolver();
8.      }
9.  }

但是并不推荐，启动类中尽量保持功能单一，如果要注册第三方bean，建议在配置类中集中注册

@Import

- 导入配置类
- 导入ImportSelector接口实现类 -> @EnableXxxx注解 封装@Import注解

@Import 注解可以让你把第三方类（比如别人写的配置类、工具类等）直接注册到 Spring 容器里，变成 Bean。这样你就能在项目里直接用这些 Bean，而不用自己写 @Component 或 @Configuration。用法很简单，比如你有个第三方类 CommonConfig，只要在你的启动类或配置类上加：

@Import(CommonConfig.class)

Spring 就会自动把 CommonConfig 注册为 Bean。如果你导入的是第三方包里的类，也一样用 @Import，不需要改第三方代码。

#### 注册条件

1.      _//注入Country对象_
2.      @Bean
3.      public Country country(@Value("${country.name}") String name,@Value("${country.system}") String system){
4.          Country country = new Country();
5.          country.setName(name);
6.          country.setSystem(system);
7.          return country ;
8.      }

使用@value注入

但是如果yml文件中没有配置，就会报错，Springboot提供了设置注册生效条件的注解@Conditional

|     |     |
| --- | --- |
| 注解  | 说明  |
| @ConditionOnProperty | 配置文件中存在对应的属性，才声明bean |
| @ConditionalOnMissingBean | 当不存在当前类型的bean时，才声明该bean |
| @ConditionalOnClass | 当前环境存在指定的这个类时，才声明该bean |

1.     _//如果配置文件中配置了指定的信息,则注入,否则不注入_
2.     @ConditionalOnProperty(prefix = "country",name = {"name","system"})

1.  _//如果ioc容器中不存在Country,则注入Province,否则不注入_
2.      @Bean
3.      @ConditionalOnMissingBean(Country.class)
4.      public Province province(){
5.          return new Province();
6.      }

需要根据配置文件参数决定是否启用某个功能（如 @ConditionalOnProperty）

只有在某个类存在时才注册 Bean（如集成第三方库时用 @ConditionalOnClass）

避免重复注册 Bean（如 @ConditionalOnMissingBean，只在容器没有某个 Bean 时注册）

根据不同环境或依赖，灵活控制 Bean 的创建，提升项目的可扩展性和定制性

1.   @Bean
2.      _//如果当前环境中存在DispatcherServlet类,则注入Province,否则不注入_
3.      _//如果当前引入了web起步依赖,则环境中有DispatcherServlet,否则没有_
4.      @ConditionalOnClass(name = "org.springframework.web.servlet.DispatcherServlet")
5.      public Province province(){
6.          return new Province();
7.      }

### 自动配置原理

自动配置：遵循约定大约配置的原则，在boot程序启动后，起步依赖中的一些bean对象会自动注入到ioc容器

程序引入spring-boot-starter-web起步依赖，启动后，会自动往ioc中注入DispatcherServlet这个bean对象

Spring Boot 自动装配原理解析  
1\. @SpringBootApplication  
我们平常写 Spring Boot 程序入口的时候，都会在启动类上加：

1.  @SpringBootApplication
2.  public class MyApp {
3.      public static void main(String\[\] args) {
4.          SpringApplication.run(MyApp.class, args);
5.      }
6.  }

  
这个注解本质上是一个组合注解，里面包含了：  
\- \`@SpringBootConfiguration\`（其实就是 \`@Configuration\`）  
\- \`@ComponentScan\`（扫描 \`@Component\`, \`@Service\`, \`@Controller\`…）  
\- \`@EnableAutoConfiguration\`（重点！开启自动配置）  

2\. @EnableAutoConfiguration  
核心是这个注解：  
@EnableAutoConfiguration  
它内部用了：  
@Import(AutoConfigurationImportSelector.class)  
意味着会调用 \`AutoConfigurationImportSelector\` 的 \`selectImports(...)\` 方法。  
\`selectImports\` 方法会返回一堆需要被导入到容器的配置类（xxxAutoConfiguration）。  
<br/>3\. META-INF/spring.factories（或 spring-autoconfigure-metadata）  
这些 \`xxxAutoConfiguration\` 类是怎么找到的？  
在 \`spring-boot-autoconfigure\` 包的 \`META-INF\` 目录下有个文件：  
org.springframework.boot.autoconfigure.AutoConfiguration.imports  
或老版本用 \`spring.factories\`。  
里面写着所有能被自动装配的配置类，比如：  
<br/>org.springframework.boot.autoconfigure.web.servlet.DispatcherServletAutoConfiguration  
org.springframework.boot.autoconfigure.web.servlet.ServletWebServerFactoryAutoConfiguration  
org.springframework.boot.autoconfigure.web.servlet.ErrorMvcAutoConfiguration  
...  
Spring Boot 启动时会把这些类都加载进来。  
<br/>4\. 以 DispatcherServletAutoConfiguration 为例  
<br/>图里展示了其中一个自动配置类：

1.  @AutoConfiguration
2.  @ConditionalOnClass(DispatcherServlet.class)
3.  public class DispatcherServletAutoConfiguration {

5.      @Configuration
6.      protected static class DispatcherServletConfiguration {
7.          @Bean
8.          public DispatcherServlet dispatcherServlet() {
9.              return new DispatcherServlet();
10.         }
11.     }
12. }

  
关键点：  
\- \`@AutoConfiguration\`：表明这是一个自动配置类  
\- \`@ConditionalOnClass(DispatcherServlet.class)\`：\*\*条件装配\*\*，只有当 classpath 里有 \`DispatcherServlet\` 类时，这个配置才生效  
\- 定义了一个 \`@Bean\` 方法，往容器里注册 \`DispatcherServlet\`  
这样，Spring Boot 在 web 环境下，就会自动帮我们配置好 \`DispatcherServlet\`，不需要手动写配置类。  

总结流程  
入口类上的 \`@SpringBootApplication\` → 激活 \`@EnableAutoConfiguration\`  
\`@EnableAutoConfiguration\` → 通过 \`@Import(AutoConfigurationImportSelector.class)\` 调用 \`selectImports(...)\`  
\`selectImports(...)\` → 去 \`META-INF/spring.factories\` 或 \`AutoConfiguration.imports\` 文件里读取所有自动配置类  
加载这些自动配置类（比如 \`DispatcherServletAutoConfiguration\`）  
每个自动配置类里通过 \`@ConditionalOnXxx\` 判断条件，决定是否往 IOC 容器注册对应的 Bean  
最终，Spring Boot 就实现了 按需自动装配，我们什么都没写，但容器里已经有了很多默认的 Bean。

自动配置（装配）与@Autowired的之间关系  
  
使用这样的操作使其能够实现自动装配

原来1.0的版本需要使用@import进行bean注册，这里就不需要了 相当于一个封装操作，就比如StringRedisTemplate 可以直接通过@Autowired注入

SpringBoot自动配置原理

### 自定义starter

1.  @AutoConfiguration_//表示当前类是一个自动配置类_
2.  public class MyBatisAutoConfig {

4.      _//SqlSessionFactoryBean_
5.      @Bean
6.      public SqlSessionFactoryBean sqlSessionFactoryBean(DataSource dataSource){
7.          SqlSessionFactoryBean sqlSessionFactoryBean = new SqlSessionFactoryBean();
8.          sqlSessionFactoryBean.setDataSource(dataSource);
9.          return sqlSessionFactoryBean;
10.     }

12.     _//MapperScannerConfigure_
13.     @Bean
14.     public MapperScannerConfigurer mapperScannerConfigurer(BeanFactory beanFactory){
15.         MapperScannerConfigurer mapperScannerConfigurer = new MapperScannerConfigurer();
16.         _//扫描的包:启动类所在的包及其子包_
17.         List&lt;String&gt; packages = AutoConfigurationPackages.get(beanFactory);
18.         String p = packages.get(0);
19.         mapperScannerConfigurer.setBasePackage(p);

21.         _//扫描的注解_
22.         mapperScannerConfigurer.setAnnotationClass(Mapper.class);
23.         return mapperScannerConfigurer;
24.     }
25. }

导入imports

在dmybatis-spring-boot-starter进行依赖管理，导入依赖及其的依赖

## 实战-后端篇

### 开发模式

### 环境搭建

执行资料中的big_event.sql脚本，准备数据库表

导入实体类

创建conroller，mapper，pojo，service，service.impl，utils包

### 用户类接口

#### 注册接口

UserController

1.  @RestController
2.  @RequestMapping("/user")
3.  public class UserController {

5.      @Autowired
6.      private UserService userService;
7.      @PostMapping("/register")
8.      public Result register(String username, String password){
9.              _//1.查询用户_
10.             User u = userService.findByUsername(username);
11.             if (u == null) {
12.                 _//2.没有用户，注册用户_
13.                 userService.register(username, password);
14.                 return Result.success("注册成功");
15.             } else {
16.                 _//3.有用户，返回用户已存在_
17.                 return Result.error("用户已被占用");
18.             }
19.         }
20.     }
21. }

UserService

1.  public interface UserService {

3.      _//根据用户名查询用户_
4.      User findByUsername(String username);

6.      _//用户注册_
7.      void register(String username, String password);
8.  }

UserServiceImpl

1.  @Service
2.  public class UserServiceImpl implements UserService {

4.      @Autowired
5.      private UserMapper userMapper;
6.      @Override
7.      public User findByUsername(String username) {
8.          User u = userMapper.findByUsername(username);
9.          return u;
10.     }

12.     @Override
13.     public void register(String username, String password) {
14.         _//加密_
15.         String md5String = Md5Util.getMD5String(password);
16.         _//调用mapper层添加_
17.         userMapper.add(username,md5String);
18.     }
19. }

UserMapper

1.  @Mapper
2.  public interface UserMapper {
3.      _//根据用户名查询用户_
4.      @Select("select \* from user where username = #{username}")
5.      User findByUsername(String username);

7.      _//添加用户_
8.      @Insert("insert into user(username,password,create_time,update_time)" +
9.              " values(#{username},#{password},now(),now())")
10.     void add(String username, String password);
11. }

#### 注册接口参数校验

Register

1.      @PostMapping("/register")
2.      public Result register(String username, String password){
3.          if(username == null && username.length() >= 5 && username.length() <= 16 &&
4.          password != null && password.length() >= 5 && password.length() <= 16
5.          ) {
6.              _//1.查询用户_
7.              User u = userService.findByUsername(username);
8.              if (u == null) {
9.                  _//2.没有用户，注册用户_
10.                 userService.register(username, password);
11.                 return Result.success("注册成功");
12.             } else {
13.                 _//3.有用户，返回用户已存在_
14.                 return Result.error("用户已被占用");
15.             }
16.         }else {
17.             return Result.error("用户名或密码不符合规范");
18.         }
19.     }

但是步骤繁琐，SpringValidation提供了快捷的校验

引入SpringValidation起步依赖

1.        _&lt;!--validation依赖--&gt;_
2.        &lt;dependency&gt;
3.            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
4.            &lt;artifactId&gt;spring-boot-starter-validation&lt;/artifactId&gt;
5.        &lt;/dependency&gt;

在参数前面添加@Pattern注解

1.  @PostMapping("/register")
2.      public Result register(@Pattern(regexp = "^\\\\S{5,16}$")String username, @Pattern(regexp = "^\\\\S{5,16}$")String password){
3.          _//1.查询用户_
4.          User u = userService.findByUsername(username);
5.          if (u == null) {
6.              _//2.没有用户，注册用户_
7.              userService.register(username, password);
8.              return Result.success("注册成功");
9.          } else {
10.             _//3.有用户，返回用户已存在_
11.             return Result.error("用户已被占用");
12.         }
13.     }

在Controller类上添加@Validated注解

在全局异常处理器中处理校验异常的情况

1.  @RestControllerAdvice
2.  public class GlobalExpectionHandler {

4.      @ExceptionHandler(Exception.class)
5.      public Result handleException(Exception e) {
6.          e.printStackTrace();
7.          return Result.error(StringUtils.hasLength(e.getMessage())?e.getMessage():"操作失败");
8.      }
9.  }

#### 登录接口

UserController

1.      @PostMapping("/login")
2.      public Result&lt;String&gt; login(@Pattern(regexp = "^\\\\S{5,16}$")String username, @Pattern(regexp = "^\\\\S{5,16}$")String password){
3.          _//1.根据用户名查询用户_
4.          User loginUser = userService.findByUsername(username);
5.          _//2.判断用户是否存在_
6.          if(loginUser == null) {
7.              return Result.error("用户名错误");
8.          }
9.          _//3.判断密码是否正确_
10.         if(Md5Util.getMD5String(password).equals(loginUser.getPassword())){
11.             return Result.success("jwt token令牌 ...");
12.         }

14.         return Result.error("密码错误");
15.     }

##### 登录验证

- 现状：在未登录的情况下，可以访问到其他资源
- 使用令牌来确认登录状态，令牌就是一段字符串，承载业务数据，减少后续请求查询数据库的次数，防篡改，保证信息的合法性和有效性
- JWT（Json Web Token）定义了一种简介的，自包含的格式，用于通信双方以json数据格式安全的传输信息
- 组成：第一部分：Header头，记录令牌类型，签名算法 第二部分：payLoad有效载荷，携带一些自定义的信息，默认信息等等 第三部分：Signature签名，防止token被篡改，确保安全性，将header，payload，并加入指定密钥，通过指定签名算法计算而来

1.      @Test
2.      public void testGen(){
3.          Map&lt;String,Object&gt; claims = new HashMap<>();
4.          claims.put("id",1);
5.          claims.put("username","张三");
6.          _// 生成JWT的代码_
7.          String token = JWT.create()
8.                  .withClaim("user", claims)_//添加载荷_
9.                  .withExpiresAt(new Date(System.currentTimeMillis() + 1000 \* 60 \* 60 \* 12))_//添加过期时间_
10.                 .sign(Algorithm.HMAC256("itheima"));_//指定算法配置密钥_

12.         System.out.println(token);
13.     }

- JWT校验时使用的签名密钥，必须和生成JWT密钥时，使用的密钥是配套的
- 如果JWT令牌解析校验错误时报错，则说明JWT令牌被篡改，或失效了，令牌非法

1.      @Test
2.      public void testParse(){
3.          String token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" +
4.                  ".eyJ1c2VyIjp7ImlkIjoxLCJ1c2VybmFtZSI6IuW8oOS4iSJ9LCJleHAiOjE3NTY0MzU0NjF9" +
5.                  ".sbb5WdiAMiZAWDU6TnVtft-ssKuLKcZTbXRMyih3fug";

7.          JWTVerifier jwtVerifier = JWT.require(Algorithm.HMAC256("itheima")).build();

9.          DecodedJWT decodedJWT = jwtVerifier.verify(token);_//验证token生成一个解析后的JWT对象_
10.         Map&lt;String, Claim&gt; claims = decodedJWT.getClaims();
11.         System.out.println(claims.get("user"));

13.     }

#### 登录拦截器优化登录验证

登录拦截器

1.  @Component
2.  public class LoginInterceptor implements HandlerInterceptor {

4.      @Override
5.      public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
6.          _//令牌验证_
7.          String token = request.getHeader("Authorization");
8.          try {
9.              Map&lt;String, Object&gt; claims = JwtUtil.parseToken(token);
10.             _//放行_
11.             return true;
12.         } catch (Exception e) {
13.             _//http响应状态码为401_
14.             response.setStatus(401);
15.             return false;
16.         }
17.     }
18. }

1.  @Configuration
2.  public class WebConfig implements WebMvcConfigurer {

4.      @Autowired
5.      private LoginInterceptor loginInterceptor;
6.      @Override
7.      public void addInterceptors(InterceptorRegistry registry) {
8.          _// 添加拦截器，登录接口和注册接口不拦截_
9.          registry.addInterceptor(loginInterceptor)
10.                 .addPathPatterns("/\*\*")
11.                 .excludePathPatterns("/user/login", "/user/register");
12.     }
13. }

这里这里没有自动将token存入Authorization的操作，使用postman手动地将token存入Authorization，我在拦截器中要求获取Authorization头中数据，这样就实现了登录校验，在后续开发中，自动存入Authorization的操作会由前端来完成

#### 获取用户详细信息接口

1.      @GetMapping("/userInfo")
2.      public Result&lt;User&gt; info(@RequestHeader(name = "Authorization") String token){
3.          _//1.根据用户名查询用户_
4.          Map&lt;String, Object&gt; map = JwtUtil.parseToken(token);
5.          String username = (String) map.get("username");

7.          User user = userService.findByUsername(username);
8.          return Result.success(user);
9.      }

开启驼峰命名

1.  mybatis:
2.    configuration:
3.      map-underscore-to-camel-case: true _# 开启驼峰命名_

ThreadLocal提供线程局部变量

- 用来存取数据：set()/get() 使用ThreadLocal存储的数据，线程安全
- 提供线程局部变量

##### 使用ThreadLocal优化获取用户详细信息

在登录拦截器中将用户数据存储到ThreadLocal中

1.  @Component
2.  public class LoginInterceptor implements HandlerInterceptor {

4.      @Override
5.      public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
6.          _//令牌验证_
7.          String token = request.getHeader("Authorization");
8.          try {
9.              Map&lt;String, Object&gt; claims = JwtUtil.parseToken(token);
10.             _//把业务数据存储到ThreadLocal_
11.             ThreadLocalUtil.set(claims);
12.             _//放行_
13.             return true;
14.         } catch (Exception e) {
15.             _//http响应状态码为401_
16.             response.setStatus(401);
17.             return false;
18.         }
19.     }

21.     @Override
22.     public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
23.         _//请求处理完成后，清空ThreadLocal中的数据_
24.         ThreadLocalUtil.remove();
25.     }

1.      @GetMapping("/userInfo")
2.      public Result&lt;User&gt; info(@RequestHeader(name = "Authorization") String token){
3.          _//1.根据用户名查询用户_
4.          Map&lt;String, Object&gt; map = ThreadLocalUtil.get();
5.          String username = (String) map.get("username");

7.          User user = userService.findByUsername(username);
8.          return Result.success(user);
9.      }

#### 更新用户基本信息接口

1.      @PutMapping("/update")
2.      public Result update(@RequestBody User user){
3.          userService.update(user);
4.          return Result.success();
5.      }

UserMapper

1.      @Update("update user set nickname = #{nickname},email = #{email},user_pic = #{userPic},update_time = now() where id = #{id}")
2.      void update(User user);

##### 实体参数校验

1.      @PutMapping("/update")
2.      public Result update(@RequestBody @Validated User user){
3.          userService.update(user);
4.          return Result.success();
5.      }

User

1.  @Data
2.  public class User {
3.      @NotNull
4.      private Integer id;_//主键ID_
5.      private String username;_//用户名_
6.      @JsonIgnore
7.      private String password;_//密码_

9.      @NotEmpty
10.     @Pattern(regexp = "^\\\\S{1,10}$")
11.     private String nickname;_//昵称_

13.     @NotEmpty
14.     @Email
15.     private String email;_//邮箱_
16.     private String userPic;_//用户头像地址_
17.     private LocalDateTime createTime;_//创建时间_
18.     private LocalDateTime updateTime;_//更新时间_
19. }

#### 更新用户头像接口

1.      @PatchMapping("/updateAvatar")
2.      public Result updateAvatar(@RequestParam @URL String avatarUrl){
3.          userService.updateAvatar(avatarUrl);
4.          return Result.success();
5.      }

1.      @Override
2.      public void updateAvatar(String avatarUrl) {
3.          Map&lt;String, Object&gt; map = ThreadLocalUtil.get();
4.          Integer id = (Integer) map.get("id");
5.          userMapper.updateAvatar(avatarUrl,id);
6.      }

1.      @Update("update user set user_pic = #{avatarUrl},update_time = now() where id = #{id}")
2.      void updateAvatar(String avatarUrl,Integer id);

#### 更新用户密码接口

1.      @PatchMapping("/updatePwd")
2.      public Result&lt;?&gt; updatePwd(@RequestBody Map&lt;String,String&gt; params){
3.          return userService.validateAndUpdatePwd(params);
4.      }

1.      @Override
2.      public Result&lt;?&gt; validateAndUpdatePwd(Map&lt;String, String&gt; params) {
3.          String oldPwd = params.get("old_pwd");
4.          String newPwd = params.get("new_pwd");
5.          String rePwd = params.get("re_pwd");

7.          if (!StringUtils.hasLength(oldPwd) || !StringUtils.hasLength(newPwd) || !StringUtils.hasLength(rePwd)) {
8.              return Result.error("缺少必要参数");
9.          }

11.         Map&lt;String, Object&gt; map = ThreadLocalUtil.get();
12.         String username = (String) map.get("username");
13.         User loginUser = findByUsername(username);
14.         if (!loginUser.getPassword().equals(Md5Util.getMD5String(oldPwd))) {
15.             return Result.error("原密码错误");
16.         }

18.         if (!rePwd.equals(newPwd)) {
19.             return Result.error("两次填写的新密码不一致");
20.         }

22.         updatePwd(newPwd);
23.         return Result.success();
24.     }

26.     public void updatePwd(String newPwd) {
27.         Map&lt;String, Object&gt; map = ThreadLocalUtil.get();
28.         Integer id = (Integer) map.get("id");
29.         userMapper.updatePwd(Md5Util.getMD5String(newPwd), id);
30.     }

### 文章分类接口

#### 新增文章分类接口

CategoryController

1.  @RestController
2.  @RequestMapping( "/category" )
3.  public class CategoryController {

5.      @Autowired
6.      private CategoryService categoryService;
7.      @PostMapping
8.      public Result add(@RequestBody @Validated Category category){
9.          categoryService.add(category);
10.         return Result.success();
11.     }
12. }

CategoryServiceImpl

1.      @Autowired
2.     private CategoryMapper categoryMapper;

4.  @Override
5.      public void add(Category category) {
6.          _//补充属性值_
7.          Map&lt;String, Object&gt; map = ThreadLocalUtil.get();
8.          Integer userId = (Integer) map.get("id");
9.          category.setCreateUser(userId);

11.         categoryMapper.add(category);
12.     }

CategoryMapper

1.      @Insert("insert into category(category_name,category_alias,create_user,create_time,update_time) " +
2.              "values(#{categoryName},#{categoryAlias},#{createUser},now(),now())")
3.      void add(Category category);

#### 文章分类列表接口

CategoryController

1.      @GetMapping
2.      public Result&lt;List<Category&gt;> list(){
3.          List&lt;Category&gt; list = categoryService.list();
4.          return Result.success(list);
5.      }

CategoryServiceImpl

1.      @Override
2.      public List&lt;Category&gt; list() {
3.          Map&lt;String, Object&gt; map = ThreadLocalUtil.get();
4.          Integer userId = (Integer) map.get("id");

6.          return categoryMapper.list(userId);
7.      }

CategoryMapper

1.      _//查询所有_
2.      @Select("select \* from category where create_user = #{userId}")
3.      List&lt;Category&gt; list(Integer userId);

#### 获取文章分类详情

CategoryController

1.      @GetMapping("/detail")
2.      public Result&lt;Category&gt; detail(Integer id){
3.          return Result.success(categoryService.findById(id));
4.      }

CategoryServiceImpl

1.      @Override
2.      public Category findById(Integer id) {
3.          return categoryMapper.findById(id);
4.      }

CategoryMapper

1.      _//根据id查询_
2.      @Select("select \* from category where id = #{id}")
3.      Category findById(Integer id);

#### 获取文章分类详情

1.      @GetMapping("/detail")
2.      public Result&lt;Category&gt; detail(Integer id){
3.          return Result.success(categoryService.findById(id));
4.      }

CategoryServiceImpl

1.      @Override
2.      public Category findById(Integer id) {
3.          return categoryMapper.findById(id);
4.      }

CategoryMapper

1.      _//根据id查询_
2.      @Select("select \* from category where id = #{id}")
3.      Category findById(Integer id);

#### 更新文章分类接口

1.      @PutMapping
2.      public Result update(@RequestBody @Validated Category category){
3.          categoryService.update(category);
4.          return Result.success();
5.      }

1.      @Override
2.      public void update(Category category) {
3.          categoryMapper.update(category);
4.      }

1.      _//更新_
2.      @Update("update category set category_name = #{categoryName},category_alias = #{categoryAlias},update_time = now() where id = #{id}")
3.      void update(Category category);

##### 分组校验

把校验项进行归类分组，在完成不同的功能的时候，校验指定组中的校验项

定义分组，定义校验项时指定归属的分组，校验时指定要校验的分组

1.      @PostMapping
2.      public Result add(@RequestBody @Validated(Category.Add.class) Category category){
3.          categoryService.add(category);
4.          return Result.success();
5.      }

7.      @PutMapping
8.      public Result update(@RequestBody @Validated(Category.Update.class) Category category){
9.          categoryService.update(category);
10.         return Result.success();
11.     }

Category

1.  @Data
2.  public class Category {
3.      @NotNull(groups = {Update.class})
4.      private Integer id;_//主键ID_
5.      @NotEmpty(groups = {Add.class,Update.class})
6.      private String categoryName;_//分类名称_
7.      @NotEmpty(groups = {Add.class,Update.class})
8.      private String categoryAlias;_//分类别名_
9.      private Integer createUser;_//创建人ID_
10.     @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
11.     private LocalDateTime createTime;_//创建时间_
12.     @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
13.     private LocalDateTime updateTime;_//更新时间_

15.     _//如果说某个校验项没有指定分组，默认属于Default分组_
16.     _//分组之间可以继承 A extends B 那么A中拥有B中所有的校验项_

18.     public interface Add extends Default {}
19.     public interface Update extends  Default{}
20. }

### 文章管理类接口

#### 新增文章

1.      @Autowired
2.      private ArticleService articleService;
3.      @PostMapping
4.      public Result add(@RequestBody Article article){
5.          articleService.add(article);
6.          return Result.success();
7.      }

ArticleServiceImpl

1.      @Override
2.      public void add(Article article) {
3.          Map&lt;String, Object&gt; map = ThreadLocalUtil.get();
4.          Integer userId = (Integer) map.get("id");
5.          article.setCreateUser(userId);

7.          articleMapper.add(article);
8.      }

ArticleMapper

1.      _//新增文章_
2.      @Insert("insert into article(title,content,cover_img,state,category_id,create_user,create_time,update_time) " +
3.              "values(#{title},#{content},#{coverImg},#{state},#{categoryId},#{createUser},now(),now())")
4.      void add(Article article);

###### 自定义校验

已有注解不能满足所有的校验需求，特殊的情况需要自定义校验（自定义校验注解）

- 自定义注解State

1.  @Documented//元注解
2.  @Constraint(validatedBy = { StateValidation.class})_//指定提供校验规则的类_
3.  @Target({FIELD})_//元注解_
4.  @Retention(RUNTIME)

6.  public @interface State {
7.      _//提供校验失败后的提示语_
8.      String message() default "{state参数的值只能是已发布或者草稿}";
9.      _//指定分组_
10.     Class&lt;?&gt;\[\] groups() default {};
11.     _//负载 获取到State注解的附加信息_
12.     Class&lt;? extends Payload&gt;\[\] payload() default {};
13. }

- 自定义校验数据的类StateValidation，实现ConstraintValidator接口

1.  public class StateValidation implements ConstraintValidator&lt;State,String&gt; {
2.      _/\*\*_
3.       \*
4.       \* @param value 将来要校验的数据
5.       \* @param context context in which the constraint is evaluated
6.       \*
7.       \* @return 如果返回false则校验失败
8.       \*/
9.      @Override
10.     public boolean isValid(String value, ConstraintValidatorContext context) {
11.         _//提供校验规则_
12.         if(value == null){
13.             return false;
14.         }
15.         if(value.equals("已发布") || value.equals("草稿")){
16.             return true;
17.         }
18.         return false;
19.     }
20. }

- 在需要校验的地方使用自定义注解

#### 文章列表（条件分页）

1.      @GetMapping
2.      public Result&lt;PageBean<Article&gt;> list(
3.              Integer pageNum,
4.              Integer pageSize,
5.              @RequestParam(required = false) Integer categoryId,
6.              @RequestParam(required = false) String state
7.      ){
8.          PageBean&lt;Article&gt; pageBean = articleService.list(pageNum,pageSize,categoryId,state);
9.          return Result.success(pageBean);
10.     }

ArticleServiceImpl

1.      @Override
2.      public PageBean&lt;Article&gt; list(Integer pageNum, Integer pageSize, Integer categoryId, String state) {
3.          _//1.创建PageBean对象_
4.          PageBean&lt;Article&gt; pb = new PageBean<>();
5.          _//2.开启分页查询_
6.          PageHelper.startPage(pageNum,pageSize);

8.          _//3.查询 调用mapper_
9.          Map&lt;String, Object&gt; map = ThreadLocalUtil.get();
10.         Integer userId = (Integer) map.get("id");
11.         List&lt;Article&gt; as = articleMapper.list(userId,categoryId,state);
12.         _//page中提供了方法，可以获取PageHelper分页查询后，得到的总记录条数和当前页的数据_
13.         Page&lt;Article&gt; p = (Page&lt;Article&gt;) as;

15.         _//4.封装到PageBean对象中_
16.         pb.setTotal(p.getTotal());
17.         pb.setItems(p.getResult());
18.         return pb;
19.     }

- 创建PageBean对象：创建用于封装分页结果的对象开启分页查询
- 使用PageHelper.startPage()设置分页参数
- 执行查询：从ThreadLocal中获取当前用户ID
- 调用articleMapper.list()方法查询文章列表，传入用户ID、分类ID和文章状态作为查询条件
- 类型转换：将查询结果转换为Page&lt;Article&gt;类型，以便获取分页信息
- 封装结果：设置总记录数和当前页数据到PageBean对象中

1.      &lt;select id="list" resultType="com.itheima.pojo.Article"&gt;
2.          select \* from article
3.          &lt;where&gt;
4.              &lt;if test="categoryId != null"&gt;
5.                  category_id = _#{categoryId}_
6.              &lt;/if&gt;

8.              &lt;if test="state != null"&gt;
9.                  and state = _#{state}_
10.             &lt;/if&gt;
11.             and create_user = _#{userId}_
12.         &lt;/where&gt;
13.     &lt;/select&gt;

### 文件上传接口

#### 本地存储

1.      @PostMapping("/upload")
2.      public Result&lt;String&gt; upload(MultipartFile file) throws IOException {
3.          _//把文件的内容保存到本地磁盘上_
4.          String originalFilename = file.getOriginalFilename();
5.          _//保证文件的名字是唯一的，从而防止文件覆盖_
6.          String filename = UUID.randomUUID().toString() + originalFilename.substring(originalFilename.lastIndexOf("."));
7.          file.transferTo(new File("F:\\\\Leaning_Java\\\\000-projects\\\\files\\\\" + filename));
8.          return Result.success("url访问地址...");
9.      }

存在问题：存储本地，不能直接在网络上访问，以及受制于本地磁盘的大小

#### 阿里云OSS

阿里云对象存储OSS（Object Storage Service），是一款海量安全低成本高可靠的云存储服务，使用OSS，可以通过网络随时存储和调用包括文本，图片，音频和视频等在内的各种文件

##### 第三方服务调用-通用思路

准备工作

|

参照官方SDK（软件开发工具包，包括辅助软件开发的依赖jar包，代码实例）编写入门程序

|

集成使用

1.  _&lt;!--阿里云oss依赖坐标--&gt;_
2.        &lt;dependency&gt;
3.            &lt;groupId&gt;com.aliyun.oss&lt;/groupId&gt;
4.            &lt;artifactId&gt;aliyun-sdk-oss&lt;/artifactId&gt;
5.            &lt;version&gt;3.17.4&lt;/version&gt;
6.        &lt;/dependency&gt;
7.        &lt;dependency&gt;
8.            &lt;groupId&gt;javax.xml.bind&lt;/groupId&gt;
9.            &lt;artifactId&gt;jaxb-api&lt;/artifactId&gt;
10.           &lt;version&gt;2.3.1&lt;/version&gt;
11.       &lt;/dependency&gt;
12.       &lt;dependency&gt;
13.           &lt;groupId&gt;javax.activation&lt;/groupId&gt;
14.           &lt;artifactId&gt;activation&lt;/artifactId&gt;
15.           &lt;version&gt;1.1.1&lt;/version&gt;
16.       &lt;/dependency&gt;
17.       _&lt;!-- no more than 2.3.3--&gt;_
18.       &lt;dependency&gt;
19.           &lt;groupId&gt;org.glassfish.jaxb&lt;/groupId&gt;
20.           &lt;artifactId&gt;jaxb-runtime&lt;/artifactId&gt;
21.           &lt;version&gt;2.3.3&lt;/version&gt;
22.       &lt;/dependency&gt;

AliOssUtil

1.  public class AliOssUtil {
2.      private static final String ENDPOINT = System.getenv("OSS_ENDPOINT");
3.      private static final String ACCESS_KEY_ID = System.getenv("OSS_ACCESS_KEY_ID");
4.      private static final String SECRET_ACCESS_KEY = System.getenv("OSS_ACCESS_KEY_SECRET");
5.      private static final String BUCKET_NAME = System.getenv("OSS_BUCKET");

7.      _//上传文件,返回文件的公网访问地址_
8.      public static String uploadFile(String objectName, InputStream inputStream){
9.          _// 创建OSSClient实例。_
10.         OSS ossClient = new OSSClientBuilder().build(ENDPOINT,ACCESS_KEY_ID,SECRET_ACCESS_KEY);
11.         _//公文访问地址_
12.         String url = "";
13.         try {
14.             _// 创建存储空间。_
15.             ossClient.createBucket(BUCKET_NAME);
16.             ossClient.putObject(BUCKET_NAME, objectName, inputStream);
17.             url = "https://" + BUCKET_NAME + "." + ENDPOINT.substring(ENDPOINT.lastIndexOf("/")+1) + "/"+objectName;
18.         } catch (OSSException oe) {
19.             System.out.println("Caught an OSSException, which means your request made it to OSS, "
20.                     + "but was rejected with an error response for some reason.");
21.             System.out.println("Error Message:" + oe.getErrorMessage());
22.             System.out.println("Error Code:" + oe.getErrorCode());
23.             System.out.println("Request ID:" + oe.getRequestId());
24.             System.out.println("Host ID:" + oe.getHostId());
25.         } catch (ClientException ce) {
26.             System.out.println("Caught an ClientException, which means the client encountered "
27.                     + "a serious internal problem while trying to communicate with OSS, "
28.                     + "such as not being able to access the network.");
29.             System.out.println("Error Message:" + ce.getMessage());
30.         } finally {
31.             if (ossClient != null) {
32.                 ossClient.shutdown();
33.             }
34.         }
35.         return url;
36.     }
37. }

FileUploadController

1.      @PostMapping("/upload")
2.      public Result&lt;String&gt; upload(MultipartFile file) throws IOException {
3.          _//把文件的内容保存到本地磁盘上_
4.          String originalFilename = file.getOriginalFilename();
5.          _//保证文件的名字是唯一的，从而防止文件覆盖_
6.          String filename = UUID.randomUUID().toString() + originalFilename.substring(originalFilename.lastIndexOf("."));
7.          _//file.transferTo(new File("F:\\\\Leaning_Java\\\\000-projects\\\\files\\\\" + filename));_
8.          String url = AliOssUtil.uploadFile(filename, file.getInputStream());
9.          return Result.success(url);
10.     }

### 使用redis优化登录

- Jwt令牌登录的弊端：登录时候会下发令牌，如果修改密码后，使用旧密码，旧密码应该作废，但是现在并没有作废令牌，使用旧令牌依然可以登录到账号，引入令牌主动失效机制（redis实现）
- 具体实现流程：
- 登录成功后，给浏览器响应令牌的同时，把令牌存储到redis中
- LoginInterceptor拦截器中，需要验证浏览器携带的令牌，并同时获取到redis中存储的与之相同的令牌
- 当用户修改密码成功后，删除redis中存储的旧令牌

#### SpringBoot集成redis

- 导入spring-boot-starter-data-redis起步依赖

1.        _&lt;!--redis坐标--&gt;_
2.        &lt;dependency&gt;
3.            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
4.            &lt;artifactId&gt;spring-boot-starter-data-redis&lt;/artifactId&gt;
5.        &lt;/dependency&gt;

- 在yml配置文件中配置redis连接信息
- 调用API（StringRedisTemplate）完成字符串的存取操作

LoginInterceptor

1.      @Override
2.      public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
3.          _//令牌验证_
4.          String token = request.getHeader("Authorization");
5.          try {
6.              _//从redis中获取token_
7.              String redisToken = stringRedisTemplate.opsForValue().get(token);
8.              if (redisToken == null) {
9.                  _//token已经失效了_
10.                 throw new RuntimeException();
11.             }
12.             Map&lt;String, Object&gt; claims = JwtUtil.parseToken(token);
13.             _//把业务数据存储到ThreadLocal_
14.             ThreadLocalUtil.set(claims);
15.             _//放行_
16.             return true;
17.         } catch (Exception e) {
18.             _//http响应状态码为401_
19.             response.setStatus(401);
20.             return false;
21.         }
22.     }

### SpringBoot项目部署

使用package命令，将文件打包成jar包

Jar包部署，要求服务器必须有jre环境

打jar包后，在jar包所在的目录使用cmd命令行，执行java -jar . . .（文件名）命令

### 属性配置方式

- 项目配置文件方式：.properties/.yml 两种形式，但是运维/客户无法直接修改
- 命令行参数方式： --键=值 --port=9999
- 使用系统环境变量的方式：黑窗口需要重新启动，才能生效
- 外部配置文件方式：application.yml批量配置
- 配置优先级：（从上到下优先级递增）

项目中resources目录下的application.yml

Jar包所在目录下的application.yml

操作系统环境变量

命令行参数

### 多环境开发-Profiles

开发/生产/测试可能使用的是不同的环境，不停的修改，修改繁琐并且容易出错

SpringBoot提供的Profiles可以用来隔离应用配置的各个部分，并在特定环境下指定部分配置生效

SpringBoot提供的Profiles可以用来隔离应用程序配置的各个部分，并在特定环境下指定某些部分的配置生效

1.  spring:
2.    profiles:
3.      active: dev

分组开发

1.  spring:
2.    profiles:
3.      group:
4.        "dev": devServer,devDB,devSelf
5.        _#"test": testServer,testDB,testSelf_
6.      active: dev

## 实战-前端篇

HTML：负责网页的结构（标签：form/table/a/div/span）

CSS：负责网页的表现（样式：color/front/background/height）

JavaScript：负责网页的行为（交互效果）

- JavaScript-导入导出

JS提供的导入到处机制，可以实现按需导入

导入和导出的时候，可以使用as重命名

### 局部使用VUE

VUE是一款用于构建用户界面的渐进式的JavaScript框架，提供声明式渲染，组件系统，客户端路由，状态管理，构建工具等功能

#### 快速入门

- 准备

准备html页面，并引入Vue模块（官方提供）

创建VUE程序的实例

准备元素（div），被Vue控制

- 构建用户界面

准备数据

通过插值表达式渲染页面

1.  &lt;body&gt;
2.      &lt;div id="app"&gt;
3.          &lt;h1&gt;{{msg}}&lt;/h1&gt;
4.      &lt;/div&gt;

6.      &lt;div &gt;
7.          &lt;h1&gt;{{msg}}&lt;/h1&gt;
8.      &lt;/div&gt;
9.      _&lt;!-- 引入vue模块 --&gt;_
10.     &lt;script type="module"&gt;
11.         import {createApp} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
12.         _/\* 创建vue的应用实例 \*/_
13.         createApp({
14.             data(){
15.                 return {
16.                     _//定义数据_
17.                     msg: 'hello vue3'
18.                 }
19.             }

21.         }).mount("#app");
22.     &lt;/script&gt;
23. &lt;/body&gt;

第二个由于没有被vue接管所以不会渲染页面

#### 常用指令

指令：HTML标签上带有 v-前缀的特殊属性，不同的指令具有不同的含义，可以实现不同的功能

##### v-for

列表渲染，遍历容器的元素或者对象的属性

语法：v-for = “(item,index) in items”

参数说明：

items为遍历的数组

Item为遍历出来的元素

Index为索引/下标，从0开始；可以省略，省略index语法：v-for = “ item in items”

1.  &lt;script type="module"&gt;
2.          _//导入vue模块_
3.          import { createApp} from 
4.                  'https://unpkg.com/vue@3/dist/vue.esm-browser.js'
5.          _//创建应用实例_
6.          createApp({
7.              data() {
8.                  return {
9.                    //定义数据
10.                     articleList:\[{
11.                                 title:"医疗反腐绝非砍医护收入",
12.                                 category:"时事",
13.                                 time:"2023-09-5",
14.                                 state:"已发布"
15.                             },
16.                             {
17.                                 title:"中国男篮缘何一败涂地？",
18.                                 category:"篮球",
19.                                 time:"2023-09-5",
20.                                 state:"草稿"
21.                             },
22.                             {
23.                                 title:"华山景区已受大风影响阵风达7-8级，未来24小时将持续",
24.                                 category:"旅游",
25.                                 time:"2023-09-5",
26.                                 state:"已发布"
27.                             }\]  
28.                 }
29.             }
30.         }).mount("#app")_//控制页面元素_

32.     &lt;/script&gt;

1.  &lt;div id="app"&gt;
2.          &lt;table border="1 solid" colspa="0" cellspacing="0"&gt;
3.              &lt;tr&gt;
4.                  &lt;th&gt;文章标题&lt;/th&gt;
5.                  &lt;th&gt;分类&lt;/th&gt;
6.                  &lt;th&gt;发表时间&lt;/th&gt;
7.                  &lt;th&gt;状态&lt;/th&gt;
8.                  &lt;th&gt;操作&lt;/th&gt;
9.              &lt;/tr&gt;
10.             _&lt;!-- 哪个元素要出现多次,v-for指令就添加到哪个元素上 --&gt;_
11.             &lt;tr v-for="(article,index) in articleList"&gt;
12.                 &lt;td&gt;{{article.title}}&lt;/td&gt;
13.                 &lt;td&gt;{{article.category}}&lt;/td&gt;
14.                 &lt;td&gt;{{article.time}}&lt;/td&gt;
15.                 &lt;td&gt;{{article.state}}&lt;/td&gt;
16.                 &lt;td&gt;
17.                     &lt;button&gt;编辑&lt;/button&gt;
18.                     &lt;button&gt;删除&lt;/button&gt;
19.                 &lt;/td&gt;
20.             &lt;/tr&gt;
21.         &lt;/table&gt;
22.     &lt;/div&gt;

基于数据循环，多次渲染整个元素

##### v-bind

为html绑定属性值，如设置href，css样式

语法：v-bind:属性名=”属性值”

简化: :属性名=”属性值”

v-bind所绑定的数据，必须在data中定义

1.  &lt;body&gt;
2.      &lt;div id="app"&gt;
3.          _&lt;!-- <a v-bind:href="url"&gt;黑马官网&lt;/a&gt; -->_
4.          &lt;a :href="url"&gt;黑马官网&lt;/a&gt;
5.      &lt;/div&gt;

7.      &lt;script type="module"&gt;
8.          _//引入vue模块_
9.          import { createApp} from 
10.                 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'
11.         _//创建vue应用实例_
12.         createApp({
13.             data() {
14.                 return {
15.                     url: 'https://www.itheima.com'
16.                 }
17.             }
18.         }).mount("#app")_//控制html元素_
19.     &lt;/script&gt;

##### v-if/v-else-if/v-else/v-show

条件性的渲染某元素，判定为true时渲染，否则不渲染 / 根据条件展示某元素，区别在于切换的是display属性的值

v-if

语法：v-if = ”表达式”，表达式值为true，显示，false，隐藏

其他：可以配合v-else-if / v-else进行链式调用条件判断

场景：要么显示，要么不显示，不频繁切换的场景

v-show

语法：v-show= ”表达式”，表达值为true，显示；false，隐藏

原理：基于css样式display来控制显示与隐藏

场景：频繁切换显示隐藏的场景

1.  &lt;body&gt;
2.      &lt;div id="app"&gt;

4.          手链价格为:  &lt;span v-if="customer.level&gt;=0 && customer.level&lt;=1"&gt;9.9&lt;/span&gt;  
5.                      &lt;span v-else-if="customer.level&gt;=2 && customer.level&lt;=4"&gt;19.9&lt;/span&gt; 
6.                      &lt;span v-else&gt;29.9&lt;/span&gt;

8.          &lt;br/&gt;
9.          手链价格为:  &lt;span v-show="customer.level&gt;=0 && customer.level&lt;=1"&gt;9.9&lt;/span&gt;  
10.                     &lt;span v-show="customer.level&gt;=2 && customer.level&lt;=4"&gt;19.9&lt;/span&gt; 
11.                     &lt;span v-show="customer.level&gt;=5">29.9&lt;/span&gt;

13.     &lt;/div&gt;

15.     &lt;script type="module"&gt;
16.         _//导入vue模块_
17.         import { createApp} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'

19.         _//创建vue应用实例_
20.         createApp({
21.             data() {
22.                 return {
23.                     customer:{
24.                         name:'张三',
25.                         level:2
26.                     }
27.                 }
28.             }
29.         }).mount("#app")_//控制html元素_
30.     &lt;/script&gt;
31. &lt;/body&gt;

##### v-on

为html标签绑定事件

语法：v-on：事件名= ”函数名”

简写为 @事件名= ”函数名”

1.  &lt;body&gt;
2.      &lt;div id="app"&gt;
3.          &lt;button v-on:click="money"&gt;点我有惊喜&lt;/button&gt; &nbsp;
4.          &lt;button @click="love"&gt;再点更惊喜&lt;/button&gt;
5.      &lt;/div&gt;

7.      &lt;script type="module"&gt;
8.          _//导入vue模块_
9.          import { createApp} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'

11.         _//创建vue应用实例_
12.         createApp({
13.             data() {
14.                 return {
15.                     _//定义数据_
16.                 }
17.             },
18.             methods:{
19.                 money: function(){
20.                     alert('送你钱100')
21.                 },
22.                 love: function(){
23.                     alert('爱你一万年')
24.                 }
25.             }
26.         }).mount("#app");_//控制html元素_

28.     &lt;/script&gt;
29. &lt;/body&gt;

##### v-model

作用：在表单元素上使用，双向数据绑定，可以方便的获取或设置表单项数据

语法：v-model = “变量名”

v-model中绑定的变量，必须在data中定义

1.      &lt;div id="app"&gt;

3.          文章分类: &lt;input type="text" v-model="searchConditions.category"/&gt; &lt;span&gt;{{searchConditions.category}}&lt;/span&gt;

5.          发布状态: &lt;input type="text" v-model="searchConditions.state"/&gt; &lt;span&gt;{{searchConditions.state}}&lt;/span&gt;

7.          &lt;button&gt;搜索&lt;/button&gt;
8.          &lt;button v-on:click="clear"&gt;重置&lt;/button&gt;

10.         &lt;br /&gt;
11.         &lt;br /&gt;
12.         &lt;table border="1 solid" colspa="0" cellspacing="0"&gt;
13.             &lt;tr&gt;
14.                 &lt;th&gt;文章标题&lt;/th&gt;
15.                 &lt;th&gt;分类&lt;/th&gt;
16.                 &lt;th&gt;发表时间&lt;/th&gt;
17.                 &lt;th&gt;状态&lt;/th&gt;
18.                 &lt;th&gt;操作&lt;/th&gt;
19.             &lt;/tr&gt;
20.             &lt;tr v-for="(article,index) in articleList"&gt;
21.                 &lt;td&gt;{{article.title}}&lt;/td&gt;
22.                 &lt;td&gt;{{article.category}}&lt;/td&gt;
23.                 &lt;td&gt;{{article.time}}&lt;/td&gt;
24.                 &lt;td&gt;{{article.state}}&lt;/td&gt;
25.                 &lt;td&gt;
26.                     &lt;button&gt;编辑&lt;/button&gt;
27.                     &lt;button&gt;删除&lt;/button&gt;
28.                 &lt;/td&gt;
29.             &lt;/tr&gt;
30.         &lt;/table&gt;
31.     &lt;/div&gt;

让输入框的值和 Vue 实例中的数据自动同步。

用户输入内容时，数据会自动更新；数据变化时，输入框内容也会自动变化。

#### 生命周期

生命周期：指一个对象从创建到销毁的整个过程

生命周期的八个阶段：每个阶段会自动执行一个生命周期钩子，让开发者有机会在特定的阶段执行自己的代码

mounted在页面加载完毕时，发起异步请求，加载数据，渲染页面

#### Axios

Axios对原生ajax进行了封装，简化书写，快速开发；使用Axios发送请求，并获取相应结果

Method：请求方式，GET/POST Url：请求路径 Data：请求数据

1.          axios({
2.              method:'get',
3.              url:'http://localhost:8080/article/getAll'
4.          }).then(result=>{
5.              _//成功的回调_
6.              _//result代表服务器响应的所有的数据,包含了响应头,响应体. result.data 代表的是接口响应的核心数据_
7.              console.log(result.data);
8.          }).catch(err=>{
9.              _//失败的回调_
10.             console.log(err);
11.         });

发送请求

1.          let article = {
2.              title: '明天会更好',
3.              category: '生活',
4.              time: '2000-01-01',
5.              state: '草稿'
6.          }
7.          axios({
8.               method:'post',
9.               url:'http://localhost:8080/article/add',
10.              data:article
11.          }).then(result=>{
12.              _//成功的回调_
13.              _//result代表服务器响应的所有的数据,包含了响应头,响应体. result.data 代表的是接口响应的核心数据_
14.              console.log(result.data);
15.          }).catch(err=>{
16.              _//失败的回调_
17.              console.log(err);
18.          }); 

为了方便起见，Axios已经为所有支持的请求方法提供了别名

别名：axios.请求方式（url \[ ,data \[ , config \]\]）

1.          _//别名的方式发送请求_
2.      axios.get('http://localhost:8080/article/getAll').then(result => {
3.              console.log(result.data);
4.          }).catch(err => {
5.              _//失败的回调_
6.              console.log(err);
7.          }); 

##### VUE案例

钩子函数mounted中，获取所有的文章数据

使用v-for指令，把数据渲染到表格上

使用v-model指令，完成表单数据的双向绑定

使用v-on指令为搜索按钮绑定单机事件

1.  &lt;body&gt;
2.      &lt;div id="app"&gt;

4.          文章分类: &lt;input type="text" v-model="searchConditions.category"&gt;

6.          发布状态: &lt;input type="text"  v-model="searchConditions.state"&gt;

8.          &lt;button v-on:click="search"&gt;搜索&lt;/button&gt;

10.         &lt;br /&gt;
11.         &lt;br /&gt;
12.         &lt;table border="1 solid" colspa="0" cellspacing="0"&gt;
13.             &lt;tr&gt;
14.                 &lt;th&gt;文章标题&lt;/th&gt;
15.                 &lt;th&gt;分类&lt;/th&gt;
16.                 &lt;th&gt;发表时间&lt;/th&gt;
17.                 &lt;th&gt;状态&lt;/th&gt;
18.                 &lt;th&gt;操作&lt;/th&gt;
19.             &lt;/tr&gt;
20.             &lt;tr v-for="(article,index) in articleList"&gt;
21.                 &lt;td&gt;{{article.title}}&lt;/td&gt;
22.                 &lt;td&gt;{{article.category}}&lt;/td&gt;
23.                 &lt;td&gt;{{article.time}}&lt;/td&gt;
24.                 &lt;td&gt;{{article.state}}&lt;/td&gt;
25.                 &lt;td&gt;
26.                     &lt;button&gt;编辑&lt;/button&gt;
27.                     &lt;button&gt;删除&lt;/button&gt;
28.                 &lt;/td&gt;
29.             &lt;/tr&gt;
30.         &lt;/table&gt;
31.     &lt;/div&gt;
32.     _&lt;!-- 导入axios的js文件 --&gt;_
33.     &lt;script src="https://unpkg.com/axios/dist/axios.min.js"&gt;&lt;/script&gt;
34.     &lt;script type="module"&gt;
35.         _//导入vue模块_
36.         import {createApp} from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
37.         _//创建vue应用实例_
38.         createApp({
39.             data(){
40.                 return {
41.                     articleList:\[\],
42.                     searchConditions:{
43.                         category:'',
44.                         state:''
45.                     }
46.                 }
47.             },
48.             methods:{
49.                 _//声明方法_
50.                 search:function(){
51.                     _//发送请求,完成搜索,携带搜索条件_
52.                     axios.get('http://localhost:8080/article/search?category='+this.searchConditions.category+'&state='+this.searchConditions.state)
53.                     .then(result=>{
54.                         _//成功回调 result.data_
55.                         _//把得到的数据赋值给articleList_
56.                         this.articleList=result.data
57.                     }).catch(err=>{
58.                         console.log(err);
59.                     });
60.                 }
61.             },
62.             _//钩子函数mounted中,获取所有文章数据_
63.             mounted:function(){
64.                 _//发送异步请求  axios_
65.                 axios.get('http://localhost:8080/article/getAll').then(result=>{
66.                     _//成功回调_
67.                     _//console.log(result.data);_
68.                     this.articleList=result.data;
69.                 }).catch(err=>{
70.                     _//失败回调_
71.                     console.log(err);
72.                 });
73.             }
74.         }).mount('#app');_//控制html元素_
75.     &lt;/script&gt;
76. &lt;/body&gt;

### 整站使用VUE（VUE工程化）

- 介绍：create-vue是Vue官方提供的最新的脚手架工具，用于快速生成一个工程化的Vue项目、
- Create-vue提供了如下功能：
- 统一的目录结构
- 本地部署
- 热部署
- 单元测试
- 集成打包
- 依赖环境：NodeJS

Npm：Node Package Manager 是NodeJS的软件包管理器

#### VUE项目创建和启动

- 创建一个工程化的Vue项目，执行命令

npm init vue@latest

执行上述指令，将会安装并执行create-vue，它是Vue官方的项目脚手架工具

- 进入项目目录，执行命令安装当前项目的依赖

npm install

创建项目以及安装依赖的过程，都是需要联网的

- 启动vue项目，执行命令

npm run dev

- 访问项目，打开浏览器，在浏览器中访问5173端口，就可以访问到vue项目

#### VUE项目开发流程

Vue是vue项目中的组件文件，在vue项目中也成为单文件组件（SFC，Single-File Component），Vue的单文件组件会将一个组件的逻辑（JS），模板（HTML）和样式（CSS）封装在同一个文件里

#### API风格

- Vue的组件有两种不同的风格：组合式API和选项式API
- 选项式API，可以包含多个选项的对象来描述组件的逻辑，如：data methods，mounted
- Script上添加setup标识，告诉Vue需要进行一些处理，让我们可以更简洁的使用组合式API
- Ref（）：接收一个内部值，返回一个响应式的ref对象，此对象只有一个指向内部值的属性value
- onMounted（）：在组合式API中的钩子方法，注册一个回调函数，在组件挂载完成后执行

1.  &lt;script setup&gt;
2.    import {ref} from 'vue';
3.    _//调用ref函数,定义响应式数据_
4.    const msg = ref('西安');

6.    _//导入 Api.vue文件_
7.    import ApiVue from './Api.vue'
8.  &lt;/script&gt;

1.  &lt;script setup&gt;
2.      import {ref,onMounted} from 'vue'
3.      _//声明响应式数据 ref  响应式对象有一个内部的属性value_
4.      const count = ref(0); _//在组合式api中,一般需要把数据定义为响应式数据_
5.      _//const count=0;_

7.      _//声明函数_
8.      function increment(){
9.          count.value++;
10.     }

12.     _//声明钩子函数 onMounted_
13.     onMounted(()=>{
14.         console.log('vue 已经挂载完毕了...');
15.     });
16. &lt;/script&gt;

#### 案例

钩子函数mounted中，获取所有的文章数据

使用v-for指令，把数据渲染到表格上展示

使用v-model指令完成表单数据的双向绑定

使用v-on指令为搜索按钮绑定单击事件

Article.vue 但是难以复用

接口调用的js代码一般会封装到.js文件中，并且以函数的形式暴露给外部

##### 拦截器

在请求或响应被then或catch处理前拦截它们

1.  _//导入axios  npm install axios_
2.  import axios from 'axios';
3.  _//定义一个变量,记录公共的前缀  ,  baseURL_
4.  const baseURL = 'http://localhost:8080';
5.  const instance = axios.create({baseURL})

8.  _//添加响应拦截器_
9.  instance.interceptors.response.use(
10.     result=>{
11.         return result.data;
12.     },
13.     err=>{
14.         alert('服务异常');
15.         return Promise.reject(err);_//异步的状态转化成失败的状态_
16.     }
17. )

### Element

- Element：是饿了么团队研发的，基于Vue3，面向设计师和开发者的组件库
- 组件：组成网页的部件，例如超链接，按钮，图片，表格，表单，分页条等等
- 准备工作：
- 创建一个工程化的vue项目
- 参照官方文档，安装Element Plus组件库（在当前工程的目录下）

npm install element-plus --save

- main.js中引入element plus组件库（参照官方文档）

#### 常用组件

- Table
- 分页条
- 表单
- 卡片

参考：[一个 Vue 3 UI 框架 | Element Plus](https://element-plus.org/zh-CN/)

### 大事件前端

#### 环境准备

- 创建Vue工程：npm init vue @latest
- 安装依赖：
- Element-Plus：npm install element-plus --save
- Axios：npm install axios
- Sass：npm install sass-D
- 目录调整
- 删除components下面自动生成的内容
- 新建目录api，utils，views
- 将资料中的静态资源拷贝到asserts目录下
- 删除APP.vue中自动生成的内容

#### 注册功能开发

##### 开发步骤

搭建页面-html标签 / css样式

|

绑定数据与事件-表单校验

|

调用后台接口-接口文档 / src, api, xx.js封装 / 页面函数中调用

##### 页面搭建以及前端校验

1.  _//定义数据模型_
2.  const registerData = ref(
3.    {
4.      username: '',
5.      password: '',
6.      rePassword: ''
7.    }
8.  )

10. _//定义确认密码的校验函数_
11. const checkRePassword = (rule, value, callback) => {
12.   if (value === '') {
13.     callback(new Error('请再次输入密码'));
14.   } else if (value !== registerData.value.password) {
15.     callback(new Error('两次输入密码不一致!'));
16.   } else{
17.     callback();
18.   }
19. }

21. _//定义表单校验规则_
22. const rules ={
23.   username: \[
24.     {required: true, message: '请输入用户名', trigger: 'blur' },
25.     { min: 5, max: 16, message: '长度在 5 到 16 个非空字符', trigger: 'blur' }
26.   \],
27.   password: \[
28.     {required: true, message: '请输入用户名', trigger: 'blur' },
29.     { min: 5, max: 16, message: '长度在 5 到 16 个非空字符', trigger: 'blur' }
30.   \],
31.   rePassword: \[
32.     {validator: checkRePassword, trigger: 'blur'},
33.   \]
34. }
35. &lt;/script&gt;

el-form标签上通过rules属性，绑定校验规则

el-form-item标签上通过prop属性，指定校验项

##### 接口对接

&lt;el-form-item prop="username"&gt;

这是 Element Plus（Element UI 的 Vue3 版本）里的表单组件。

el-form-item 相当于一行表单项，里面一般放输入框、选择器等。

prop="username"：作用是指定当前表单项对应的 字段名。

如果你在外层 el-form 里写了 model="registerData"，并配置了 校验规则（rules），这里的 prop 会告诉 el-form-item：这个输入框绑定的字段是 registerData.username。这样验证的时候就能对应到正确的规则。

application/x-www-form-urlencoded 是一种常见的数据编码格式，用于将表单数据转换为 URL 可传输的格式。它将表单数据编码为键值对，类似于 URL 查询参数。

user.js

1.  _//导入request.js请求工具_
2.  import request from '@/utils/request.js'

4.  _//提供调用注册接口的函数_
5.  export const userRegisterService = ( registerData ) => {
6.      _//借助于urlSearchParams对象来处理参数_
7.      const params = new URLSearchParams();
8.      _//遍历对象的每一个属性_
9.      for (let key in registerData) {
10.         params.append(key, registerData\[key\]);
11.     }
12.     return request.post('/user/register', registerData);
13. }

Login.vue

1.  _//调用后台接口完成注册_
2.  import {userRegisterService} from '@/api/user.js'
3.  const register = async () => {
4.    _//registerData是一个响应式对象，如果要获取值，需要.value_
5.    let result = await userRegisterService(registerData.value);
6.    if (result.code === 0) {
7.      _//成功了_
8.      alert(result.msg ? result.msg:'注册成功')
9.    } else{
10.     _//失败了_
11.     alert('注册失败')
12.   }
13. }

添加单击事件

1.          &lt;el-form-item prop="username"&gt;
2.            &lt;el-input :prefix-icon="User" placeholder="请输入用户名" v-model="registerData.username" @click="register"&gt;&lt;/el-input&gt;
3.          &lt;/el-form-item&gt;

###### 跨域问题

由于浏览器的同源策略限制，向不同源（不同协议/不同域名/不同接口）发送ajax请求会失败

vite.config.js

1.      server: {
2.          proxy: {
3.          '/api': {
4.              target: 'http://localhost:8080', _// 后台服务器地址_
5.              changeOrigin: true, _// 是否更改请求头中的Origin字段，修改源_
6.              rewrite: (path) => path.replace(/^\\/api/, '') _// 重写路径 将/api 替换为空_
7.          }
8.          }
9.      }

#### 登录功能开发

1.  _//绑定数据，复用注册表单的数据模型_
2.  _//表单数据校验_
3.  _//登录函数_
4.  const login = async () => {
5.    _//调用后台登录接口_
6.    let result = await userLoginService(registerData.value);
7.    if (result.code === 0) {
8.      _//成功了_
9.      alert(result.msg ? result.msg:'登录成功')
10.   } else{
11.     _//失败了_
12.     alert('登录失败')
13.   }
14. }

16. _//定义函数，清空数据模型数据_
17. const clearRegisterData = () => {
18.   registerData.value.username = '';
19.   registerData.value.password = '';
20.   registerData.value.rePassword = '';
21. }

User.js

1.  _//提供调用登录接口的函数_
2.  export const userLoginService = (loginData) => {
3.      _//借助于urlSearchParams对象来处理参数_
4.      const params = new URLSearchParams();
5.      _//遍历对象的每一个属性_
6.      for (let key in loginData) {
7.          params.append(key, loginData\[key\]);
8.      }
9.      return request.post('/user/login', params);
10. }

##### 优化axios响应拦截器

1.  _//添加响应拦截器_
2.  instance.interceptors.response.use(
3.      result=>{
4.          _//判断业务状态码_
5.          if(result.data.code === 0){
6.              return result.data;
7.          }

9.          _//操作失败_
10.         ElMessage.error(result.data.msg?result.data.msg:'服务异常');
11.         _//异步操作的状态转为失败_
12.         return Promise.reject(result.data);
13.     },
14.     err=>{
15.         alert('服务异常');
16.         return Promise.reject(err);_//异步的状态转化成失败的状态_
17.     }
18. )

封装对状态码的响应，并引入element-plus的消息提示组件

#### 主页面搭建

问题：无法在显示登录窗口后成功进入到主页面

解决方案：路由

##### 路由

- 路由，决定从起点到终点的路径的进程
- 在前端工程中，路由指的是根据不同的访问路径，展示不同组件的内容
- Vue Router是vue官方的路由
- 安装vue router

npm install vue-router@4

- 在src/router/index.js中创建路由器，并导出
- 在vue应用实例中使用vue-router
- 声明router-view标签，展示组件内容

1.  import {createRouter,createWebHistory} from 'vue-router'

3.  _//导入组件_
4.  import LoginVue from '@/views/Login.vue'
5.  import LayoutVue from '@/views/Layout.vue'

7.  _//定义路由关系_
8.  const routes = \[
9.      {path:'/login',component:LoginVue},
10.     {path:'/',component:LayoutVue}
11. \]

13. _//创建路由器_
14. const router = createRouter({
15.     history:createWebHistory(),
16.     routes:routes
17. })

19. _//导出路由_
20. export default router

路由实现跳转 在vue实例中使用vue-router

1.  _//绑定数据，复用注册表单的数据模型_
2.  _//表单数据校验_
3.  _//登录函数_
4.  import { useRouter } from 'vue-router'
5.  const router = useRouter();
6.  const login = async () => {
7.    _//调用后台登录接口_
8.    let result = await userLoginService(registerData.value);
9.    ElMessage.success(result.msg? result.msg:'登录成功');
10.   _//跳转到首页 路由完成跳转_
11.   router.push('/')
12. }

###### 二级路由（子路由）

配置子路由

声明router-view标签

为菜单项el-menu-item设置index属性，设置点击后的路由路径

Route/index.js

1.  import ArticleCategoryVue from '@/views/article/ArticleCategory.vue'
2.  import ArticleManageVue from '@/views/article/ArticleManage.vue'
3.  import UserAvatarVue from '@/views/user/UserAvatar.vue'
4.  import UserInfoVue from '@/views/user/UserInfo.vue'
5.  import UserResetPassword from "@/views/user/UserResetPassword.vue";

7.  _//定义路由关系_
8.  const routes = \[
9.      {path:'/login',component:LoginVue},
10.     {
11.         path:'/',component:LayoutVue,redirect: '/article/manage',children:\[
12.             { path: '/article/category', component: ArticleCategoryVue},
13.             { path: '/article/manage', component: ArticleManageVue},
14.             { path: '/user/info', component: UserInfoVue},
15.             { path: '/user/avatar', component: UserAvatarVue},
16.           { path: '/user/resetPassword', component: UserResetPassword}
17.         \]
18.     }
19. \]

重定向到/article/manage | 在layout中加入索引

#### 文章分类列表

Article.js

1.  import request from '@/utils/request.js'

3.  _//文章分类列表查询_
4.  export const articleCategoryListService = () => {
5.      return request.get('/category')
6.  }

ArticleCategory.vue

1.  import { ref } from 'vue'
2.  const categorys = ref(\[

4.  \])
5.  _//声明一个异步函数_
6.  import {articleCategoryListService} from '@/api/article.js'
7.  const articleCategoryList = async () => {
8.    let result = await articleCategoryListService();
9.    categorys.value = result.data;
10. }
11. articleCategoryList();

Bug：没有携带JWT token所以会出现401报错

##### Pinia状态管理库

- Pinia是Vue的专属状态管理库，它允许你跨组件或页面共享状态
- 现状：Login中存在token，但是无法传递到ArticleCategory
- Pinia状态管理库的使用
- 安装pinia

npm install pinia

- 在vue应用实例中使用pinia
- 在src/stores/token.js中定义store
- 在组件中使用store

article.js

1.  import request from '@/utils/request.js'
2.  import { useTokenStore } from "@/stores/token.js"
3.  export const articleCategoryListService = () => {
4.      const tokenStore = useTokenStore()
5.      _//在pinia中定义的响应式数据都不需要.value_
6.      return request.get('/category',{headers:{'Authorization':tokenStore.token}})
7.  }

token.js

1.  _//定义store_
2.  import { defineStore } from 'pinia'
3.  import {ref} from "vue";
4.  _/\*_
5.     第一个参数：名字，唯一性
6.     第二个参数：函数，函数的内部可以定义状态的所有内容
7.   \*/
8.  export const useTokenStore = defineStore('token',()=>{
9.      _//定义状态的内容_

11.     _//1.响应式变量_
12.     const token = ref('');

14.     _//2.定义一个函数，用于修改token_
15.     const setToken = (newToken) => {
16.         token.value = newToken;
17.     }

19.     _//3.函数，移除token的值_
20.     const removeToken = () => {
21.         token.value = '';
22.     }

24.     return {
25.         token,
26.         setToken,
27.         removeToken
28.     }
29. });

Login.vue

1.  _//绑定数据，复用注册表单的数据模型_
2.  _//表单数据校验_
3.  _//登录函数_
4.  import { useTokenStore } from "@/stores/token.js";
5.  import { useRouter } from 'vue-router'
6.  const router = useRouter();
7.  const tokenStore = useTokenStore();
8.  const login = async () => {
9.    _//调用后台登录接口_
10.   let result = await userLoginService(registerData.value);
11.   ElMessage.success(result.msg? result.msg:'登录成功');
12.   _//将token存储到pinia_
13.   tokenStore.setToken(result.data);
14.   _//跳转到首页 路由完成跳转_
15.   router.push('/')
16. }

通过请求头Authorization携带token

return request.get('/category',{headers:{'Authorization':tokenStore.token}})

书写繁琐，可以配置axios请求拦截器

###### axios配置请求拦截器

1.  _//添加请求拦截器_
2.  _//导入pinia的用户信息仓库_
3.  import { useTokenStore } from '@/stores/token.js'
4.  instance.interceptors.request.use(
5.      (config)=> {
6.          _//请求前的回调_
7.          _//添加token，从pinia中获取_
8.          const tokenStore = useTokenStore();
9.          if (tokenStore.token) {
10.             config.headers\['Authorization'\] = tokenStore.token;
11.         }
12.         return config;
13.     },
14.     (err)=> {
15.         _//请求失败的回调_
16.         Promise.reject(err)
17.     }
18. )

1.  export const articleCategoryListService = () => {
2.      return request.get('/category')
3.  }

拦截器不是拦截页面，而是拦截所有通过 axios 发送的 HTTP 请求。

只要你的项目里用 axios 发请求（比如获取文章分类、登录、获取用户信息等），拦截器就会统一处理这些请求，比如自动加 token、设置请求头等。这样每个页面或接口请求都会被拦截器“经过”，实现统一管理。

如果 pinia 里没有 token 就不加 token，所以登录请求不会带 token，不会有影响。

###### Pinia持久化插件-persist

- Pinia默认是内存存储，当刷新浏览器的时候会丢失数据
- Persist插件可以将pinia中的数据持久化的存储
- 定义状态时指定持久化配置参数
- 安装persist

npm install pinia-persistedstate-plugin

- 在pinia中使用persist

1.  import { createPersistedState } from "pinia-persistedstate-plugin";

3.  import App from './App.vue'

5.  const app = createApp(App)
6.  const pinia = createPinia()
7.  const persist = createPersistedState();
8.  pinia.use(persist);

- 定义状态store时指定持久化配置参数

1.  ,{persist: true}_//持久化存储_

###### 未登录统一处理

要求未登录的需要跳转到登录页面

非组件实例（比如工具函数、请求封装、状态管理等）需要直接导入 Vue 实例（如路由、Pinia 仓库），是因为这些文件本身不是 Vue 组件，无法通过 this.$router、this.$store 等方式访问 Vue 实例上的属性和方法。

在这些非组件文件里，只有通过直接导入相关实例（如 import router from '@/router'），才能使用路由跳转、状态管理等功能。这种做法可以让工具类、请求拦截器等在没有组件上下文的情况下也能访问和操作全局实例。

1.  _//导入路由实例_
2.  import router from '@/router'

1.      err=>{
2.          _//判断响应状态码，如果为401，跳转登录_
3.          if(err.response.status === 401){
4.              ElMessage.error("请先登录");
5.              router.push('/login');
6.          }else{
7.              ElMessage.error('服务异常');
8.          }
9.  }

Q：为什么不用重定向 使用路由

A：未登录用户跳转到登录页，应该用路由跳转（如 router.push('/login')），因为这是在运行时根据用户状态主动导航，而不是在路由配置里写死的路径跳转。

重定向是路由配置里的静态跳转，比如访问 / 自动跳到 /home，它不关心用户状态。

而登录校验需要根据实际情况判断，只有代码里用路由跳转才能实现动态控制。

#### 添加文章分类

数据模型与表单校验规则

1.  _//控制添加分类弹窗_
2.  const dialogVisible = ref(false)

4.  _//添加分类数据模型_
5.  const categoryModel = ref({
6.    categoryName: '',
7.    categoryAlias: ''
8.  })
9.  _//添加分类表单校验_
10. const rules = {
11.   categoryName: \[
12.     { required: true, message: '请输入分类名称', trigger: 'blur' },
13.   \],
14.   categoryAlias: \[
15.     { required: true, message: '请输入分类别名', trigger: 'blur' },
16.   \]
17. }

19. _//调用接口，添加表单_
20. import { ElMessage } from 'element-plus'
21. const addCategory = async () => {
22.   let result = await articleCategoryAddService(categoryModel.value);
23.   ElMessage.success(result.msg?result.msg:'添加成功');

25.   _//调用获取所有文章分类的函数（刷新页面）_
26.   articleCategoryList();
27.   dialogVisible.value = false
28. }

弹窗

1.      _&lt;!-- 添加分类弹窗 --&gt;_
2.      &lt;el-dialog v-model="dialogVisible" title="添加弹层" width="30%"&gt;
3.        &lt;el-form :model="categoryModel" :rules="rules" label-width="100px" style="padding-right: 30px"&gt;
4.          &lt;el-form-item label="分类名称" prop="categoryName"&gt;
5.            &lt;el-input v-model="categoryModel.categoryName" minlength="1" maxlength="10"&gt;&lt;/el-input&gt;
6.          &lt;/el-form-item&gt;
7.          &lt;el-form-item label="分类别名" prop="categoryAlias"&gt;
8.            &lt;el-input v-model="categoryModel.categoryAlias" minlength="1" maxlength="15"&gt;&lt;/el-input&gt;
9.          &lt;/el-form-item&gt;
10.       &lt;/el-form&gt;
11.       &lt;template #footer&gt;
12.         &lt;span class="dialog-footer"&gt;
13.             &lt;el-button @click="dialogVisible = false"&gt;取消&lt;/el-button&gt;
14.             &lt;el-button type="primary" @click = "addCategory"&gt; 确认 &lt;/el-button&gt;
15.         &lt;/span&gt;
16.       &lt;/template&gt;
17.     &lt;/el-dialog&gt;

#### 修改文章分类

1.  _//定义变量，控制标题的展示_
2.  const title = ref('')

4.  _//展示编辑弹窗_
5.  const showDialog = (row) => {
6.    dialogVisible.value = true;title.value ='编辑分类'
7.    _//数据拷贝_
8.    categoryModel.value.categoryName = row.categoryName;
9.    categoryModel.value.categoryAlias = row.categoryAlias;
10.   _//扩展id属性，将来要传递给后台，完成分类的修改_
11.   categoryModel.value.id = row.id;
12. }

让标题被数据模型控制

1.  &lt;el-button type="primary" @click="dialogVisible = true , title = '添加分类'"&gt;添加分类&lt;/el-button&gt;

完成数据拷贝以及单击事件/标题控制的绑定

1.          &lt;template #default="{ row }"&gt;
2.            &lt;el-button :icon="Edit" circle plain type="primary" @click = "showDialog(row)"&gt;&lt;/el-button&gt;
3.            &lt;el-button :icon="Delete" circle plain type="danger"&gt;&lt;/el-button&gt;
4.          &lt;/template&gt;

##### 文章修改分类接口对接

1.  _//编辑分类_
2.  const updateCategory = async () => {
3.   let result = await articleCategoryUpdateService(categoryModel.value);
4.    ElMessage.success(result.msg?result.msg:'修改成功');
5.    _//调用获取所有文章分类的函数（刷新页面）_
6.    articleCategoryList();
7.    dialogVisible.value = false
8.  }

10. _//清空编辑弹窗模型的数据_
11. const clearData = () => {
12.   categoryModel.value = {
13.     categoryName: '',
14.     categoryAlias: ''
15.   }
16. }

对title进行判断

1.              &lt;el-button type="primary" @click = "title === '添加分类'? addCategory() : updateCategory()"&gt; 确认 &lt;/el-button&gt;

如果title是添加分类那么执行addCategory逻辑

添加分类中加入清空弹窗模型的函数 因为它们共用同一个模型

1.            &lt;el-button type="primary" @click="dialogVisible = true , title = '添加分类',clearData"&gt;添加分类&lt;/el-button&gt;

#### 删除文章分类

引入确认框

1.  _//删除分类_
2.  import { ElMessageBox } from 'element-plus'
3.  const deleteCategory = (row) => {
4.    _//提示用户 确认框_
5.    ElMessageBox.confirm(
6.        '你确认删除改分类信息吗？',
7.        '温馨提示',
8.        {
9.          confirmButtonText: '确认',
10.         cancelButtonText: '取消',
11.         type: 'warning',
12.       }
13.   )
14.       .then(async () => {
15.         //调用接口，完成删除
16.         let result = await articleCategoryDeleteService(row.id)
17.         ElMessage({
18.           type: 'success',
19.           message: '删除成功',
20.         })
21.         //刷新列表
22.         articleCategoryList();
23.       })
24.       .catch(() => {
25.         ElMessage({
26.           type: 'info',
27.           message: '用户取消了删除',
28.         })
29.       })
30. }

使用单击事件来接收对应行的数据

1.          &lt;template #default="{ row }"&gt;
2.            &lt;el-button :icon="Edit" circle plain type="primary" @click = "showDialog(row)"&gt;&lt;/el-button&gt;
3.            &lt;el-button :icon="Delete" circle plain type="danger" @click = "deleteCategory(row)"&gt;&lt;/el-button&gt;
4.          &lt;/template&gt;

文章删除接口服务类

1.  _//文章分类删除_
2.  export const articleCategoryDeleteService = (id) => {
3.      return request.delete('/category?id=' + id)
4.  }

#### 文章分类列表查询

1.  _//获取文章列表数据_
2.  const articleList = async () => {
3.    let params = {
4.      pageNum: pageNum.value,
5.      pageSize: pageSize.value,
6.      categoryId: categoryId.value ? categoryId.value:null,
7.      state: state.value ? state.value:null
8.    }
9.    let result = await articleListService(params);

11.   _//渲染视图_
12.   total.value = result.data.total;
13.   articles.value = result.data.items;

15.   _//处理数据，给数据模型扩展一个属性categoryName，分类名称_
16.   for(let i=0;i<articles.value.length;i++){
17.     let article = articles.value\[i\];
18.     for (let j = 0; j < categorys.value.length; j++) {
19.       if (article.categoryId = categorys.value\[j\].id) {
20.         article.categoryName = categorys.value\[j\].categoryName;
21.       }
22.     }
23.   }
24. }

优化：原方案中接收后台传来的categoryId，并呈现在前端，经过优化扩展了一个属性categoryName，用来返回id对应的类名

1.  _//文章列表查询_
2.  export const articleListService = (params) => {
3.      return request.get('/article',{params: params})
4.  }

#### 新增文章接口对接

##### 文章封面上传

1.          &lt;el-form-item label="文章封面"&gt;
2.            _<!--_
3.            auto-upload:是否在选中文件后自动上传
4.            action：设置服务器接口路径
5.            name：设置上传的文件字段名
6.            headers：设置上传的请求头
7.            on-success：上传成功时的回调函数
8.            -->

10.           <el-upload class="avatar-uploader" :auto-upload="true" :show-file-list="false"
11.           action = '/api/upload'
12.           name = 'file'
13.           :headers = "{'Authorization': tokenStore.token }"
14.           :on-success="uploadSuccess"
15.           >
16.             &lt;img v-if="articleModel.coverImg" :src="articleModel.coverImg" class="avatar" /&gt;
17.             &lt;el-icon v-else class="avatar-uploader-icon"&gt;
18.               &lt;Plus /&gt;
19.             &lt;/el-icon&gt;
20.           &lt;/el-upload&gt;
21.         &lt;/el-form-item&gt;

##### 接口对接

1.  _//添加文章_
2.  import {ElMessage} from "element-plus";
3.  const addArticle = async (state) => {
4.    _//给文章状态赋值_
5.    articleModel.value.state = state;

7.    _//调用添加文章接口_
8.    let result = await articleAddService(articleModel.value);

10.   _//添加成功_
11.   ElMessage.success(result.msg ? result.msg : '添加文章成功');

13.   _//关闭抽屉_
14.   visibleDrawer.value = false;
15.   _//刷新文章列表_
16.   articleList()

18.   _//重置表单_
19.   articleModel.value = {
20.     title: '',
21.     categoryId: '',
22.     coverImg: '',
23.     content:'',
24.     state:''
25.   }
26. }

1.            &lt;el-button type="primary" @click = "addArticle('已发布')"&gt;发布&lt;/el-button&gt;
2.            &lt;el-button type="info" @click = "addArticle('草稿')"&gt;草稿&lt;/el-button&gt;

Article.js

1.  _//文章添加_
2.  export const articleAddService = (articleData) => {
3.      return request.post('/article' , articleData)
4.  }

#### 顶部导航栏信息显示

1.  _//调用函数，获取用户详细信息_
2.  import { userInfoService } from '@/api/user.js'
3.  import useUserInfoStore from '@/stores/userInfo.js'
4.  const userInfoStore = useUserInfoStore()
5.  const getUserInfo = async () => {
6.    _//调用接口_
7.    let result = await userInfoService()
8.    _//数据存储到pinia中_
9.    userInfoStore.setInfo(result.data)
10. }

12. getUserInfo()

userInfo.js

1.  import {defineStore} from "pinia";
2.  import {ref} from "vue";

4.  const useUserInfoStore = defineStore('userInfo',()=>{
5.      _//定义状态相关的内容_
6.      const info = ref({})

8.      const setInfo = (newInfo)=>{
9.          info.value = newInfo
10.     }

12.     const removeInfo = ()=>{
13.         info.value = {}
14.     }

16.     return {info,setInfo,removeInfo}

18. },{persist:true});

20. export default useUserInfoStore;

定义状态相关的内容

1.  _//提供用户详细信息_
2.  export const userInfoService = () => {
3.      return request.get('/user/userInfo');
4.  }

##### 退出登录

1.  _//条目被点击后调用的函数_
2.  import { useRouter } from 'vue-router'
3.  import {ElMessage, ElMessageBox} from "element-plus";
4.  import { useTokenStore }  from "@/stores/token.js";
5.  const tokenStore = useTokenStore();
6.  const router = useRouter()
7.  const handleCommand = (command) => {
8.    _//判断指令_
9.    if(command === 'logout') {
10.     _//退出登录_
11.     ElMessageBox.confirm(
12.         '你确认要退出吗？',
13.         '温馨提示',
14.         {
15.           confirmButtonText: '确认',
16.           cancelButtonText: '取消',
17.           type: 'warning',
18.         }
19.     )
20.         .then(async () => {
21.           _//退出登录_
22.           _//1.清除pinia中存储的的token以及个人信息_
23.           tokenStore.removeToken();
24.           userInfoStore.removeInfo();

26.           _//2.跳转到登录页面_
27.           router.push('/login')

29.           ElMessage({
30.             type: 'success',
31.             message: '退出登录成功',
32.           })

34.         })
35.         .catch(() => {
36.           ElMessage({
37.             type: 'info',
38.             message: '用户取消了退出登录',
39.           })
40.         })
41.   }
42.   else{
43.     _//路由_
44.     router.push('/user/' + command)
45.   }
46. }

使用command命令绑定

1.          _&lt;!-- 头像下拉菜单 --&gt;_
2.          _&lt;!--command : 条目被点击后会出发，在事件函数上可以声明一个参数，用于接收条目对应的指令 --&gt;_
3.          &lt;el-dropdown placement="bottom-end" @command = "handleCommand"&gt;

##### 基本资料修改

1.  &lt;script setup&gt;
2.  import { ref } from 'vue'
3.  import userUserInfoStore from '@/stores/userInfo.js'
4.  const userInfoStore = userUserInfoStore()
5.  const userInfo = ref({...userInfoStore.info})
6.  const rules = {
7.    nickname: \[
8.      { required: true, message: '请输入用户昵称', trigger: 'blur' },
9.      {
10.       pattern: /^\\S{2,10}$/,
11.       message: '昵称必须是2-10位的非空字符串',
12.       trigger: 'blur'
13.     }
14.   \],
15.   email: \[
16.     { required: true, message: '请输入用户邮箱', trigger: 'blur' },
17.     { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
18.   \]
19. }

21. _//修改个人信息_
22. import { userInfoUpdateService } from '@/api/user.js'
23. import {ElMessage} from "element-plus";
24. const updateUserInfo = async () => {
25.   _//调用接口_
26.   let result = await userInfoUpdateService(userInfo.value);
27.   ElMessage.success(result.msg ? result.msg : "修改成功");

29.   _//更新store中的用户信息_
30.   userInfoStore.setInfo(userInfo.value);
31. }
32. &lt;/script&gt;
33. &lt;template&gt;
34.   &lt;el-card class="page-container"&gt;
35.     &lt;template #header&gt;
36.       &lt;div class="header"&gt;
37.         &lt;span&gt;基本资料&lt;/span&gt;
38.       &lt;/div&gt;
39.     &lt;/template&gt;
40.     &lt;el-row&gt;
41.       &lt;el-col :span="12"&gt;
42.         &lt;el-form :model="userInfo" :rules="rules" label-width="100px" size="large"&gt;
43.           &lt;el-form-item label="登录名称"&gt;
44.             &lt;el-input v-model="userInfo.username" disabled&gt;&lt;/el-input&gt;
45.           &lt;/el-form-item&gt;
46.           &lt;el-form-item label="用户昵称" prop="nickname"&gt;
47.             &lt;el-input v-model="userInfo.nickname"&gt;&lt;/el-input&gt;
48.           &lt;/el-form-item&gt;
49.           &lt;el-form-item label="用户邮箱" prop="email"&gt;
50.             &lt;el-input v-model="userInfo.email"&gt;&lt;/el-input&gt;
51.           &lt;/el-form-item&gt;
52.           &lt;el-form-item&gt;
53.             &lt;el-button type="primary" @click = "updateUserInfo"&gt;提交修改&lt;/el-button&gt;
54.           &lt;/el-form-item&gt;
55.         &lt;/el-form&gt;
56.       &lt;/el-col&gt;
57.     &lt;/el-row&gt;
58.   &lt;/el-card&gt;
59. &lt;/template&gt;

1.  _//修改个人信息_
2.  export const userInfoUpdateService = (userInfoData) => {
3.      return request.put('/user/update', userInfoData );
4.  }

##### 用户头像修改

实现头像回显/图片上传/头像修改

1.  &lt;script setup&gt;
2.  import { Plus, Upload } from '@element-plus/icons-vue'
3.  import {ref} from 'vue'
4.  import avatar from '@/assets/default.png'
5.  const uploadRef = ref()
6.  import { useTokenStore } from '@/stores/token.js'
7.  const tokenStore = useTokenStore()

9.  import useUserInfoStore from '@/stores/userInfo.js'
10. const userInfoStore = useUserInfoStore()

12. _//用户头像地址_
13. const imgUrl= ref(userInfoStore.info.userPic)

15. _//图片上传成功的回调_
16. const uploadSuccess = (result) => {
17.   imgUrl.value = result.data;
18. }

20. import { userAvatarUpdateService } from '@/api/user.js'
21. import {ElMessage} from "element-plus";
22. _//头像修改_
23. const updateAvatar = async () => {
24.   _//调用接口_
25.   let result = await userAvatarUpdateService(imgUrl.value);

27.   ElMessage.success(result.msg ? result.msg : "头像修改成功")

29.   _//修改pinia中的数据_
30.   userInfoStore.info.userPic = imgUrl.value;
31. }
32. &lt;/script&gt;

34. &lt;template&gt;
35.   &lt;el-card class="page-container"&gt;
36.     &lt;template #header&gt;
37.       &lt;div class="header"&gt;
38.         &lt;span&gt;更换头像&lt;/span&gt;
39.       &lt;/div&gt;
40.     &lt;/template&gt;
41.     &lt;el-row&gt;
42.       &lt;el-col :span="12"&gt;
43.         <el-upload
44.             ref="uploadRef"
45.             class="avatar-uploader"
46.             :show-file-list="false"
47.             :auto-upload="true"
48.             action="/api/upload"
49.             name="file"
50.             :headers="{ 'Authorization': tokenStore.token }"
51.             :on-success="uploadSuccess"
52.         >
53.           &lt;img v-if="imgUrl" :src="imgUrl" class="avatar" /&gt;
54.           &lt;img v-else :src="avatar" width="278" /&gt;
55.         &lt;/el-upload&gt;
56.         &lt;br /&gt;
57.         &lt;el-button type="primary" :icon="Plus" size="large"  @click="uploadRef.$el.querySelector('input').click()"&gt;
58.           选择图片
59.         &lt;/el-button&gt;
60.         &lt;el-button type="success" :icon="Upload" size="large" @click="updateAvatar"&gt;
61.           上传头像
62.         &lt;/el-button&gt;
63.       &lt;/el-col&gt;
64.     &lt;/el-row&gt;
65.   &lt;/el-card&gt;
66. &lt;/template&gt;

68. &lt;style lang="scss" scoped&gt;
69. .avatar-uploader {
70.   :deep() {
71.     .avatar {
72.       width: 278px;
73.       height: 278px;
74.       display: block;
75.     }

77.     .el-upload {
78.       border: 1px dashed var(--el-border-color);
79.       border-radius: 6px;
80.       cursor: pointer;
81.       position: relative;
82.       overflow: hidden;
83.       transition: var(--el-transition-duration-fast);
84.     }

86.     .el-upload:hover {
87.       border-color: var(--el-color-primary);
88.     }

90.     .el-icon.avatar-uploader-icon {
91.       font-size: 28px;
92.       color: #8c939d;
93.       width: 278px;
94.       height: 278px;
95.       text-align: center;
96.     }
97.   }
98. }
99. &lt;/style&gt;

修改头像

1.  _//修改头像_
2.  export const userAvatarUpdateService = (avatarUrl) => {
3.      const params = new URLSearchParams();
4.      params.append('avatarUrl', avatarUrl);
5.      return request.patch('/user/updateAvatar', params);
6.  }

# 苍穹外卖

项目介绍：专门为餐饮企业（餐厅，饭店）定制的一款软件产品

功能架构：体现项目中的业务功能模块

管理端-员工管理/分类管理/菜品管理/套餐管理/订单管理/工作台/数据统计/来单提醒

用户端-微信登录/商品浏览/购物车/用户下单/微信支付/历史订单/地址管理/用户催单

技术选型：展示项目中使用到的技术框架和中间件

用户层：node.js/VUE.js/ElementUI/微信小程序/apache echarts（展示图标） 前端技术

网关层：Nginx

应用层：SpringBoot/SpringMVC/Spring Task/httpclient/springCache/JWT/阿里云oss/

Swagger（后端用于生成接口文档）/POI （操作excel）/WebSocket（协议）

数据层：MySQL/Redis/mybatis/pageHelper/spring data redis

工具：Git/maven/Junit/postman

## 开发环境搭建

整体结构：

前端（管理端web + 用户端 小程序）

后端：后端服务（Java）

### 前端环境搭建

前端工程基于nginx运行，双击nginx即可启动nginx服务，访问端口号为80

### 后端环境搭建

后端工程基于maven进行项目构建，并且进行分模块开发

Sky-take-our maven父工程，统一管理依赖版本，聚合其他子模块

Sky-common 子模块，存放公共类，例如工具类，常量类，异常类

sky-pojo 子模块，存放实体类，VO DTO等

（

DTO：数据传输对象，通常用于程序中各层之间传递数据，

VO：视图对象，为前端展示数据提供的对象，

POJO：普通java对象，只有属性和对应的getter/setter

）

Sky-server 子模块，后端服务，存放配置文件，Controller，Service，Mapper

#### 数据库环境搭建

通过数据库建表语句创建数据库表结构

员工表/分类表/菜品表/菜品口味表/套餐表/套餐菜品关系表/用户表/地址表/购物车表/订单表/订单明细表

#### Nginx代理

后端的初始工程中已经实现了登录功能，直接进行前后端联调测试即可

浏览器--Controller--service--mapper--数据库

前端发送的请求，如何请求到后端服务

前端请求的地址：localhost/api/employee/login

后端接口地址：localhost：8080/admin/employee/login

后端基于tomcat内嵌服务器，端口为8080 接口并不匹配

原因：nginx反向代理，将前端发送的动态请求有nginx转发到后端服务器

浏览器 -- localhost/api/employee/login -- nginx -- localhost：8080/admin/employee/login --Tomcat

Nginx反向代理的好处：

提高访问速度

进行负载均衡（把大量请求按照我们指定的方式均衡的分配给集群中的每台服务器）

保证后端服务安全

Nginx反向代理的配置方式

1.  Location/api/{
2.     Proxy_pass http://localhost:8080/admin/;
3.  }

Nginx负载均衡的配置方式

1.  upstream webservers{
2.   server 192.168.100.128:8080;
3.   server 192.168.100.129:8080;
4.  }

6.  server{
7.   listen 80;
8.   server_name localhost;

10.  location /api/ {
11.               proxy_pass   http://webservers/admin/;  _#负载均衡_
12.  }
13. }

底层基于反向代理实现

Nginx负载均衡策略：

轮询（默认方式）

Weight：权重方式，默认为1，权重越高，被分配的客户端请求就越多

Ip_hash：依据ip分配方式，这样每个访客可以固定访问一个后端服务

Least_conn：依据最少连接方式，把请求优先分配给连接数少的后端服务

Url_hash：依据url分配方式，这样相同的url会被分配到同一个后端服务

Fair：依据响应时间方式，响应时间短的服务将会被优先分配

### 完善登录功能

问题：员工表中的密码是明文存储，安全性太低

解决：将密码加密后存储，提高安全性，使用MD5加密算法对明文密码加密（不可逆）

修改数据库中明文密码，改为MD5加密后的密文

修改java代码，前端提交的密码进行MD5加密后在跟数据库中的密码比对

1.          _//密码比对_
2.          _//对于前端传来的明文密码进行md5加密，然后再进行比对_
3.          password = DigestUtils.md5DigestAsHex(password.getBytes());
4.          if (!password.equals(employee.getPassword())) {
5.              _//密码错误_
6.              throw new PasswordErrorException(MessageConstant.PASSWORD_ERROR);
7.          }

9.          if (employee.getStatus() == StatusConstant.DISABLE) {
10.             _//账号被锁定_
11.             throw new AccountLockedException(MessageConstant.ACCOUNT_LOCKED);
12.         }

### 导入接口文档

#### 前后端分离开发流程

定制接口 - 前端开发/后端开发 - 联调（校验格式） - 提测（提测）

### Swagger

#### 介绍

使用Swagger你只需要按照它的规范去定义接口以及接口相关的信息，就可以做到生成接口文档，在线接口调试页面

Knifej是为java MVC框架集成Swagger生成Api文档的增强解决方案

#### 使用方式

导入knife4j的maven坐标

在配置类中加入knife4j相关配置

设置静态资源映射 否则接口文档页面无法访问

1.  _/\*\*_
2.       \* 通过knife4j生成接口文档
3.       \* @return
4.       \*/
5.      @Bean
6.      public Docket docket() {
7.          ApiInfo apiInfo = new ApiInfoBuilder()
8.                  .title("苍穹外卖项目接口文档")
9.                  .version("2.0")
10.                 .description("苍穹外卖项目接口文档")
11.                 .build();
12.         Docket docket = new Docket(DocumentationType.SWAGGER_2)
13.                 .apiInfo(apiInfo)
14.                 .select()
15.                 .apis(RequestHandlerSelectors.basePackage("com.sky.controller"))
16.                 .paths(PathSelectors.any())
17.                 .build();
18.         return docket;
19.     }

21.     _/\*\*_
22.      \* 设置静态资源映射
23.      \* @param registry
24.      \*/
25.     protected void addResourceHandlers(ResourceHandlerRegistry registry) {
26.         registry.addResourceHandler("/doc.html").addResourceLocations("classpath:/META-INF/resources/");
27.         registry.addResourceHandler("/webjars/\*\*").addResourceLocations("classpath:/META-INF/resources/webjars/");
28.     }

生成如上

Postman/Yapi是设计阶段使用的工具，管理和维护接口

Swagger在开发阶段使用的框架，帮助后端开发人员做后端的接口测试

#### 常用注解

通过注解可以控制生成的接口文档，是接口文档拥有更好的可读性，常用注解如下

@Api 用在类上，例如Controller，表示到类的说明

@ApiModel 用在类上，例如entity DTO VO

@ApiModelProperty 用在属性上，描述属性信息

@ApiOperation 用在方法上 例如Controller的方法 说明方法的用途 作用

注解示例

1.  _/\*\*_
2.       \* 登录
3.       \*
4.       \* @param employeeLoginDTO
5.       \* @return
6.       \*/
7.      @PostMapping("/login")
8.      @ApiOperation("员工登录")
9.      public Result&lt;EmployeeLoginVO&gt; login(@RequestBody EmployeeLoginDTO employeeLoginDTO) {}

1.  @RestController
2.  @RequestMapping("/admin/employee")
3.  @Slf4j
4.  @Api(tags = "员工相关接口")

通过注解影响接口文档的生成

## 员工管理

新增员工/员工分页查询/启用禁用员工账号/编辑员工/导入分类模块功能代码

### 新增员工

#### 需求分析和设计

账号必须是唯一的/手机号校验，必须为11位手机号码（不能重复？）/

性别二选一/身份证是合法的18位身份证号码

密码默认为123456 后续可修改

使用Post请求提交json格式数据

项目约定：

管理端发出的请求，统一使用/admin作为前缀

用户端发出的请求，统一使用/user作为前缀

#### 代码开发

根据新增员工接口设计对应的DTO

如果直接使用实体类来接收？-可以 但当前端提交的数据和实体类中对应的属性差别比较大时，建议使用DTO来封装数据（精确封装）

EmployeeController

1.  _/\*\*_
2.       \* 新增员工
3.       \*
4.       \* @param employeeDTO
5.       \* @return
6.       \*/
7.      @PostMapping
8.      @ApiOperation("新增员工")
9.      public Result save(@RequestBody EmployeeDTO employeeDTO) {
10.         log.info("新增员工，员工数据：{}", employeeDTO);
11.         employeeService.save(employeeDTO);
12.         return Result.success();
13.     }

employeeService

employeeServiceImpl

1.      _/\*\*_
2.       \* 新增员工
3.       \*
4.       \* @param employeeDTO
5.       \*/
6.      public void save(EmployeeDTO employeeDTO) {
7.          Employee employee = new Employee();

9.          _// 对象属性拷贝(属性名要一致）_
10.         BeanUtils.copyProperties(employeeDTO, employee);

12.         _// 设置账号状态，默认正常状态_
13.         employee.setStatus(StatusConstant.ENABLE);

15.         _//设置密码，默认密码123456 （需要进行md5加密）_
16.         employee.setPassword(DigestUtils.md5DigestAsHex(PasswordConstant.DEFAULT_PASSWORD.getBytes()));

18.         _//设置当前记录的创建时间和修改时间_
19.         employee.setCreateTime(LocalDateTime.now());
20.         employee.setUpdateTime(LocalDateTime.now());

22.         _// 设置当前记录创建人id和修改人id_
23.         _// TODO: 改为当前登录用户的id_
24.         employee.setCreateUser(10L);
25.         employee.setUpdateUser(10L);

27.         employeeMapper.insert(employee);
28.     }

#### 功能测试

通过接口文档（swagger）测试

通过前后端联调测试（如果前端没有开发好 则无法联调）

开发阶段中，后端测试主要以接口文档测试为主

#### 代码完善

程序存在的问题：

##### 录入的用户名已存在

抛出异常后没有处理 只会报500错

1.      _/\*\*_
2.       \* 处理数据重复录入异常
3.       \* @param ex
4.       \* @return
5.       \*/
6.      @ExceptionHandler
7.      public Result exceptionHandler(SQLIntegrityConstraintViolationException ex){
8.          _//Duplicate entry 'zhangsan' for key 'idx_username'_
9.          String message = ex.getMessage();
10.         if(message.contains("Duplicate entry")){
11.             String\[\] split = message.split(" ");
12.             String username = split\[2\];
13.             String msg = username + MessageConstant.ALREADY_EXISTS;
14.             return Result.error(msg);
15.         }else{
16.             return Result.error(MessageConstant.UNKNOWN_ERROR);
17.         }
18.     }

##### 新增员工时，创建人id和修改人id设置为了固定值

需要通过某种动态获取当前登录员工的id

认证流程：前端用户认证（提交用户名和密码）— 后端认证通过 生成JWT token返回给前端 — 前端在本地保存JWT Token — 后续请求后端接口 每次都在请求头中携带JWT token —被拦截器截获 拦截请求验证JWT token 通过则执行业务逻辑 反之则返回错误信息（401 未授权）

面临的问题 ： 解析出登录员工id后，如何传递给Service中的Save方法

解决：ThreadLocal 是 Thread的局部变量

为每个线程提供单独一份存储空间（因为每一个请求都是单独的线程） 具有线程隔离的效果 只有在线程内才能获取到对应的值 线程外则不能访问

1.  public class BaseContext {

3.      public static ThreadLocal&lt;Long&gt; threadLocal = new ThreadLocal<>();

5.      public static void setCurrentId(Long id) {
6.          threadLocal.set(id);
7.      }

9.      public static Long getCurrentId() {
10.         return threadLocal.get();
11.     }

13.     public static void removeCurrentId() {
14.         threadLocal.remove();
15.     }

17. }

BaseContext 是一个用于保存和管理当前线程用户 ID 的工具类。它通过 ThreadLocal&lt;Long&gt; 实现线程隔离，每个线程都可以独立存取自己的用户 ID，常用于登录态或用户上下文的保存。

setCurrentId(Long id)：设置当前线程的用户 ID。

getCurrentId()：获取当前线程的用户 ID。

removeCurrentId()：移除当前线程的用户 ID，防止内存泄漏。

拦截器

1.  public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
2.          _//判断当前拦截到的是Controller的方法还是其他资源_
3.          if (!(handler instanceof HandlerMethod)) {
4.              _//当前拦截到的不是动态方法，直接放行_
5.              return true;
6.          }

8.          _//1、从请求头中获取令牌_
9.          String token = request.getHeader(jwtProperties.getAdminTokenName());

11.         _//2、校验令牌_
12.         try {
13.             log.info("jwt校验:{}", token);
14.             Claims claims = JwtUtil.parseJWT(jwtProperties.getAdminSecretKey(), token);
15.             Long empId = Long.valueOf(claims.get(JwtClaimsConstant.EMP_ID).toString());
16.             log.info("当前员工id：", empId);
17.             BaseContext.setCurrentId(empId);
18.             _//3、通过，放行_
19.             return true;
20.         } catch (Exception ex) {
21.             _//4、不通过，响应401状态码_
22.             response.setStatus(401);
23.             return false;
24.         }
25.     }

ServiceImpl

1.          _// 设置当前记录创建人id和修改人id_
2.          _// 改为当前登录用户的id_
3.          employee.setCreateUser(BaseContext.getCurrentId());
4.          employee.setUpdateUser(BaseContext.getCurrentId());

### 员工分页查询

#### 需求分析和设计

根据页码展示员工信息/每页展示10条数据/分页查询时可以根据需要 输入员工姓名进行查询

前端接口需要提交三个数据：页码page/每页展示的数据数pageSize/员工的姓名name

后端响应的：总的记录数total / 当前页需要展示的数据集合 records

#### 代码开发

根据分页查询接口设计对应的DTO 只需要封装name/page/pageSize

后面所有的分页查询，统一封装成PageResult对象

1.  @Data
2.  @AllArgsConstructor
3.  @NoArgsConstructor
4.  public class PageResult implements Serializable {
5.      private long total; _//总记录数_
6.      private List records; _//当前页数据集合_
7.  }

员工信息分页查询后端返回的对象类型为Result&lt;PageResult&gt;

1.      _/\*\*_
2.       \* 员工分页查询
3.       \*
4.       \* @param employeePageQueryDTO
5.       \* @return
6.       \*/
7.      @GetMapping("/page")
8.      @ApiOperation("员工分页查询")
9.      public Result&lt;PageResult&gt; page (EmployeePageQueryDTO employeePageQueryDTO) {
10.         log.info("员工分页查询，查询条件：{}", employeePageQueryDTO);
11.         PageResult pageResult = employeeService.pageQuery(employeePageQueryDTO);
12.         return Result.success(pageResult);
13.     }

使用pageHelper辅助分页，底层基于拦截器实现

1.      @Override
2.      public PageResult pageQuery(EmployeePageQueryDTO employeePageQueryDTO) {
3.          _//select \* from employee limit 0,10_
4.          _//开始分页查询_
5.          PageHelper.startPage(employeePageQueryDTO.getPage(), employeePageQueryDTO.getPageSize());

7.          Page&lt;Employee&gt; page = employeeMapper.pageQuery(employeePageQueryDTO);

9.          long total = page.getTotal();
10.         List&lt;Employee&gt; records = page.getResult();

12.         return new PageResult(total, records);
13.     }

Mapper

1.      &lt;select id = "pageQuery"  resultType = "com.sky.entity.Employee"&gt;
2.          select \* from employee
3.          &lt;where&gt;
4.              &lt;if test="name != null and name != ''"&gt;
5.                  and name like concat('%', _#{name}, '%')_
6.              &lt;/if&gt;
7.          &lt;/where&gt;
8.          order by update_time desc
9.      &lt;/select&gt;

PageHelper会自动地拼接limit条件 接收体中封装了前端传来的分页DTO

#### 功能测试

可以通过接口文档进行测试，也可以进行前后端联调测试

问题：最后操作时间字段展示有问题

返回给前端的数据有问题 展示的形式不符合习惯

#### 代码完善

解决方式：

方式一：在属性上加入注解，对日期进行格式化

方式二：在WebMvcConfiguration中扩展springMVC的消息转换器，统一对日期类型进行格式化处理

1.      _/\*\*_
2.       \* 扩展springMVC的消息转换器
3.       \* @param converters
4.       \*/
5.      protected  void extendMessageConverters(List&lt;HttpMessageConverter<?&gt;> converters) {
6.          _// 创建一个消息转换器对象_
7.          MappingJackson2HttpMessageConverter converter = new MappingJackson2HttpMessageConverter();
8.          _//需要为消息转换器设置一个对象转换器 对象转换器可以将Java对象序列化转为json_
9.          converter.setObjectMapper(new JacksonObjectMapper());
10.     }
11. _//将自己的消息转换器加入容器中_
12. converters.add(0,converter);

1.  public class JacksonObjectMapper extends ObjectMapper {

3.      public static final String DEFAULT_DATE_FORMAT = "yyyy-MM-dd";
4.      _//public static final String DEFAULT_DATE_TIME_FORMAT = "yyyy-MM-dd HH:mm:ss";_
5.      public static final String DEFAULT_DATE_TIME_FORMAT = "yyyy-MM-dd HH:mm";
6.      public static final String DEFAULT_TIME_FORMAT = "HH:mm:ss";

8.      public JacksonObjectMapper() {
9.          super();
10.         _//收到未知属性时不报异常_
11.         this.configure(FAIL_ON_UNKNOWN_PROPERTIES, false);

13.         _//反序列化时，属性不存在的兼容处理_
14.         this.getDeserializationConfig().withoutFeatures(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);

16.         SimpleModule simpleModule = new SimpleModule()
17.                 .addDeserializer(LocalDateTime.class, new LocalDateTimeDeserializer(DateTimeFormatter.ofPattern(DEFAULT_DATE_TIME_FORMAT)))
18.                 .addDeserializer(LocalDate.class, new LocalDateDeserializer(DateTimeFormatter.ofPattern(DEFAULT_DATE_FORMAT)))
19.                 .addDeserializer(LocalTime.class, new LocalTimeDeserializer(DateTimeFormatter.ofPattern(DEFAULT_TIME_FORMAT)))
20.                 .addSerializer(LocalDateTime.class, new LocalDateTimeSerializer(DateTimeFormatter.ofPattern(DEFAULT_DATE_TIME_FORMAT)))
21.                 .addSerializer(LocalDate.class, new LocalDateSerializer(DateTimeFormatter.ofPattern(DEFAULT_DATE_FORMAT)))
22.                 .addSerializer(LocalTime.class, new LocalTimeSerializer(DateTimeFormatter.ofPattern(DEFAULT_TIME_FORMAT)));

24.         _//注册功能模块 例如，可以添加自定义序列化器和反序列化器_
25.         this.registerModule(simpleModule);
26.     }
27. }

### 启用/禁用员工账号

#### 需求分析和设计

业务规则：可以对状态为“启用”的员工账号进行“禁用操作”/可以对状态为“禁用”的员工账号进行“启用”操作/状态为“禁用”的员工账号不能登录系统

#### 代码开发

1.      _/\*\*_
2.       \* 启用禁用员工状态
3.       \* @param status
4.       \* @param id
5.       \*/
6.      @PostMapping("/status/{status}")
7.      @ApiOperation("启用禁用员工账号")
8.      public Result startOrStop(@PathVariable Integer status, Long id) {
9.          log.info("启用禁用员工账号，员工id：{}，状态：{}", id, status);
10.         employeeService.startOrStop(status, id);
11.         return Result.success();
12.     }

ServiceImpl

1.      _/\*\*_
2.       \* 启用禁用员工
3.       \*
4.       \* @param status
5.       \* @param id
6.       \*/
7.      @Override
8.      public void startOrStop(Integer status, Long id) {
9.          _//update employee set status = ? where id = ?_
10. _/\*        Employee employee = new Employee();_
11.         employee.setId(id);
12.         employee.setStatus(status);\*/

14.         Employee employee = Employee.builder()
15.                 .status(status)
16.                 .id(id)
17.                 .build();

19.         employeeMapper.update(employee);
20.     }

这里传 employee 对象是因为 employeeMapper.update(employee) 方法需要一个包含要更新字段的实体对象。这样可以灵活地只更新需要变更的字段（比如只改状态），而不是直接传 id 和 status，避免手动拼接 SQL，提高代码可维护性和扩展性。如果后续要更新更多字段，只需在对象里设置即可，无需修改方法签名。

EmployeeMapper

1.      &lt;update id="update" parameterType="Employee"&gt;
2.          update employee
3.          &lt;set&gt;
4.              &lt;if test="name != null"&gt;name = _#{name},&lt;/if&gt;_
5.              &lt;if test="username != null"&gt;username = _#{username},&lt;/if&gt;_
6.              &lt;if test="password != null"&gt;password = _#{password},&lt;/if&gt;_
7.              &lt;if test="phone != null"&gt;phone = _#{phone},&lt;/if&gt;_
8.              &lt;if test="sex != null"&gt;sex = _#{sex} &lt;/if&gt;_
9.              &lt;if test="idNumber != null"&gt;id_number = _#{idNumber},&lt;/if&gt;_
10.             &lt;if test="status != null"&gt;status = _#{status},&lt;/if&gt;_
11.             &lt;if test="updateTime != null"&gt;update_time = _#{updateTime},&lt;/if&gt;_
12.             &lt;if test="updateUser != null"&gt;update_user = _#{updateUser}&lt;/if&gt;_
13.         &lt;/set&gt;
14.         where id = _#{id}_
15.     &lt;/update&gt;

#### 功能测试

前后端联调

### 编辑员工

#### 需求分析和设计

编辑员工功能涉及两个接口：根据id查询员工信息/编辑员工信息

#### 代码开发

需要两种功能 一个是根据用户id查询员工信息 来完成点击修改按钮后的数据复现

还有一个则是调用mapper层的update完成根据id查询

1.      _/\*\*_
2.       \* 根据id查询员工信息
3.       \* @param id
4.       \* @return
5.       \*/
6.      @GetMapping("/{id}")
7.      @ApiOperation("根据id查询员工信息")
8.      public Result&lt;Employee&gt; getById(@PathVariable Long id) {
9.          log.info("根据id查询员工信息，员工id：{}", id);
10.         Employee employee = employeeService.getById(id);
11.         return Result.success(employee);
12.     }

14.     _/\*\*_
15.      \* 编辑员工信息
16.      \* @param employeeDTO
17.      \* @return
18.      \*/
19.     @PutMapping
20.     @ApiOperation("编辑员工信息")
21.     public Result update(@RequestBody EmployeeDTO employeeDTO) {
22.         log.info("编辑员工信息，员工信息：{}", employeeDTO);
23.         employeeService.update(employeeDTO);
24.         return Result.success();
25.     }

ServiceImpl

1.      _/\*\*_
2.       \* 根据id查询员工信息
3.       \*
4.       \* @param id
5.       \* @return
6.       \*/
7.      @Override
8.      public Employee getById(Long id) {
9.          Employee employee = employeeMapper.getById(id);
10.         employee.setPassword("\*\*\*\*");
11.         return employee;
12.     }

14.     _/\*\*_
15.      \* 编辑员工信息
16.      \*
17.      \* @param employeeDTO
18.      \*/
19.     @Override
20.     public void update(EmployeeDTO employeeDTO) {
21.         _//数据拷贝_
22.         Employee employee = new Employee();
23.         BeanUtils.copyProperties(employeeDTO, employee);

25.         employee.setUpdateTime(LocalDateTime.now());
26.         employee.setUpdateUser(BaseContext.getCurrentId());

28.         employeeMapper.update(employee);
29.     }

#### 功能测试

前后端联调与Swagger测试

## 分类管理

### 需求分析和设计

分类名称必须是唯一的

分类按照类型可以分为菜品分类和套餐分类

新添加的分类状态默认为“禁用”

### 接口设计

新增分类/分类分页查询/根据id删除分类/修改分类/启用禁用分类/根据类型查询分类

### 数据库开发

（category表）

Id 自增/name 唯一/type-菜品分类 套餐分类/sort-用于分类数据的排序/status/create_time/update_time/create_user/update_user

### 代码导入

. . .

### 功能测试

前后端联调

## 菜品管理

### 公共字段自动填充

偏向技术

业务表中有公共字段例如创建时间/创建人id/修改时间/修改人id，此前一直使用set来设置 会造成代码冗余

示例：

1.          _//设置当前记录的创建时间和修改时间_
2.          employee.setCreateTime(LocalDateTime.now());
3.          employee.setUpdateTime(LocalDateTime.now());

5.          _// 设置当前记录创建人id和修改人id_
6.          _// 改为当前登录用户的id_
7.          employee.setCreateUser(BaseContext.getCurrentId());
8.          employee.setUpdateUser(BaseContext.getCurrentId());

解决：

自定义注解AutoFill 用于表示需要进行公共字段自动填充的方法

1.  _/\*\*_
2.   \* 自动填充注解 用于表示某个方法需要进行功能字段自动填充处理
3.   \*/
4.  @Target(ElementType.METHOD)
5.  @Retention(RetentionPolicy.RUNTIME)
6.  public @interface AutoFill {
7.      _//数据库操作类型：UPDATE INSERT_
8.      OperationType value();
9.  }

自定义切面类AutoFillAspect，统一拦截加入AutoFill注解的方法，通过反射为公共字段赋值

1.  _/\*\*_
2.   \* 自动填充切面类 实现公共字段自动填充逻辑
3.   \*/
4.  @Aspect
5.  @Component
6.  @Slf4j
7.  public class AutoFillAspect {

9.      _/\*\*_
10.      \* 切入点
11.      \*/
12.     @Pointcut("execution(\* com.sky.mapper.\*.\*(..)) && @annotation(com.sky.annotation.AutoFill)")
13.     public void autoFillPointCut() {}

15.     @Before("autoFillPointCut()")
16.     public void autoFill(JoinPoint joinPoint) {
17.         log.info("开始进行公共字段自动填充...");

19.         _//获取当前被拦截的方法上的数据库操作类型（链式调用）_
20.         MethodSignature signature = (MethodSignature) joinPoint.getSignature();_//方法签名对象_
21.         AutoFill autoFill = signature.getMethod().getAnnotation(AutoFill.class);_//获得方法上得注解对象_
22.         OperationType operationType = autoFill.value();_//获得数据库操作类型对象_

24.         _//获取到当前被拦截的方法的参数--实体对象_
25.         Object\[\] args = joinPoint.getArgs();
26.         if (args == null || args.length == 0) {
27.             return;
28.         }

30.         Object entity = args\[0\];

32.         _//准备赋值的数据_
33.         LocalDateTime now = LocalDateTime.now();
34.         Long currentId = BaseContext.getCurrentId();

36.         _//根据不同的操作类型进行不同的自动填充_
37.         if (operationType == OperationType.INSERT) {
38.             _//为4个公共字段赋值_
39.             try {
40.                 Method setCreateTime = entity.getClass().getDeclaredMethod(AutoFillConstant.SET_CREATE_TIME, LocalDateTime.class);
41.                 Method setUpdateTime = entity.getClass().getDeclaredMethod(AutoFillConstant.SET_UPDATE_TIME, LocalDateTime.class);
42.                 Method setCreateUser = entity.getClass().getDeclaredMethod(AutoFillConstant.SET_CREATE_USER, Long.class);
43.                 Method setUpdateUser = entity.getClass().getDeclaredMethod(AutoFillConstant.SET_UPDATE_USER, Long.class);

45.                 _//通过反射为对象属性赋值_
46.                 setCreateTime.invoke(entity, now);
47.                 setUpdateTime.invoke(entity, now);
48.                 setCreateUser.invoke(entity, currentId);
49.                 setUpdateUser.invoke(entity, currentId);

51.             } catch (Exception e) {
52.                 e.printStackTrace();
53.             }
54.         } else if (operationType == OperationType.UPDATE) {
55.             _//为2个公共字段赋值_
56.             try {
57.                 Method setUpdateTime = entity.getClass().getDeclaredMethod(AutoFillConstant.SET_UPDATE_TIME, LocalDateTime.class);
58.                 Method setUpdateUser = entity.getClass().getDeclaredMethod(AutoFillConstant.SET_UPDATE_USER, Long.class);

60.                 setUpdateTime.invoke(entity, now);
61.                 setUpdateUser.invoke(entity, currentId);
62.             } catch (Exception e) {
63.                 e.printStackTrace();
64.             }
65.         }
66.     }
67. }

在Mapper的方法中加入AutoFill注解

1.      @AutoFill(value = OperationType.INSERT)
2.      @Insert("insert into category(type, name, sort, status, create_time, update_time, create_user, update_user)" +
3.              " VALUES" +
4.              " (#{type}, #{name}, #{sort}, #{status}, #{createTime}, #{updateTime}, #{createUser}, #{updateUser})")
5.      void insert(Category category);

### 新增菜品

#### 需求分析和设计

业务规则：菜品名称必须是唯一的/菜品必须属于某个分类下，不能单独存在/新增菜品时可以根据情况选择菜品的口味/每个菜品必须对应一个图片

接口设计：根据类型查询分类（已完成）/文件上传/新增菜品

数据库设计（dish菜品表和dish_flavour口味表）

#### 代码开发

##### 开发文件上传接口

浏览器-后端服务-阿里云OSS

CommonController

1.  _/\*\*_
2.   \* 通用接口
3.   \*/
4.  @RestController
5.  @RequestMapping("/admin/common")
6.  @Api(tags = "通用接口")
7.  @Slf4j
8.  public class CommonController {

10.     @Autowired
11.     private AliOssUtil aliOssUtil;

13.     @PostMapping("/upload")
14.     @ApiOperation("文件上传")
15.     public Result&lt;String&gt; upload(MultipartFile file) {
16.         log.info("文件上传：{}", file);

18.         try {
19.             _//原始文件名_
20.             String originalFilename = file.getOriginalFilename();
21.             _//截取原始文件名的后缀_
22.             String extension = originalFilename.substring(originalFilename.lastIndexOf("."));
23.             _//新文件名称_
24.             String objectName = UUID.randomUUID().toString() + extension;

26.             _//文件的请求路径_
27.             String filePath = aliOssUtil.upload(file.getBytes(), objectName);
28.             return Result.success(filePath);
29.         } catch (IOException e) {
30.             log.error("文件上传失败", e);
31.         }

33.         return Result.error(MessageConstant.UPLOAD_FAILED);
34.     }

OssConfiguration

1.  _/\*\*_
2.   \* oss配置类 用于创建AliOssUtil对象
3.   \*/
4.  @Configuration
5.  @Slf4j
6.  public class OssConfiguration {

8.      @Bean
9.      @ConditionalOnMissingBean
10.     public AliOssUtil aliOssUtil(AliOssProperties aliOssProperties) {
11.         log.info("开始创建AliOssUtil对象，参数：{}", aliOssProperties);
12.         return new AliOssUtil(aliOssProperties.getEndpoint(),
13.                 aliOssProperties.getAccessKeyId(),
14.                 aliOssProperties.getAccessKeySecret(),
15.                 aliOssProperties.getBucketName());
16.     }
17. }

配置到环境变量中 防止密钥泄露

1.    alioss:
2.      endpoint: ${sky.alioss.endpoint}
3.      access-key-id: ${sky.alioss.access-key-id}
4.      access-key-secret: ${sky.alioss.access-key-secret}
5.      bucket-name: ${sky.alioss.bucket-name}

采用松散绑定

##### 新增菜品接口

1.  @RestController
2.  @RequestMapping("/admin/dish")
3.  @Api(tags = "菜品管理")
4.  @Slf4j
5.  public class DishController {

7.      @Autowired
8.      private DishService dishService;

10.     _/\*\*_
11.      \* 新增菜品
12.      \* @param dishDTO
13.      \* @return
14.      \*/
15.     @PostMapping
16.     @ApiOperation("新增菜品")
17.     public Result save(@RequestBody DishDTO dishDTO) {
18.         log.info("新增菜品：{}", dishDTO);
19.         dishService.saveWithFlavor(dishDTO);
20.         return Result.success();
21.     }
22. }

新增菜品要求与口味一起保存

在实现类中将新增菜品分两张表保存 先插入dishMapper再插入dishFlavorMapper

涉及到两张表所以使用事务统一的管理

1.  @Service
2.  @Slf4j
3.  public class DishServiceImpl implements DishService {

5.      @Autowired
6.      private DishMapper dishMapper;

8.      @Autowired
9.      private DishFlavorMapper dishFlavorMapper;

11.     _/\*\*_
12.      \* 新增菜品，同时保存对应的口味数据
13.      \* @param dishDTO
14.      \*/
15.     @Override
16.     @Transactional
17.     public void saveWithFlavor(DishDTO dishDTO) {

19.         Dish dish = new Dish();
20.         BeanUtils.copyProperties(dishDTO,dish);

22.         _//向菜品表中插入1条数据_
23.         dishMapper.insert(dish);

25.         _//获取insert语句生成的主键值_
26.         Long dishId = dish.getId();

28.         _//向口味表插入n条数据_
29.         List&lt;DishFlavor&gt; flavors = dishDTO.getFlavors();

31.         if(flavors != null && flavors.size() > 0){
32.             flavors.forEach(flavor -> {
33.                 flavor.setDishId(dishId);
34.             });
35.             _//向口味表插入n条数据_
36.             dishFlavorMapper.insertBatch(flavors);
37.         }
38.     }
39. }

主键返回

DishMapper

1.      &lt;insert id="insert" useGeneratedKeys="true" keyProperty="id"&gt;
2.          INSERT INTO dish (name, category_id, price, image, description, create_time, update_time,create_user, update_user,  status)
3.          VALUES (#{name}, #{categoryId}, #{price}, #{image}, #{description}, #{createTime}, #{updateTime},#{createUser}, #{updateUser},#{status})
4.      &lt;/insert&gt;

DishFlavorMapper

1.      &lt;insert id="insertBatch"&gt;
2.          INSERT INTO dish_flavor (dish_id, name, value)
3.          VALUES
4.          &lt;foreach collection="flavors" item="df" separator=","&gt;
5.              (#{df.dishId}, _#{df.name}, #{df.value})_
6.          &lt;/foreach&gt;
7.      &lt;/insert&gt;

#### 功能测试

前后端联调

### 菜品分页查询

#### 需求分析和设计

业务规则：根据页码展示菜品信息

每页展示10条数据

分页查询时可以根据需要输入菜品名称，菜品分类，菜品状态进行查询

#### 代码开发

根据菜品分页查询接口定义设计对应的DTO 这是接受的数据类型

还需要设计一个dishVO 扩展了一个categoryName 回传给前端的数据

DishController

1.      _/\*\*_
2.       \* 菜品分页查询
3.       \* @param dishPageQueryDTO
4.       \* @return
5.       \*/
6.      @GetMapping("/page")
7.      @ApiOperation("菜品分页查询")
8.      public Result&lt;PageResult&gt; page(DishPageQueryDTO dishPageQueryDTO) {
9.          log.info("菜品分页查询：{}", dishPageQueryDTO);
10.         PageResult pageResult = dishService.pageQuery(dishPageQueryDTO);
11.         return Result.success(pageResult);
12.     }

从前端获取一个DishPageQueryDTO 包含page/pageSize/name/categoryId/status

返回一个Result对象，内部封装pageResult

ServiceImpl

1.      public PageResult pageQuery(DishPageQueryDTO dishPageQueryDTO) {

3.          PageHelper.startPage(dishPageQueryDTO.getPage(),dishPageQueryDTO.getPageSize());

5.          Page&lt;DishVO&gt; page = dishMapper.pageQuery(dishPageQueryDTO);

7.          return new PageResult(page.getTotal(),page.getResult());
8.      }

page泛型DishVO 内部包含

id/name/categoryId/price/description/status/updateTime/categoryName/flavor 表示返回给前端的数据

为什么用 DishVO：

DishVO 是“视图对象”，用于返回给前端的数据结构。它通常比实体类 Dish 包含更多展示信息，比如口味、分类名等，便于页面展示和数据封装。这样可以灵活控制返回内容，避免直接暴露数据库结构

dishMapper

通过组装查询来实现

1.      &lt;select id="pageQuery" resultType="com.sky.vo.DishVO"&gt;
2.          SELECT d.\* , c.name AS categoryName from dish d left outer join category c on d.category_id = c.id
3.          &lt;where&gt;
4.              &lt;if test="name != null"&gt;
5.                  and d.name like concat('%', _#{name}, '%')_
6.              &lt;/if&gt;
7.              &lt;if test="categoryId != null"&gt;
8.                  and d.category_id = _#{categoryId}_
9.              &lt;/if&gt;
10.             &lt;if test="status != null"&gt;
11.                 and d.status = _#{status}_
12.             &lt;/if&gt;
13.         &lt;/where&gt;
14.         order by d.create_time desc
15.     &lt;/select&gt;

resultType 标签用于指定 SQL 查询结果要映射成哪个 Java 类型。

在你的例子里，resultType="com.sky.vo.DishVO" 表示查询结果会自动封装到 DishVO 类的对象中，字段名要和 SQL 查询的列名对应。这样 MyBatis 会把每一行结果转成一个 DishVO 实例，方便后续业务处理和返回前端。

#### 功能测试

前后端联调/Swagger

### 删除菜品

#### 需求分析和设计

业务规则：

可以一次删除一个菜品，也可以批量删除菜品

起售中的菜品不能删除

被套餐关联的菜品不能删除

删除菜品后，关联的口味数据也需要删除

设计数据库：

Dish表/dish_flavor表/setmeal_dish表（套餐dish关系表）

#### 代码开发

DishController

1.      @DeleteMapping
2.      @ApiOperation("菜品批量删除")
3.      public Result delete(@RequestParam List&lt;Long&gt; ids){
4.          log.info("菜品批量删除：{}", ids);
5.          dishService.deleteBatch(ids);
6.          return Result.success();
7.      }

批量删除 传入字符串ids 请求参数1，2，3 菜品id 之间用逗号分隔

@RequestParam 用于接收前端请求 URL 中的参数，并自动绑定到方法参数上。

在这里，@RequestParam List&lt;Long&gt; ids 表示前端通过类似 /admin/dish?ids=1&ids=2 传递多个 ids，Spring 会自动把这些参数组装成一个 List&lt;Long&gt; 传给 delete 方法。

DishServiceImpl

1.      _/\*\*_
2.       \* 菜品批量删除
3.       \* @param ids
4.       \*/
5.      @Override
6.      @Transactional
7.      public void deleteBatch(List&lt;Long&gt; ids) {
8.          _//判断当前菜品是否能够删除---是否存在起售中的菜品_
9.          for (Long id : ids) {
10.             Dish dish = dishMapper.getById(id);
11.             if(dish.getStatus() == StatusConstant.ENABLE){
12.                 _//当前菜品处于起售中不能删除_
13.                 throw new DeletionNotAllowedException(MessageConstant.DISH_ON_SALE);
14.             }
15.         }

17.         _//判断当前菜品是否能够删除---是否被套餐关联_
18.         List&lt;Long&gt; setmealIds = setmealDishMapper.getSetmealIdsByDishIds(ids);
19.         if(setmealIds != null && setmealIds.size() > 0){
20.             _//当前菜品被套餐关联，不能删除_
21.             throw new DeletionNotAllowedException(MessageConstant.DISH_BE_RELATED_BY_SETMEAL);
22.         }

24.         _//删除菜品表中的菜品数据_
25.         for (Long id : ids) {
26.             dishMapper.deleteById(id);
27.             _//删除菜品关联的口味数据_
28.             dishFlavorMapper.deleteByDishId(id);
29.         }
30.     }

删除操作 匹配dishId

DishFlavorMapper

1.      _/\*\*_
2.       \* 根据菜品id查删除对应的口味数据
3.       \* @param dishId
4.       \* @return
5.       \*/
6.      @Delete("delete from dish_flavor where dish_id = #{dishId}")
7.      void deleteByDishId(Long dishId);

DishMapper

1.      /\*\*
2.       \* 根据id查询菜品
3.       \*
4.       \* @param id
5.       \* @return
6.       \*/
7.      @Select("select \* from dish where id = #{id}")
8.      Dish getById(Long id);

10.     /\*\*
11.      \* 根据主键删除
12.      \* @param id
13.      \*/
14.     @Delete("delete from dish where id = #{id}")
15.     void deleteById(Long id);

根据id查询是为了获取对应id的状态 是否起售

查询确认可以删除后执行delete sql语句

#### 代码优化

此前使用for循环来对符合要求的逐个删除 以实现批量删除

现在写入sql用foreach遍历

1.      &lt;delete id="deleteByDishIds"&gt;
2.          delete from dish_flavor where dish_id in
3.          &lt;foreach collection="dishIds" item="dishId" open="(" separator="," close=")"&gt;
4.              _#{dishId}_
5.          &lt;/foreach&gt;
6.      &lt;/delete&gt;

1.      &lt;delete id="deleteByIds"&gt;
2.          delete from dish where id in
3.          &lt;foreach collection="ids" item="id" open="(" separator="," close=")"&gt;
4.              _#{id}_
5.          &lt;/foreach&gt;
6.      &lt;/delete&gt;

ServiceImpl

1.          //根据菜品id集合批量删除菜品数据
2.          //sql: delete from dish where id in (1,2,3)
3.          dishMapper.deleteByIds(ids);

5.          //根据菜品id集合批量删除关联的口味数据
6.          //sql: delete from dish_flavor where dish_id in (1,2,3)
7.          dishFlavorMapper.deleteByDishIds(ids);

### 修改菜品

#### 需求分析和设计

接口设计：根据id查询菜品（完成数据回显）

/根据类型查询分类（已实现）

/文件上传（已实现）

/修改菜品

#### 代码开发

##### 根据id查询菜品-数据回显

DishService

1.      _/\*\*_
2.       \* 根据id查询菜品及其对应的口味信息
3.       \* @param id
4.       \* @return
5.       \*/
6.      @GetMapping("/{id}")
7.      @ApiOperation("根据id查询菜品及其口味信息")
8.      public Result&lt;DishVO&gt; getById(@PathVariable Long id){
9.          log.info("根据id查询菜品及其口味信息：{}", id);
10.         DishVO dishVO = dishService.getByIdWithFlavor(id);
11.         return Result.success(dishVO);
12.     }

ServiceImpl

1.      _/\*\*_
2.       \* 根据id查询菜品及其对应的口味信息
3.       \* @param id
4.       \* @return
5.       \*/
6.      @Override
7.      public DishVO getByIdWithFlavor(Long id) {
8.          _//根据id查询菜品数据_
9.          Dish dish = dishMapper.getById(id);

11.         _//根据菜品id查询口味数据_
12.         List&lt;DishFlavor&gt; dishFlavors = dishFlavorMapper.getByDishId(id);

14.         _//将查询到的数据封装到VO_
15.         DishVO dishVO = new DishVO();
16.         BeanUtils.copyProperties(dish,dishVO);

18.         dishVO.setFlavors(dishFlavors);
19.         return dishVO;
20.     }

将查询到的数据封装到VO中返回到前端

1.      _/\*\*_
2.       \* 根据菜品id查询对应的口味数据
3.       \* @param dishId
4.       \* @return
5.       \*/
6.      @Select("select \* from dish_flavor where dish_id = #{dishId}")
7.      List&lt;DishFlavor&gt; getByDishId(Long dishId);

##### 实现修改菜品

同时修改对应的口味数据

1.      _/\*\*_
2.       \* 修改菜品，同时修改对应的口味数据
3.       \* @param dishDTO
4.       \*/
5.      @PutMapping
6.      @ApiOperation("修改菜品")
7.      public Result update(@RequestBody DishDTO dishDTO){
8.          dishService.updateWithFlavor(dishDTO);
9.          return Result.success();
10.     }

修改菜品 底层采用删除原有的口味数据 再插入新的口味数据

为了简化操作并提高代码复用 并且因为口味操作可能涉及的增删改复杂 所以这里先删除原有口味数据 再插入操作

1.      _/\*\*_
2.       \* 修改菜品，同时修改对应的口味数据
3.       \* @param dishDTO
4.       \*/
5.      @Override
6.      @Transactional
7.      public void updateWithFlavor(DishDTO dishDTO) {
8.          _//由于只修改基本数据 不修改口味数据_
9.          Dish dish = new Dish();
10.         BeanUtils.copyProperties(dishDTO,dish);

12.         _//修改菜品表基本数据_
13.         dishMapper.update(dish);

15.         _//删除原有的口味数据_
16.         dishFlavorMapper.deleteByDishId(dish.getId());

18.         _//插入新的口味数据_
19.         List&lt;DishFlavor&gt; flavors = dishDTO.getFlavors();
20.         if(flavors != null && flavors.size() > 0){
21.             flavors.forEach(flavor -> {
22.                 flavor.setDishId(dish.getId());
23.             });
24.             _//向口味表插入n条数据_
25.             dishFlavorMapper.insertBatch(flavors);
26.         }
27.     }

#### 功能测试

前后端联调

## 店铺营业状态管理

### Redis入门

Redis是一个基于内存的key-value 基于内存存储，读写性能高，适合存储热点数据（热点商品 咨询 新闻）

### Redis常用命令在java中操作Redis店铺营业状态设置

#### 需求分析

接口设计：设置营业状态/管理端查询营业状态/用户端查询营业状态

本项目约定：

管理端发出的请求，统一使用/admin作为前缀

用户端发出的请求，统一使用/user作为前缀

营业状态数据存储方式：基于Redis的字符串进行存储 因为字符串总是0/1

SHOP_STATUS作为键

#### 代码开发

RedisConfiguration

1.  @Configuration
2.  @Slf4j
3.  public class RedisConfigurartion {

5.      @Bean
6.      public RedisTemplate redisTemplate(RedisConnectionFactory redisConnectionFactory) {
7.          log.info("开始创建redis模板对象...");
8.          RedisTemplate redisTemplate = new RedisTemplate();
9.          _//设置redis的连接工厂对象_
10.         redisTemplate.setConnectionFactory(redisConnectionFactory);
11.         _//设置key的序列化器_
12.         redisTemplate.setKeySerializer(new StringRedisSerializer());
13.         return redisTemplate;
14.     }
15. }

1.  @RestController("adminShopController")
2.  @RequestMapping("/admin/shop")
3.  @Api(tags = "店铺相关接口")
4.  @Slf4j
5.  public class ShopController {

7.      public static final String SHOP_STATUS_KEY = "SHOP_STATUS";

9.      @Autowired
10.     private RedisTemplate redisTemplate;

12.     _/\*\*_
13.      \* 店铺状态修改
14.      \* @param status
15.      \* @return
16.      \*/
17.     @PutMapping("/{status}")
18.     @ApiOperation("店铺状态修改")
19.     public Result setStatus(@PathVariable Integer status){
20.         log.info("店铺状态修改为，status：{}", status == 1 ? "营业中" : "打烊中");
21.         redisTemplate.opsForValue().set(SHOP_STATUS_KEY, status);
22.         return Result.success();
23.     }

25.     _/\*\*_
26.      \* 店铺状态查询
27.      \* @return
28.      \*/
29.     @GetMapping("/status")
30.     @ApiOperation("店铺状态查询")
31.     public Result&lt;Integer&gt; getStatus(){
32.         Integer status = (Integer) redisTemplate.opsForValue().get(SHOP_STATUS_KEY);
33.         log.info("店铺状态查询，status：{}", status == 1 ? "营业中" : "打烊中");
34.         return Result.success(status);
35.     }
36. }

#### 功能测试

Swagger