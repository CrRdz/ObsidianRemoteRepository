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

# MyBatis快速入门

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

# Mapper代理开发

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

# MyBatis核心配置文件

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

# 配置文件完成增删改查

例：完成品牌数据的增删改操作

## 环境准备

数据库表tb_brand
实体类Brand
测试用例
安装MyBatisX插件 实现XML和接口方法跳转，根据接口方法生成statement

## 查询-所有数据

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
## 查看详情

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
	特殊字符处理：
	\* 转义字符
	\* CDATA区

```xml
<![CDATA[
...(特殊字符)
]]>
```

```xml
 <select id="selectById" resultMap="brandResultMap">
     select
         *
     from tb_brand where id = #{id};
 </select>
```

3.执行方法，测试
```java
@Test
public void testSelectById() throws Exception {
    //0.接受参数
    int id = 1;
    
    //1.获取SqlSessionFactory
    String resource = "mybatis-config.xml";
     InputStream inputStream = Resources.getResourceAsStream(resource);
    SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder()
														   .build(inputStream);
    
    //2. 获取SqlSession对象
    SqlSession sqlSession = sqlSessionFactory.openSession();
    
    //3.获取Mapper接口的代理对象
    BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);
    
    //4.执行方法
    Brand brand = brandMapper.selectById(id);
    System.out.println(brand);
    
    //5.释放资源
    sqlSession.close();
}
```

## 条件查询

- 多条件查询

1.  编写接口方法：Mapper接口

- 参数：所有查询条件
- 结果：`List<Brand>`

散装参数接收 使用@Param
```java
 /**
  * 根据条件查询
  * 参数接收
  * 散装参数：如果方法中有多个参数，需要使用@Param("SQL参数占位符名称"）
  * @param status
  * @param companyName
  * @param brandName
  * @return
  *
  */ List<Brand> selectByCondition(@Param("status")int status,@Param("companyName")String companyName,@Param("brandName")String brandName);
}
```
	
对象参数 I：对象中的属性名称要和SQL参数占位符名称一致
```java
List<Brand> selectByCondition(Brand brand);
```

对象参数 II：对象中的属性名称要和SQL参数占位符名称一致

```java
List<Brand> selectByCondition(Map map);
```

2.  编写SQL语句：SQL映射文件
```xml
 <!--
 条件查询
 -->
 <select id="selectByCondition" resultMap="brandResultMap">
     select
         *
     from tb_brand
      where
         status = #{status}
        and company_name like #{companyName}
        and brand_name like #{brandName}
</select>
```

3. 执行方法，测试
```java
 @Test
     public void testSelectByCondition() throws Exception {
         //0.接受参数
         int status = 1;
         String companyName = "华为";
         String brandName = "华为";
          //处理参数
         companyName = "%" + companyName + "%";
         brandName = "%" + brandName + "%";
         
 //        //封装对象 对应对象参数接收
 //        Brand brand = new Brand();
 //        brand.setStatus(status);
 //        brand.setCompanyName(companyName);
 //        brand.setBrandName(brandName);
 
		 //封装对象 对应map参数接受
         Map map = new HashMap<>();
         map.put("status",status);
         map.put("companyName",companyName);
         map.put("brandName",brandName);
         //1.获取SqlSessionFactory
         String resource = "mybatis-config.xml";
         InputStream inputStream = Resources.getResourceAsStream(resource);
         SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
         //2. 获取SqlSession对象
         SqlSession sqlSession = sqlSessionFactory.openSession();
         //3.获取Mapper接口的代理对象
         BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);
         //4.执行方法
 //        List<Brand> brands = brandMapper.selectByCondition(status, companyName, brandName); //对应散装参数接收
 //        List<Brand> brands = brandMapper.selectByCondition(brand);//对应对象参数接收
         List<Brand> brands = brandMapper.selectByCondition(map);_//对应Map参数接收_
         System.out.println(brands);
         
         //5.释放资源
         sqlSession.close();
     }
```

4. 存在问题

	用户输入条件时，是否所有条件都会填写？
	优化：动态条件查询

- 多条件-动态条件查询

动态SQL ：SQL语句会随着用户的输入或外部条件的变化而变化

BrandMapper.xml

```xml
 <select id="selectByCondition" resultMap="brandResultMap">
     select
         \*
     from tb_brand
     where
         <if test="status != null">
             status = _#{status}_
         </if>
     <if test="companyName != null and companyName != ''">
         and company_name like _#{companyName}_
     </if>
     <if test="brandName != null and brandName != ''">
         and brand_name like _#{brandName}_
     </if>
 </select>
```

test=”条件”条件中使用其真正输入的值而不是属性 即companyName

1.  存在问题

如果第一个条件不存在的话，会多出一个and，MySQL语法错误

优化

1.1  每个语句都加and，并且在where后加上1 = 1 恒等式
```xml
<select id="selectByCondition" resultMap="brandResultMap">
     select
         *
     from tb_brand
     where 1 = 1
         <if test="status != null">
         and status = #{status}
         </if>
     <if test="companyName != null and companyName != ''">
         and company_name like #{companyName}
     </if>
     <if test="brandName != null and brandName != ''">
         and brand_name like #{brandName}
     </if>
 </select>
```

1.2  where 标签（较常用）
```xml
 <select id="selectByCondition" resultMap="brandResultMap">
     select
         \*
     from tb_brand
     <where>
         <if test="status != null">
         and status = _#{status}_
         </if>
    <if test="companyName != null and companyName != ''">
        and company_name like _#{companyName}_
    </if>
    <if test="brandName != null and brandName != ''">
        and brand_name like _#{brandName}_
    </if>
    </where>
</select>
```

- 单条件-动态条件查询
	- 从多个条件中选择一个
	- choose（when，otherwise）：选择，类似于Java中的switch语句

1.  编写接口方法：Mapper接口

- 参数：查询条件
- 结果：`List<Brand>`

```java
List<Brand> selectByConditionSingle(Brand brand);
```

2.  编写SQL语句：SQL映射文件
```xml
</select>
<select id="selectByConditionSingle" resultMap="brandResultMap">
    select
        \*
    from tb_brand
    where
    <choose>_<!--相当于switch-->_
        <when test="status != null">_<!--相当于case-->_
            status = #{status}
        </when>
        <when test="companyName != null and companyName != ''"> _<!--相当于case-->_
            company_name like #{companyName}
        </when>
        <when test="brandName != null and brandName != ''">_<!--相当于case-->_
            brand_name like #{brandName}
        </when>
    </choose>
</select>
```

3.  执行方法，测试
```java
     @Test
     public void testSelectByConditionSingle() throws Exception {
         //0.接受参数
         int status = 1;
         String companyName = "华为";
         String brandName = "华为";
          //处理参数
         companyName = "%" + companyName + "%";
         brandName = "%" + brandName + "%";
         //封装对象 对应对象参数接收
         Brand brand = new Brand();
         brand.setStatus(status);
         brand.setCompanyName(companyName);
         brand.setBrandName(brandName);
 //        Map map = new HashMap<>();
 //        map.put("status",status);
 //        map.put("companyName",companyName);
 //        map.put("brandName",brandName);
         //1.获取SqlSessionFactory
         String resource = "mybatis-config.xml";
         InputStream inputStream = Resources.getResourceAsStream(resource);
         SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
         //2. 获取SqlSession对象
         SqlSession sqlSession = sqlSessionFactory.openSession();
         //3.获取Mapper接口的代理对象
         BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);
         //4.执行方法
         List<Brand> brands = brandMapper.selectByConditionSingle(brand);
         System.out.println(brands);
         //5.释放资源
         sqlSession.close();
     }
```

4.  存在问题

如果用户一个都不选，语法会报错

优化：恒等式

```java
 <otherwise> <!--相当于default-->
    1=1
 </otherwise>
```

## 添加

1.  编辑接口方法：Mapper接口

- 参数：除了id之外的所有数据
- 结果：void

```java
void add(Brand brand);
```

2.  编写SQL语句：SQL映射文件
```xml
  <insert id="add">
     insert into tb_brand (brand_name,company_name,ordered,description,status)
      values (#{brandName},#{companyName},#{ordered},#{description},#{status});
  </insert>
```
 
3. 执行方法，测试
```java
 @Test
 public void add() throws Exception {
     //0.接受参数
     int status = 1;
     String companyName = "波导手机";
     String brandName = "波导";
      String description = "手机中的战斗机";
      int ordered = 100;
      
     //封装对象 对应对象参数接收
     Brand brand = new Brand();
     brand.setStatus(status);
     brand.setCompanyName(companyName);
     brand.setBrandName(brandName);
     brand.setDescription(description);
     brand.setOrdered(ordered);
     
     //1.获取SqlSessionFactory
     String resource = "mybatis-config.xml";
     InputStream inputStream = Resources.getResourceAsStream(resource);
     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder()
													     .build(inputStream);
     //2. 获取SqlSession对象
     SqlSession sqlSession = sqlSessionFactory.openSession();
     
     //3.获取Mapper接口的代理对象
     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);
     
     //4.执行方法
     brandMapper.add(brand);
	//提交事务
     sqlSession.commit();
     
     //5.释放资源
     sqlSession.close();
 }
```
 
 4. 优化
需要手动提交事务 - 可在获取Sqlsession对象时 可以传递布尔值

```java
SqlSession sqlSession = sqlSessionFactory.openSession(true);
```

则可省略#33行
```java
sqlSession.commit();
```

- 添加-主键返回

 在数据添加成功后，需要插入数据库数据的主键的值

```xml
  <insert id="add" useGeneratedKeys="true" keyProperty="id">
      insert into tb_brand 
  (brand_name,company_name,ordered,description,status)
      values 
  (#{brandName},#{companyName},#{ordered},#{description},#{status});
 </insert>
```

## 修改

- 修改全部字段

1.  编写接口方法：Mapper接口
	- 参数：所有数据
	- 结果：void/受影响的行数

```java
int update (Brand brand);
```

2.  编写SQL语句：SQL映射文件
```xml
 <update id="update">
     update tb_brand 
     set 
 brand_name = _#{brandName},
 company_name = #{companyName},
 ordered = #{ordered},
 description = #{description},
  status = #{status}
 where id = #{id};
 </update>
```
3.  执行方法，测试
```java
 @Test
 public void testUpdate() throws Exception {
     //0.接受参数
     int status = 1;
     String companyName = "波导手机";
     String brandName = "波导";
     String description = "波导手机，手机中的战斗机";
     int ordered = 200;
     int id = 4;
     
     //封装对象 对应对象参数接收
     Brand brand = new Brand();
     brand.setStatus(status);
     brand.setCompanyName(companyName);
     brand.setBrandName(brandName);
     brand.setDescription(description);
     brand.setOrdered(ordered);
     brand.setId(id);
     
     //1.获取SqlSessionFactory
     String resource = "mybatis-config.xml";
     InputStream inputStream = Resources.getResourceAsStream(resource);
     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder()
														     .build(inputStream);
     
     //2. 获取SqlSession对象
     SqlSession sqlSession = sqlSessionFactory.openSession(true);
     
     //3.获取Mapper接口的代理对象
     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);
     
     //4.执行方法
     int count = brandMapper.update(brand);
     System.out.println(count);
     
     //5.释放资源
     sqlSession.close();
 }
```

- 修改动态字段

1.  编写接口方法：Mapper接口
	- 参数：部分数据，封装到对象中
	- 结果：void

2.  编写SQL语句：SQL映射文件
```xml
 <update id="update">
     update tb_brand
     <set>
         <if test="brandName != null and brandName != ''">
         brand_name = _#{brandName},_
         </if>
          <if test="companyName != null and companyName != ''">
          company_name = _#{companyName},_
          </if>
         <if test="ordered != null ">
         ordered = _#{ordered},_
         </if>
         <if test="description != null and description != ''">
             description = _#{description},_
         </if>
         <if test="status != null ">
         status = _#{status}_
         </if>
     </set>
        where id = _#{id};_
 </update>
```

3.  执行方法，测试

## 删除

- 删除一个

1.  编写接口方法：Mapper接口
	- 参数：id值
	- 结果：void

```java
void deleteById(int id);
```

1.  编写SQL语句：SQL映射文件
```java
 <delete id="deleteById">
     delete from tb_brand where id = #{id};
 </delete>
```

2.  执行方法，测试
```java
 @Test
 public void testDelete() throws Exception {
     //0.接受参数
     int id = 6;
     //封装对象 对应对象参数接收
     Brand brand = new Brand();
     brand.setId(id);
     //1.获取SqlSessionFactory
     String resource = "mybatis-config.xml";
     InputStream inputStream = Resources.getResourceAsStream(resource);
     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
     
     //2. 获取SqlSession对象
     SqlSession sqlSession = sqlSessionFactory.openSession(true);
     
     //3.获取Mapper接口的代理对象
     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);
     
     //4.执行方法
     brandMapper.deleteById(id);
     
     //5.释放资源
     sqlSession.close();
 }
```

- 批量删除

1.  编写接口方法：Mapper接口
	- 参数：id数组
	- 结果：void

```java
void deleteByIds(@Param("ids") int\[\] ids);
```

1.  编写SQL语句：SQL映射文件
```xml
  <delete id="deleteByIds">
      delete from tb_brand where id
      in (
          <foreach collection="ids" item="id" separator=","open="(" close=")">
              #{id}#{id}#{id}
          </foreach>
          
  </delete>
```

2.  执行方法，测试
```java
@Test
public void testDeleteByIds() throws Exception {
    //0.接受参数_
    int[]ids = {5,7,8};
    //1.获取SqlSessionFactory
    String resource = "mybatis-config.xml";
   InputStream inputStream = Resources.getResourceAsStream(resource);
    SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
    
    //2. 获取SqlSession对象
    SqlSession sqlSession = sqlSessionFactory.openSession(true);
    
    //3.获取Mapper接口的代理对象
    BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);
    
    //4.执行方法
    brandMapper.deleteByIds(ids);
    
    //5.释放资源
    sqlSessionclose();
```
 优化

```java
open="(" close=")"
```

# MyBatis参数查询

Mybatis接口方法中可以接受各种的参数，MyBatis底层对于这些参数进行不同的封装处理方式

- 单个参数

1.  pojo类型：直接使用，属性名 与 参数占位符名称一致
2.  Map集合：直接使用，键名 与 参数占位符一致
3.  Collection：封装为Map集合，可以使用@Param注解，替换Map集合中默认的arg键名
```java
map.put(“arg0”,collection集合)
map.put(“collection”,collection集合)
```
4.  List：封装为Map集合，可以使用@Param注解，替换Map集合中默认的arg键名

```java
map.put(“arg0”,list集合)
map.put(“collection”,list集合)
map.put(“list”,list集合)
```

5.  Array:封装为Map集合，可以使用@Param注解，替换Map集合中默认的arg键名
```java
map.put(“arg0”,数组)
map.put(“array”,数组）
```

6.  其他类型：直接使用
- 多个参数：封装为Map集合，可以使用@Param注解，替换Map集合中默认的arg键名 
- MyBatis提供了ParaNameResolver类来进行参数封装
- 都使用@Param注解来修改Map集合中默认的键名，并使用修改后的名称来获取值，可读性更高

注解完成增删改查

使用注解开发会比配置文件开发更加方便，注解完成简单功能，配置文件完成复杂功能

查询@select

添加@Insert

修改@Update

删除@Delete

案例
1.  编写接口方法及注释开发
```java
@Select("select * from user where id = #{id}")
User selectById(int id);
```
2.  测试用例
	同testSelectById
