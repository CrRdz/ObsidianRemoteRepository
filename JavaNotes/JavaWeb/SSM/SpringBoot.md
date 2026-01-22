# SpringBoot 简介

SpringBoot 是由 Pivotal 团队提供的全新框架，其设计目的是用来简化 Spring 应用的初始搭建以及开发过程。

## 入门案例

**1. 制作 Controller 类**

```Java
@RestController
@RequestMapping("/books")
public class BookController {

    @GetMapping("/{id}")
    public String getById(@PathVariable Integer id){
        System.out.println("id ==> " + id);
        return "hello , spring boot!";
    }
}
```

**2. Application 类**

```Java
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

> **注意**：SpringBoot 内嵌 Tomcat，已经能直接启动。

## SpringBoot 与 Spring 对比

**最简 SpringBoot 程序所包含的基础文件：**

- `pom.xml`
    
- `Application` 类
    

**Spring 程序与 SpringBoot 程序对比**

|**类/配置文件**|**Spring**|**SpringBoot**|
|---|---|---|
|Pom 文件中的坐标|手工制作|勾选添加|
|Web3.0 配置类|手工制作|无|
|Spring/SpringMVC 配置类|手工制作|无|
|控制器|手工制作|手工制作|

> **提示**：基于 IDEA 开发 Spring Boot 程序需要确保联网，且能加载到程序框架结构。

## SpringBoot 项目快速启动

1. 先对 SpringBoot 项目打包（执行 Maven 构建指令 `package`）。
    
2. 找到 `springboot_01_quickstart-0.0.1-SNAPSHOT` 文件，打开对应位置。
    
3. 使用 cmd 打开输入 `java -jar springboot_01_quickstart-0.0.1-SNAPSHOT`。
    

> jar 支持命令行启动，但需要依赖 maven 插件支持：

```XML
<plugins>
    <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
    </plugin>
</plugins>
```

成功快速启动。

## SpringBoot 概述

简化 Spring 应用的初始搭建以及开发过程，核心特性包括：**自动配置**、**起步依赖**、**辅助功能（内置服务器）**。

- **Spring 程序缺点**：配置繁琐，依赖设置繁琐。
    
- **起步依赖**：一次性地写了若干个依赖。
    

**开发 web 程序所需要的起步依赖：**

```XML
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
           <groupId>org.springframework.boot</groupId>
           <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

**Parent**：所有 SpringBoot 项目要继承的项目，定义若干个坐标版本号，以达到减少依赖冲突的目的。

**引导类**：

```Java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

> SpringBoot 的引导类是项目的入口，运行 main 方法就可以启动项目。

**更改 Tomcat 服务器**

需要先排除 Tomcat，更换 Jetty 服务器（更轻量级，可扩展性更强）：

```XML
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
           <groupId>org.springframework.boot</groupId>
           <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jetty</artifactId>
</dependency>
```

---

# 基础配置

## 三种配置文件

1. `application.properties` (例如: `server.port=80`)
    
2. `application.yaml`
    
3. `application.yml`
    

**主写 yml 文件**

> 注：自动提示功能消失解决方案：
> 
> File -> Project Structure -> Facets -> Spring -> 需要配的工程 -> 追加配置文件（yaml/yml）

**加载顺序**： `.properties` > `.yml` > `.yaml`

## YAML

YAML 一种数据序列化格式，容易阅读，容易与脚本语言交互，以数据为核心，重数据轻格式。

### 语法规则

- 大小写敏感。
    
- 属性层级关系使用多行描述，每行结尾使用冒号结束。
    
- 使用缩进表示层级关系，同层级左侧对齐，只允许使用空格。
    
- 属性值前添加空格（属性名与属性值之间使用冒号 + 空格作为风格）。
    
- `#` 表示注释。
    
- 数组数据在数据书写的位置下方使用减号作为数据开始符号，每行书写一个数据，减号与数据间空格分隔。
    

### Yaml 数据读取方式

**Application.yaml 配置：**

```YAML
lesson: SpringBoot

server:
  port: 80

enterprise:
  name: itcast
  age: 16
  tel: 4006184000
  subject:
    - Java
    - 前端
    - 大数据
```

**方式一：使用 @Value 读取单一属性数据**

```Java
@RestController
@RequestMapping("/books")
public class BookController {
    //使用@Value读取单一属性数据
    @Value("${lesson}")
    private String lesson;
    
    @Value("${server.port}")
    private Integer port;
    
    @Value("${enterprise.subject[0]}")
    private String subject_00;

    @GetMapping("/{id}")
    public String getById(@PathVariable Integer id){
        System.out.println(lesson);
        System.out.println(port);
        System.out.println(subject_00);
        return "hello , spring boot!";
    }
}
```

**方式二：使用 Environment 封装全配置数据**

```Java
//使用Environment封装全配置数据
@Autowired
private Environment environment;

// 在方法中调用
System.out.println("--------------------");
System.out.println(environment.getProperty("lesson"));
System.out.println(environment.getProperty("server.port"));
System.out.println("---------------------");
```

**方式三：使用实体封装 yaml 数据**

```Java
//封装yaml对象格式数据必须先声明当前实体类受Spring管控
@Component
//使用@ConfigurationProperties注解定义当前实体类读取配置属性信息，通过prefix属性设置读取哪个数据
@ConfigurationProperties(prefix = "enterprise")
public class Enterprise {
    private String name;
    private Integer age;
    private String tel;
    private String[] subject;
    // ... getters and setters
}
```

使用时自动装配：

```Java
@Autowired
private Enterprise enterprise;

// 调用
System.out.println(enterprise);
```

## 多环境启动

### 配置

**1. 在 application.yaml 中配置**

```YAML
#设置启用的环境
spring:
  profiles:
    active: dev

---
#开发
spring:
  config:
    activate:
      on-profile: dev
server:
  port: 80
---
#生产
spring:
  profiles: pro
server:
  port: 81
---
#测试
spring:
  profiles: test
server:
  port: 82
```

**2. 使用 .properties 配置**

- 主启动配置文件 application.properties:
    
    spring.profiles.active=pro
    
- 环境分类配置文件 application-dev.properties:
    
    server.port=8080
    
- 环境分类配置文件 application-pro.properties:
    
    server.port=8081
    

### 多环境启动命令格式

1. 先 `clean` 再 `package`
    
2. 带参数启动 SpringBoot：
    
    java -jar springboot.jar --spring.profile.active=test
    

### 多环境开发兼容问题

**Maven 中设置多环境属性**

```XML
<profiles>
    <profile>
        <id>dev</id>
        <properties>
            <profile.active>dev</profile.active>
        </properties>
    </profile>
    <profile>
        <id>pro</id>
        <properties>
            <profile.active>pro</profile.active>
        </properties>
        <activation>
            <activeByDefault>true</activeByDefault>
        </activation>
    </profile>
    <profile>
        <id>test</id>
        <properties>
            <profile.active>test</profile.active>
        </properties>
    </profile>
</profiles>
```

**SpringBoot 中应用 Maven 属性**

```YAML
#设置启用的环境
spring:
  profiles:
    active: ${profile.active}
```

> 问题：Maven 执行 package 指令时，类参与编译，但是配置文件并没有编译，而是直接复制到包中。
> 
> 解决：对于源码中非 java 类对的操作要求加载 Maven 对应的属性，解析 ${} 占位符。需要配置 maven 插件：

```XML

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-resources-plugin</artifactId>
    <version>3.2.0</version>
    <configuration>
        <encoding>UTF-8</encoding>
        <useDefaultDelimiters>true</useDefaultDelimiters>
    </configuration>
</plugin>
```

## 配置文件分类

SpringBoot 中 4 级配置文件（优先级从高到低）：

1. `file:config/application.yml` **[最高]** （在文件系统位置中）
    
2. `file:application.yml`
    
3. `classpath:config/application.yml` （在 IDEA classpath 中）
    
4. `classpath:application.yml`
    

- **1级与2级**：留做系统打包后设置通用属性。
    
- **3级与4级**：留做系统开发阶段设置通用属性。
    

---

# 整合第三方技术

## 整合 Junit

**Spring 整合 Junit (旧方式)**

```Java
//设置类运行器
@RunWith(SpringJUnit4ClassRunner.class)
//设置Spring环境对应的配置类
@ContextConfiguration(classes = SpringConfig.class)
public class AccountServiceTest {
    //支持自动装配注入bean
    @Autowired
    private AccountService accountService;

    @Test
    public void testFindById(){
        System.out.println(accountService.findById(1));
    }

    @Test
    public void testFindAll(){
        System.out.println(accountService.findAll());
    }
}
```

**SpringBootTest 整合 (新方式)**

如果测试类在 SpringBoot 启动类的包或子包中，可以省略启动类的设置（即省略 `classes` 设定）：

```Java
@SpringBootTest
class Springboot07TestApplicationTests {

    @Autowired
    private BookService bookService;

    @Test
    public void save() {
        bookService.save();
    }
}
```

如果不放在同一包下，需指定地址：

@SpringBootTest(classes = Springboot07TestApplication.class)

## 整合 MyBatis

**基于 Spring 实现 SSM 整合回顾**

1. SpringConfig
    
2. 导入 JdbcConfig
    
    - 定义数据源（加载 properties 配置项：driver，url，username，password）
        
3. 导入 MyBatisConfig
    
    - 定义 SqlsessionFactoryBean
        
    - 定义映射配置
        

**SpringBoot 整合 MyBatis**

**1. BookDao**

```Java
@Mapper
public interface BookDao {
    @Select("select * from tbl_book where id = #{id}")
    public Book getById(Integer id);
}
```

**2. Application.yml**

```YAML
spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/ssm_db?serverTimezone=UTC
    username: root
    password: root
    type: com.alibaba.druid.pool.DruidDataSource
```

> **注意**：`type` 属性配置数据源。SpringBoot 版本 2.4.3（不含）之前需要配置 `serverTimezone`。

## 案例：基于 SpringBoot 的 SSM 整合案例

1. **pom.xml**：配置起步依赖，必要的资源坐标。
    
2. **Application.yml**：设置数据源，接口等。
    
3. **配置类**：全部删除（SpringBoot 自动配置）。
    
4. **Dao**：设置 `@Mapper`。
    
5. **测试类**：自动生成。
    

**Git 获取案例代码：**


```Bash
git sparse-checkout init --cone
git sparse-checkout set 04-springboot/code/springboot
git clone --filter=blob:none https://github.com/CrRdz/Learning_SSM.git
```