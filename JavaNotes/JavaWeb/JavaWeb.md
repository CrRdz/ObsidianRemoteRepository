


# SSM

Spring +SpringMVC +Mybatis

Dao=Mapper

domain=pojo

git clone git@github.com:CrRdz/Learning_SSM.git





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

