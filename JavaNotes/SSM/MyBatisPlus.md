# 1. MyBatisPlus 简介

- **定义**：MyBatisPlus (MP) 是基于 MyBatis 框架基础上开发的增强型工具，旨在简化开发，提高效率。
    
- **开发方式**：
    
    - 基于 MyBatis 使用 MyBatisPlus
        
    - 基于 Spring 使用 MyBatisPlus
        
    - 基于 SpringBoot 使用 MyBatisPlus
        

## 1.1 SpringBoot 整合 MyBatisPlus 快速入门

**开发过程：**

1. 创建 SpringBoot 工程
    
2. 勾选配置使用的技术 (MyBatis, MySQL Driver 等)
    
3. 设置 dataSource 相关属性 (JDBC 参数)
    
4. 定义数据层接口映射配置
    

### 1.1.1 引入依赖

由于 MP 并未被收录到 IDEA 的系统内置配置，需手动添加 MP 起步依赖。

```XML
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-boot-starter</artifactId>
    <version>3.4.1</version>
</dependency>
```

### 1.1.2 配置 JDBC 参数 (application.yml)

```YAML
spring:
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/mybatisplus_db?serverTimezone=UTC
    username: root
    password: root
```

### 1.1.3 制作实体类与 Mapper

定义数据接口，继承 `BaseMapper<T>` 即可获得通用 CRUD 能力。

```Java
@Mapper
public interface UserDao extends BaseMapper<User> {
}
```

## 1.2 MyBatisPlus 特性

- **无侵入**：只做增强不做改变，不会对现有工程产生影响。
    
- **强大的 CRUD 操作**：内置通用 Mapper，少量配置即可实现单表 CRUD 操作。
    
- **支持 Lambda**：编写查询条件无需担心字段写错。
    
- **支持主键自动生成**。
    
- **内置分页插件**。
    

---

# 2. 标准数据层开发

## 2.1 标准数据层 CRUD 功能对照

|**功能**|**自定义接口**|**MP 接口**|
|---|---|---|
|**新增**|`boolean save(T t)`|`int insert(T t)`|
|**删除**|`boolean delete(int id)`|`int deleteById(Serializable id)`|
|**修改**|`boolean update(T t)`|`int updateById(T t)`|
|**根据ID查询**|`T getById(int id)`|`T selectById(Serializable id)`|
|**查询全部**|`List<T> getAll()`|`List<T> selectList(Wrapper queryWrapper)`|
|**分页查询**|`PageInfo<T> getAll(int page, int size)`|`IPage<T> selectPage(IPage<T> page, Wrapper<T> queryWrapper)`|

## 2.2 快速开发实体类 (Lombok)

### 引入依赖

```XML
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.18.12</version>
</dependency>
```

### 实体类示例

使用 `@Data` 注解可替代 Getter/Setter/ToString 等方法。

```Java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    private Long id;
    private String name;
    private String password;
    private Integer age;
    private String tel;
}
```

## 2.3 分页查询

### 2.3.1 配置分页拦截器

配置 MP 拦截器作为 Spring 管理的 bean。

```Java
@Configuration
public class MpConfig {
    @Bean
    public MybatisPlusInterceptor mpInterceptor(){
        // 1.定义Mp拦截器
        MybatisPlusInterceptor mpInterceptor = new MybatisPlusInterceptor();
        // 2.添加具体的拦截器
        mpInterceptor.addInnerInterceptor(new PaginationInnerInterceptor());
        return mpInterceptor;
    }
}
```

### 2.3.2 执行分页查询

```Java
@Test
void testGetByPage(){
    // IPage对象封装了分页操作相关的数据
    IPage page = new Page(2, 3);
    userDao.selectPage(page, null);
    
    System.out.println("当前页码值：" + page.getCurrent());
    System.out.println("每页显示数：" + page.getSize());
    System.out.println("一共多少页：" + page.getPages());
    System.out.println("一共多少条数据：" + page.getTotal());
    System.out.println("数据：" + page.getRecords());
}
```

### 2.3.3 开启 MP 日志

为了查看 SQL 执行情况，可在 YAML 中开启日志输出到控制台。

```YAML
mybatis-plus:
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
```

---

# 3. DQL 查询控制

MyBatisPlus 将复杂的 SQL 查询条件进行了封装，使用编程的形式完成查询条件的组合。

## 3.1 条件查询方式

**方式一：QueryWrapper (硬编码字段名)**

```Java
QueryWrapper qw = new QueryWrapper();
qw.lt("age", 18);
List<User> userList = userDao.selectList(qw);
System.out.println(userList);
```

**方式二：QueryWrapper Lambda 格式**

```Java
QueryWrapper<User> qw = new QueryWrapper<User>();
qw.lambda().lt(User::getAge, 10);
List<User> userList = userDao.selectList(qw);
System.out.println(userList);
```

**方式三：LambdaQueryWrapper (推荐)**

```Java
LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
lqw.lt(User::getAge, 10);
List<User> userList = userDao.selectList(lqw);
System.out.println(userList);
```

## 3.2 链式编程与逻辑查询

```Java
LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
// 并且关系：10到30岁之间 (默认为 AND)
// lqw.lt(User::getAge, 30).gt(User::getAge, 10);

// 或者关系：小于10岁或者大于30岁
lqw.lt(User::getAge, 10).or().gt(User::getAge, 30);
List<User> userList = userDao.selectList(lqw);
```

## 3.3 Null 值处理

在查询条件中动态判断参数是否为空，避免繁琐的 `if` 判断。

```Java
LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
// 语法：condition(boolean), column, value
// 先判定第一个参数是否为true，如果为true连接当前条件
lqw.lt(null != uq.getAge2(), User::getAge, uq.getAge2());
lqw.gt(null != uq.getAge(), User::getAge, uq.getAge());

List<User> userList = userDao.selectList(lqw);
```

## 3.4 查询投影 (Select)

**只查询部分字段：**

```Java
LambdaQueryWrapper<User> lqw = new LambdaQueryWrapper<User>();
lqw.select(User::getId, User::getName, User::getAge);
List<User> userList = userDao.selectList(lqw);
```

**查询模型中未定义的属性 (如聚合函数)：**

```Java
QueryWrapper<User> lqw = new QueryWrapper<User>();
lqw.select("count(*) as count, tel");
lqw.groupBy("tel");
List<Map<String, Object>> userList = userDao.selectMaps(lqw);
```

## 3.5 常用查询条件设定

- **精确查询 (eq)**：
    
    ```    Java
    lqw.eq(User::getName, "Jerry").eq(User::getPassword, "jerry");
    User loginUser = userDao.selectOne(lqw);
    ```
    
- **范围查询 (between)**：
    
    ```    Java
    // 范围查询 lt le gt ge eq between
    lqw.between(User::getAge, 10, 30); // 前面小值后面大值
    ```
    
- **模糊匹配 (like)**：
    
    ```    Java
    // likeLeft: %J, likeRight: J%, like: %J%
    lqw.likeLeft(User::getName, "J");
    ```
    

## 3.6 字段映射与表名映射注解

当数据库设计与 Java 实体类设计不一致时使用。

1. **表字段与属性名不同步**：
    
    - `@TableField(value = "pwd")`：设置当前属性对应数据库中的 `pwd` 字段。
        
2. **编码中添加了数据库未定义的属性**：
    
    - `@TableField(exist = false)`：设置该属性不参与数据库操作。
        
3. **敏感字段不参与查询**：
    
    - `@TableField(select = false)`：默认不查询该字段（如密码）。
        
4. **表名与类名不同步**：
    
    - `@TableName("tbl_user")`：设置当前类对应的数据库表名。
        

---

# 4. DML 操作控制 (增删改)

## 4.1 ID 生成策略控制 (`@TableId`)

位置：模型类中主键属性定义上方。

作用：设置主键生成策略。

**常见策略 (`IdType`)：**

- `AUTO (0)`：使用数据库 ID 自增策略。
    
- `NONE (1)`：不设置策略。
    
- `INPUT (2)`：用户手工输入。
    
- `ASSIGN_ID (3)`：**雪花算法**生成 ID (兼容数值与字符串，默认策略)。
    
- `ASSIGN_UUID (4)`：以 UUID 生成。
    

**全局配置 (application.yml)：**

YAML

```
mybatis-plus:
  global-config:
    db-config:
      id-type: assign_id
      table-prefix: tbl_  # 设置表名前缀，实体类 User 自动映射 tbl_user
```

## 4.2 多记录操作 (批量)

```Java
// 删除指定多条数据
List<Long> list = new ArrayList<>();
list.add(1402551342481838081L);
list.add(1402553134049501186L);
userDao.deleteBatchIds(list);

// 查询指定多条数据
List<Long> qList = new ArrayList<>();
qList.add(1L);
qList.add(3L);
userDao.selectBatchIds(qList);
```

## 4.3 逻辑删除

**概念**：数据不真正删除，而是将状态字段修改为“不可用”，以保留历史数据。

**实现步骤：**

1. **实体类注解**：
    
    
    ```    Java
    // 逻辑删除字段，标记当前记录是否被删除
    @TableLogic(value = "0", delval = "1")
    private Integer deleted;
    ```
    
1. **全局配置 (推荐)**：
    
    ```    YAML
    mybatis-plus:
      global-config:
        db-config:
          logic-delete-field: deleted       # 逻辑删除字段名
          logic-not-delete-value: 0         # 未删除字面值
          logic-delete-value: 1             # 删除字面值
    ```
    

**效果**：执行 `delete` 操作时，底层 SQL 变为 `UPDATE tbl_user SET deleted=1 WHERE id=?`；执行 `select` 时自动带上 `WHERE deleted=0`。

## 4.4 乐观锁

**场景**：解决并发修改问题（如秒杀），防止旧数据覆盖新数据。

**实现步骤：**

1. **实体类添加 Version 字段**：
    
    ```    Java
    @Version
    private Integer version;
    ```
    
2. **配置拦截器**：
    
    ```    Java
    // 在 MpConfig 中添加
    mpInterceptor.addInnerInterceptor(new OptimisticLockerInnerInterceptor());
    ```
    
1. **测试流程**：
    
    ```    Java
    @Test
    void testUpdate(){
        // 1. 必须先查询出数据（获取当前 version）
        User user = userDao.selectById(3L); // version=3
    
        // 2. 修改数据
        user.setName("Jock bbb");
    
        // 3. 执行更新
        // SQL: UPDATE user SET name=?, version=4 WHERE id=3 AND version=3
        userDao.updateById(user); 
    }
    ```
    

---

# 5. 快速开发：代码生成器 (Generator)

## 5.1 引入依赖

```XML
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-generator</artifactId>
    <version>3.4.1</version>
</dependency>

<dependency>
    <groupId>org.apache.velocity</groupId>
    <artifactId>velocity-engine-core</artifactId>
    <version>2.3</version>
</dependency>
```

## 5.2 Generator 配置类

```Java
public class CodeGenerator {
    public static void main(String[] args) {
        // 1. 获取代码生成器的对象
        AutoGenerator autoGenerator = new AutoGenerator();

        // 2. 设置数据库相关配置
        DataSourceConfig dataSource = new DataSourceConfig();
        dataSource.setDriverName("com.mysql.cj.jdbc.Driver");
        dataSource.setUrl("jdbc:mysql://localhost:3306/mybatisplus_db?serverTimezone=UTC");
        dataSource.setUsername("root");
        dataSource.setPassword("root");
        autoGenerator.setDataSource(dataSource);

        // 3. 设置全局配置
        GlobalConfig globalConfig = new GlobalConfig();
        // 设置代码生成位置
        globalConfig.setOutputDir(System.getProperty("user.dir") + "/mybatisplus_04_generator/src/main/java");
        globalConfig.setOpen(false);                // 生成后是否打开目录
        globalConfig.setAuthor("黑马程序员");         // 设置作者
        globalConfig.setFileOverride(true);         // 是否覆盖原始文件
        globalConfig.setMapperName("%sDao");        // 数据层接口名后缀 (UserDao)
        globalConfig.setIdType(IdType.ASSIGN_ID);   // Id生成策略
        autoGenerator.setGlobalConfig(globalConfig);

        // 4. 设置包名配置
        PackageConfig packageInfo = new PackageConfig();
        packageInfo.setParent("com.aaa");           // 父包名
        packageInfo.setEntity("domain");            // 实体类包名
        packageInfo.setMapper("dao");               // 数据层包名
        autoGenerator.setPackageInfo(packageInfo);

        // 5. 策略设置
        StrategyConfig strategyConfig = new StrategyConfig();
        strategyConfig.setInclude("tbl_user");              // 参与生成的表名
        strategyConfig.setTablePrefix("tbl_");              // 去除表前缀 (tbl_user -> User)
        strategyConfig.setRestControllerStyle(true);        // 启用 Rest 风格
        strategyConfig.setVersionFieldName("version");      // 乐观锁字段
        strategyConfig.setLogicDeleteFieldName("deleted");  // 逻辑删除字段
        strategyConfig.setEntityLombokModel(true);          // 启用 Lombok
        autoGenerator.setStrategy(strategyConfig);

        // 6. 执行生成
        autoGenerator.execute();
    }
}
```
