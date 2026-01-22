
- Spring 技术是 JavaEE 开发的必备技术，企业开发技术选型命中率 >90%。
    
- 简化开发，框架整合（MyBatis/Struts/Hibernate）。
    
- Spring 发展到今天已经形成一种开发生态圈，Spring 提供若干个项目，每个项目用于完成特定的功能。
# Spring Framework

Spring Framework 是 Spring 生态中最基础的项目，是其他项目的根基。

## 系统架构

架构上层依赖于下层。

- **底层**：Core Container 核心容器（Beans, Core, Context, SpEL）
    
- **中层**：AOP（面向切面编程）、Aspects（AOP 思想实现）
    
- **上层**：
    
    - Data Access/Integration 数据访问/集成（JDBC, ORM, OXM, JMS, Transaction 事务）
        
    - Web 开发（WebSocket, Servlet, Web, Portlet）
        

## 核心概念

**代码书写现状**：耦合度偏高。

> **解决方案**：使用对象时，在程序中不要主动使用 `new` 产生新对象，转换为由外部提供对象。

**数据层实现：**

```Java
public class BookDaoImpl implements BookDao {
    public void save() {
        System.out.println("book dao save ...");
    }
}

public class BookDaoImpl2 implements BookDao {
    public void save() {
        System.out.println("book dao save ...2");
    }
}
```

**业务层实现：**

```Java
public class BookServiceImpl implements BookService {
    private BookDao bookDao = new BookDaoImpl2(); // 问题所在
    public void save() {
        bookDao.save();
    }
}
```

如果数据层出现了一个新的实现类，因为业务层需要创建新的对象（`BookDaoImpl` 改成 `BookDaoImpl2`），那么需要重新编译、重新部署... 如果不显式实例化对象，就可以降低耦合。

- **IoC（Inversion of Control）控制反转**：对象的创建控制权由程序转移到外部的思想。
    
    - 它将对象的创建和依赖关系的管理交给 Spring 框架，而不是在代码中手动创建对象。这种设计思想可以降低代码的耦合度，提高代码的可维护性和可测试性。
        
    - Spring 提供了一个 IoC 容器，用来充当 IoC 思想的外部。
        
    - IoC 容器负责对象的创建、初始化等一系列工作。
        
    - 被 IoC 容器创建或管理的对象在 IoC 容器中统称为 **Bean**。
        
- **DI（Dependency Injection）依赖注入**：
    
    - 在容器中建立 Bean 与 Bean 之间的依赖关系的整个过程（例如 Service 依赖于 Dao，绑定 Service 和 Dao）。
        
- **目标**：充分解耦。
    
    - 使用 IoC 容器管理 Bean（IoC）。
        
    - 在容器中将有依赖关系的 Bean 进行关系绑定（DI）。
        
    - 使用对象时不仅可以直接从 IoC 容器中直接获取，并且获取到的 Bean 已经绑定了所有依赖关系。
        

---

# 核心容器

## IoC 快速入门

1. 管理 Service 与 Dao。
    
2. 通过配置文件的方式将被管理的对象告知 IoC 容器。
    
3. 被管理的对象交给 IoC，通过接口获取到 IoC 容器。
    
4. IoC 容器得到后，通过接口方法中获取 Bean。
    

**准备：导入坐标 (pom.xml)**

XML

```
<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-context</artifactId>
  <version>5.2.10.RELEASE</version>
</dependency>
```

**创建配置文件 (applicationContext.xml)**

XML

```
<bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"/>
<bean id="bookService" class="com.itheima.service.impl.BookServiceImpl"/>
```

**获取 IoC 容器并获取 Bean (App2.java)**

Java

```
public class App2 {
    public static void main(String[] args) {
        // 3.获取IoC容器
        ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
        
        // 4.获取bean（根据bean配置id获取）
        // BookDao bookDao = (BookDao) ctx.getBean("bookDao");
        // bookDao.save();

        BookService bookService = (BookService) ctx.getBean("bookService");
        bookService.save();
    }
}
```

## DI 快速入门

- 基于 IoC 管理 Bean。
    
- Service 中使用 `new` 形式创建的 Dao 对象不保留。
    
- Service 中需要的 Dao 对象通过提供方法进入到 Service 中。
    
- Service 与 Dao 之间的关系用配置文件描述。
    

**BookServiceImpl.java**

Java

```
public class BookServiceImpl implements BookService {
    // 5.删除业务层中使用new的方式创建的dao对象
    private BookDao bookDao;

    public void save() {
        System.out.println("book service save ...");
        bookDao.save();
    }
    
    // 6.提供对应的set方法
    public void setBookDao(BookDao bookDao) {
        this.bookDao = bookDao;
    }
}
```

**applicationContext.xml**

XML

```
<bean id="bookService" class="com.itheima.service.impl.BookServiceImpl">
    <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"/>
    <property name="bookDao" ref="bookDao"/>
</bean>
```

## Bean 配置

### 基础配置

XML

```
<beans>
    <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"/>
</beans>
```

- **id**：Bean 的 id，使用容器可以通过 id 值获取对应的 Bean，在一个容器中 id 值唯一。
    
- **class**：Bean 的类型，即配置的 Bean 的全路径名。
    

### 别名配置

XML

```
<bean id="bookService" name="service service4 bookEbi" class="com.itheima.service.impl.BookServiceImpl">
    <property name="bookDao" ref="bookDao"/>
</bean>
```

_建议使用 id 引用。_

### Bean 作用范围

XML

```
<bean id="bookDao" name="dao" class="com.itheima.dao.impl.BookDaoImpl" scope="prototype"/>
```

- **singleton**：单例（默认）。
    
- **prototype**：非单例。
    
- **为什么默认单例？** 因为希望对象是可以复用的。
    
    - **适合交给容器管理的 Bean**：表现层对象、业务层对象、数据层对象、工具对象。
        
    - **不适合交给容器管理的 Bean**：封装实体的域对象。
        

## Bean 实例化

Bean 本质上就是对象，创建 Bean 使用构造方法完成。

### 1. 构造方法实例化 (常用)

XML

```
<bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"/>
```

_注意：无参构造方法如果不存在，将抛出 `BeanCreationException`。_

### 2. 静态工厂实例化

**OrderDaoFactory.java**

Java

```
public class OrderDaoFactory {
    public static OrderDao getOrderDao(){
        System.out.println("factory setup....");
        return new OrderDaoImpl();
    }
}
```

**配置**

XML

```
<bean id="orderDao" class="com.itheima.factory.OrderDaoFactory" factory-method="getOrderDao"/>
```

### 3. 实例工厂实例化

**UserDaoFactory.java**

Java

```
public class UserDaoFactory {
    public UserDao getUserDao(){
        return new UserDaoImpl();
    }
}
```

**配置**

XML

```
<bean id="userFactory" class="com.itheima.factory.UserDaoFactory"/>
<bean id="userDao" factory-method="getUserDao" factory-bean="userFactory"/>
```

### 4. 使用 FactoryBean (方式3的变种，实用)

Java

```
public class UserDaoFactoryBean implements FactoryBean<UserDao> {
    // 代替原始实例工厂中创建对象的方法
    public UserDao getObject() throws Exception {
        return new UserDaoImpl();
    }

    public Class<?> getObjectType() {
        return UserDao.class;
    }
    
    // 可以控制单例/非单例
    // public boolean isSingleton() { return true; }
}
```

**配置**

XML

```
<bean id="userDao" class="com.itheima.factory.UserDaoFactoryBean"/>
```

## Bean 的生命周期

- **生命周期**：从创建到消亡的完整过程。
    
    1. **初始化容器**：创建对象（内存分配） -> 执行构造方法 -> 执行属性注入（set 操作） -> 执行 Bean 初始化方法。
        
    2. **使用 Bean**：执行业务操作。
        
    3. **关闭/销毁容器**：执行 Bean 销毁方法。
        

### 方式一：配置文件控制

XML

```
<bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl" init-method="init" destroy-method="destroy"/>
```

**关闭容器：**

Java

```
ClassPathXmlApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
// ... 业务操作
// 注册关闭钩子函数，在虚拟机退出之前回调此函数，关闭容器
// ctx.registerShutdownHook(); 
// 或者直接关闭
ctx.close();
```

### 方式二：接口控制 (推荐)

实现 `InitializingBean`, `DisposableBean` 接口。

Java

```
public class BookServiceImpl implements BookService, InitializingBean, DisposableBean {
    public void destroy() throws Exception {
        System.out.println("service destroy");
    }

    public void afterPropertiesSet() throws Exception {
        System.out.println("service init");
    }
}
```

## 依赖注入方式 (DI)

### 1. Setter 注入

**引用类型：**

Java

```
public class BookServiceImpl implements BookService{
    private BookDao bookDao;
    public void setBookDao(BookDao bookDao) {
        this.bookDao = bookDao;
    }
}
```

XML

```
<bean id="bookService" class="com.itheima.service.impl.BookServiceImpl">
    <property name="bookDao" ref="bookDao"/>
</bean>
```

**简单类型：**

Java

```
public class BookDaoImpl implements BookDao {
    private int connectionNum;
    public void setConnectionNum(int connectionNum) {
        this.connectionNum = connectionNum;
    }
}
```

XML

```
<bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
    <property name="connectionNum" value="100"/>
</bean>
```

### 2. 构造器注入

**配置方式：**

XML

```
<bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
    <constructor-arg name="connectionNum" value="10"/>
    <constructor-arg name="databaseName" value="mysql"/>
    
    <constructor-arg type="int" value="10"/>
    
    <constructor-arg index="0" value="mysql"/>
</bean>
```

**选择建议**：

- **强制依赖**：使用构造器注入（不注入会导致对象创建失败或 Null）。
    
- **可选依赖**：使用 Setter 注入（灵活性强）。
    
- Spring 倡导使用构造器，但自己开发的模块推荐使用 Setter 注入。
    

### 3. 依赖自动装配

IoC 容器根据 Bean 所依赖的资源在容器中自动查找并注入。

XML

```
<bean id="bookService" class="com.itheima.service.impl.BookServiceImpl" autowire="byType"/>
```

- **byType**：按类型（必须保障容器中相同类型的 Bean 唯一，推荐）。
    
- **byName**：按名称（必须保障容器中具有指定名称的 Bean，耦合高）。
    
- 自动装配优先级低于 Setter 和构造器注入。
    

### 4. 集合注入

支持数组、List、Set、Map、Properties。

XML

```
<bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
    <property name="array">
        <array>
            <value>100</value>
            <value>200</value>
        </array>
    </property>
    <property name="list">
        <list>
            <value>itcast</value>
            <value>itheima</value>
        </list>
    </property>
    <property name="map">
        <map>
            <entry key="country" value="china"/>
            <entry key="province" value="henan"/>
        </map>
    </property>
    <property name="properties">
        <props>
            <prop key="country">china</prop>
            <prop key="province">henan</prop>
        </props>
    </property>
</bean>
```

## 加载 Properties 文件

管理第三方 Bean（如 DruidDataSource）时常需要。

1. 开启 `context` 命名空间。
    
2. 使用 `context:property-placeholder` 加载文件。
    
3. 使用 `${}` 占位符读取。
    

XML

```
<context:property-placeholder location="classpath*:*.properties" system-properties-mode="NEVER"/>

<bean class="com.alibaba.druid.pool.DruidDataSource">
    <property name="driverClassName" value="${jdbc.driver}"/>
    <property name="url" value="${jdbc.url}"/>
    <property name="username" value="${jdbc.username}"/>
    <property name="password" value="${jdbc.password}"/>
</bean>
```

## 容器补充

**容器类层次结构**：

- **BeanFactory**：IoC 的顶层接口，延迟加载 Bean（懒汉）。
    
- **ApplicationContext**：Spring 容器的核心接口，立即加载 Bean（饿汉）。
    
    - `ClassPathXmlApplicationContext`：类路径加载。
        
    - `FileSystemXmlApplicationContext`：文件系统路径加载。
        

---

# 注解开发

## 定义 Bean

使用 `@Component` 及其衍生注解替代 XML 中的 `<bean>`。

- `@Component`：通用。
    
- `@Controller`：表现层。
    
- `@Service`：业务层。
    
- `@Repository`：数据层。
    

Java

```
@Service
public class BookServiceImpl implements BookService {
    // ...
}
```

在 XML 中配置扫描：

XML

```
<context:component-scan base-package="com.itheima"/>
```

## 纯注解开发

使用 Java 类替代 XML 配置文件。

Java

```
@Configuration
@ComponentScan({"com.itheima.service","com.itheima.dao"})
public class SpringConfig {
}
```

**加载方式：**

Java

```
ApplicationContext ctx = new AnnotationConfigApplicationContext(SpringConfig.class);
```

## Bean 管理

- **作用范围**：`@Scope("singleton")` 或 `@Scope("prototype")`。
    
- **生命周期**：`@PostConstruct` (初始化), `@PreDestroy` (销毁)。
    

## 依赖注入

- **自动装配 (引用类型)**：`@Autowired`。
    
    - 默认按类型装配。
        
    - 如果需要按名称，配合 `@Qualifier("beanName")` 使用。
        
- **简单类型**：`@Value("${name}")`。
    
- **加载 Properties**：`@PropertySource({"jdbc.properties"})`。
    

## 第三方 Bean 管理

使用 `@Bean` 注解在配置类中定义。

Java

```
public class JdbcConfig {
    @Value("${jdbc.driver}")
    private String driver;
    // ... 其他属性

    @Bean
    public DataSource dataSource(BookDao bookDao){ // 形参自动装配
        DruidDataSource ds = new DruidDataSource();
        ds.setDriverClassName(driver);
        // ...
        return ds;
    }
}
```

**导入配置：**

Java

```
@Configuration
@ComponentScan("com.itheima")
@Import({JdbcConfig.class}) // 导入其他配置类
public class SpringConfig {
}
```

## XML 配置 vs 注解开发

|**功能**|**XML 配置**|**注解**|
|---|---|---|
|**定义 Bean**|`<bean id="" class=""/>`|`@Component`, `@Controller`, `@Service`, `@Repository`|
|**依赖注入**|Setter 注入, 构造器注入, 自动装配|`@Autowired`, `@Qualifier`, `@Value`|
|**配置第三方 Bean**|`<bean>`, 静态/实例工厂|`@Bean`|
|**作用范围**|`scope` 属性|`@Scope`|
|**生命周期**|`init-method`, `destroy-method`|`@PostConstruct`, `@PreDestroy`|

---

# 整合

## Spring 整合 MyBatis

**核心思路**：管理 `SqlSessionFactory` 和 `MapperScannerConfigurer`。

**依赖坐标**：`spring-jdbc`, `mybatis-spring`。

**MybatisConfig.java**

Java

```
public class MybatisConfig {
    // 定义bean，SqlSessionFactoryBean，用于产生SqlSessionFactory对象
    @Bean
    public SqlSessionFactoryBean sqlSessionFactory(DataSource dataSource){
        SqlSessionFactoryBean ssfb = new SqlSessionFactoryBean();
        ssfb.setTypeAliasesPackage("com.itheima.domain"); // 别名扫描
        ssfb.setDataSource(dataSource);
        return ssfb;
    }
    
    // 定义bean，扫描Dao接口
    @Bean
    public MapperScannerConfigurer mapperScannerConfigurer(){
        MapperScannerConfigurer msc = new MapperScannerConfigurer();
        msc.setBasePackage("com.itheima.dao");
        return msc;
    }
}
```

## Spring 整合 JUnit

Java

```
// 设置类运行器
@RunWith(SpringJUnit4ClassRunner.class)
// 设置Spring环境对应的配置类
@ContextConfiguration(classes = SpringConfig.class)
public class AccountServiceTest {
    @Autowired
    private AccountService accountService;

    @Test
    public void testFindById(){
        System.out.println(accountService.findById(1));
    }
}
```

---

# AOP (面向切面编程)

## 核心概念

- **AOP**：在不惊动原始设计（不修改源代码）的基础上进行功能增强。
    
- **连接点（JoinPoint）**：程序执行过程中的任意位置，Spring AOP 中理解为方法的执行。
    
- **切入点（PointCut）**：匹配连接点的式子。
    
- **通知（Advice）**：在切入点执行的操作（共性功能）。
    
- **切面（Aspect）**：描述通知与切入点的对应关系。
    

## AOP 入门

1. **导入坐标**：`aspectjweaver`。
    
2. **开启注解 AOP**：`@EnableAspectJAutoProxy`。
    
3. **定义切面类**：
    

Java

```
@Component
@Aspect
public class MyAdvice {
    // 定义切入点
    @Pointcut("execution(void com.itheima.dao.BookDao.update())")
    private void pt(){}

    // 绑定通知
    @Before("pt()")
    public void method(){
        System.out.println(System.currentTimeMillis());
    }
}
```

## 切入点表达式

标准格式：`execution(访问修饰符 返回值 包名.类/接口名.方法名(参数) 异常名)`

- **通配符**：
    
    - `*`：单个独立的任意符号。
        
    - `..`：多个连续的任意符号（常用于包名或参数）。
        
    - `+`：匹配子类类型。
        
- **示例**：
    
    - `execution(* com.itheima.*Service.*(..))`：匹配 com.itheima 包下任意以 Service 结尾的接口/类的任意方法。
        

## 通知类型

1. **@Before**：前置通知。
    
2. **@After**：后置通知（无论是否异常都执行）。
    
3. **@Around**：环绕通知（重点）。
    
4. **@AfterReturning**：返回后通知（无异常时）。
    
5. **@AfterThrowing**：抛出异常后通知。
    

**环绕通知示例：**

Java

```
@Around("pt()")
public Object around(ProceedingJoinPoint pjp) throws Throwable {
    System.out.println("around before ...");
    // 调用原始方法
    Object ret = pjp.proceed();
    System.out.println("around after ...");
    return ret;
}
```

## 获取数据

- **获取参数**：`JoinPoint.getArgs()` 或 `ProceedingJoinPoint.getArgs()`。
    
- **获取返回值**：`@AfterReturning(returning = "ret")`。
    
- **获取异常**：`@AfterThrowing(throwing = "t")`。
    

---

# 事务

## Spring 事务简介

- **作用**：在数据层保障一系列数据库操作同成功同失败。
    
- **平台事务管理器**：`PlatformTransactionManager` (接口)，MyBatis 使用 `DataSourceTransactionManager` 实现。
    

## 开启事务

1. **配置事务管理器**：
    

Java

```
@Bean
public PlatformTransactionManager transactionManager(DataSource dataSource){
    DataSourceTransactionManager transactionManager = new DataSourceTransactionManager();
    transactionManager.setDataSource(dataSource);
    return transactionManager;
}
```

2. **开启注解事务驱动**：`@EnableTransactionManagement`。
    
3. **使用注解**：在接口或方法上添加 `@Transactional`。
    

Java

```
public interface AccountService {
    @Transactional
    public void transfer(String out, String in, Double money);
}
```

## 事务属性

|**属性**|**说明**|
|---|---|
|**readOnly**|设置只读事务（true/false）。|
|**timeout**|事务超时时间，-1 为永不超时。|
|**rollbackFor**|设置回滚异常（Class），默认只回滚 RuntimeException 和 Error。|
|**noRollbackFor**|设置不回滚异常。|
|**propagation**|**事务传播行为**（重点）。|

**事务传播行为 (propagation)**：

- `REQUIRED` (默认)：有事务就加入，没有就新建。
    
- `REQUIRES_NEW`：无论有没有，都新建事务（挂起当前事务）。
    
- `SUPPORTS`：有就加入，没有就不使用事务。
    
- `NEVER`：有事务就报错。
    

**案例**：转账过程中无论成功失败，都要记录日志。

- 日志方法需要开启一个新的事务，不受转账事务回滚的影响。
    

Java

```
public interface LogService {
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    void log(String out, String in, Double money);
}
```