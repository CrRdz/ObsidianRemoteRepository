> 该笔记为 SSM 的后置课程

# 基础篇

## 1. SpringBoot 概述

- **定义**：SpringBoot 是 Spring 提供的一个子项目，用于快速构建 Spring 应用程序。
    
- **解决的问题**：传统方式构建 Spring 应用程序存在“导入配置繁琐”和“项目配置繁琐”的问题。
    
- **核心特性**：
    
    - **起步依赖**：本质上是一个 Maven 坐标，整合了完成一个功能需要的所有坐标。
        
    - **自动配置**：遵循“约定大于配置”的原则。在 boot 程序启动后，一些 bean 对象会自动注入到 IOC 容器，不需要手动声明，简化开发。
        
    - **其他特性**：内嵌 Tomcat/Jetty（无需部署 WAR 文件）、外部化配置、不需要 XML 配置（properties/yaml）。
        

## 2. SpringBoot 入门

**需求**：使用 SpringBoot 开发一个 Web 应用，浏览器发起 `/hello` 请求后，给浏览器返回 "hello world" 字符串。

**步骤**：

1. 创建 Maven 工程
    
2. 导入 `spring-boot-starter-web` 起步依赖
    
3. 编写 Controller
    

```Java
@RestController
public class HelloController {

    @RequestMapping("/hello")
    public String hello(){
        return "hello world";
    }
}
```

4. 提供启动类
    

```Java
@SpringBootApplication
public class SpringbootQuickstartApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringbootQuickstartApplication.class, args);
    }
}
```

## 3. 配置文件

SpringBoot 提供了多种属性配置方式：

- `application.properties`
    
- `application.yml` / `application.yaml`（层次清晰，配置简单，推荐）
    

### YAML 配置信息书写与获取

- **规则**：值前边必须有空格作为分隔符；使用空格作为缩进标识层级关系；相同的层级左侧对齐。
    
```YAML
# 发件人相关的信息
email:
  user: 593140521@qq.com
  code: jfejwezhcrzcbbbb
  host: smtp.qq.com
  auth: true
```

### 获取配置信息

1. **使用 `@Value` 注解**：
    
    ```    Java
    @Value("${email.user}")
    private String emailUser;
    ```
    
2. 使用 @ConfigurationProperties：
    
    指定前缀，前缀与配置文件中的保持一致。
    
    ```    Java
    @ConfigurationProperties(prefix = "email")
    public class EmailProperties {
        // 属性名与配置文件 key 一致
        private String user;
        // ... getters and setters
    }
    ```
    

## 4. SpringBoot 整合 MyBatis

### 引入依赖

```XML
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
</dependency>

<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>3.0.0</version>
</dependency>
```

### 配置 YAML 文件

```YAML
spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/mybatis
    username: root
    password: 1234
```

## 5. Bean 管理

### Bean 扫描

- **传统 XML**：`<context:component-scan base-package="com.itheima"/>`
    
- **注解方式**：`@ComponentScan(basePackages = "com.itheima")`
    
- **SpringBoot 默认**：`@SpringBootApplication` 是一个组合注解，其中包含了 `@ComponentScan`。如果不指定扫描路径，**默认扫描启动类所在的包及其子包**。
    

### Bean 注册（第三方 Bean）

|**注解**|**说明**|**位置**|
|---|---|---|
|`@Component`|声明 bean 的基础注解|不属于以下三类时使用|
|`@Controller`|`@Component` 的衍生注解|标注在控制器类上|
|`@Service`|`@Component` 的衍生注解|标注在业务类上|
|`@Repository`|`@Component` 的衍生注解|标注在数据访问类上|

如果要注册的 Bean 对象来自于第三方（不是自定义的，无法加 `@Component`），可以使用以下方式：

**方式 1：@Bean (不推荐在启动类中写)**

```Java
@SpringBootApplication
public class SpringbootRegisterApplication {

    public static void main(String[] args) {
       // ...
    }

    @Bean // 将方法返回值交给 IOC 容器管理
    public Resolver resolver(){
          return new Resolver();
    }
}
```

方式 2：@Import (推荐)

@Import 注解可以把第三方类直接注册到 Spring 容器里。


```Java
@Configuration
@Import(CommonConfig.class) // 导入配置类或第三方类
public class WebConfig {
}
```

### 注册条件 (@Conditional)

SpringBoot 提供了根据条件决定 Bean 是否生效的注解。

|**注解**|**说明**|
|---|---|
|`@ConditionalOnProperty`|配置文件中存在对应的属性，才声明 bean|
|`@ConditionalOnMissingBean`|当不存在当前类型的 bean 时，才声明该 bean|
|`@ConditionalOnClass`|当前环境存在指定的这个类时，才声明该 bean|

**示例代码**：

```Java
// 1. 如果配置文件中配置了指定的信息则注入
@Bean
@ConditionalOnProperty(prefix = "country", name = {"name", "system"})
public Country country(@Value("${country.name}") String name, @Value("${country.system}") String system){
    Country country = new Country();
    country.setName(name);
    country.setSystem(system);
    return country;
}

// 2. 如果 IOC 容器中不存在 Country，则注入 Province
@Bean
@ConditionalOnMissingBean(Country.class)
public Province province(){
    return new Province();
}

// 3. 如果当前环境中存在 DispatcherServlet 类（例如引入了 web 起步依赖），则注入
@Bean
@ConditionalOnClass(name = "org.springframework.web.servlet.DispatcherServlet")
public Province provinceWithWeb(){
    return new Province();
}
```

## 6. 自动配置原理

**核心原理**：遵循约定大于配置，启动后起步依赖中的 Bean 会自动注入。

### 源码解析

1. @SpringBootApplication
    
    这是一个组合注解，包含：
    
    - `@SpringBootConfiguration`（即 `@Configuration`）
        
    - `@ComponentScan`
        
    - `@EnableAutoConfiguration`（核心！）
        
2. @EnableAutoConfiguration
    
    内部使用 @Import(AutoConfigurationImportSelector.class)。
    
    调用 AutoConfigurationImportSelector 的 selectImports(...) 方法。
    
3. 加载配置类
    
    selectImports 方法会去读取 META-INF/spring.factories (旧版) 或 META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports (新版) 文件。
    
    这些文件中列出了所有自动配置类（xxxAutoConfiguration），例如 DispatcherServletAutoConfiguration。
    
4. 按需装配
    
    自动配置类中大量使用了 @ConditionalOnClass、@ConditionalOnMissingBean 等注解。
    
    结论：Spring Boot 启动时加载所有自动配置类，但只有满足条件（如引入了对应依赖）的配置类才会生效并注册 Bean。
    

### 自定义 Starter 示例

```Java
@AutoConfiguration // 表示当前类是一个自动配置类
public class MyBatisAutoConfig {

    // 注入 SqlSessionFactoryBean
    @Bean
    public SqlSessionFactoryBean sqlSessionFactoryBean(DataSource dataSource){
        SqlSessionFactoryBean sqlSessionFactoryBean = new SqlSessionFactoryBean();
        sqlSessionFactoryBean.setDataSource(dataSource);
        return sqlSessionFactoryBean;
    }

    // 注入 MapperScannerConfigurer
    @Bean
    public MapperScannerConfigurer mapperScannerConfigurer(BeanFactory beanFactory){
        MapperScannerConfigurer mapperScannerConfigurer = new MapperScannerConfigurer();
        // 扫描的包: 启动类所在的包及其子包
        List<String> packages = AutoConfigurationPackages.get(beanFactory);
        String p = packages.get(0);
        mapperScannerConfigurer.setBasePackage(p);

        // 扫描的注解
        mapperScannerConfigurer.setAnnotationClass(Mapper.class);
        return mapperScannerConfigurer;
    }
}
```

---

# 实战-后端篇

^cc174a

## 1. 环境搭建

- 执行 `big_event.sql` 脚本。
    
- 创建包结构：`controller`, `mapper`, `pojo`, `service`, `service.impl`, `utils`。
    

## 2. 用户类接口

### 2.1 注册接口

**Controller**:

```Java
@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public Result register(String username, String password){
        // 1.查询用户
        User u = userService.findByUsername(username);
        if (u == null) {
            // 2.没有用户，注册用户
            userService.register(username, password);
            return Result.success("注册成功");
        } else {
            // 3.有用户，返回用户已存在
            return Result.error("用户已被占用");
        }
    }
}
```

**Service**:

```Java
public interface UserService {
    User findByUsername(String username);
    void register(String username, String password);
}
```

**ServiceImpl**:

```Java
@Service
public class UserServiceImpl implements UserService {
    @Autowired
    private UserMapper userMapper;

    @Override
    public User findByUsername(String username) {
        return userMapper.findByUsername(username);
    }

    @Override
    public void register(String username, String password) {
        // 加密
        String md5String = Md5Util.getMD5String(password);
        // 调用mapper层添加
        userMapper.add(username, md5String);
    }
}
```

**Mapper**:

```Java
@Mapper
public interface UserMapper {
    @Select("select * from user where username = #{username}")
    User findByUsername(String username);

    @Insert("insert into user(username,password,create_time,update_time) values(#{username},#{password},now(),now())")
    void add(String username, String password);
}
```

### 2.2 注册参数校验 (Spring Validation)

使用 `spring-boot-starter-validation` 进行参数校验，避免繁琐的 `if` 判断。

**步骤**：

1. 引入依赖。
    
2. 在 Controller 参数前添加 `@Pattern` 等注解。
    
3. 在 Controller 类上添加 `@Validated` 注解。
    
4. 在全局异常处理器中捕获异常。
    
```Java
// Controller
@PostMapping("/register")
public Result register(@Pattern(regexp = "^\\S{5,16}$") String username, 
                       @Pattern(regexp = "^\\S{5,16}$") String password) {
    // 业务逻辑...
}

// 全局异常处理
@RestControllerAdvice
public class GlobalExpectionHandler {
    @ExceptionHandler(Exception.class)
    public Result handleException(Exception e) {
        e.printStackTrace();
        return Result.error(StringUtils.hasLength(e.getMessage()) ? e.getMessage() : "操作失败");
    }
}
```

### 2.3 登录接口与 JWT 验证

**Controller**:

```Java
@PostMapping("/login")
public Result<String> login(@Pattern(regexp = "^\\S{5,16}$") String username, 
                            @Pattern(regexp = "^\\S{5,16}$") String password) {
    User loginUser = userService.findByUsername(username);
    if (loginUser == null) {
        return Result.error("用户名错误");
    }
    if (Md5Util.getMD5String(password).equals(loginUser.getPassword())) {
        // 生成 JWT 令牌逻辑...
        return Result.success("jwt token令牌...");
    }
    return Result.error("密码错误");
}
```

**JWT (Json Web Token) 介绍**:

- 组成：Header（头）、Payload（有效载荷）、Signature（签名）。
    
- 生成 JWT：
    
    ```    Java
    String token = JWT.create()
            .withClaim("user", claims) // 添加载荷
            .withExpiresAt(new Date(System.currentTimeMillis() + 1000 * 60 * 60 * 12)) // 过期时间
            .sign(Algorithm.HMAC256("itheima")); // 签名
    ```
    
- 解析 JWT：
    
    ```    Java
    JWTVerifier jwtVerifier = JWT.require(Algorithm.HMAC256("itheima")).build();
    DecodedJWT decodedJWT = jwtVerifier.verify(token);
    Map<String, Claim> claims = decodedJWT.getClaims();
    ```
    

### 2.4 登录拦截器 (Interceptor)

**定义拦截器**:

```Java
@Component
public class LoginInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String token = request.getHeader("Authorization");
        try {
            Map<String, Object> claims = JwtUtil.parseToken(token);
            // 放行
            return true;
        } catch (Exception e) {
            response.setStatus(401);
            return false;
        }
    }
}
```

**注册拦截器**:

```Java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Autowired
    private LoginInterceptor loginInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(loginInterceptor)
                .addPathPatterns("/**")
                .excludePathPatterns("/user/login", "/user/register");
    }
}
```

### 2.5 获取用户详情与 ThreadLocal 优化

**ThreadLocal**:

- 提供线程局部变量，线程安全。
    
- **优化思路**：在拦截器校验 Token 成功后，将用户信息存入 ThreadLocal；Controller 直接从 ThreadLocal 取数据；请求结束后清除。
    

**拦截器修改**:

```Java
// preHandle 中
ThreadLocalUtil.set(claims);

// afterCompletion 中
ThreadLocalUtil.remove();
```

**Controller 获取**:

```Java
@GetMapping("/userInfo")
public Result<User> info() {
    Map<String, Object> map = ThreadLocalUtil.get();
    String username = (String) map.get("username");
    User user = userService.findByUsername(username);
    return Result.success(user);
}
```

**配置驼峰命名映射**:

```YAML
mybatis:
  configuration:
    map-underscore-to-camel-case: true
```

### 2.6 更新用户信息接口

**Controller**:

```Java
@PutMapping("/update")
public Result update(@RequestBody @Validated User user){
    userService.update(user);
    return Result.success();
}
```

**User 实体类验证**:

```Java
@Data
public class User {
    @NotNull
    private Integer id;
    @NotEmpty
    @Pattern(regexp = "^\\S{1,10}$")
    private String nickname;
    @NotEmpty
    @Email
    private String email;
    @JsonIgnore // 响应时不返回密码
    private String password;
    // ...
}
```

### 2.7 更新头像与密码

- **更新头像 (`PATCH`)**:
    
    ```    Java
    @PatchMapping("/updateAvatar")
    public Result updateAvatar(@RequestParam @URL String avatarUrl){
        userService.updateAvatar(avatarUrl);
        return Result.success();
    }
    ```
    
- 更新密码 (PATCH):
    
    需校验原密码是否正确，两次新密码是否一致。
    

## 3. 文章分类接口

### 3.1 分组校验 (Groups)

当同一个实体类在“新增”和“更新”时有不同的校验规则（例如更新需要 ID，新增不需要），可以使用分组校验。

1. **定义分组接口**:
    
    ```    Java
    public interface Add extends Default {}
    public interface Update extends Default {}
    ```
    
2. **实体类指定分组**:
    
    ```    Java
    @Data
    public class Category {
        @NotNull(groups = {Update.class})
        private Integer id;
    
        @NotEmpty(groups = {Add.class, Update.class})
        private String categoryName;
    }
    ```
    
3. **Controller 使用**:
    
    ```    Java
    @PostMapping
    public Result add(@RequestBody @Validated(Category.Add.class) Category category) { ... }
    
    @PutMapping
    public Result update(@RequestBody @Validated(Category.Update.class) Category category) { ... }
    ```
    

## 4. 文章管理类接口

### 4.1 自定义校验注解

当已有注解不能满足需求（如 `state` 只能是“已发布”或“草稿”），需要自定义。

1. **定义注解 `@State`**:
    
    ```    Java
    @Documented
    @Constraint(validatedBy = { StateValidation.class }) // 指定校验器
    @Target({FIELD})
    @Retention(RUNTIME)
    public @interface State {
        String message() default "state参数的值只能是已发布或者草稿";
        Class<?>[] groups() default {};
        Class<? extends Payload>[] payload() default {};
    }
    ```
    
2. **实现校验器 `StateValidation`**:
    
    ```    Java
    public class StateValidation implements ConstraintValidator<State, String> {
        @Override
        public boolean isValid(String value, ConstraintValidatorContext context) {
            if (value == null) return false;
            return value.equals("已发布") || value.equals("草稿");
        }
    }
    ```
    

### 4.2 文章列表（条件分页）

使用 **PageHelper** 插件。

**Controller**:

```Java
@GetMapping
public Result<PageBean<Article>> list(Integer pageNum, Integer pageSize,
                                      @RequestParam(required = false) Integer categoryId,
                                      @RequestParam(required = false) String state) {
    PageBean<Article> pb = articleService.list(pageNum, pageSize, categoryId, state);
    return Result.success(pb);
}
```

**Service**:


```Java
public PageBean<Article> list(Integer pageNum, Integer pageSize, Integer categoryId, String state) {
    PageBean<Article> pb = new PageBean<>();
    PageHelper.startPage(pageNum, pageSize); // 开启分页

    Map<String, Object> map = ThreadLocalUtil.get();
    Integer userId = (Integer) map.get("id");
    List<Article> as = articleMapper.list(userId, categoryId, state);

    Page<Article> p = (Page<Article>) as; // 强转获取总条数
    pb.setTotal(p.getTotal());
    pb.setItems(p.getResult());
    return pb;
}
```

**Mapper XML (动态 SQL)**:

```XML
<select id="list" resultType="com.itheima.pojo.Article">
    select * from article
    <where>
        <if test="categoryId != null">
            category_id = #{categoryId}
        </if>
        <if test="state != null">
            and state = #{state}
        </if>
        and create_user = #{userId}
    </where>
</select>
```

## 5. 文件上传接口

### 5.1 本地存储

缺点：无法直接通过网络访问，受制于磁盘空间。

```Java
file.transferTo(new File("F:\\Leaning_Java\\files\\" + filename));
```

### 5.2 阿里云 OSS (对象存储)

1. **引入 SDK**:
    
    ```    XML
    <dependency>
        <groupId>com.aliyun.oss</groupId>
        <artifactId>aliyun-sdk-oss</artifactId>
        <version>3.17.4</version>
    </dependency>
    ```
    
2. 工具类 AliOssUtil:
    
    使用 OSSClientBuilder 创建实例，调用 putObject 上传文件，最后拼接返回 URL。
    

## 6. Redis 优化登录

问题：JWT 修改密码后，旧令牌未失效。

方案：登录成功将 Token 存入 Redis；拦截器验证时对比 Redis 中的 Token；修改密码后删除 Redis 中的 Token。

1. **引入依赖**: `spring-boot-starter-data-redis`
    
2. **拦截器逻辑更新**:
    
    ```    Java
    @Autowired
    private StringRedisTemplate stringRedisTemplate;
    
    @Override
    public boolean preHandle(...) {
        String token = request.getHeader("Authorization");
        String redisToken = stringRedisTemplate.opsForValue().get(token);
        if (redisToken == null) {
            throw new RuntimeException("Token已失效");
        }
        // ... 继续后续逻辑
    }
    ```
    

---

# 部署与高级配置

## 1. SpringBoot 项目部署

- **打包**：使用 Maven 的 `package` 命令生成 Jar 包。
    
- **运行**：`java -jar xxx.jar` (服务器需安装 JRE)。
    

## 2. 属性配置优先级

优先级从低到高：

1. 项目中的 `application.yml`
    
2. Jar 包同级目录下的 `application.yml`
    
3. 操作系统环境变量
    
4. 命令行参数 (`--server.port=9000`)
    

## 3. 多环境开发 (Profiles)

用于隔离不同环境（开发、测试、生产）的配置。

**激活方式**:

```YAML
spring:
  profiles:
    active: dev
```

**分组配置**:

```YAML
spring:
  profiles:
    group:
      "dev": devServer, devDB, devSelf
    active: dev
```