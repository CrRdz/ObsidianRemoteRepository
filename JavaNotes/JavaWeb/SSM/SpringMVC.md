SpringMVC 技术与 Servlet 技术功能等同，均属于 Web（表现层）层开发技术。

# SpringMVC 简介

- `@ResponseBody` 注解用于将控制器方法返回的对象转换为 JSON 或 XML 数据并直接写入 HTTP 响应体，常用于异步请求处理。
    
- `@RequestBody` 则用于从前端请求中读取 JSON 或 XML 数据，并将其绑定到方法参数上。
    

**架构分层对比：**

- **表现层**：HTML (此前使用 Servlet，现在使用 SpringMVC 替代)
    
- **业务层**：Service
    
- **数据层**：MyBatis
    
- **前端技术栈**：CSS, VUE, ElementUI
    

**定义**：SpringMVC 是一种基于 Java 实现 MVC 模型的轻量级 Web 框架。

**优点**：使用简单，开发便捷，灵活性强。

---

# SpringMVC 入门案例

## 1. 导入坐标

使用 SpringMVC 技术需要先导入 SpringMVC 与 Servlet 坐标。

```XML
<dependency>
  <groupId>javax.servlet</groupId>
  <artifactId>javax.servlet-api</artifactId>
  <version>3.1.0</version>
  <scope>provided</scope>
</dependency>
<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-webmvc</artifactId>
  <version>5.2.10.RELEASE</version>
</dependency>
```

## 2. 创建 SpringMVC 控制器类

同 Servlet，定义表现层控制器 Bean。

```Java
// 定义表现层控制器bean
@Controller
public class UserController {

    // 设置映射路径为/save，即外部访问路径
    @RequestMapping("/save")
    // 设置当前操作返回结果为指定json数据（本质上是一个字符串信息）
    @ResponseBody
    public String save(){
        System.out.println("user save ...");
        return "{'info':'springmvc'}";
    }

    // 设置映射路径为/delete，即外部访问路径
    @RequestMapping("/delete")
    @ResponseBody
    public String delete(){
        System.out.println("user save ...");
        return "{'info':'springmvc'}";
    }
}
```

## 3. 初始化 SpringMVC 环境

设定 SpringMVC 加载 Controller 对应的 Bean。

```Java
// springmvc配置类，本质上还是一个spring配置类
@Configuration
@ComponentScan("com.itheima.controller")
public class SpringMvcConfig {
}
```

## 4. 初始化 Servlet 容器

加载 SpringMVC 环境并设置 SpringMVC 技术处理的请求。

```Java
// web容器配置类
public class ServletContainersInitConfig extends AbstractDispatcherServletInitializer {
    // 加载springmvc配置类，产生springmvc容器（本质还是spring容器）
    protected WebApplicationContext createServletApplicationContext() {
        // 初始化WebApplicationContext对象
        AnnotationConfigWebApplicationContext ctx = new AnnotationConfigWebApplicationContext();
        // 加载指定配置类
        ctx.register(SpringMvcConfig.class);
        return ctx;
    }

    // 设置由springmvc控制器处理的请求映射路径 哪些请求归属SpringMVC处理
    protected String[] getServletMappings() {
        return new String[]{"/"};
    }

    // 加载spring配置类
    protected WebApplicationContext createRootApplicationContext() {
        return null;
    }
}
```

**核心注解说明**：

- `@Controller` (类注解)：SpringMVC 控制器定义上方，设定 SpringMVC 的核心控制器 Bean。
    
- `@ResponseBody` (方法注解)：SpringMVC 控制器方法定义上方，设置当前控制器方法响应内容为当前返回值，无需解析。
    

## 5. 入门案例工作流程

**启动服务器初始化过程**：

1. 服务器启动，执行 `ServletContainerInitConfig` 类，初始化 Web 容器。
    
2. 执行 `createServletAplicationContext` 方法，创建 `WebApplicationContext` 对象。
    
3. 加载 `SpringMvcConfig`。
    
4. 执行 `@ComponentScan` 加载对应的 Bean。
    
5. 加载 `UserController`，每个 `@RequestMapping` 的名称对应一个具体方法。
    
6. 执行 `getServletMappings` 方法，定义所有的请求都通过 SpringMVC。
    

**单次请求过程**：

1. 发送请求 `localhost/save`。
    
2. Web 容器发现所有请求都经过 SpringMVC，将请求交给 SpringMVC 处理。
    
3. 解析请求路径 `/save`。
    
4. 由 `/save` 匹配执行对应的方法 `save()`。
    
5. 执行 `save()`。
    
6. 检测到 `@ResponseBody` 直接将 `save()` 方法的返回值作为响应请求体返回给请求方。
    

## 6. Bean 加载控制

问题：怎么避免 Spring 错误地加载到 Controller（SpringMVC）的 Bean？

方案：加载 Spring 控制的 Bean 的时候，排除掉 SpringMVC 控制的 Bean。

**方式：扫描指定包并过滤**

```Java
@Configuration
// @ComponentScan({"com.itheima.service","com.itheima.dao"})
// 设置spring配置类加载bean时的过滤规则，当前要求排除掉表现层对应的bean
// excludeFilters属性：设置扫描加载bean时，排除的过滤规则
// type属性：设置排除规则，当前使用按照bean定义时的注解类型进行排除
// classes属性：设置排除的具体注解类，当前设置排除@Controller定义的bean
@ComponentScan(value="com.itheima",
    excludeFilters = @ComponentScan.Filter(
        type = FilterType.ANNOTATION,
        classes = Controller.class
    )
)
public class SpringConfig {
}
```

_过滤规则类型：_

- `ANNOTATION`：按照注解过滤
    
- `ASSIGNABLE_TYPE`：按照类型过滤
    
- `ASPECTJ`：按照 ASPECTJ 表达式过滤
    
- `REGEX`：按照正则表达式过滤
    
- `CUSTOM`：按照自定义的过滤规则过滤
    

**简化开发配置类**：

```Java
// web配置类简化开发，仅设置配置类类名即可
public class ServletContainersInitConfig extends AbstractAnnotationConfigDispatcherServletInitializer {

    protected Class<?>[] getRootConfigClasses() {
        return new Class[]{SpringConfig.class};
    }

    protected Class<?>[] getServletConfigClasses() {
        return new Class[]{SpringMvcConfig.class};
    }

    protected String[] getServletMappings() {
        return new String[]{"/"};
    }
}
```

---

# 请求与响应

## 请求映射路径

- `@RequestMapping` (方法注解/类注解)：类上方配置的请求映射与方法上面配置的请求映射连接在一起，形成完整的请求映射路径。常用于设置模块名作为请求路径前缀。
    
```Java
@Controller
@RequestMapping("/user")
public class UserController {
    @RequestMapping("/save")
    @ResponseBody
    public String save(){
        System.out.println("user save ...");
        return "{'module':'user save'}";
    }
}
```

## 请求参数

### 1. 普通参数传递

**请求参数与形参名称相同**：

```Java
@RequestMapping("/commonParam")
@ResponseBody
public String commonParam(String name ,int age){
    System.out.println("普通参数传递 name ==> "+name);
    System.out.println("普通参数传递 age ==> "+age);
    return "{'module':'common param'}";
}
```

**请求参数与形参名称不同**：使用 `@RequestParam` 注解关联。

```Java
@RequestMapping("/commonParamDifferentName")
@ResponseBody
public String commonParamDifferentName(@RequestParam("name") String userName , int age){
    System.out.println("普通参数传递 userName ==> "+userName);
    return "{'module':'common param different name'}";
}
```

**中文乱码处理** (`ServletContainerInitConfig`)：

```Java
@Override
protected Filter[] getServletFilters() {
    CharacterEncodingFilter filter = new CharacterEncodingFilter();
    filter.setEncoding("UTF-8");
    return new Filter[]{filter};
}
```

### 2. POJO 参数传递

请求参数与形参对象属性名相同，定义 POJO 类型形参即可接受参数。

```Java
@RequestMapping("/pojoParam")
@ResponseBody
public String pojoParam(User user){
    System.out.println("pojo参数传递 user ==> "+user);
    return "{'module':'pojo param'}";
}
```

### 3. 嵌套 POJO 参数传递

嵌套属性按照层次结构设定名称即可（如 `address.city`）。

### 4. 数组与集合传参

- **数组**：同名请求参数可以直接映射到对应名称的形参数组对象中。
    
- **集合**：同名请求参数可以使用 `@RequestParam` 注解映射到对应名称的集合对象中。
    
```Java
@RequestMapping("/listParam")
@ResponseBody
public String listParam(@RequestParam List<String> likes){
    System.out.println("集合参数传递 likes ==> "+ likes);
    return "{'module':'list param'}";
}
```

### 5. JSON 数据传递参数

**Step 1: 导入依赖**



```XML
<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-databind</artifactId>
  <version>2.9.0</version>
</dependency>
```

Step 2: 开启 JSON 自动转换

在配置类中添加 @EnableWebMvc。

Step 3: 接收 JSON 数据

使用 @RequestBody 注解将外部传递的 JSON 数据映射到形参。

```Java
// 集合参数：json格式
@RequestMapping("/listPojoParamForJson")
@ResponseBody
public String listPojoParamForJson(@RequestBody List<User> list){
    System.out.println("list pojo(json)参数传递 list ==> "+list);
    return "{'module':'list pojo for json param'}";
}

// POJO参数：json格式
@RequestMapping("/pojoParamForJson")
@ResponseBody
public String pojoParamForJson(@RequestBody User user){
    System.out.println("pojo(json)参数传递 user ==> "+user);
    return "{'module':'pojo for json param'}";
}
```

### 6. 日期类型参数传递

使用 `@DateTimeFormat` 注解设置日期类型数据格式。

```Java
@RequestMapping("/dataParam")
@ResponseBody
public String dataParam(Date date,
                        @DateTimeFormat(pattern="yyyy-MM-dd") Date date1,
                        @DateTimeFormat(pattern="yyyy/MM/dd HH:mm:ss") Date date2){
    return "{'module':'data param'}";
}
```

## 响应

**响应页面**：返回值为 String 类型，设置返回值为页面名称。

```Java
@RequestMapping("/toJumpPage")
public String toJumpPage(){
    return "page.jsp";
}
```

**响应文本数据**：需要依赖 `@ResponseBody` 注解。

```Java
@RequestMapping("/toText")
@ResponseBody
public String toText(){
    return "response text";
}
```

**响应 POJO 对象 (JSON)**：返回值为实体类对象，配合 `@ResponseBody` 和 `@EnableWebMvc`。

```Java
@RequestMapping("/toJsonPOJO")
@ResponseBody
public User toJsonPOJO(){
    User user = new User();
    user.setName("itcast");
    return user;
}
```

---

# REST 风格

**简介**：REST (Representational State Transfer) 表现形式状态转换。

- **HTTP 动作约定**：
    
    - `GET`: 查询 (http://localhost/user/1)
        
    - `POST`: 新增 (http://localhost/user)
        
    - `PUT`: 修改 (http://localhost/user)
        
    - `DELETE`: 删除 (http://localhost/user/1)
        

## RESTful 入门案例

使用 `@PathVariable` 接收路径变量。

```Java
// 删除
@RequestMapping(value = "/users/{id}", method = RequestMethod.DELETE)
@ResponseBody
public String delete(@PathVariable Integer id){
    System.out.println("user delete..." + id);
    return "{'module':'user delete'}";
}

// 保存
@RequestMapping(value = "/users", method = RequestMethod.POST)
@ResponseBody
public String save(){
    return "{'module':'user save'}";
}
```

## REST 快速开发（简化注解）

使用 @RestController 替换 @Controller + @ResponseBody。

使用 @GetMapping, @PostMapping, @PutMapping, @DeleteMapping 简化映射配置。

```Java
@RestController
@RequestMapping("/books")
public class BookController {

    @PostMapping
    public String save(@RequestBody Book book){
        System.out.println("book save..." + book);
        return "{'module':'book save'}";
    }

    @DeleteMapping("/{id}")
    public String delete(@PathVariable Integer id){
        System.out.println("book delete..." + id);
        return "{'module':'book delete'}";
    }
    // ... 其他方法类似
}
```

## 案例：基于 RESTful 页面数据交互

静态资源访问放行：

新建配置类继承 WebMvcConfigurationSupport。

```Java
@Configuration
public class SpringMvcSupport extends WebMvcConfigurationSupport {
    @Override
    protected void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/pages/**").addResourceLocations("/pages/");
        registry.addResourceHandler("/js/**").addResourceLocations("/js/");
        registry.addResourceHandler("/css/**").addResourceLocations("/css/");
        registry.addResourceHandler("/plugins/**").addResourceLocations("/plugins/");
    }
}
```

---

# SSM 整合

## 1. 整合流程

1. **创建工程**：导入 Spring-webmvc, Spring-jdbc, Spring-test, Mybatis, Mysql, Druid, Junit, Servlet, Jackson 等坐标。
    
2. **Spring Config**: 加载 JdbcConfig, MyBatisConfig, 开启事务。
    
3. **MyBatis Config**: `SqlSessionFactoryBean`, `MapperScannerConfigurer` (在 xml 中通常省略，Java 配置需注意)。
    
4. **SpringMVC Config**: 扫描 Controller, `@EnableWebMvc`。
    
5. **Servlet Config**: 加载配置类，设置映射路径。
    

## 2. SSM 整合配置示例

**SpringConfig**:

```Java
@Configuration
@ComponentScan({"com.itheima.service"})
@PropertySource("classpath:jdbc.properties")
@Import({JdbcConfig.class, MyBatisConfig.class})
@EnableTransactionManagement
public class SpringConfig {
}
```

**JdbcConfig**:


```Java
public class JdbcConfig {
    @Value("${jdbc.driver}")
    private String driver;
    @Value("${jdbc.url}")
    private String url;
    @Value("${jdbc.username}")
    private String username;
    @Value("${jdbc.password}")
    private String password;

    @Bean
    public DataSource dataSource(){
        DruidDataSource dataSource = new DruidDataSource();
        dataSource.setDriverClassName(driver);
        dataSource.setUrl(url);
        dataSource.setUsername(username);
        dataSource.setPassword(password);
        return dataSource;
    }

    @Bean
    public PlatformTransactionManager transactionManager(DataSource dataSource){
        DataSourceTransactionManager ds = new DataSourceTransactionManager();
        ds.setDataSource(dataSource);
        return ds;
    }
}
```

**MyBatisConfig**:

```Java
public class MyBatisConfig {
    @Bean
    public SqlSessionFactoryBean sqlSessionFactory(DataSource dataSource){
        SqlSessionFactoryBean factoryBean = new SqlSessionFactoryBean();
        factoryBean.setDataSource(dataSource);
        factoryBean.setTypeAliasesPackage("com.itheima.domain");
        return factoryBean;
    }
}
```

**SpringMvcConfig**:

```Java
@Configuration
@ComponentScan("com.itheima.controller")
@EnableWebMvc
public class SpringMvcConfig {
}
```

## 3. 表现层数据封装（Result）

定义统一的返回结果格式。

```Java
public class Result {
    private Object data;
    private Integer code;
    private String msg;

    public Result() {}
    public Result(Integer code,Object data) {
        this.data = data;
        this.code = code;
    }
    public Result(Integer code, Object data, String msg) {
        this.data = data;
        this.code = code;
        this.msg = msg;
    }
    // Getters and Setters...
}
```

**状态码 Code 类**:

```Java
public class Code {
    public static final Integer SAVE_OK = 20011;
    public static final Integer DELETE_OK = 20021;
    public static final Integer UPDATE_OK = 20031;
    public static final Integer GET_OK = 20041;

    public static final Integer SAVE_ERR = 20010;
    public static final Integer DELETE_ERR = 20020;
    public static final Integer UPDATE_ERR = 20030;
    public static final Integer GET_ERR = 20040;
    public static final Integer SYSTEM_UNKNOW_ERR = 59999;
}
```

## 4. 异常处理器

使用 `@RestControllerAdvice` 和 `@ExceptionHandler` 集中处理异常。

```Java
@RestControllerAdvice
public class ProjectExceptionAdvice {
    // 处理系统异常
    @ExceptionHandler(SystemException.class)
    public Result doSystemException(SystemException ex){
        // 记录日志、发送消息给运维/开发
        return new Result(ex.getCode(), null, ex.getMessage());
    }

    // 处理业务异常
    @ExceptionHandler(BusinessException.class)
    public Result doBusinessException(BusinessException ex){
        return new Result(ex.getCode(), null, ex.getMessage());
    }

    // 处理未知异常
    @ExceptionHandler(Exception.class)
    public Result doOtherException(Exception ex){
        return new Result(Code.SYSTEM_UNKNOW_ERR, null, "系统繁忙，请稍后再试！");
    }
}
```

**自定义异常类**：

```Java
public class BusinessException extends RuntimeException{
    private Integer code;
    public BusinessException(Integer code, String message) {
        super(message);
        this.code = code;
    }
    // Getters/Setters...
}
```

## 5. 前端整合 (Vue + Axios)

**列表查询**:
```JavaScript

getAll() {
    axios.get("/books").then((res)=>{
        this.dataList = res.data.data;
    });
}
```

**添加操作**:

```JavaScript
handleAdd() {
    axios.post("/books", this.formData).then((res)=>{
        if(res.data.code == 20011){
            this.dialogFormVisible = false;
            this.$message.success("添加成功");
        } else if(res.data.code == 20010){
            this.$message.error("添加失败");
        } else {
            this.$message.error(res.data.msg);
        }
    }).finally(()=>{
        this.getAll();
    });
}
```

**删除操作**:

```JavaScript
handleDelete(row) {
    this.$confirm("此操作永久删除当前数据，是否继续？","提示",{
        type:'info'
    }).then(()=>{
        axios.delete("/books/"+row.id).then((res)=>{
            if(res.data.code == 20021){
                this.$message.success("删除成功");
            } else {
                this.$message.error("删除失败");
            }
        }).finally(()=>{
            this.getAll();
        });
    }).catch(()=>{
        this.$message.info("取消删除操作");
    });
}
```

---

# 拦截器 (Interceptor)

概念：一种动态拦截方法调用的机制。

作用：在指定的方法调用前后执行预先设定的代码，或阻止原始方法的执行。

区别：Filter 属于 Servlet 技术（对所有访问增强），Interceptor 属于 SpringMVC 技术（仅针对 SpringMVC 访问增强）。

## 入门案例

1. 制作拦截器类

实现 HandlerInterceptor 接口。

```Java
@Component
public class ProjectInterceptor implements HandlerInterceptor {
    @Override
    // 原始方法调用前执行，返回true放行，false终止
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        System.out.println("preHandle...");
        return true;
    }

    @Override
    // 原始方法调用后执行
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        System.out.println("postHandle...");
    }

    @Override
    // 原始方法调用完成后执行
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        System.out.println("afterCompletion...");
    }
}
```

2. 配置拦截器

在配置类中重写 addInterceptors 方法。

```Java
@Configuration
@ComponentScan({"com.itheima.controller"})
@EnableWebMvc
public class SpringMvcConfig implements WebMvcConfigurer {
    @Autowired
    private ProjectInterceptor projectInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 配置拦截器及拦截路径
        registry.addInterceptor(projectInterceptor).addPathPatterns("/books", "/books/*");
    }
}
```

## 拦截器链

当配置多个拦截器时，形成拦截器链。

- **PreHandle**：与配置顺序相同，必定运行。
    
- **PostHandle**：与配置顺序相反，可能不运行。
    
- **AfterCompletion**：与配置顺序相反，可能不运行。