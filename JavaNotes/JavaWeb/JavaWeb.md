
# MyBatis

- MyBitis 一款持久层框架，用于简化JDBC开发
	持久层：负责将数据保存到数据库的那一层代码

- JavaEE三层框架：表现层，业务层，持久层

框架：框架是一个半成品软件，一套可重用，通用，软件基础代码模型 在框架基础之上构建软件编写更加高效，规范，通用，可扩展

- JDBC缺点
	- 硬编码 -配置文件
	- 注册驱动，获取连接
	- SQL语句 操作繁琐 -自动完成
	- 手动设置参数
	- 手动封装结果集

## MyBatis快速入门

查询user表中所有数据

1.  创建user表，添加数据（在navicat中完成）
2.  创建模块，导入坐标
3.  编写Mybatis核心配置文件 --- 替换连接信息 解决硬编码问题

Mybatis-config.xml
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql:///mybatis?useSSL=false"/>
                <property name="username" value="root"/>
                <property name="password" value="1234"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
<!--加载sql映射文件-->
        <mapper resource="UserMapper.xml"/>
    </mappers>
</configuration>
```
 编写SQL映射文件 --- 统一管理sql语句 解决硬编码问题

操作User表就定义UserMapper.xml
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="test">
    <select id="selectAll" resultType="com.itheima.pojo.User">
        select \* from tb_user;
    </select>
/mapper>
```

编码
- 定义pojo类
```java
public class User {
    private Integer id;
    private String username;
    private String password;
    private String gender;
    private String addr;
     @setter
@getter
    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", username='" + username + '\\'' +
                ", password='" + password + '\\'' +
                ", gender='" + gender + '\\'' +
                ", addr='" + addr + '\\'' +
                '}';
    }
}
```
 - 加载核心配置文件，获取SqlSessionFactory对象
 - 获取SqlSession对象，执行SQL语句
 - 释放资源
```java
 public static void main(String\[\] args) throws IOException {
     //1. 加载mybatis的核心配置文件，获取 SqlSessionFactory
     String resource = "mybatis-config.xml";
     InputStream inputStream = Resources.getResourceAsStream(resource);
     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
    //2. 获取SqlSession对象，用它来执行sql
    SqlSession sqlSession = sqlSessionFactory.openSession();
    //3. 执行sql 传入名称空间.唯一标识
    List<User> users = sqlSession.selectList("test.selectAll");
    System.out.println(users);
    //4. 释放资源
    sqlSession.close();
}
```

## Mapper代理开发

1.  定义与SQL映射文件同名的Mapper接口，并将Mapper接口和SQL映射文件放在同一目录, 在resource下创建directory时用分隔符：/来代替”.”

```java
public interface UserMapper {
	List<User> selectAll();
}
```

2.  设置SQL映射文件的namespace属性为Mapper接口全限定名

```xml
<mapper namespace="com.itheima.mapper.UsrMapper">
```

3.  在Mapper接口中定义方法，方法名就是SQL映射文件中sql语句中的id，并保持参数类型和返回值类型一致
4.  编码
- 通过SqlSession的getMapper方法获取Mapper接口的代理对象
- 调用对应方法完成sql的执行

```java
public static void main(String[] args) throws IOException {
    //1. 加载mybatis的核心配置文件，获取 SqlSessionFactory
    String resource = "mybatis-config.xml";
    InputStream inputStream = Resources.getResourceAsStream(resource);
    SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
    //2. 获取SqlSession对象，用它来执行sql
     SqlSession sqlSession = sqlSessionFactory.openSession();
    //3. 执行sql
    //List<User> users = sqlSession.selectList("test.selectAll");
    //System.out.println(users);
    //3.1获取UserMapper接口的代理对象_
    UserMapper userMapper = sqlSession.getMapper(UserMapper.class);
    List<User> users = userMapper.selectAll();
    //4. 释放资源
    sqlSession.close();
}
```

如果Mapper接口和SQL映射文件名称相同，并在同一目录下，则可以使用包扫描的方式简化SQL映射文件的加载

```xml
 <mappers>
 <!--加载sql的映射文件-->
 <!-- <mapper resource="com/itheima/mapper/UserMapper.xml"/>-->
     <package name="com.itheima.mapper"/>
 </mappers>
```

## MyBatis核心配置文件

Mybatis-config.xml配置文件

1.  Environment

配置数据库连接环境信息。可以配置多个environment，通过default属性切换不同的environment
```xml
<environment default="   ">
```

2.  配置别名 可不区分大小写
```xml
<typeAliases>
       <package name ="com.itheima.pojo"/>
</typeAliases>
```

## 配置文件完成增删改查

例：完成品牌数据的增删改操作

### 环境准备

数据库表tb_brand
实体类Brand
测试用例
安装MyBatisX插件 实现XML和接口方法跳转，根据接口方法生成statement

### 查询-所有数据

1.  编写接口方法：Mapper接口 -Mapper-Brandmapper

- 参数：无
- 结果：`List<Brand>`

```java
 public interface BrandMapper {
     /**
      * 查询所有
      */
     List<Brand> selectAll();
 }
```

2.  编写SQL语句：SQL映射文件 -BrandMapper.xml
```xml
  <select id="selectAll" resultType="com.itheima.pojo.Brand"
      select \* from tb_brand;
  </select>
```

3.  执行方法，测试
```java
@Test
public void testSelectAll() throws Exception {
    //1.获取SqlSessionFactory
   String resource = "mybatis-config.xml";
   InputStream inputStream = Resources.getResourceAsStream(resource);
     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
    //2. 获取SqlSession对象
   SqlSession sqlSession = sqlSessionFactory.openSession();
   
   //3.获取Mapper接口的代理对象
    BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);
    
    //4.执行方法
    List<Brand> brands = brandMapper.selectAll();
    System.out.println(brands);
    
    //5.释放资源
    sqlSession.close();
}    
```


4.  执行后问题

部分数据没有成功加载
原因：数据库表的名称字段和实体类的属性名称不一样，则不能自动封装

pojo实体类Brand中Brand字段 与 MySQL中Brand（Brand_name）字段不一样

解决：

1.  起别名：//缺点：每次查询都需要定义一次别名

```sql
select id,brand_name,company_name,ordered,description,status 

from tb_brand;

--使用别名

select 

id,

brand_name as brandN     me,

company_name as companyName,

ordered,

Description,

status 

from tb_brand;
```

2.  Sql片段 -不灵活
```xml
 <sql id="brand_column">
      id,
 brandName as brandName,
 companyName as companyName,
 ordered,
 description,
 status
  </sql>
```

```xml
<select id="selectAll" resultType="com.itheima.pojo.Brand">
    select 
        <include refid="brand_column"/>    
    from tb_brand
</select>
```

3.  resultMap 完成不一致的属性名和列名的映射
```xml
 <!-- id：唯一标识 type 映射的类型 支持别名-->
  <resultMap id="brandResultMap" type="brand">
  <!--
  id:完成主键字段的映射
  result：完成一般字段的映射
  -->
      <result column="brand_name" property="brandName"/>
     <result column="company_name" property="companyName"/>
 </resultMap>
 
<!-- 将resultType 更改成resultMap-->
 <select id="selectAll" resultMap="brandResultMap">
     select 
	 * 
	 from tb_brand
 </select>
```
### 查看详情

1.  编写接口方法：Mapper接口

- 参数：id
- 结果：brand

```xml
  /**
  * 查看详情 根据id查询
  */
  Brand selectById(int id);
```

2.  编写SQL语句：SQL映射文件
	 参数占位符：
	#{}：会将其替换为 ？.为了防止SQL注入
	${}：拼sql，会存在SQL注入问题

	使用时机：参数传递时：#{}
		表名或列名不固定情况下：${} 会存在SQL注入问题
		
	参数类型：
	parameterType:可以省略

1.  特殊字符处理

\* 转义字符

\* CDATA区

<!\[CDATA\[

...(特殊字符)

\]\]>

1.  <select id="selectById" resultMap="brandResultMap">
2.      select
3.          \*
4.      from tb_brand where id = _#{id};_
5.  </select>

6.  执行方法，测试
7.  @Test
8.  public void testSelectById() throws Exception {
9.      _//0.接受参数_
10.      int id = 1;

11.      _//1.获取SqlSessionFactory_
12.      String resource = "mybatis-config.xml";
13.      InputStream inputStream = Resources.getResourceAsStream(resource);
14.     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

15.     _//2. 获取SqlSession对象_
16.     SqlSession sqlSession = sqlSessionFactory.openSession();

17.     _//3.获取Mapper接口的代理对象_
18.     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

19.     _//4.执行方法_
20.     Brand brand = brandMapper.selectById(id);
21.     System.out.println(brand);

22.     _//5.释放资源_
23.     sqlSession.close();

24. }

### 条件查询

- 多条件查询

1.  编写接口方法：Mapper接口

- 参数：所有查询条件
- 结果：List<Brand>

1.  散装参数接收 使用@Param
2.  _/\*\*_
3.   \* 根据条件查询
4.   \* 参数接收
5.   \* 散装参数：如果方法中有多个参数，需要使用@Param("SQL参数占位符名称"）
6.   \* @param status
7.   \* @param companyName
8.   \* @param brandName
9.   \* @return
10.  \*
11.  \*/

12. List<Brand> selectByCondition(@Param("status")int status,@Param("companyName")String companyName,@Param("brandName")String brandName);

13. }
14. 对象参数：对象中的属性名称要和SQL参数占位符名称一致

List<Brand> selectByCondition(Brand brand);

1.  对象参数：对象中的属性名称要和SQL参数占位符名称一致

List<Brand> selectByCondition(Map map);

1.  编写SQL语句：SQL映射文件
2.  _<!--_
3.  条件查询
4.  \-->
5.  <select id="selectByCondition" resultMap="brandResultMap">
6.      select
7.          \*
8.      from tb_brand
9.      where
10.         status = #{status}
11.        and company_name like #{companyName}
12.        and brand_name like #{brandName}
13. </select>

14.  执行方法，测试
15.  @Test
16.      public void testSelectByCondition() throws Exception {
17.          _//0.接受参数_
18.          int status = 1;
19.          String companyName = "华为";
20.          String brandName = "华为";

21.          _//处理参数_
22.         companyName = "%" + companyName + "%";
23.         brandName = "%" + brandName + "%";

24. _//        //封装对象 对应对象参数接收_
25. _//        Brand brand = new Brand();_
26. _//        brand.setStatus(status);_
27. _//        brand.setCompanyName(companyName);_
28. _//        brand.setBrandName(brandName);_

29. _//封装对象 对应map参数接受_
30.         Map map = new HashMap<>();
31.         map.put("status",status);
32.         map.put("companyName",companyName);
33.         map.put("brandName",brandName);

34.         _//1.获取SqlSessionFactory_
35.         String resource = "mybatis-config.xml";
36.         InputStream inputStream = Resources.getResourceAsStream(resource);
37.         SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

38.         _//2. 获取SqlSession对象_
39.         SqlSession sqlSession = sqlSessionFactory.openSession();

40.         _//3.获取Mapper接口的代理对象_
41.         BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

42.         _//4.执行方法_
43. _//        List<Brand> brands = brandMapper.selectByCondition(status, companyName, brandName); //对应散装参数接收_
44. _//        List<Brand> brands = brandMapper.selectByCondition(brand);//对应对象参数接收_
45.         List<Brand> brands = brandMapper.selectByCondition(map);_//对应Map参数接收_
46.         System.out.println(brands);

47.         _//5.释放资源_
48.         sqlSession.close();

49.     }

50.  存在问题

用户输入条件时，是否所有条件都会填写？

优化：动态条件查询

- 多条件-动态条件查询

动态SQL ：SQL语句会随着用户的输入或外部条件的变化而变化

BrandMapper.xml

1.  <select id="selectByCondition" resultMap="brandResultMap">
2.      select
3.          \*
4.      from tb_brand
5.      where
6.          <if test="status != null">
7.              status = _#{status}_
8.          </if>
9.      <if test="companyName != null and companyName != ''">
10.         and company_name like _#{companyName}_
11.     </if>
12.     <if test="brandName != null and brandName != ''">
13.         and brand_name like _#{brandName}_
14.     </if>

15. </select>

test=”条件”条件中使用其真正输入的值而不是属性 即companyName

1.  存在问题

如果第一个条件不存在的话，会多出一个and，MySQL语法错误

优化

1.  每个语句都加and，并且在where后加上1 = 1 恒等式
2.  <select id="selectByCondition" resultMap="brandResultMap">
3.      select
4.          \*
5.      from tb_brand
6.      where 1 = 1
7.          <if test="status != null">
8.          and status = _#{status}_
9.          </if>
10.     <if test="companyName != null and companyName != ''">
11.         and company_name like _#{companyName}_
12.     </if>
13.     <if test="brandName != null and brandName != ''">
14.         and brand_name like _#{brandName}_
15.     </if>

16. </select>

17.  where 标签（较常用）
18.  <select id="selectByCondition" resultMap="brandResultMap">
19.      select
20.          \*
21.      from tb_brand
22.      <where>
23.          <if test="status != null">
24.          and status = _#{status}_
25.          </if>
26.     <if test="companyName != null and companyName != ''">
27.         and company_name like _#{companyName}_
28.     </if>
29.     <if test="brandName != null and brandName != ''">
30.         and brand_name like _#{brandName}_
31.     </if>
32.     </where>

33. </select>

- 单条件-动态条件查询
- 从多个条件中选择一个
- choose（when，otherwise）：选择，类似于Java中的switch语句

1.  编写接口方法：Mapper接口

- 参数：查询条件
- 结果：List<Brand>

List<Brand> selectByConditionSingle(Brand brand);

1.  编写SQL语句：SQL映射文件
2.  </select>
3.  <select id="selectByConditionSingle" resultMap="brandResultMap">
4.      select
5.          \*
6.      from tb_brand
7.      where
8.      <choose>_<!--相当于switch-->_
9.          <when test="status != null">_<!--相当于case-->_
10.             status = #{status}
11.         </when>
12.         <when test="companyName != null and companyName != ''"> _<!--相当于case-->_
13.             company_name like #{companyName}
14.         </when>
15.         <when test="brandName != null and brandName != ''">_<!--相当于case-->_
16.             brand_name like #{brandName}
17.         </when>
18.     </choose>
19. </select>

20.  执行方法，测试
21.      @Test
22.      public void testSelectByConditionSingle() throws Exception {
23.          _//0.接受参数_
24.          int status = 1;
25.          String companyName = "华为";
26.          String brandName = "华为";

27.          _//处理参数_
28.         companyName = "%" + companyName + "%";
29.         brandName = "%" + brandName + "%";

30.         _//封装对象 对应对象参数接收_
31.         Brand brand = new Brand();
32.         brand.setStatus(status);
33.         brand.setCompanyName(companyName);
34.         brand.setBrandName(brandName);

35. _//        Map map = new HashMap<>();_
36. _//        map.put("status",status);_
37. _//        map.put("companyName",companyName);_
38. _//        map.put("brandName",brandName);_

39.         _//1.获取SqlSessionFactory_
40.         String resource = "mybatis-config.xml";
41.         InputStream inputStream = Resources.getResourceAsStream(resource);
42.         SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

43.         _//2. 获取SqlSession对象_
44.         SqlSession sqlSession = sqlSessionFactory.openSession();

45.         _//3.获取Mapper接口的代理对象_
46.         BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

47.         _//4.执行方法_
48.         List<Brand> brands = brandMapper.selectByConditionSingle(brand);
49.         System.out.println(brands);

50.         _//5.释放资源_
51.         sqlSession.close();

52.     }

53.  存在问题

如果用户一个都不选，语法会报错

优化：恒等式

1.  <otherwise>_<!--相当于default-->_
2.     1=1
3.  </otherwise>

### 添加

5.1 添加

1.  编辑接口方法：Mapper接口

- 参数：除了id之外的所有数据
- 结果：void

void add(Brand brand);

1.  编写SQL语句：SQL映射文件
2.  <insert id="add">
3.      insert into tb_brand (brand_name,company_name,ordered,description,status)
4.      values (#{brandName},#{companyName},#{ordered},#{description},#{status});
5.  </insert>

6.  执行方法，测试
7.  @Test
8.  public void add() throws Exception {
9.      _//0.接受参数_
10.      int status = 1;
11.      String companyName = "波导手机";
12.      String brandName = "波导";
13.      String description = "手机中的战斗机";
14.      int ordered = 100;

15.     _//封装对象 对应对象参数接收_
16.     Brand brand = new Brand();
17.     brand.setStatus(status);
18.     brand.setCompanyName(companyName);
19.     brand.setBrandName(brandName);
20.     brand.setDescription(description);
21.     brand.setOrdered(ordered);

22.     _//1.获取SqlSessionFactory_
23.     String resource = "mybatis-config.xml";
24.     InputStream inputStream = Resources.getResourceAsStream(resource);
25.     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

26.     _//2. 获取SqlSession对象_
27.     SqlSession sqlSession = sqlSessionFactory.openSession();

28.     _//3.获取Mapper接口的代理对象_
29.     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

30.     _//4.执行方法_
31.     brandMapper.add(brand);

32. _//提交事务_
33.     sqlSession.commit();

34.     _//5.释放资源_
35.     sqlSession.close();

36. }
37. 优化

需要手动提交事务

可在获取Sqlsession对象时 可以传递布尔值

SqlSession sqlSession = sqlSessionFactory.openSession(true);

则可省略#33行

5.2添加-主键返回

在数据添加成功后，需要插入数据库数据的主键的值

1.  <insert id="add" useGeneratedKeys="true" keyProperty="id">
2.      insert into tb_brand 
3.  (brand_name,company_name,ordered,description,status)
4.      values 
5.  (#{brandName},#{companyName},#{ordered},#{description},#{status});
6.  </insert>

### 修改

6.1 修改全部字段

1.  编写接口方法：Mapper接口

- 参数：所有数据
- 结果：void/受影响的行数

int update (Brand brand);

1.  编写SQL语句：SQL映射文件
2.  <update id="update">
3.      update tb_brand 
4.      set 
5.  brand_name = _#{brandName},_
6.  _company_name = #{companyName},_
7.  _ordered = #{ordered},_
8.  _description = #{description},_
9.  _status = #{status}_ 
10. where _id = #{id};_
11. </update>

12.  执行方法，测试
13.  @Test
14.  public void testUpdate() throws Exception {
15.      _//0.接受参数_
16.      int status = 1;
17.      String companyName = "波导手机";
18.      String brandName = "波导";
19.      String description = "波导手机，手机中的战斗机";
20.      int ordered = 200;
21.     int id = 4;

22.     _//封装对象 对应对象参数接收_
23.     Brand brand = new Brand();
24.     brand.setStatus(status);
25.     brand.setCompanyName(companyName);
26.     brand.setBrandName(brandName);
27.     brand.setDescription(description);
28.     brand.setOrdered(ordered);
29.     brand.setId(id);

30.     _//1.获取SqlSessionFactory_
31.     String resource = "mybatis-config.xml";
32.     InputStream inputStream = Resources.getResourceAsStream(resource);
33.     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

34.     _//2. 获取SqlSession对象_
35.     SqlSession sqlSession = sqlSessionFactory.openSession(true);

36.     _//3.获取Mapper接口的代理对象_
37.     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

38.     _//4.执行方法_
39.     int count = brandMapper.update(brand);
40.     System.out.println(count);

41.     _//5.释放资源_
42.     sqlSession.close();

43. }

6.2 修改动态字段

1.  编写接口方法：Mapper接口

- 参数：部分数据，封装到对象中
- 结果：void

1.  编写SQL语句：SQL映射文件
2.  <update id="update">
3.      update tb_brand
4.      <set>
5.          <if test="brandName != null and brandName != ''">
6.          brand_name = _#{brandName},_
7.          </if>
8.           <if test="companyName != null and companyName != ''">
9.          company_name = _#{companyName},_
10.          </if>
11.         <if test="ordered != null ">
12.         ordered = _#{ordered},_
13.         </if>
14.         <if test="description != null and description != ''">
15.             description = _#{description},_
16.         </if>
17.         <if test="status != null ">
18.         status = _#{status}_
19.         </if>
20.     </set>
21.          where id = _#{id};_
22. </update>

23.  执行方法，测试

24.  删除

7.1删除一个

1.  编写接口方法：Mapper接口

- 参数：id值
- 结果：void

void deleteById(int id);

1.  编写SQL语句：SQL映射文件
2.  <delete id="deleteById">
3.      delete from tb_brand where id = _#{id};_
4.  </delete>

5.  执行方法，测试
6.  @Test
7.  public void testDelete() throws Exception {
8.      _//0.接受参数_
9.      int id = 6;

10.      _//封装对象 对应对象参数接收_
11.      Brand brand = new Brand();
12.      brand.setId(id);

13.     _//1.获取SqlSessionFactory_
14.     String resource = "mybatis-config.xml";
15.     InputStream inputStream = Resources.getResourceAsStream(resource);
16.     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

17.     _//2. 获取SqlSession对象_
18.     SqlSession sqlSession = sqlSessionFactory.openSession(true);

19.     _//3.获取Mapper接口的代理对象_
20.     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

21.     _//4.执行方法_
22.     brandMapper.deleteById(id);

23.     _//5.释放资源_
24.     sqlSession.close();

25. }

7.2批量删除

1.  编写接口方法：Mapper接口

- 参数：id数组
- 结果：void

void deleteByIds(@Param("ids") int\[\] ids);

1.  编写SQL语句：SQL映射文件
2.  <delete id="deleteByIds">
3.      delete from tb_brand where id
4.      in (
5.          <foreach collection="ids" item="id" separator=","open="(" close=")">
6.              _#{id}#{id}#{id}_
7.          </foreach>
8.          )
9.  </delete>

10.  执行方法，测试
11.  @Test
12.  public void testDeleteByIds() throws Exception {
13.      _//0.接受参数_
14.      int\[\]ids = {5,7,8};

15.      _//1.获取SqlSessionFactory_
16.      String resource = "mybatis-config.xml";
17.     InputStream inputStream = Resources.getResourceAsStream(resource);
18.     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

19.     _//2. 获取SqlSession对象_
20.     SqlSession sqlSession = sqlSessionFactory.openSession(true);

21.     _//3.获取Mapper接口的代理对象_
22.     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

23.     _//4.执行方法_
24.     brandMapper.deleteByIds(ids);

25.     _//5.释放资源_
26.     sqlSession.close();

27.  优化

open="(" close=")"

## MyBatis参数查询

Mybatis接口方法中可以接受各种的参数，MyBatis底层对于这些参数进行不同的封装处理方式

- 单个参数

1.  pojo类型：直接使用，属性名 与 参数占位符名称一致
2.  Map集合：直接使用，键名 与 参数占位符一致
3.  Collection：封装为Map集合，可以使用@Param注解，替换Map集合中默认的arg键名

map.put(“arg0”,collection集合)

map.put(“collection”,collection集合)

1.  List：封装为Map集合，可以使用@Param注解，替换Map集合中默认的arg键名

map.put(“arg0”,list集合)

map.put(“collection”,list集合)

map.put(“list”,list集合)

1.  Array:封装为Map集合，可以使用@Param注解，替换Map集合中默认的arg键名

map.put(“arg0”,数组)

map.put(“array”,数组）

1.  其他类型：直接使用

- 多个参数：封装为Map集合，可以使用@Param注解，替换Map集合中默认的arg键名

MyBatis提供了ParaNameResolver类来进行参数封装

都使用@Param注解来修改Map集合中默认的键名，并使用修改后的名称来获取值，可读性更高

注解完成增删改查

使用注解开发会比配置文件开发更加方便，注解完成简单功能，配置文件完成复杂功能

查询@select

添加@Insert

修改@Update

删除@Delete

1.  案例
2.  编写接口方法及注释开发
3.  @Select("select \* from user where id = #{id}")
4.  User selectById(int id);
5.  测试用例

同testSelectById

# HTML

- HTML（HyperText Markup Language）是一种语言，所有语言都是用HTML语言编写出来的
- 标记语言：由标签构成的语言
- HTML运行在浏览器上，HTML标签由浏览器来解析
- HTML标签都是预定义好的。例如：使用<img>展示图片
- W3C标准：网页主要由三部分组成
- 结构：HTML
- 表现：CSS
- 行为：JavaScript

## HTML快速入门

1.  <html>
2.      <head>
3.          <title>hello html</title>
4.      </head>
5.      <body>
6.          <font color = "red">htmllllll</font>
7.      </body>
8.  </html>

9.  HTML文件以.htm或.html为扩展名
10.  HTML结构标签

- <HTML> 定义HTML文档
- <head> 定义关于文档的信息
- <title> 定义文档的标题
- <body> 定义文档的主题

1.  HTML标签不区分大小写
2.  HTML标签属性值 单双引皆可
3.  语法松散

## HTML标签

### 基础标签

<h1>-<h6> 定义标题，h1最大，h6最小

<b> 定义粗体文本

<i> 定义斜体文本 <u> 定义文本下划线

<p> 定义段落<center> 定义文本居中

<br> 定义新行<hr> 水平分割线

html表示颜色：

1.  英文单词：red,pink,blue..
2.  RGB表示（值1，值2，值3）取值范围0-255
3.  #值1 #值2 #值3 ; 值的范围00~FF 十六进制表示

4.  _<!-- html5 标识-->_
5.  <!DOCTYPE html>
6.  <html lang="en">
7.  <head>
8.      _<!-- 页面的字符集-->_
9.      <meta charset="UTF-8">
10.      <title>Title</title>
11.  </head>
12.  <body>

13. <h1>我是标题 h1</h1>
14. <h2>我是标题 h2</h2>
15. <h3>我是标题 h3</h3>
16. <h4>我是标题 h4</h4>
17. <h5>我是标题 h5</h5>
18. <h6>我是标题 h6</h6>

19. <hr>
20. _<!--_
21.     html 表示颜色：
22.         1. 英文单词：red,pink,blue...
23.         2. rgb(值1,值2,值3)：值的取值范围：0~255  rgb(255,0,0)
24.         3. #值1值2值3：值的范围：00~FF
25. \-->
26. <font face="楷体" size="5" color="#ff0000">传智教育</font>

27. <hr>

28. 刚察草原绿草如茵，沙柳河水流淌入湖。藏族牧民索南才让家中，茶几上摆着馓子、麻花和水果，炉子上刚煮开的奶茶香气四溢……<br>

29. 6月8日下午，习近平总书记来到青海省海北藏族自治州刚察县沙柳河镇果洛藏贡麻村，走进牧民索南才让家中，看望慰问藏族群众。

30. <hr>
31. <p>
32. 刚察草原绿草如茵，沙柳河水流淌入湖。藏族牧民索南才让家中，茶几上摆着馓子、麻花和水果，炉子上刚煮开的奶茶香气四溢……
33. </p>
34. <p>6月8日下午，习近平总书记来到青海省海北藏族自治州刚察县沙柳河镇果洛藏贡麻村，走进牧民索南才让家中，看望慰问藏族群众。
35. </p>
36. <hr>

37. 沙柳河水流淌<br>
38. 
39. <b>沙柳河水流淌</b><br>
40. <i>沙柳河水流淌</i><br>
41. <u>沙柳河水流淌</u><br>

42. <hr>
43. <center>
44. <b>沙柳河水流淌</b>
45. </center>
46. </body>
47. </html>

### 图片，音频，视频标签

<img> 定义图片

<audio> 定义音频

<video> 定义视频

1.  img：定义图片

- Src: 规定显示图像的URL（统一资源定位符）
- Height：定义图像的高度
- Width：定义图像的宽度

1.  <img src="../img/a.jpg" width="300" height="400">
2.  audio：定义音频，支持的音频格式：MP3，WAV，OGG

- Src：规定的音频的URL
- Controls：显示播放控件

1.  <audio src="b.mp3" controls></audio>
2.  Video：定义视频，支持的视频格式：MP4,WebM,OGG

- Src：规定视频的URL
- Controls：显示播放控件

1.  <video src="c.mp4" controls width="500" height="300"></video>

注：资源路径：

1.  绝对路径：完整路径
2.  相对路径：相对位置关系

### 超链接标签

<a> 定义超链接

Href：指定访问资源的URL

Target：指定打开资源的方式

- \_self：默认值，在当前页面打开
- \_blank：在空白页面打开

1.  <a href="https://www.itcast.cn" target="\_blank">点我有惊喜</a>

### 列表标签

1.  有序列表（order list）
2.  无序列表（unorder list）

<ol> 定义有序列表

<ul> 定义无序列表

<li> 定义列表项

1.  <ol type="A">
2.      <li>咖啡</li>
3.      <li>茶</li>
4.      <li>牛奶</li>
5.  </ol>

6.  <ul type="circle">
7.      <li>咖啡</li>
8.     <li>茶</li>
9.     <li>牛奶</li>
10. </ul>

Type设置项目符号 不推荐使用

### 表格标签

<table> 定义有序列表

<tr> 定义行

<td> 定义单元格

<th> 定义表头单元格

1.  table：定义表格

- Border：规定表格边框的宽度
- Width：规定表格的宽度
- Cellspacing：规定单元格之间的空白

1.  tr：定义行

- Align：定义行的对齐方式

1.  td：定义单元格

- rowspan：规定单元格可横跨的行数
- colspan：规定单元格可横跨的列数

1.  <table border="1" cellspacing="0" width="500">
2.      <tr>
3.          <th>序号</th>
4.          <th>品牌logo</th>
5.          <th>品牌名称</th>
6.          <th>企业名称</th>

7.      </tr>
8.      <tr align="center">
9.         <td>010</td>
10.         <td><img src="../img/三只松鼠.png" width="60" height="50"></td>
11.         <td>三只松鼠</td>
12.         <td>三只松鼠</td>
13.     </tr>

14.     <tr align="center">
15.         <td>009</td>
16.         <td><img src="../img/优衣库.png" width="60" height="50"></td>
17.         <td>优衣库</td>
18.         <td>优衣库</td>
19.     </tr>

20.     <tr align="center">
21.         <td>008</td>
22.         <td><img src="../img/小米.png" width="60" height="50"></td>
23.         <td>小米</td>
24.         <td>小米科技有限公司</td>
25.     </tr>

26. </table>

对逐行进行编辑

### 布局标签

<div> 定义html文档中的一个区域部分，经常与CSS一起使用。用来布局网页

<span> 用来组合行内元素

### 表单标签

表单：在网页中主要负责数据采集功能，使用<form>标签定义表单

表单项（元素）：不同类型的input元素，下拉列表，文本域等

<form> 定义表单

<input> 定义表单项，通过type属性控制输入形式

<label> 为表单项定义标注

<select> 定义下拉列表

<option> 定义下拉列表的列表项

<textarea> 定义文本域

Form：定义表单

- action：规定当提交表单时向何处发送表单数据，URL
- method：规定用于发送表单数据的方式
- Get：浏览器会将数据附在表单的action URL之后，大小有限制
- Post：浏览器会将数据放到http请求协议的请求体中，大小无限制

1.      <form action="#" method="post/get">
2.          <input type="text" name="username">
3.          <input type="submit">
4.      </form>

type取值：

Text：默认值，定义单行的输入字段

Password：定义密码字段

Radio：定义单选按钮

Checkbox：定义复选框

File：定义文件上传按钮

Hidden：定义隐藏的输入字段

Submit：定义提交按钮，提交按钮会把表单数据发送到服务器

Reset：定义重置按钮，重置按钮会清除表单中的所有数据

Button：定义可点击按钮

1.  <form action="#" method="post">
2.      <input type="hidden" name="id" value="123">

3.      <label for="username">用户名：</label>
4.      <input type="text" name="username" id="username"><br>

5.      <label for="password">密码：</label>
6.      <input type="password" name="password" id="password"><br>

7.     性别：
8.     <input type="radio" name="gender" value="1" id="male"> <label for="male">男</label>
9.     <input type="radio" name="gender" value="2" id="female"> <label for="female">女</label>
10.     <br>

11.     爱好：
12.     <input type="checkbox" name="hobby" value="1"> 旅游
13.     <input type="checkbox" name="hobby" value="2"> 电影
14.     <input type="checkbox" name="hobby" value="3"> 游戏
15.     <br>

16.     头像：
17.     <input type="file"><br>

18.     城市:
19.     <select name="city">
20.         <option>北京</option>
21.         <option value="shanghai">上海</option>
22.         <option>广州</option>
23.     </select>
24.     <br>

25.     个人描述：
26.     <textarea cols="20" rows="5" name="desc"></textarea>
27.     <br>
28.     <br>
29.     <input type="submit" value="免费注册">
30.     <input type="reset" value="重置">
31.     <input type="button" value="一个按钮">
32. </form>

## CSS

css是一门语言，用于控制网页表现，Cacading Style Sheet：层叠样式表

### CSS导入方式

CSS导入HTML有三种方式：

1.  内联样式：在标签内部使用style属性，属性值是css属性键值对
2.  内部样式：定义<style>标签，在标签内部定义css样式
3.  外部样式：定义link标签，导入外部的css文件
4.  <head>
5.      <meta charset="UTF-8">
6.      <title>Title</title>
7.      <style> --内部样式
8.          span{
9.              color: #ff0000;
10.         }
11.     </style>

12.     <link href="../css/demo.css" rel="stylesheet">--外部样式
13. </head>
14. <body>

15.     <div style="color: red">hello css</div>--内联样式

16.     <span>hello css </span>

17.     <p>hello css</p>

### CSS选择器

选择器是选取需设置的元素（标签）

1.  元素选择器
2.  Id选择器 --id要唯一
3.  类选择器 --可选择多个元素

\--谁选择的范围越小 谁就生效

1.  <head>
2.      <meta charset="UTF-8">
3.      <title>Title</title>

4.      <style>

5.          div{
6.              color: red;
7.          }

8.         #name{
9.             color: blue;
10.         }

11.         .cls{
12.             color: pink;
13.         }
14.     </style>

15. </head>
16. <body>

17. <div>div1</div>
18. <div id="name">div2</div>
19. <div class="cls">div3</div>

20. <span class="cls">span</span>

## JavaScript

- JavaScirpt是一门跨平台，面向对象的脚本语言，来控制网页行为，他能使网页可交付
- JavaScript和Java是完全不同的语言，不论是概念还是设计。但是基础语法类似

### JavaScript引入方式

1.  内部脚本：将JS代码定义在HTML页面中

在html中，JavaScript代码必须位于<Script>与</script>标签中

注：在HTML文档中可以在任意位置放置任意数量的<script>

一般把脚本置于<body>元素的底部，可改善显示速度，不会因为脚本执行而拖慢显示

1.  <script>
2.      alert("hello js1");
3.  </script>

外部脚本：将JS代码定义在外部Js文件中，然后引入到HTML页面中

<script src="../js/demo.js"></script>

注：外部脚本不能包含<script>标签

<script>标签不能自闭合

### JavaScript基础语法

1.  书写语法
2.  区分大小写：与Java一样，变量名，函数名以及其他一切东西都是区分大小写的
3.  每行结尾的分号可有可无
4.  大括号表示代码块

5.  输出语句

使用window.alert()写入警告框

使用document.write() 写入html输出

使用console.log() 写入浏览器控制台

1.  变量
2.  JavaScript 中用var关键字（variable的缩写）来声明变量

Var作用域：全局变量，变量可以重复定义

1.  JavaScript是一门弱类型语言，变量可以存放不同类型的值
2.  变量名需要遵循如下规则：

- 组成字符可以是任何字母，数字，下划线，或美元符号
- 数字不能开头
- 建议使用驼峰命名

1.  Script6中新增了let关键字来定义变量，他的用法类似于var，但是声明的变量只在let关键字所在的代码块内有效，且不允许重复声明
2.  Script6中新增了constant关键字来定义常量，用来声明一个只读的常量。一旦声明，常量的值就不能改变

3.  数据类型

JavaScript中分为：原始类型 和 引用类型

5种原始类型：

Number：数字（整数，小数，NaN）

String：字符，字符串，单双引皆可

Boolean：布尔，true/false

Null：对象为空（特殊）

var obj = null;

alert(typeof obj);_//object_

Undefined：当声明的变量未初始化时，该变量的默认值是undefined

使用typeof运算符可以获取数据类型

1.  运算符

同Java

\=== 与 ==

\==：判断类型是否一样，如果不一样，则进行类型转换

再去比较其值

\===：判断类型时候一样，如果不一样，则返回false

类型转换

其他类型转为number：

- - 1.  string: 按照字符串的字面值，转为数字,如果字面值不是数字，则转为NaN。一般使用parseInt或者在字符串前使用一个 “+”

var str = "20";

alert(parseInt(str) + 1);

- - 1.  boolean: true 转为1，false转为0

其他类型转为boolean：

1.  number:0和NaN转为false，其他的数字转为true
2.  string:空字符串转为false，其他的字符串转为true
3.  null:false
4.  undefined:false

5.  流程控制语句（同Java语言）

If

Switch

For

While

Do...while

1.  函数

函数是被设计为执行特定任务的代码块

JavaScript函数通过function关键词进行定义，语法为：

定义方式一：

1.  function functionName（参数1，参数2）{
2.   要执行的代码
3.  }

形式参数不需要类型，因为JavaScript是弱类型语言

返回值也不需要定义类型，可以在函数内部直接使用return返回即可

调用：函数名称（实际参数列表）

1.     function add(a,b){
2.         return a + b;
3.     }

4.     var result = add(1,2);

5.     alert(result);

定义方式二：

1.  var functionName = function(参数列表){
2.    要执行的代码
3.  }

4.  var add = function (a,b){
5.      return a + b;
6.  }

JS中，函数调用可以传递任意个数参数，只接收需要数量的参数

### JavaScript对象

1.  Array

JS Array对象用于定义数组

1.  定义
2.  var 变量名 = new Array（元素列表）;_//方式一_
3.  var 变量名 = \[元素列表\];_//方式二_

访问：

arr\[索引\]=值

索引从0开始

JavaScript数组 变长变类型

1.  属性：length
2.  方法

Push：添加方法

1.  var arr5 = \[1,2,3\];
2.  arr5.push(10);
3.  alert(arr5);

输出 1，2，3，10

Splice：删除元素

1.  arr5.splice(0,1);
2.  alert(arr5);

输出 2，3

1.  String
2.  定义
3.  var 变量名 = new String（“s”）;_//方式一_
4.  var 变量名 = s;_//方式二_
5.  属性：length
6.  方法：charAt（）；IndexOf（）...

Trim（）：去除字符串前后两端的空白字符

1.  自定义对象
2.  var 对象名称 ={
3.               属性名称：属性值1
4.               属性名称：属性值2
5.               ...
6.               函数名称：function（形参列表）{}
7.               ...
8.                 };

### BOM

- Browser Object Model 浏览器对象模型
- JavaScript将浏览器的各个组成部分封装为对象
- 组成：

Window：浏览器窗口对象

Navigator：浏览器对象

Screen：屏幕对象

History：历史记录对象

Location：地址栏对象

1.  Window

浏览器窗口对象

获取：直接使用window，其中window.可省略

1.  属性：获取其他BOM对象

History：对history对象的只读引用

方法：back（）：加载history列表中前一个URL

forward（）：加载history列表中的下一个URL

Navigator：对Navigator对象的只读引用

Screen：对Screen对象的只读引用

Location：用于窗口或框架的Location对象

属性：href：设置或返回完整的URL

1.      _//3秒跳转到首页_

2.      document.write("3秒跳转到首页...");
3.      setTimeout(function (){
4.          location.href = "https://www.baidu.com"
5.      },3000);

6.  方法

alert（）：显示一段消息和一个确认按钮的警告框

1.      //alert
2.      window.alert("abc");
3.      alert("bbb");

confirm（）：显示带有一段消息以及确认按钮和取消按钮的对话框

1.      _// confirm，点击确定按钮，返回true，点击取消按钮，返回false_
2.      var flag = confirm("确认删除？");

3.      _//alert(flag);_

4.      if(flag){
5.          _//删除逻辑_
6.      }

setInterval（）：按照指定的周期（以毫秒计）来调用函数或计算表达式

setTimeout（）：在指定的毫秒数后调用函数或计算表达式

1.      _/\*_
2.  _定时器_
3.          setTimeout(function,毫秒值): 在一定的时间间隔后执行一个function，只执行一次

4.          setInterval(function,毫秒值):在一定的时间间隔后执行一个function，循环执行
5.       \*/

6.      setTimeout(function (){
7.          alert("hehe");
8.     },3000);

9.     setInterval(function (){
10.         alert("hehe");
11.     },2000);

12.  定时器案例

要求实现：交替开关灯（一秒切换一张图片）

1.  <body>

2.  <input type="button" onclick="on()" value="开灯">
3.  <img id="myImage" border="0" src="../imgs/off.gif" style="text-align:center;">
4.  <input type="button" onclick="off()" value="关灯">

5.  <script>

6.      function on(){
7.         document.getElementById('myImage').src='../imgs/on.gif';
8.     }

9.     function off(){
10.         document.getElementById('myImage').src='../imgs/off.gif'
11.     }
12.     var x = 0;

13.     _// 根据一个变化的数字，产生固定个数的值； 2  x % 2     3   x % 3_
14.     _//定时器_
15.     setInterval(function (){

16.         if(x % 2 == 0){
17.             on();
18.         }else {
19.             off();
20.         }

21.         x ++;

22.     },1000);

23. </script>

24. </body>

### DOM

- Document Object Model 文档对象模型
- DOM定义了访问HTML和XML文档的标准
- 将标记语言的各个组成部分封装为对象

Document：整个文档对象

Element：元素对象

Attribute：属性对象

Text：文本对象

Comment：注释对象

1.  获取Element对象

Element：元素对象

获取：使用Document对象的方法来获取

1.  <img id="light" src="../imgs/off.gif"> <br>

2.  <div class="cls">传智教育</div>   <br>
3.  <div class="cls">黑马程序员</div> <br>

4.  <input type="checkbox" name="hobby"> 电影
5.  <input type="checkbox" name="hobby"> 旅游
6.  <input type="checkbox" name="hobby"> 游戏
7.  <br>

getElementById：根据id属性值获取，返回一个Element对象

1.  var img = document.getElementById("light");
2.  alert(img);

getElementByTagName：根据标签名称获取，返回Element对象数组

1.  var divs = document.getElementsByTagName("div");
2.  _// alert(divs.length);_
3.  for (let i = 0; i < divs.length; i++) {
4.      alert(divs\[i\]);
5.  }

getElementByName：根据name属性值获取，返回Element对象数组

1.  var hobbys = document.getElementsByName("hobby");
2.  for (let i = 0; i < hobbys.length; i++) {
3.      alert(hobbys\[i\]);
4.  }

getElementByClassName：根据class属性值获取，返回Element对象数组

1.  var clss = document.getElementsByClassName("cls");
2.  for (let i = 0; i < clss.length; i++) {
3.      alert(clss\[i\]);
4.  }

5.  常见HTML Element对象的使用

\--查阅文档 w3school.com

<img> src:img.src//改变图片属性

<div> style:设置元素css样式

innnerHTML：设置元素内容

<checkbox> checked:设置或返回checkbox是否被选中 true--被选中

1.  _[VUE](#_VUE)_

### 事件监听

- 事件：HTML事件是发生在HTML元素上的事情。比如

按钮被点击

鼠标移动到元素之上

按下键盘按键

- 事件监听：JavaScript可以在事件被侦测到时执行代码

1.  事件绑定

方式一：通过HTML标签中的按属性进行绑定

1.  <input type="button" value="点我" onclick="on()"> <br>
2.  <input type="button" value="再点我" id="btn">

3.  <script>

4.      function on(){
5.          alert("我被点了");
6.      }

7. </script>

方式二：通过DOM元素属性绑定

1.      document.getElementById("btn").onclick = function (){
2.          alert("我被点了");
3.      }

4.  常见事件

[HTML DOM 事件](https://www.w3school.com.cn/jsref/dom_obj_event.asp)

1.  <form id="register" action="#" >
2.      <input type="text" name="username" />

3.      <input type="submit" value="提交">
4.  </form>

5.  <script>
6.      document.getElementById("register").onsubmit = function (){
7.          _//onsubmit 返回true，则表单会被提交，返回false，则表单不提交_
8.         return true;
9.     }

10. </script>

常见事件：

Onclick 鼠标单击事件

Onblur 元素失去焦点

Onfocus 元素获得焦点

Onload 某个页面或图像被完成加载

Onsubmit 当表单提交时触发该事件

Onkeydown 某个键盘的键被按下

<font> 定义文本的字体，字体尺寸，字体颜色

Onmousover 鼠标被移到某元素之上

Onmouseout 鼠标从某元素移开

Event 代表事件对象

### 案例-表单验证

需求：

1.  当输入框失去焦点时，验证输入内容是否符合要求
2.  获取表单输入 var usernameInput = document.getElementById("username");
3.  绑定onblur事件 usernameInput.onblur = function(){}_;_
4.  获取输入内容 var username = usernameInput.value.trim();
5.  判断是否符合规则 var reg = /^\\w{6,12}$/;//正则表达式
6.  如果不符合规则，则显示错误提示信息

7.  当点击注册按钮时，判断所有输入框的内容是否都符合要求，如果不符合则组织表单提交
8.  获取表单对象 var regForm = document.getElementById("reg-form");
9.  为表单对象绑定onsubmit regForm.onsubmit = function () {}
10.  判断所有输入框是否都符合要求 如果符合返回true

完整代码见APPENDIX

### 正则表达式

1.  正则表达式定义了字符串组成的规则
2.  定义：
3.  直接量：注意不要加引号

var reg = /^\\w{6,12}$/;//不用引号

1.  创建RegExp对象

var reg = new RegExp("^\\w{6,12}$")；

1.  方法：

test（str）：判断指定字符串是否符合规则，返回true或false

1.  语法：

^：表示开始

$：表示结束

\[\]：代表某个范围内的单个字符，比如\[0-9\]单个数字字符

.：代表任意单个字符，除了换行和结束符

\\w：代表单词字符：字母，数字，下划线_

\\d：代表数字字符，相当于\[0-9\]

量词：

+：至少一个

\*：两个或多个

?：零个或一个

{x}：x个

{m,}：至少m个

{m,n}：至少m个，至多n个

1.  _//判断手机号是否符合规则：长度 11，数字组成，第一位是1_
2.  var reg = /^\[1\]\\d{10}$/;

## APPENDIX

7-表单验证

1.  <!DOCTYPE html>
2.  <html lang="en">
3.  <head>
4.      <meta charset="UTF-8">
5.      <title>欢迎注册</title>
6.      <link href="../css/register.css" rel="stylesheet">
7.  </head>
8.  <body>

9. <div class="form-div">
10.     <div class="reg-content">
11.         <h1>欢迎注册</h1>
12.         <span>已有账号？</span> <a href="#">登录</a>
13.     </div>
14.     <form id="reg-form" action="#" method="get">

15.         <table>

16.             <tr>
17.                 <td>用户名</td>
18.                 <td class="inputs">
19.                     <input name="username" type="text" id="username">
20.                     <br>
21.                     <span id="username_err" class="err_msg" style="display: none">用户名不太受欢迎</span>
22.                 </td>

23.             </tr>

24.             <tr>
25.                 <td>密码</td>
26.                 <td class="inputs">
27.                     <input name="password" type="password" id="password">
28.                     <br>
29.                     <span id="password_err" class="err_msg" style="display: none">密码格式有误</span>
30.                 </td>
31.             </tr>

32.             <tr>
33.                 <td>手机号</td>
34.                 <td class="inputs"><input name="tel" type="text" id="tel">
35.                     <br>
36.                     <span id="tel_err" class="err_msg" style="display: none">手机号格式有误</span>
37.                 </td>
38.             </tr>

39.         </table>

40.         <div class="buttons">
41.             <input value="注 册" type="submit" id="reg_btn">
42.         </div>
43.         <br class="clear">
44.     </form>

45. </div>

46. <script>

47.     _//1. 验证用户名是否符合规则_
48.     _//1.1 获取用户名的输入框_
49.     var usernameInput = document.getElementById("username");

50.     _//1.2 绑定onblur事件 失去焦点_
51.     usernameInput.onblur = checkUsername;

52.     function checkUsername() {
53.         _//1.3 获取用户输入的用户名_
54.         var username = usernameInput.value.trim();

55.         _//1.4 判断用户名是否符合规则：长度 6~12,单词字符组成_
56.         var reg = /^\\w{6,12}$/;
57.         var flag = reg.test(username);

58.         _//var flag = username.length >= 6 && username.length <= 12;_
59.         if (flag) {
60.             _//符合规则_
61.             document.getElementById("username_err").style.display = 'none';
62.         } else {
63.             _//不符合规则_
64.             document.getElementById("username_err").style.display = '';//设置css的style文件
65.         }

66.         return flag;
67.     }

68.     _//1. 验证密码是否符合规则_
69.     _//1.1 获取密码的输入框_
70.     var passwordInput = document.getElementById("password");

71.     _//1.2 绑定onblur事件 失去焦点_
72.     passwordInput.onblur = checkPassword;

73.     function checkPassword() {
74.         _//1.3 获取用户输入的密码_
75.         var password = passwordInput.value.trim();

76.         _//1.4 判断密码是否符合规则：长度 6~12_
100.        var reg = /^\\w{6,12}$/;
101.        var flag = reg.test(password);

103.        _//var flag = password.length >= 6 && password.length <= 12;_
104.        if (flag) {
105.            _//符合规则_
106.            document.getElementById("password_err").style.display = 'none';
107.        } else {
108.            _//不符合规则_
109.            document.getElementById("password_err").style.display = '';
110.        }

112.        return flag;
113.    }

116.    _//1. 验证手机号是否符合规则_
117.    _//1.1 获取手机号的输入框_
118.    var telInput = document.getElementById("tel");

120.    _//1.2 绑定onblur事件 失去焦点_
121.    telInput.onblur = checkTel;

123.    function checkTel() {
124.        _//1.3 获取用户输入的手机号_
125.        var tel = telInput.value.trim();

127.        _//1.4 判断手机号是否符合规则：长度 11，数字组成，第一位是1_

129.        _//var flag = tel.length == 11;_
130.        var reg = /^\[1\]\\d{10}$/;
131.        var flag = reg.test(tel);
132.        if (flag) {
133.            _//符合规则_
134.            document.getElementById("tel_err").style.display = 'none';
135.        } else {
136.            _//不符合规则_
137.            document.getElementById("tel_err").style.display = '';
138.        }

140.        return flag;
141.    }

144.    _//1. 获取表单对象_
145.    var regForm = document.getElementById("reg-form");

147.    _//2. 绑定onsubmit 事件_
148.    regForm.onsubmit = function () {
149.        _//挨个判断每一个表单项是否都符合要求，如果有一个不符合，则返回false_

151.        var flag = checkUsername() && checkPassword() && checkTel();

153.        return flag;
154.    }

156.</script>
157.</body>
158.</html>

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

## Servlet

- Servlet是Java提供的一门动态web资源开发技术
- Servlet是JavaEE规范之一，其实就是一个接口，将来需要定义Servlet接口，并由web服务器运行Servlet

### 快速入门

1.  创建web项目，导入Servlet依赖坐标
2.      _<!-- 导入Servlet依赖坐标 -->_
3.      <dependencies>
4.          <dependency>
5.              <groupId>javax.servlet</groupId>
6.              <artifactId>javax.servlet-api</artifactId>
7.              <version>3.1.0</version>
8.              <scope>provided</scope>
9.          </dependency>
10.     </dependencies>

11.  创建：定义一个类，实现Servlet接口，并重写接口中所有方法，并在service方法中输入一句话

注：重写接口中所有方法 在继承类后快捷键Alt+Enter

1.  public class ServletDemo1 implements Servlet {

2.      @Override
3.      public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {
4.          System.out.println("servlet hello world");
5.      }

6.      @Override
7.      public String getServletInfo() {
8.         return "";
9.     }

10.     @Override
11.     public void destroy() {

12.     }

13.     @Override
14.     public void init(ServletConfig servletConfig) throws ServletException {

15.     }

16.     @Override
17.     public ServletConfig getServletConfig() {
18.         return null;
19.     }
20. }

21.  配置：在类中使用@WebServlet注解，配置该Servlet的访问路径

@WebServlet("/demo1")

1.  访问：启动Tomcat，浏览器输入URL访问该Servlet

### Servlet执行流程

https：//localhost:8080/web-demo/demo1

| | |

访问到服务器 访问到web项目 访问到对应的Servlet

Servlet由web服务器创建，servlet方法由web服务器调用

自定义的Servlet，必须实现Servlet接口并复写其方法，而servle接口中由service方法

### Servlet生命周期

1.  对象的生命周期指一个对象从被创建到被销毁的整个过程
2.  Servlet运行在Servlet容器（Web服务器）中，其生命周期由容器来管理，分为四个阶段：
3.  加载和实例化：默认情况下，当Servlet第一次被访问时，由容器创建Servlet对象
4.  初始化：在Servlet实例化之后，容器将调用Servlet的init（）方法初始化这个对象，完

成一些如加载配置文件，创建链接等初始化工作。该方法只调用一次

1.  请求处理：每次请求servlet时，Servlet容器都会调用Servlet的service（）方法对请求进

行处理

1.  服务终止：当需要释放内存或容器关闭时，容器就会调用Servlet实例中的destory（）方

法完成资源的释放。在destory（）方法调用之后，容器会释放这个Servlet实例，该实例随后会被Java的垃圾收集器所回收

1.  Init：

调用时机：默认情况下，Servlet被第一次访问时调用

调用次数：1次

loadOnStartup：更改注释，负整数时第一次被访问时创建Servlet对象，0或正整数时服务器启动时创建Servlet对象，数字越小优先级越高

@WebServlet(urlPatterns ="/demo1"，loadOnStartup =1)

1.  Service：

调用时机：每一次servlet被访问时调用

调用次数：多次

1.  Destroy：

调用时机：内存释放或服务器关闭时，Servlet对象会被销毁，调用

调用次数：1次

1.  Servlet方法

初始化方法，在Servlet被创建时执行，只执行一次

void init(ServletConfig servletConfig)

提供服务方法，每次Servlet被访问，都会调用该方法

void service(ServletRequest servletRequest, ServletResponse servletResponse)

销毁方法：当Servlet被销毁时，调用该方法，在内存释放或服务器关闭时销毁Servlet

void destroy()

获取ServletConfig对象

void init(ServletConfig servletConfig)

获取Servlet信息

ServletConfig getServletConfig()

### Servlet体系结构

Servlet ---Servlet体系根接口

|

GenericServlet ----Servlet抽象实现类

|

HttpServlet -----对HTTP协议封装的Servlet实现类

开发B/S架构的web项目，都是针对http协议，所以自定义Servlet时会继承HttpServlet

HttpServlet原理：根据请求方式的不同，进行分别的处理，获取请求方式进行不同逻辑判断

详细解析：

1.  public class ServletDemo6 implements Servlet {
2.      @Override
3.      public void init(ServletConfig config) throws ServletException {

4.      }

5.      @Override
6.      public ServletConfig getServletConfig() {
7.          return null;
8.     }

9.     @Override
10.     public void service(ServletRequest req, ServletResponse res) throws ServletException, IOException {
11.         _// 根据请求方式的不同，进行分别的处理_

12.         HttpServletRequest request = (HttpServletRequest) req;

13.         _//1. 获取请求方式_
14.         String method = request.getMethod();
15.         _//2. 判断_
16.         if("GET".equals(method)){
17.             _// get方式的处理逻辑_
18.         }else if("POST".equals(method)){
19.             _// post方式的处理逻辑_
20.         }
21.     }

22.     @Override
23.     public String getServletInfo() {
24.         return null;
25.     }

26.     @Override
27.     public void destroy() {

28.     }
29. }

编写一个原始的实现Servlet类 需要复写四种方法，应为get/post请求参数位置不同 post的请求参数在请求体中，而get在请求行中，所以在service层中需要不同的处理逻辑，根据请求方式的不同，进行分别的处理，而这一部分的逻辑代码完全重复，可以写一个类，让所有servlet都继承自这个类，复用代码，这个类就是HttpServlet，将get的处理逻辑封装成方法doGet()，将post的处理逻辑封装成方法doPost(),这样就不需要实现Servlet接口了，直接继承自HttpServlet，复写doPost()和doGet()用来处理业务逻辑。做到了Http协议的封装，并且完成了对不同请求方式的分发。

HttpServlet使用步骤：继承HttpServlet，重写doGet，doPost方法

### Servlet urlPattern配置

Servlet要想被访问，必须配置其访问路径（urlPattern）

1.  一个Servlet，可以配置多个urlPattern

@WebServlet(urlPatterns ="/demo1","/demo2")

1.  urlPattern配置规则
2.  精确匹配

配置路径：@WebServlet(urlPatterns = "/user/select")

访问路径：localhost:8080/web-demo/user/select

范围小的优先级更高，如果一个目录同时满足精确匹配与目录匹配时，精确匹配优先

1.  目录匹配

配置路径：@WebServlet(urlPatterns = "/user/\*")

访问路径：localhost:8080/web-demo/user/aaa

localhost:8080/web-demo/user/bbb

1.  扩展名匹配

配置路径：@WebServlet(urlPatterns = "\*.do")

访问路径：localhost:8080/web-demo/aaa.do

localhost:8080/web-demo/bbb.do

注：不以/开头  

1.  任意匹配

配置路径：@WebServlet("/")

@WebServlet("/\*")

访问路径：localhost:8080/web-demo/haha

localhost:8080/web-demo/hehe

注：

当项目中的Servlet配置了”/”，会覆盖掉tomcat中的DefaultServlet，当其他的url-pattern都匹配不上时都会走这个Servlet

当项目中的Servlet配置了”/\*”，意味着匹配所有路径

尽量不用任意匹配

精确路径>目录路径>扩展名路径> /\* > /

### XML配置方法编写Servlet（旧版本）

Servlet从3.0开始支持使用注解注释，3.0之前只支持XML配置文件的配置方式

步骤

1.  编写Servlet类
2.  在web.xml中配置该Servlet
3.      _<!--_Servlet 全类名-->
4.      <servlet>
5.          <servlet-name>demo13</servlet-name>
6.          <servlet-class>com.itheima.web.ServletDemo13</servlet-class>
7.      </servlet>

8.      _<!--_Servlet 访问路径-->
9.     <servlet-mapping>
10.         <servlet-name>demo13</servlet-name>
11.         <url-pattern>/demo13</url-pattern>
12.     </servlet-mapping>

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

## JSP

- JavaServerPages，java服务端页面
- 一种动态的网页技术，其中既可以定义HTML，JS，CSS等静态内容，还可以定义Java代码的动态内容
- JSP = HTML + Java
- JSP的作用：简化开发，避免了在Servlet中直接输出HTML标签

### JSP原理

- JSP本质上是一个Servlet
- JSP容器（Tomcat）会将.jsp文件转换成.java文件，再由JSP容器（Tomcat）将其编译，最终对外提供服务的其实就是这个字节码文件

### JSP脚本

- JSP脚本用于在JSP页面内定义Java代码
- JSP脚本分类

<%..%>：内容会直接放到_jspService()方法之中

<%=...%>：内容会放到out.print()方法中，作为out.print()的参数

<%!...%>：内容会放到_jspService()之外，被类直接包含

1.  关于脚本与截断的案例
2.  <table border="1" cellspacing="0" width="800">
3.      <tr>
4.          <th>序号</th>
5.          <th>品牌名称</th>
6.          <th>企业名称</th>
7.          <th>排序</th>
8.          <th>品牌介绍</th>
9.          <th>状态</th>
10.         <th>操作</th>
11.     </tr>
12.     <%
13.         for (int i = 0; i < brands.size(); i++) {
14.             Brand brand = brands.get(i);
15.     %>

16.     <tr align="center">
17.         <td><%=brand.getId()%></td>
18.         <td><%=brand.getBrandName()%></td>
19.         <td><%=brand.getCompanyName()%></td>
20.         <td><%=brand.getOrdered()%></td>
21.         <td><%=brand.getDescription()%></td>

22.         <%
23.             if(brand.getStatus() == 1){
24.                 //显示启用
25.         %>
26.             <td><%="启用"%></td>
27.         <%
28.             }else {
29.                 // 显示禁用
30.         %>
31.             <td><%="禁用"%></td>
32.         <%
33.             }
34.         %>

35.         <td><a href="#">修改</a> <a href="#">删除</a></td>
36.     </tr>
37.     <%
38.         }
39.     %>

40. </table>

41.  JSP的缺点

由于JSP页面内，既可以定义HTML标签，又可以定义Java代码，造成以下问题：

1.  书写麻烦：特别是复杂的页面
2.  阅读麻烦
3.  复杂度高：运行需要依赖于各种环境，JRE，JSP容器，JavaEE
4.  占内存和磁盘：JSP会自动生成.java和.class文件占磁盘，运行的是.class文件占内存
5.  调试困难：出错后，需要找到自动生成的.java文件进行调试
6.  不利于团队协作

Servlet-----------JSP----------Servlet+JSP--------------------------------------------Servlet+html+ajax

|

JSP只负责数据的展示而不负责数据的处理，不直接在JSP中写代码

Servlet负责逻辑处理与数据封装处理，转发到JSP中

### JSP快速入门

1.  导入JSP坐标
2.  <dependency>
3.      <groupId>javax.servlet.jsp</groupId>
4.      <artifactId>jsp-api</artifactId>
5.      <version>2.2</version>
6.      <scope>provided</scope>
7.  </dependency>

8.  创建JSP文件
9.  编写HTML标签和Java代码
10.      <h1>hello jsp</h1>

11.      <%
12.          System.out.println("hello,jsp~");
13.          int i = 3;
14.      %>

### EL表达式

- ExpressionLanguage 表达式语言，用于简化JSP页面内的Java代码
- 主要功能：获取数据
- 语法：${expression}

${brands}：获取域中存储的key为brands的数据

1.  @Override
2.  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
3.      _//1. 准备数据_
4.      List<Brand> brands = new ArrayList<Brand>();
5.      brands.add(new Brand(1,"三只松鼠","三只松鼠",100,"三只松鼠，好吃不上火",1));
6.      brands.add(new Brand(2,"优衣库","优衣库",200,"优衣库，服适人生",0));
7.      brands.add(new Brand(3,"小米","小米科技有限公司",1000,"为发烧而生",1));

8.      _//2. 存储到request域中_
9.     request.setAttribute("brands",brands);
10.     request.setAttribute("status",1);

11.     _//3. 转发到 el-demo.jsp_
12.     request.getRequestDispatcher("/el-demo.jsp").forward(request,response);

el-demo.jsp:

${brands}

JavaWeb中的四大域对象：

Page：当前页面有效

Request：当前请求有效

Session：当前会话有效

Application：当前应用有效

el表达式获取数据，会依次从这4个域中寻找，直到找到为止

### JSTL标签

- Jsp Standard Tag Library，JSP标准标签库。使用标签取代JSP页面上的Java代码

<c:if>

<c:foreach>

1）JSTL快速入门

1.  导入坐标
2.  <dependency>
3.      <groupId>jstl</groupId>
4.      <artifactId>jstl</artifactId>
5.      <version>1.2</version>
6.  </dependency>
7.  <dependency>
8.       <groupId>taglibs</groupId>
9.       <artifactId>standard</artifactId>
10.      <version>1.1.2</version>
11. </dependency>

12.  在JSP页面上引入JSTL标签库

<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

1.  使用：一般与EL表达式结合使用

<c:if>

jstl-if.jsp

1.      <c:if test="${status ==1}">
2.          启用
3.      </c:if>

4.      <c:if test="${status ==0}">
5.          禁用
6.      </c:if>

ServletDemo1:

request.getRequestDispatcher("/jstl-if.jsp").forward(request,response);

<c:forEach>：相当于for循环

Items：被遍历的容器

Var：遍历产生的临时变量

varStatus：生成序号

status有两个属性 index从0开始，count从1开始

jstl-foreach.jsp

1.  <input type="button" value="新增"><br>
2.  <hr>
3.  <table border="1" cellspacing="0" width="800">
4.      <tr>
5.          <th>序号</th>
6.          <th>品牌名称</th>
7.          <th>企业名称</th>
8.          <th>排序</th>
9.          <th>品牌介绍</th>
10.         <th>状态</th>
11.         <th>操作</th>

12.     </tr>

13.     <c:forEach items="${brands}" var="brand" varStatus="status">
14.         <tr align="center">
15.             <--<td>${brand.id}</td>-->
16.             <td>${status.count}</td>
17.             <td>${brand.brandName}</td>
18.             <td>${brand.companyName}</td>
19.             <td>${brand.ordered}</td>
20.             <td>${brand.description}</td>
21.             <c:if test="${brand.status == 1}">
22.                 <td>启用</td>
23.             </c:if>
24.             <c:if test="${brand.status != 1}">
25.                 <td>禁用</td>
26.             </c:if>

27.             <td><a href="#">修改</a> <a href="#">删除</a></td>
28.         </tr>

29.     </c:forEach>

普通for循环

1.  <c:forEach begin="1" end="10" step="1" var="i">
2.      <a href="#">${i}</a>
3.  </c:forEach>

应用-分页进度条

### MVC模式和三层架构

- MVC是一种分层开发的模式，其中：
- M：model，业务模型，处理业务--JavaBean
- V：view，视图，界面展示--JSP
- C：controller，控制器，处理请求，调用模型和视图--Servlet
- MVC好处
- 职责单一，互不影响
- 有利于分工协作
- 有利于组件重组
- 三层架构与三大框架（SSM）
- 表现层 com.org.web/controller 框架：SpringMVC/Struts2

接收请求，封装数据，调用业务逻辑层，响应数据

- 业务逻辑层 com.org.service 框架：Spring

对业务逻辑进行封装，组合数据访问层中基本功能，形成复杂的业务逻辑功能

- 数据访问层 com.org.dao/mapper 框架：MyBatis/Hibername

JDBC，MyBatis，对数据库的CRUD操作

### 案例

完成品牌的增删改查操作 Servlet/JSP/三层架构

#### 准备环境

- 创建新的模块，brand_demo，引入坐标

1.  <dependencies>
2.          _<!--mybatis-->_
3.          _<!--mysql-->_
4.          _<!--servlet-->_
5.          _<!--jsp-->_
6.          _<!--jstl-->_
7.  </dependencies>
8.      <build> 
9.          <plugins> 
10.             <plugin> 
11.                 <groupId>org.apache.tomcat.maven</groupId>
12.                 <artifactId>tomcat7-maven-plugin</artifactId>
13.                 <version>2.2</version>
14.             </plugin>
15.         </plugins>
16.     </build>

- 创建三层架构的包结构
- 数据库表 tb_brand
- 实体类Brand
- MyBatis基础环境
- Mybatis-config.xml
- BrandMapper.xml
- BrandMapper接口

#### 查询所有

1.  Dao层

BrandMapper.java

1.      _/\*\*_
2.       \* 查询所有
3.       \* @return
4.       \*/
5.  @ResultMap("brandResultMap")
6.      @Select("select \* from tb_brand")
7.      List<Brand> selectAll();

在接口中创建一个方法，selectAll返回一个Brand的list集合

注解sql @Select

注解ResultMap @ResultMap确定映射关系，驼峰命名与原变量的命名映射

BrandMapper.xml

1.      <resultMap id="brandResultMap" type="brand">
2.          <result column="brand_name" property="brandName"></result>
3.          <result column="company_name" property="companyName"></result>
4.      </resultMap>

5.  Service层

在service包中新建BrandService.java

1.  public class BrandService {
2.      SqlSessionFactory factory = SqlSessionFactoryUtils.getSqlSessionFactory();

3.      _/\*\*_
4.       \* 查询所有
5.       \* @return
6.       \*/
7.      public List<Brand> selectAll() {

8.         _//调用brandMapper.selectAll()_

9.         _//2.获取SqlSession对象_
10.         SqlSession sqlSession = factory.openSession();

11.         _//3.获取brandMapper_
12.         BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

13.         _//4.调用方法_
14.         List<Brand> brands = mapper.selectAll();

15.         sqlSession.close();

16.         return brands;
17.     }
18. }

Utill类 -同JavaWeb-Web核心-Request & Response-案例-代码优化

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

17.  Web层

web-selectAllServlet

1.  @WebServlet("/selectAllServlet")
2.  public class SelectAllServlet extends HttpServlet {

3.      private BrandService service = new BrandService();
4.      @Override
5.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

6.          _//1.调用BrandService完成查询_
7.          BrandService service = new BrandService();
8.         List<Brand> brands = service.selectAll();

9.         _//2.将brands存入request域中_
10.         request.setAttribute("brands",brands);

11.         _//3.转发到brand.jsp页面_
12.         request.getRequestDispatcher("/brand.jsp").forward(request,response);

13.     }

14.     @Override
15.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
16.         this.doGet(request, response);
17.     }
18. }

- 创建Brandservice对象，使用selectAll（）方法进行查询，并把查询到的结果brands封装到list集合
- 将brands存入request域中
- 转发到brand.jsp页面中

brand.jsp

1.  <input type="button" value="新增"><br>
2.  <hr>
3.  <table border="1" cellspacing="0" width="800">
4.      <tr>
5.          <th>序号</th>
6.          <th>品牌名称</th>
7.          <th>企业名称</th>
8.          <th>排序</th>
9.          <th>品牌介绍</th>
10.         <th>状态</th>
11.         <th>操作</th>

12.     </tr>

13.     <c:forEach items="${brands}" var="brand" varStatus="status">
14.         <tr align="center">
15.             <%--<td>${brand.id}</td>--%>
16.             <td>${status.count}</td>
17.             <td>${brand.brandName}</td>
18.             <td>${brand.companyName}</td>
19.             <td>${brand.ordered}</td>
20.             <td>${brand.description}</td>
21.             <c:if test="${brand.status == 1}">
22.                 <td>启用</td>
23.             </c:if>
24.             <c:if test="${brand.status != 1}">
25.                 <td>禁用</td>
26.             </c:if>

27.             <td><a href="#">修改</a> <a href="#">删除</a></td>
28.         </tr>

29.     </c:forEach>
30. </table>

brand.jsp负责显示

#### 添加

1.  Dao层

BrandMapper.java

1.  @Insert("insert into tb_brand values (null,#{brandName},#{companyName},#{ordered},#{description},#{status})")
2.  @ResultMap("brandResultMap")
3.  void add(Brand brand);

4.  Service层

BrandService.java

1.  _/\*\*_
2.       \* 添加
3.       \* @param brand
4.       \*/
5.      public void add(Brand brand) {

6.          _//调用brandMapper.add(brand)_

7.          _//2.获取SqlSession对象_
8.         SqlSession sqlSession = factory.openSession();

9.         _//3.获取brandMapper_
10.         BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

11.         mapper.add(brand);

12.         _//提交事务_
13.         sqlSession.commit();
14.         sqlSession.close();
15.     }

增删改行为需要提交事务

1.  Web层

对brand.jsp进行修改

1.  <input type="button" value="新增" id="add"><br>
2.  ...
3.  <script>
4.      document.getElementById("add").onclick = function () {
5.          location.href = "/brand-demo/addBrand.jsp"
6.      }
7.  </script>

在新增按钮上添加id，并用JavaScript的onclick事件绑定按钮

AddServlet.java

1.  @WebServlet("/addServlet")
2.  public class AddServlet extends HttpServlet {
3.      private BrandService service = new BrandService();

4.      @Override
5.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
6.          _//1.接收数据_
7.          request.setCharacterEncoding("utf-8");_//处理post请求乱码问题_
8.          String brandName = request.getParameter("brandName");
9.         String companyName = request.getParameter("companyName");
10.         String description = request.getParameter("description");
11.         String ordered = request.getParameter("ordered");
12.         String status = request.getParameter("status");

13.         _//2.封装数据_
14.         Brand brand = new Brand();
15.         brand.setBrandName(brandName);
16.         brand.setCompanyName(companyName);
17.         brand.setDescription(description);
18.         brand.setOrdered(Integer.parseInt(ordered));
19.         brand.setStatus(Integer.parseInt(status));

20.         _//3.调用service 完成添加_
21.         service.add(brand);

22.         _//转发到查询所有Servlet_
23.         request.getRequestDispatcher("/selectAllServlet").forward(request,response);

24.     }

25.     @Override
26.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
27.         this.doGet(request, response);
28.     }

新建一个添加页表单，静态页面，完成添加操作

1.  <!DOCTYPE html>
2.  <html lang="en">

3.  <head>
4.    <meta charset="UTF-8">
5.    <title>添加品牌</title>
6.  </head>
7.  <body>
8.  <h3>添加品牌</h3>
9. <form action="/brand-demo/addServlet" method="post">
10.   品牌名称：<input name="brandName"><br>
11.   企业名称：<input name="companyName"><br>
12.   排序：<input name="ordered"><br>
13.   描述信息：<textarea rows="5" cols="20" name="description"></textarea><br>
14.   状态：
15.   <input type="radio" name="status" value="0">禁用
16.   <input type="radio" name="status" value="1">启用<br>

17.   <input type="submit" value="提交">
18. </form>
19. </body>
20. </html>

#### 修改-回显数据

1.  Dao层

BrandMapper.java

1.      @Select("select \* from tb_brand where id=#{id}")
2.      @ResultMap("brandResultMap")
3.      Brand selectById(int id);

4.  Service层
5.      public Brand selectById(int id) {

6.          _//调用brandMapper.selectAll()_

7.          _//2.获取SqlSession对象_
8.          SqlSession sqlSession = factory.openSession();

9.         _//3.获取brandMapper_
10.         BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

11.         _//4.调用方法_
12.         Brand brand = mapper.selectById(id);

13.         sqlSession.close();

14.         return brand;
15.     }

16.  Web层

SelectByIdServlet.java

1.  @WebServlet("/selectByIdServlet")
2.  public class SelectByIdServlet extends HttpServlet {
3.      private BrandService service = new BrandService();

4.      @Override
5.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
6.          _//接受id_
7.          String id = request.getParameter("id");

8.         _//调用service查询_
9.         Brand brand = service.selectById(Integer.parseInt(id));

10.         _//存储到request中_
11.         request.setAttribute("brand",brand);

12.         _//转发到update.jsp_
13.         request.getRequestDispatcher("/update.jsp").forward(request,response);

14.     }

15.     @Override
16.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
17.         this.doGet(request, response);
18.     }
19. }

新建update.jsp

1.  <h3>修改品牌</h3>
2.  <form action="/brand-demo/updateServlet" method="post">
3.    品牌名称：<input name="brandName" value="${brand.brandName}"><br>
4.    企业名称：<input name="companyName"value="${brand.companyName}><br>
5.    排序：<input name="ordered"value="${brand.ordered}><br>
6.    描述信息：<textarea rows="5" cols="20" name ="description"${brand.brandName}></textarea><br>
7.    状态：
8.    <c:if test="${brand.status == 1}">
9.      <input type="radio" name="status" value="1" checked>启用
10.     <input type="radio" name="status" value="0">禁用<br>
11.   </c:if>

12.   <c:if test="${brand.status == 0}">
13.   <input type="radio" name="status" value="0" checked>禁用
14.   <input type="radio" name="status" value="1">启用<br>
15.   </c:if>

16.   <input type="submit" value="提交">
17. </form>

修改brand.jsp

<td><a href="/brand-demo/selectByIdServlet?id=${brand.id}">修改</a> 

修改处使用超链接，跳转到selectByIdServlet，

${brand.id} 是 JSP EL 表达式，表示从 brand 对象中获取 id 属性的值。

#### 修改-修改数据

1.  Dao层
2.  @Update("update tb_brand set brand_name=#{brandName},company_name=#{companyName},ordered=#{ordered},description=#{description},status=#{status} where id=#{id}")
3.  void update(Brand brand);

这里不需要使用@ResultMap

@ResultMap 是 MyBatis 中用于定义查询结果如何映射到 Java 对象的注解，结果集映射。

它仅在 有返回值的 SQL 操作（如 @Select）中使用，用来告诉 MyBatis 如何将数据库字段映射到实体类属性。@Update 是执行更新操作（UPDATE），它没有返回值（或返回受影响行数），MyBatis 不需要进行结果集映射。因此，MyBatis 不允许在 @Update / @Insert /@Delete上使用 @ResultMap 注解，否则编译或运行时报错。

1.  Service层
2.  _/\*\*_
3.   \* 修改
4.   \* @param brand
5.   \*/
6.  public void update(Brand brand) {

7.      _//调用brandMapper.add(brand)_

8.     _//2.获取SqlSession对象_
9.     SqlSession sqlSession = factory.openSession();

10.     _//3.获取brandMapper_
11.     BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

12.     mapper.update(brand);

13.     _//提交事务_
14.     sqlSession.commit();
15.     sqlSession.close();
16. }

17.  Web层

UpdateServlet.java

1.  @WebServlet("/updateServlet")
2.  public class UpdateServlet extends HttpServlet {
3.      private BrandService service = new BrandService();

4.      @Override
5.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
6.          _//1.接收数据_
7.          request.setCharacterEncoding("utf-8");_//处理post请求乱码问题_
8.          String id = request.getParameter("id");
9.         String brandName = request.getParameter("brandName");
10.         String companyName = request.getParameter("companyName");
11.         String description = request.getParameter("description");
12.         String ordered = request.getParameter("ordered");
13.         String status = request.getParameter("status");

14.         _//2.封装数据_
15.         Brand brand = new Brand();
16.         brand.setId(Integer.parseInt(id));
17.         brand.setBrandName(brandName);
18.         brand.setCompanyName(companyName);
19.         brand.setDescription(description);
20.         brand.setOrdered(Integer.parseInt(ordered));
21.         brand.setStatus(Integer.parseInt(status));

22.         _//3.调用service 完成修改_
23.         service.update(brand);

24.         _//转发到查询所有Servlet_
25.         request.getRequestDispatcher("/selectAllServlet").forward(request,response);

26.     }

27.     @Override
28.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
29.         this.doGet(request, response);
30.     }
31. }

新建update.jsp

1.  <h3>修改品牌</h3>
2.  <form action="/brand-demo/updateServlet" method="post">

3.    <%--隐藏域，提交id--%>
4.    <input type="hidden" name="id" value="${brand.id}">

5.    品牌名称：<input name="brandName" value="${brand.brandName}"><br>
6.    企业名称：<input name="companyName"value="${brand.companyName}"><br>
7.    排序：<input name="ordered"value="${brand.ordered}"><br>
8.   描述信息：<textarea rows="5" cols="20" name="description"${brand.description}></textarea><br>
9.   状态：
10.   <c:if test="${brand.status == 1}">
11.     <input type="radio" name="status" value="1" checked>启用
12.     <input type="radio" name="status" value="0">禁用<br>
13.   </c:if>

14.   <c:if test="${brand.status == 0}">
15.   <input type="radio" name="status" value="0" checked>禁用
16.   <input type="radio" name="status" value="1">启用<br>
17.   </c:if>
18.   <input type="submit" value="提交">
19. </form>

#### 删除数据

见brand-demo

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

## AJAX

- Asnchronous JavaScript And XML：异步的JavaScript和XML
- AJAX作用：
- 与服务器进行数据交换：通过AJAX可以给服务器发送请求，并获取服务器响应的数据，

在此之前通过Servlet查询数据，将数据存到域对象中，转发到JSP展示数据，将JSP当作视图，对浏览器做响应

- 使用AJAX和服务器进行通信，就可以使用HTML+AJAX来替换JSP页面了
- 实现前后端分离，前端HTML+AJAX 后端负责数据提交逻辑处理
- 异步交互：可以在不重新加载整个页面的情况下，与服务器交换数据，并更新部分网页的技术，如：搜索联想，用户名是否可用校验...

### AJAX快速入门

原生代码开发

1.  编写AjaxServlet，并使用response输出字符串
2.  创建XMLHttpRequest对象：用于和服务器交换数据
3.  var xhttp;
4.      if (window.XMLHttpRequest) {
5.          xhttp = new XMLHttpRequest();
6.      } else {
7.          _// code for IE6, IE5_
8.          xhttp = new ActiveXObject("Microsoft.XMLHTTP");
9.      }

10.  向服务器发送请求
11.  xhttp.open("GET", "http://localhost:8080/ajax-demo/ajaxServlet");
12.      xhttp.send();

写全路径

1.  获取服务器响应数据
2.      xhttp.onreadystatechange = function() {
3.          if (this.readyState == 4 && this.status == 200) {
4.                 alert(this.responseText);
5.          }
6.      };

readyState：保存了XMLhttpRequest的状态

0：请求未初始化

1：服务器连接已建立

2：请求已接收

3：正在处理请求

4：请求已完成且响应已就绪

### 案例

使用AJAX验证用户名是否存在

需求：在完成用户注册时，当用户名输入框失去焦点时，校验用户名是否在数据库已存在

SelectUserServlet.java

1.  @WebServlet("/selectUserServlet")
2.  public class SelectUserServlet extends HttpServlet {
3.      @Override
4.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

5.          _//1. 接收用户名_
6.          String username = request.getParameter("username");

7.          _//2. 调用service查询User对象_

8.         boolean flag = true;

9.         _//3. 响应标记_
10.         response.getWriter().write("" + flag);

11.     }

12.     @Override
13.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
14.         this.doGet(request, response);
15.     }
16. }

Register.html

在前面配置好静态页面

1.  <script>

2.      _//1. 给用户名输入框绑定 失去焦点事件_
3.      document.getElementById("username").onblur = function () {
4.          _//2. 发送ajax请求_
5.          _// 获取用户名的值_
6.          var username = this.value;

7.          _//2.1. 创建核心对象_
8.         var xhttp;
9.         if (window.XMLHttpRequest) {
10.             xhttp = new XMLHttpRequest();
11.         } else {
12.             _// code for IE6, IE5_
13.             xhttp = new ActiveXObject("Microsoft.XMLHTTP");
14.         }
15.         _//2.2. 发送请求_
16.         xhttp.open("GET", "http://localhost:8080/ajax-demo/selectUserServlet?username="+username);
17.         xhttp.send();

18.         _//2.3. 获取响应_
19.         xhttp.onreadystatechange = function() {
20.             if (this.readyState == 4 && this.status == 200) {
21.                 _//alert(this.responseText);_
22.                 _//判断_
23.                 if(this.responseText == "true"){
24.                     _//用户名存在，显示提示信息_
25.                     document.getElementById("username_err").style.display = '';
26.                 }else {
27.                     _//用户名不存在 ，清除提示信息_
28.                     document.getElementById("username_err").style.display = 'none';
29.                 }
30.             }
31.         };

32.     }
33. </script>

当用户名输入框失去焦点（绑定事件）时，校验用户名是否在数据库已存在

### Axios异步框架

Axios对原生的AJAX进行封装，简化书写

[Axios-中文](https://www.axios-http.cn/)

1.  引入axios的js文件

在webapp中创建一个js包，用来存放所有的js文件 这里存入axios源码

<script src="js/axios-0.18.0.js"></script>

1.  使用axios发送请求，并获取响应结果

AxiosServlet.java

1.  @WebServlet("/axiosServlet")
2.  public class AxiosServlet extends HttpServlet {
3.      @Override
4.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
5.          System.out.println("get...");

6.          _//1. 接收请求参数_
7.          String username = request.getParameter("username");
8.          System.out.println(username);

9.         _//2. 响应数据_
10.         response.getWriter().write("hello Axios~");
11.     }

12.     @Override
13.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
14.         System.out.println("post...");
15.         this.doGet(request, response);
16.     }
17. }

axios-demo.html

1.  <script>
2.      _//1. get_
3.      axios({
4.          method:"get",
5.          url:"http://localhost:8080/ajax-demo/axiosServlet?username=zhangsan"
6.      }).then(function (resp) {
7.          alert(resp.data);
8.      })

9.     _//2. post_
10.     axios({
11.         method:"post",
12.         url:"http://localhost:8080/ajax-demo/axiosServlet",
13.         data:"username=zhangsan"
14.     }).then(function (resp) {
15.         alert(resp.data);
16.     })

17. </script>

通过.then获取对应的响应，方法被执行时，resp就有响应数据

1.  Axios请求方式别名

Axios为所有支持的请求方法提供了别名

axios.get(url\[,config\])

axios.post(url\[.data\[,config\]\])

...

Get

1.  axios.get("http://localhost:8080/ajax-demo/axiosServlet?username=zhangsan").then(function (resp) {
2.      alert(resp.data);
3.  })

Post

1.  axios.post("http://localhost:8080/ajax-demo/axiosServlet","username=zhangsan").then(function (resp) {
2.      alert(resp.data);
3.  })

简化但是阅读性不如原生书写格式

1.  Axios复写AJAX验证用户名是否存在
2.  _// 给用户名输入框绑定失去焦点事件_
3.  document.getElementById("username").onblur = function () {
4.      _// 获取用户名的值_
5.      var username = this.value;

6.      _// 使用 axios 发送 GET 请求_
7.      axios.request({
8.          method: 'get',
9.         url: 'http://localhost:8080/ajax-demo/selectUserServlet?username=zhangsan',
10.     }).then(function (response) {
11.         _// 处理响应结果_
12.         if (response.data === "true") {
13.             _// 用户名存在，显示提示信息_
14.             document.getElementById("username_err").style.display = '';
15.         } else {
16.             _// 用户名不存在，隐藏提示信息_
17.             document.getElementById("username_err").style.display = 'none';
18.         }
19. }).

### JSON

- JavaScript Object Notation，JavaScript对象表示法
- 由于语法简单，层次结构鲜明，多用于数据载体，在网络中进行数据传输

#### JSON基础语法

1.  var 变量名 = {"key1":value1,
2.                "key2":value2,
3.               ...
4.                }

Value的数据类型：

- 数字（整数/浮点数）
- 字符串（在双引号中）
- 逻辑值（true/false）
- 数组（在方括号中）
- 对象（在花括号中）
- Null

获取数据：

变量名.key

Json.name

#### JSON数据和Java对象转换

请求数据：JSON字符串转为Java对象

响应数据：Java对象转为JSON字符串

- Fastjson：一个Java语言编写的高性能功能完善的JSON库，可以实现Java和JSON字符串的相互转换
- 使用：
    1.  导入坐标

1.  <dependency>
2.      <groupId>com.alibaba</groupId>
3.      <artifactId>fastjson</artifactId>
4.      <version>1.2.62</version>
5.  </dependency>

- 1.  Java对象转JSON

String jsonStr = JSON.toJSONString();

- 1.  JSON字符串转Java对象

User user = JSON.parseObject(jsonStr,User.class);

#### 案例

需求：完成品牌列表查询和添加

之前使用servlet + jsp完成品牌查询

##### 查询所有

使用Axios+JSON

1.  service层
2.      _/\*\*_
3.       \* 查询所有
4.       \* @return
5.       \*/
6.      public List<Brand> selectAll(){
7.          _//调用BrandMapper.selectAll()_

8.          _//2. 获取SqlSession_
9.         SqlSession sqlSession = factory.openSession();
10.         _//3. 获取BrandMapper_
11.         BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

12.         _//4. 调用方法_
13.         List<Brand> brands = mapper.selectAll();

14.         sqlSession.close();

15.         return brands;
16.     }

17.  Web层

SelectAllServlet.java

1.  @WebServlet("/selectAllServlet")
2.  public class SelectAllServlet extends HttpServlet {
3.      private BrandService brandService = new BrandService();

4.      @Override
5.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
6.          _//1. 调用Service查询_
7.          List<Brand> brands = brandService.selectAll();

8.         _//2. 将集合转换为JSON数据   序列化_
9.         String jsonString = JSON.toJSONString(brands);

10.         _//3. 响应数据，响应到对应页面上_
11.         response.setContentType("text/json;charset=utf-8");
12.         response.getWriter().write(jsonString);
13.     }

14.     @Override
15.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
16.         this.doGet(request, response);
17.     }
18. }

返回一个json数据 其中存放brand集合列表中的brands数据

Brand.html

1.  <script>
2.      _//1. 当页面加载完成后，发送ajax请求_
3.      window.onload = function () {
4.          _//2. 发送ajax请求_
5.          axios({
6.              method:"get",
7.              url:"http://localhost:8080/brand-demo/selectAllServlet"
8.          }).then(function (resp) {
9.              _//获取数据_
10.             let brands = resp.data;
11.             let tableData = " <tr>\\n" +
12.                 "        <th>序号</th>\\n" +
13.                 "        <th>品牌名称</th>\\n" +
14.                 "        <th>企业名称</th>\\n" +
15.                 "        <th>排序</th>\\n" +
16.                 "        <th>品牌介绍</th>\\n" +
17.                 "        <th>状态</th>\\n" +
18.                 "        <th>操作</th>\\n" +
19.                 "    </tr>";

20.             for (let i = 0; i < brands.length ; i++) {
21.                 let brand = brands\[i\];

22.                 tableData += "\\n" +
23.                     "    <tr align=\\"center\\">\\n" +
24.                     "        <td>"+(i+1)+"</td>\\n" +
25.                     "        <td>"+brand.brandName+"</td>\\n" +
26.                     "        <td>"+brand.companyName+"</td>\\n" +
27.                     "        <td>"+brand.ordered+"</td>\\n" +
28.                     "        <td>"+brand.description+"</td>\\n" +
29.                     "        <td>"+brand.status+"</td>\\n" +
30.                     "\\n" +
31.                     "        <td><a href=\\"#\\">修改</a> <a href=\\"#\\">删除</a></td>\\n" +
32.                     "    </tr>";
33.             }

34.           _// 设置表格数据_
35.           document.getElementById("brandTable").innerHTML = tableData;
36.         })
37.     }

通过resp接收数据brands，在brand中遍历数组brands，获得brand对象，将brand数据放到tr中，通过拼字符串的形式，对表格数据进行修改。

##### 新增品牌

resp 是 axios 发起的 HTTP 请求成功返回后，传递给 .then() 回调函数的响应对象。

具体说明如下：

resp 是 Response Object（响应对象），由 axios 提供。

它包含了服务器返回的所有信息，比如状态码、响应头和响应数据等。

常用属性包括：

resp.data: 实际从服务器返回的数据（通常是 JSON 格式）

resp.status: HTTP 状态码，如 200 表示请求成功。

resp.statusText: HTTP 状态描述，如 "OK"。

resp.headers: 响应头信息。

resp.config: 当前请求的配置信息。

addBrand.html

1.  <script>
2.      _//1. 给按钮绑定单击事件_
3.      document.getElementById("btn").onclick = function () {
4.          _// 将表单数据转为json_
5.          var formData = {
6.              brandName:"",
7.              companyName:"",
8.              ordered:"",
9.              description:"",
10.             status:"",
11.         };
12.         _// 获取表单数据_
13.         let brandName = document.getElementById("brandName").value;
14.         _// 设置数据_
15.         formData.brandName = brandName;

16.         _// 获取表单数据_
17.         let companyName = document.getElementById("companyName").value;
18.         _// 设置数据_
19.         formData.companyName = companyName;

20.         _// 获取表单数据_
21.         let ordered = document.getElementById("ordered").value;
22.         _// 设置数据_
23.         formData.ordered = ordered;

24.         _// 获取表单数据_
25.         let description = document.getElementById("description").value;
26.         _// 设置数据_
27.         formData.description = description;

28.         let status = document.getElementsByName("status");
29.         for (let i = 0; i < status.length; i++) {
30.             if(status\[i\].checked){
31.                 _//_
32.                 formData.status = status\[i\].value ;
33.             }
34.         }

35.         console.log(formData);
36.         _//2. 发送ajax请求_
37.         axios({
38.             method:"post",
39.             url:"http://localhost:8080/brand-demo/addServlet",
40.             data:formData
41.         }).then(function (resp) {
42.             _// 判断响应数据是否为 success_
43.             if(resp.data == "success"){
44.                 location.href = "http://localhost:8080/brand-demo/brand.html";
45.             }
46.         })
47.     }
48. </script>

增删改一般建议使用post的请求方式，var formdata操作是为了创建json对象

Console.log用于在控制台输出任何类型的信息

addServlet.java

1.  @WebServlet("/addServlet")
2.  public class AddServlet extends HttpServlet {

3.      private BrandService brandService = new BrandService();

4.      @Override
5.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

6.          _//1. 接收数据,request.getParameter 不能接收json的数据_
7.        _/\* String brandName = request.getParameter("brandName");_
8.         System.out.println(brandName);\*/

9.         _// 获取请求体数据_
10.         BufferedReader br = request.getReader();
11.         String params = br.readLine();

12.         _// 将JSON字符串转为Java对象_
13.         Brand brand = JSON.parseObject(params, Brand.class);

14.         _//2. 调用service 添加_
15.         brandService.add(brand);

16.         _//3. 响应成功标识_
17.         response.getWriter().write("success");
18.     }

19.     @Override
20.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
21.         this.doGet(request, response);
22.     }
23. }

Request.getParameter不能接收json数据，需要通过bufferreader来获取请求体数据，并把json字符转为java对象，使得json数据可以被add方法调用

application/x- www-form-urlencoded是Post请求默认的请求体内容类型，也是form表单默认的类型。[Servlet](https://so.csdn.net/so/search?q=Servlet&spm=1001.2101.3001.7020"%20\t%20"https://blog.csdn.net/qq_36719449/article/details/_blank) API规范中对该类型的请求内容提供了request.getParameter()方法来获取请求参数值。但当请求内容不是该类型时，需要调用request.getInputStream()或request.getReader()方法来获取请求内容值。

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

## Git

- 分布式版本控制系统
- 版本控制系统：集中式（SVN）/分布式（git）
- 集中式控制系统：所有文件保存在中央服务器，每个人的电脑上保存着副本，但需要修改时，首先要从中央服务器上下载最新的版本，然后添加修改内容，修改完成后再上传到中央服务器。缺点上单点故障问题，中央服务器的故障是致命的
- 分布式版本控制系统：每个人的设备上都有一个完整的版本库，但需要分享内容给其他人时，只需要同步仓库内容即可
- Git工作流程图

Clone（克隆）：从远程仓库中克隆代码到本地仓库

Checkout（检出）：从本地仓库中检出一个仓库分支然后进行修订

add（添加）: 在提交前先将代码提交到暂存区

commit（提交）: 提交到本地仓库。本地仓库中保存修改的各个历史版本

fetch (抓取) ： 从远程库，抓取到本地仓库，不进行任何的合并动作，一般操作比较少。

pull (拉取) ： 从远程库拉到本地库，自动进行合并(merge)，然后放到工作区，相当于

fetch+merge

push（推送） : 修改完成后，需要和团队成员共享代码时，将代码推送到远程仓库

- 简单Linux指令

ls/ll 查看当前目录

Cat 查看文件内容

Touch 创建文件

Vi vi编辑器

### 初始化配置

### 新建仓库

Repo-可以理解成目录，这个目录里所有的文件可以被git管理起来，每个文件的增删改操作都可以被Git跟踪到，以便任何时候都可以追踪历史或还原到之前的某一个版本

创建仓库的两种方式：

- Git init 在自己电脑本地直接创建一个仓库
- Git clone 从远程服务器上克隆一个已经存在的仓库

要使用Git对我们的代码进行版本控制，首先需要获得本地仓库

1）在电脑的任意位置创建一个空目录（例如test）作为我们的本地Git仓库

2）进入这个目录中，点击右键打开Git bash窗口

3）执行命令git init

4）如果创建成功后可在文件夹下看到隐藏的.git目录。

### Git的工作区域和文件状态

#### 工作区域

- 工作区 Work Directory 电脑上的目录，资源管理器中能看到的文件夹就是工作区，实际操作的目录
- 暂存区 Staging Area/Index 临时存储区域，用于保存即将提交到git仓库的修改内容，版本控制的重要区域
- 本地仓库 Local repository Git存储代码和版本信息的主要位置

git -add 可以将修改的文件先添加到暂存区中

git -commit 一次性地将暂存区文件运送到本地仓库

#### 文件状态

- 未跟踪 Untracked
- 未修改 Unmodified
- 已修改 modified
- 已暂存 Staged

### Git常用指令

1.  查看修改的状态（status）

作用：查看修改的状态（暂存区、工作区）

命令：git status

1.  添加工作区到暂存区（add）

作用：添加工作区一个或多个文件的修改到暂存区

命令形式：git add 单个文件名|通配符

将所有修改加入暂存区：git add .

1.  提交到暂存区到本地仓库（commit）

作用：提交到暂存区内容到本地仓库的当前分支

命令形式：git commit -m’注释内容’

1.  查看提交日志（log）

作用：查看提交记录

命令形式：git log\[option\]

Options：

\--all 显示所有分支

\--pretty=oneline 将提交信息显示为一行

\--abbrev-commit 使得输出的commitid更简短

\--graph 以图的形式显示

1.  版本回退

作用：版本切换

命令形式：git reset --hard commitID

commitID可以使用git-log 或git lo指令查看

使用HEAD表示当前版本，上一个版本就是HEAD~

回退到上一个版本git reset --hard HEAD^

- git reset --soft：回退到某一个版本，保留工作区和暂存区的所有内容
- git reset --hard：回退到某一个版本，丢弃工作区和暂存区的所有内容，一般决定放弃本地的所有修改内容时使用
- git reset --mixed：回退到某一个版本，只保留工作区的修改内容（reset的默认参数），执行get add 操作将变动过的内容重新添加到暂存区

查看已经删除的记录：git reflog

1.  gitignore文件

作用：一般我们总会有些文件无需纳入Git 的管理，也不希望它们总出现在未跟踪文件列表。 通常都是些自动生成的文件，比如日志文件，或者编译过程中创建的临时文件（字节码文件）等。 在这种情况下，我们可以在工作目录中创建一个名为 .gitignore 的文件（文件名称固定），列出要忽略的文件模式。

1.  _# no .a files_
2.   \*.a
3.   _# but do track lib.a, even though you're ignoring .a files above_
4.   !lib.a
5.   _# only ignore the TODO file in the current directory, not subdir/TODO_
6.   /TODO
7.   _# ignore all files in the build/ directory_
8.   build/
9.   _# ignore doc/notes.txt, but not doc/server/arch.txt_
10.  doc/\*.txt
11.  _# ignore all .pdf files in the doc/ directory_
12.  doc/\*\*/\*.pdf

### Git分支

几乎所有的版本控制系统都以某种形式支持分支。 使用分支意味着你可以把你的工作从开发主线上分离开来进行重大的Bug修改、开发新的功能，以免影响开发主线。

1.  查看本地分支

命令：git branch

1.  创建本地分支

命令：git branch 分支名

1.  切换分支（checkout）

命令：git checkout 分支名

还可以直接切换到一个不存在的分支（创建并切换）

命令：git checkout -b分支名

1.  合并分支（merge）

一个分支上的提交可以合并到另一个分支

命令：git merge 分支名称

1.  删除分支

不能删除当前分支，只能删除其他分支

git branch -d b1删除分支时，需要做各种检查

git branch -D b1 不做任何检查，强制删除

1.  解决冲突

当两个分支上对文件的修改可能会存在冲突，例如同时修改了同一个文件的同一行，这时就需要手动解决冲突，解决冲突步骤：

1\. 处理文件中冲突的地方

2\. 将解决完冲突的文件加入暂存区(add)

3\. 提交到仓库(commit)

1.  开发中分支使用原则与流程

在开发中，一般有如下分支使用原则与流程：

master （生产） 分支

线上分支，主分支，中小规模项目作为线上运行的应用对应的分支；

develop（开发）分支

是从master创建的分支，一般作为开发部门的主要开发分支，如果没有其他并行开发不同期上线要求，都可以在此版本进行开发，阶段开发完成后，需要合并到master分支,准备上线。

feature/xxxx分支从develop创建的分支，一般是同期并行开发，但不同期上线时创建的分支，分支上的研发任务完成后合并到develop分支。

hotfix/xxxx分支，

从master派生的分支，一般作为线上bug修复使用，修复完成后需要合并到master、test、

develop分支。

还有一些其他分支，在此不再详述，例如test分支（用于代码测试）、pre分支（预上线分支）

1.  _###########################创建并切换到dev01分支，在dev01分支提交_
2.  _# \[master\]创建分支dev01_
3.   git branch dev01
4.   _# \[master\]切换到dev01_
5.   git checkout dev01
6.   _# \[dev01\]创建文件file02.txt_
7.  略
8.  _# \[dev01\]将修改加入暂存区并提交到仓库,提交记录内容为：add file02 on dev_
9.   git add .
10.  git commit -m 'add file02 on dev'
11.  _# \[dev01\]以精简的方式显示提交记录_
12. git-log
13.  _###########################切换到master分支，将dev01合并到master分支_
14. _# \[dev01\]切换到master分支_
15. git checkout master
16.  _# \[master\]合并dev01到master分支_
17. git merge dev01
18.  _# \[master\]以精简的方式显示提交记录_
19. git-log
20.  _# \[master\]查看文件变化(目录下也出现了file02.txt)_
21. 略
22. _##########################删除dev01分支_
23. _# \[master\]删除dev01分支_
24. git branch -d dev01
25.  _# \[master\]以精简的方式显示提交记录_
26. git-log

### Git远程仓库

1.  配置SSH公钥

生成SSH公钥

ssh-keygen -t rsa

不断回车

如果公钥已经存在，则自动覆盖

Gitee设置账户共公钥

获取公钥 cat ~/.ssh/id_rsa.pub

1.  操作远程仓库
2.  添加远程仓库

此操作是先初始化本地库，然后与已创建的远程库连接

命令： git remote add <远端名称> <仓库路径>

远端名称，默认是origin，取决于远端服务器设置

仓库路径，从远端服务器获取此URL

例如: git remote add origin git@gitee.com:czbk_zhang_meng/git_test.git

1.  查看远程仓库

命令：git remote

1.  推送到远程仓库

命令：git push \[-f\] \[--set-upstream\] \[远端名称 \[本地分支名\]\[:远端分支名\] \]

- 如果远程分支名和本地分支名称相同，则可以只写本地分支

git push origin master

- \-f 表示强制覆盖
- \--set-upstream 推送到远端的同时并且建立起和远端分支的关联关系。

git push --set-upstream origin master

- 如果当前分支已经和远端分支关联，则可以省略分支名和远端名。

git push 将master分支推送到已关联的远端分支。

1.  本地分支与远程分支的关联关系

查看关联关系我们可以使用

git branch -vv命令

1.  从远程仓库克隆

如果已经有一个远端仓库，我们可以直接clone到本地。

命令: git clone <仓库路径> \[本地目录\] 指定一个名字

本地目录可以省略，会自动生成一个目录

1.  从远程仓库中抓取和拉取

远程分支和本地分支一样，我们可以进行merge操作，只是需要想把远端仓库里的更新都下载到本地，再进行操作

- 抓取 命令：git fetch \[remote name\] \[branch name\]

抓取指令就是将仓库里的更新都抓取到本地，不会进行合并

如果不指定远端名称和分支名，则抓取所有分支。

- 拉取命令：git pull \[remote name\] \[branch name\]

拉取指令就是将远端仓库的修改拉到本地并自动进行合并，等同于fetch+merge

如果不指定远端名称和分支名，则抓取所有并更新当前分支。

1.  解决合并冲突

在一段时间，A、B用户修改了同一个文件，且修改了同一行位置的代码，此时会发生合并冲突。 A用户在本地修改代码后优先推送到远程仓库，此时B用户在本地修订代码，提交到本地仓库后，也需要推送到远程仓库，此时B用户晚于A用户，故需要先拉取远程仓库的提交，经过合并后才能推送到远端分支,如下图所示。

### 在IDEA中使用Git

1.  创建项目远程仓库（gitee/github）
2.  初始化本地仓库，准备gitignore文件

选择git仓库目录，默认是当前项目的目录

1.  设置远程仓库

Mange remotes中输入远程仓库的地址

1.  提交到本地仓库

Commit

1.  推送到远程仓库

Push

1.  [在项目中解除idea与git的绑定](https://blog.csdn.net/m0_65992672/article/details/132338170)

# JavaWeb综合案例

完成品牌数据的增删改查，批量删除，分页查询，条件查询

前端Vue Element + 后端MyBatis servlet

## 查询所有

Mapper-brandMapper.java

1.      @Select("select \* from tb_brand")
2.      @ResultMap（"brandResultMap"）
3.      List<Brand> selectAll();

由于Brand实体类中的名称与数据库表中字段不匹配，需要使用resultMap进行映射

resourses-com-itheima-mapper-brandMapper.xml

1.  <mapper namespace="com.itheima.mapper.BrandMapper">
2.      <resultMap id="brandResultMap" type="brand">
3.          <result property="brandName" column="brand_name" />
4.          <result property="companyName" column="company_name" />
5.      </resultMap>
6.  </mapper>

service-BrandMapper.java

创建一个接口，在接口中写方法

1.  List<Brand> selectAll();

service-impl-brandServiceImpl

1.  public class brandServiceImpl implements BrandService {
2.      _//1.创建sqlSessionFactory_
3.      SqlSessionFactory sqlSessionFactory = SqlSessionFactoryUtils.getSqlSessionFactory();
4.      @Override
5.      public List<Brand> selectAll() {

6.          _//2.获取SqlSession对象_
7.          SqlSession sqlSession = sqlSessionFactory.openSession();    

8.         _//3.获取BrandMapper_
9.         BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

10.         List<Brand> brands = mapper.selectAll();

11. _//5.释放资源_
12. sqlSession.close();
13.         return brands;

14.     }
15. }

通过接口-实现类，通过一些框架设计web层和service层可以解耦合

web-SelectAllServlet

1.  @WebServlet("/selectAllServlet")
2.  public class SelectAllServlet {

3.      private BrandService brandService = new brandServiceImpl();

4.      protected void doGet(HttpServletRequest request, HttpServletResponse response)
5.              throws ServletException, IOException {

6.         _//1. 调用service查询_
7.         List<Brand> brands = brandService.selectAll();

8.         _//2.转为json_
9.         String jsonString = JSON.toJSONString(brands);   

10.         _//3.写数据_
11.         response.setContentType("text/json;charset=utf-8");
12.         response.getWriter().write(jsonString);
13.     }

14.     protected void doPost(HttpServletRequest request, HttpServletResponse response)
15.             throws ServletException, IOException {
16. this.doGet(request, response);
17.     }
18. }

关于测试：Tomcat启程序，访问selectAllservlet，看到一系列的json数据则后台接收数据无误

\--后台代码#end

brand.html

1.      new Vue({
2.          el: "#app",

3.          mounted() {
4.              _//当页面加载完成后，发送异步请求_

5.              var \_this = this;

6.              axios({
7.                 method: "get",
8.                 url: "http://localhost:8080/brand-case/selectAllServlet"
9.             }).then(function(resp) {

10.                 \_this.tableData = resp.data;
11.             })

12.         },
13. }

当页面加载完成时候，发送异步请求来获取数据

通过then回调，获取响应，绑定function函数，resp.data就是列表数据，传到表格数据的模型上，this不能直接使用，声明提高级别

\--前端代码#end

## 新增品牌

Mapper-BrandMapper.java

1.      @Insert("insert into tb_brand values (null,#{brandName},#{companyName},#{ordered},#{description},#{status})")
2.      void add(Brand brand);

service-BrandMapper.java

1.  void add(Brand brand);

service-impl-BrandServiceImpl

1.      @Override
2.      public void add(Brand brand) {

3.          _//2.获取SqlSession对象_
4.          SqlSession sqlSession = sqlSessionFactory.openSession();

5.          _//3.获取BrandMapper_
6.          BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

7.         mapper.add(brand);

8.         _//4.提交事务_
9.         sqlSession.commit();

10.         _//5.释放资源_
11.         sqlSession.close();

12.     }

web-AddServlet

1.  @WebServlet("/addServlet")
2.  public class AddServlet {

3.      private BrandService brandService = new brandServiceImpl();

4.      protected void doGet(HttpServletRequest request, HttpServletResponse response)
5.              throws ServletException, IOException {

6.        _//1.接收品牌数据_
7.         BufferedReader br = request.getReader();
8.         String params = br.readLine();_//json字符串_

9.         _//2.转为brand对象_
10.         Brand brand = JSON.parseObject(params, Brand.class);

11.         _//3.调用service添加_
12.         brandService.add(brand);

13.         _//4.响应结果_
14.         response.getWriter().write("success");
15.     }

16.     protected void doPost(HttpServletRequest request, HttpServletResponse response)
17.             throws ServletException, IOException {
18. this.doGet(request, response);
19.     }
20. }

数据以json格式提交，使用request.getReader来获取消息体数据

\--后端代码#end

1.              <el-form-item>
2.                  <el-button type="primary" @click="addBrand">提交</el-button>
3.                  <el-button @click="dialogVisible = false">取消</el-button>
4.              </el-form-item>

静态页面表单的案件绑定，将按钮绑定单击事件addBrand

brand.html

1.              addBrand(){
2.                  _//console.log(this.brand);_

3.                  var \_this = this;

4.                  _//发送ajax异步请求_
5.                  axios({
6.                     method: "post",
7.                     url: "http://localhost:8080/brand-case/addServlet",
8.                    data: \_this.brand

9.                 }).then(function (resp){

10.                     _//添加成功_
11.                     if(resp.data() == "success"){

12.                         _//关闭窗口_
13.                         \_this.dialogVisible = false;

14.                         _//重新查询数据_                        
15.                         \_this.selectAll();

16.                         \_this.$message({
17.                             message: '添加成功',
18.                             type: 'success'
19.                         });

20.                     }
21.                 })
22.             },
23.                 })
24.             },

为了方便调用selectAll来展示数据，直接将selectAll封装成一个方法

1.   mounted() {this.selectAll()；},

可以加入’添加成功’提示框功能

前端代码#end

#修改品牌

#删除品牌

## Servlet代码优化

- Web层的Servlet个数太多，不利于管理和编写
- 将Servlet进行归类，对于同一个实体的操作方法，写到一个Servlet中，比如BrandServlet，UserServlet
- 不能继承HttpServlet，自定义Servlet，使用请求路径进行方法分发，替换HttpServlet的根据请求方式进行方法分发

反射调用：

1.  _/\*\*_
2.   \* 替换HttpServlet，根据请求的最后一段路径来进行方法分发
3.   \*/
4.  public class BaseServlet extends HttpServlet {
5.      @Override
6.      protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
7.          _//1.获取请求路径_
8.         String uri = req.getRequestURI();_// /brand-case/brand/selectAll_

9.         _//2.获取最后一段路径，方法名_
10.         int index = uri.lastIndexOf('/');_//获取最后一个/的位置_
11.         String methodName = uri.substring(index + 1);

12.         _//3.获取BrandServlet/UserServlet 字节码对象 class_
13.         _//谁调用我（this所在的方法），我（this）调用谁，这里的this指BrandServlet(baseServlet的子类们)，而不是Httpservlet_
14.         Class<? extends BaseServlet> cls = this.getClass();

15.         _//获取方法Method对象_
16.         try {
17.             Method method = cls.getMethod(methodName, HttpServletRequest.class, HttpServletResponse.class);
18.             _//执行方法_
19.             method.invoke(this,req,resp);

20.         }catch (NoSuchMethodException e){
21.             e.printStackTrace();
22.         } catch (InvocationTargetException e) {
23.             throw new RuntimeException(e);
24.         } catch (IllegalAccessException e) {
25.             throw new RuntimeException(e);
26.         }
27.     }
28. }

一个通用的 HttpServlet 替代类，用于根据 URL 路径动态调用子类中的方法。继承自 HttpServlet。然后重写父类 service() 方法，处理所有 HTTP 请求（GET、POST 等）。参数：req: 封装了客户端的请求信息。resp: 用于向客户端发送响应。再获取当前请求的 URI。当访问 /brand-case/brand/selectAll 时，得到字符串 /brand-case/brand/selectAll。找到最后一个斜杠 / 的位置，并提取其后的内容作为方法名。uri.substring(index + 1) 得到 "selectAll"。获取当前对象的实际运行时类的 Class 对象。如果当前是 BrandServlet 实例，则返回 BrandServlet.class。使用反射获取名为 methodName 的方法对象，要求该方法接受两个参数：HttpServletRequest 和 HttpServletResponse。使用反射调用该方法，并传入当前请求和响应对象。

对此前写的代码进行优化

1.  @WebServlet("/brand/\*")
2.  public class BrandServlet {

3.      private BrandService brandService = new brandServiceImpl();

4.      public void selectAll(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {}

5.      public void add(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{}
6.  }

## 批量删除

Mapper-BrandMapper.java

1.      void deleteByIds(@Param("ids")int\[\] ids);

@Param("ids") 表示将方法参数 int\[\] ids 命名为 "ids"，以便在对应的 SQL 语句中引用。

当这个方法被调用时，传入的 ids 数组可以通过名称 "ids" 在 MyBatis 的 XML 映射文件或注解中的 SQL 语句里使用。

Resources-com-itheima-brandMapper.xml

1.      <delete id="delectByIds" >
2.          delete from tb_brand where in
3.          <foreach item="id" collection="ids" separator="," open="(" close=")">
4.              _#{id}_
5.          </foreach>
6.      </delete>

Sql语句复杂使用配置文件编写sql语句

service-BrandService.java

1.      void deleteByIds(int\[\] ids);

在接口中创建方法，接下来在实现类中实现该方法

service-BrandServiceImpl.java

1.      @Override
2.      public void deleteByIds(int\[\] ids) {

3.          _//2.获取SqlSession对象_
4.          SqlSession sqlSession = sqlSessionFactory.openSession();

5.          _//3.获取BrandMapper_
6.          BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

7.         mapper.deleteByIds(ids);

8.         _//4.提交事务_
9.         sqlSession.commit();

10.         _//5.释放资源_
11.         sqlSession.close();

12.     }

在实现类中调用方法

web-BrandServlet

1.      public void deleteByIds(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{

2.          _//1.接收id数组\[1,2,3\]_
3.          BufferedReader br = request.getReader();
4.          String params = br.readLine();_//json字符串_

5.          _//2.转为int数组_
6.          int\[\] ids = JSON.parseObject(params, int\[\].class);

7.         _//3.调用service添加_
8.         brandService.deleteByIds(ids);

9.         _//4.响应结果_
10.         response.getWriter().write("success");
11.     }

\--后端代码#end

brand.html

1.  <el-button type="danger" plain @click="deleteByIds">批量删除</el-button>

静态页面，按键绑定deleteByIds事件，实现批量删除

1.              deleteByIds(){
2.                  _//1.创建id数组\[1,2,3\]_
3.                  for (let i = 0; i < this.multipleSelection.length; i++) {
4.                      let selectionElements = this.multipleSelection\[i\];
5.                      this.selectedIds\[i\] = selectionElements.id;
6.                  }

7.                  _//2.发送ajax异步请求_
8.                  axiosaxios({
9.                     method: "post",
10.                     url: "http://localhost:8080/brand-case/deleteByIds",
11.                     data: \_this.deleteByIds

12.                 }).then(function (resp){

13.                     _//删除成功_
14.                     if(resp.data() == "success"){

15.                         _//重新查询数据_
16.                         \_this.selectAll();

17.                         \_this.$message({
18.                             message: '添加成功',
19.                             type: 'success'
20.                         });
21.                     }
22.                 })
23.             }

创建方法deleteByIds，从multipleSelection中获取数据，并通过遍历，将数据存储到自建的selectedIds模型中

在data中新建一个selectedIds模型 id被选中，数组值发生变化，提交数据时提交数组到后台

1.                  //被选中的id数组
2.                  selectedIds:\[\],

优化：在删除时跳出确认框，确认是否删除

1.              _//批量删除_
2.              deleteByIds(){
3.                  _// 弹出确认提示框_

4.                  this.$confirm('此操作将删除该数据, 是否继续?', '提示', {
5.                      confirmButtonText: '确定',
6.                      cancelButtonText: '取消',
7.                      type: 'warning'
8.                  }).then(() => {
9.                     _//用户点击确认按钮_

10.                     _//1. 创建id数组 \[1,2,3\], 从 this.multipleSelection 获取即可_
11.                     for (let i = 0; i < this.multipleSelection.length; i++) {
12.                         let selectionElement = this.multipleSelection\[i\];
13.                         this.selectedIds\[i\] = selectionElement.id;

14.                     }

15.                     _//2. 发送AJAX请求_
16.                     var \_this = this;

17.                     _// 发送ajax请求，添加数据_
18.                     axios({
19.                         method:"post",
20.                         url:"http://localhost:8080/brand-case/brand/deleteByIds",
21.                         data:\_this.selectedIds
22.                     }).then(function (resp) {
23.                         if(resp.data == "success"){
24.                             _//删除成功_

25.                             _// 重新查询数据_
26.                             \_this.selectAll();
27.                             _// 弹出消息提示_
28.                             \_this.$message({
29.                                 message: '恭喜你，删除成功',
30.                                 type: 'success'
31.                             });

32.                         }
33.                     })
34.                 }).catch(() => {
35.                     _//用户点击取消按钮_

36.                     this.$message({
37.                         type: 'info',
38.                         message: '已取消删除'
39.                     });
40.                 });

41.             }

用then catch包裹两种条件

\--前端代码#end

## 分页查询

- 分页查询LIMIT，参数1：开始索引，参数2：查询的条目数

SELECT \* FROM tb_brand LIMIT 0,5

- 页面（前端）传递的参数- 当前页码currentPage 与 每页查询的条目数pageSize
- 后台返回的数据- 当前页数据 List 与 总记录数 totalCount
- 开始索引 = （当前页数-1）\* 每页显示条数
- 查询条目数 = 查询的条目数 = 每页显示条数

Pojo-PageBean

1.  _//分页查询的JavaBean_
2.  public class PageBean<T> {
3.      _// 总记录数_
4.      private int totalCount;
5.      _// 当前页数据_
6.      private List<T> rows;

7.      public int getTotalCount() {
8.         return totalCount;
9.     }

10.     public void setTotalCount(int totalCount) {
11.         this.totalCount = totalCount;
12.     }

13.     public List<T> getRows() {
14.         return rows;
15.     }

16.     public void setRows(List<T> rows) {
17.         this.rows = rows;
18.     }
19. }

实体类中定义bean，泛型声明一个T，可以让代码通用，在pagebean中存放总记录数与当前页数据，并设置getter/setter方法

Mapper-BrandMapper.java

1.  _/\*\*_
2.       \* 分页查询
3.       \* @param begin
4.       \* @param size
5.       \* @return
6.       \*/
7.      @Select("select \* from tb_brand limit #{begin} , #{size}")
8.      @ResultMap("brandResultMap")
9.      List<Brand> selectByPage(@Param("begin") int begin,@Param("size") int size);

10.     _/\*\*_
11.      \* 查询总记录数
12.      \* @return
13.      \*/
14.     @Select("select count(\*) from tb_brand ")
15. @ResultMap("brandResultMap")
16.     int selectTotalCount();

BrandService.java

1.      _/\*\*_
2.       \* 分页查询
3.       \* @param currentPage  当前页码
4.       \* @param pageSize   每页展示条数
5.       \* @return
6.       \*/
7.      PageBean<Brand>  selectByPage(int currentPage,int pageSize);

返回一个Pagebean对象，由前端传入currentPage和pageSize

Service-impl-brandServiceImpl.java

1.  @Override
2.      public PageBean<Brand> selectByPage(int currentPage, int pageSize) {
3.          _//2. 获取SqlSession对象_
4.          SqlSession sqlSession = factory.openSession();
5.          _//3. 获取BrandMapper_
6.          BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

7.          _//4. 计算开始索引_
8.         int begin = (currentPage - 1) \* pageSize;
9.         _// 计算查询条目数_
10.         int size = pageSize;

11.         _//5. 查询当前页数据_
12.         List<Brand> rows = mapper.selectByPage(begin, size);

13.         _//6. 查询总记录数_
14.         int totalCount = mapper.selectTotalCount();

15.         _//7. 封装PageBean对象_
16.         PageBean<Brand> pageBean = new PageBean<>();
17.         pageBean.setRows(rows);
18.         pageBean.setTotalCount(totalCount);

19.         _//8. 释放资源_
20.         sqlSession.close();

21.         return pageBean;
22.     }

BrandServlet.java

1.  public void selectByPage(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
2.          _//1. 接收 当前页码 和 每页展示数    url?currentPage=1&pageSize=5_
3.          String \_currentPage = request.getParameter("currentPage");
4.          String \_pageSize = request.getParameter("pageSize");

5.          int currentPage = Integer.parseInt(\_currentPage);
6.          int pageSize = Integer.parseInt(\_pageSize);

7.          _//2. 调用service查询_
8.         PageBean<Brand> pageBean = brandService.selectByPage(currentPage, pageSize);

9.         _//2. 转为JSON_
10.         String jsonString = JSON.toJSONString(pageBean);
11.         _//3. 写数据_
12.         response.setContentType("text/json;charset=utf-8");
13.         response.getWriter().write(jsonString);
14.     }

请求中接收的类型是String类型，而查询中需要的为int类型，所以需要强制转换

后端代码#end

brand.html

1.              selectAll(){

2.                  var \_this = this;

3.                  axios( {
4.                      method: "post",
5.                      url: "http://localhost:8080/brand-case/brand/selectByPage?currentPage=" + \_this.currentPage + "&pageSize="+ \_this.pageSize,

6.                 }).then(function(resp){
7.                     \_this.tableData = resp.data.rows;
8.                     \_this.totalCount = resp.data.totalCount;
9.                     console.log(resp.data);
10.                 })

11.             },

因为修改分页查询，相当于修改了selectAll的显示方式，此前是加载完成之后就执行selectAll，这里url直接使用拼字符串的方式，将tableData模型数据设置成rows即当前页的数据，totalCount为页的数量，也建立到一个模型中。通过响应到的数据来为这两个模型设置值

在data中设置模型：pageSize，totalCount和currentPage其中5，100为默认值

1.                  _//每页显示的条数_
2.                  pageSize:5,
3.                  _//总记录数_
4.                  totalCount:100,
5.                  _// 当前页码_
6.                  currentPage: 1,

分页工具条

1.      <!--分页工具条-->
2.      <el-pagination
3.              @size-change="handleSizeChange"
4.              @current-change="handleCurrentChange"
5.              :current-page="currentPage"
6.              :page-sizes="\[5, 10, 15, 20\]"
7.              :page-size="5"
8.              layout="total, sizes, prev, pager, next, jumper"
9.              :total="totalCount">
10.     </el-pagination>

Total处展示总记录数，建立到totalCount模型中，@size-change，@current-change是动态分页的方法

动态分页

1.    _//分页_
2.              handleSizeChange(val) {
3.                  _// console.log(\`每页 ${val} 条\`);_
4.                  _//重新设置每页显示的条数_
5.                  this.pageSize = val;
6.                  this.selectAll();
7.              },
8.              handleCurrentChange(val) {
9.                  _//console.log(\`当前页: ${val}\`);_

10.                 _//重新设置当前页码_
11.                 this.currentPage = val;
12.                 this.selectAll();
13.             },

Val用来接收分页工具栏停留的位置，以及需要显示的数量

前端代码#end

## 条件查询

需要完成条件查询，并且按照分页的形式展示

BrandMapper.java

1.      _/\*\*_
2.       \* 分页条件查询
3.       \* @param begin
4.       \* @param size
5.       \* @return
6.       \*/
7.      List<Brand> selectByPageAndCondition(@Param("begin") int begin, @Param("size") int size, @Param("brand") Brand brand);

8.      _/\*\*_
9.      \* 根据条件查询总记录数
10.      \* @return
11.      \*/

12.     Integer selectTotalCountByCondition(Brand brand);

使用Integer即使查询结果为空，MyBatis 也能安全地返回 null，而不会引发类型不匹配异常

BrandMapper.xml

1.      <select id="selectByPageAndCondition" resultMap="brandResultMap">
2.          select \*
3.          from tb_brand
4.          <where>
5.          <if test=" brandName != null and  brandName ！=''">
6.              and brand_name like _#{ brandName}_
7.          </if>

8.          <if test=" companyName != null and  companyName ！=''">
9.             and company_name like _#{ companyName}_
10.         </if>

11.         <if test=" status != null ">
12.             and status = _#{ status}_
13.         </if>

14.         </where>

15.         limit _#{begin},#{size}_
16.     </select>

17.     <select id="selectTotalCountByCondition" resultMap="brandResultMap">
18.         select count(\*)
19.         from tb_brand
20.         <where>
21.             <if test=" brandName != null and  brandName ！=''">
22.                 and brand_name like _#{ brandName}_
23.             </if>

24.             <if test=" companyName != null and  companyName ！=''">
25.                 and company_name like _#{ companyName}_
26.             </if>

27.             <if test=" status != null ">
28.                 and status = _#{ status}_
29.             </if>

30.         </where>

31.     </select>

由于需要写动态SQL，所以在XML文件中编辑，第二个select语句中，由于没有采用@brand注解，可以直接使用brand实体类中的属性，所以可以省略brand. ，同时希望模糊匹配没使用like，而不是=

BrandService.java

1.  PageBean<Brand> selectByPageAndCondition(int currentPage, int pageSize, Brand brand);

分页条件查询，返回一个pageBean

BrandServiceImpl.java

1.      @Override
2.      public PageBean<Brand> selectByPageAndCondition(int currentPage, int pageSize, Brand brand) {

3.          _//2.获取SqlSession对象_
4.          SqlSession sqlSession = factory.openSession();

5.          _//3.获取BrandMapper_
6.          BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

7.         _//计算开始索引_
8.         int begin = (currentPage-1) \* pageSize;
9.         _//计算查询条目数_
10.         int size = pageSize;

11.         _//处理brand条件，模糊表达式_
12.         String brandName = brand.getBrandName();
13.         if(brandName != null && brandName.length() > 0){
14.             brand.setBrandName("%" + brandName + "%");
15.         }

16.         String companyName = brand.getCompanyName();
17.         if(companyName != null && companyName.length() > 0){
18.             brand.setCompanyName("%" + companyName + "%");
19.         }

20.         _//4.查询当前页数据_
21.         List<Brand> rows = mapper.selectByPageAndCondition(begin, size,brand);

22.         _//5.查询总记录数_
23.         int totalCount = mapper.selectTotalCountByCondition(brand);

24.         PageBean<Brand> pageBean = new PageBean<>();
25.         pageBean.setRows(rows);
26.         pageBean.setTotalCount(totalCount);

27.         sqlSession.close();

28.         return pageBean;
29.     }

新增处理brand对象，使模糊表达式，对用户的输入封装成模糊表达式的形式

BrandServlet.java

1.      public void selectByPageAndCondition(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
2.          _//1. 接收两个参数 currentPage pageSize_
3.          String \_currentPage = request.getParameter("currentPage");
4.          String \_pageSize = request.getParameter("pageSize");

5.          _//获取查询条件对象_
6.          BufferedReader br = request.getReader();
7.          String params = br.readLine();_//json字符串_

8.         Brand brand = JSON.parseObject(params, Brand.class);

9.         int currentPage = Integer.parseInt(\_currentPage);
10.         int pageSize = Integer.parseInt(\_pageSize);

11.         PageBean<Brand> pageBean = brandService.selectByPageAndCondition(currentPage, pageSize,brand);

12.         _//转为json_
13.         String json = JSON.toJSONString(pageBean);
14.         response.setContentType("text/json;charset=utf-8");
15.         response.getWriter().write(json);
16.     }

Brand的数据通过前端传递，将method改为post方式，使用data来传递，接收请求体的参数，currentPage和pageSize使用url来传递

后端代码#end

Brand.html

1.              _//查询所有_
2.              selectAll(){

3.                  var \_this = this;

4.                  axios( {
5.                      method: "post",
6.                      url: "http://localhost:8080/brand-case/brand/selectByPageAndCondition?currentPage=" + \_this.currentPage + "&pageSize="+ \_this.pageSize,
7.                      data:this.brand

8.                 }).then(function(resp){
9.                     \_this.tableData = resp.data.rows;
10.                     \_this.totalCount = resp.data.totalCount;
11.                     console.log(resp.data);
12.                 })

13.             },
14.             onSubmit() {
15.                 console.log(this.brand);
16.                 this.selectAll()
17.             },

将请求改为post形式，并使用data将brand传入selectAll中，查询按键绑定onSubmit事件，点击时调用selectAll方法

前端代码优化

Var \_this = this 使用麻烦

使用=>箭头函数，不用再使用_this

1.  axios({
2.                      method:"post",
3.                      url:"http://localhost:8080/brand-case/brand/selectByPageAndCondition?currentPage="+this.currentPage+"&pageSize="+this.pageSize,
4.                      data:this.brand
5.                  }).then(resp =>{
6.                      _//设置表格数据_
7.                      this.tableData = resp.data.rows; _// {rows:\[\],totalCount:100}_
8.                      _//设置总记录数_
9.                      this.totalCount = resp.data.totalCount;
10.                 })

\--前端代码#end

# SSM

Spring +SpringMVC +Mybatis

Dao=Mapper

domain=pojo

git clone git@github.com:CrRdz/Learning_SSM.git

## Spring

- Spring技术是JavaEE开发的必备技术，企业开发技术选型命中率>90%
- 简化开发，框架整合（MyBatis/Struts/Hibernate）
- Spring发展到今天已经形成一种开发生态圈，Spring提供若干个项目，每个项目用于完成特定的功能

### Spring Framework

Spring Framework是Spring生态中最基础的项目，是其他项目的根基

#### 系统架构

架构上层依赖于下层

底层：

Core Container 核心容器（beans Core Context SpEL）

中层：

AOP（面向切面编程）Aspects（AOP思想实现）

上层：

Data Access/Integration数据访问/集成（JDBC ORM OXM JMS Transaction事务）

Web Web开发（WebSocket Servlet Web Portlet）

#### 核心概念

- 代码书写现状：耦合度偏高

|

解决方案：使用对象时，在程序中不要主动使用new产生新对象，转换为由外部提供对象

数据层实现

1.  public class BookDaoImpl implements BookDao {
2.      public void save() {
3.          System.out.println("book dao save ...");
4.      }
5.  }

6.  public class BookDaoImpl2 implements BookDao {
7.      public void save() {
8.          System.out.println("book dao save ...2");
9.      }
10.  }

业务层实现

1.  public class BookServiceImpl implements BookService {
2.      private BookDao bookDao = new BookDaoImpl2;
3.      public void save() {
4.          bookDao.save();
5.      }
6.  }

如果数据层出现了一个新的实现类，因为业务层需要创建新的对象，BookDaoImpl改成BookDaoImpl2那么需要重新编译，重新部署...

那么不实现对象，就可以降低耦合

- IoC（Inversion of Control）控制反转：对象的创建控制权由程序转移到外部的思想

它将对象的创建和依赖关系的管理交给Spring框架，而不是在代码中手动创建对象。这种设计思想可以降低代码的耦合度，提高代码的可维护性和可测试性。

- Spring提供了一个IoC容器，用来充当IoC思想的外部

|

负责对象的创建，初始化等一系列工作

被IoC容器创建或管理的对象在IoC容器中统称为bean

- DI（Dependency Injection）依赖注入

|

在容器中建立bean与bean之间的依赖关系的整个过程（service依赖于dao 绑定service和dao）

- 目标：充分解耦

使用IoC容器管理bean（IoC）在容器中将有依赖关系的bean进行关系绑定（DI）使用对象时不仅可以直接从IoC容器中直接获取，并且获取到的bean已经绑定了所有依赖关系

#### 核心容器

##### IoC快速入门

- 管理Service与Dao
- 通过配置文件的方式将被管理的对象告知IoC容器
- 被管理的对象交给IoC通过接口获取到IoC容器
- IoC容器得到后，通过接口方法中获取bean

准备：

定义spring管理的类

导包spring-context 导入坐标

pom.xml

1.      <dependency>
2.        <groupId>org.springframework</groupId>
3.        <artifactId>spring-context</artifactId>
4.        <version>5.2.10.RELEASE</version>
5.      </dependency>

创建配置文件将被管理的对象告知IoC容器

resouse中创建spring.config配置文件xml 配置对应类作为Spring管理的bean

ApplicationContext.xml

1.      _<!--1.导入spring的坐标spring-context，对应版本是5.2.10.RELEASE-->_

2.      _<!--2.配置bean-->_
3.      _<!--bean标签标示配置bean_
4.      id属性标示给bean起名字
5.      class属性表示给bean定义类型-->
6.      <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"/>

7.      <bean id="bookService" class="com.itheima.service.impl.BookServiceImpl"/>

围堵标签或者空标签皆可

App2.java

获取IoC容器 初始化IoC容器，通过容器获取bean

1.  public class App2 {
2.      public static void main(String\[\] args) {
3.          _//3.获取IoC容器_
4.          ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
5.          _//4.获取bean（根据bean配置id获取）_
6.  _//        BookDao bookDao = (BookDao) ctx.getBean("bookDao");_
7.  _//        bookDao.save();_

8.          BookService bookService = (BookService) ctx.getBean("bookService");
9.         bookService.save();

10.     }
11. }

##### DI快速入门

- 基于IoC管理bean
- Service中使用new形式创建的Dao对象不保留
- Service中需要的Dao对象通过提供方法进入到Service中
- Service与Dao之间的关系用配置文件描述

BookServiceImpl.java

1.  public class BookServiceImpl implements BookService {
2.      _//5.删除业务层中使用new的方式创建的dao对象_
3.      private BookDao bookDao;

4.      public void save() {
5.          System.out.println("book service save ...");
6.          bookDao.save();
7.      }
8.      _//6.提供对应的set方法_
9.     public void setBookDao(BookDao bookDao) {
10.         this.bookDao = bookDao;
11.     }
12. }

applicationContext

1.      <bean id="bookService" class="com.itheima.service.impl.BookServiceImpl">
2.          _<!--7.配置server与dao的关系-->_
3.          _<!--property标签表示配置当前bean的属性_
4.          name属性表示配置哪一个具体的属性
5.          ref属性表示参照哪一个bean-->
6.          <property name="bookDao" ref="bookDao"/>
7.      </bean>

Ref-reference

Dao告知service关系 对service修改

Service中有个属性是bookDao 对应需要参照的对象bookDao（id）两个bookDao并不是一个

##### Bean-IoC

1.  Bean配置

- Bean基础配置
- Bean别名配置
- Bean作用范围配置

基础配置:

功能：定义Spring核心容器管理的对象

格式

1.  <beans>
2.      <bean/>
3.      <bean></bean>
4.  </beans>

属性列表:

Id：bean的id，使用容器可以通过id值获取对应的bean，在一个容器中id值唯一

Class：bean的类型，即配置的bean的全路径名

别名配置

1.      _<!--name:为bean指定别名，别名可以有多个，使用逗号，分号，空格进行分隔-->_
2.      <bean id="bookService" name="service service4 bookEbi" class="com.itheima.service.impl.BookServiceImpl">
3.          <property name="bookDao" ref="bookDao"/>
4.      </bean>

使用name属性配置 但还是建议使用id引用

Bean作用范围

1.      _<!--scope：为bean设置作用范围，可选值为单例singloton，非单例prototype-->_
2.      <bean id="bookDao" name="dao" class="com.itheima.dao.impl.BookDaoImpl" scope="prototype"/>

为了控制同一个bean是不是同一个bean对象，即是否为单例，同一个为单例

Singleton：单例（默认）

Prototype：非单例

为什么bean默认为单例？

\--因为希望对象是可以复用的

适合交给容器进行管理的bean

\-表现层对象

\-业务层对象

\-数据层对象

\-工具对象

不适合交给容器管理的bean

\-封装实体的域对象

1.  Bean实例化

- Bean如何创建
- Bean创建的三种形式

1.  提供可访问的构造方法

Bean本质上就是对象，创建bean使用构造方法完成

BookDaoImpl.java

1.  public class BookDaoImpl implements BookDao {

2.      public BookDaoImpl() {
3.          System.out.println("book dao constructor is running ....");
4.      }

5.      public void save() {
6.          System.out.println("book dao save ...");
7.      }
8. }

无参构造方法如果不存在，将抛出BeanCreationException

配置

1.  _<!--方式一：构造方法实例化bean-->_
2.  <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"/>

3.  通过静态工厂

现在不常用，一般为兼容早期遗留系统

AppForInstanceOrder.java

1.  public class AppForInstanceOrder {
2.      public static void main(String\[\] args) {
3.          _//通过静态工厂创建对象_

4.          ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");

5.          OrderDao orderDao = (OrderDao) ctx.getBean("orderDao");

6.          orderDao.save();

7.     }
8. }

OrderDaoFactory.java

1.  public class OrderDaoFactory {
2.      public static OrderDao getOrderDao(){
3.          System.out.println("factory setup....");
4.          return new OrderDaoImpl();
5.      }
6.  }

配置

1.      _<!--方式二：使用静态工厂实例化bean-->_
2.  <bean id="orderDao" class="com.itheima.factory.OrderDaoFactory" factory-method="getOrderDao"/>

Class是工厂类名，如果不加factory-method 那么配出来的bean是工厂的实例对象，还需要加上工厂内路径

1.  使用实例工厂

相对于静态工厂更为繁琐

1.  public class AppForInstanceUser {
2.      public static void main(String\[\] args) {
3.          _//创建实例工厂对象_
4.          UserDaoFactory userDaoFactory = new UserDaoFactory();
5.          _//通过实例工厂对象创建对象_
6.          UserDao userDao = userDaoFactory.getUserDao();
7.          userDao.save();
8.      }
9.  }

创建实例工厂对象，通过实例工厂对象创建对象

UserDaoFactory.java

1.  _//实例工厂创建对象_
2.  public class UserDaoFactory {
3.      public UserDao getUserDao(){
4.          return new UserDaoImpl();
5.      }
6.  }

配置

1.      _<!--方式三：使用实例工厂实例化bean-->_
2.  <bean id="userFactory" class="com.itheima.factory.UserDaoFactory"/>
3.  <bean id="userDao" factory-method="getUserDao" factory-bean="userFactory"/>

需要先造出工厂对象 工厂中的路径是getUserDao方法 工厂对象对应的bean使用工厂id

1.  使用factoryBean（方式C的变种）
2.  public class UserDaoFactoryBean implements FactoryBean<UserDao> {
3.      _//代替原始实例工厂中创建对象的方法_
4.      public UserDao getObject() throws Exception {
5.          return new UserDaoImpl();
6.      }

7.      public Class<?> getObjectType() {
8.          return UserDao.class;
9.     }
10. }

需要实现FactoryBean 泛型中写需要实例化的对象

配置

1.     _<!--方式四：使用FactoryBean实例化bean-->_
2.     <bean id="userDao" class="com.itheima.factory.UserDaoFactoryBean"/>

配置时更简单

默认的对象是单例的，通过override一个isSingleton方法 通过修改true-单例 和false-非单例切换，一般不用刻意书写

1.  Bean的生命周期

- 生命周期：从创建到消亡的完整过程
- Bean生命周期：bean从创建到销毁的整体过程

1.  初始化容器

创建对象（内存分配）-执行构造方法-执行属性注入（set操作）-执行bean初始化方法

1.  使用bean

执行业务操作

1.  关闭/销毁容器

执行bean销毁方法

- Bean生命周期控制：在bean创建到销毁前做一些事情

BookDaoImpl.java

1.  public class BookDaoImpl implements BookDao {
2.      public void save() {
3.          System.out.println("book dao save ...");
4.      }
5.      _//表示bean初始化对应的操作_
6.      public void init(){
7.          System.out.println("init...");
8.      }
9.      _//表示bean销毁前对应的操作_
10.     public void destory(){
11.         System.out.println("destory...");
12.     }

13. }

配置

1.      _<!--init-method：设置bean初始化生命周期回调函数-->_
2.      _<!--destroy-method：设置bean销毁生命周期回调函数，仅适用于单例对象-->_
3.      <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl" init-method="init" destroy-method="destory"/>

4.  public class AppForLifeCycle {
5.      public static void main( String\[\] args ) {
6.          ClassPathXmlApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");

7.          BookDao bookDao = (BookDao) ctx.getBean("bookDao");
8.          bookDao.save();
9.          _//注册关闭钩子函数，在虚拟机退出之前回调此函数，关闭容器_
10.          _//ctx.registerShutdownHook();_
11.          _//关闭容器_
12.         ctx.close();
13.     }
14. }

registerShutdownHook在虚拟机退出之前回调此函数关闭容器

Close相对更暴力

但实际开发中，关闭容器应伴随Tomcat

使用接口控制生命周期

1.  public class BookServiceImpl implements BookService, InitializingBean, DisposableBean {
2.      private BookDao bookDao;

3.      public void setBookDao(BookDao bookDao) {
4.          System.out.println("set .....");
5.          this.bookDao = bookDao;
6.      }

7.      public void save() {
8.         System.out.println("book service save ...");
9.         bookDao.save();
10.     }

11.     public void destroy() throws Exception {
12.         System.out.println("service destroy");
13.     }

14.     public void afterPropertiesSet() throws Exception {
15.         System.out.println("service init");
16.     }
17. }

这样可以省略配置文件中的init-method...

Bean销毁时机

容器关闭前触发bean的销毁

关闭容器方法：手工关闭容器/注册关闭钩子，在虚拟机退出前关闭容器再退出虚拟机

##### 依赖注入方式-DI

Dependency-Injection

- 向一个类中传递数据的方式：普通方法（set）/构造方法
- 依赖注入描述了在容器中建立Bean与bean之间依赖关系的过程，当处理数字或字符串时，需要区分类型，引用类型/简单类型（基本数据类型与String）
- 依赖注入方式：

Setter注入：简单类型/引用类型

构造器注入：简单类型/引用类型

1.  Setter注入

空参

- 引用类型

BookServiceImpl.java

1.  public class BookServiceImpl implements BookService{
2.      private BookDao bookDao;
3.      private UserDao userDao;
4.      _//setter注入需要提供要注入对象的set方法_
5.      public void setUserDao(UserDao userDao) {
6.          this.userDao = userDao;
7.      }
8.      _//setter注入需要提供要注入对象的set方法_
9.      public void setBookDao(BookDao bookDao) {
10.         this.bookDao = bookDao;
11.     }

12.     public void save() {
13.         System.out.println("book service save ...");
14.         bookDao.save();
15.         userDao.save();
16.     }
17. }

applicationContext

1.      _<!--注入引用类型-->_
2.      <bean id="bookService" class="com.itheima.service.impl.BookServiceImpl">
3.          _<!--property标签：设置注入属性-->_
4.          _<!--name属性：设置注入的属性名，实际是set方法对应的名称-->_
5.          _<!--ref属性：设置注入引用类型bean的id或name-->_
6.          <property name="bookDao" ref="bookDao"/>
7.          <property name="userDao" ref="userDao"/>
8.      </bean>

- 简单类型

BookDaoImpl.java

1.  public class BookDaoImpl implements BookDao {

2.      private String databaseName;
3.      private int connectionNum;
4.      _//setter注入需要提供要注入对象的set方法_
5.      public void setConnectionNum(int connectionNum) {
6.          this.connectionNum = connectionNum;
7.      }
8.      _//setter注入需要提供要注入对象的set方法_
9.     public void setDatabaseName(String databaseName) {
10.         this.databaseName = databaseName;
11.     }
12.     public void save() {
13.         System.out.println("book dao save ..."+databaseName+","+connectionNum);
14.     }
15. }

applicationContext

1.      _<!--注入简单类型-->_
2.      <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
3.          _<!--property标签：设置注入属性-->_
4.          _<!--name属性：设置注入的属性名，实际是set方法对应的名称-->_
5.          _<!--value属性：设置注入简单类型数据值-->_
6.          <property name="connectionNum" value="100"/>
7.          <property name="databaseName" value="mysql"/>
8.      </bean>

提供可访问的set方法

配置中使用property标签value属性注入简单类型数据

1.  构造器注入

- 引用类型

BookServiceImpl.java

1.  public class BookServiceImpl implements BookService{
2.      private BookDao bookDao;
3.      private UserDao userDao;

4.      public BookServiceImpl(BookDao bookDao, UserDao userDao) {
5.          this.bookDao = bookDao;
6.          this.userDao = userDao;
7.      }

8.     public void save() {
9.         System.out.println("book service save ...");
10.         bookDao.save();
11.         userDao.save();
12.     }
13. }

ApplicationContext

1.      <bean id="bookService" class="com.itheima.service.impl.BookServiceImpl">
2.          <constructor-arg name="userDao" ref="userDao"/>
3.          <constructor-arg name="bookDao" ref="bookDao"/>
4.      </bean>

- 简单类型

1.  public class BookDaoImpl implements BookDao {
2.      private String databaseName;
3.      private int connectionNum;

4.      public BookDaoImpl(String databaseName, int connectionNum) {
5.          this.databaseName = databaseName;
6.          this.connectionNum = connectionNum;
7.      }

8.     public void save() {
9.         System.out.println("book dao save ..."+databaseName+","+connectionNum);
10.     }
11. }

applicationContext

1.      <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
2.          <constructor-arg name="connectionNum" value="10"/>
3.          <constructor-arg name="databaseName" value="mysql"/>
4.      </bean>

5.  问题

耦合度高 applicationContext与BookDaoImpl耦合度高 如果形参名称更改，applicaton中constructor-arg中的name属性也要同步修改

1.  _<!--解决形参名称的问题，与形参名不耦合 根据构造方法类型注入-->_
2.  <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
3.          <constructor-arg type="int" value="10"/>
4.          <constructor-arg type="java.lang.String" value="mysql"/>
5.  </bean>

6.  _<!--解决参数类型重复问题，使用位置解决参数匹配-->_
7.      <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
8.          _<!--根据构造方法参数位置注入-->_
9.          <constructor-arg index="0" value="mysql"/>
10.          <constructor-arg index="1" value="100"/>
11.      </bean>

12.  依赖注入方式选择

- 强制依赖使用构造器，使用setter注入有概率不进行注入导致null对象出现
- 可选依赖使用setter注入进行，灵活性强
- Spring框架倡导使用构造器，第三方内部大多数采用构造器注入的形式进行数据初始化，相对严谨
- 如果有必要可以两者同时使用，使用构造器注入完成强制依赖注入，使用setter注入完成可选依赖注入
- 实际开发中还需要根据实际情况分析，如果受控对象没有提供setter方法就必须使用构造器注入
- 自己开发的模块推荐使用setter注入

##### 依赖自动装配

IoC容器根据bean所依赖的资源在容器中自动查找并注入bean中的过程称为自动装配

自动装配方式：按类型/按名称/按构造方法/不启用自动装配

1.  <bean id="bookDao" class="com.itheima.service.impl.BookDaoImpl" />
2.  _<!--autowire属性：开启自动装配，通常使用按类型装配-->_
3.  <bean id="bookService" class="com.itheima.service.impl.BookServiceImpl" autowire="byType"/>

按类型装配时，bean对象需唯一 连id都可以省略

如果有两个实现类-按名称装配，但是耦合度高

- 依赖自动装配特征

1.  自动装配用于引用类型依赖注入，不能对简单类型进行操作
2.  使用按类型装配时必须保障容器中相同类型的bean唯一推荐使用
3.  使用按名称装配时必须保障容器中具有指定名称的bean，变量名与配置名耦合高
4.  自动装配优先级低于setter注入与构造器注入，同时出现时自动装配配置失效

##### 集合注入

数组/List/Set/Map/Properties

1.  public class BookDaoImpl implements BookDao {

2.      private int\[\] array;
3.      private List<String> list;
4.      private Set<String> set;
5.      private Map<String,String> map;
6.      private Properties properties;

7.      public void setArray(int\[\] array) {
8.         this.array = array;
9.     }
10.     public void setList(List<String> list) {
11.         this.list = list;
12.     }
13.     public void setSet(Set<String> set) {
14.         this.set = set;
15.     }
16.     public void setMap(Map<String, String> map) {
17.         this.map = map;
18.     }
19.     public void setProperties(Properties properties) {
20.         this.properties = properties;
21.     }
22.     public void save() {
23.         System.out.println("book dao save ...");
24.         System.out.println("遍历数组:" + Arrays.toString(array));
25.         System.out.println("遍历List" + list);
26.         System.out.println("遍历Set" + set);
27.         System.out.println("遍历Map" + map);
28.         System.out.println("遍历Properties" + properties);
29.     }
30. }

配置

1.  <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
2.          _<!--数组注入-->_
3.          <property name="array">
4.              <array>
5.                  <value>100</value>
6.                  <value>200</value>
7.                  <value>300</value>
8.              </array>
9.          </property>
10.         _<!--list集合注入-->_
11.         <property name="list">
12.             <list>
13.                 <value>itcast</value>
14.                 <value>itheima</value>
15.                 <value>boxuegu</value>
16.                 <value>chuanzhihui</value>
17.             </list>
18.         </property>
19.         _<!--set集合注入-->_
20.         <property name="set">
21.             <set>
22.                 <value>itcast</value>
23.                 <value>itheima</value>
24.                 <value>boxuegu</value>
25.                 <value>boxuegu</value>
26.             </set>
27.         </property>
28.         _<!--map集合注入-->_
29.         <property name="map">
30.             <map>
31.                 <entry key="country" value="china"/>
32.                 <entry key="province" value="henan"/>
33.                 <entry key="city" value="kaifeng"/>
34.             </map>
35.         </property>
36.         _<!--Properties注入-->_
37.         <property name="properties">
38.             <props>
39.                 <prop key="country">china</prop>
40.                 <prop key="province">henan</prop>
41.                 <prop key="city">kaifeng</prop>
42.             </props>
43.         </property>
44.     </bean>

注：

Set如果重复会自动过滤

Array与list能混用

<ref bean = “beanId’’> 如果使用引用类型

##### 案例：数据源对象管理

导入坐标

配置数据源对象作为spring管理的bean

管理第三方数据连接池

1.  _<!--    管理DruidDataSource对象-->_
2.     <bean id ="dataSouce" class="com.alibaba.druid.pool.DruidDataSource">
3.          <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
4.          <property name="url" value="jdbc:mysql://localhost:3306/spring_db"/>
5.          <property name="username" value="root"/>
6.          <property name="password" value="root"/>
7.     </bean>

管理c3p0

1.      <bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource">
2.          <property name="driverClass" value="com.mysql.jdbc.Driver"/>
3.          <property name="jdbcUrl" value="jdbc:mysql://localhost:3306/spring_db"/>
4.          <property name="user" value="root"/>
5.          <property name="password" value="root"/>
6.          <property name="maxPoolSize" value="1000"/>
7.      </bean>

使用setter注入

##### 加载properties文件

1.  <beans xmlns="http://www.springframework.org/schema/beans"
2.         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
3.         xmlns:context="http://www.springframework.org/schema/context"
4.         xsi:schemaLocation="
5.              http://www.springframework.org/schema/beans
6.              http://www.springframework.org/schema/beans/spring-beans.xsd
7.              http://www.springframework.org/schema/context
8.              http://www.springframework.org/schema/context/spring-context.xsd
9.              ">
10. 开启一个全新的context命名空间
11. 使用context空间加载properties文件
12. 使用属性占位符${}读取properties文件中的属性
13. <context:property-placeholder location="jdbc.properties">
14.     <bean class="com.alibaba.druid.pool.DruidDataSource">
15.         <property name="driverClassName" value="${jdbc.driver}"/>
16.         <property name="url" value="${jdbc.url}"/>
17.         <property name="username" value="${jdbc.username}"/>
18.         <property name="password" value="${jdbc.password}"/>
19.     </bean>

不加载系统变量system-properties-mode="NEVER"

加载多个properties使用通配符

Classpath\*表示不仅可以从当前目录读取也可以读取框架中jar包，设置加载当前工程类路径和当前工程所依赖的所有jar包中的所有properties文件

1.  <context:property-placeholder location="classpath\*:\*.properties" system-properties-mode="NEVER"/>

##### 容器补充

- 创建容器
- 方式一：类路径加载配置文件
- 方式二：文件路径加载配置文件
- 获取bean
- 方式一：使用bean名称获取，强转
- 方式二：使用bean名称获取并指定类型
- 方式三：使用bean类型获取，容器中这个类型的bean只能有一个

1.  public class App {
2.      public static void main(String\[\] args) {
3.          _//1.加载类路径下的配置文件_
4.          ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
5.          _//2.从文件系统下加载配置文件_
6.  _//        ApplicationContext ctx = new FileSystemXmlApplicationContext("D:\\\\workspace\\\\spring\\\\spring_10_container\\\\src\\\\main\\\\resources\\\\applicationContext.xml");_
7.  _//        BookDao bookDao = (BookDao) ctx.getBean("bookDao");_
8.  _//        BookDao bookDao = ctx.getBean("bookDao",BookDao.class);_
9.  _//        BookDao bookDao = ctx.getBean(BookDao.class);_
10. _//        bookDao.save();_
11.     }
12. }

- 容器类层次结构

顶层接口beanFactory

- BeanFactory

1.  _//初始化BeanFactory_
2.  public class AppForBeanFactory {
3.      public static void main(String\[\] args) {
4.          Resource resources = new ClassPathResource("applicationContext.xml");
5.          BeanFactory bf = new XmlBeanFactory(resources);
6.  _//        BookDao bookDao = bf.getBean(BookDao.class);_
7.  _//        bookDao.save();_
8.      }
9.  }

Beanfactory与applicationContext加载bean的实际不一样，beanFactory是延迟加载bean（懒汉），application是立即加载bean（饿汉）

1.  <bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl" lazy-init="true"/>

在配置文件中加入这一行，也可以使application延迟加载

##### 核心容器总结

1.  容器相关

BeanFactory是IoC的顶层接口，初始化BeanFactory对象时，加载的bean延迟加载

ApplicationContext接口是Spring容器的核心接口，初始化bean立即加载

ApplicationContext接口提供基础的bean操作相关方法，通过其他接口扩展其功能

ApplicationContext接口常用初始化类：

ClassPathXmlApplicationContext，FileSystemXmlApplicationContext

1.  Bean相关

Bean的id

Bean别名

Bean类型，静态工厂类，factoryBean类

控制bean的实例数量

生命周期初始化方法

生命周期销毁方法

自动装配类型

Bean工厂方法，应用于静态工厂或实例工厂

实例工厂bean

控制bean延迟加载

1.  依赖注入相关

构造器注入引用类型

构造器注入简单类型

类型匹配与索引匹配

Setter注入引用类型

Setter注入简单类型

List集合

集合注入简单类型

集合注入引用类型

#### 注解开发

##### 注解开发定义bean

使用@Component定义bean

1.  _//@Component定义bean_
2.  @Component("bookDao")
3.  public class BookDaoImpl implements BookDao {
4.      public void save() {
5.          System.out.println("book dao save ...");
6.      }
7.  }

8.  _//@Component定义bean_
9.  @Component
10.  public class BookServiceImpl implements BookService {
11.      private BookDao bookDao;

12.      public void setBookDao(BookDao bookDao) {
13.          this.bookDao = bookDao;
14.      }

15.     public void save() {
16.         System.out.println("book service save ...");
17.         bookDao.save();
18.     }
19. }

Component可以指定名称理解成id

核心配置文件中通过组件扫描加载bean

1.  <context:component-scan base-package="com.itheima"/>

Spring提供@Component注解的三个衍生注解，功能完全一致，方便理解

业务层@Service

数据层@Repository

表现层@Controller

##### 纯注解开发

- Spring3.0升级了纯注解开发模式，使用java类替代配置文件，开启Spring快速开发赛道
- 读取Spring核心配置文件初始化容器对象切换为Java配置类初始化容器对象

新建config包下建SpringConfig类

1.  _//声明当前类为Spring配置类_
2.  @Configuration
3.  _//设置bean扫描路径，多个路径书写为字符串数组格式_
4.  @ComponentScan({"com.itheima.service","com.itheima.dao"})
5.  public class SpringConfig {
6.  }

作用完全替代：applicationContext

@ComponentScan注解用于设定扫描路径，此诸结只能添加一次，多个数据用数组格式

修改：

ApplicationContext ctx = new AnnotationConfigApplicationContext(SpringConfig.class);

1.  public class AppForAnnotation {
2.      public static void main(String\[\] args) {
3.          _//AnnotationConfigApplicationContext加载Spring配置类初始化Spring容器_
4.          ApplicationContext ctx = new AnnotationConfigApplicationContext(SpringConfig.class);
5.          BookDao bookDao = (BookDao) ctx.getBean("bookDao");
6.          System.out.println(bookDao);
7.          _//按类型获取bean_
8.          BookService bookService = ctx.getBean(BookService.class);
9.          System.out.println(bookService);
10.     }
11. }

##### Bean管理

1.  bean作用范围
2.  @Repository
3.  _//@Scope设置bean的作用范围_
4.  @Scope("singleton")
5.  public class BookDaoImpl implements BookDao {

6.      public void save() {
7.          System.out.println("book dao save ...");
8.      }
9. }

10.  Bean生命周期
11.      _//@PostConstruct设置bean的初始化方法_
12.      @PostConstruct
13.      public void init() {
14.          System.out.println("init ...");
15.      }
16.      _//@PreDestroy设置bean的销毁方法_
17.      @PreDestroy
18.      public void destroy() {
19.         System.out.println("destroy ...");
20.     }

##### 依赖注入

自动装配

1.  @Service
2.  public class BookServiceImpl implements BookService {
3.      _//@Autowired：注入引用类型，自动装配模式，默认按类型装配_
4.      @Autowired
5.      private BookDao bookDao;
6.      public void save() {
7.          System.out.println("book service save ...");
8.          bookDao.save();
9.      }
10. }

可以去除setter注入，直接使用Autowired注解，自动装配基于反射设计创建对象并暴力反射对应属性为私有属性初始化数据

自动装配建议使用无参构造方法创建对象

当有两个实现类时候，按名称注入 开启指定名称装配bean

1.  _//@Qualifier：自动装配bean时按bean名称装配_
2.  @Qualifier("bookDao")

但是这个注解必须依赖@Autowired

注入简单类型

1.  @Repository("bookDao")
2.  public class BookDaoImpl implements BookDao {
3.      _//@Value：注入简单类型（无需提供set方法）_
4.      @Value("${name}")
5.      private String name;

6.      public void save() {
7.          System.out.println("book dao save ..." + name);
8.      }
9. }

配置文件

1.  @Configuration
2.  @ComponentScan("com.itheima")
3.  _//@PropertySource加载properties配置文件_
4.  @PropertySource({"jdbc.properties"})
5.  public class SpringConfig {
6.  }

写多个properties配置文件，使用数组

@PropertySource({"jdbc.properties","jdbc.properties","jdbc.properties"})

这里不支持通配符，仅支持单一文件配置

##### 第三方bean管理

1.  第三方bean管理
2.  public class SpringConfig {
3.      _//1.定义一个方法获得要管理的对象_
4.      _//2.添加@Bean，表示当前方法的返回值是一个bean_
5.      _//@Bean修饰的方法，形参根据类型自动装配_
6.      @Bean
7.      public DataSource dataSource(BookDao bookDao){

8.          DruidDataSource ds = new DruidDataSource();
9.         ds.setDriverClassName("com.mysql.jdbc.Driver");
10.         ds.setUrl("jdbc:mysql://localhost:3306/spring_db");
11.         ds.setUsername("root");
12.         ds.setPassword("root");
13.         return ds;
14.     }
15. }

16.  public class App {
17.      public static void main(String\[\] args) {
18.          AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(SpringConfig.class);
19.          DataSource dataSource = ctx.getBean(DataSource.class);
20.          System.out.println(dataSource);
21.      }
22.  }

问题：耦合度高

解决：新建jdbc.config

1.  @Configuration配置JdbcConfig
2.  @Configuration
3.  public class JdbcConfig {
4.      _//1.定义一个方法获得要管理的对象_
5.      _//2.添加@Bean，表示当前方法的返回值是一个bean_
6.      _//@Bean修饰的方法，形参根据类型自动装配_
7.      @Bean
8.      public DataSource dataSource(BookDao bookDao){

9.         DruidDataSource ds = new DruidDataSource();
10.         ds.setDriverClassName("com.mysql.jdbc.Driver");
11.         ds.setUrl("jdbc:mysql://localhost:3306/spring_db");
12.         ds.setUsername("root");
13.         ds.setPassword("root");
14.         return ds;
15.     }
16. }

扫描config

1.  @Configuration
2.  @ComponentScan("com.itheima.config")
3.  public class SpringConfig {
4.  }

问题：不知道导入的是哪个配置，如果配置文件很多时

1.  Import
2.  @Configuration
3.  @ComponentScan("com.itheima")
4.  _//@Import:导入配置信息_
5.  @Import({JdbcConfig.class})
6.  public class SpringConfig {
7.  }

并取消@Configuration配置jdbc

1.  第三方bean依赖注入

简单类型注入

1.  public class JdbcConfig {
2.      _//1.定义一个方法获得要管理的对象_
3.      @Value("com.mysql.jdbc.Driver")
4.      private String driver;
5.      @Value("jdbc:mysql://localhost:3306/spring_db")
6.      private String url;
7.      @Value("root")
8.      private String userName;
9.      @Value("root")
10.     private String password;
11.     _//2.添加@Bean，表示当前方法的返回值是一个bean_
12.     _//@Bean修饰的方法_
13.     @Bean
14.     public DataSource dataSource(){
15.         DruidDataSource ds = new DruidDataSource();
16.         ds.setDriverClassName(driver);
17.         ds.setUrl(url);
18.         ds.setUsername(userName);
19.         ds.setPassword(password);
20.         return ds;
21.     }
22. }

引用类型注入

1.      _//@Bean修饰的方法，形参根据类型自动装配_
2.      @Bean
3.      public DataSource dataSource(BookDao bookDao){
4.          System.out.println(bookDao);
5.          DruidDataSource ds = new DruidDataSource();
6.          ds.setDriverClassName(driver);
7.          ds.setUrl(url);
8.          ds.setUsername(userName);
9.          ds.setPassword(password);
10.         return ds;
11.     }
12. }

放在形参列表中，按类型自动装配

##### 注解开发总结

XML配置vs注解开发

<div class="joplin-table-wrapper"><table><tbody><tr><td><p>功能</p></td><td><p>XML配置</p></td><td><p>注解</p></td></tr><tr><td><p>定义bean</p></td><td><p>Bean标签</p><ul><li>Id属性</li><li>Class属性</li></ul></td><td><p>@Component</p><p>@Controller</p><p>@Service</p><p>@Repository</p><p>@ComponentScan</p></td></tr><tr><td><p>设置依赖注入</p></td><td><p>Setter注入</p><p>构造器注入</p><p>自动装配</p></td><td><p>@Autowired</p><p>@Qualifier</p><p>@Value</p></td></tr><tr><td><p>配置第三方bean</p></td><td><p>Bean标签</p><p>静态工厂，实例工厂，FactoryBean</p></td><td><p>@Bean</p></td></tr><tr><td><p>作用范围</p></td><td><p>Scope属性</p></td><td><p>@scope</p></td></tr><tr><td><p>生命周期</p></td><td><p>标准接口</p><ul><li>init-method</li><li>destory-method</li></ul></td><td><p>@PostConstructor</p><p>@PreDestory</p></td></tr></tbody></table></div>

#### 整合

##### Spring整合MyBatis

1.  MyBatis核心流程分析
2.          _// 1. 创建SqlSessionFactoryBuilder对象_
3.          SqlSessionFactoryBuilder sqlSessionFactoryBuilder = new SqlSessionFactoryBuilder();
4.          _// 2. 加载SqlMapConfig.xml配置文件_
5.          InputStream inputStream = Resources.getResourceAsStream("SqlMapConfig.xml.bak");
6.          _// 3. 创建SqlSessionFactory对象_
7.          SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(inputStream);
8.          _// 4. 获取SqlSession_
9.          SqlSession sqlSession = sqlSessionFactory.openSession();
10.         _// 5. 执行SqlSession对象执行查询，获取结果User_
11.        AccountDao accountDao = sqlSession.getMapper(AccountDao.class);

12.         _// 6. 释放资源_
13.         sqlSession.close();

初始化SqlSessionFactory - 获取连接，获取实现 - 获取数据层接口 - 关闭连接

核心对象：SqlSessionFactory

SqlMapConfig

1.  <configuration>
2.      <properties resource="jdbc.properties"></properties>
3.      <typeAliases>
4.          <package name="com.itheima.domain"/>
5.      </typeAliases>
6.      <environments default="mysql">
7.          <environment id="mysql">
8.              <transactionManager type="JDBC"></transactionManager>
9.              <dataSource type="POOLED">
10.                 <property name="driver" value="${jdbc.driver}"></property>
11.                 <property name="url" value="${jdbc.url}"></property>
12.                 <property name="username" value="${jdbc.username}"></property>
13.                 <property name="password" value="${jdbc.password}"></property>
14.             </dataSource>
15.         </environment>
16.     </environments>
17.     <mappers>
18.         <package name="com.itheima.dao"></package>
19.     </mappers>
20. </configuration>

整合MyBatis

初始化属性数据 - 初始化类别别名 - 初始化dataSource - 初始化映射配置

1.  整合MyBatis

准备：

额外导包

1.      <dependency>
2.        <groupId>org.springframework</groupId>
3.        <artifactId>spring-jdbc</artifactId>
4.        <version>5.2.10.RELEASE</version>
5.      </dependency>

6.      <dependency>
7.        <groupId>org.mybatis</groupId>
8.        <artifactId>mybatis-spring</artifactId>
9.       <version>1.3.0</version>
10.     </dependency>

SpringConfig

1.  @Configuration
2.  @ComponentScan("com.itheima")
3.  _//@PropertySource：加载类路径jdbc.properties文件_
4.  @PropertySource("classpath:jdbc.properties")
5.  @Import({JdbcConfig.class,MybatisConfig.class})
6.  public class SpringConfig {
7.  }

JdbcConfig

1.  public class JdbcConfig {
2.      @Value("${jdbc.driver}")
3.      private String driver;
4.      @Value("${jdbc.url}")
5.      private String url;
6.      @Value("${jdbc.username}")
7.      private String userName;
8.      @Value("${jdbc.password}")
9.      private String password;

10.     @Bean
11.     public DataSource dataSource(){
12.         DruidDataSource ds = new DruidDataSource();
13.         ds.setDriverClassName(driver);
14.         ds.setUrl(url);
15.         ds.setUsername(userName);
16.         ds.setPassword(password);
17.         return ds;
18.     }
19. }

准备#end

在SqlMapConfig中的所有操作都是为了SqlSessionFactory准备

所以要在SqlSessionFactorybean中管理

1.  public class MybatisConfig {
2.      _//定义bean，SqlSessionFactoryBean，用于产生SqlSessionFactory对象_
3.      @Bean
4.      public SqlSessionFactoryBean sqlSessionFactory(DataSource dataSource){
5.          SqlSessionFactoryBean ssfb = new SqlSessionFactoryBean();
6.          ssfb.setTypeAliasesPackage("com.itheima.domain");
7.          ssfb.setDataSource(dataSource);
8.          return ssfb;
9.      }
10.     _//定义bean，返回MapperScannerConfigurer对象_
11.     @Bean
12.     public MapperScannerConfigurer mapperScannerConfigurer(){
13.         MapperScannerConfigurer msc = new MapperScannerConfigurer();
14.         msc.setBasePackage("com.itheima.dao");
15.         return msc;
16.     }
17. }

完全替代

1.      <typeAliases>
2.          <package name="com.itheima.domain"/>
3.      </typeAliases>
4.      <environments default="mysql">
5.          <environment id="mysql">
6.              <transactionManager type="JDBC"></transactionManager>
7.              <dataSource type="POOLED">
8.                  <property name="driver" value="${jdbc.driver}"></property>
9.                  <property name="url" value="${jdbc.url}"></property>
10.                 <property name="username" value="${jdbc.username}"></property>
11.                 <property name="password" value="${jdbc.password}"></property>
12.             </dataSource>
13.         </environment>
14.     </environments>
15.     <mappers>
16.         <package name="com.itheima.dao"></package>
17.     </mappers>

只需要配置不是默认的部分

2.Line1-3对应1.Line6

2.Line15-17对应1.Line14

1.Line7使用形参注入引用类型，引用JdbcConfig中的dataSouce （bean）

1.      <mappers>
2.          <package name="com.itheima.dao"></package>
3.      </mappers>

对于这一段与SqlSession不是一体的，SqlSessionFactoryBean只负责造出SqlSession

##### Spring整合JUnit

src\\test\\java\\com\\itheima\\service\\AccountServiceTest.java

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

使用Spring整合Junit专用的类加载器

#### AOP

##### AOP简介

- AOP（Aspect Oriented Programming）面向切面编程，一种编程范式，知道开发者如何组织程序结构
- 作用：在不惊动原始设计（不需要修改源代码）的基础上为其进行功能增强
- Spring理念：无入侵式编程

##### AOP核心概念

原始方法称为连接点

需要追加功能的称为切入点

共性功能，需要被追加的操作叫通知

- 连接点（JoinPoint）：程序执行过程中的任意位置，粒度为执行方法，抛出异常，设置变量，在SpringAOP中，；理解为方法的执行
- 切入点（PointCut）：匹配连接点的式子，在SpringAOP中，一个切入点可以只描述一个具体方法，也可以匹配多个方法
- 一个具体方法：com.itheima.dao包下的BookDao接口中无形参无返回值的save方法
- 匹配多个方法：所有的save方法，所有的get开头的方法，所有以Dao结尾的接口中的任意方法，所有带有一个参数的方法
- 通知（advice）：在切入点执行的操作，也就是共性功能，在SpringAOP中，功能以方法的形式呈现
- 通知类：定义通知的类
- 切面（Aspect）：描述通知与切入点的对应关系

##### AOP入门案例

1.  AOP入门案例思路分析

案例设定：测定接口执行效率

简化设定：在接口执行前输出当前系统时间

开发模式：注解

1.  AOP入门案例实现

- 导入坐标（pom.xml）

1.      <dependency>
2.        <groupId>org.springframework</groupId>
3.        <artifactId>spring-context</artifactId>
4.        <version>5.2.10.RELEASE</version>
5.      </dependency>
6.      <dependency>
7.        <groupId>org.aspectj</groupId>
8.        <artifactId>aspectjweaver</artifactId>
9.        <version>1.9.4</version>
10.     </dependency>

- 制作连接点方法（原始操作，Dao接口与实现类）
- 制作共性功能（通知类与通知）

1.      public void method(){
2.          System.out.println(System.currentTimeMillis());
3.      }

- 定义切入点@Pointcut("execution(void com.itheima.dao.BookDao.update())")

切入点定义依托一个不具有实际意义的方法进行，即无参数，无返回值，方法体无实际逻辑

- 绑定切入点与通知关系（切面）_@Before("pt()")_

aop-Myadvice

1.  _//通知类必须配置成Spring管理的bean_
2.  @Component
3.  _//设置当前类为切面类_
4.  @Aspect
5.  public class MyAdvice {
6.      _//设置切入点，要求配置在方法上方_
7.      @Pointcut("execution(void com.itheima.dao.BookDao.update())")
8.      private void pt(){}

9.     _//设置在切入点pt()的前面运行当前操作（前置通知）_
10. @Before("pt()")
11.     public void method(){
12.         System.out.println(System.currentTimeMillis());
13.     }
14. }

配置@EnableAspectJAutoProxy

1.  @Configuration
2.  @ComponentScan("com.itheima")
3.  _//开启注解开发AOP功能_
4.  @EnableAspectJAutoProxy
5.  public class SpringConfig {
6.  }

开启注解式AOP注解驱动支持

##### AOP工作流程

1.  Spring容器启动
2.  读取所有切面配置中的切入点
3.  初始化bean，判定bean对应的类中的方法是否匹配任意切入点

匹配失败，创建对象

匹配成功，创建原始对象（目标对象）的代理对象

1.  获取bean执行方法

获取bean，调用方法并执行，完成操作

获取的bean是代理对象时，根据代理对象的运行模式运行原始方法与增强的内容，完成操作

注：

目标对象：原始功能去掉共性功能对应的类产生的对象，这种对象是无法直接完成最终工作

代理：目标对象无法直接完成工作，需要对其功能回填，通过原始对象的代理对象实现

##### AOP切入点表达式

切入点：需要增强的方法

切入点表达式：要进行增强的方法的描述方式

描述方式一：执行com.itheima.dao包下的BookDao接口中的无参数update方法

@Pointcut("execution(void com.itheima.dao.BookDao.update())")

描述方式二：执行com.itheima.dao.impl包下的BookDaoImpl类中的无参数update方法

@Pointcut("execution(void com.itheima.dao.impl.BookDaoImpl.update())")

切入点表达式标准格式：

动作关键字（访问修饰符 返回值 包名.类/接口名.方法名（参数）异常名）

动作关键字：例如execution表示执行到指定切入点

访问修饰符：public/private 可以省略

1.  使用通配符描述切入点，快速描述

\*：单个独立的任意符号，可以独立出现，也可以作为前缀或者后缀的匹配符出现

execution(public \* com.itheima.\*.UserService.find\*(\*))

匹配com.itheima包下的任意包中的UserService类或接口中所有find开头的带有一个参数的方法

..：多个连续的任意符号，可以独立出现，常用于简化包名与参数的书写

execution(public User com..UserService.findById(..))

匹配com包下的任意包中的UserService类或接口中所有名称为findById的方法

+：专用于匹配子类类型

execution(\* \*..Service+.\*(..))

匹配任意业务层方法

1.  书写技巧

- 所有代码按照标准规范开发
- 描述切入点通常描述接口，而不描述实现类（耦合）
- 访问控制修饰符针对接口开发均采用public（可省略）
- 返回值类型对于增删改查类使用精准类型加速匹配，对于查询类使用\*快速描述
- 包名书写尽量不适用..匹配，效率过低，常用\*做单个包描述匹配，或精准匹配
- 接口名/类名书写名称与模块相关的采用\*匹配，例如UserService书写成\*Service,绑定业务层接口名
- 方法名书写以动词进行精准匹配，名词采用\*匹配，例如getById书写成getBy\*，selectAll书写成select\*
- 参数规则较为复杂，根据业务方法灵活调整
- 通常不使用异常作为匹配规则

##### AOP通知类型

- AOP通知类型描述了抽取的共性功能，根据共性功能抽取的位置不同，最终运行代码时要将其加入合理的位置
- AOP通知共分为5种类型
- 前置通知
- 后置通知

1.      @Pointcut("execution(void com.itheima.dao.BookDao.update())")
2.      private void pt(){}
3.      @Pointcut("execution(int com.itheima.dao.BookDao.select())")
4.      private void pt2(){}

5.      _//@Before：前置通知，在原始方法运行之前执行_
6.  @Before("pt()")
7.      public void before() {
8.          System.out.println("before advice ...");
9.     }

10.     _//@After：后置通知，在原始方法运行之后执行_
11. @After("pt2()")
12.     public void after() {
13.         System.out.println("after advice ...");
14.     }

输出结果

before advice ...

book dao update is running ...

after advice...

- 环绕通知

1.      @Around("pt()")
2.      public void around(ProceedingJoinPoint pjp) throws Throwable {
3.          System.out.println("around before advice ...");
4.          _//表示对原始操作的调用_
5.          pjp.proceed();
6.          System.out.println("around after advice ...");
7.      }

抛出异常是因为无法预期原始操作是否存在异常

标准写法

1.      @Around("pt()")
2.      public Object around(ProceedingJoinPoint pjp) throws Throwable {
3.          System.out.println("around before advice ...");
4.          _//表示对原始操作的调用_
5.          Object ret = pjp.proceed();
6.          System.out.println("around after advice ...");
7.          return ret;
8.      }

- 对原始方法调用可直接返回值ret

@Around注意事项

- 环绕通知需要依赖形参ProceedingJoinPoint才能实现对原始方法的调用，进而实现原始方法调用前后同时添加通知
- 通知中如果未使用ProceedingJoinPoint对原始方法进行调用将跳过原始方法的执行
- 对原始方法的调用可以不接受返回值，通知方法设置成void即可，如果接收返回值，必须设定为Object类型
- 由于无法预知原始方法运行后是否会抛出异常，因此环绕通知方法必须抛出Throwable对象

- 返回后通知

1.      _//@AfterReturning：返回后通知，在原始方法执行完毕后运行，且原始方法执行过程中未出现异常现象_
2.      @AfterReturning("pt2()")
3.      public void afterReturning() {
4.          System.out.println("afterReturning advice ...");
5.      }

- 抛出异常后通知

1.      _//@AfterThrowing：抛出异常后通知，在原始方法执行过程中出现异常后运行_
2.      @AfterThrowing("pt2()")
3.      public void afterThrowing() {
4.          System.out.println("afterThrowing advice ...");
5.      }
6.  }

##### 案例：测量业务层接口万次执行效率

需求：任意业务层接口执行均可显示其执行效率（执行时长）

分析

业务功能：业务层接口执行前后分别记录时间，求差值得到执行效率

通知类型选择前后均可增强的类型--环绕通知

配置

1.  @Configuration
2.  @ComponentScan("com.itheima")
3.  @PropertySource("classpath:jdbc.properties")
4.  @Import({JdbcConfig.class,MybatisConfig.class})
5.  @EnableAspectJAutoProxy
6.  public class SpringConfig {
7.  }

ProjectAdvice

1.  @Component
2.  @Aspect
3.  public class ProjectAdvice {
4.      _//匹配业务层的所有方法_
5.      @Pointcut("execution(\* com.itheima.service.\*Service.\*(..))")
6.      private void servicePt(){}

7.      _//设置环绕通知，在原始操作的运行前后记录执行时间_
8.      @Around("ProjectAdvice.servicePt()")
9.     public void runSpeed(ProceedingJoinPoint pjp) throws Throwable {
10.         _//获取执行的签名对象_
11.         Signature signature = pjp.getSignature();
12.         String className = signature.getDeclaringTypeName();
13.         String methodName = signature.getName();

14.         long start = System.currentTimeMillis();
15.         for (int i = 0; i < 10000; i++) {
16.            pjp.proceed();
17.         }

18.         long end = System.currentTimeMillis();
19.         System.out.println("万次执行："+ className+"."+methodName+"---->" +(end-start) + "ms");
20.     }
21. }

注：

模拟当前测试的接口执行效率仅仅是一个理论值，并不是一次完整的执行过程

##### AOP通知获取数据

- 获取切入点方法参数
- JoinPoint：适用于前置后置返回后抛出异常后通知

1.      _//JoinPoint：用于描述切入点的对象，必须配置成通知方法中的第一个参数，可用于获取原始方法调用的参数_
2.      @Before("pt()")
3.      public void before(JoinPoint jp) {
4.          Object\[\] args = jp.getArgs();
5.          System.out.println(Arrays.toString(args));
6.          System.out.println("before advice ..." );
7.      }

8.      @After("pt()")
9.     public void after(JoinPoint jp) {
10.         Object\[\] args = jp.getArgs();
11.         System.out.println(Arrays.toString(args));
12.         System.out.println("after advice ...");
13.     }

- ProceedJointPoint：适用于环绕通知

1.      @Around("pt()")
2.      public Object around(ProceedingJoinPoint pjp) {
3.          Object\[\] args = pjp.getArgs();
4.          System.out.println(Arrays.toString(args));
5.          args\[0\] = 666;
6.          Object ret = pjq.proceed(args);
7.          return ret;
8.      }

args可以先处理传入的参数，保证健壮性

- 获取返回值
- 返回后通知

1.      _//设置返回后通知获取原始方法的返回值，要求returning属性值必须与方法形参名相同_
2.      @AfterReturning(value = "pt()",returning = "ret")
3.      public void afterReturning(JoinPoint jp,String ret) {
4.          System.out.println("afterReturning advice ..."+ret);
5.      }

JoinPoint如有必须放第一个

- 环绕方法

1.      @Around("pt()")
2.      public Object around(ProceedingJoinPoint pjp) {
3.          Object\[\] args = pjp.getArgs();
4.          System.out.println(Arrays.toString(args));
5.          args\[0\] = 666;
6.          Object ret = pjq.proceed(args);
7.          return ret;
8.      }

- 获取异常
- 抛出异常后通知 使用形参接收对应的异常对象

1.      _//设置抛出异常后通知获取原始方法运行时抛出的异常对象，要求throwing属性值必须与方法形参名相同_
2.      @AfterThrowing(value = "pt()",throwing = "t")
3.      public void afterThrowing(Throwable t) {
4.          System.out.println("afterThrowing advice ..."+t);
5.      }

- 环绕通知

1.      @Around("pt()")
2.      public Object around(ProceedingJoinPoint pjp) {
3.          Object\[\] args = pjp.getArgs();
4.          System.out.println(Arrays.toString(args));
5.          args\[0\] = 666;
6.          Object ret = null;
7.          try {
8.              ret = pjp.proceed(args);
9.          } catch (Throwable t) {
10.             t.printStackTrace();
11.         }
12.         return ret;
13.     }

##### 案例：百度网盘密码数据兼容处理

分析：

在业务方法执行之前对所有输入参数进行格式处理-trim()

使用处理后参数调用原始方法-环绕通用之中存在对原始方法的调用

DataAdvice

1.  @Component
2.  @Aspect
3.  public class DataAdvice {
4.     @Pointcut("execution(boolean com.itheima.service.\*Service.\*(\*,\*))")
5.      private void servicePt(){}

6.      @Around("DataAdvice.servicePt()")
7.      public Object trimStr(ProceedingJoinPoint pjp) throws Throwable {
8.          Object\[\] args = pjp.getArgs();
9.         for (int i = 0; i < args.length; i++) {
10.             _//判断参数是不是字符串_
11.             if(args\[i\].getClass().equals(String.class)){
12.                 args\[i\] = args\[i\].toString().trim();
13.             }
14.         }
15.         Object ret = pjp.proceed(args);
16.         return ret;
17.     }

18. }

##### AOP总结

- 概念：面向切面编程，一种编程范式
- 作用：在不惊动原始设计的基础上为方法进行功能增强
- 核心概念
- 代理（Proxy）：SpringAOP中理解为任意方法的执行
- 连接点（JoinPoint）：在SpringAOP中，理解为任意方法的执行
- [切入点（PointCut）](#_AOP切入点表达式)：匹配连接点的式子，也有具有共性功能的方法描述
- [通知（Advice）](#_AOP通知类型)：若干个方法的共性功能，在切入点处执行，最终体现为一个方法
- 切面（Aspect）：描述通知与切入点的对应关系
- 目标对象（Target）：被代理的原始对象成为目标对象

#### 事务

- 事务作用：在数据层保障一系列数据库操作同成功同失败
- Spring事务作用：在数据层保障一系列数据库操作同成功同失败

##### Spring事务简介

案例：模拟银行将转账业务

需求：实现任意两个账户间转账操作

需求微缩：A账户减钱，B账户加钱

分析:

数据层提供基础操作，指定账户减钱（outMoney），指定账户加钱（inMoney）

业务层提供转账操作（transfer），调用减钱与加钱操作

提供2个账户和操作金额执行转账操作

基于Spring整合MyBatis环境搭建上述操作

结果分析：

程序正常执行时，账户金额A减B加没有问题

程序出现异常后，转账失败，但是异常之后操作失败，整体业务失败

1.      public void transfer(String out,String in ,Double money) {
2.          accountDao.outMoney(out,money);
3.  int i = 1/0;
4.          accountDao.inMoney(in,money);
5.      }

- 在需要添加事务的接口上添加Spring事务管理

1.  public interface AccountService {
2.      _/\*\*_
3.       \* 转账操作
4.       \* @param out 传出方
5.       \* @param in 转入方
6.       \* @param money 金额
7.       \*/
8.      _//配置当前接口方法具有事务_
9.      @Transactional
10.     public void transfer(String out,String in ,Double money) ;
11. }

Spring注解式事务通常添加在业务层接口中，降低耦合

注解式事务可以添加到业务方法上表示当前方法开启事务，也可以添加到接口上表示当前接口所有方法开启事务

- 设置事务管理器

JdbcConfig

1.      _//配置事务管理器，mybatis使用的是jdbc事务_
2.      @Bean
3.      public PlatformTransactionManager transactionManager(DataSource dataSource){
4.          DataSourceTransactionManager transactionManager = new DataSourceTransactionManager();
5.          transactionManager.setDataSource(dataSource);
6.          return transactionManager;
7.      }

- 开启注解式事务驱动

SpringConfig

1.  @Configuration
2.  @ComponentScan("com.itheima")
3.  @PropertySource("classpath:jdbc.properties")
4.  @Import({JdbcConfig.class,MybatisConfig.class})
5.  _//开启注解式事务驱动_
6.  @EnableTransactionManagement
7.  public class SpringConfig {
8.  }

##### Spring事务角色

事务1（事务协调员）

|

1.      @Update("update tbl_account set money = money + #{money} where name = #{name}")
2.      void inMoney(@Param("name") String name, @Param("money") Double money);

3.      @Update("update tbl_account set money = money - #{money} where name = #{name}")
4.      void outMoney(@Param("name") String name, @Param("money") Double money);

|

事务2（事务协调员）

1.      public void transfer(String out,String in ,Double money) {
2.          accountDao.outMoney(out,money);
3.          accountDao.inMoney(in,money);
4.      }

|

事务3（事务管理员）

Spring将事务1 2全部加入事务3中，只剩1个事务

事务管理员：发起事务方，在Spring中通常指业务层开启事务的方法

事务协调员：加入事务方，在Spring中通常指数据层方法，也可以是业务层方法

##### Spring事务属性

1.  事务配置

@Transactional(rollbackFor = IOException.class)

设置回滚异常（class）

readOnly 设置只读事务 readOnly = true 只读事务

timeout 设置事务超时时间 timeout = -1 永不超时

rollbackFor 设置回滚异常（class）

rollbackForClassName设置回滚异常（String）

noRollbackFor 设置事务不回滚异常（class）

noRollbackForClassName 设置事务不回滚异常（String）

propagation 设置事务传播行为

1.  案例：转账业务追加日志

需求：实现任意两个账户转账操作，并对每次转账操作在数据库留痕

需求微缩：A账户减钱，B账户加钱，数据库记录日志

分析：

基于转账操作案例添加日志模块，实现数据库中记录日志

业务层转账操作（transfer）调用减钱，加钱，与记录日志功能

实现效果预期：

不论转账操作是否成功，均记录留痕

问题：

日志的记录与转账操作隶属于同一个事务，同成功同失败

1.      public void transfer(String out,String in ,Double money) {
2.          try{
3.              accountDao.outMoney(out,money);
4.              int i = 1/0;
5.              accountDao.inMoney(in,money);
6.          }finally {
7.              logService.log(out,in,money);
8.          }
9.      }

对应三个事务，log与update1与update2 同时隶属于这个Spring事务

要求log不要加入事务

1.  事务传播行为

事务协调员对事务管理员所携带事务的处理态度

propagation 设置事务传播行为

1.  public interface LogService {
2.      _//propagation设置事务属性：传播行为设置为当前操作需要新事务_
3.      @Transactional(propagation = Propagation.REQUIRES_NEW)
4.      void log(String out, String in, Double money);
5.  }

设置事务传播行为REQUIRES_NEW 需要新事务

|     |     |     |
| --- | --- | --- |
| 传播属性 | 事务管理员 | 事务协调员 |
| REQUIRED（默认） | 开启T | 加入T |
| 无   | 新建T2 |
| REQUIRED_NEW | 开启T | 新建T2 |
| 无   | 新建T2 |
| SUPPORTS | 开启T | 加入T |
| 无   | 无   |
| NOT_SUPPORTED | 开启T | 无   |
| 无   | 无   |
| MANDATORY | 开启T | 加入T |
| 无   | ERROR |
| NEVER | 开启T | ERROR |
| 无   | 无   |
| NSESTED | 设置savePoint，一旦事务回滚，事务将回滚到savePoint处，交由客户响应提交/回滚 |     |

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

