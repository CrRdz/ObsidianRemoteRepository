- JDBC（Java DataBase Connectivity）是使用JAVA语言操作关系型数据库的一套API
- 本质：一套操作所有关系型数据库的规则（接口），各个数据库厂商去实现这个接口，提供数据库驱动jar包 MySQL/Oracle... 实现类-驱动

# 1. JDBC快速入门

```Java
// 创建工程，导入jar包 添加到lib文件中
public static void main(String\[\] args) throws Exception {   
    //1. 注册驱动
    //Class.forName("com.mysql.jdbc.Driver");
    
    //2. 获取连接
    String url = "jdbc:mysql://127.0.0.1:3306/db1";
    String username = "root";
    String password = "1234";
    Connection conn = DriverManager.getConnection(url, username, password);
    
    //3. 定义sql
    String sql = "update account set money = 2000 where id = 1";
    
    //4. 获取执行sql的对象 Statement
    Statement stmt = conn.createStatement();
    
    //5. 执行sql
    int count = stmt.executeUpdate(sql);//受影响的行数
    
    //6. 处理结果
    System.out.println(count);
    
    //7. 释放资源
    stmt.close();
    conn.close();
}
```

# 2.JDBC API

## DriverManger（驱动管理类）

0.  注册驱动（可省略）

```java
Class.forName("com.mysql.jdbc.Driver");
```

1.  获取数据库连接

```java
static Connection 
getConnection（String url, String user, string password）
```

	Url: 连接路径

```java
jdbc：mysql：//ip地址：端口号/数据库名称？参考键值对1&参考键值对2...
```

(Localhost)

如果连接的是本机mysql并且端口是默认的3306 可省略

## 3. Connection（数据库连接对象）

2.  获取执行SQL的对象

普通执行SQL对象

```java
createStatement()
```

预编译SQL的执行SQL对象：防止SQL的注入

```java
prepareStatement（sql）
```

执行存储过程的对象

```java
prepareCall（sql）
```

3.  管理事务

MySQL 事务管理：
	开启事务：BEGIN；/START TRANACTION；
	提交事务COMMIT；
	回滚事务 ROLLBACK；

JDBC事务管理：
	开启事务：setAutoCommit（boolean autoCommit）
		TRUE为自动提交事务，FALSE为自动提交事务，即为开启事务
	提交事务：commit（）
	回滚事务：rollback（）
```java
public class JDBCDemo3_Connection {
    public static void main(String\[\] args) throws Exception {
        //1. 注册驱动
        //Class.forName("com.mysql.jdbc.Driver");
        //2. 获取连接：如果连接的是本机mysql并且端口是默认的 3306 可以简化书写
        String url = "jdbc:mysql:///db1?useSSL=false";
        String username = "root";
        String password = "1234";
       Connection conn = DriverManager.getConnection(url, username, password);
       
        //3. 定义sql
        String sql1 = "update account set money = 3000 where id = 1";
        String sql2 = "update account set money = 3000 where id = 2";
        
        //4. 获取执行sql的对象 Statement
        Statement stmt = conn.createStatement();
        try {
            // 开启事务
            conn.setAutoCommit(false);
            //5. 执行sql
            int count1 = stmt.executeUpdate(sql1);_//受影响的行数_
            //6. 处理结果
            System.out.println(count1);
            int i = 3/0;
            //5. 执行sql
            int count2 = stmt.executeUpdate(sql2);_//受影响的行数_
            //6. 处理结果
            System.out.println(count2);
            // 提交事务
            conn.commit();
        } catch (Exception throwables) {
            // 回滚事务
            conn.rollback();
            throwables.printStackTrace();
        }
        //7. 释放资源
        stmt.close();
        conn.close();
    }
}
```

## Statement

执行sql语言

1.  执行DML（增删改），DDL语句

```java
int executeUpdate(sql)；
```

返回值：DML语句影响的行数，DDL语句成功执行后也可能返回0

2.  执行DQL语句

```java
ResultSet executeQuery(sql)；
```

返回值：ResultSet结果集对象

## ResultSet（结果集对象）

1.  封装DQL查询语句的结果 执行DQL语句，返回ResultSet对象

```java
ResultSet stmt.executeQuery(sql)；
```

2.  获取查询结果

```java
boolean next()
```
将光标从当前位置向前移动一行，判断当前行是否为有效行

返回值：
	TRUE有效行，当前行有数据
	FALSE无效行，当前行没有数据

xxx getXxx(参数)

xxx：数据类型；如int getInt；String getString

参数：

int：列的编号，从1开始

String：列的名称

使用步骤：

 游标向下移动一行，并判断该行是否有数据：next（）
 获取数据：getXxx（参数）
 
```java
 // 6.1 光标向下移动一行，并且判断当前行是否有数据_
 while (rs.next()){
     //6.2 获取数据  getXxx()
     int id = rs.getInt("id");//or: rs.getInt(1)
     String name = rs.getString("name");
     double money = rs.getDouble("money");
     System.out.println(id);
     System.out.println(name);
     System.out.println(money);
     System.out.println("--------------");
 }
 
  /**
  * 查询account账户表数据
  * 封装为Account对象中，并且存储到ArrayList集合中
  * 1. 定义实体类Account
  * 2. 查询数据，封装到Account对象中
  * 3. 将Account对象存入ArrayList集合中     
  * @throws Exception
  */
 @Test
 public void testResultSet2() throws  Exception {
    //1. 注册驱动
    //Class.forName("com.mysql.jdbc.Driver");
    //2. 获取连接：如果连接的是本机mysql并且端口是默认的 3306 可以简化书写
    String url = "jdbc:mysql:///db1?useSSL=false";
    String username = "root";
    String password = "1234";
    Connection conn = DriverManager.getConnection(url, username, password);
    
     //3. 定义sql
     String sql = "select * from account";
     
     //4. 获取statement对象
     Statement stmt = conn.createStatement();
     
     //5. 执行sql
     ResultSet rs = stmt.executeQuery(sql);
     
     // 创建集合
     List<Account> list = new ArrayList<>();
     
     // 6.1 光标向下移动一行，并且判断当前行是否有数据
     while (rs.next()){
        Account account = new Account();
        //6.2 获取数据  getXxx()
        int id = rs.getInt("id");
        String name = rs.getString("name");
        double money = rs.getDouble("money");
         //赋值
         account.setId(id);
         account.setName(name);
         account.setMoney(money);
         // 存入集合
         list.add(account);
     }
     System.out.println(list);
     //7. 释放资源
     rs.close();
     stmt.close();
     conn.close();
 }
```

PreparedStatement
  预编译SQL并执行SQL语句，预防SQL注入（通过操作输入事先定义好的SQL语句，用以达到执行代码对服务器攻击的方法）
  
  获取PreparedStatement对象
  
```java
  //SQL语句中的参数值，使用？占位符替代
  String sql="select \* from user where username =? and password = ?";
  //通过Connection对象获取，并传入对应的sql语句
  PreparedStatement psmt = conn.prepareStatement(sql);
```
  
  设置参数值
	PreparedStatement对象：setXxx（参数1，参数2）：给？赋值
	Xxx：数据类型；如setInt（参数1，参数2）
	参数：
		参数1：？的位置编号，从1开始
		参数2：？的值
	执行SQL
```java
executeUpdate()；
executeQuery();//不需要再传递sql
```


```java
@Test
public void testPreparedStatement() throws  Exception {
   //获取连接：如果连接的是本机mysql并且端口是默认的 3306 可以简化书写
   String url = "jdbc:mysql:///db1?useSSL=false";
   String username = "root";
   String password = "1234";
   Connection conn = DriverManager.getConnection(url, username, password);
   // 接收用户输入 用户名和密码_
   String name = "zhangsan";
   String pwd = "' or '1' = '1";
   // 定义sql
   String sql = "select \* from tb_user where username = ? and password = ?";
    // 获取pstmt对象
    PreparedStatement pstmt = conn.prepareStatement(sql);
    // 设置？的值
    pstmt.setString(1,name);
    pstmt.setString(2,pwd);
    // 执行sql
    ResultSet rs = pstmt.executeQuery();
    // 判断登录是否成功
    if(rs.next()){
        System.out.println("登录成功~");
    }
    else{
        System.out.println("登录失败~");
    }
    //7. 释放资源
    rs.close();
    pstmt.close();
    conn.close();
}
```


PreparedStatement好处 & 原理
好处：预编译SQL，性能更好，防止SQL注入，将敏感字符转义

原理：
- 在获取PreparedStatement对象时，将sql语句发送给mysql服务器进行检查，编译
- 执行时将不用再进行这些步骤，速度更快
- 如果sql模板一样，则只需要进行一次检查，编译

# 数据连接池

- 数据库连接池是个容器，负责分配，管理数据库连接（Connection）
- 它允许应用程序重复使用一个现有的数据库连接而不是再重新建立一个
- 释放空闲时间超过最大空闲时间的数据库连接来避免因为没有释放数据库连接池引起的数据库连接遗漏

标准接口：DataSource
常见数据库连接池：DBCP C3P0 Druid

## Druid
```java
public static void main(String\[\] args) throws Exception {
    //1.导入jar包
    //2.定义配置文件
    //3. 加载配置文件
    Properties prop = new Properties();
    prop.load(new FileInputStream("jdbc-demo/src/druid.properties"));
   //4. 获取连接池对象
   DataSource dataSource = DruidDataSourceFactory.createDataSource(prop);
   //5. 获取数据库连接 Connection
    Connection connection = dataSource.getConnection();
    System.out.println(connection);
```

# JDBC 小结

JDBC基本步骤（标红为可变语句）

1.  获取Connection
2.  定义SQL
3.  获取PreparedStatement对象
4.  设置参数
5.  执行SQL
6.  处理结果
7.  释放资源

# APPENDIX

## 查询
```java
 /**
  * 查询所有
  * 1. SQL：select \* from tb_brand;
  * 2. 参数：不需要
  * 3. 结果：List&lt;Brand&gt;
  */
 @Test
 public void testSelectAll() throws Exception {
     //1. 获取Connection
     //3. 加载配置文件
     Properties prop = new Properties();
     prop.load(new FileInputStream("jdbc-demo/src/druid.properties"));
     
     //4. 获取连接池对象
     DataSource dataSource = DruidDataSourceFactory.createDataSource(prop);
     
     //5. 获取数据库连接 Connection
     Connection conn = dataSource.getConnection();
     
     //2. 定义SQL
     String sql = "select \* from tb_brand;";
     
     //3. 获取pstmt对象
     PreparedStatement pstmt = conn.prepareStatement(sql);
     
     //4. 设置参数
     //5. 执行SQL
     ResultSet rs = pstmt.executeQuery();
     
     //6. 处理结果 List<Brand> 封装Brand对象，装载List集合
     Brand brand = null;
     List<Brand> brands = new ArrayList<>();
     while (rs.next()){
         //获取数据
         int id = rs.getInt("id");
         String brandName = rs.getString("brand_name");
         String companyName = rs.getString("company_name");
         int ordered = rs.getInt("ordered");
         String description = rs.getString("description");
         int status = rs.getInt("status");
         //封装Brand对象
         brand = new Brand();
         brand.setId(id);
         brand.setBrandName(brandName);
         brand.setCompanyName(companyName);
         brand.setOrdered(ordered);
         brand.setDescription(description);
         brand.setStatus(status);
         //装载集合
         brands.add(brand);
     }
     System.out.println(brands);
     
     //7. 释放资源
     rs.close();
     pstmt.close();
     conn.close();
 }
```