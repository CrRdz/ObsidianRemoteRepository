# 技术栈

- Javaweb：MySQL，JDBC，Maven，MyBatis，HTML，CSS，JavaScript，JSP，AJAX，Axios，VUE，ElementUI，Git
- SSM：Spring，SpringMVC，Maven advanced，SpringBoot，MyBatisPlus
- [[Linux]]
- [[Redis]]：redis，redission，LuaScript，Lombok
- SpringBoot3 + VUE3

# JavaWeb

## 数据库DataBase

- 存储数据的仓库，数据是有组织地进行存储
- 数据管理系统DBMS：管理数据库的大型软件
- SQL: Structured Query language 结构化查询语言，操作数据库的编程语言

关系型数据库

建立在关系模型基础上的数据库，由多张能相互连接的二维表组成。

1.  都是使用表结构，格式一致，易于维护。
2.  使用通用的SQL语言操作，使用方便，可用于复杂查询。
3.  数据存储在磁盘中，安全。

### SQL语法

SQL可以单行或者多行书写，以分号结尾，不区分大小写（关键词建议使用大写）

#### 注释

单行注释： --注释内容 或 # 注释内容 （MySQL特有）

多行注释： /\*注释\*/ 同java

#### DDL（数据定义语言）

操作数据库，表

- 操作数据库

1.  查询

SHOW DATABASES；

1.  创建

CREATE DATABASE IF NOT EXISTS 数据库名称

1.  删除

DROP DATABASES IF EXISTS 数据库名称；

1.  使用数据库

SELECT DATABASE(); --查询当前使用的数据库

USE 数据库名称；--使用数据库

2.2 操作表

1.  查询表 Retrive

SHOW TABLES； _\--查询当前数据库下所有表的名称_

DESC 表名称； _\--查询表结构_
```sql
1.  创建表 CREATE
2.  CREATE TABLE 表名（
3.         字段名1 数据类型1，
4.         字段名2 数据类型2，_\--字符串VARCHAR（最大位数）_
5.         字段名3 数据类型3，
6.         ...
7.         字段名n 数据类型n  _\--最后一行末尾不能加逗号_
8.  ）；
9.  删除表
```

DROP TABLE IF EXISTS 表名；

1.  修改表

- 修改表名

ALTER TABLE 表名 RENAME TO 新的表名；

- 添加一列

ALTER TABLE 表名 ADD 列名 数据类型；

- 修改数据类型

ALTER TABLE 表名 MODIFY 列名 新数据类型；

- 修改列名和数据类型

ALTER TABLE 表名 CHANGE 列名 新列名 新数据类型

- 删除列

ALTER TABLE 表名 DROP 列名；

注：数值类型

一般字符串使用VARCHAR可变长度 且 保证性能 过大的使用文件服务器保存路径

Double（总长度，小数点后保留的位数）

#### DML（数据操纵语言）

对表中数据进行增删改

1.  添加数据

- 给指定列添加数据

INSERT INTO 表名（列名1，列名2，...）VALUES（值1，值2，...）

- 给全部列添加数据

INSERT INTO 表名 VALUES（值1，值2）

- 批量添加数据

INSERT INTO 表名（列名1，列名2，...）VALUES（值1，值2，...）,（值1，值2，...）... ;

INSERT INTO 表名 VALUES（值1，值2，...）,（值1，值2，...）,（值1，值2...）...;

1.  修改数据

UPDATE 表名 SET 列名1 = 值1，列名2 = 值2，...\[WHERE 条件\]；

\--如果update语句没有加where条件，则将表中所有数据全部修改

1.  删除数据

DELETE FROM表名 \[WHERE 条件\]；

#### DQL（数据查询语言）

对表中的数据进行查询

1.  基础查询

- 查询多个字段

SELECT 字段列表 FROM 表；

&nbsp; SELECT \* FROM 表名；_\--查询所有数据_

- 去除重复记录

SELECT DISTINCT 字段列表 FROM 表名；

- 起别名

AS：As也可以省略

1.  条件查询

SELECT 字段列表 FROM 表名 WHERE 条件；

注：

条件：

\>/< 大于/小于

<>/!= 不等于

BETWEEN... AND 在某个范围里（都包含）

IN（...）多选一

LIKE占位符 模糊查询 \_单个任意字符 %多个任意字符

IS NULL/IS NOT NULL

AND/&& 并且

OR/|| 或者

NOT/！ 非

1.  排序查询（ORDER BY）

SELECT 字段列表 FROM 表名 

ORDER BY 排序字段名1 \[排序方式1\] ，排序字段2 \[排序方式2\]  

ASC：升序排列（默认值）

DESC：降序排列

如果有多个排序条件，当前边的条件值一样时才会根据第二条件进行排序

1.  分组查询（GROUP BY）

SELECT 字段列表 FROM 表名 

\[WHERE 分组前条件限定\] 

GROUP BY 分组字段名 

\[HAVING 分组后条件过滤\]

WHERE和HAVING区别：执行时机不一样，WHERE是分组之前限定，不满足WHERE条件，则不参与分组，而HABVING是分组之后对结果进行过滤

执行顺序：where>聚合函数>having

注：

聚合函数：将一组数据作为一个整体，进行纵向计算

聚合函数分类：

Count（列名）：统计行数量 取值：主键/\* count(\*) 返回所有行的数量

Max（列名），min（列名），sum（列名） AVG（列名）

1.  分页查询（LIMIT）

SELECT 字段列表 FROM 表名 LIMIT 起始索引，查询条目数

起始索引从0开始 起始索引 = （当前页码 - 1） \* 每页显示的条数

1.  DCL（数据控制语言）

对数据库进行权限控制

### 约束

约束是作用于表上列的规则，用于限制加入表的数据

约束的存在保证了数据库中数据的正确性，完整性和有效性


非空约束 保证列中所有数据不能有null值 NOT NULL

唯一约束 保证列中所有数据各不相同 UNIQUE

主键约束 主键是一行数据的唯一标识 要求非空且唯一 PRIMARY KEY

检查约束 保证列中的值满足其某一条件 CHECK（MySQL不支持）

默认约束 保存数据时，未指定值则采用默认值 NULL属于指定值 DEFAULT

外键约束 外键用来让两个表之间的数据建立连接 FOREIGN KEY

自动增长 auto_increment

外键约束

外键用来让两个表的数据之间建立链接，保证数据的一致性和完整性

添加约束：

（--创建表时添加外键约束）

1.  CREATE TABLE 表名（
2.    列名 数据类型
3.    ...
4.    \[CONSTRAINT\]\[外键名称\] FOREIGN KEY（外键列名）REFERENCES 主表（主表列名）
5.  ）

（--建完表后添加外键约束）

ALTER TABLE表名 ADD CONSTRAINT 外键名称 FOREIGN KEY（外键字段名称）REFERENCE 主表名称（主表列名称）；

删除约束：

ALTER TABLE 表名 DROP FOREIGN KEY 外键名称；

### 数据库设计

#### 数据库设计概念

建立数据库中的表结构以及表与表之间的关联关系的过程

\-有哪些表? 表中有哪些字段? 表和表之间有什么关系？

设计的步骤：

1.  需求分析（数据，数据的属性）
2.  逻辑分析（ER图对数据库进行逻辑建模 不需要考虑选用的dbms）
3.  物理设计（根据数据库自身特点把逻辑设计转换为物理设计）
4.  维护设计（对新的需求进行建表 表优化

#### 表关系

1.  一对一：用户和用户详情

实现方式：在任意一方加入外键，关联另一方主键，并且设置外键为唯一（UNIQUE）

1.  一对多：部门和员工 一个部门有多个员工 一个员工对应一个部门

实现方式：在多的乙方建立外键，指向一的一方的主键

1.  多对多：商品和订单 一个商品对应多个订单 一个订单包含多个商品

实现方式：建立第三层中间表，中间表至少把含两个外键，分别关联两个主键

#### 数据库设计案例

音乐软件: 抽象成四个表，曲目 专辑 用户 短评

专辑-曲目 一对多 |

用户-短评 一对多 |

专辑-短评 一对多 | 字段分析……

用户-专辑 多对多 |

### 多表查询

#### 笛卡儿积

从多张表查询数据 返回多张表所有的可能集合

#### 连接查询

1.  内连接：查询AB交集数据

隐式内连接

SELECT 字段列表 FROM 表1，表2... WHERE 条件；

显式内连接

SELECT 字段列表 FROM 表1 \[INNER\] JOIN 表2 ON 条件；

1.  外连接：
2.  左外连接：相当于查询A表（左表）所有数据和交集部分数据

SELECT 字段列表 FROM 表1  LEFT \[OUTER\] JOIN 表2 ON 条件

1.  右外连接：相当于查询B表（右表）所有数据和交集部分数据

SELECT 字段列表 FROM 表1  RIGHT \[OUTER\] JOIN 表2 ON 条件

#### 子查询

子查询根据查询结果不同 作用不通过

1.  单行单列：作为条件值，使用 = ！ = > < 等进行条件判断

SELECT 字段列表 FROM 表 WHERE 字段名 = （子查询）；

1.  多行多列：作为条件值，使用in等关键词进行条件判断

SELECT 字段列表 FROM 表 WHERE 字段名 in （子查询）；

1.  多行多列：作为虚拟表 多表查询

SELECT 字段列表 FROM （子查询）WHERE 条件；

#### 多表查询示例

1.  _\-- 部门表_
2.  CREATE TABLE dept (
3.    id INT PRIMARY KEY PRIMARY KEY, _\-- 部门id_
4.    dname VARCHAR(50), _\-- 部门名称_
5.    loc VARCHAR(50) _\-- 部门所在地_
6.  );

1.  _\-- 职务表，职务名称，职务描述_
2.  CREATE TABLE job (
3.    id INT PRIMARY KEY,
4.    jname VARCHAR(20),
5.    description VARCHAR(50)
6.  );

1.  _\-- 员工表_
2.  CREATE TABLE emp (
3.    id INT PRIMARY KEY, _\-- 员工id_
4.    ename VARCHAR(50), _\-- 员工姓名_
5.    job_id INT, _\-- 职务id_
6.    mgr INT , _\-- 上级领导_
7.    joindate DATE, _\-- 入职日期_
8.    salary DECIMAL(7,2), _\-- 工资_
9.    bonus DECIMAL(7,2), _\-- 奖金_
10.   dept_id INT, _\-- 所在部门编号_
11.   CONSTRAINT emp_jobid_ref_job_id_fk FOREIGN KEY (job_id) REFERENCES job (id),
12.   CONSTRAINT emp_deptid_ref_dept_id_fk FOREIGN KEY (dept_id) REFERENCES dept (id)
13. );

1.  _\-- 工资等级表_
2.  CREATE TABLE salarygrade (
3.    grade INT PRIMARY KEY,   _\-- 级别_
4.    losalary INT,  _\-- 最低工资_
5.    hisalary INT _\-- 最高工资_
6.  );

8.  _\-- 添加4个部门_
9.  INSERT INTO dept(id,dname,loc) VALUES 
10. (10,'教研部','北京'),
11. (20,'学工部','上海'),
12. (30,'销售部','广州'),
13. (40,'财务部','深圳');

1.  _\-- 添加4个职务_
2.  INSERT INTO job (id, jname, description) VALUES
3.  (1, '董事长', '管理整个公司，接单'),
4.  (2, '经理', '管理部门员工'),
5.  (3, '销售员', '向客人推销产品'),
6.  (4, '文员', '使用办公软件');

1.  _\-- 添加员工_
2.  INSERT INTO emp(id,ename,job_id,mgr,joindate,salary,bonus,dept_id) VALUES 
3.  (1001,'孙悟空',4,1004,'2000-12-17','8000.00',NULL,20),
4.  (1002,'卢俊义',3,1006,'2001-02-20','16000.00','3000.00',30),
5.  (1003,'林冲',3,1006,'2001-02-22','12500.00','5000.00',30),
6.  (1004,'唐僧',2,1009,'2001-04-02','29750.00',NULL,20),
7.  (1005,'李逵',4,1006,'2001-09-28','12500.00','14000.00',30),
8.  (1006,'宋江',2,1009,'2001-05-01','28500.00',NULL,30),
9.  (1007,'刘备',2,1009,'2001-09-01','24500.00',NULL,10),
10. (1008,'猪八戒',4,1004,'2007-04-19','30000.00',NULL,20),
11. (1009,'罗贯中',1,NULL,'2001-11-17','50000.00',NULL,10),
12. (1010,'吴用',3,1006,'2001-09-08','15000.00','0.00',30),
13. (1011,'沙僧',4,1004,'2007-05-23','11000.00',NULL,20),
14. (1012,'李逵',4,1006,'2001-12-03','9500.00',NULL,30),
15. (1013,'小白龙',4,1004,'2001-12-03','30000.00',NULL,20),
16. (1014,'关羽',4,1007,'2002-01-23','13000.00',NULL,10);

1.  _\-- 添加5个工资等级_
2.  INSERT INTO salarygrade(grade,losalary,hisalary) VALUES 
3.  (1,7000,12000),
4.  (2,12010,14000),
5.  (3,14010,20000),
6.  (4,20010,30000),
7.  (5,30010,99990);

Q&A

1.  _\-- 1.查询所有员工信息。查询员工编号，员工姓名，工资，职务名称，职务描述_
2.  SELECT emp.id,emp.ename,emp.salary,job.jname,job.description 
3.  FROM job,emp WHERE emp.job_id =job.id

1.  _\-- 2.查询员工编号，员工姓名，工资，职务名称，职务描述，部门名称，部门位置_
2.  SELECT emp.id,emp.ename,emp.salary,job.jname,job.description,dept.dname,dept.loc 
3.  FROM emp,job,dept
4.  WHERE emp.job_id =job.id and dept.id =emp.dept_id;

1.  _\-- 3.查询员工姓名，工资，工资等级_
2.  SELECT emp.ename,emp.salary,salarygrade.\* FROM emp,salarygrade
3.  WHERE emp.salary>= salarygrade.losalary AND emp.salary <= salarygrade.hisalary

1.  _\-- 4.查询员工姓名，工资，职务名称，职务描述，部门名称，部门位置，工资等级_
2.  SELECT emp.ename,emp.salary,job.jname,job.description,dept.dname,dept.loc,salarygrade.grade 
3.  FROM emp,job,dept,salarygrade
4.  WHERE emp.salary>= salarygrade.losalary 
5.  AND emp.salary <= salarygrade.hisalary 
6.  AND emp.job_id =job.id and dept.id =emp.dept_id;

1.  _\-- 5.查询出部门编号、部门名称、部门位置、部门人数_
2.  SELECT dept.id,dept.dname,dept.loc,t1.count 
3.  FROM dept,
4.  (SELECT dept_id, count(\*)count from emp GROUP BY dept_id) t1 
5.  WHERE dept.id = t1.dept_id

### 事务

事务是一种机制，一个操作序列，包含一组数据库操作命令，把所有的命令作为一个整体一起向系统提交或撤销操作请求，这一组数据库命令要么同时失败，要么同时成功。事务是一个不可分割的工作逻辑单元。

#### 事务操作

1.  _\--开启事务_
2.  START TRANSACTION；
3.  BEGIN
4.  _\--提交事务_
5.  COMMIT；
6.  _\--回滚事务 回滚到事务开始的时候_
7.  ROLLBACK；

#### 事务四大特征

原子性（Atomicity）事务是不可分割的最小操作单位要么同时成功，要么同时失败

一致性（Consistency）事务完成时，必须使所有的数据都保持一致状态

隔离性（Isolation）多个事务之间，操作的可见性

持久性（Durability）事务一旦提交或者回滚，它对数据库中的数据的更改就是永久的

MySQL默认自动提交

## JDBC

- JDBC（Java DataBase Connectivity）是使用JAVA语言操作关系型数据库的一套API
- 本质：一套操作所有关系型数据库的规则（接口），各个数据库厂商去实现这个接口，提供数据库驱动jar包 MySQL/Oracle... 实现类-驱动

### JDBC快速入门

1.  创建工程，导入jar包 添加到lib文件中
2.  public static void main(String\[\] args) throws Exception {   
3.      _//1. 注册驱动_
4.      _//Class.forName("com.mysql.jdbc.Driver");_
5.      _//2. 获取连接_
6.      String url = "jdbc:mysql://127.0.0.1:3306/db1";
7.      String username = "root";
8.      String password = "1234";
9.      Connection conn = DriverManager.getConnection(url, username, password);
10.     _//3. 定义sql_
11.     String sql = "update account set money = 2000 where id = 1";
12.     _//4. 获取执行sql的对象 Statement_
13.     Statement stmt = conn.createStatement();
14.     _//5. 执行sql_
15.     int count = stmt.executeUpdate(sql);_//受影响的行数_
16.     _//6. 处理结果_
17.     System.out.println(count);
18.     _//7. 释放资源_
19.     stmt.close();
20.     conn.close();
21. }

### JDBC API

#### DriverManger（驱动管理类）

1.  注册驱动（可省略）

Class.forName("com.mysql.jdbc.Driver");

1.  获取数据库连接

static Connection 

getConnection（String url, String user, string password）

Url: 连接路径

语法：jdbc：mysql：//ip地址：端口号/数据库名称？参考键值对1&参考键值对2...

(Localhost)

如果连接的是本机mysql并且端口是默认的3306 可省略

#### Connection（数据库连接对象）

1.  获取执行SQL的对象

普通执行SQL对象

createStatement()

预编译SQL的执行SQL对象：防止SQL的注入

prepareStatement（sql）

执行存储过程的对象

prepareCall（sql）

1.  管理事务

MySQL 事务管理：

开启事务：BEGIN；/START TRANSACTION；

提交事务COMMIT；

回滚事务 ROLLBACK；

JDBC事务管理：

开启事务：setAutoCommit（boolean autoCommit）

TRUE为自动提交事务，FALSE为自动提交事务，即为开启事务

提交事务：commit（）

回滚事务：rollback（）

``
1.  public class JDBCDemo3_Connection {

2.      public static void main(String\[\] args) throws Exception {
3.          _//1. 注册驱动_
4.          _//Class.forName("com.mysql.jdbc.Driver");_
5.          _//2. 获取连接：如果连接的是本机mysql并且端口是默认的 3306 可以简化书写_
6.          String url = "jdbc:mysql:///db1?useSSL=false";
7.          String username = "root";
8.          String password = "1234";
9.         Connection conn = DriverManager.getConnection(url, username, password);
10.         _//3. 定义sql_
11.         String sql1 = "update account set money = 3000 where id = 1";
12.         String sql2 = "update account set money = 3000 where id = 2";
13.         _//4. 获取执行sql的对象 Statement_
14.         Statement stmt = conn.createStatement();

15.         try {
16.             _// 开启事务_
17.             conn.setAutoCommit(false);
18.             _//5. 执行sql_
19.             int count1 = stmt.executeUpdate(sql1);_//受影响的行数_
20.             _//6. 处理结果_
21.             System.out.println(count1);
22.             int i = 3/0;
23.             _//5. 执行sql_
24.             int count2 = stmt.executeUpdate(sql2);_//受影响的行数_
25.             _//6. 处理结果_
26.             System.out.println(count2);

27.             _// 提交事务_
28.             conn.commit();
29.         } catch (Exception throwables) {
30.             _// 回滚事务_
31.             conn.rollback();
32.             throwables.printStackTrace();
33.         }

34.         _//7. 释放资源_
35.         stmt.close();
36.         conn.close();
37.     }
38. }

#### Statement

执行sql语言

1.  执行DML（增删改），DDL语句

int executeUpdate(sql)；

返回值：DML语句影响的行数，DDL语句成功执行后也可能返回0

1.  执行DQL语句

ResultSet executeQuery(sql)；

返回值：ResultSet结果集对象

#### ResultSet（结果集对象）

1.  封装DQL查询语句的结果 执行DQL语句，返回ResultSet对象

ResultSet  stmt.executeQuery(sql)；

1.  获取查询结果

boolean next（）

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

1.  游标向下移动一行，并判断该行是否有数据：next（）
2.  获取数据：getXxx（参数）

1.  _// 6.1 光标向下移动一行，并且判断当前行是否有数据_
2.  while (rs.next()){
3.      _//6.2 获取数据  getXxx()_
4.      int id = rs.getInt("id");//or: rs.getInt(1)
5.      String name = rs.getString("name");
6.      double money = rs.getDouble("money");

8.      System.out.println(id);
9.      System.out.println(name);
10.     System.out.println(money);

12.     System.out.println("--------------");
13. }

1.  案例
2.  _/\*\*_
3.  \* 查询account账户表数据
4.  \* 封装为Account对象中，并且存储到ArrayList集合中
5.  \* 1. 定义实体类Account
6.  \* 2. 查询数据，封装到Account对象中
7.  \* 3. 将Account对象存入ArrayList集合中     
8.  \* @throws Exception
9.  \*/
10. @Test
11. public void testResultSet2() throws  Exception {
12.     _//1. 注册驱动_
13.    _//Class.forName("com.mysql.jdbc.Driver");_
14.   _//2. 获取连接：如果连接的是本机mysql并且端口是默认的 3306 可以简化书写_
15.    String url = "jdbc:mysql:///db1?useSSL=false";
16.    String username = "root";
17.    String password = "1234";
18.    Connection conn = DriverManager.getConnection(url, username, password);

20.     _//3. 定义sql_
21.     String sql = "select \* from account";

23.     _//4. 获取statement对象_
24.     Statement stmt = conn.createStatement();

26.     _//5. 执行sql_
27.     ResultSet rs = stmt.executeQuery(sql);

29.     _// 创建集合_
30.     List&lt;Account&gt; list = new ArrayList<>();

32.     _// 6.1 光标向下移动一行，并且判断当前行是否有数据_
33.     while (rs.next()){
34.        Account account = new Account();

36.        _//6.2 获取数据  getXxx()_
37.        int id = rs.getInt("id");
38.        String name = rs.getString("name");
39.        double money = rs.getDouble("money");

41.         _//赋值_
42.         account.setId(id);
43.         account.setName(name);
44.         account.setMoney(money);

46.         _// 存入集合_
47.         list.add(account);
48.     }

50.     System.out.println(list);

52.     _//7. 释放资源_
53.     rs.close();
54.     stmt.close();
55.     conn.close();
56. }

1.  PreparedStatement
2.  预编译SQL并执行SQL语句，预防SQL注入（通过操作输入事先定义好的SQL语句，用以达到执行代码对服务器攻击的方法）
3.  获取PreparedStatement对象
4.  //SQL语句中的参数值，使用？占位符替代
5.  String sql="select \* from user where username =? and password = ?";

7.  //通过Connection对象获取，并传入对应的sql语句
8.  PreparedStatement psmt = conn.prepareStatement(sql);
9.  设置参数值

PreparedStatement对象：setXxx（参数1，参数2）：给？赋值

Xxx：数据类型；如setInt（参数1，参数2）

参数：

参数1：？的位置编号，从1开始

参数2：？的值

1.  执行SQL

executeUpdate();

executeQuery();//不需要再传递sql

1.  @Test
2.  public void testPreparedStatement() throws  Exception {
3.     _//获取连接：如果连接的是本机mysql并且端口是默认的 3306 可以简化书写_
4.     String url = "jdbc:mysql:///db1?useSSL=false";
5.     String username = "root";
6.     String password = "1234";
7.     Connection conn = DriverManager.getConnection(url, username, password);

9.     _// 接收用户输入 用户名和密码_
10.    String name = "zhangsan";
11.    String pwd = "' or '1' = '1";

13.    _// 定义sql_
14.    String sql = "select \* from tb_user where username = ? and password = ?";

16.     _// 获取pstmt对象_
17.     PreparedStatement pstmt = conn.prepareStatement(sql);

19.     _// 设置？的值_
20.     pstmt.setString(1,name);
21.     pstmt.setString(2,pwd);

23.     _// 执行sql_
24.     ResultSet rs = pstmt.executeQuery();

26.     _// 判断登录是否成功_
27.     if(rs.next()){
28.         System.out.println("登录成功~");
29.     }else{
30.         System.out.println("登录失败~");
31.     }

33.     _//7. 释放资源_
34.     rs.close();
35.     pstmt.close();
36.     conn.close();
37. }
38. PreparedStatement好处 & 原理

好处：

预编译SQL，性能更好，防止SQL注入，将敏感字符转义

原理：

- 在获取PreparedStatement对象时，将sql语句发送给mysql服务器进行检查，编译
- 执行时将不用再进行这些步骤，速度更快
- 如果sql模板一样，则只需要进行一次检查，编译

### 数据连接池

- 数据库连接池是个容器，负责分配，管理数据库连接（Connection）
- 它允许应用程序重复使用一个现有的数据库连接而不是再重新建立一个
- 释放空闲时间超过最大空闲时间的数据库连接来避免因为没有释放数据库连接池引起的数据库连接遗漏

标准接口：DataSource

常见数据库连接池：

DBCP C3P0 Druid

#### Druid

1.  public static void main(String\[\] args) throws Exception {
2.      _//1.导入jar包_
3.      _//2.定义配置文件_

5.      _//3. 加载配置文件_
6.      Properties prop = new Properties();
7.      prop.load(new FileInputStream("jdbc-demo/src/druid.properties"));

9.  _//4. 获取连接池对象_
10.     DataSource dataSource = DruidDataSourceFactory.createDataSource(prop);

12.     _//5. 获取数据库连接 Connection_
13.     Connection connection = dataSource.getConnection();

15.     System.out.println(connection);

### JDBC 小结

JDBC基本步骤（标红为可变语句）

1.  获取Connection
2.  定义SQL
3.  获取PreparedStatement对象
4.  设置参数
5.  执行SQL
6.  处理结果
7.  释放资源

### APPENDIX

#### 查询

1.  _/\*\*_
2.   \* 查询所有
3.   \* 1. SQL：select \* from tb_brand;
4.   \* 2. 参数：不需要
5.   \* 3. 结果：List&lt;Brand&gt;
6.   \*/
7.  @Test
8.  public void testSelectAll() throws Exception {
9.      _//1. 获取Connection_
10.     _//3. 加载配置文件_
11.     Properties prop = new Properties();
12.     prop.load(new FileInputStream("jdbc-demo/src/druid.properties"));
13.     _//4. 获取连接池对象_
14.     DataSource dataSource = DruidDataSourceFactory.createDataSource(prop);

16.     _//5. 获取数据库连接 Connection_
17.     Connection conn = dataSource.getConnection();

19.     _//2. 定义SQL_
20.     String sql = "select \* from tb_brand;";

22.     _//3. 获取pstmt对象_
23.     PreparedStatement pstmt = conn.prepareStatement(sql);

25.     _//4. 设置参数_

27.     _//5. 执行SQL_
28.     ResultSet rs = pstmt.executeQuery();

30.     _//6. 处理结果 List&lt;Brand&gt; 封装Brand对象，装载List集合_
31.     Brand brand = null;
32.     List&lt;Brand&gt; brands = new ArrayList<>();
33.     while (rs.next()){
34.         _//获取数据_
35.         int id = rs.getInt("id");
36.         String brandName = rs.getString("brand_name");
37.         String companyName = rs.getString("company_name");
38.         int ordered = rs.getInt("ordered");
39.         String description = rs.getString("description");
40.         int status = rs.getInt("status");

42.         _//封装Brand对象_
43.         brand = new Brand();
44.         brand.setId(id);
45.         brand.setBrandName(brandName);
46.         brand.setCompanyName(companyName);
47.         brand.setOrdered(ordered);
48.         brand.setDescription(description);
49.         brand.setStatus(status);

51.         _//装载集合_
52.         brands.add(brand);

54.     }
55.     System.out.println(brands);
56.     _//7. 释放资源_
57.     rs.close();
58.     pstmt.close();
59.     conn.close();
60. }

#### 增加

1.  _/\*\*_
2.   \* 添加
3.   \* 1. SQL：insert into tb_brand(brand_name, company_name, ordered, description, status) values(?,?,?,?,?);
4.   \* 2. 参数：需要，除了id之外的所有参数信息
5.   \* 3. 结果：boolean
6.   \*/

8.  @Test
9.  public void testAdd() throws Exception {
10.     _// 接收页面提交的参数_
11.     String brandName = "香飘飘";
12.     String companyName = "香飘飘";
13.     int ordered = 1;
14.     String description = "绕地球一圈";
15.     int status = 1;
16.     _//1. 获取Connection_
17.     _//3. 加载配置文件_
18.     Properties prop = new Properties();
19.     prop.load(new FileInputStream("jdbc-demo/src/druid.properties"));
20.     _//4. 获取连接池对象_
21.     DataSource dataSource = DruidDataSourceFactory.createDataSource(prop);

23.     _//5. 获取数据库连接 Connection_
24.     Connection conn = dataSource.getConnection();

26.     _//2. 定义SQL_
27.     String sql = "insert into tb_brand(brand_name, company_name, ordered, description, status) values(?,?,?,?,?);";

29.     _//3. 获取pstmt对象_
30.     PreparedStatement pstmt = conn.prepareStatement(sql);

32.     _//4. 设置参数_
33.     pstmt.setString(1,brandName);
34.     pstmt.setString(2,companyName);
35.     pstmt.setInt(3,ordered);
36.     pstmt.setString(4,description);
37.     pstmt.setInt(5,status);

39.     _//5. 执行SQL_
40.     int count = pstmt.executeUpdate(); _// 影响的行数_

42.     _//6. 处理结果_
43.     System.out.println(count > 0);

1.      _//7. 释放资源_
2.      pstmt.close();
3.      conn.close();

5.  }

#### 修改

1.  _/\*\*_
2.   \* 修改
3.   \* 1. SQL：

5.   update tb_brand
6.       set brand_name  = ?,
7.       company_name= ?,
8.       ordered     = ?,
9.       description = ?,
10.      status      = ?
11.  where id = ?
12.  \* 2. 参数：需要，所有数据
13.  \* 3. 结果：boolean
14.  \*/

16. @Test
17. public void testUpdate() throws Exception {
18.     _// 接收页面提交的参数_
19.     String brandName = "香飘飘";
20.     String companyName = "香飘飘";
21.     int ordered = 1000;
22.     String description = "绕地球三圈";
23.     int status = 1;
24.     int id = 4;

26.     _//1. 获取Connection_
27.     _//3. 加载配置文件_
28.     Properties prop = new Properties();
29.     prop.load(new FileInputStream("jdbc-demo/src/druid.properties"));
30.     _//4. 获取连接池对象_
31.     DataSource dataSource = DruidDataSourceFactory.createDataSource(prop);

33.     _//5. 获取数据库连接 Connection_
34.     Connection conn = dataSource.getConnection();

36.     _//2. 定义SQL_
37.     String sql = " update tb_brand\\n" +
38.             "         set brand_name  = ?,\\n" +
39.             "         company_name= ?,\\n" +
40.             "         ordered     = ?,\\n" +
41.             "         description = ?,\\n" +
42.             "         status      = ?\\n" +
43.             "     where id = ?";

45.     _//3. 获取pstmt对象_
46.     PreparedStatement pstmt = conn.prepareStatement(sql);

48.     _//4. 设置参数_
49.     pstmt.setString(1,brandName);
50.     pstmt.setString(2,companyName);
51.     pstmt.setInt(3,ordered);
52.     pstmt.setString(4,description);
53.     pstmt.setInt(5,status);
54.     pstmt.setInt(6,id);

56.     _//5. 执行SQL_
57.     int count = pstmt.executeUpdate(); _// 影响的行数_
58.     _//6. 处理结果_
59.     System.out.println(count > 0);

61.     _//7. 释放资源_
62.     pstmt.close();
63.     conn.close();
64. }

#### 删除

1.  _/\*\*_
2.   \* 删除
3.   \* 1. SQL：

5.          delete from tb_brand where id = ?

7.   \* 2. 参数：需要，id
8.   \* 3. 结果：boolean
9.   \*/

11. @Test
12. public void testDeleteById() throws Exception {
13.     _// 接收页面提交的参数_
14.     int id = 4;

16.     _//1. 获取Connection_
17.     _//3. 加载配置文件_
18.     Properties prop = new Properties();
19.     prop.load(new FileInputStream("jdbc-demo/src/druid.properties"));

21.     _//4. 获取连接池对象_
22.     DataSource dataSource = DruidDataSourceFactory.createDataSource(prop);

24.     _//5. 获取数据库连接 Connection_
25.     Connection conn = dataSource.getConnection();

27.     _//2. 定义SQL_
28.     String sql = " delete from tb_brand where id = ?";

30.     _//3. 获取pstmt对象_
31.     PreparedStatement pstmt = conn.prepareStatement(sql);

33.     _//4. 设置参数_
34.     pstmt.setInt(1,id);

36.     _//5. 执行SQL_
37.     int count = pstmt.executeUpdate(); _// 影响的行数_

39.     _//6. 处理结果_
40.     System.out.println(count > 0);

42.     _//7. 释放资源_
43.     pstmt.close();
44.     conn.close();
45. }

## Maven

- Maven是专门用于管理和构建Java项目的工具
- 提供一套标准化的项目结构
- 提供一套标准化的构建流程（编译，测试，打包，发布）
- 提供一套依赖（第三方资源 插件 jar包）管理机制

### Maven简介

项目管理和构建工具，基于项目对象模型的概念，通过一小段描述信息来管理项目的构建，报告和文档

#### 仓库（repository）分类

本地仓库：自己计算机上的一个目录

中央仓库：有Maven团队维护的全球唯一的仓库

远程仓库（私服）：一般由公司团队搭建的私有仓库

当项目中使用坐标引入对应依赖jar包，首先会查找本地仓库中是否有对应的jar包：

如果有，则在项目中直接引用

如果没有，则去中央仓库中下载对应的jar包到本地仓库

### Maven基本使用

#### Maven常用命令

mvn compile 编译

mvn clean 清理

mvn test 测试

mvn package 打包

mvn install 安装

#### Maven生命周期

Maven构建项目生命周期描述的是一次构建过程经历了多少个事件

Maven对项目构建的生命周期划分为3套

同一生命周期内，执行后边的命令，前边的所有命令会自动执行

- Clean：清理工作

Preclean-clean-postclean

- default：核心工作，编译测试打包安装

compile-test-package-install

- Site：产生报告，发布站点

presite-site-postsite

#### Maven坐标

Maven中的坐标是资源的唯一标识

使用坐标来定义项目或引入项目中需要的依赖

Maven坐标主要组成

1.  groupid：定义当前Maven项目隶属组织名称（通常域名反写）
2.  Artifactid：定义当前Maven项目名称（通常是模块名称，例如order-service）
3.  Version：定义当前版本号

#### 使用坐标导入jar包

1.  在pom.xml中编写&lt;dependencies&gt;标签
2.  在&lt;dependencies&gt;标签中，使用&lt;dependencies&gt;引入坐标
3.  定义坐标的groupId,artifactId,version //_Alt+Insert_ 如果本地仓库有 模板生成
4.  点击刷新按钮，使坐标生效

#### 依赖管理

通过设置坐标的依赖范围（scope），可以设置对应jar包的作用范围：编译环境，测试环境，运行环境

依赖范围取值：  
compile；test；provided；runtime；system；import

| | | | | |

编译 测试 编译 测试 编译 引入DependencyManagement

测试 测试 运行 测试

运行

&lt;scope&gt;默认值:compile

Idea实用插件：Maven Helper

## MyBatis

- MyBitis 一款持久层框架，用于简化JDBC开发

|

持久层：负责将数据保存到数据库的那一层代码

\--JavaEE三层框架：表现层，业务层，持久层

|

框架：

框架是一个半成品软件，一套可重用，通用，软件基础代码模型

在框架基础之上构建软件编写更加高效，规范，通用，可扩展

- JDBC缺点
- 硬编码 -配置文件

注册驱动，获取连接

SQL语句

- 操作繁琐 -自动完成

手动设置参数

手动封装结果集

### MyBatis快速入门

查询user表中所有数据

1.  创建user表，添加数据（在navicat中完成）
2.  创建模块，导入坐标
3.  编写Mybatis核心配置文件 --- 替换连接信息 解决硬编码问题

Mybatis-config.xml

1.  &lt;?xml version="1.0" encoding="UTF-8" ?&gt;
2.  <!DOCTYPE configuration
3.          PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
4.          "http://mybatis.org/dtd/mybatis-3-config.dtd">
5.  &lt;configuration&gt;
6.      &lt;environments default="development"&gt;
7.          &lt;environment id="development"&gt;
8.              &lt;transactionManager type="JDBC"/&gt;
9.              &lt;dataSource type="POOLED"&gt;

11.                 &lt;property name="driver" value="com.mysql.jdbc.Driver"/&gt;
12.                 &lt;property name="url" value="jdbc:mysql:///mybatis?useSSL=false"/&gt;
13.                 &lt;property name="username" value="root"/&gt;
14.                 &lt;property name="password" value="1234"/&gt;
15.             &lt;/dataSource&gt;
16.         &lt;/environment&gt;
17.     &lt;/environments&gt;
18.     &lt;mappers&gt;
19. &lt;!--加载sql映射文件--&gt;
20.         &lt;mapper resource="UserMapper.xml"/&gt;
21.     &lt;/mappers&gt;
22. &lt;/configuration&gt;

1.  编写SQL映射文件 --- 统一管理sql语句 解决硬编码问题

操作User表就定义UserMapper.xml

1.  &lt;?xml version="1.0" encoding="UTF-8" ?&gt;
2.  <!DOCTYPE mapper
3.          PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
4.          "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

6.  &lt;mapper namespace="test"&gt;
7.      &lt;select id="selectAll" resultType="com.itheima.pojo.User"&gt;
8.          select \* from tb_user;
9.      &lt;/select&gt;
10. &lt;/mapper&gt;
11. 编码
12. 定义pojo类
13. public class User {

15.     private Integer id;
16.     private String username;
17.     private String password;
18.     private String gender;
19.     private String addr;

21.      @setter
22. @getter

24.     @Override
25.     public String toString() {
26.         return "User{" +
27.                 "id=" + id +
28.                 ", username='" + username + '\\'' +
29.                 ", password='" + password + '\\'' +
30.                 ", gender='" + gender + '\\'' +
31.                 ", addr='" + addr + '\\'' +
32.                 '}';
33.     }
34. }

1.  加载核心配置文件，获取SqlSessionFactory对象
2.  获取SqlSession对象，执行SQL语句
3.  释放资源
4.  public static void main(String\[\] args) throws IOException {

6.      _//1. 加载mybatis的核心配置文件，获取 SqlSessionFactory_
7.      String resource = "mybatis-config.xml";
8.      InputStream inputStream = Resources.getResourceAsStream(resource);
9.      SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

11.     _//2. 获取SqlSession对象，用它来执行sql_
12.     SqlSession sqlSession = sqlSessionFactory.openSession();

14.     _//3. 执行sql 传入名称空间.唯一标识_
15.     List&lt;User&gt; users = sqlSession.selectList("test.selectAll");
16.     System.out.println(users);

18.     _//4. 释放资源_
19.     sqlSession.close();
20. }

### Mapper代理开发

1.  定义与SQL映射文件同名的Mapper接口，并将Mapper接口和SQL映射文件放在同一目录

在resource下创建directory时用分隔符：/来代替”.”

public interface UserMapper {

&nbsp;   List&lt;User&gt; selectAll();

}

1.  设置SQL映射文件的namespace属性为Mapper接口全限定名

&lt;mapper namespace="com.itheima.mapper.UsrMapper"&gt;

1.  在Mapper接口中定义方法，方法名就是SQL映射文件中sql语句中的id，并保持参数类型和返回值类型一致
2.  编码
3.  通过SqlSession的getMapper方法获取Mapper接口的代理对象
4.  调用对应方法完成sql的执行

1.  public static void main(String\[\] args) throws IOException {

3.      _//1. 加载mybatis的核心配置文件，获取 SqlSessionFactory_
4.      String resource = "mybatis-config.xml";
5.      InputStream inputStream = Resources.getResourceAsStream(resource);
6.      SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

8.      _//2. 获取SqlSession对象，用它来执行sql_
9.      SqlSession sqlSession = sqlSessionFactory.openSession();

11.     _//3. 执行sql_
12.     _//List&lt;User&gt; users = sqlSession.selectList("test.selectAll");_
13.     _//System.out.println(users);_

15.     _//3.1获取UserMapper接口的代理对象_
16.     UserMapper userMapper = sqlSession.getMapper(UserMapper.class);
17.     List&lt;User&gt; users = userMapper.selectAll();

19.     _//4. 释放资源_
20.     sqlSession.close();

22. }

如果Mapper接口和SQL映射文件名称相同，并在同一目录下，则可以使用包扫描的方式简化SQL映射文件的加载

1.  &lt;mappers&gt;
2.  &lt;!--加载sql的映射文件--&gt;
3.  &lt;!-- <mapper resource="com/itheima/mapper/UserMapper.xml"/&gt;-->
4.      &lt;package name="com.itheima.mapper"/&gt;
5.  &lt;/mappers&gt;

### MyBatis核心配置文件

Mybatis-config.xml配置文件

1.  Environment

配置数据库连接环境信息。可以配置多个environment，通过default属性切换不同的environment

&lt;environment default="   "&gt;

1.  配置别名 可不区分大小写

&lt;typeAliases&gt;

&nbsp;       &lt;package name ="com.itheima.pojo"/&gt;

&lt;/typeAliases&gt;

### 配置文件完成增删改查

例：完成品牌数据的增删改查操作

#### 环境准备

数据库表tb_brand

实体类Brand

测试用例

安装MyBatisX插件 实现XML和接口方法跳转，根据接口方法生成statement

#### 查询-所有数据

1.  编写接口方法：Mapper接口 -Mapper-Brandmapper

- 参数：无
- 结果：List&lt;Brand&gt;

1.  public interface BrandMapper {
2.      _/\*\*_
3.       \* 查询所有
4.       \*/
5.      List&lt;Brand&gt; selectAll();
6.  }

1.  编写SQL语句：SQL映射文件 -BrandMapper.xml
2.  &lt;select id="selectAll" resultType="com.itheima.pojo.Brand"&gt;

别名 brand

1.      select \* from tb_brand;
2.  &lt;/select&gt;

1.  执行方法，测试
2.  @Test
3.  public void testSelectAll() throws Exception {
4.      _//1.获取SqlSessionFactory_
5.     String resource = "mybatis-config.xml";
6.     InputStream inputStream = Resources.getResourceAsStream(resource);
7.     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

9.     _//2. 获取SqlSession对象_
10.    SqlSession sqlSession = sqlSessionFactory.openSession();

12.    _//3.获取Mapper接口的代理对象_
13.     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

15.     _//4.执行方法_
16.     List&lt;Brand&gt; brands = brandMapper.selectAll();
17.     System.out.println(brands);

19.     _//5.释放资源_
20.     sqlSession.close();

22. }

1.  执行后问题

部分数据没有成功加载

原因：数据库表的名称字段和实体类的属性名称不一样，则不能自动封装

pojo实体类Brand中Brand字段

MySQL中Brand字段

解决：

1.  起别名：//缺点：每次查询都需要定义一次别名

select id,brand_name,company_name,ordered,description,status 

from tb_brand;

\--使用别名

select 

id,

brand_name as brandName,

company_name as companyName,

ordered,

Description,

status 

from tb_brand;

1.  Sql片段 //不灵活
2.  &lt;sql id="brand_column"&gt;
3.       id,
4.  brandName as brandName,
5.  companyName as companyName,
6.  ordered,
7.  description,
8.  status
9.  &lt;/sql&gt;

11. &lt;select id="selectAll" resultType="com.itheima.pojo.Brand"&gt;
12.     select 
13.         &lt;include refid="brand_column"/&gt;    
14.     from tb_brand;
15. &lt;/select&gt;

1.  resultMap 完成不一致的属性名和列名的映射
2.  &lt;!-- id：唯一标识 type 映射的类型 支持别名--&gt;
3.  &lt;resultMap id="brandResultMap" type="brand"&gt;
4.  <!--
5.  id:完成主键字段的映射
6.  result：完成一般字段的映射
7.  \-->
8.      &lt;result column="brand_name" property="brandName"/&gt;
9.      &lt;result column="company_name" property="companyName"/&gt;
10. &lt;/resultMap&gt;

12. &lt;!-- 将resultType 更改成resultMap--&gt;
13. &lt;select id="selectAll" resultMap="brandResultMap"&gt;
14.     select 
15. \* 
16. from tb_brand;
17. &lt;/select&gt;

#### 查看详情

1.  编写接口方法：Mapper接口

- 参数：id
- 结果：brand

1.  _/\*\*_
2.  \* 查看详情 根据id查询
3.  \*/
4.  Brand selectById(int id);

1.  编写SQL语句：SQL映射文件
2.  参数占位符：

#{}：会将其替换为 ？.为了防止SQL注入

${}：拼sql，会存在SQL注入问题

使用时机：参数传递时：#{}

表名或列名不固定情况下：${} 会存在SQL注入问题

1.  参数类型：

parameterType:可以省略

1.  特殊字符处理

\* 转义字符

\* CDATA区

<!\[CDATA\[

...(特殊字符)

\]\]>

1.  &lt;select id="selectById" resultMap="brandResultMap"&gt;
2.      select
3.          \*
4.      from tb_brand where id = _#{id};_
5.  &lt;/select&gt;

1.  执行方法，测试
2.  @Test
3.  public void testSelectById() throws Exception {
4.      _//0.接受参数_
5.      int id = 1;

7.      _//1.获取SqlSessionFactory_
8.      String resource = "mybatis-config.xml";
9.      InputStream inputStream = Resources.getResourceAsStream(resource);
10.     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

12.     _//2. 获取SqlSession对象_
13.     SqlSession sqlSession = sqlSessionFactory.openSession();

15.     _//3.获取Mapper接口的代理对象_
16.     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

18.     _//4.执行方法_
19.     Brand brand = brandMapper.selectById(id);
20.     System.out.println(brand);

22.     _//5.释放资源_
23.     sqlSession.close();

25. }

#### 条件查询

- 多条件查询

1.  编写接口方法：Mapper接口

- 参数：所有查询条件
- 结果：List&lt;Brand&gt;

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

13. List&lt;Brand&gt; selectByCondition(@Param("status")int status,@Param("companyName")String companyName,@Param("brandName")String brandName);

15. }
16. 对象参数：对象中的属性名称要和SQL参数占位符名称一致

List&lt;Brand&gt; selectByCondition(Brand brand);

1.  对象参数：对象中的属性名称要和SQL参数占位符名称一致

List&lt;Brand&gt; selectByCondition(Map map);

1.  编写SQL语句：SQL映射文件
2.  _<!--_
3.  条件查询
4.  \-->
5.  &lt;select id="selectByCondition" resultMap="brandResultMap"&gt;
6.      select
7.          \*
8.      from tb_brand
9.      where
10.         status = #{status}
11.        and company_name like #{companyName}
12.        and brand_name like #{brandName}
13. &lt;/select&gt;

1.  执行方法，测试
2.  @Test
3.      public void testSelectByCondition() throws Exception {
4.          _//0.接受参数_
5.          int status = 1;
6.          String companyName = "华为";
7.          String brandName = "华为";

9.          _//处理参数_
10.         companyName = "%" + companyName + "%";
11.         brandName = "%" + brandName + "%";

13. _//        //封装对象 对应对象参数接收_
14. _//        Brand brand = new Brand();_
15. _//        brand.setStatus(status);_
16. _//        brand.setCompanyName(companyName);_
17. _//        brand.setBrandName(brandName);_

19. _//封装对象 对应map参数接受_
20.         Map map = new HashMap<>();
21.         map.put("status",status);
22.         map.put("companyName",companyName);
23.         map.put("brandName",brandName);

25.         _//1.获取SqlSessionFactory_
26.         String resource = "mybatis-config.xml";
27.         InputStream inputStream = Resources.getResourceAsStream(resource);
28.         SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

30.         _//2. 获取SqlSession对象_
31.         SqlSession sqlSession = sqlSessionFactory.openSession();

33.         _//3.获取Mapper接口的代理对象_
34.         BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

36.         _//4.执行方法_
37. _//        List&lt;Brand&gt; brands = brandMapper.selectByCondition(status, companyName, brandName); //对应散装参数接收_
38. _//        List&lt;Brand&gt; brands = brandMapper.selectByCondition(brand);//对应对象参数接收_
39.         List&lt;Brand&gt; brands = brandMapper.selectByCondition(map);_//对应Map参数接收_
40.         System.out.println(brands);

42.         _//5.释放资源_
43.         sqlSession.close();

46.     }

1.  存在问题

用户输入条件时，是否所有条件都会填写？

优化：动态条件查询

- 多条件-动态条件查询

动态SQL ：SQL语句会随着用户的输入或外部条件的变化而变化

BrandMapper.xml

1.  &lt;select id="selectByCondition" resultMap="brandResultMap"&gt;
2.      select
3.          \*
4.      from tb_brand
5.      where
6.          &lt;if test="status != null"&gt;
7.              status = _#{status}_
8.          &lt;/if&gt;
9.      &lt;if test="companyName != null and companyName != ''"&gt;
10.         and company_name like _#{companyName}_
11.     &lt;/if&gt;
12.     &lt;if test="brandName != null and brandName != ''"&gt;
13.         and brand_name like _#{brandName}_
14.     &lt;/if&gt;

16. &lt;/select&gt;

test=”条件”条件中使用其真正输入的值而不是属性 即companyName

1.  存在问题

如果第一个条件不存在的话，会多出一个and，MySQL语法错误

优化

1.  每个语句都加and，并且在where后加上1 = 1 恒等式
2.  &lt;select id="selectByCondition" resultMap="brandResultMap"&gt;
3.      select
4.          \*
5.      from tb_brand
6.      where 1 = 1
7.          &lt;if test="status != null"&gt;
8.          and status = _#{status}_
9.          &lt;/if&gt;
10.     &lt;if test="companyName != null and companyName != ''"&gt;
11.         and company_name like _#{companyName}_
12.     &lt;/if&gt;
13.     &lt;if test="brandName != null and brandName != ''"&gt;
14.         and brand_name like _#{brandName}_
15.     &lt;/if&gt;

17. &lt;/select&gt;

1.  where 标签（较常用）
2.  &lt;select id="selectByCondition" resultMap="brandResultMap"&gt;
3.      select
4.          \*
5.      from tb_brand
6.      &lt;where&gt;
7.          &lt;if test="status != null"&gt;
8.          and status = _#{status}_
9.          &lt;/if&gt;
10.     &lt;if test="companyName != null and companyName != ''"&gt;
11.         and company_name like _#{companyName}_
12.     &lt;/if&gt;
13.     &lt;if test="brandName != null and brandName != ''"&gt;
14.         and brand_name like _#{brandName}_
15.     &lt;/if&gt;
16.     &lt;/where&gt;

18. &lt;/select&gt;

- 单条件-动态条件查询
- 从多个条件中选择一个
- choose（when，otherwise）：选择，类似于Java中的switch语句

1.  编写接口方法：Mapper接口

- 参数：查询条件
- 结果：List&lt;Brand&gt;

List&lt;Brand&gt; selectByConditionSingle(Brand brand);

1.  编写SQL语句：SQL映射文件
2.  &lt;/select&gt;
3.  &lt;select id="selectByConditionSingle" resultMap="brandResultMap"&gt;
4.      select
5.          \*
6.      from tb_brand
7.      where
8.      &lt;choose&gt;_&lt;!--相当于switch--&gt;_
9.          &lt;when test="status != null"&gt;_&lt;!--相当于case--&gt;_
10.             status = #{status}
11.         &lt;/when&gt;
12.         &lt;when test="companyName != null and companyName != ''"&gt; _&lt;!--相当于case--&gt;_
13.             company_name like #{companyName}
14.         &lt;/when&gt;
15.         &lt;when test="brandName != null and brandName != ''"&gt;_&lt;!--相当于case--&gt;_
16.             brand_name like #{brandName}
17.         &lt;/when&gt;
18.     &lt;/choose&gt;
19. &lt;/select&gt;

1.  执行方法，测试
2.      @Test
3.      public void testSelectByConditionSingle() throws Exception {
4.          _//0.接受参数_
5.          int status = 1;
6.          String companyName = "华为";
7.          String brandName = "华为";

9.          _//处理参数_
10.         companyName = "%" + companyName + "%";
11.         brandName = "%" + brandName + "%";

13.         _//封装对象 对应对象参数接收_
14.         Brand brand = new Brand();
15.         brand.setStatus(status);
16.         brand.setCompanyName(companyName);
17.         brand.setBrandName(brandName);

19. _//        Map map = new HashMap<>();_
20. _//        map.put("status",status);_
21. _//        map.put("companyName",companyName);_
22. _//        map.put("brandName",brandName);_

24.         _//1.获取SqlSessionFactory_
25.         String resource = "mybatis-config.xml";
26.         InputStream inputStream = Resources.getResourceAsStream(resource);
27.         SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

29.         _//2. 获取SqlSession对象_
30.         SqlSession sqlSession = sqlSessionFactory.openSession();

32.         _//3.获取Mapper接口的代理对象_
33.         BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

35.         _//4.执行方法_
36.         List&lt;Brand&gt; brands = brandMapper.selectByConditionSingle(brand);
37.         System.out.println(brands);

39.         _//5.释放资源_
40.         sqlSession.close();

43.     }

1.  存在问题

如果用户一个都不选，语法会报错

优化：恒等式

1.  &lt;otherwise&gt;_&lt;!--相当于default--&gt;_
2.     1=1
3.  &lt;/otherwise&gt;

#### 添加

5.1 添加

1.  编辑接口方法：Mapper接口

- 参数：除了id之外的所有数据
- 结果：void

void add(Brand brand);

1.  编写SQL语句：SQL映射文件
2.  &lt;insert id="add"&gt;
3.      insert into tb_brand (brand_name,company_name,ordered,description,status)
4.      values (#{brandName},#{companyName},#{ordered},#{description},#{status});
5.  &lt;/insert&gt;

1.  执行方法，测试
2.  @Test
3.  public void add() throws Exception {
4.      _//0.接受参数_
5.      int status = 1;
6.      String companyName = "波导手机";
7.      String brandName = "波导";
8.      String description = "手机中的战斗机";
9.      int ordered = 100;

11.     _//封装对象 对应对象参数接收_
12.     Brand brand = new Brand();
13.     brand.setStatus(status);
14.     brand.setCompanyName(companyName);
15.     brand.setBrandName(brandName);
16.     brand.setDescription(description);
17.     brand.setOrdered(ordered);

19.     _//1.获取SqlSessionFactory_
20.     String resource = "mybatis-config.xml";
21.     InputStream inputStream = Resources.getResourceAsStream(resource);
22.     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

24.     _//2. 获取SqlSession对象_
25.     SqlSession sqlSession = sqlSessionFactory.openSession();

27.     _//3.获取Mapper接口的代理对象_
28.     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

30.     _//4.执行方法_
31.     brandMapper.add(brand);

33. _//提交事务_
34.     sqlSession.commit();

36.     _//5.释放资源_
37.     sqlSession.close();

39. }
40. 优化

需要手动提交事务

可在获取Sqlsession对象时 可以传递布尔值

SqlSession sqlSession = sqlSessionFactory.openSession(true);

则可省略#33行

5.2添加-主键返回

在数据添加成功后，需要插入数据库数据的主键的值

1.  &lt;insert id="add" useGeneratedKeys="true" keyProperty="id"&gt;
2.      insert into tb_brand 
3.  (brand_name,company_name,ordered,description,status)
4.      values 
5.  (#{brandName},#{companyName},#{ordered},#{description},#{status});
6.  &lt;/insert&gt;

#### 修改

6.1 修改全部字段

1.  编写接口方法：Mapper接口

- 参数：所有数据
- 结果：void/受影响的行数

int update (Brand brand);

1.  编写SQL语句：SQL映射文件
2.  &lt;update id="update"&gt;
3.      update tb_brand 
4.      set 
5.  brand_name = _#{brandName},_
6.  _company_name = #{companyName},_
7.  _ordered = #{ordered},_
8.  _description = #{description},_
9.  _status = #{status}_ 
10. where _id = #{id};_
11. &lt;/update&gt;

1.  执行方法，测试
2.  @Test
3.  public void testUpdate() throws Exception {
4.      _//0.接受参数_
5.      int status = 1;
6.      String companyName = "波导手机";
7.      String brandName = "波导";
8.      String description = "波导手机，手机中的战斗机";
9.      int ordered = 200;
10.     int id = 4;

12.     _//封装对象 对应对象参数接收_
13.     Brand brand = new Brand();
14.     brand.setStatus(status);
15.     brand.setCompanyName(companyName);
16.     brand.setBrandName(brandName);
17.     brand.setDescription(description);
18.     brand.setOrdered(ordered);
19.     brand.setId(id);

21.     _//1.获取SqlSessionFactory_
22.     String resource = "mybatis-config.xml";
23.     InputStream inputStream = Resources.getResourceAsStream(resource);
24.     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

26.     _//2. 获取SqlSession对象_
27.     SqlSession sqlSession = sqlSessionFactory.openSession(true);

29.     _//3.获取Mapper接口的代理对象_
30.     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

32.     _//4.执行方法_
33.     int count = brandMapper.update(brand);
34.     System.out.println(count);

37.     _//5.释放资源_
38.     sqlSession.close();

40. }

6.2 修改动态字段

1.  编写接口方法：Mapper接口

- 参数：部分数据，封装到对象中
- 结果：void

1.  编写SQL语句：SQL映射文件
2.  &lt;update id="update"&gt;
3.      update tb_brand
4.      &lt;set&gt;
5.          &lt;if test="brandName != null and brandName != ''"&gt;
6.          brand_name = _#{brandName},_
7.          &lt;/if&gt;
8.           &lt;if test="companyName != null and companyName != ''"&gt;
9.          company_name = _#{companyName},_
10.          &lt;/if&gt;
11.         &lt;if test="ordered != null "&gt;
12.         ordered = _#{ordered},_
13.         &lt;/if&gt;
14.         &lt;if test="description != null and description != ''"&gt;
15.             description = _#{description},_
16.         &lt;/if&gt;
17.         &lt;if test="status != null "&gt;
18.         status = _#{status}_
19.         &lt;/if&gt;
20.     &lt;/set&gt;
21.          where id = _#{id};_
22. &lt;/update&gt;

1.  执行方法，测试

1.  删除

7.1删除一个

1.  编写接口方法：Mapper接口

- 参数：id值
- 结果：void

void deleteById(int id);

1.  编写SQL语句：SQL映射文件
2.  &lt;delete id="deleteById"&gt;
3.      delete from tb_brand where id = _#{id};_
4.  &lt;/delete&gt;

1.  执行方法，测试
2.  @Test
3.  public void testDelete() throws Exception {
4.      _//0.接受参数_
5.      int id = 6;

7.      _//封装对象 对应对象参数接收_
8.      Brand brand = new Brand();
9.      brand.setId(id);

11.     _//1.获取SqlSessionFactory_
12.     String resource = "mybatis-config.xml";
13.     InputStream inputStream = Resources.getResourceAsStream(resource);
14.     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

16.     _//2. 获取SqlSession对象_
17.     SqlSession sqlSession = sqlSessionFactory.openSession(true);

19.     _//3.获取Mapper接口的代理对象_
20.     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

22.     _//4.执行方法_
23.     brandMapper.deleteById(id);

25.     _//5.释放资源_
26.     sqlSession.close();

28. }

7.2批量删除

1.  编写接口方法：Mapper接口

- 参数：id数组
- 结果：void

void deleteByIds(@Param("ids") int\[\] ids);

1.  编写SQL语句：SQL映射文件
2.  &lt;delete id="deleteByIds"&gt;
3.      delete from tb_brand where id
4.      in (
5.          &lt;foreach collection="ids" item="id" separator=","open="(" close=")"&gt;
6.              _#{id}#{id}#{id}_
7.          &lt;/foreach&gt;
8.          )
9.  &lt;/delete&gt;

1.  执行方法，测试
2.  @Test
3.  public void testDeleteByIds() throws Exception {
4.      _//0.接受参数_
5.      int\[\]ids = {5,7,8};

8.      _//1.获取SqlSessionFactory_
9.      String resource = "mybatis-config.xml";
10.     InputStream inputStream = Resources.getResourceAsStream(resource);
11.     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

13.     _//2. 获取SqlSession对象_
14.     SqlSession sqlSession = sqlSessionFactory.openSession(true);

16.     _//3.获取Mapper接口的代理对象_
17.     BrandMapper brandMapper = sqlSession.getMapper(BrandMapper.class);

19.     _//4.执行方法_
20.     brandMapper.deleteByIds(ids);

22.     _//5.释放资源_
23.     sqlSession.close();

1.  优化

open="(" close=")"

### MyBatis参数查询

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

## HTML

- HTML（HyperText Markup Language）是一种语言，所有语言都是用HTML语言编写出来的
- 标记语言：由标签构成的语言
- HTML运行在浏览器上，HTML标签由浏览器来解析
- HTML标签都是预定义好的。例如：使用&lt;img&gt;展示图片
- W3C标准：网页主要由三部分组成
- 结构：HTML
- 表现：CSS
- 行为：JavaScript

### HTML快速入门

1.  &lt;html&gt;
2.      &lt;head&gt;
3.          &lt;title&gt;hello html&lt;/title&gt;
4.      &lt;/head&gt;
5.      &lt;body&gt;
6.          &lt;font color = "red"&gt;htmllllll&lt;/font&gt;
7.      &lt;/body&gt;
8.  &lt;/html&gt;

1.  HTML文件以.htm或.html为扩展名
2.  HTML结构标签

- &lt;HTML&gt; 定义HTML文档
- &lt;head&gt; 定义关于文档的信息
- &lt;title&gt; 定义文档的标题
- &lt;body&gt; 定义文档的主题

1.  HTML标签不区分大小写
2.  HTML标签属性值 单双引皆可
3.  语法松散

### HTML标签

#### 基础标签

&lt;h1&gt;-&lt;h6&gt; 定义标题，h1最大，h6最小

&lt;b&gt; 定义粗体文本

&lt;i&gt; 定义斜体文本 &lt;u&gt; 定义文本下划线

&lt;p&gt; 定义段落&lt;center&gt; 定义文本居中

&lt;br&gt; 定义新行&lt;hr&gt; 水平分割线

html表示颜色：

1.  英文单词：red,pink,blue..
2.  RGB表示（值1，值2，值3）取值范围0-255
3.  #值1 #值2 #值3 ; 值的范围00~FF 十六进制表示

1.  _&lt;!-- html5 标识--&gt;_
2.  &lt;!DOCTYPE html&gt;
3.  &lt;html lang="en"&gt;
4.  &lt;head&gt;
5.      _&lt;!-- 页面的字符集--&gt;_
6.      &lt;meta charset="UTF-8"&gt;
7.      &lt;title&gt;Title&lt;/title&gt;
8.  &lt;/head&gt;
9.  &lt;body&gt;

11. &lt;h1&gt;我是标题 h1&lt;/h1&gt;
12. &lt;h2&gt;我是标题 h2&lt;/h2&gt;
13. &lt;h3&gt;我是标题 h3&lt;/h3&gt;
14. &lt;h4&gt;我是标题 h4&lt;/h4&gt;
15. &lt;h5&gt;我是标题 h5&lt;/h5&gt;
16. &lt;h6&gt;我是标题 h6&lt;/h6&gt;

18. &lt;hr&gt;
19. _<!--_
20.     html 表示颜色：
21.         1. 英文单词：red,pink,blue...
22.         2. rgb(值1,值2,值3)：值的取值范围：0~255  rgb(255,0,0)
23.         3. #值1值2值3：值的范围：00~FF
24. \-->
25. &lt;font face="楷体" size="5" color="#ff0000"&gt;传智教育&lt;/font&gt;

27. &lt;hr&gt;

29. 刚察草原绿草如茵，沙柳河水流淌入湖。藏族牧民索南才让家中，茶几上摆着馓子、麻花和水果，炉子上刚煮开的奶茶香气四溢……&lt;br&gt;

31. 6月8日下午，习近平总书记来到青海省海北藏族自治州刚察县沙柳河镇果洛藏贡麻村，走进牧民索南才让家中，看望慰问藏族群众。

33. &lt;hr&gt;
34. &lt;p&gt;
35. 刚察草原绿草如茵，沙柳河水流淌入湖。藏族牧民索南才让家中，茶几上摆着馓子、麻花和水果，炉子上刚煮开的奶茶香气四溢……
36. &lt;/p&gt;
37. &lt;p&gt;6月8日下午，习近平总书记来到青海省海北藏族自治州刚察县沙柳河镇果洛藏贡麻村，走进牧民索南才让家中，看望慰问藏族群众。
38. &lt;/p&gt;
39. &lt;hr&gt;

41. 沙柳河水流淌&lt;br&gt;
42. 
43. &lt;b&gt;沙柳河水流淌&lt;/b&gt;&lt;br&gt;
44. &lt;i&gt;沙柳河水流淌&lt;/i&gt;&lt;br&gt;
45. &lt;u&gt;沙柳河水流淌&lt;/u&gt;&lt;br&gt;

47. &lt;hr&gt;
48. &lt;center&gt;
49. &lt;b&gt;沙柳河水流淌&lt;/b&gt;
50. &lt;/center&gt;
51. &lt;/body&gt;
52. &lt;/html&gt;

#### 图片，音频，视频标签

&lt;img&gt; 定义图片

&lt;audio&gt; 定义音频

&lt;video&gt; 定义视频

1.  img：定义图片

- Src: 规定显示图像的URL（统一资源定位符）
- Height：定义图像的高度
- Width：定义图像的宽度

1.  &lt;img src="../img/a.jpg" width="300" height="400"&gt;
2.  audio：定义音频，支持的音频格式：MP3，WAV，OGG

- Src：规定的音频的URL
- Controls：显示播放控件

1.  &lt;audio src="b.mp3" controls&gt;&lt;/audio&gt;
2.  Video：定义视频，支持的视频格式：MP4,WebM,OGG

- Src：规定视频的URL
- Controls：显示播放控件

1.  &lt;video src="c.mp4" controls width="500" height="300"&gt;&lt;/video&gt;

注：资源路径：

1.  绝对路径：完整路径
2.  相对路径：相对位置关系

#### 超链接标签

&lt;a&gt; 定义超链接

Href：指定访问资源的URL

Target：指定打开资源的方式

- \_self：默认值，在当前页面打开
- \_blank：在空白页面打开

1.  &lt;a href="https://www.itcast.cn" target="\_blank"&gt;点我有惊喜&lt;/a&gt;

#### 列表标签

1.  有序列表（order list）
2.  无序列表（unorder list）

&lt;ol&gt; 定义有序列表

&lt;ul&gt; 定义无序列表

&lt;li&gt; 定义列表项

1.  &lt;ol type="A"&gt;
2.      &lt;li&gt;咖啡&lt;/li&gt;
3.      &lt;li&gt;茶&lt;/li&gt;
4.      &lt;li&gt;牛奶&lt;/li&gt;
5.  &lt;/ol&gt;

8.  &lt;ul type="circle"&gt;
9.      &lt;li&gt;咖啡&lt;/li&gt;
10.     &lt;li&gt;茶&lt;/li&gt;
11.     &lt;li&gt;牛奶&lt;/li&gt;
12. &lt;/ul&gt;

Type设置项目符号 不推荐使用

#### 表格标签

&lt;table&gt; 定义有序列表

&lt;tr&gt; 定义行

&lt;td&gt; 定义单元格

&lt;th&gt; 定义表头单元格

1.  table：定义表格

- Border：规定表格边框的宽度
- Width：规定表格的宽度
- Cellspacing：规定单元格之间的空白

1.  tr：定义行

- Align：定义行的对齐方式

1.  td：定义单元格

- rowspan：规定单元格可横跨的行数
- colspan：规定单元格可横跨的列数

1.  &lt;table border="1" cellspacing="0" width="500"&gt;
2.      &lt;tr&gt;
3.          &lt;th&gt;序号&lt;/th&gt;
4.          &lt;th&gt;品牌logo&lt;/th&gt;
5.          &lt;th&gt;品牌名称&lt;/th&gt;
6.          &lt;th&gt;企业名称&lt;/th&gt;

8.      &lt;/tr&gt;
9.      &lt;tr align="center"&gt;
10.         &lt;td&gt;010&lt;/td&gt;
11.         &lt;td&gt;&lt;img src="../img/三只松鼠.png" width="60" height="50"&gt;&lt;/td&gt;
12.         &lt;td&gt;三只松鼠&lt;/td&gt;
13.         &lt;td&gt;三只松鼠&lt;/td&gt;
14.     &lt;/tr&gt;

16.     &lt;tr align="center"&gt;
17.         &lt;td&gt;009&lt;/td&gt;
18.         &lt;td&gt;&lt;img src="../img/优衣库.png" width="60" height="50"&gt;&lt;/td&gt;
19.         &lt;td&gt;优衣库&lt;/td&gt;
20.         &lt;td&gt;优衣库&lt;/td&gt;
21.     &lt;/tr&gt;

23.     &lt;tr align="center"&gt;
24.         &lt;td&gt;008&lt;/td&gt;
25.         &lt;td&gt;&lt;img src="../img/小米.png" width="60" height="50"&gt;&lt;/td&gt;
26.         &lt;td&gt;小米&lt;/td&gt;
27.         &lt;td&gt;小米科技有限公司&lt;/td&gt;
28.     &lt;/tr&gt;

31. &lt;/table&gt;

对逐行进行编辑

#### 布局标签

&lt;div&gt; 定义html文档中的一个区域部分，经常与CSS一起使用。用来布局网页

&lt;span&gt; 用来组合行内元素

#### 表单标签

表单：在网页中主要负责数据采集功能，使用&lt;form&gt;标签定义表单

表单项（元素）：不同类型的input元素，下拉列表，文本域等

&lt;form&gt; 定义表单

&lt;input&gt; 定义表单项，通过type属性控制输入形式

&lt;label&gt; 为表单项定义标注

&lt;select&gt; 定义下拉列表

&lt;option&gt; 定义下拉列表的列表项

&lt;textarea&gt; 定义文本域

Form：定义表单

- action：规定当提交表单时向何处发送表单数据，URL
- method：规定用于发送表单数据的方式
- Get：浏览器会将数据附在表单的action URL之后，大小有限制
- Post：浏览器会将数据放到http请求协议的请求体中，大小无限制

1.      &lt;form action="#" method="post/get"&gt;
2.          &lt;input type="text" name="username"&gt;
3.          &lt;input type="submit"&gt;
4.      &lt;/form&gt;

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

1.  &lt;form action="#" method="post"&gt;
2.      &lt;input type="hidden" name="id" value="123"&gt;

5.      &lt;label for="username"&gt;用户名：&lt;/label&gt;
6.      &lt;input type="text" name="username" id="username"&gt;&lt;br&gt;

8.      &lt;label for="password"&gt;密码：&lt;/label&gt;
9.      &lt;input type="password" name="password" id="password"&gt;&lt;br&gt;

11.     性别：
12.     &lt;input type="radio" name="gender" value="1" id="male"&gt; &lt;label for="male"&gt;男&lt;/label&gt;
13.     &lt;input type="radio" name="gender" value="2" id="female"&gt; &lt;label for="female"&gt;女&lt;/label&gt;
14.     &lt;br&gt;

16.     爱好：
17.     &lt;input type="checkbox" name="hobby" value="1"&gt; 旅游
18.     &lt;input type="checkbox" name="hobby" value="2"&gt; 电影
19.     &lt;input type="checkbox" name="hobby" value="3"&gt; 游戏
20.     &lt;br&gt;

22.     头像：
23.     &lt;input type="file"&gt;&lt;br&gt;

25.     城市:
26.     &lt;select name="city"&gt;
27.         &lt;option&gt;北京&lt;/option&gt;
28.         &lt;option value="shanghai"&gt;上海&lt;/option&gt;
29.         &lt;option&gt;广州&lt;/option&gt;
30.     &lt;/select&gt;
31.     &lt;br&gt;

33.     个人描述：
34.     &lt;textarea cols="20" rows="5" name="desc"&gt;&lt;/textarea&gt;
35.     &lt;br&gt;
36.     &lt;br&gt;
37.     &lt;input type="submit" value="免费注册"&gt;
38.     &lt;input type="reset" value="重置"&gt;
39.     &lt;input type="button" value="一个按钮"&gt;
40. &lt;/form&gt;

### CSS

css是一门语言，用于控制网页表现，Cacading Style Sheet：层叠样式表

#### CSS导入方式

CSS导入HTML有三种方式：

1.  内联样式：在标签内部使用style属性，属性值是css属性键值对
2.  内部样式：定义&lt;style&gt;标签，在标签内部定义css样式
3.  外部样式：定义link标签，导入外部的css文件
4.  &lt;head&gt;
5.      &lt;meta charset="UTF-8"&gt;
6.      &lt;title&gt;Title&lt;/title&gt;
7.      &lt;style&gt; --内部样式
8.          span{
9.              color: #ff0000;
10.         }
11.     &lt;/style&gt;

14.     &lt;link href="../css/demo.css" rel="stylesheet"&gt;--外部样式
15. &lt;/head&gt;
16. &lt;body&gt;

18.     &lt;div style="color: red"&gt;hello css&lt;/div&gt;--内联样式

20.     &lt;span&gt;hello css &lt;/span&gt;

23.     &lt;p&gt;hello css&lt;/p&gt;

#### CSS选择器

选择器是选取需设置的元素（标签）

1.  元素选择器
2.  Id选择器 --id要唯一
3.  类选择器 --可选择多个元素

\--谁选择的范围越小 谁就生效

1.  &lt;head&gt;
2.      &lt;meta charset="UTF-8"&gt;
3.      &lt;title&gt;Title&lt;/title&gt;

5.      &lt;style&gt;

7.          div{
8.              color: red;
9.          }

11.         #name{
12.             color: blue;
13.         }

15.         .cls{
16.             color: pink;
17.         }
18.     &lt;/style&gt;

20. &lt;/head&gt;
21. &lt;body&gt;

23. &lt;div&gt;div1&lt;/div&gt;
24. &lt;div id="name"&gt;div2&lt;/div&gt;
25. &lt;div class="cls"&gt;div3&lt;/div&gt;

27. &lt;span class="cls"&gt;span&lt;/span&gt;

### JavaScript

- JavaScirpt是一门跨平台，面向对象的脚本语言，来控制网页行为，他能使网页可交付
- JavaScript和Java是完全不同的语言，不论是概念还是设计。但是基础语法类似

#### JavaScript引入方式

1.  内部脚本：将JS代码定义在HTML页面中

在html中，JavaScript代码必须位于&lt;Script&gt;与&lt;/script&gt;标签中

注：在HTML文档中可以在任意位置放置任意数量的&lt;script&gt;

一般把脚本置于&lt;body&gt;元素的底部，可改善显示速度，不会因为脚本执行而拖慢显示

1.  &lt;script&gt;
2.      alert("hello js1");
3.  &lt;/script&gt;

外部脚本：将JS代码定义在外部Js文件中，然后引入到HTML页面中

&lt;script src="../js/demo.js"&gt;&lt;/script&gt;

注：外部脚本不能包含&lt;script&gt;标签

&lt;script&gt;标签不能自闭合

#### JavaScript基础语法

1.  书写语法
2.  区分大小写：与Java一样，变量名，函数名以及其他一切东西都是区分大小写的
3.  每行结尾的分号可有可无
4.  大括号表示代码块

1.  输出语句

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

1.  数据类型

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

1.  流程控制语句（同Java语言）

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

5.     var result = add(1,2);

7.     alert(result);

定义方式二：

1.  var functionName = function(参数列表){
2.    要执行的代码
3.  }

1.  var add = function (a,b){
2.      return a + b;
3.  }

JS中，函数调用可以传递任意个数参数，只接收需要数量的参数

#### JavaScript对象

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

#### BOM

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

3.      document.write("3秒跳转到首页...");
4.      setTimeout(function (){
5.          location.href = "https://www.baidu.com"
6.      },3000);

1.  方法

alert（）：显示一段消息和一个确认按钮的警告框

1.      //alert
2.      window.alert("abc");
3.      alert("bbb");

confirm（）：显示带有一段消息以及确认按钮和取消按钮的对话框

1.      _// confirm，点击确定按钮，返回true，点击取消按钮，返回false_
2.      var flag = confirm("确认删除？");

4.      _//alert(flag);_

6.      if(flag){
7.          _//删除逻辑_
8.      }

setInterval（）：按照指定的周期（以毫秒计）来调用函数或计算表达式

setTimeout（）：在指定的毫秒数后调用函数或计算表达式

1.      _/\*_
2.  _定时器_
3.          setTimeout(function,毫秒值): 在一定的时间间隔后执行一个function，只执行一次

5.          setInterval(function,毫秒值):在一定的时间间隔后执行一个function，循环执行
6.       \*/

8.      setTimeout(function (){
9.          alert("hehe");
10.     },3000);

12.     setInterval(function (){
13.         alert("hehe");
14.     },2000);

1.  定时器案例

要求实现：交替开关灯（一秒切换一张图片）

1.  &lt;body&gt;

3.  &lt;input type="button" onclick="on()" value="开灯"&gt;
4.  &lt;img id="myImage" border="0" src="../imgs/off.gif" style="text-align:center;"&gt;
5.  &lt;input type="button" onclick="off()" value="关灯"&gt;

7.  &lt;script&gt;

9.      function on(){
10.         document.getElementById('myImage').src='../imgs/on.gif';
11.     }

13.     function off(){
14.         document.getElementById('myImage').src='../imgs/off.gif'
15.     }
16.     var x = 0;

18.     _// 根据一个变化的数字，产生固定个数的值； 2  x % 2     3   x % 3_
19.     _//定时器_
20.     setInterval(function (){

22.         if(x % 2 == 0){
23.             on();
24.         }else {
25.             off();
26.         }

28.         x ++;

30.     },1000);

32. &lt;/script&gt;

34. &lt;/body&gt;

#### DOM

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

1.  &lt;img id="light" src="../imgs/off.gif"&gt; &lt;br&gt;

3.  &lt;div class="cls"&gt;传智教育&lt;/div&gt;   &lt;br&gt;
4.  &lt;div class="cls"&gt;黑马程序员&lt;/div&gt; &lt;br&gt;

6.  &lt;input type="checkbox" name="hobby"&gt; 电影
7.  &lt;input type="checkbox" name="hobby"&gt; 旅游
8.  &lt;input type="checkbox" name="hobby"&gt; 游戏
9.  &lt;br&gt;

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

1.  常见HTML Element对象的使用

\--查阅文档 w3school.com

&lt;img&gt; src:img.src//改变图片属性

&lt;div&gt; style:设置元素css样式

innnerHTML：设置元素内容

&lt;checkbox&gt; checked:设置或返回checkbox是否被选中 true--被选中

1.  _[VUE](#_VUE)_

#### 事件监听

- 事件：HTML事件是发生在HTML元素上的事情。比如

按钮被点击

鼠标移动到元素之上

按下键盘按键

- 事件监听：JavaScript可以在事件被侦测到时执行代码

1.  事件绑定

方式一：通过HTML标签中的按属性进行绑定

1.  &lt;input type="button" value="点我" onclick="on()"&gt; &lt;br&gt;
2.  &lt;input type="button" value="再点我" id="btn"&gt;

5.  &lt;script&gt;

7.      function on(){
8.          alert("我被点了");
9.      }

11. &lt;/script&gt;

方式二：通过DOM元素属性绑定

1.      document.getElementById("btn").onclick = function (){
2.          alert("我被点了");
3.      }

1.  常见事件

[HTML DOM 事件](https://www.w3school.com.cn/jsref/dom_obj_event.asp)

1.  &lt;form id="register" action="#" &gt;
2.      &lt;input type="text" name="username" /&gt;

4.      &lt;input type="submit" value="提交"&gt;
5.  &lt;/form&gt;

7.  &lt;script&gt;
8.      document.getElementById("register").onsubmit = function (){
9.          _//onsubmit 返回true，则表单会被提交，返回false，则表单不提交_
10.         return true;
11.     }

13. &lt;/script&gt;

常见事件：

Onclick 鼠标单击事件

Onblur 元素失去焦点

Onfocus 元素获得焦点

Onload 某个页面或图像被完成加载

Onsubmit 当表单提交时触发该事件

Onkeydown 某个键盘的键被按下

&lt;font&gt; 定义文本的字体，字体尺寸，字体颜色

Onmousover 鼠标被移到某元素之上

Onmouseout 鼠标从某元素移开

Event 代表事件对象

#### 案例-表单验证

需求：

1.  当输入框失去焦点时，验证输入内容是否符合要求
2.  获取表单输入 var usernameInput = document.getElementById("username");
3.  绑定onblur事件 usernameInput.onblur = function(){}_;_
4.  获取输入内容 var username = usernameInput.value.trim();
5.  判断是否符合规则 var reg = /^\\w{6,12}$/;//正则表达式
6.  如果不符合规则，则显示错误提示信息

1.  当点击注册按钮时，判断所有输入框的内容是否都符合要求，如果不符合则组织表单提交
2.  获取表单对象 var regForm = document.getElementById("reg-form");
3.  为表单对象绑定onsubmit regForm.onsubmit = function () {}
4.  判断所有输入框是否都符合要求 如果符合返回true

完整代码见APPENDIX

#### 正则表达式

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

### APPENDIX

7-表单验证

1.  &lt;!DOCTYPE html&gt;
2.  &lt;html lang="en"&gt;
3.  &lt;head&gt;
4.      &lt;meta charset="UTF-8"&gt;
5.      &lt;title&gt;欢迎注册&lt;/title&gt;
6.      &lt;link href="../css/register.css" rel="stylesheet"&gt;
7.  &lt;/head&gt;
8.  &lt;body&gt;

10. &lt;div class="form-div"&gt;
11.     &lt;div class="reg-content"&gt;
12.         &lt;h1&gt;欢迎注册&lt;/h1&gt;
13.         &lt;span&gt;已有账号？&lt;/span&gt; &lt;a href="#"&gt;登录&lt;/a&gt;
14.     &lt;/div&gt;
15.     &lt;form id="reg-form" action="#" method="get"&gt;

17.         &lt;table&gt;

19.             &lt;tr&gt;
20.                 &lt;td&gt;用户名&lt;/td&gt;
21.                 &lt;td class="inputs"&gt;
22.                     &lt;input name="username" type="text" id="username"&gt;
23.                     &lt;br&gt;
24.                     &lt;span id="username_err" class="err_msg" style="display: none"&gt;用户名不太受欢迎&lt;/span&gt;
25.                 &lt;/td&gt;

27.             &lt;/tr&gt;

29.             &lt;tr&gt;
30.                 &lt;td&gt;密码&lt;/td&gt;
31.                 &lt;td class="inputs"&gt;
32.                     &lt;input name="password" type="password" id="password"&gt;
33.                     &lt;br&gt;
34.                     &lt;span id="password_err" class="err_msg" style="display: none"&gt;密码格式有误&lt;/span&gt;
35.                 &lt;/td&gt;
36.             &lt;/tr&gt;

39.             &lt;tr&gt;
40.                 &lt;td&gt;手机号&lt;/td&gt;
41.                 &lt;td class="inputs"&gt;&lt;input name="tel" type="text" id="tel"&gt;
42.                     &lt;br&gt;
43.                     &lt;span id="tel_err" class="err_msg" style="display: none"&gt;手机号格式有误&lt;/span&gt;
44.                 &lt;/td&gt;
45.             &lt;/tr&gt;

47.         &lt;/table&gt;

49.         &lt;div class="buttons"&gt;
50.             &lt;input value="注 册" type="submit" id="reg_btn"&gt;
51.         &lt;/div&gt;
52.         &lt;br class="clear"&gt;
53.     &lt;/form&gt;

55. &lt;/div&gt;

58. &lt;script&gt;

60.     _//1. 验证用户名是否符合规则_
61.     _//1.1 获取用户名的输入框_
62.     var usernameInput = document.getElementById("username");

64.     _//1.2 绑定onblur事件 失去焦点_
65.     usernameInput.onblur = checkUsername;

67.     function checkUsername() {
68.         _//1.3 获取用户输入的用户名_
69.         var username = usernameInput.value.trim();

71.         _//1.4 判断用户名是否符合规则：长度 6~12,单词字符组成_
72.         var reg = /^\\w{6,12}$/;
73.         var flag = reg.test(username);

75.         _//var flag = username.length >= 6 && username.length <= 12;_
76.         if (flag) {
77.             _//符合规则_
78.             document.getElementById("username_err").style.display = 'none';
79.         } else {
80.             _//不符合规则_
81.             document.getElementById("username_err").style.display = '';//设置css的style文件
82.         }

84.         return flag;
85.     }

88.     _//1. 验证密码是否符合规则_
89.     _//1.1 获取密码的输入框_
90.     var passwordInput = document.getElementById("password");

92.     _//1.2 绑定onblur事件 失去焦点_
93.     passwordInput.onblur = checkPassword;

95.     function checkPassword() {
96.         _//1.3 获取用户输入的密码_
97.         var password = passwordInput.value.trim();

99.         _//1.4 判断密码是否符合规则：长度 6~12_
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

156.&lt;/script&gt;
157.&lt;/body&gt;
158.&lt;/html&gt;

## Web核心

- JavaWeb技术栈
- B/S架构：Browser/Server，浏览器/服务器 架构模式，它的特点是，客户端只需要浏览器，应用程序的逻辑和数据都存储在服务器端，浏览器只需要请求服务器，获取Web资源，服务器把Web资源发送给浏览器即可

好处：易于维护升级，服务端升级后，客户端无需任何部署就可以使用到新的版本

- 静态资源：HTML，CSS，JavaScript，图片等。负责页面展现
- 动态资源：Servlet，JSP等。负责逻辑处理
- 数据库：负责存储管理
- HTTP协议：定义通信规则
- Web服务器（Tomcat）：负责解析HTTP协议，解析请求数据，并发送响应数据

### HTTP

- HyperTextTranferProtocol，超文本传输协议，规定了浏览器和服务器之间的数据传输规则
- HTTP协议特点：
- 基于TCP协议：面向连接，安全
- 基于请求-响应模型的：一次请求对应一次响应
- HTTP协议时无状态的协议：对于事务处理没有记忆能力。每次请求-响应都是独立的

缺点：多次请求间不能共享数据。Java中使用会话技术（Cookie，Session）来解决问题

优点：速度快

#### 请求数据格式

请求数据分为3部分：

1.  请求行：请求数据的第一行。其中GET表示请求方式，/表示请求资源路径，HTTP/1.1表示协议版本

1.  请求头：第二行开始，格式为key：value形式

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

#### 响应数据格式

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

### Web服务器-Tomcat

- Web服务器是一个应用程序，对HTTP协议的操作进行封装，使得程序员不必直接对协议进行操作，让web开发更加便捷，主要功能是”提供网上信息浏览服务”
- Tomcat
- 轻量级的Web服务器，支持Servlet/JSP少量JavaEE规范，Tomcat也被称为Web服务器，Servlet容器。Servlet需要依赖Tomcat才能运行
- JavaEE：Java企业级开发的计数规范总和

#### 基本使用

1.  启动：双击：bin\\startup.bat

控制台中文乱码：修改conf/logging.properties UTF-8改为GBK

1.  关闭：强制关闭，直接叉掉/shutdown.bat关闭/黑窗口中ctrl-c关闭
2.  配置

修改启动端口号：conf/server.xml

Http协议默认端口号为80，如果将Tomcat端口号改为80，则将来访问Tomcat时，将不用输入端口号

1.  启动时可能出现的问题
2.  端口号冲突：找到对应程序，将其关闭掉
3.  启动窗口一闪而过 [Tomcat双击startup.bat闪退](https://zhuanlan.zhihu.com/p/353404326)/Java_home没有正确配置

1.  部署项目

- Tomcat部署项目：将项目放置到webapps目录下，即部署完成
- 一般将JavaWeb项目打包成war包，然后将war包放到webapps目录下，Tomcat会自动解压缩war文件

#### IDEA中创建Maven Web项目

1.  web项目结构

编译后Java字节码文件和resources的资源文件，放到WEB-INF下的classes目录下

Pom.xml中以来坐标对应的jar包，放入WEB-INF下的lib目录下

但是package过程中可以自动完成这些进程

1.  使用骨架

Archtype 创建项目 补齐缺失的目录结构：webapp

1.  不使用骨架

同样创建maven文件，在file-project structure-Facets中添加目录

4）在Tomcat中运行 通过

&lt;packaging&gt;war&lt;/packaging&gt;

打包成war包移动到webapps目录下，即可自动解压

1.  IDEA中创建Maven Web项目
2.  将本地Tomcat集成到idea中，然后进行项目部署即可
3.  Pom.xml中添加TomCat插件

右键文件选择run Maven-tomcat7：run

1.      _&lt;!-- tomcat插件 --&gt;_
2.      &lt;build&gt;
3.          &lt;plugins&gt;
4.              &lt;plugin&gt;
5.                  &lt;groupId&gt;org.apache.tomcat.maven&lt;/groupId&gt;
6.                  &lt;artifactId&gt;tomcat7-maven-plugin&lt;/artifactId&gt;
7.                  &lt;version&gt;2.2&lt;/version&gt;
8.              &lt;/plugin&gt;
9.          &lt;/plugins&gt;
10.     &lt;/build&gt;

可以设置端口号以及路径

1.  &lt;port&gt;80&lt;/port&gt;
2.  &lt;path&gt;/&lt;/path&gt;

### Servlet

- Servlet是Java提供的一门动态web资源开发技术
- Servlet是JavaEE规范之一，其实就是一个接口，将来需要定义Servlet接口，并由web服务器运行Servlet

#### 快速入门

1.  创建web项目，导入Servlet依赖坐标
2.      _&lt;!-- 导入Servlet依赖坐标 --&gt;_
3.      &lt;dependencies&gt;
4.          &lt;dependency&gt;
5.              &lt;groupId&gt;javax.servlet&lt;/groupId&gt;
6.              &lt;artifactId&gt;javax.servlet-api&lt;/artifactId&gt;
7.              &lt;version&gt;3.1.0&lt;/version&gt;
8.              &lt;scope&gt;provided&lt;/scope&gt;
9.          &lt;/dependency&gt;
10.     &lt;/dependencies&gt;

1.  创建：定义一个类，实现Servlet接口，并重写接口中所有方法，并在service方法中输入一句话

注：重写接口中所有方法 在继承类后快捷键Alt+Enter

1.  public class ServletDemo1 implements Servlet {

3.      @Override
4.      public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {
5.          System.out.println("servlet hello world");
6.      }

8.      @Override
9.      public String getServletInfo() {
10.         return "";
11.     }

13.     @Override
14.     public void destroy() {

16.     }

18.     @Override
19.     public void init(ServletConfig servletConfig) throws ServletException {

21.     }

23.     @Override
24.     public ServletConfig getServletConfig() {
25.         return null;
26.     }
27. }

1.  配置：在类中使用@WebServlet注解，配置该Servlet的访问路径

@WebServlet("/demo1")

1.  访问：启动Tomcat，浏览器输入URL访问该Servlet

#### Servlet执行流程

https：//localhost:8080/web-demo/demo1

| | |

访问到服务器 访问到web项目 访问到对应的Servlet

Servlet由web服务器创建，servlet方法由web服务器调用

自定义的Servlet，必须实现Servlet接口并复写其方法，而servle接口中由service方法

#### Servlet生命周期

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

#### Servlet体系结构

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

5.      }

7.      @Override
8.      public ServletConfig getServletConfig() {
9.          return null;
10.     }

12.     @Override
13.     public void service(ServletRequest req, ServletResponse res) throws ServletException, IOException {
14.         _// 根据请求方式的不同，进行分别的处理_

16.         HttpServletRequest request = (HttpServletRequest) req;

18.         _//1. 获取请求方式_
19.         String method = request.getMethod();
20.         _//2. 判断_
21.         if("GET".equals(method)){
22.             _// get方式的处理逻辑_
23.         }else if("POST".equals(method)){
24.             _// post方式的处理逻辑_
25.         }
26.     }

28.     @Override
29.     public String getServletInfo() {
30.         return null;
31.     }

33.     @Override
34.     public void destroy() {

36.     }
37. }

编写一个原始的实现Servlet类 需要复写四种方法，应为get/post请求参数位置不同 post的请求参数在请求体中，而get在请求行中，所以在service层中需要不同的处理逻辑，根据请求方式的不同，进行分别的处理，而这一部分的逻辑代码完全重复，可以写一个类，让所有servlet都继承自这个类，复用代码，这个类就是HttpServlet，将get的处理逻辑封装成方法doGet()，将post的处理逻辑封装成方法doPost(),这样就不需要实现Servlet接口了，直接继承自HttpServlet，复写doPost()和doGet()用来处理业务逻辑。做到了Http协议的封装，并且完成了对不同请求方式的分发。

HttpServlet使用步骤：继承HttpServlet，重写doGet，doPost方法

#### Servlet urlPattern配置

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

#### XML配置方法编写Servlet（旧版本）

Servlet从3.0开始支持使用注解注释，3.0之前只支持XML配置文件的配置方式

步骤

1.  编写Servlet类
2.  在web.xml中配置该Servlet
3.      _<!--_Servlet 全类名-->
4.      &lt;servlet&gt;
5.          &lt;servlet-name&gt;demo13&lt;/servlet-name&gt;
6.          &lt;servlet-class&gt;com.itheima.web.ServletDemo13&lt;/servlet-class&gt;
7.      &lt;/servlet&gt;

9.      _<!--_Servlet 访问路径-->
10.     &lt;servlet-mapping&gt;
11.         &lt;servlet-name&gt;demo13&lt;/servlet-name&gt;
12.         &lt;url-pattern&gt;/demo13&lt;/url-pattern&gt;
13.     &lt;/servlet-mapping&gt;

### Request & Response

- Request：获取请求数据
- Response：设置响应数据

#### Request

##### Request继承体系

ServletRequest ---Java提供的请求对象体系根接口

|

HttpServletRequest ----Java提供的对Http协议封装的对象请求接口

|

requestFacade -----Tomcat定义的实现类

Tomcat需要解析请求数据，分装为request对象，并且创建request对象传递到service方法中

使用request对象，查阅JavaEE API文档的HttpServletRequest接口

##### Request获取请求数据

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

Map&lt;String,String\[\]&gt;getParameterMap():获取所有参数Map集合

String\[\] getParameterValues(String name)：根据名称获取参数值（数组）

String getParameter(String name):根据名称获取参数值（单个值）

1.  &lt;form action="/request-demo/req2" method="get"&gt;
2.      &lt;input type="text" name="username"&gt;&lt;br&gt;
3.      &lt;input type="password" name="password"&gt;&lt;br&gt;
4.      &lt;input type="checkbox" name="hobby" value="1"&gt; 游泳
5.      &lt;input type="checkbox" name="hobby" value="2"&gt; 爬山 &lt;br&gt;
6.      &lt;input type="submit"&gt;

后端：

1.  protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
2.          _//GET请求逻辑_
3.          _//System.out.println("get....");_

5.          _//1. 获取所有参数的Map集合_
6.          Map&lt;String, String\[\]&gt; map = req.getParameterMap();
7.          for (String key : map.keySet()) {
8.              _// username:zhangsan lisi_
9.              System.out.print(key+":");

11.             _//获取值_
12.             String\[\] values = map.get(key);
13.             for (String value : values) {
14.                 System.out.print(value + " ");
15.             }

17.             System.out.println();
18.         }

20.         System.out.println("------------");

22.         _//2. 根据key获取参数值，数组_
23.         String\[\] hobbies = req.getParameterValues("hobby");
24.         for (String hobby : hobbies) {

26.             System.out.println(hobby);
27.         }

29.         _//3. 根据key 获取单个参数值_
30.         String username = req.getParameter("username");
31.         String password = req.getParameter("password");

33.         System.out.println(username);
34.         System.out.println(password);
35.     }

doPost

1.      @Override
2.      protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
3.          _//POST请求逻辑_

5.          this.doGet(req,resp);

7.  }

实现方式的底层逻辑

1.          String method = request.getMethod();

3.          if("GET".equals(method)){
4.              _// get方式的处理逻辑_
5.  params_\= this.getQueryString();_
6.          }else if("POST".equals(method)){
7.              _// post方式的处理逻辑_
8.  params _= reader.readLine();_
9.          }

工具：IDEA模板创建Servlet

1.  Request请求参数中文乱码处理

请求中如果存在中文数据，这可能出现乱码

1.  POST解决方案
2.  _//1. 解决乱码：POST，getReader()_
3.  request.setCharacterEncoding("UTF-8");_//设置字符输入流的编码_

5.  _//2. 获取username_
6.  String username = request.getParameter("username");
7.  System.out.println(username);

1.  GET解决方案

编码与解码不一致

1.    _//获取username_
2.          String username = request.getParameter("username");
3.          System.out.println("解决乱码前："+username);

5.          _//GET,获取参数的方式：getQueryString_
6.          _// 乱码原因：tomcat进行URL解码，默认的字符集ISO-8859-1_
7.      _//先对乱码数据进行编码：转为字节数组_
8.  //      byte\[\] bytes = username.getBytes(StandardCharsets.ISO_8859_1);
9.          //字节数组解码
10. //      username = new String(bytes, StandardCharsets.UTF_8);

12.         username  = new String(username.getBytes(StandardCharsets.ISO_8859_1),StandardCharsets.UTF_8);

14.         System.out.println("解决乱码后："+username);

通用解决方案：既可以解决GET也可以解决POST

username  = new String(username.getBytes(StandardCharsets.ISO_8859_1),StandardCharsets.UTF_8);

Tomcat 8.0之后，已将GET请求乱码问题解决，设置默认的解码方式为UTF-8

##### Request请求转发

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

#### Response

##### Response设置响应数据功能介绍

1.  响应行 HTTP/1.1 200OK

void setStatus(int sc)：设置响应状态码

1.  响应头 Content-Type:text/html

void setHeader（String name，String value）：设置响应头键值对

1.  响应体 &lt;html&gt;&lt;head&gt;&lt;head&gt;&lt;body&gt;&lt;/body&gt;&lt;/html&gt;

PrintWriter getWriter：获取字符输出流

ServletOutputStream getOutputStream（）：获取字节输出流

##### Response完成重定向

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

&lt;a href = ‘路径’&gt; 加虚拟目录

&lt;form action = ’路径’&gt; 加虚拟目录

req.getrequestDispatcher（‘路径’） 不加虚拟目录

resp.sendRedirect（‘路径’） 加虚拟目录

1.  动态获取虚拟目录
2.  String contextPath =request.getContextPath();
3.  Response.sendRedierect(contextPath + “/resp2”)；

##### Response响应字符数据

1.  使用
2.  通过Response对象获取字符输出流

PrintWriter writer = resp.getwriter（）；

1.  写数据

writer.write("aaa");

1.  PrintWriter writer = resp.getwriter（）；
2.  response.setHeader("content-type","text/html");
3.  writer.write("&lt;h1&gt;aaa&lt;/h1&gt;");

1.  细节
2.  流不需要关闭
3.  如果响应字符是中文，会乱码，处理方法：setContentType
4.  response.setContentType("text/html;charset = utf-8");
5.  PrintWriter writer = resp.getwriter（）；
6.  writer.write("你好");
7.  writer.write("&lt;h1&gt;aaa&lt;/h1&gt;");

##### Response响应字节数据

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

1.  &lt;dependency&gt;
2.        &lt;groupId&gt;commons-io&lt;/groupId&gt;
3.        &lt;artifactId&gt;commons-io&lt;/artifactId&gt;
4.        &lt;version&gt;2.6&lt;/version&gt;
5.  &lt;/dependency&gt;

使用:

IOUtils.copy(fis,os);

1.  关闭流

fis.close();

#### 案例

##### 用户登录

1.  需求分析：
2.  用户填写用户名密码，提交到LoginServlet
3.  在LoginServlet中使用MyBatis查询数据库，验证用户名密码是否正确
4.  如果正确，响应登录成功，如果错误，响应登录失败

1.  准备环境
2.  准备静态页面到项目的webapp目录下
3.  创建db1数据表，创建tb_user表，创建User实体类
4.  导入Mybatis坐标，MySQL驱动坐标
5.  创建mybatis-config.xml核心配置文件，UserMapper.xml映射文件，UserMapper接口

Mybatis-config配置文件

1.  &lt;configuration&gt;
2.      _&lt;!--起别名--&gt;_
3.      &lt;typeAliases&gt;
4.          &lt;package name="com.itheima.pojo"/&gt;
5.      &lt;/typeAliases&gt;

7.      &lt;environments default="development"&gt;
8.          &lt;environment id="development"&gt;
9.              &lt;transactionManager type="JDBC"/&gt;
10.             &lt;dataSource type="POOLED"&gt;
11.                 &lt;property name="driver" value="com.mysql.jdbc.Driver"/&gt;
12.                 &lt;property name="url" value="jdbc:mysql:///db1?useSSL=false&amp;useServerPrepStmts=true"/&gt;
13.                 &lt;property name="username" value="root"/&gt;
14.                 &lt;property name="password" value="1234"/&gt;
15.             &lt;/dataSource&gt;
16.         &lt;/environment&gt;
17.     &lt;/environments&gt;
18.     &lt;mappers&gt;
19.         _&lt;!--扫描mapper--&gt;_
20.         &lt;package name="com.itheima.mapper"/&gt;
21.     &lt;/mappers&gt;

UserMapper.xml映射文件

1.  &lt;mapper namespace="com.itheima.mapper.UserMapper"&gt;

3.  &lt;/mapper&gt;

1.  接口UseMapper
2.  @Select("select \* from tb_user where username = #{username} and password = #{password}")
3.  User select(@Param("username") String username,@Param("password")  String password);

1.  用户填写用户名密码，提交到LoginServlet

Login.html

1.  &lt;div id="loginDiv"&gt;
2.      &lt;form action="/request-demo/loginServlet" method="post" id="form"&gt;
3.          &lt;h1 id="loginMsg"&gt;LOGIN IN&lt;/h1&gt;
4.          &lt;p&gt;Username:&lt;input id="username" name="username" type="text"&gt;&lt;/p&gt;

6.          &lt;p&gt;Password:&lt;input id="password" name="password" type="password"&gt;&lt;/p&gt;

8.          &lt;div id="subDiv"&gt;
9.              &lt;input type="submit" class="button" value="login up"&gt;
10.             &lt;input type="reset" class="button" value="reset"&gt;&nbsp;&nbsp;&nbsp;
11.             &lt;a href="register.html"&gt;没有账号？点击注册&lt;/a&gt;
12.         &lt;/div&gt;
13.     &lt;/form&gt;
14. &lt;/div&gt;

1.  在LoginServlet中使用MyBatis查询数据库，验证用户名密码是否正确

LoginServlet.java

1.  _//2. 调用MyBatis完成查询_
2.  _//2.1 获取SqlSessionFactory对象_
3.  String resource = "mybatis-config.xml";
4.  InputStream inputStream = Resources.getResourceAsStream(resource);
5.  SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

7.  SqlSessionFactory sqlSessionFactory = SqlSessionFactoryUtils.getSqlSessionFactory();
8.  _//2.2 获取SqlSession对象_
9.  _//2.3 获取Mapper_
10. UserMapper userMapper = sqlSession.getMapper(UserMapper.class);
11. _//2.4 调用方法_
12. User user = userMapper.select(username, password);
13. _//2.5 释放资源_
14. sqlSession.close();

1.  如果正确，响应登录成功，如果错误，响应登录失败，即判断user释放是否为null 如果不等于null则登录成功，等于null则登录失败
2.          _//获取字符输出流，并设置content type_
3.          response.setContentType("text/html;charset=utf-8");
4.          PrintWriter writer = response.getWriter();
5.          _//3. 判断user释放为null_
6.          if(user != null){
7.              _// 登录成功_
8.              writer.write("登录成功");
9.          }else {
10.             _// 登录失败_
11.             writer.write("登录失败");
12.         }

##### 用户注册

1.  需求分析
2.  用户填写用户名，密码等信息，点击注册按钮，提交到registerServlet
3.  在RegisterServlet中使用MyBatis保存数据
4.  保存前需要判断用户名是否已经存在：根据用户名查询数据库

1.  接口UserMapper
2.      _/\*\*_
3.       \* 根据用户名查询用户对象
4.       \* @param username
5.       \* @return
6.       \*/
7.      @Select("select \* from tb_user where username = #{username}")
8.      User selectByUsername(String username);

10.     _/\*\*_
11.      \* 添加用户
12.      \* @param user
13.      \*/
14.    @Insert("insert into tb_user values(null,#{username},#{password})")
15.    void add(User user);

1.  用户填写用户名，密码等信息，点击注册按钮，提交到registerServlet
2.  &lt;div class="form-div"&gt;
3.      &lt;div class="reg-content"&gt;
4.          &lt;h1&gt;欢迎注册&lt;/h1&gt;
5.          &lt;span&gt;已有账号？&lt;/span&gt; &lt;a href="login.html"&gt;登录&lt;/a&gt;
6.      &lt;/div&gt;
7.      &lt;form id="reg-form" action="/request-demo/registerServlet" method="post"&gt;

9.          &lt;table&gt;

11.             &lt;tr&gt;
12.                 &lt;td&gt;用户名&lt;/td&gt;
13.                 &lt;td class="inputs"&gt;
14.                     &lt;input name="username" type="text" id="username"&gt;
15.                     &lt;br&gt;
16.                     &lt;span id="username_err" class="err_msg" style="display: none"&gt;用户名不太受欢迎&lt;/span&gt;
17.                 &lt;/td&gt;

19.             &lt;/tr&gt;

21.             &lt;tr&gt;
22.                 &lt;td&gt;密码&lt;/td&gt;
23.                 &lt;td class="inputs"&gt;
24.                     &lt;input name="password" type="password" id="password"&gt;
25.                     &lt;br&gt;
26.                     &lt;span id="password_err" class="err_msg" style="display: none"&gt;密码格式有误&lt;/span&gt;
27.                 &lt;/td&gt;
28.             &lt;/tr&gt;

30.         &lt;/table&gt;

32.         &lt;div class="buttons"&gt;
33.             &lt;input value="注 册" type="submit" id="reg_btn"&gt;
34.         &lt;/div&gt;
35.         &lt;br class="clear"&gt;
36.     &lt;/form&gt;

38. &lt;/div&gt;

1.  在RegisterServlet中使用MyBatis保存数据
2.  @Override
3.  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
4.      _//1. 接收用户数据_
5.      String username = request.getParameter("username");
6.      String password = request.getParameter("password");

8.      _//封装用户对象_
9.      User user = new User();
10.     user.setUsername(username);
11.     user.setPassword(password);

13.     _//2. 调用mapper 根据用户名查询用户对象_
14.     _//2.1 获取SqlSessionFactory对象_
15.     String resource = "mybatis-config.xml";
16.     InputStream inputStream = Resources.getResourceAsStream(resource);
17.     SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
18.     SqlSessionFactory sqlSessionFactory = SqlSessionFactoryUtils.getSqlSessionFactory();

20.     _//2.2 获取SqlSession对象_
21.     SqlSession sqlSession = sqlSessionFactory.openSession();
22.     _//2.3 获取Mapper_
23.     UserMapper userMapper = sqlSession.getMapper(UserMapper.class);

25.     _//2.4 调用方法_
26.     User u = userMapper.selectByUsername(username);
27.     }

1.  保存前需要判断用户名是否已经存在：根据用户名查询数据库
2.   _//3. 判断用户对象释放为null_
3.      if( u == null){
4.          _// 用户名不存在，添加用户_
5.          userMapper.add(user);
6.          _// 提交事务_
7.          sqlSession.commit();
8.          _// 释放资源_
9.          sqlSession.close();
10.     }else {
11.         _// 用户名存在，给出提示信息_
12.         response.setContentType("text/html;charset=utf-8");
13.         response.getWriter().write("用户名已存在");
14.     }

##### 代码优化

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

3.      private static SqlSessionFactory sqlSessionFactory;

5.      static {
6.          _//静态代码块会随着类的加载而自动执行，且只执行一次_

8.          try {
9.              String resource = "mybatis-config.xml";
10.             InputStream inputStream = Resources.getResourceAsStream(resource);
11.             sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
12.         } catch (IOException e) {
13.             e.printStackTrace();
14.         }
15.     }
16.     public static SqlSessionFactory getSqlSessionFactory(){
17.         return sqlSessionFactory;
18.     }
19. }

### JSP

- JavaServerPages，java服务端页面
- 一种动态的网页技术，其中既可以定义HTML，JS，CSS等静态内容，还可以定义Java代码的动态内容
- JSP = HTML + Java
- JSP的作用：简化开发，避免了在Servlet中直接输出HTML标签

#### JSP原理

- JSP本质上是一个Servlet
- JSP容器（Tomcat）会将.jsp文件转换成.java文件，再由JSP容器（Tomcat）将其编译，最终对外提供服务的其实就是这个字节码文件

#### JSP脚本

- JSP脚本用于在JSP页面内定义Java代码
- JSP脚本分类

&lt;%..%&gt;：内容会直接放到_jspService()方法之中

&lt;%=...%&gt;：内容会放到out.print()方法中，作为out.print()的参数

&lt;%!...%&gt;：内容会放到_jspService()之外，被类直接包含

1.  关于脚本与截断的案例
2.  &lt;table border="1" cellspacing="0" width="800"&gt;
3.      &lt;tr&gt;
4.          &lt;th&gt;序号&lt;/th&gt;
5.          &lt;th&gt;品牌名称&lt;/th&gt;
6.          &lt;th&gt;企业名称&lt;/th&gt;
7.          &lt;th&gt;排序&lt;/th&gt;
8.          &lt;th&gt;品牌介绍&lt;/th&gt;
9.          &lt;th&gt;状态&lt;/th&gt;
10.         &lt;th&gt;操作&lt;/th&gt;
11.     &lt;/tr&gt;
12.     <%
13.         for (int i = 0; i < brands.size(); i++) {
14.             Brand brand = brands.get(i);
15.     %>

17.     &lt;tr align="center"&gt;
18.         &lt;td&gt;&lt;%=brand.getId()%&gt;&lt;/td&gt;
19.         &lt;td&gt;&lt;%=brand.getBrandName()%&gt;&lt;/td&gt;
20.         &lt;td&gt;&lt;%=brand.getCompanyName()%&gt;&lt;/td&gt;
21.         &lt;td&gt;&lt;%=brand.getOrdered()%&gt;&lt;/td&gt;
22.         &lt;td&gt;&lt;%=brand.getDescription()%&gt;&lt;/td&gt;

24.         <%
25.             if(brand.getStatus() == 1){
26.                 //显示启用
27.         %>
28.             &lt;td&gt;&lt;%="启用"%&gt;&lt;/td&gt;
29.         <%
30.             }else {
31.                 // 显示禁用
32.         %>
33.             &lt;td&gt;&lt;%="禁用"%&gt;&lt;/td&gt;
34.         <%
35.             }
36.         %>

38.         &lt;td&gt;&lt;a href="#"&gt;修改&lt;/a&gt; &lt;a href="#"&gt;删除&lt;/a&gt;&lt;/td&gt;
39.     &lt;/tr&gt;
40.     <%
41.         }
42.     %>

44. &lt;/table&gt;

1.  JSP的缺点

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

#### JSP快速入门

1.  导入JSP坐标
2.  &lt;dependency&gt;
3.      &lt;groupId&gt;javax.servlet.jsp&lt;/groupId&gt;
4.      &lt;artifactId&gt;jsp-api&lt;/artifactId&gt;
5.      &lt;version&gt;2.2&lt;/version&gt;
6.      &lt;scope&gt;provided&lt;/scope&gt;
7.  &lt;/dependency&gt;

1.  创建JSP文件
2.  编写HTML标签和Java代码
3.      &lt;h1&gt;hello jsp&lt;/h1&gt;

5.      <%
6.          System.out.println("hello,jsp~");
7.          int i = 3;
8.      %>

#### EL表达式

- ExpressionLanguage 表达式语言，用于简化JSP页面内的Java代码
- 主要功能：获取数据
- 语法：${expression}

${brands}：获取域中存储的key为brands的数据

1.  @Override
2.  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
3.      _//1. 准备数据_
4.      List&lt;Brand&gt; brands = new ArrayList&lt;Brand&gt;();
5.      brands.add(new Brand(1,"三只松鼠","三只松鼠",100,"三只松鼠，好吃不上火",1));
6.      brands.add(new Brand(2,"优衣库","优衣库",200,"优衣库，服适人生",0));
7.      brands.add(new Brand(3,"小米","小米科技有限公司",1000,"为发烧而生",1));

9.      _//2. 存储到request域中_
10.     request.setAttribute("brands",brands);
11.     request.setAttribute("status",1);

13.     _//3. 转发到 el-demo.jsp_
14.     request.getRequestDispatcher("/el-demo.jsp").forward(request,response);

el-demo.jsp:

${brands}

JavaWeb中的四大域对象：

Page：当前页面有效

Request：当前请求有效

Session：当前会话有效

Application：当前应用有效

el表达式获取数据，会依次从这4个域中寻找，直到找到为止

#### JSTL标签

- Jsp Standard Tag Library，JSP标准标签库。使用标签取代JSP页面上的Java代码

&lt;c:if&gt;

&lt;c:foreach&gt;

1）JSTL快速入门

1.  导入坐标
2.  &lt;dependency&gt;
3.      &lt;groupId&gt;jstl&lt;/groupId&gt;
4.      &lt;artifactId&gt;jstl&lt;/artifactId&gt;
5.      &lt;version&gt;1.2&lt;/version&gt;
6.  &lt;/dependency&gt;
7.  &lt;dependency&gt;
8.       &lt;groupId&gt;taglibs&lt;/groupId&gt;
9.       &lt;artifactId&gt;standard&lt;/artifactId&gt;
10.      &lt;version&gt;1.1.2&lt;/version&gt;
11. &lt;/dependency&gt;

1.  在JSP页面上引入JSTL标签库

&lt;%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %&gt;

1.  使用：一般与EL表达式结合使用

&lt;c:if&gt;

jstl-if.jsp

1.      &lt;c:if test="${status ==1}"&gt;
2.          启用
3.      &lt;/c:if&gt;

5.      &lt;c:if test="${status ==0}"&gt;
6.          禁用
7.      &lt;/c:if&gt;

ServletDemo1:

request.getRequestDispatcher("/jstl-if.jsp").forward(request,response);

&lt;c:forEach&gt;：相当于for循环

Items：被遍历的容器

Var：遍历产生的临时变量

varStatus：生成序号

status有两个属性 index从0开始，count从1开始

jstl-foreach.jsp

1.  &lt;input type="button" value="新增"&gt;&lt;br&gt;
2.  &lt;hr&gt;
3.  &lt;table border="1" cellspacing="0" width="800"&gt;
4.      &lt;tr&gt;
5.          &lt;th&gt;序号&lt;/th&gt;
6.          &lt;th&gt;品牌名称&lt;/th&gt;
7.          &lt;th&gt;企业名称&lt;/th&gt;
8.          &lt;th&gt;排序&lt;/th&gt;
9.          &lt;th&gt;品牌介绍&lt;/th&gt;
10.         &lt;th&gt;状态&lt;/th&gt;
11.         &lt;th&gt;操作&lt;/th&gt;

13.     &lt;/tr&gt;

16.     &lt;c:forEach items="${brands}" var="brand" varStatus="status"&gt;
17.         &lt;tr align="center"&gt;
18.             &lt;--<td&gt;${brand.id}&lt;/td&gt;-->
19.             &lt;td&gt;${status.count}&lt;/td&gt;
20.             &lt;td&gt;${brand.brandName}&lt;/td&gt;
21.             &lt;td&gt;${brand.companyName}&lt;/td&gt;
22.             &lt;td&gt;${brand.ordered}&lt;/td&gt;
23.             &lt;td&gt;${brand.description}&lt;/td&gt;
24.             &lt;c:if test="${brand.status == 1}"&gt;
25.                 &lt;td&gt;启用&lt;/td&gt;
26.             &lt;/c:if&gt;
27.             &lt;c:if test="${brand.status != 1}"&gt;
28.                 &lt;td&gt;禁用&lt;/td&gt;
29.             &lt;/c:if&gt;

31.             &lt;td&gt;&lt;a href="#"&gt;修改&lt;/a&gt; &lt;a href="#"&gt;删除&lt;/a&gt;&lt;/td&gt;
32.         &lt;/tr&gt;

34.     &lt;/c:forEach&gt;

普通for循环

1.  &lt;c:forEach begin="1" end="10" step="1" var="i"&gt;
2.      &lt;a href="#"&gt;${i}&lt;/a&gt;
3.  &lt;/c:forEach&gt;

应用-分页进度条

#### MVC模式和三层架构

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

#### 案例

完成品牌的增删改查操作 Servlet/JSP/三层架构

##### 准备环境

- 创建新的模块，brand_demo，引入坐标

1.  &lt;dependencies&gt;
2.          _&lt;!--mybatis--&gt;_
3.          _&lt;!--mysql--&gt;_
4.          _&lt;!--servlet--&gt;_
5.          _&lt;!--jsp--&gt;_
6.          _&lt;!--jstl--&gt;_
7.  &lt;/dependencies&gt;
8.      &lt;build&gt; 
9.          &lt;plugins&gt; 
10.             &lt;plugin&gt; 
11.                 &lt;groupId&gt;org.apache.tomcat.maven&lt;/groupId&gt;
12.                 &lt;artifactId&gt;tomcat7-maven-plugin&lt;/artifactId&gt;
13.                 &lt;version&gt;2.2&lt;/version&gt;
14.             &lt;/plugin&gt;
15.         &lt;/plugins&gt;
16.     &lt;/build&gt;

- 创建三层架构的包结构
- 数据库表 tb_brand
- 实体类Brand
- MyBatis基础环境
- Mybatis-config.xml
- BrandMapper.xml
- BrandMapper接口

##### 查询所有

1.  Dao层

BrandMapper.java

1.      _/\*\*_
2.       \* 查询所有
3.       \* @return
4.       \*/
5.  @ResultMap("brandResultMap")
6.      @Select("select \* from tb_brand")
7.      List&lt;Brand&gt; selectAll();

在接口中创建一个方法，selectAll返回一个Brand的list集合

注解sql @Select

注解ResultMap @ResultMap确定映射关系，驼峰命名与原变量的命名映射

BrandMapper.xml

1.      &lt;resultMap id="brandResultMap" type="brand"&gt;
2.          &lt;result column="brand_name" property="brandName"&gt;&lt;/result&gt;
3.          &lt;result column="company_name" property="companyName"&gt;&lt;/result&gt;
4.      &lt;/resultMap&gt;

1.  Service层

在service包中新建BrandService.java

1.  public class BrandService {
2.      SqlSessionFactory factory = SqlSessionFactoryUtils.getSqlSessionFactory();

4.      _/\*\*_
5.       \* 查询所有
6.       \* @return
7.       \*/
8.      public List&lt;Brand&gt; selectAll() {

10.         _//调用brandMapper.selectAll()_

13.         _//2.获取SqlSession对象_
14.         SqlSession sqlSession = factory.openSession();

16.         _//3.获取brandMapper_
17.         BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

19.         _//4.调用方法_
20.         List&lt;Brand&gt; brands = mapper.selectAll();

22.         sqlSession.close();

24.         return brands;
25.     }
26. }

Utill类 -同JavaWeb-Web核心-Request & Response-案例-代码优化

1.  public class SqlSessionFactoryUtils {

3.      private static SqlSessionFactory sqlSessionFactory;

5.      static {
6.          _//静态代码块会随着类的加载而自动执行，且只执行一次_

8.          try {
9.              String resource = "mybatis-config.xml";
10.             InputStream inputStream = Resources.getResourceAsStream(resource);
11.             sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
12.         } catch (IOException e) {
13.             e.printStackTrace();
14.         }
15.     }

18.     public static SqlSessionFactory getSqlSessionFactory(){
19.         return sqlSessionFactory;
20.     }
21. }

1.  Web层

web-selectAllServlet

1.  @WebServlet("/selectAllServlet")
2.  public class SelectAllServlet extends HttpServlet {

4.      private BrandService service = new BrandService();
5.      @Override
6.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

8.          _//1.调用BrandService完成查询_
9.          BrandService service = new BrandService();
10.         List&lt;Brand&gt; brands = service.selectAll();

12.         _//2.将brands存入request域中_
13.         request.setAttribute("brands",brands);

15.         _//3.转发到brand.jsp页面_
16.         request.getRequestDispatcher("/brand.jsp").forward(request,response);

18.     }

20.     @Override
21.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
22.         this.doGet(request, response);
23.     }
24. }

- 创建Brandservice对象，使用selectAll（）方法进行查询，并把查询到的结果brands封装到list集合
- 将brands存入request域中
- 转发到brand.jsp页面中

brand.jsp

1.  &lt;input type="button" value="新增"&gt;&lt;br&gt;
2.  &lt;hr&gt;
3.  &lt;table border="1" cellspacing="0" width="800"&gt;
4.      &lt;tr&gt;
5.          &lt;th&gt;序号&lt;/th&gt;
6.          &lt;th&gt;品牌名称&lt;/th&gt;
7.          &lt;th&gt;企业名称&lt;/th&gt;
8.          &lt;th&gt;排序&lt;/th&gt;
9.          &lt;th&gt;品牌介绍&lt;/th&gt;
10.         &lt;th&gt;状态&lt;/th&gt;
11.         &lt;th&gt;操作&lt;/th&gt;

13.     &lt;/tr&gt;

16.     &lt;c:forEach items="${brands}" var="brand" varStatus="status"&gt;
17.         &lt;tr align="center"&gt;
18.             &lt;%--<td&gt;${brand.id}&lt;/td&gt;--%>
19.             &lt;td&gt;${status.count}&lt;/td&gt;
20.             &lt;td&gt;${brand.brandName}&lt;/td&gt;
21.             &lt;td&gt;${brand.companyName}&lt;/td&gt;
22.             &lt;td&gt;${brand.ordered}&lt;/td&gt;
23.             &lt;td&gt;${brand.description}&lt;/td&gt;
24.             &lt;c:if test="${brand.status == 1}"&gt;
25.                 &lt;td&gt;启用&lt;/td&gt;
26.             &lt;/c:if&gt;
27.             &lt;c:if test="${brand.status != 1}"&gt;
28.                 &lt;td&gt;禁用&lt;/td&gt;
29.             &lt;/c:if&gt;

31.             &lt;td&gt;&lt;a href="#"&gt;修改&lt;/a&gt; &lt;a href="#"&gt;删除&lt;/a&gt;&lt;/td&gt;
32.         &lt;/tr&gt;

34.     &lt;/c:forEach&gt;
35. &lt;/table&gt;

brand.jsp负责显示

##### 添加

1.  Dao层

BrandMapper.java

1.  @Insert("insert into tb_brand values (null,#{brandName},#{companyName},#{ordered},#{description},#{status})")
2.  @ResultMap("brandResultMap")
3.  void add(Brand brand);

1.  Service层

BrandService.java

1.  _/\*\*_
2.       \* 添加
3.       \* @param brand
4.       \*/
5.      public void add(Brand brand) {

7.          _//调用brandMapper.add(brand)_

9.          _//2.获取SqlSession对象_
10.         SqlSession sqlSession = factory.openSession();

12.         _//3.获取brandMapper_
13.         BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

15.         mapper.add(brand);

17.         _//提交事务_
18.         sqlSession.commit();
19.         sqlSession.close();
20.     }

增删改行为需要提交事务

1.  Web层

对brand.jsp进行修改

1.  &lt;input type="button" value="新增" id="add"&gt;&lt;br&gt;
2.  ...
3.  &lt;script&gt;
4.      document.getElementById("add").onclick = function () {
5.          location.href = "/brand-demo/addBrand.jsp"
6.      }
7.  &lt;/script&gt;

在新增按钮上添加id，并用JavaScript的onclick事件绑定按钮

AddServlet.java

1.  @WebServlet("/addServlet")
2.  public class AddServlet extends HttpServlet {
3.      private BrandService service = new BrandService();

5.      @Override
6.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
7.          _//1.接收数据_
8.          request.setCharacterEncoding("utf-8");_//处理post请求乱码问题_
9.          String brandName = request.getParameter("brandName");
10.         String companyName = request.getParameter("companyName");
11.         String description = request.getParameter("description");
12.         String ordered = request.getParameter("ordered");
13.         String status = request.getParameter("status");

15.         _//2.封装数据_
16.         Brand brand = new Brand();
17.         brand.setBrandName(brandName);
18.         brand.setCompanyName(companyName);
19.         brand.setDescription(description);
20.         brand.setOrdered(Integer.parseInt(ordered));
21.         brand.setStatus(Integer.parseInt(status));

23.         _//3.调用service 完成添加_
24.         service.add(brand);

26.         _//转发到查询所有Servlet_
27.         request.getRequestDispatcher("/selectAllServlet").forward(request,response);

29.     }

31.     @Override
32.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
33.         this.doGet(request, response);
34.     }

新建一个添加页表单，静态页面，完成添加操作

1.  &lt;!DOCTYPE html&gt;
2.  &lt;html lang="en"&gt;

4.  &lt;head&gt;
5.    &lt;meta charset="UTF-8"&gt;
6.    &lt;title&gt;添加品牌&lt;/title&gt;
7.  &lt;/head&gt;
8.  &lt;body&gt;
9.  &lt;h3&gt;添加品牌&lt;/h3&gt;
10. &lt;form action="/brand-demo/addServlet" method="post"&gt;
11.   品牌名称：&lt;input name="brandName"&gt;&lt;br&gt;
12.   企业名称：&lt;input name="companyName"&gt;&lt;br&gt;
13.   排序：&lt;input name="ordered"&gt;&lt;br&gt;
14.   描述信息：&lt;textarea rows="5" cols="20" name="description"&gt;&lt;/textarea&gt;&lt;br&gt;
15.   状态：
16.   &lt;input type="radio" name="status" value="0"&gt;禁用
17.   &lt;input type="radio" name="status" value="1"&gt;启用&lt;br&gt;

19.   &lt;input type="submit" value="提交"&gt;
20. &lt;/form&gt;
21. &lt;/body&gt;
22. &lt;/html&gt;

##### 修改-回显数据

1.  Dao层

BrandMapper.java

1.      @Select("select \* from tb_brand where id=#{id}")
2.      @ResultMap("brandResultMap")
3.      Brand selectById(int id);

1.  Service层
2.      public Brand selectById(int id) {

4.          _//调用brandMapper.selectAll()_

7.          _//2.获取SqlSession对象_
8.          SqlSession sqlSession = factory.openSession();

10.         _//3.获取brandMapper_
11.         BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

13.         _//4.调用方法_
14.         Brand brand = mapper.selectById(id);

16.         sqlSession.close();

18.         return brand;
19.     }

1.  Web层

SelectByIdServlet.java

1.  @WebServlet("/selectByIdServlet")
2.  public class SelectByIdServlet extends HttpServlet {
3.      private BrandService service = new BrandService();

5.      @Override
6.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
7.          _//接受id_
8.          String id = request.getParameter("id");

10.         _//调用service查询_
11.         Brand brand = service.selectById(Integer.parseInt(id));

13.         _//存储到request中_
14.         request.setAttribute("brand",brand);

16.         _//转发到update.jsp_
17.         request.getRequestDispatcher("/update.jsp").forward(request,response);

20.     }

22.     @Override
23.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
24.         this.doGet(request, response);
25.     }
26. }

新建update.jsp

1.  &lt;h3&gt;修改品牌&lt;/h3&gt;
2.  &lt;form action="/brand-demo/updateServlet" method="post"&gt;
3.    品牌名称：&lt;input name="brandName" value="${brand.brandName}"&gt;&lt;br&gt;
4.    企业名称：&lt;input name="companyName"value="${brand.companyName}&gt;&lt;br&gt;
5.    排序：&lt;input name="ordered"value="${brand.ordered}&gt;&lt;br&gt;
6.    描述信息：&lt;textarea rows="5" cols="20" name ="description"${brand.brandName}&gt;&lt;/textarea&gt;&lt;br&gt;
7.    状态：
8.    &lt;c:if test="${brand.status == 1}"&gt;
9.      &lt;input type="radio" name="status" value="1" checked&gt;启用
10.     &lt;input type="radio" name="status" value="0"&gt;禁用&lt;br&gt;
11.   &lt;/c:if&gt;

13.   &lt;c:if test="${brand.status == 0}"&gt;
14.   &lt;input type="radio" name="status" value="0" checked&gt;禁用
15.   &lt;input type="radio" name="status" value="1"&gt;启用&lt;br&gt;
16.   &lt;/c:if&gt;

18.   &lt;input type="submit" value="提交"&gt;
19. &lt;/form&gt;

修改brand.jsp

&lt;td&gt;&lt;a href="/brand-demo/selectByIdServlet?id=${brand.id}"&gt;修改&lt;/a&gt; 

修改处使用超链接，跳转到selectByIdServlet，

${brand.id} 是 JSP EL 表达式，表示从 brand 对象中获取 id 属性的值。

##### 修改-修改数据

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

8.      _//调用brandMapper.add(brand)_

10.     _//2.获取SqlSession对象_
11.     SqlSession sqlSession = factory.openSession();

13.     _//3.获取brandMapper_
14.     BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

16.     mapper.update(brand);

18.     _//提交事务_
19.     sqlSession.commit();
20.     sqlSession.close();
21. }

1.  Web层

UpdateServlet.java

1.  @WebServlet("/updateServlet")
2.  public class UpdateServlet extends HttpServlet {
3.      private BrandService service = new BrandService();

5.      @Override
6.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
7.          _//1.接收数据_
8.          request.setCharacterEncoding("utf-8");_//处理post请求乱码问题_
9.          String id = request.getParameter("id");
10.         String brandName = request.getParameter("brandName");
11.         String companyName = request.getParameter("companyName");
12.         String description = request.getParameter("description");
13.         String ordered = request.getParameter("ordered");
14.         String status = request.getParameter("status");

16.         _//2.封装数据_
17.         Brand brand = new Brand();
18.         brand.setId(Integer.parseInt(id));
19.         brand.setBrandName(brandName);
20.         brand.setCompanyName(companyName);
21.         brand.setDescription(description);
22.         brand.setOrdered(Integer.parseInt(ordered));
23.         brand.setStatus(Integer.parseInt(status));

25.         _//3.调用service 完成修改_
26.         service.update(brand);

28.         _//转发到查询所有Servlet_
29.         request.getRequestDispatcher("/selectAllServlet").forward(request,response);

31.     }

33.     @Override
34.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
35.         this.doGet(request, response);
36.     }
37. }

新建update.jsp

1.  &lt;h3&gt;修改品牌&lt;/h3&gt;
2.  &lt;form action="/brand-demo/updateServlet" method="post"&gt;

4.    &lt;%--隐藏域，提交id--%&gt;
5.    &lt;input type="hidden" name="id" value="${brand.id}"&gt;

7.    品牌名称：&lt;input name="brandName" value="${brand.brandName}"&gt;&lt;br&gt;
8.    企业名称：&lt;input name="companyName"value="${brand.companyName}"&gt;&lt;br&gt;
9.    排序：&lt;input name="ordered"value="${brand.ordered}"&gt;&lt;br&gt;
10.   描述信息：&lt;textarea rows="5" cols="20" name="description"${brand.description}&gt;&lt;/textarea&gt;&lt;br&gt;
11.   状态：
12.   &lt;c:if test="${brand.status == 1}"&gt;
13.     &lt;input type="radio" name="status" value="1" checked&gt;启用
14.     &lt;input type="radio" name="status" value="0"&gt;禁用&lt;br&gt;
15.   &lt;/c:if&gt;

17.   &lt;c:if test="${brand.status == 0}"&gt;
18.   &lt;input type="radio" name="status" value="0" checked&gt;禁用
19.   &lt;input type="radio" name="status" value="1"&gt;启用&lt;br&gt;
20.   &lt;/c:if&gt;
21.   &lt;input type="submit" value="提交"&gt;
22. &lt;/form&gt;

##### 删除数据

见brand-demo

### 会话跟踪技术

- 会话：用户打开浏览器，访问web服务器的资源，会话建立，直到有一方断开连接，会话结束，在一次会话中包含多次请求和响应
- 会话跟踪：是一种维护浏览器状态的方法，服务器需要识别多次请求是否来自同一浏览器，以便在同一次会话的多次请求间共享数据
- HTTP协议是无状态的，每次浏览器向服务器请求时，服务器都会将该请求视为新的请求，因此需要会话跟踪技术来实现会话内数据共享
- 实现方式：客户端会话跟踪技术（cookie），服务端会话跟踪技术（Session）
- 目的：一次会话的多次请求间获取数据

#### Cookie基本使用

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

#### Cookie原理

- Cookie的实现是基于HTTP协议的
- 发送cookie响应头：set-cookie
- 获取cookie请求头：cookie

#### Cookie使用细节

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

#### Session基本使用

- 服务端会话跟踪技术：将数据保存到服务端
- JavaEE提供HttpSession接口，来实现一次会话的多次请求间数据共享功能
- 使用

1.  获取Session对象

HttpSession session = request.getSession();

1.  Session对象功能

- void setAttribute（String name，Object o）：存储数据到session域中
- Object getAttribute（String name）：根据key，获取值
- void removeAttribute（String name）：根据key，删除该键值对

#### Session原理

- Session是基于Cookie实现的
- 一次会话的多个请求间，不论获取多少次session对象，获取的session对象始终是同一个
- 通过COOKIE对象中的JSESSIONID来实现，查找id

#### Session使用细节

- Session钝化，活化（自动实现）
- 服务器正常重启后，Session中的数据仍然存在
- 钝化：在服务器正常关闭后，Tomcat会自动将Session数据写入硬盘的文件
- 活化：再次启动服务器后，从文件中加载数据到Session中，但是session不是同一个session对象
- Session销毁
- 默认情况下，无操作，30分钟自动销毁，使用session-config标签配置时间

1.  &lt;session-config&gt;
2.       &lt;session-timeout&gt;100&lt;/session-timeout&gt;
3.  &lt;/session-config&gt;

- 调用Session对象的invalidate（）方法

#### 小结

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

#### 登录注册案例

##### 需求说明

- 完成用户登录功能，如果用户勾选“记住用户”，则下次访问登录页面，自动填充用户名和密码
- 完成注册功能，并实现验证码功能

##### 用户登录

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

1.  Service层

新建UserService并在其中创建方法login

1.  public class UserService {

3.      SqlSessionFactory factory = SqlSessionFactoryUtils.getSqlSessionFactory();

5.      _/\*\*_
6.       \* 登录
7.       \* @param username
8.       \* @param password
9.       \* @return
10.      \*/
11.     public User login(String username,String password){        _//2. 获取SqlSession_
12.         _//获取sqlSession_
13.         SqlSession sqlSession = factory.openSession();

15.         _//获取UserMapper_
16.         UserMapper mapper = sqlSession.getMapper(UserMapper.class);

18.         _//调用方法_
19.         User user = mapper.select(username,password);

22.         _//释放资源_
23.         sqlSession.close();

26.         return null ;
27.     }
28. }

1.  Web层

导入css/imgs文件到webapp包中

新建login.jsp定义静态页面并定义action

&lt;form action="/brand-demo/loginServlet" id="form"&gt;

新建loginServlet完成业务

1.  @WebServlet("/loginServlet")
2.  public class LoginServlet extends HttpServlet {
3.      private UserService service = new UserService();

5.      @Override
6.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
7.          _//1.获取用户名和密码_
8.          String username = request.getParameter("username");
9.          String password = request.getParameter("password");

11.         _//2.调用service查询_
12.         User user = service.login(username,password);

14.         if (user != null){
15.             _//登录成功，跳转到查询所有的BrandServlet_

17.             _//将登录成功后的user对象存储到session中_
18.             HttpSession session = request.getSession();
19.             session.setAttribute("user",user);

21.             String contextPath = request.getContextPath();
22.             response.sendRedirect(contextPath + "/selectAllServlet");
23.         }else{
24.             _//登录失败_

26.             _//错误信息到request_
27.             request.setAttribute("login_msg","用户名或密码错误");

29.             _//跳转到login.jsp_
30.             request.getRequestDispatcher("/login.jsp").forward(request,response);
31.         }
32.     }

34.     @Override
35.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
36.         this.doGet(request, response);
37.     }
38. }

- 登录成功，跳转到查询所有的BrandServlet中，登录请求与查询所有的请求之间没有数据需要共享，使用重定向，如果资源跳转需要资源共享，则需要转发
- 登录成功是一次请求，重定向到另一个页面是另一次请求，同一会话的两次请求之间共享数据需要把数据存在cookie或者session，这里有安全性要求，所以登录成功后将登录成功的user对象存储到session域中，然后使用EL表达式查找
- 登录失败，要携带用户名登录错误这类错误信息提示跳转回login页面，可以采用将数据存到request域中，将其转发回对应的login.jsp，request域中存的数据只能通过转发的形式才能获取这个数据

修改login.jsp

&lt;div id="errorMsg"&gt;${login_msg}&lt;/div&gt;

- 使用EL表达式，这里称为动态的表达

##### 记住用户--写Cookie

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

7.          _//获取复选框数据_
8.          String remember = request.getParameter("remember");

10.         _//2.调用service查询_
11.         User user = service.login(username,password);

13.         if (user != null){
14.             _//登录成功，跳转到查询所有的BrandServle_

16.             _//判断用户是否勾选记住我_

18.             if("1".equals(remember)){
19.                 _//勾选了记住我_

21.                 _//创建Cookie_
22.                 Cookie c_username = new Cookie("username",username);
23.                 Cookie c_password = new Cookie("password",password);

26.                 _//设置Cookie的存活时间_
27.                 c_username.setMaxAge( 60\*60\*24\*7 );
28.                 c_password.setMaxAge( 60\*60\*24\*7 );

30.                 _//发送_
31.                 response.addCookie(c_username);
32.                 response.addCookie(c_password);

34.             }
35.             _//将登录成功后的user对象存储到session中_
36.             HttpSession session = request.getSession();
37.             session.setAttribute("user",user);

39.             String contextPath = request.getContextPath();
40.             response.sendRedirect(contextPath + "/selectAllServlet");
41.         }else{
42.             _//登录失败_
43.             _//错误信息到request_
44.             request.setAttribute("login_msg","用户名或密码错误");

46.             _//跳转到login.jsp_
47.             request.getRequestDispatcher("/login.jsp").forward(request,response);
48.         }
49.     }

修改Login.jsp

&lt;p&gt;Remember:&lt;input id="remember" name="remember" value ="1" type="checkbox"&gt;&lt;/p&gt;

加入value使得确认remember复选框的内容

##### 记住用户--获取Cookie

- 在页面获取cookie数据后，设置到用户名和密码框中：EL表达式
- ${cookie.key.value}//key指存储在cookie中的键名称

修改login.jsp

1.  &lt;p&gt;Username:&lt;input id="username" name="username" value ="${cookie.username.value}"type="text"&gt;&lt;/p&gt;

3.  &lt;p&gt;Password:&lt;input id="password" name="password" type="password" value ="${cookie.password.value}"&gt;&lt;/p&gt;

##### 用户注册--注册功能

保存用户信息到数据库

1.  Dao层
2.      _/\*\*_
3.       \* 根据用户名查询用户对象
4.       \* @param username
5.       \* @return
6.       \*/
7.      @Select("select \* from tb_user where username = #{username}")
8.      User selectByUsername(String username);

10.     _/\*\*_
11.      \* 添加用户
12.      \* @param user
13.      \*/
14.     @Insert("insert into tb_user values(null,#{username},#{password})")
15.     void add(User user);

1.  Service层
2.  public boolean register(User user){
3.          _//获取sqlSession_
4.          SqlSession sqlSession = factory.openSession();

6.          _//获取UserMapper_
7.          UserMapper mapper = sqlSession.getMapper(UserMapper.class);

9.          _//判断用户名是否存在_
10.         User u = mapper.selectByUsername(user.getUsername());

12.         if (u == null){
13.             _//用户名不存在，注册_
14.             mapper.add(user);
15.             sqlSession.commit();

17.         }
18.         sqlSession.close();

20.         return u == null;
21.     }

1.  Web层

新建RegisterServlet

1.  @WebServlet("/registerServlet")
2.  public class RegisterServlet extends HttpServlet {
3.      private UserService service = new UserService();

5.      @Override
6.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
7.          _//获取用户名和密码数据_
8.          String username = request.getParameter("username");
9.          String password = request.getParameter("password");

11.         User user = new User();
12.         user.setUsername(username);
13.         user.setPassword(password);

15.         _//调用service查询_
16.         boolean flag = service.register(user);
17.         _//判断注册成功与否_
18.         if (flag){
19.             _//注册功能，跳转登录页面_

21.             request.setAttribute("register_msg","注册成功请登录");
22.             request.getRequestDispatcher("/login.jsp").forward(request,response);

24.         }else{
25.             _//注册失败，跳转到注册页面_

27.             request.setAttribute("register_msg","用户名已存在");
28.             request.getRequestDispatcher("/register.jsp").forward(request,response);

30.         }

33.     }

35.     @Override
36.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
37.         this.doGet(request, response);
38.     }
39. }

修改login.jsp

&lt;div id="errorMsg"&gt;${login_msg}${register_msg}&lt;/div&gt;

##### 用户注册--验证码功能

- 验证码就是使用Java代码生成的一张图片
- 验证码作用：防止机器自动注册，攻击服务器

导入CheckCodeUtil，生成验证码工具类

新建CheckCodeServlet类-生成一个验证码图片

1.  @WebServlet("/checkCodeServlet")
2.  public class CheckCodeServlet extends HttpServlet {

4.      @Override
5.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

7.     ServletOutputStream os = response.getOutputStream();
8.     String checkCode = CheckCodeUtil.outputVerifyImage(100, 50, os, 4);
9.      }

11.     @Override
12.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
13.         this.doGet(request, response);
14.     }
15. }

实现点击看不清，验证码图片更换一张

修改register.jsp

1.  &lt;div class="form-div"&gt;
2.      &lt;div class="reg-content"&gt;
3.          &lt;h1&gt;欢迎注册&lt;/h1&gt;
4.          &lt;span&gt;已有账号？&lt;/span&gt; &lt;a href="login.html"&gt;登录&lt;/a&gt;
5.      &lt;/div&gt;
6.      &lt;form id="reg-form" action="/brand-demo/registerServlet" method="post"&gt;

8.          &lt;table&gt;

10.             &lt;tr&gt;
11.                 &lt;td&gt;用户名&lt;/td&gt;
12.                 &lt;td class="inputs"&gt;
13.                     &lt;input name="username" type="text" id="username"&gt;
14.                     &lt;br&gt;
15.                     &lt;span id="username_err" class="err_msg"&gt;${register_msg}&lt;/span&gt;
16.                 &lt;/td&gt;

18.             &lt;/tr&gt;

20.             &lt;tr&gt;
21.                 &lt;td&gt;密码&lt;/td&gt;
22.                 &lt;td class="inputs"&gt;
23.                     &lt;input name="password" type="password" id="password"&gt;
24.                     &lt;br&gt;
25.                     &lt;span id="password_err" class="err_msg" style="display: none"&gt;密码格式有误&lt;/span&gt;
26.                 &lt;/td&gt;
27.             &lt;/tr&gt;

30.             &lt;tr&gt;
31.                 &lt;td&gt;验证码&lt;/td&gt;
32.                 &lt;td class="inputs"&gt;
33.                     &lt;input name="checkCode" type="text" id="checkCode"&gt;
34.                     &lt;img id="checkCodeImg" src="/brand-demo/checkCodeServlet"&gt;
35.                     &lt;a href="#" id="changeImg" &gt;看不清？&lt;/a&gt;
36.                 &lt;/td&gt;
37.             &lt;/tr&gt;

39.         &lt;/table&gt;

41.         &lt;div class="buttons"&gt;
42.             &lt;input value="注 册" type="submit" id="reg_btn"&gt;
43.         &lt;/div&gt;
44.         &lt;br class="clear"&gt;
45.     &lt;/form&gt;

47. &lt;/div&gt;

49. &lt;script&gt;
50.     document.getElementById("changeImg").onclick = function (){
51.         document.getElementById("checkCodeImg").src = "/brand-demo/checkCodeServlet?time="+new Date().getTime();
52.     }
53. &lt;/script&gt;

主要修改在30-53行之间 对图片src进行修改，使得通过servlet生成，并对看不清超链接设置id”changeImg”，然后使用getElementId查护照这个超链接，绑定单击事件，使得再一次请求时更换图片，但是不能单一请求/brand-demo/checkCodeServlet，因为图片路径 已经载入缓存，只需要加一个参数使用时间，确保不重复。

##### 用户注册--校验验证码

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

4.  _//程序生成的验证码，从Session中获取_
5.  HttpSession session = request.getSession();
6.  String checkCodeGen = (String) session.getAttribute("checkCodeGen");

8.  _//比对_
9.  if(!checkCodeGen.equalsIgnoreCase(checkCode)){
10. _//不允许注册_
11. request.setAttribute("register_msg","验证码错误");
12. request.getRequestDispatcher("/register.jsp").forward(request,response);
13. return;
14. }

在RegisterServlet中获取用户输入的验证码，并获取Session中存储的CheckCodeServlet中存入的生成验证码，并进行比对

### Filter & Listener

- 概念：Filter表示过滤器，是JavaWeb三大组件（Servlet，Filter，Listener）之一
- 过滤器可以把资源的请求拦截下来，从而实现一些特殊的功能
- 过滤器一般完成一些通用的操作，比如权限控制，统一编码处理，敏感字符处理等等...

#### Filter

##### Filter快速入门

（类似Servlet）

1.  定义类，实现Filter接口，并重写其所有方法
2.  配置Filter拦截资源的路径：在类上定义@WebFilter注解
3.  在doFilter方法中输出一句话，并放行
4.  @WebFilter("/\*")
5.  public class FilterDemo implements Filter {
6.      @Override
7.      public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {

9.          _//1. 放行前，对 request数据进行处理_
10.         System.out.println("1.FilterDemo...");

12.         _//放行_
13.         chain.doFilter(request,response);
14.         _//2. 放行后，对Response 数据进行处理_
15.         System.out.println("5.FilterDemo...");
16.     }

18.     @Override
19.    public void init(FilterConfig filterConfig) throws ServletException {}

23.     @Override
24.     public void destroy() {}

##### Filter执行流程

- Filter：执行放行前逻辑-放行-访问资源-执行放行后逻辑
- 放行后访问对应资源，资源访问完成后还会回到Filter中
- 回到Filter会执行放行后逻辑而不是从头逻辑

##### Filter使用细节

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

##### 案例

需求：访问服务器资源时，需要先进行登录验证，如果没有登录，则自动跳转到登录页面

新建LoginFilter实现登录验证的过滤

1.  _/\*\*_
2.   \* 登录验证过滤器
3.   \*/
4.  @WebFilter("/\*")
5.  public class LoginFilter implements Filter {
6.      @Override
7.    public void init(FilterConfig filterConfig) throws ServletException {}

9.      @Override
10.     public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {

12.         HttpServletRequest req = (HttpServletRequest) request;

14.         _//判断session中是否有user_
15.         HttpSession session = req.getSession();
16.         Object user = session.getAttribute("user");

18.         if(user != null){
19.             _//登录过了_
20.             _//放行_
21.             chain.doFilter(request,response);
22.         }else{

24.             req.setAttribute("login_msg","您尚未登录");
25.             req.getRequestDispatcher("/login.jsp").forward(req,response);
26.         }

29.         _//放行_
30.         chain.doFilter(request,response);

32.     }

34.     @Override
35.     public void destroy() {}
36. }

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

#### Listener

- Listener监听器，是JavaWeb三大组件（Servlet，Filter，Listener）之一
- 监听器可以监听在application，session，request三个对象创建，销毁或者往其中添加修改删除属性是自动执行代码的功能组件

##### Listener分类

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

##### ServletContextListener使用

1.  定义类，实现ServletContextListener接口
2.  在类上添加@WebListener注解
3.  @WebListener
4.  public class ContextLoaderListener implements ServletContextListener {

6.      _/\*\*_
7.       \* ServletContext对象被创建，整个web应用发布成功
8.       \* @param servletContextEvent
9.       \*/
10.     @Override
11.     public void contextInitialized(ServletContextEvent servletContextEvent) {}

13.     _/\*\*_
14.      \* ServletContext对象被销毁，整个web应用卸载
15.      \* @param servletContextEvent
16.      \*/
17.     @Override
18.     public void contextDestroyed(ServletContextEvent servletContextEvent) {}
19. }

### AJAX

- Asnchronous JavaScript And XML：异步的JavaScript和XML
- AJAX作用：
- 与服务器进行数据交换：通过AJAX可以给服务器发送请求，并获取服务器响应的数据，

在此之前通过Servlet查询数据，将数据存到域对象中，转发到JSP展示数据，将JSP当作视图，对浏览器做响应

- 使用AJAX和服务器进行通信，就可以使用HTML+AJAX来替换JSP页面了
- 实现前后端分离，前端HTML+AJAX 后端负责数据提交逻辑处理
- 异步交互：可以在不重新加载整个页面的情况下，与服务器交换数据，并更新部分网页的技术，如：搜索联想，用户名是否可用校验...

#### AJAX快速入门

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

1.  向服务器发送请求
2.  xhttp.open("GET", "http://localhost:8080/ajax-demo/ajaxServlet");
3.      xhttp.send();

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

#### 案例

使用AJAX验证用户名是否存在

需求：在完成用户注册时，当用户名输入框失去焦点时，校验用户名是否在数据库已存在

SelectUserServlet.java

1.  @WebServlet("/selectUserServlet")
2.  public class SelectUserServlet extends HttpServlet {
3.      @Override
4.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

6.          _//1. 接收用户名_
7.          String username = request.getParameter("username");

9.          _//2. 调用service查询User对象_

11.         boolean flag = true;

13.         _//3. 响应标记_
14.         response.getWriter().write("" + flag);

16.     }

18.     @Override
19.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
20.         this.doGet(request, response);
21.     }
22. }

Register.html

在前面配置好静态页面

1.  &lt;script&gt;

3.      _//1. 给用户名输入框绑定 失去焦点事件_
4.      document.getElementById("username").onblur = function () {
5.          _//2. 发送ajax请求_
6.          _// 获取用户名的值_
7.          var username = this.value;

9.          _//2.1. 创建核心对象_
10.         var xhttp;
11.         if (window.XMLHttpRequest) {
12.             xhttp = new XMLHttpRequest();
13.         } else {
14.             _// code for IE6, IE5_
15.             xhttp = new ActiveXObject("Microsoft.XMLHTTP");
16.         }
17.         _//2.2. 发送请求_
18.         xhttp.open("GET", "http://localhost:8080/ajax-demo/selectUserServlet?username="+username);
19.         xhttp.send();

21.         _//2.3. 获取响应_
22.         xhttp.onreadystatechange = function() {
23.             if (this.readyState == 4 && this.status == 200) {
24.                 _//alert(this.responseText);_
25.                 _//判断_
26.                 if(this.responseText == "true"){
27.                     _//用户名存在，显示提示信息_
28.                     document.getElementById("username_err").style.display = '';
29.                 }else {
30.                     _//用户名不存在 ，清除提示信息_
31.                     document.getElementById("username_err").style.display = 'none';
32.                 }
33.             }
34.         };

36.     }
37. &lt;/script&gt;

当用户名输入框失去焦点（绑定事件）时，校验用户名是否在数据库已存在

#### Axios异步框架

Axios对原生的AJAX进行封装，简化书写

[Axios-中文](https://www.axios-http.cn/)

1.  引入axios的js文件

在webapp中创建一个js包，用来存放所有的js文件 这里存入axios源码

&lt;script src="js/axios-0.18.0.js"&gt;&lt;/script&gt;

1.  使用axios发送请求，并获取响应结果

AxiosServlet.java

1.  @WebServlet("/axiosServlet")
2.  public class AxiosServlet extends HttpServlet {
3.      @Override
4.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
5.          System.out.println("get...");

7.          _//1. 接收请求参数_
8.          String username = request.getParameter("username");
9.          System.out.println(username);

11.         _//2. 响应数据_
12.         response.getWriter().write("hello Axios~");
13.     }

15.     @Override
16.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
17.         System.out.println("post...");
18.         this.doGet(request, response);
19.     }
20. }

axios-demo.html

1.  &lt;script&gt;
2.      _//1. get_
3.      axios({
4.          method:"get",
5.          url:"http://localhost:8080/ajax-demo/axiosServlet?username=zhangsan"
6.      }).then(function (resp) {
7.          alert(resp.data);
8.      })

11.     _//2. post_
12.     axios({
13.         method:"post",
14.         url:"http://localhost:8080/ajax-demo/axiosServlet",
15.         data:"username=zhangsan"
16.     }).then(function (resp) {
17.         alert(resp.data);
18.     })

20. &lt;/script&gt;

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

7.      _// 使用 axios 发送 GET 请求_
8.      axios.request({
9.          method: 'get',
10.         url: 'http://localhost:8080/ajax-demo/selectUserServlet?username=zhangsan',
11.     }).then(function (response) {
12.         _// 处理响应结果_
13.         if (response.data === "true") {
14.             _// 用户名存在，显示提示信息_
15.             document.getElementById("username_err").style.display = '';
16.         } else {
17.             _// 用户名不存在，隐藏提示信息_
18.             document.getElementById("username_err").style.display = 'none';
19.         }
20. }).

#### JSON

- JavaScript Object Notation，JavaScript对象表示法
- 由于语法简单，层次结构鲜明，多用于数据载体，在网络中进行数据传输

##### JSON基础语法

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

##### JSON数据和Java对象转换

请求数据：JSON字符串转为Java对象

响应数据：Java对象转为JSON字符串

- Fastjson：一个Java语言编写的高性能功能完善的JSON库，可以实现Java和JSON字符串的相互转换
- 使用：
    1.  导入坐标

1.  &lt;dependency&gt;
2.      &lt;groupId&gt;com.alibaba&lt;/groupId&gt;
3.      &lt;artifactId&gt;fastjson&lt;/artifactId&gt;
4.      &lt;version&gt;1.2.62&lt;/version&gt;
5.  &lt;/dependency&gt;

- 1.  Java对象转JSON

String jsonStr = JSON.toJSONString();

- 1.  JSON字符串转Java对象

User user = JSON.parseObject(jsonStr,User.class);

##### 案例

需求：完成品牌列表查询和添加

之前使用servlet + jsp完成品牌查询

###### 查询所有

使用Axios+JSON

1.  service层
2.      _/\*\*_
3.       \* 查询所有
4.       \* @return
5.       \*/
6.      public List&lt;Brand&gt; selectAll(){
7.          _//调用BrandMapper.selectAll()_

9.          _//2. 获取SqlSession_
10.         SqlSession sqlSession = factory.openSession();
11.         _//3. 获取BrandMapper_
12.         BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

14.         _//4. 调用方法_
15.         List&lt;Brand&gt; brands = mapper.selectAll();

17.         sqlSession.close();

19.         return brands;
20.     }

1.  Web层

SelectAllServlet.java

1.  @WebServlet("/selectAllServlet")
2.  public class SelectAllServlet extends HttpServlet {
3.      private BrandService brandService = new BrandService();

5.      @Override
6.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
7.          _//1. 调用Service查询_
8.          List&lt;Brand&gt; brands = brandService.selectAll();

10.         _//2. 将集合转换为JSON数据   序列化_
11.         String jsonString = JSON.toJSONString(brands);

13.         _//3. 响应数据，响应到对应页面上_
14.         response.setContentType("text/json;charset=utf-8");
15.         response.getWriter().write(jsonString);
16.     }

18.     @Override
19.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
20.         this.doGet(request, response);
21.     }
22. }

返回一个json数据 其中存放brand集合列表中的brands数据

Brand.html

1.  &lt;script&gt;
2.      _//1. 当页面加载完成后，发送ajax请求_
3.      window.onload = function () {
4.          _//2. 发送ajax请求_
5.          axios({
6.              method:"get",
7.              url:"http://localhost:8080/brand-demo/selectAllServlet"
8.          }).then(function (resp) {
9.              _//获取数据_
10.             let brands = resp.data;
11.             let tableData = " &lt;tr&gt;\\n" +
12.                 "        &lt;th&gt;序号&lt;/th&gt;\\n" +
13.                 "        &lt;th&gt;品牌名称&lt;/th&gt;\\n" +
14.                 "        &lt;th&gt;企业名称&lt;/th&gt;\\n" +
15.                 "        &lt;th&gt;排序&lt;/th&gt;\\n" +
16.                 "        &lt;th&gt;品牌介绍&lt;/th&gt;\\n" +
17.                 "        &lt;th&gt;状态&lt;/th&gt;\\n" +
18.                 "        &lt;th&gt;操作&lt;/th&gt;\\n" +
19.                 "    &lt;/tr&gt;";

21.             for (let i = 0; i < brands.length ; i++) {
22.                 let brand = brands\[i\];

24.                 tableData += "\\n" +
25.                     "    &lt;tr align=\\"center\\"&gt;\\n" +
26.                     "        &lt;td&gt;"+(i+1)+"&lt;/td&gt;\\n" +
27.                     "        &lt;td&gt;"+brand.brandName+"&lt;/td&gt;\\n" +
28.                     "        &lt;td&gt;"+brand.companyName+"&lt;/td&gt;\\n" +
29.                     "        &lt;td&gt;"+brand.ordered+"&lt;/td&gt;\\n" +
30.                     "        &lt;td&gt;"+brand.description+"&lt;/td&gt;\\n" +
31.                     "        &lt;td&gt;"+brand.status+"&lt;/td&gt;\\n" +
32.                     "\\n" +
33.                     "        &lt;td&gt;&lt;a href=\\"#\\"&gt;修改&lt;/a&gt; &lt;a href=\\"#\\"&gt;删除&lt;/a&gt;&lt;/td&gt;\\n" +
34.                     "    &lt;/tr&gt;";
35.             }

37.           _// 设置表格数据_
38.           document.getElementById("brandTable").innerHTML = tableData;
39.         })
40.     }

通过resp接收数据brands，在brand中遍历数组brands，获得brand对象，将brand数据放到tr中，通过拼字符串的形式，对表格数据进行修改。

###### 新增品牌

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

1.  &lt;script&gt;
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

17.         _// 获取表单数据_
18.         let companyName = document.getElementById("companyName").value;
19.         _// 设置数据_
20.         formData.companyName = companyName;

22.         _// 获取表单数据_
23.         let ordered = document.getElementById("ordered").value;
24.         _// 设置数据_
25.         formData.ordered = ordered;

27.         _// 获取表单数据_
28.         let description = document.getElementById("description").value;
29.         _// 设置数据_
30.         formData.description = description;

32.         let status = document.getElementsByName("status");
33.         for (let i = 0; i < status.length; i++) {
34.             if(status\[i\].checked){
35.                 _//_
36.                 formData.status = status\[i\].value ;
37.             }
38.         }

40.         console.log(formData);
41.         _//2. 发送ajax请求_
42.         axios({
43.             method:"post",
44.             url:"http://localhost:8080/brand-demo/addServlet",
45.             data:formData
46.         }).then(function (resp) {
47.             _// 判断响应数据是否为 success_
48.             if(resp.data == "success"){
49.                 location.href = "http://localhost:8080/brand-demo/brand.html";
50.             }
51.         })
52.     }
53. &lt;/script&gt;

增删改一般建议使用post的请求方式，var formdata操作是为了创建json对象

Console.log用于在控制台输出任何类型的信息

addServlet.java

1.  @WebServlet("/addServlet")
2.  public class AddServlet extends HttpServlet {

4.      private BrandService brandService = new BrandService();

6.      @Override
7.      protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

9.          _//1. 接收数据,request.getParameter 不能接收json的数据_
10.        _/\* String brandName = request.getParameter("brandName");_
11.         System.out.println(brandName);\*/

13.         _// 获取请求体数据_
14.         BufferedReader br = request.getReader();
15.         String params = br.readLine();

17.         _// 将JSON字符串转为Java对象_
18.         Brand brand = JSON.parseObject(params, Brand.class);

21.         _//2. 调用service 添加_
22.         brandService.add(brand);

24.         _//3. 响应成功标识_
25.         response.getWriter().write("success");
26.     }

28.     @Override
29.     protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
30.         this.doGet(request, response);
31.     }
32. }

Request.getParameter不能接收json数据，需要通过bufferreader来获取请求体数据，并把json字符转为java对象，使得json数据可以被add方法调用

application/x- www-form-urlencoded是Post请求默认的请求体内容类型，也是form表单默认的类型。[Servlet](https://so.csdn.net/so/search?q=Servlet&spm=1001.2101.3001.7020"%20\t%20"https://blog.csdn.net/qq_36719449/article/details/_blank) API规范中对该类型的请求内容提供了request.getParameter()方法来获取请求参数值。但当请求内容不是该类型时，需要调用request.getInputStream()或request.getReader()方法来获取请求内容值。

### Vue

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

14.         _// 获取表单数据_
15.         let companyName = document.getElementById("companyName").value;
16.         _// 设置数据_
17.         formData.companyName = companyName;

19.         _// 获取表单数据_
20.         let ordered = document.getElementById("ordered").value;
21.         _// 设置数据_
22.         formData.ordered = ordered;

24.         _// 获取表单数据_
25.         let description = document.getElementById("description").value;
26.         _// 设置数据_
27.         formData.description = description;

29.         let status = document.getElementsByName("status");
30.         for (let i = 0; i < status.length; i++) {
31.             if(status\[i\].checked){
32.                 _//_
33.                 formData.status = status\[i\].value ;
34.             }
35.         }

- 基于MVVM（Model-View-ViewModel）思想，实现数据的双向绑定，将编程的关注点放在数据上，当ViewModel中的数据发生变化时，数据绑定会自动更新View中绑定到这些数据的部分，反之亦然

#### Vue快速入门

1.  新建HTML页面，引入Vue.js文件

&lt;script src="js/vue.js"&gt;&lt;/script&gt;

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
2.  &lt;div id="app"&gt;

4.      &lt;input v-model="username"&gt;
5.      _&lt;!--插值表达式--&gt;_
6.      {{username}}

8.  &lt;/div&gt;

插值表达式，取出模型数据

#### Vue常用指令

指令：HTML标签上带有v-前缀的特殊属性，不同指令具有不同翻译

1.  v-bind：为HTML标签绑定属性值，如设置href，css样式等

讲话书写：直接在href前加 ：即可

1.  &lt;div id="app"&gt;

3.     &lt;a v-bind:href="url"&gt;点击一下&lt;/a&gt;

5.      &lt;a :href="url"&gt;点击一下&lt;/a&gt;

8.      &lt;input v-model="url"&gt;

10. &lt;/div&gt;

12. &lt;script src="js/vue.js"&gt;&lt;/script&gt;
13. &lt;script&gt;

15.     _//1. 创建Vue核心对象_
16.     new Vue({
17.         el:"#app",
18.         data(){
19.             return {
20.                 username:"",
21.                 url:"https://www.baidu.com"
22.             }
23.         }
24.     });

26. &lt;/script&gt;

1.  v-model：在表单元素上创建双向数据绑定
2.  v-on：为HTML标签绑定事件

简化书写：@

1.  &lt;div id="app"&gt;

5.      &lt;input type="button" value="一个按钮" v-on:click="show()"&gt;&lt;br&gt;
6.      &lt;input type="button" value="一个按钮" @click="show()"&gt;

8.  &lt;/div&gt;

10. &lt;script src="js/vue.js"&gt;&lt;/script&gt;
11. &lt;script&gt;

13.     _//1. 创建Vue核心对象_
14.     new Vue({
15.         el:"#app",
16.         data(){
17.             return {
18.                 username:"",
19.                 url:"https://www.baidu.com"
20.             }
21.         },
22.         methods:{
23.             show(){
24.                 alert("我被点了...");
25.             }
26.         }
27.     });

29. &lt;/script&gt;

1.  v-if与v-show

实现效果一样，但底层渲染不一致

If条件性地渲染某元素，判断为true时渲染，否则不渲染

Show根据条件展示莫元素，区别在于切换的是display属性的值

1.  &lt;div id="app"&gt;

3.      &lt;div v-if="count == 3"&gt;div1&lt;/div&gt;
4.      &lt;div v-else-if="count == 4"&gt;div2&lt;/div&gt;
5.      &lt;div v-else&gt;div3&lt;/div&gt;
6.      &lt;hr&gt;
7.      &lt;div v-show="count == 3"&gt;div v-show&lt;/div&gt;
8.      &lt;br&gt;

10.     &lt;input v-model="count"&gt;

13. &lt;/div&gt;

15. &lt;script src="js/vue.js"&gt;&lt;/script&gt;
16. &lt;script&gt;

18.     _//1. 创建Vue核心对象_
19.     new Vue({
20.         el:"#app",
21.         data(){
22.             return {
23.                 username:"",
24.                 url:"https://www.baidu.com",
25.                 count:3
26.             }
27.         },
28.         methods:{
29.             show(){
30.                 alert("我被点了...");
31.             }
32.         }
33.     });

35. &lt;/script&gt;

1.  v-for

列表渲染，遍历容器的元素和对象的属性

1.  &lt;div id="app"&gt;

3.      &lt;div v-for="addr in addrs"&gt;
4.          {{addr}} &lt;br&gt;
5.      &lt;/div&gt;

7.      &lt;hr&gt;
8.      &lt;div v-for="(addr,i) in addrs"&gt;
9.          {{i+1}}--{{addr}} &lt;br&gt;
10.     &lt;/div&gt;
11. &lt;/div&gt;

13. &lt;script src="js/vue.js"&gt;&lt;/script&gt;
14. &lt;script&gt;

16.     _//1. 创建Vue核心对象_
17.     new Vue({
18.         el:"#app",
19.         data(){
20.             return {
21.                 username:"",
22.                 url:"https://www.baidu.com",
23.                 count:3,
24.                 addrs:\["北京","上海","西安"\]
25.             }
26.         },
27.         methods:{
28.             show(){
29.                 alert("我被点了...");
30.             }
31.         }
32.     });

34. &lt;/script&gt;

i表示索引，从0开始

#### Vue生命周期

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

19.         }\*/
20.         mounted(){
21.             alert("加载完成...")
22.         }
23.     });

25. &lt;/script&gt;

在这之前使用window.unload来实现页面加载完成，发送异步请求，现在可以使用mounted来代替

- beforeUpdate 更新前
- Updated 更新后
- beforeDestory 销毁前
- Destoryed 销毁后

#### 案例

需求：使用Vue简化品牌列表数据查询和添加功能

###### 查询所有

brand.html

1.  &lt;div id="app"&gt;
2.      &lt;a href="addBrand.html"&gt;&lt;input type="button" value="新增"&gt;&lt;/a&gt;&lt;br&gt;
3.      &lt;hr&gt;
4.      &lt;table id="brandTable" border="1" cellspacing="0" width="100%"&gt;
5.          &lt;tr&gt;
6.              &lt;th&gt;序号&lt;/th&gt;
7.              &lt;th&gt;品牌名称&lt;/th&gt;
8.              &lt;th&gt;企业名称&lt;/th&gt;
9.              &lt;th&gt;排序&lt;/th&gt;
10.             &lt;th&gt;品牌介绍&lt;/th&gt;
11.             &lt;th&gt;状态&lt;/th&gt;
12.             &lt;th&gt;操作&lt;/th&gt;
13.         &lt;/tr&gt;

15.         _<!--_
16.             使用v-for遍历tr
17.         -->

19.         &lt;tr v-for="(brand,i) in brands" align="center"&gt;
20.             &lt;td&gt;{{i + 1}}&lt;/td&gt;
21.             &lt;td&gt;{{brand.brandName}}&lt;/td&gt;
22.             &lt;td&gt;{{brand.companyName}}&lt;/td&gt;
23.             &lt;td&gt;{{brand.ordered}}&lt;/td&gt;
24.             &lt;td&gt;{{brand.description}}&lt;/td&gt;
25.             &lt;td&gt;{{brand.statusStr}}&lt;/td&gt;
26.             &lt;td&gt;&lt;a href="#"&gt;修改&lt;/a&gt; &lt;a href="#"&gt;删除&lt;/a&gt;&lt;/td&gt;
27.         &lt;/tr&gt;

29.     &lt;/table&gt;
30. &lt;/div&gt;
31. &lt;script src="js/axios-0.18.0.js"&gt;&lt;/script&gt;
32. &lt;script src="js/vue.js"&gt;&lt;/script&gt;

34. &lt;script&gt;

36.     new Vue({
37.         el: "#app",
38.         data(){
39.             return{
40.                 brands:\[\]
41.             }
42.         },
43.         mounted(){
44.             _// 页面加载完成后，发送异步请求，查询数据_
45.             var \_this = this;
46.             axios({
47.                 method:"get",
48.                 url:"http://localhost:8080/brand-demo/selectAllServlet"
49.             }).then(function (resp) {
50.                 \_this.brands = resp.data;
51.             })
52.         }
53.     })
54. &lt;/script&gt;

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

###### 查询所有

1.  &lt;div id="app"&gt;
2.      &lt;h3&gt;添加品牌&lt;/h3&gt;
3.      &lt;form action="" method="post"&gt;
4.          品牌名称：&lt;input id="brandName" v-model="brand.brandName" name="brandName"&gt;&lt;br&gt;
5.          企业名称：&lt;input id="companyName" v-model="brand.companyName" name="companyName"&gt;&lt;br&gt;
6.          排序：&lt;input id="ordered" v-model="brand.ordered" name="ordered"&gt;&lt;br&gt;
7.          描述信息：&lt;textarea rows="5" cols="20" id="description" v-model="brand.description" name="description"&gt;&lt;/textarea&gt;&lt;br&gt;
8.          状态：
9.          &lt;input type="radio" name="status" v-model="brand.status" value="0"&gt;禁用
10.         &lt;input type="radio" name="status" v-model="brand.status" value="1"&gt;启用&lt;br&gt;

12.         &lt;input type="button" id="btn" @click="submitForm" value="提交"&gt;
13.     &lt;/form&gt;
14. &lt;/div&gt;
15. &lt;script src="js/axios-0.18.0.js"&gt;&lt;/script&gt;

17. &lt;script src="js/vue.js"&gt;&lt;/script&gt;

19. &lt;script&gt;

21.     new Vue({
22.         el: "#app",
23.         data(){
24.             return {
25.                 brand:{}
26.             }
27.         },
28.         methods:{
29.             submitForm(){
30.                 _// 发送ajax请求，添加_
31.                 var \_this = this;
32.                 axios({
33.                     method:"post",
34.                     url:"http://localhost:8080/brand-demo/addServlet",
35.                     data:\_this.brand
36.                 }).then(function (resp) {
37.                     _// 判断响应数据是否为 success_
38.                     if(resp.data == "success"){
39.                         location.href = "http://localhost:8080/brand-demo/brand.html";
40.                     }
41.                 })

43.             }
44.         }
45.     })
46. &lt;/script&gt;

1.  _//1. 给按钮绑定单击事件_
2.      document.getElementById("btn").onclick = function () {
3.          _// 将表单数据转为json_
4.          var formData = {
5.              brandName:"",
6.              companyName:"",
7.              ordered:"",
8.              description:"",
9.              status:"",
10.         };

按钮上绑定单击事件@click 在vue中定义method submitForm 在submitForm方法中发送异步数据，请求数据，在之前的案例中data是formdata，这里在vue框架下，应该有一个模型来绑定data，所以定义一个data() 返回brand，axios中的data是通过data（）传入，与查询所有一致，也用_this传入，brand中的数据使用v-model的双向数据绑定。

### Element UI

- 一套基于Vue的网站组件库，用于快速构建网页
- 组件：组成网页的构件，例如超链接，按钮，图片，表格等等

#### Element快速入门

1.  引入Element的css，js文件和Vue.js
2.  &lt;script src="js/vue.js"&gt;&lt;/script&gt;
3.  &lt;script src="element-ui/lib/index.js"&gt;&lt;/script&gt;
4.  &lt;link rel="stylesheet" href="element-ui/lib/theme-chalk/index.css"&gt;

1.  创建Vue核心对象
2.  &lt;script&gt;
3.      new Vue({
4.          el:"#app"
5.      })

1.  官网复制Element组件代码

_[Element](https://element.eleme.cn/"%20\l%20"/zh-CN)_

#### Element布局

1.  layout布局：通过基础的24分栏，迅速简便地创建布局
2.  Contaioner布局容器：用于布局的容器组件，方便快速搭建页面的基本结构

#### Element组件

_[组件 | Element](https://element.eleme.cn/"%20\l%20"/zh-CN/component/installation)_

### Git

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

#### 初始化配置

#### 新建仓库

Repo-可以理解成目录，这个目录里所有的文件可以被git管理起来，每个文件的增删改操作都可以被Git跟踪到，以便任何时候都可以追踪历史或还原到之前的某一个版本

创建仓库的两种方式：

- Git init 在自己电脑本地直接创建一个仓库
- Git clone 从远程服务器上克隆一个已经存在的仓库

要使用Git对我们的代码进行版本控制，首先需要获得本地仓库

1）在电脑的任意位置创建一个空目录（例如test）作为我们的本地Git仓库

2）进入这个目录中，点击右键打开Git bash窗口

3）执行命令git init

4）如果创建成功后可在文件夹下看到隐藏的.git目录。

#### Git的工作区域和文件状态

##### 工作区域

- 工作区 Work Directory 电脑上的目录，资源管理器中能看到的文件夹就是工作区，实际操作的目录
- 暂存区 Staging Area/Index 临时存储区域，用于保存即将提交到git仓库的修改内容，版本控制的重要区域
- 本地仓库 Local repository Git存储代码和版本信息的主要位置

git -add 可以将修改的文件先添加到暂存区中

git -commit 一次性地将暂存区文件运送到本地仓库

##### 文件状态

- 未跟踪 Untracked
- 未修改 Unmodified
- 已修改 modified
- 已暂存 Staged

#### Git常用指令

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

#### Git分支

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

#### Git远程仓库

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

命令： git remote add &lt;远端名称&gt; &lt;仓库路径&gt;

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

命令: git clone &lt;仓库路径&gt; \[本地目录\] 指定一个名字

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

#### 在IDEA中使用Git

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

## JavaWeb综合案例

完成品牌数据的增删改查，批量删除，分页查询，条件查询

前端Vue Element + 后端MyBatis servlet

### 查询所有

Mapper-brandMapper.java

1.      @Select("select \* from tb_brand")
2.      @ResultMap（"brandResultMap"）
3.      List&lt;Brand&gt; selectAll();

由于Brand实体类中的名称与数据库表中字段不匹配，需要使用resultMap进行映射

resourses-com-itheima-mapper-brandMapper.xml

1.  &lt;mapper namespace="com.itheima.mapper.BrandMapper"&gt;
2.      &lt;resultMap id="brandResultMap" type="brand"&gt;
3.          &lt;result property="brandName" column="brand_name" /&gt;
4.          &lt;result property="companyName" column="company_name" /&gt;
5.      &lt;/resultMap&gt;
6.  &lt;/mapper&gt;

service-BrandMapper.java

创建一个接口，在接口中写方法

1.  List&lt;Brand&gt; selectAll();

service-impl-brandServiceImpl

1.  public class brandServiceImpl implements BrandService {
2.      _//1.创建sqlSessionFactory_
3.      SqlSessionFactory sqlSessionFactory = SqlSessionFactoryUtils.getSqlSessionFactory();
4.      @Override
5.      public List&lt;Brand&gt; selectAll() {

7.          _//2.获取SqlSession对象_
8.          SqlSession sqlSession = sqlSessionFactory.openSession();    

10.         _//3.获取BrandMapper_
11.         BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

13.         List&lt;Brand&gt; brands = mapper.selectAll();

15. _//5.释放资源_
16. sqlSession.close();
17.         return brands;

19.     }
20. }

通过接口-实现类，通过一些框架设计web层和service层可以解耦合

web-SelectAllServlet

1.  @WebServlet("/selectAllServlet")
2.  public class SelectAllServlet {

4.      private BrandService brandService = new brandServiceImpl();

7.      protected void doGet(HttpServletRequest request, HttpServletResponse response)
8.              throws ServletException, IOException {

10.         _//1. 调用service查询_
11.         List&lt;Brand&gt; brands = brandService.selectAll();

13.         _//2.转为json_
14.         String jsonString = JSON.toJSONString(brands);   

16.         _//3.写数据_
17.         response.setContentType("text/json;charset=utf-8");
18.         response.getWriter().write(jsonString);
19.     }

21.     protected void doPost(HttpServletRequest request, HttpServletResponse response)
22.             throws ServletException, IOException {
23. this.doGet(request, response);
24.     }
25. }

关于测试：Tomcat启程序，访问selectAllservlet，看到一系列的json数据则后台接收数据无误

\--后台代码#end

brand.html

1.      new Vue({
2.          el: "#app",

4.          mounted() {
5.              _//当页面加载完成后，发送异步请求_

7.              var \_this = this;

9.              axios({
10.                 method: "get",
11.                 url: "http://localhost:8080/brand-case/selectAllServlet"
12.             }).then(function(resp) {

14.                 \_this.tableData = resp.data;
15.             })

17.         },
18. }

当页面加载完成时候，发送异步请求来获取数据

通过then回调，获取响应，绑定function函数，resp.data就是列表数据，传到表格数据的模型上，this不能直接使用，声明提高级别

\--前端代码#end

### 新增品牌

Mapper-BrandMapper.java

1.      @Insert("insert into tb_brand values (null,#{brandName},#{companyName},#{ordered},#{description},#{status})")
2.      void add(Brand brand);

service-BrandMapper.java

1.  void add(Brand brand);

service-impl-BrandServiceImpl

1.      @Override
2.      public void add(Brand brand) {

4.          _//2.获取SqlSession对象_
5.          SqlSession sqlSession = sqlSessionFactory.openSession();

7.          _//3.获取BrandMapper_
8.          BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

10.         mapper.add(brand);

12.         _//4.提交事务_
13.         sqlSession.commit();

15.         _//5.释放资源_
16.         sqlSession.close();

18.     }

web-AddServlet

1.  @WebServlet("/addServlet")
2.  public class AddServlet {

4.      private BrandService brandService = new brandServiceImpl();

7.      protected void doGet(HttpServletRequest request, HttpServletResponse response)
8.              throws ServletException, IOException {

10.        _//1.接收品牌数据_
11.         BufferedReader br = request.getReader();
12.         String params = br.readLine();_//json字符串_

14.         _//2.转为brand对象_
15.         Brand brand = JSON.parseObject(params, Brand.class);

17.         _//3.调用service添加_
18.         brandService.add(brand);

20.         _//4.响应结果_
21.         response.getWriter().write("success");
22.     }

24.     protected void doPost(HttpServletRequest request, HttpServletResponse response)
25.             throws ServletException, IOException {
26. this.doGet(request, response);
27.     }
28. }

数据以json格式提交，使用request.getReader来获取消息体数据

\--后端代码#end

1.              &lt;el-form-item&gt;
2.                  &lt;el-button type="primary" @click="addBrand"&gt;提交&lt;/el-button&gt;
3.                  &lt;el-button @click="dialogVisible = false"&gt;取消&lt;/el-button&gt;
4.              &lt;/el-form-item&gt;

静态页面表单的案件绑定，将按钮绑定单击事件addBrand

brand.html

1.              addBrand(){
2.                  _//console.log(this.brand);_

4.                  var \_this = this;

6.                  _//发送ajax异步请求_
7.                  axios({
8.                     method: "post",
9.                     url: "http://localhost:8080/brand-case/addServlet",
10.                    data: \_this.brand

12.                 }).then(function (resp){

14.                     _//添加成功_
15.                     if(resp.data() == "success"){

17.                         _//关闭窗口_
18.                         \_this.dialogVisible = false;

20.                         _//重新查询数据_                        
21.                         \_this.selectAll();

23.                         \_this.$message({
24.                             message: '添加成功',
25.                             type: 'success'
26.                         });

28.                     }
29.                 })
30.             },
31.                 })
32.             },

为了方便调用selectAll来展示数据，直接将selectAll封装成一个方法

1.   mounted() {this.selectAll()；},

可以加入’添加成功’提示框功能

前端代码#end

#修改品牌

#删除品牌

### Servlet代码优化

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

10.         _//2.获取最后一段路径，方法名_
11.         int index = uri.lastIndexOf('/');_//获取最后一个/的位置_
12.         String methodName = uri.substring(index + 1);

14.         _//3.获取BrandServlet/UserServlet 字节码对象 class_
15.         _//谁调用我（this所在的方法），我（this）调用谁，这里的this指BrandServlet(baseServlet的子类们)，而不是Httpservlet_
16.         Class&lt;? extends BaseServlet&gt; cls = this.getClass();

18.         _//获取方法Method对象_
19.         try {
20.             Method method = cls.getMethod(methodName, HttpServletRequest.class, HttpServletResponse.class);
21.             _//执行方法_
22.             method.invoke(this,req,resp);

24.         }catch (NoSuchMethodException e){
25.             e.printStackTrace();
26.         } catch (InvocationTargetException e) {
27.             throw new RuntimeException(e);
28.         } catch (IllegalAccessException e) {
29.             throw new RuntimeException(e);
30.         }
31.     }
32. }

一个通用的 HttpServlet 替代类，用于根据 URL 路径动态调用子类中的方法。继承自 HttpServlet。然后重写父类 service() 方法，处理所有 HTTP 请求（GET、POST 等）。参数：req: 封装了客户端的请求信息。resp: 用于向客户端发送响应。再获取当前请求的 URI。当访问 /brand-case/brand/selectAll 时，得到字符串 /brand-case/brand/selectAll。找到最后一个斜杠 / 的位置，并提取其后的内容作为方法名。uri.substring(index + 1) 得到 "selectAll"。获取当前对象的实际运行时类的 Class 对象。如果当前是 BrandServlet 实例，则返回 BrandServlet.class。使用反射获取名为 methodName 的方法对象，要求该方法接受两个参数：HttpServletRequest 和 HttpServletResponse。使用反射调用该方法，并传入当前请求和响应对象。

对此前写的代码进行优化

1.  @WebServlet("/brand/\*")
2.  public class BrandServlet {

4.      private BrandService brandService = new brandServiceImpl();

6.      public void selectAll(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {}

8.      public void add(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{}
9.  }

### 批量删除

Mapper-BrandMapper.java

1.      void deleteByIds(@Param("ids")int\[\] ids);

@Param("ids") 表示将方法参数 int\[\] ids 命名为 "ids"，以便在对应的 SQL 语句中引用。

当这个方法被调用时，传入的 ids 数组可以通过名称 "ids" 在 MyBatis 的 XML 映射文件或注解中的 SQL 语句里使用。

Resources-com-itheima-brandMapper.xml

1.      &lt;delete id="delectByIds" &gt;
2.          delete from tb_brand where in
3.          &lt;foreach item="id" collection="ids" separator="," open="(" close=")"&gt;
4.              _#{id}_
5.          &lt;/foreach&gt;
6.      &lt;/delete&gt;

Sql语句复杂使用配置文件编写sql语句

service-BrandService.java

1.      void deleteByIds(int\[\] ids);

在接口中创建方法，接下来在实现类中实现该方法

service-BrandServiceImpl.java

1.      @Override
2.      public void deleteByIds(int\[\] ids) {

4.          _//2.获取SqlSession对象_
5.          SqlSession sqlSession = sqlSessionFactory.openSession();

7.          _//3.获取BrandMapper_
8.          BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

10.         mapper.deleteByIds(ids);

12.         _//4.提交事务_
13.         sqlSession.commit();

15.         _//5.释放资源_
16.         sqlSession.close();

18.     }

在实现类中调用方法

web-BrandServlet

1.      public void deleteByIds(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{

3.          _//1.接收id数组\[1,2,3\]_
4.          BufferedReader br = request.getReader();
5.          String params = br.readLine();_//json字符串_

7.          _//2.转为int数组_
8.          int\[\] ids = JSON.parseObject(params, int\[\].class);

10.         _//3.调用service添加_
11.         brandService.deleteByIds(ids);

13.         _//4.响应结果_
14.         response.getWriter().write("success");
15.     }

\--后端代码#end

brand.html

1.  &lt;el-button type="danger" plain @click="deleteByIds"&gt;批量删除&lt;/el-button&gt;

静态页面，按键绑定deleteByIds事件，实现批量删除

1.              deleteByIds(){
2.                  _//1.创建id数组\[1,2,3\]_
3.                  for (let i = 0; i < this.multipleSelection.length; i++) {
4.                      let selectionElements = this.multipleSelection\[i\];
5.                      this.selectedIds\[i\] = selectionElements.id;
6.                  }

8.                  _//2.发送ajax异步请求_
9.                  axiosaxios({
10.                     method: "post",
11.                     url: "http://localhost:8080/brand-case/deleteByIds",
12.                     data: \_this.deleteByIds

14.                 }).then(function (resp){

16.                     _//删除成功_
17.                     if(resp.data() == "success"){

19.                         _//重新查询数据_
20.                         \_this.selectAll();

22.                         \_this.$message({
23.                             message: '添加成功',
24.                             type: 'success'
25.                         });
26.                     }
27.                 })
28.             }

创建方法deleteByIds，从multipleSelection中获取数据，并通过遍历，将数据存储到自建的selectedIds模型中

在data中新建一个selectedIds模型 id被选中，数组值发生变化，提交数据时提交数组到后台

1.                  //被选中的id数组
2.                  selectedIds:\[\],

优化：在删除时跳出确认框，确认是否删除

1.              _//批量删除_
2.              deleteByIds(){
3.                  _// 弹出确认提示框_

5.                  this.$confirm('此操作将删除该数据, 是否继续?', '提示', {
6.                      confirmButtonText: '确定',
7.                      cancelButtonText: '取消',
8.                      type: 'warning'
9.                  }).then(() => {
10.                     _//用户点击确认按钮_

12.                     _//1. 创建id数组 \[1,2,3\], 从 this.multipleSelection 获取即可_
13.                     for (let i = 0; i < this.multipleSelection.length; i++) {
14.                         let selectionElement = this.multipleSelection\[i\];
15.                         this.selectedIds\[i\] = selectionElement.id;

17.                     }

19.                     _//2. 发送AJAX请求_
20.                     var \_this = this;

22.                     _// 发送ajax请求，添加数据_
23.                     axios({
24.                         method:"post",
25.                         url:"http://localhost:8080/brand-case/brand/deleteByIds",
26.                         data:\_this.selectedIds
27.                     }).then(function (resp) {
28.                         if(resp.data == "success"){
29.                             _//删除成功_

31.                             _// 重新查询数据_
32.                             \_this.selectAll();
33.                             _// 弹出消息提示_
34.                             \_this.$message({
35.                                 message: '恭喜你，删除成功',
36.                                 type: 'success'
37.                             });

39.                         }
40.                     })
41.                 }).catch(() => {
42.                     _//用户点击取消按钮_

44.                     this.$message({
45.                         type: 'info',
46.                         message: '已取消删除'
47.                     });
48.                 });

51.             }

用then catch包裹两种条件

\--前端代码#end

### 分页查询

- 分页查询LIMIT，参数1：开始索引，参数2：查询的条目数

SELECT \* FROM tb_brand LIMIT 0,5

- 页面（前端）传递的参数- 当前页码currentPage 与 每页查询的条目数pageSize
- 后台返回的数据- 当前页数据 List 与 总记录数 totalCount
- 开始索引 = （当前页数-1）\* 每页显示条数
- 查询条目数 = 查询的条目数 = 每页显示条数

Pojo-PageBean

1.  _//分页查询的JavaBean_
2.  public class PageBean&lt;T&gt; {
3.      _// 总记录数_
4.      private int totalCount;
5.      _// 当前页数据_
6.      private List&lt;T&gt; rows;

9.      public int getTotalCount() {
10.         return totalCount;
11.     }

13.     public void setTotalCount(int totalCount) {
14.         this.totalCount = totalCount;
15.     }

17.     public List&lt;T&gt; getRows() {
18.         return rows;
19.     }

21.     public void setRows(List&lt;T&gt; rows) {
22.         this.rows = rows;
23.     }
24. }

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
9.      List&lt;Brand&gt; selectByPage(@Param("begin") int begin,@Param("size") int size);

11.     _/\*\*_
12.      \* 查询总记录数
13.      \* @return
14.      \*/
15.     @Select("select count(\*) from tb_brand ")
16. @ResultMap("brandResultMap")
17.     int selectTotalCount();

BrandService.java

1.      _/\*\*_
2.       \* 分页查询
3.       \* @param currentPage  当前页码
4.       \* @param pageSize   每页展示条数
5.       \* @return
6.       \*/
7.      PageBean&lt;Brand&gt;  selectByPage(int currentPage,int pageSize);

返回一个Pagebean对象，由前端传入currentPage和pageSize

Service-impl-brandServiceImpl.java

1.  @Override
2.      public PageBean&lt;Brand&gt; selectByPage(int currentPage, int pageSize) {
3.          _//2. 获取SqlSession对象_
4.          SqlSession sqlSession = factory.openSession();
5.          _//3. 获取BrandMapper_
6.          BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

9.          _//4. 计算开始索引_
10.         int begin = (currentPage - 1) \* pageSize;
11.         _// 计算查询条目数_
12.         int size = pageSize;

14.         _//5. 查询当前页数据_
15.         List&lt;Brand&gt; rows = mapper.selectByPage(begin, size);

17.         _//6. 查询总记录数_
18.         int totalCount = mapper.selectTotalCount();

20.         _//7. 封装PageBean对象_
21.         PageBean&lt;Brand&gt; pageBean = new PageBean<>();
22.         pageBean.setRows(rows);
23.         pageBean.setTotalCount(totalCount);

25.         _//8. 释放资源_
26.         sqlSession.close();

28.         return pageBean;
29.     }

BrandServlet.java

1.  public void selectByPage(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
2.          _//1. 接收 当前页码 和 每页展示数    url?currentPage=1&pageSize=5_
3.          String \_currentPage = request.getParameter("currentPage");
4.          String \_pageSize = request.getParameter("pageSize");

6.          int currentPage = Integer.parseInt(\_currentPage);
7.          int pageSize = Integer.parseInt(\_pageSize);

9.          _//2. 调用service查询_
10.         PageBean&lt;Brand&gt; pageBean = brandService.selectByPage(currentPage, pageSize);

12.         _//2. 转为JSON_
13.         String jsonString = JSON.toJSONString(pageBean);
14.         _//3. 写数据_
15.         response.setContentType("text/json;charset=utf-8");
16.         response.getWriter().write(jsonString);
17.     }

请求中接收的类型是String类型，而查询中需要的为int类型，所以需要强制转换

后端代码#end

brand.html

1.              selectAll(){

4.                  var \_this = this;

6.                  axios( {
7.                      method: "post",
8.                      url: "http://localhost:8080/brand-case/brand/selectByPage?currentPage=" + \_this.currentPage + "&pageSize="+ \_this.pageSize,

10.                 }).then(function(resp){
11.                     \_this.tableData = resp.data.rows;
12.                     \_this.totalCount = resp.data.totalCount;
13.                     console.log(resp.data);
14.                 })

16.             },

因为修改分页查询，相当于修改了selectAll的显示方式，此前是加载完成之后就执行selectAll，这里url直接使用拼字符串的方式，将tableData模型数据设置成rows即当前页的数据，totalCount为页的数量，也建立到一个模型中。通过响应到的数据来为这两个模型设置值

在data中设置模型：pageSize，totalCount和currentPage其中5，100为默认值

1.                  _//每页显示的条数_
2.                  pageSize:5,
3.                  _//总记录数_
4.                  totalCount:100,
5.                  _// 当前页码_
6.                  currentPage: 1,

分页工具条

1.      &lt;!--分页工具条--&gt;
2.      <el-pagination
3.              @size-change="handleSizeChange"
4.              @current-change="handleCurrentChange"
5.              :current-page="currentPage"
6.              :page-sizes="\[5, 10, 15, 20\]"
7.              :page-size="5"
8.              layout="total, sizes, prev, pager, next, jumper"
9.              :total="totalCount">
10.     &lt;/el-pagination&gt;

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

11.                 _//重新设置当前页码_
12.                 this.currentPage = val;
13.                 this.selectAll();
14.             },

Val用来接收分页工具栏停留的位置，以及需要显示的数量

前端代码#end

### 条件查询

需要完成条件查询，并且按照分页的形式展示

BrandMapper.java

1.      _/\*\*_
2.       \* 分页条件查询
3.       \* @param begin
4.       \* @param size
5.       \* @return
6.       \*/
7.      List&lt;Brand&gt; selectByPageAndCondition(@Param("begin") int begin, @Param("size") int size, @Param("brand") Brand brand);

9.      _/\*\*_
10.      \* 根据条件查询总记录数
11.      \* @return
12.      \*/

14.     Integer selectTotalCountByCondition(Brand brand);

使用Integer即使查询结果为空，MyBatis 也能安全地返回 null，而不会引发类型不匹配异常

BrandMapper.xml

1.      &lt;select id="selectByPageAndCondition" resultMap="brandResultMap"&gt;
2.          select \*
3.          from tb_brand
4.          &lt;where&gt;
5.          &lt;if test=" brandName != null and  brandName ！=''"&gt;
6.              and brand_name like _#{ brandName}_
7.          &lt;/if&gt;

9.          &lt;if test=" companyName != null and  companyName ！=''"&gt;
10.             and company_name like _#{ companyName}_
11.         &lt;/if&gt;

13.         &lt;if test=" status != null "&gt;
14.             and status = _#{ status}_
15.         &lt;/if&gt;

17.         &lt;/where&gt;

19.         limit _#{begin},#{size}_
20.     &lt;/select&gt;

22.     &lt;select id="selectTotalCountByCondition" resultMap="brandResultMap"&gt;
23.         select count(\*)
24.         from tb_brand
25.         &lt;where&gt;
26.             &lt;if test=" brandName != null and  brandName ！=''"&gt;
27.                 and brand_name like _#{ brandName}_
28.             &lt;/if&gt;

30.             &lt;if test=" companyName != null and  companyName ！=''"&gt;
31.                 and company_name like _#{ companyName}_
32.             &lt;/if&gt;

34.             &lt;if test=" status != null "&gt;
35.                 and status = _#{ status}_
36.             &lt;/if&gt;

38.         &lt;/where&gt;

40.     &lt;/select&gt;

由于需要写动态SQL，所以在XML文件中编辑，第二个select语句中，由于没有采用@brand注解，可以直接使用brand实体类中的属性，所以可以省略brand. ，同时希望模糊匹配没使用like，而不是=

BrandService.java

1.  PageBean&lt;Brand&gt; selectByPageAndCondition(int currentPage, int pageSize, Brand brand);

分页条件查询，返回一个pageBean

BrandServiceImpl.java

1.      @Override
2.      public PageBean&lt;Brand&gt; selectByPageAndCondition(int currentPage, int pageSize, Brand brand) {

4.          _//2.获取SqlSession对象_
5.          SqlSession sqlSession = factory.openSession();

7.          _//3.获取BrandMapper_
8.          BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

10.         _//计算开始索引_
11.         int begin = (currentPage-1) \* pageSize;
12.         _//计算查询条目数_
13.         int size = pageSize;

15.         _//处理brand条件，模糊表达式_
16.         String brandName = brand.getBrandName();
17.         if(brandName != null && brandName.length() > 0){
18.             brand.setBrandName("%" + brandName + "%");
19.         }

21.         String companyName = brand.getCompanyName();
22.         if(companyName != null && companyName.length() > 0){
23.             brand.setCompanyName("%" + companyName + "%");
24.         }

26.         _//4.查询当前页数据_
27.         List&lt;Brand&gt; rows = mapper.selectByPageAndCondition(begin, size,brand);

29.         _//5.查询总记录数_
30.         int totalCount = mapper.selectTotalCountByCondition(brand);

33.         PageBean&lt;Brand&gt; pageBean = new PageBean<>();
34.         pageBean.setRows(rows);
35.         pageBean.setTotalCount(totalCount);

37.         sqlSession.close();

39.         return pageBean;
40.     }

新增处理brand对象，使模糊表达式，对用户的输入封装成模糊表达式的形式

BrandServlet.java

1.      public void selectByPageAndCondition(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
2.          _//1. 接收两个参数 currentPage pageSize_
3.          String \_currentPage = request.getParameter("currentPage");
4.          String \_pageSize = request.getParameter("pageSize");

6.          _//获取查询条件对象_
7.          BufferedReader br = request.getReader();
8.          String params = br.readLine();_//json字符串_

10.         Brand brand = JSON.parseObject(params, Brand.class);

12.         int currentPage = Integer.parseInt(\_currentPage);
13.         int pageSize = Integer.parseInt(\_pageSize);

16.         PageBean&lt;Brand&gt; pageBean = brandService.selectByPageAndCondition(currentPage, pageSize,brand);

18.         _//转为json_
19.         String json = JSON.toJSONString(pageBean);
20.         response.setContentType("text/json;charset=utf-8");
21.         response.getWriter().write(json);
22.     }

Brand的数据通过前端传递，将method改为post方式，使用data来传递，接收请求体的参数，currentPage和pageSize使用url来传递

后端代码#end

Brand.html

1.              _//查询所有_
2.              selectAll(){

4.                  var \_this = this;

6.                  axios( {
7.                      method: "post",
8.                      url: "http://localhost:8080/brand-case/brand/selectByPageAndCondition?currentPage=" + \_this.currentPage + "&pageSize="+ \_this.pageSize,
9.                      data:this.brand

11.                 }).then(function(resp){
12.                     \_this.tableData = resp.data.rows;
13.                     \_this.totalCount = resp.data.totalCount;
14.                     console.log(resp.data);
15.                 })

17.             },
18.             onSubmit() {
19.                 console.log(this.brand);
20.                 this.selectAll()
21.             },

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

## SSM

Spring +SpringMVC +Mybatis

Dao=Mapper

domain=pojo

git clone git@github.com:CrRdz/Learning_SSM.git

### Spring

- Spring技术是JavaEE开发的必备技术，企业开发技术选型命中率>90%
- 简化开发，框架整合（MyBatis/Struts/Hibernate）
- Spring发展到今天已经形成一种开发生态圈，Spring提供若干个项目，每个项目用于完成特定的功能

#### Spring Framework

Spring Framework是Spring生态中最基础的项目，是其他项目的根基

##### 系统架构

架构上层依赖于下层

底层：

Core Container 核心容器（beans Core Context SpEL）

中层：

AOP（面向切面编程）Aspects（AOP思想实现）

上层：

Data Access/Integration数据访问/集成（JDBC ORM OXM JMS Transaction事务）

Web Web开发（WebSocket Servlet Web Portlet）

##### 核心概念

- 代码书写现状：耦合度偏高

|

解决方案：使用对象时，在程序中不要主动使用new产生新对象，转换为由外部提供对象

数据层实现

1.  public class BookDaoImpl implements BookDao {
2.      public void save() {
3.          System.out.println("book dao save ...");
4.      }
5.  }

1.  public class BookDaoImpl2 implements BookDao {
2.      public void save() {
3.          System.out.println("book dao save ...2");
4.      }
5.  }

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

##### 核心容器

###### IoC快速入门

- 管理Service与Dao
- 通过配置文件的方式将被管理的对象告知IoC容器
- 被管理的对象交给IoC通过接口获取到IoC容器
- IoC容器得到后，通过接口方法中获取bean

准备：

定义spring管理的类

导包spring-context 导入坐标

pom.xml

1.      &lt;dependency&gt;
2.        &lt;groupId&gt;org.springframework&lt;/groupId&gt;
3.        &lt;artifactId&gt;spring-context&lt;/artifactId&gt;
4.        &lt;version&gt;5.2.10.RELEASE&lt;/version&gt;
5.      &lt;/dependency&gt;

创建配置文件将被管理的对象告知IoC容器

resouse中创建spring.config配置文件xml 配置对应类作为Spring管理的bean

ApplicationContext.xml

1.      _&lt;!--1.导入spring的坐标spring-context，对应版本是5.2.10.RELEASE--&gt;_

3.      _&lt;!--2.配置bean--&gt;_
4.      _<!--bean标签标示配置bean_
5.      id属性标示给bean起名字
6.      class属性表示给bean定义类型-->
7.      &lt;bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"/&gt;

9.      &lt;bean id="bookService" class="com.itheima.service.impl.BookServiceImpl"/&gt;

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

9.          BookService bookService = (BookService) ctx.getBean("bookService");
10.         bookService.save();

12.     }
13. }

###### DI快速入门

- 基于IoC管理bean
- Service中使用new形式创建的Dao对象不保留
- Service中需要的Dao对象通过提供方法进入到Service中
- Service与Dao之间的关系用配置文件描述

BookServiceImpl.java

1.  public class BookServiceImpl implements BookService {
2.      _//5.删除业务层中使用new的方式创建的dao对象_
3.      private BookDao bookDao;

5.      public void save() {
6.          System.out.println("book service save ...");
7.          bookDao.save();
8.      }
9.      _//6.提供对应的set方法_
10.     public void setBookDao(BookDao bookDao) {
11.         this.bookDao = bookDao;
12.     }
13. }

applicationContext

1.      &lt;bean id="bookService" class="com.itheima.service.impl.BookServiceImpl"&gt;
2.          _&lt;!--7.配置server与dao的关系--&gt;_
3.          _<!--property标签表示配置当前bean的属性_
4.          name属性表示配置哪一个具体的属性
5.          ref属性表示参照哪一个bean-->
6.          &lt;property name="bookDao" ref="bookDao"/&gt;
7.      &lt;/bean&gt;

Ref-reference

Dao告知service关系 对service修改

Service中有个属性是bookDao 对应需要参照的对象bookDao（id）两个bookDao并不是一个

###### Bean-IoC

1.  Bean配置

- Bean基础配置
- Bean别名配置
- Bean作用范围配置

基础配置:

功能：定义Spring核心容器管理的对象

格式

1.  &lt;beans&gt;
2.      &lt;bean/&gt;
3.      &lt;bean&gt;&lt;/bean&gt;
4.  &lt;/beans&gt;

属性列表:

Id：bean的id，使用容器可以通过id值获取对应的bean，在一个容器中id值唯一

Class：bean的类型，即配置的bean的全路径名

别名配置

1.      _&lt;!--name:为bean指定别名，别名可以有多个，使用逗号，分号，空格进行分隔--&gt;_
2.      &lt;bean id="bookService" name="service service4 bookEbi" class="com.itheima.service.impl.BookServiceImpl"&gt;
3.          &lt;property name="bookDao" ref="bookDao"/&gt;
4.      &lt;/bean&gt;

使用name属性配置 但还是建议使用id引用

Bean作用范围

1.      _&lt;!--scope：为bean设置作用范围，可选值为单例singloton，非单例prototype--&gt;_
2.      &lt;bean id="bookDao" name="dao" class="com.itheima.dao.impl.BookDaoImpl" scope="prototype"/&gt;

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

3.      public BookDaoImpl() {
4.          System.out.println("book dao constructor is running ....");
5.      }

7.      public void save() {
8.          System.out.println("book dao save ...");
9.      }
10. }

无参构造方法如果不存在，将抛出BeanCreationException

配置

1.  _&lt;!--方式一：构造方法实例化bean--&gt;_
2.  &lt;bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"/&gt;

1.  通过静态工厂

现在不常用，一般为兼容早期遗留系统

AppForInstanceOrder.java

1.  public class AppForInstanceOrder {
2.      public static void main(String\[\] args) {
3.          _//通过静态工厂创建对象_

5.          ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");

7.          OrderDao orderDao = (OrderDao) ctx.getBean("orderDao");

9.          orderDao.save();

11.     }
12. }

OrderDaoFactory.java

1.  public class OrderDaoFactory {
2.      public static OrderDao getOrderDao(){
3.          System.out.println("factory setup....");
4.          return new OrderDaoImpl();
5.      }
6.  }

配置

1.      _&lt;!--方式二：使用静态工厂实例化bean--&gt;_
2.  &lt;bean id="orderDao" class="com.itheima.factory.OrderDaoFactory" factory-method="getOrderDao"/&gt;

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

1.      _&lt;!--方式三：使用实例工厂实例化bean--&gt;_
2.  &lt;bean id="userFactory" class="com.itheima.factory.UserDaoFactory"/&gt;
3.  &lt;bean id="userDao" factory-method="getUserDao" factory-bean="userFactory"/&gt;

需要先造出工厂对象 工厂中的路径是getUserDao方法 工厂对象对应的bean使用工厂id

1.  使用factoryBean（方式C的变种）
2.  public class UserDaoFactoryBean implements FactoryBean&lt;UserDao&gt; {
3.      _//代替原始实例工厂中创建对象的方法_
4.      public UserDao getObject() throws Exception {
5.          return new UserDaoImpl();
6.      }

8.      public Class&lt;?&gt; getObjectType() {
9.          return UserDao.class;
10.     }
11. }

需要实现FactoryBean 泛型中写需要实例化的对象

配置

1.     _&lt;!--方式四：使用FactoryBean实例化bean--&gt;_
2.     &lt;bean id="userDao" class="com.itheima.factory.UserDaoFactoryBean"/&gt;

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

14. }

配置

1.      _&lt;!--init-method：设置bean初始化生命周期回调函数--&gt;_
2.      _&lt;!--destroy-method：设置bean销毁生命周期回调函数，仅适用于单例对象--&gt;_
3.      &lt;bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl" init-method="init" destroy-method="destory"/&gt;

1.  public class AppForLifeCycle {
2.      public static void main( String\[\] args ) {
3.          ClassPathXmlApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");

5.          BookDao bookDao = (BookDao) ctx.getBean("bookDao");
6.          bookDao.save();
7.          _//注册关闭钩子函数，在虚拟机退出之前回调此函数，关闭容器_
8.          _//ctx.registerShutdownHook();_
9.          _//关闭容器_
10.         ctx.close();
11.     }
12. }

registerShutdownHook在虚拟机退出之前回调此函数关闭容器

Close相对更暴力

但实际开发中，关闭容器应伴随Tomcat

使用接口控制生命周期

1.  public class BookServiceImpl implements BookService, InitializingBean, DisposableBean {
2.      private BookDao bookDao;

4.      public void setBookDao(BookDao bookDao) {
5.          System.out.println("set .....");
6.          this.bookDao = bookDao;
7.      }

9.      public void save() {
10.         System.out.println("book service save ...");
11.         bookDao.save();
12.     }

14.     public void destroy() throws Exception {
15.         System.out.println("service destroy");
16.     }

18.     public void afterPropertiesSet() throws Exception {
19.         System.out.println("service init");
20.     }
21. }

这样可以省略配置文件中的init-method...

Bean销毁时机

容器关闭前触发bean的销毁

关闭容器方法：手工关闭容器/注册关闭钩子，在虚拟机退出前关闭容器再退出虚拟机

###### 依赖注入方式-DI

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

13.     public void save() {
14.         System.out.println("book service save ...");
15.         bookDao.save();
16.         userDao.save();
17.     }
18. }

applicationContext

1.      _&lt;!--注入引用类型--&gt;_
2.      &lt;bean id="bookService" class="com.itheima.service.impl.BookServiceImpl"&gt;
3.          _&lt;!--property标签：设置注入属性--&gt;_
4.          _&lt;!--name属性：设置注入的属性名，实际是set方法对应的名称--&gt;_
5.          _&lt;!--ref属性：设置注入引用类型bean的id或name--&gt;_
6.          &lt;property name="bookDao" ref="bookDao"/&gt;
7.          &lt;property name="userDao" ref="userDao"/&gt;
8.      &lt;/bean&gt;

- 简单类型

BookDaoImpl.java

1.  public class BookDaoImpl implements BookDao {

3.      private String databaseName;
4.      private int connectionNum;
5.      _//setter注入需要提供要注入对象的set方法_
6.      public void setConnectionNum(int connectionNum) {
7.          this.connectionNum = connectionNum;
8.      }
9.      _//setter注入需要提供要注入对象的set方法_
10.     public void setDatabaseName(String databaseName) {
11.         this.databaseName = databaseName;
12.     }
13.     public void save() {
14.         System.out.println("book dao save ..."+databaseName+","+connectionNum);
15.     }
16. }

applicationContext

1.      _&lt;!--注入简单类型--&gt;_
2.      &lt;bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"&gt;
3.          _&lt;!--property标签：设置注入属性--&gt;_
4.          _&lt;!--name属性：设置注入的属性名，实际是set方法对应的名称--&gt;_
5.          _&lt;!--value属性：设置注入简单类型数据值--&gt;_
6.          &lt;property name="connectionNum" value="100"/&gt;
7.          &lt;property name="databaseName" value="mysql"/&gt;
8.      &lt;/bean&gt;

提供可访问的set方法

配置中使用property标签value属性注入简单类型数据

1.  构造器注入

- 引用类型

BookServiceImpl.java

1.  public class BookServiceImpl implements BookService{
2.      private BookDao bookDao;
3.      private UserDao userDao;

5.      public BookServiceImpl(BookDao bookDao, UserDao userDao) {
6.          this.bookDao = bookDao;
7.          this.userDao = userDao;
8.      }

10.     public void save() {
11.         System.out.println("book service save ...");
12.         bookDao.save();
13.         userDao.save();
14.     }
15. }

ApplicationContext

1.      &lt;bean id="bookService" class="com.itheima.service.impl.BookServiceImpl"&gt;
2.          &lt;constructor-arg name="userDao" ref="userDao"/&gt;
3.          &lt;constructor-arg name="bookDao" ref="bookDao"/&gt;
4.      &lt;/bean&gt;

- 简单类型

1.  public class BookDaoImpl implements BookDao {
2.      private String databaseName;
3.      private int connectionNum;

5.      public BookDaoImpl(String databaseName, int connectionNum) {
6.          this.databaseName = databaseName;
7.          this.connectionNum = connectionNum;
8.      }

10.     public void save() {
11.         System.out.println("book dao save ..."+databaseName+","+connectionNum);
12.     }
13. }

applicationContext

1.      &lt;bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"&gt;
2.          &lt;constructor-arg name="connectionNum" value="10"/&gt;
3.          &lt;constructor-arg name="databaseName" value="mysql"/&gt;
4.      &lt;/bean&gt;

1.  问题

耦合度高 applicationContext与BookDaoImpl耦合度高 如果形参名称更改，applicaton中constructor-arg中的name属性也要同步修改

1.  _&lt;!--解决形参名称的问题，与形参名不耦合 根据构造方法类型注入--&gt;_
2.  &lt;bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"&gt;
3.          &lt;constructor-arg type="int" value="10"/&gt;
4.          &lt;constructor-arg type="java.lang.String" value="mysql"/&gt;
5.  &lt;/bean&gt;

1.  _&lt;!--解决参数类型重复问题，使用位置解决参数匹配--&gt;_
2.      &lt;bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"&gt;
3.          _&lt;!--根据构造方法参数位置注入--&gt;_
4.          &lt;constructor-arg index="0" value="mysql"/&gt;
5.          &lt;constructor-arg index="1" value="100"/&gt;
6.      &lt;/bean&gt;

1.  依赖注入方式选择

- 强制依赖使用构造器，使用setter注入有概率不进行注入导致null对象出现
- 可选依赖使用setter注入进行，灵活性强
- Spring框架倡导使用构造器，第三方内部大多数采用构造器注入的形式进行数据初始化，相对严谨
- 如果有必要可以两者同时使用，使用构造器注入完成强制依赖注入，使用setter注入完成可选依赖注入
- 实际开发中还需要根据实际情况分析，如果受控对象没有提供setter方法就必须使用构造器注入
- 自己开发的模块推荐使用setter注入

###### 依赖自动装配

IoC容器根据bean所依赖的资源在容器中自动查找并注入bean中的过程称为自动装配

自动装配方式：按类型/按名称/按构造方法/不启用自动装配

1.  &lt;bean id="bookDao" class="com.itheima.service.impl.BookDaoImpl" /&gt;
2.  _&lt;!--autowire属性：开启自动装配，通常使用按类型装配--&gt;_
3.  &lt;bean id="bookService" class="com.itheima.service.impl.BookServiceImpl" autowire="byType"/&gt;

按类型装配时，bean对象需唯一 连id都可以省略

如果有两个实现类-按名称装配，但是耦合度高

- 依赖自动装配特征

1.  自动装配用于引用类型依赖注入，不能对简单类型进行操作
2.  使用按类型装配时必须保障容器中相同类型的bean唯一推荐使用
3.  使用按名称装配时必须保障容器中具有指定名称的bean，变量名与配置名耦合高
4.  自动装配优先级低于setter注入与构造器注入，同时出现时自动装配配置失效

###### 集合注入

数组/List/Set/Map/Properties

1.  public class BookDaoImpl implements BookDao {

3.      private int\[\] array;
4.      private List&lt;String&gt; list;
5.      private Set&lt;String&gt; set;
6.      private Map&lt;String,String&gt; map;
7.      private Properties properties;

9.      public void setArray(int\[\] array) {
10.         this.array = array;
11.     }
12.     public void setList(List&lt;String&gt; list) {
13.         this.list = list;
14.     }
15.     public void setSet(Set&lt;String&gt; set) {
16.         this.set = set;
17.     }
18.     public void setMap(Map&lt;String, String&gt; map) {
19.         this.map = map;
20.     }
21.     public void setProperties(Properties properties) {
22.         this.properties = properties;
23.     }
24.     public void save() {
25.         System.out.println("book dao save ...");
26.         System.out.println("遍历数组:" + Arrays.toString(array));
27.         System.out.println("遍历List" + list);
28.         System.out.println("遍历Set" + set);
29.         System.out.println("遍历Map" + map);
30.         System.out.println("遍历Properties" + properties);
31.     }
32. }

配置

1.  &lt;bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"&gt;
2.          _&lt;!--数组注入--&gt;_
3.          &lt;property name="array"&gt;
4.              &lt;array&gt;
5.                  &lt;value&gt;100&lt;/value&gt;
6.                  &lt;value&gt;200&lt;/value&gt;
7.                  &lt;value&gt;300&lt;/value&gt;
8.              &lt;/array&gt;
9.          &lt;/property&gt;
10.         _&lt;!--list集合注入--&gt;_
11.         &lt;property name="list"&gt;
12.             &lt;list&gt;
13.                 &lt;value&gt;itcast&lt;/value&gt;
14.                 &lt;value&gt;itheima&lt;/value&gt;
15.                 &lt;value&gt;boxuegu&lt;/value&gt;
16.                 &lt;value&gt;chuanzhihui&lt;/value&gt;
17.             &lt;/list&gt;
18.         &lt;/property&gt;
19.         _&lt;!--set集合注入--&gt;_
20.         &lt;property name="set"&gt;
21.             &lt;set&gt;
22.                 &lt;value&gt;itcast&lt;/value&gt;
23.                 &lt;value&gt;itheima&lt;/value&gt;
24.                 &lt;value&gt;boxuegu&lt;/value&gt;
25.                 &lt;value&gt;boxuegu&lt;/value&gt;
26.             &lt;/set&gt;
27.         &lt;/property&gt;
28.         _&lt;!--map集合注入--&gt;_
29.         &lt;property name="map"&gt;
30.             &lt;map&gt;
31.                 &lt;entry key="country" value="china"/&gt;
32.                 &lt;entry key="province" value="henan"/&gt;
33.                 &lt;entry key="city" value="kaifeng"/&gt;
34.             &lt;/map&gt;
35.         &lt;/property&gt;
36.         _&lt;!--Properties注入--&gt;_
37.         &lt;property name="properties"&gt;
38.             &lt;props&gt;
39.                 &lt;prop key="country"&gt;china&lt;/prop&gt;
40.                 &lt;prop key="province"&gt;henan&lt;/prop&gt;
41.                 &lt;prop key="city"&gt;kaifeng&lt;/prop&gt;
42.             &lt;/props&gt;
43.         &lt;/property&gt;
44.     &lt;/bean&gt;

注：

Set如果重复会自动过滤

Array与list能混用

&lt;ref bean = “beanId’’&gt; 如果使用引用类型

###### 案例：数据源对象管理

导入坐标

配置数据源对象作为spring管理的bean

管理第三方数据连接池

1.  _&lt;!--    管理DruidDataSource对象--&gt;_
2.     &lt;bean id ="dataSouce" class="com.alibaba.druid.pool.DruidDataSource"&gt;
3.          &lt;property name="driverClassName" value="com.mysql.jdbc.Driver"/&gt;
4.          &lt;property name="url" value="jdbc:mysql://localhost:3306/spring_db"/&gt;
5.          &lt;property name="username" value="root"/&gt;
6.          &lt;property name="password" value="root"/&gt;
7.     &lt;/bean&gt;

管理c3p0

1.      &lt;bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource"&gt;
2.          &lt;property name="driverClass" value="com.mysql.jdbc.Driver"/&gt;
3.          &lt;property name="jdbcUrl" value="jdbc:mysql://localhost:3306/spring_db"/&gt;
4.          &lt;property name="user" value="root"/&gt;
5.          &lt;property name="password" value="root"/&gt;
6.          &lt;property name="maxPoolSize" value="1000"/&gt;
7.      &lt;/bean&gt;

使用setter注入

###### 加载properties文件

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
13. &lt;context:property-placeholder location="jdbc.properties"&gt;
14.     &lt;bean class="com.alibaba.druid.pool.DruidDataSource"&gt;
15.         &lt;property name="driverClassName" value="${jdbc.driver}"/&gt;
16.         &lt;property name="url" value="${jdbc.url}"/&gt;
17.         &lt;property name="username" value="${jdbc.username}"/&gt;
18.         &lt;property name="password" value="${jdbc.password}"/&gt;
19.     &lt;/bean&gt;

不加载系统变量system-properties-mode="NEVER"

加载多个properties使用通配符

Classpath\*表示不仅可以从当前目录读取也可以读取框架中jar包，设置加载当前工程类路径和当前工程所依赖的所有jar包中的所有properties文件

1.  &lt;context:property-placeholder location="classpath\*:\*.properties" system-properties-mode="NEVER"/&gt;

###### 容器补充

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

1.  &lt;bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl" lazy-init="true"/&gt;

在配置文件中加入这一行，也可以使application延迟加载

###### 核心容器总结

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

##### 注解开发

###### 注解开发定义bean

使用@Component定义bean

1.  _//@Component定义bean_
2.  @Component("bookDao")
3.  public class BookDaoImpl implements BookDao {
4.      public void save() {
5.          System.out.println("book dao save ...");
6.      }
7.  }

1.  _//@Component定义bean_
2.  @Component
3.  public class BookServiceImpl implements BookService {
4.      private BookDao bookDao;

6.      public void setBookDao(BookDao bookDao) {
7.          this.bookDao = bookDao;
8.      }

10.     public void save() {
11.         System.out.println("book service save ...");
12.         bookDao.save();
13.     }
14. }

Component可以指定名称理解成id

核心配置文件中通过组件扫描加载bean

1.  &lt;context:component-scan base-package="com.itheima"/&gt;

Spring提供@Component注解的三个衍生注解，功能完全一致，方便理解

业务层@Service

数据层@Repository

表现层@Controller

###### 纯注解开发

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

###### Bean管理

1.  bean作用范围
2.  @Repository
3.  _//@Scope设置bean的作用范围_
4.  @Scope("singleton")
5.  public class BookDaoImpl implements BookDao {

7.      public void save() {
8.          System.out.println("book dao save ...");
9.      }
10. }

1.  Bean生命周期
2.      _//@PostConstruct设置bean的初始化方法_
3.      @PostConstruct
4.      public void init() {
5.          System.out.println("init ...");
6.      }
7.      _//@PreDestroy设置bean的销毁方法_
8.      @PreDestroy
9.      public void destroy() {
10.         System.out.println("destroy ...");
11.     }

###### 依赖注入

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

7.      public void save() {
8.          System.out.println("book dao save ..." + name);
9.      }
10. }

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

###### 第三方bean管理

1.  第三方bean管理
2.  public class SpringConfig {
3.      _//1.定义一个方法获得要管理的对象_
4.      _//2.添加@Bean，表示当前方法的返回值是一个bean_
5.      _//@Bean修饰的方法，形参根据类型自动装配_
6.      @Bean
7.      public DataSource dataSource(BookDao bookDao){

9.          DruidDataSource ds = new DruidDataSource();
10.         ds.setDriverClassName("com.mysql.jdbc.Driver");
11.         ds.setUrl("jdbc:mysql://localhost:3306/spring_db");
12.         ds.setUsername("root");
13.         ds.setPassword("root");
14.         return ds;
15.     }
16. }

1.  public class App {
2.      public static void main(String\[\] args) {
3.          AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(SpringConfig.class);
4.          DataSource dataSource = ctx.getBean(DataSource.class);
5.          System.out.println(dataSource);
6.      }
7.  }

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

10.         DruidDataSource ds = new DruidDataSource();
11.         ds.setDriverClassName("com.mysql.jdbc.Driver");
12.         ds.setUrl("jdbc:mysql://localhost:3306/spring_db");
13.         ds.setUsername("root");
14.         ds.setPassword("root");
15.         return ds;
16.     }
17. }

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

###### 注解开发总结

XML配置vs注解开发

<div class="joplin-table-wrapper"><table><tbody><tr><td><p>功能</p></td><td><p>XML配置</p></td><td><p>注解</p></td></tr><tr><td><p>定义bean</p></td><td><p>Bean标签</p><ul><li>Id属性</li><li>Class属性</li></ul></td><td><p>@Component</p><p>@Controller</p><p>@Service</p><p>@Repository</p><p>@ComponentScan</p></td></tr><tr><td><p>设置依赖注入</p></td><td><p>Setter注入</p><p>构造器注入</p><p>自动装配</p></td><td><p>@Autowired</p><p>@Qualifier</p><p>@Value</p></td></tr><tr><td><p>配置第三方bean</p></td><td><p>Bean标签</p><p>静态工厂，实例工厂，FactoryBean</p></td><td><p>@Bean</p></td></tr><tr><td><p>作用范围</p></td><td><p>Scope属性</p></td><td><p>@scope</p></td></tr><tr><td><p>生命周期</p></td><td><p>标准接口</p><ul><li>init-method</li><li>destory-method</li></ul></td><td><p>@PostConstructor</p><p>@PreDestory</p></td></tr></tbody></table></div>

##### 整合

###### Spring整合MyBatis

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

13.         _// 6. 释放资源_
14.         sqlSession.close();

初始化SqlSessionFactory - 获取连接，获取实现 - 获取数据层接口 - 关闭连接

核心对象：SqlSessionFactory

SqlMapConfig

1.  &lt;configuration&gt;
2.      &lt;properties resource="jdbc.properties"&gt;&lt;/properties&gt;
3.      &lt;typeAliases&gt;
4.          &lt;package name="com.itheima.domain"/&gt;
5.      &lt;/typeAliases&gt;
6.      &lt;environments default="mysql"&gt;
7.          &lt;environment id="mysql"&gt;
8.              &lt;transactionManager type="JDBC"&gt;&lt;/transactionManager&gt;
9.              &lt;dataSource type="POOLED"&gt;
10.                 &lt;property name="driver" value="${jdbc.driver}"&gt;&lt;/property&gt;
11.                 &lt;property name="url" value="${jdbc.url}"&gt;&lt;/property&gt;
12.                 &lt;property name="username" value="${jdbc.username}"&gt;&lt;/property&gt;
13.                 &lt;property name="password" value="${jdbc.password}"&gt;&lt;/property&gt;
14.             &lt;/dataSource&gt;
15.         &lt;/environment&gt;
16.     &lt;/environments&gt;
17.     &lt;mappers&gt;
18.         &lt;package name="com.itheima.dao"&gt;&lt;/package&gt;
19.     &lt;/mappers&gt;
20. &lt;/configuration&gt;

整合MyBatis

初始化属性数据 - 初始化类别别名 - 初始化dataSource - 初始化映射配置

1.  整合MyBatis

准备：

额外导包

1.      &lt;dependency&gt;
2.        &lt;groupId&gt;org.springframework&lt;/groupId&gt;
3.        &lt;artifactId&gt;spring-jdbc&lt;/artifactId&gt;
4.        &lt;version&gt;5.2.10.RELEASE&lt;/version&gt;
5.      &lt;/dependency&gt;

7.      &lt;dependency&gt;
8.        &lt;groupId&gt;org.mybatis&lt;/groupId&gt;
9.        &lt;artifactId&gt;mybatis-spring&lt;/artifactId&gt;
10.       &lt;version&gt;1.3.0&lt;/version&gt;
11.     &lt;/dependency&gt;

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

11.     @Bean
12.     public DataSource dataSource(){
13.         DruidDataSource ds = new DruidDataSource();
14.         ds.setDriverClassName(driver);
15.         ds.setUrl(url);
16.         ds.setUsername(userName);
17.         ds.setPassword(password);
18.         return ds;
19.     }
20. }

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

1.      &lt;typeAliases&gt;
2.          &lt;package name="com.itheima.domain"/&gt;
3.      &lt;/typeAliases&gt;
4.      &lt;environments default="mysql"&gt;
5.          &lt;environment id="mysql"&gt;
6.              &lt;transactionManager type="JDBC"&gt;&lt;/transactionManager&gt;
7.              &lt;dataSource type="POOLED"&gt;
8.                  &lt;property name="driver" value="${jdbc.driver}"&gt;&lt;/property&gt;
9.                  &lt;property name="url" value="${jdbc.url}"&gt;&lt;/property&gt;
10.                 &lt;property name="username" value="${jdbc.username}"&gt;&lt;/property&gt;
11.                 &lt;property name="password" value="${jdbc.password}"&gt;&lt;/property&gt;
12.             &lt;/dataSource&gt;
13.         &lt;/environment&gt;
14.     &lt;/environments&gt;
15.     &lt;mappers&gt;
16.         &lt;package name="com.itheima.dao"&gt;&lt;/package&gt;
17.     &lt;/mappers&gt;

只需要配置不是默认的部分

2.Line1-3对应1.Line6

2.Line15-17对应1.Line14

1.Line7使用形参注入引用类型，引用JdbcConfig中的dataSouce （bean）

1.      &lt;mappers&gt;
2.          &lt;package name="com.itheima.dao"&gt;&lt;/package&gt;
3.      &lt;/mappers&gt;

对于这一段与SqlSession不是一体的，SqlSessionFactoryBean只负责造出SqlSession

###### Spring整合JUnit

src\\test\\java\\com\\itheima\\service\\AccountServiceTest.java

1.  _//设置类运行器_
2.  @RunWith(SpringJUnit4ClassRunner.class)
3.  _//设置Spring环境对应的配置类_
4.  @ContextConfiguration(classes = SpringConfig.class)
5.  public class AccountServiceTest {
6.      _//支持自动装配注入bean_
7.      @Autowired
8.      private AccountService accountService;

10.     @Test
11.     public void testFindById(){
12.         System.out.println(accountService.findById(1));

14.     }

16.     @Test
17.     public void testFindAll(){
18.         System.out.println(accountService.findAll());
19.     }
20. }

使用Spring整合Junit专用的类加载器

##### AOP

###### AOP简介

- AOP（Aspect Oriented Programming）面向切面编程，一种编程范式，知道开发者如何组织程序结构
- 作用：在不惊动原始设计（不需要修改源代码）的基础上为其进行功能增强
- Spring理念：无入侵式编程

###### AOP核心概念

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

###### AOP入门案例

1.  AOP入门案例思路分析

案例设定：测定接口执行效率

简化设定：在接口执行前输出当前系统时间

开发模式：注解

1.  AOP入门案例实现

- 导入坐标（pom.xml）

1.      &lt;dependency&gt;
2.        &lt;groupId&gt;org.springframework&lt;/groupId&gt;
3.        &lt;artifactId&gt;spring-context&lt;/artifactId&gt;
4.        &lt;version&gt;5.2.10.RELEASE&lt;/version&gt;
5.      &lt;/dependency&gt;
6.      &lt;dependency&gt;
7.        &lt;groupId&gt;org.aspectj&lt;/groupId&gt;
8.        &lt;artifactId&gt;aspectjweaver&lt;/artifactId&gt;
9.        &lt;version&gt;1.9.4&lt;/version&gt;
10.     &lt;/dependency&gt;

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

10.     _//设置在切入点pt()的前面运行当前操作（前置通知）_
11. @Before("pt()")
12.     public void method(){
13.         System.out.println(System.currentTimeMillis());
14.     }
15. }

配置@EnableAspectJAutoProxy

1.  @Configuration
2.  @ComponentScan("com.itheima")
3.  _//开启注解开发AOP功能_
4.  @EnableAspectJAutoProxy
5.  public class SpringConfig {
6.  }

开启注解式AOP注解驱动支持

###### AOP工作流程

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

###### AOP切入点表达式

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

###### AOP通知类型

- AOP通知类型描述了抽取的共性功能，根据共性功能抽取的位置不同，最终运行代码时要将其加入合理的位置
- AOP通知共分为5种类型
- 前置通知
- 后置通知

1.      @Pointcut("execution(void com.itheima.dao.BookDao.update())")
2.      private void pt(){}
3.      @Pointcut("execution(int com.itheima.dao.BookDao.select())")
4.      private void pt2(){}

6.      _//@Before：前置通知，在原始方法运行之前执行_
7.  @Before("pt()")
8.      public void before() {
9.          System.out.println("before advice ...");
10.     }

12.     _//@After：后置通知，在原始方法运行之后执行_
13. @After("pt2()")
14.     public void after() {
15.         System.out.println("after advice ...");
16.     }

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

###### 案例：测量业务层接口万次执行效率

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

8.      _//设置环绕通知，在原始操作的运行前后记录执行时间_
9.      @Around("ProjectAdvice.servicePt()")
10.     public void runSpeed(ProceedingJoinPoint pjp) throws Throwable {
11.         _//获取执行的签名对象_
12.         Signature signature = pjp.getSignature();
13.         String className = signature.getDeclaringTypeName();
14.         String methodName = signature.getName();

16.         long start = System.currentTimeMillis();
17.         for (int i = 0; i < 10000; i++) {
18.            pjp.proceed();
19.         }

21.         long end = System.currentTimeMillis();
22.         System.out.println("万次执行："+ className+"."+methodName+"---->" +(end-start) + "ms");
23.     }
24. }

注：

模拟当前测试的接口执行效率仅仅是一个理论值，并不是一次完整的执行过程

###### AOP通知获取数据

- 获取切入点方法参数
- JoinPoint：适用于前置后置返回后抛出异常后通知

1.      _//JoinPoint：用于描述切入点的对象，必须配置成通知方法中的第一个参数，可用于获取原始方法调用的参数_
2.      @Before("pt()")
3.      public void before(JoinPoint jp) {
4.          Object\[\] args = jp.getArgs();
5.          System.out.println(Arrays.toString(args));
6.          System.out.println("before advice ..." );
7.      }

9.      @After("pt()")
10.     public void after(JoinPoint jp) {
11.         Object\[\] args = jp.getArgs();
12.         System.out.println(Arrays.toString(args));
13.         System.out.println("after advice ...");
14.     }

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

###### 案例：百度网盘密码数据兼容处理

分析：

在业务方法执行之前对所有输入参数进行格式处理-trim()

使用处理后参数调用原始方法-环绕通用之中存在对原始方法的调用

DataAdvice

1.  @Component
2.  @Aspect
3.  public class DataAdvice {
4.     @Pointcut("execution(boolean com.itheima.service.\*Service.\*(\*,\*))")
5.      private void servicePt(){}

7.      @Around("DataAdvice.servicePt()")
8.      public Object trimStr(ProceedingJoinPoint pjp) throws Throwable {
9.          Object\[\] args = pjp.getArgs();
10.         for (int i = 0; i < args.length; i++) {
11.             _//判断参数是不是字符串_
12.             if(args\[i\].getClass().equals(String.class)){
13.                 args\[i\] = args\[i\].toString().trim();
14.             }
15.         }
16.         Object ret = pjp.proceed(args);
17.         return ret;
18.     }

20. }

###### AOP总结

- 概念：面向切面编程，一种编程范式
- 作用：在不惊动原始设计的基础上为方法进行功能增强
- 核心概念
- 代理（Proxy）：SpringAOP中理解为任意方法的执行
- 连接点（JoinPoint）：在SpringAOP中，理解为任意方法的执行
- [切入点（PointCut）](#_AOP切入点表达式)：匹配连接点的式子，也有具有共性功能的方法描述
- [通知（Advice）](#_AOP通知类型)：若干个方法的共性功能，在切入点处执行，最终体现为一个方法
- 切面（Aspect）：描述通知与切入点的对应关系
- 目标对象（Target）：被代理的原始对象成为目标对象

##### 事务

- 事务作用：在数据层保障一系列数据库操作同成功同失败
- Spring事务作用：在数据层保障一系列数据库操作同成功同失败

###### Spring事务简介

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

###### Spring事务角色

事务1（事务协调员）

|

1.      @Update("update tbl_account set money = money + #{money} where name = #{name}")
2.      void inMoney(@Param("name") String name, @Param("money") Double money);

4.      @Update("update tbl_account set money = money - #{money} where name = #{name}")
5.      void outMoney(@Param("name") String name, @Param("money") Double money);

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

###### Spring事务属性

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

### SpringMVC

SpringMVC技术与Servlet技术功能等同，均属于web（表现层）层开发技术

#### SpringMVC简介

@ResponseBody注解用于将控制器方法返回的对象转换为JSON或XML数据并直接写入HTTP响应体，常用于异步请求处理。@RequestBody则用于从前端请求中读取JSON或XML数据，并将其绑定到方法参数上。

页面————后端服务器

HTML 表现层（此前使用Servlet，现在使用SpringMVC替代）

CSS 业务层

VUE 数据层（Mybatis）

ElementUI

SpringMVC是一种基于Java实现MVC模型的轻量级Web框架

优点：使用简单，开发便捷，灵活性强

##### SpringMVC入门案例

1.  使用SpringMVC技术需要先导入SpringMVC与Servlet坐标
2.      &lt;dependency&gt;
3.        &lt;groupId&gt;javax.servlet&lt;/groupId&gt;
4.        &lt;artifactId&gt;javax.servlet-api&lt;/artifactId&gt;
5.        &lt;version&gt;3.1.0&lt;/version&gt;
6.        &lt;scope&gt;provided&lt;/scope&gt;ws
7.      &lt;/dependency&gt;
8.      &lt;dependency&gt;
9.        &lt;groupId&gt;org.springframework&lt;/groupId&gt;
10.       &lt;artifactId&gt;spring-webmvc&lt;/artifactId&gt;
11.       &lt;version&gt;5.2.10.RELEASE&lt;/version&gt;
12.     &lt;/dependency&gt;

1.  创建SpringMVC控制器类（同Servlet）
2.  _//定义表现层控制器bean_
3.  @Controller
4.  public class UserController {

6.      _//设置映射路径为/save，即外部访问路径_
7.      @RequestMapping("/save")
8.      _//设置当前操作返回结果为指定json数据（本质上是一个字符串信息）_
9.      @ResponseBody
10.     public String save(){
11.         System.out.println("user save ...");
12.         return "{'info':'springmvc'}";
13.     }

15.     _//设置映射路径为/delete，即外部访问路径_
16.     @RequestMapping("/delete")
17.     @ResponseBody
18.     public String delete(){
19.         System.out.println("user save ...");
20.         return "{'info':'springmvc'}";
21.     }
22. }

1.  初始化SpringMVC环境（同Spring环境），设定SpringMVC加载Controller对应的bean
2.  _//springmvc配置类，本质上还是一个spring配置类_
3.  @Configuration
4.  @ComponentScan("com.itheima.controller")
5.  public class SpringMvcConfig {
6.  }

1.  初始化Servlet容器（Tomcat），加载SpringMVC环境并设置SpringMVC技术处理的请求
2.  _//web容器配置类_
3.  public class ServletContainersInitConfig extends AbstractDispatcherServletInitializer {
4.      _//加载springmvc配置类，产生springmvc容器（本质还是spring容器）_
5.      protected WebApplicationContext createServletApplicationContext() {
6.          _//初始化WebApplicationContext对象_
7.          AnnotationConfigWebApplicationContext ctx = new AnnotationConfigWebApplicationContext();
8.          _//加载指定配置类_
9.          ctx.register(SpringMvcConfig.class);
10.         return ctx;
11.     }

13.     _//设置由springmvc控制器处理的请求映射路径 哪些请求归属SpringMVC处理_
14.     protected String\[\] getServletMappings() {
15.         return new String\[\]{"/"};
16.     }

18.     _//加载spring配置类_
19.     protected WebApplicationContext createRootApplicationContext() {
20.         return null;
21.     }
22. }

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

##### 入门案例工作流程

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

##### Bean加载控制

因为功能不同，怎么避免Spring错误地加载到Controller（SpringMVC）的bean

\--加载Spring控制的bean的时候，排除掉SpringMVC控制的bean

两种方式：扫描指定包/过滤

1.  @Configuration
2.  _//@ComponentScan({"com.itheima.service","com.itheima.dao"})_

4.  _//设置spring配置类加载bean时的过滤规则，当前要求排除掉表现层对应的bean_
5.  _//excludeFilters属性：设置扫描加载bean时，排除的过滤规则_
6.  _//type属性：设置排除规则，当前使用按照bean定义时的注解类型进行排除_
7.  _//classes属性：设置排除的具体注解类，当前设置排除@Controller定义的bean_
8.  @ComponentScan(value="com.itheima",
9.      excludeFilters = @ComponentScan.Filter(
10.         type = FilterType.ANNOTATION,
11.         classes = Controller.class
12.     )
13. )
14. public class SpringConfig {
15. }

ANNOTATION//按照注解过滤

ASSIGNABLE_TYPE //按照类型过滤

ASPECTJ//按照ASPECTJ表达式过滤

REGEX//按照正则表达式过滤

CUSTOM//按照自定义的过滤规则过滤

简化开发

1.  _//web配置类简化开发，仅设置配置类类名即可_
2.  public class ServletContainersInitConfig extends AbstractAnnotationConfigDispatcherServletInitializer {

4.      protected Class&lt;?&gt;\[\] getRootConfigClasses() {
5.          return new Class\[\]{SpringConfig.class};
6.      }

8.      protected Class&lt;?&gt;\[\] getServletConfigClasses() {
9.          return new Class\[\]{SpringMvcConfig.class};
10.     }

12.     protected String\[\] getServletMappings() {
13.         return new String\[\]{"/"};
14.     }
15. }

修改继承的类，简化配置

##### PostMan

功能强大的网页调试与发送网页HTTP请求的Chrome插件

作用：常用于接口测试

#### 请求与响应

##### 请求映射路径

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

##### 请求参数

###### 普通参数传递

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

###### 其余四种参数传递

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
20.     public String listParam(@RequestParam List&lt;String&gt; likes){
21.         System.out.println("集合参数传递 likes ==> "+ likes);
22.         return "{'module':'list param'}";
23.     }

###### json数据传递参数（接收请求中的json数据）

Step1：导入json依赖

1.      &lt;dependency&gt;
2.        &lt;groupId&gt;com.fasterxml.jackson.core&lt;/groupId&gt;
3.        &lt;artifactId&gt;jackson-databind&lt;/artifactId&gt;
4.        &lt;version&gt;2.9.0&lt;/version&gt;
5.      &lt;/dependency&gt;

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
6.      public String listPojoParamForJson(@RequestBody List&lt;User&gt; likes){
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
6.      public String listPojoParamForJson(@RequestBody List&lt;User&gt; list){
7.          System.out.println("list pojo(json)参数传递 list ==> "+list);
8.          return "{'module':'list pojo for json param'}";
9.      }

后期开发中，发送json格式数据为主，@RequestBody应用较广

如果发送非json格式数据，选用@RequestParam接收请求参数

###### 日期类型参数传递

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

##### 响应

###### 响应页面/文本数据

1.  _//响应页面/跳转页面_
2.      _//返回值为String类型，设置返回值为页面名称，即可实现页面跳转_
3.      @RequestMapping("/toJumpPage")
4.      public String toJumpPage(){
5.          System.out.println("跳转页面");
6.          return "page.jsp";
7.      }

9.      _//响应文本数据_
10.     _//返回值为String类型，设置返回值为任意字符串信息，即可实现返回指定字符串信息，需要依赖@ResponseBody注解_
11.     @RequestMapping("/toText")
12.     @ResponseBody
13.     public String toText(){
14.         System.out.println("返回纯文本数据");
15.         return "response text";
16.     }

1.  响应pojo对象
2.      _//响应POJO对象_
3.      _//返回值为实体类对象，设置返回值为实体类类型，即可实现返回对应对象的json数据，需要依赖@ResponseBody注解和@EnableWebMvc注解_
4.      @RequestMapping("/toJsonPOJO")
5.      @ResponseBody
6.      public User toJsonPOJO(){
7.          System.out.println("返回json对象数据");
8.          User user = new User();
9.          user.setName("itcast");
10.         user.setAge(15);
11.         return user;
12.     }

@ResponseBody

类型：方法注解

位置：SpringMVC控制器定义上方

作用：设置当前控制器返回值作为响应体

通过HttpMessageConverter接口（类型转换器）实现

#### REST风格

##### REST简介

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

##### RESTful入门案例

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

##### REST快速开发（简化开发）

1.  _//@Controller_
2.  _//@ResponseBody配置在类上可以简化配置，表示设置当前每个方法的返回值都作为响应体_
3.  _//@ResponseBody_
4.  @RestController     
5.  _//使用@RestController注解替换@Controller与@ResponseBody注解，简化书写_
6.  @RequestMapping("/books")
7.  public class BookController {

9.  _//    @RequestMapping( method = RequestMethod.POST)_
10.     @PostMapping        
11. _//使用@PostMapping简化Post请求方法对应的映射配置_
12.     public String save(@RequestBody Book book){
13.         System.out.println("book save..." + book);
14.         return "{'module':'book save'}";
15.     }

17. _//    @RequestMapping(value = "/{id}" ,method = RequestMethod.DELETE)_
18.     @DeleteMapping("/{id}")     
19. _//使用@DeleteMapping简化DELETE请求方法对应的映射配置_
20.     public String delete(@PathVariable Integer id){
21.         System.out.println("book delete..." + id);
22.         return "{'module':'book delete'}";
23.     }

25. _//    @RequestMapping(method = RequestMethod.PUT)_
26.     @PutMapping         
27. _//使用@PutMapping简化Put请求方法对应的映射配置_
28.     public String update(@RequestBody Book book){
29.         System.out.println("book update..."+book);
30.         return "{'module':'book update'}";
31.     }

33. _//    @RequestMapping(value = "/{id}" ,method = RequestMethod.GET)_
34.     @GetMapping("/{id}")    
35. _//使用@GetMapping简化GET请求方法对应的映射配置_
36.     public String getById(@PathVariable Integer id){
37.         System.out.println("book getById..."+id);
38.         return "{'module':'book getById'}";
39.     }

41. _//    @RequestMapping(method = RequestMethod.GET)_
42.     @GetMapping             
43. _//使用@GetMapping简化GET请求方法对应的映射配置_
44.     public String getAll(){
45.         System.out.println("book getAll...");
46.         return "{'module':'book getAll'}";
47.     }
48. }

@RestController替换@Controller与@ResponseBody注解，简化书写

@GetMapping @PostMapping @PutMapping @DeleteMapping 每个都对应一个请求动作

##### 案例：基于RESTful页面数据交互

接口制作

1.  @RestController
2.  @RequestMapping("/books")
3.  public class BookController {

5.      @PostMapping
6.      public String save(@RequestBody Book book){
7.          System.out.println("book save ==> "+ book);
8.          return "{'module':'book save success'}";
9.      }

11.     @GetMapping
12.     public List&lt;Book&gt; getAll(){ 
13.         System.out.println("book getAll is running ...");
14.         List&lt;Book&gt; bookList = new ArrayList&lt;Book&gt;();

16.         Book book1 = new Book();
17.         book1.setType("计算机");
18.         book1.setName("SpringMVC入门教程");
19.         book1.setDescription("小试牛刀");
20.         bookList.add(book1);

22.         Book book2 = new Book();
23.         book2.setType("计算机");
24.         book2.setName("SpringMVC实战教程");
25.         book2.setDescription("一代宗师");
26.         bookList.add(book2);

28.         Book book3 = new Book();
29.         book3.setType("计算机丛书");
30.         book3.setName("SpringMVC实战教程进阶");
31.         book3.setDescription("一代宗师呕心创作");
32.         bookList.add(book3);

34.         return bookList;
35.     }

37. }

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

1.  &lt;script&gt;
2.          var vue = new Vue({

4.              el: '#app',

6.              data:{
7.      dataList: \[\],_//当前页要展示的分页列表数据_
8.                  formData: {},_//表单数据_
9.                  dialogFormVisible: false,_//增加表单是否可见_
10.                 dialogFormVisible4Edit:false,_//编辑表单是否可见_
11.                 pagination: {},_//分页模型数据，暂时弃用_
12.             },

14.             _//钩子函数，VUE对象初始化完成后自动执行_
15.             created() {
16.                 this.getAll();
17.             },

19.             methods: {
20.                 _// 重置表单_
21.                 resetForm() {
22.                     _//清空输入框_
23.                     this.formData = {};
24.                 },

26.                 _// 弹出添加窗口_
27.                 openSave() {
28.                     this.dialogFormVisible = true;
29.                     this.resetForm();
30.                 },

32.                 _//添加_
33.                 saveBook () {
34.                     axios.post("/books",this.formData).then((res)=>{

36.                     });
37.                 },

39.                 _//主页列表查询_
40.                 getAll() {
41.                     axios.get("/books").then((res)=>{
42.                         this.dataList = res.data;
43.                     });
44.                 },

46.             }
47.         })
48.     &lt;/script&gt;

小结：

制作SpringMVC控制器，并通过PostMan测试接口功能（使用假数据）

设置对静态资源的访问放行

前端页面通过异步提交访问后台控制器

#### SSM整合

##### SSM整合

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

###### 创建工程

需要导入坐标

Spring-webmvc/Spring-jdbc/Spring-test/Mybatis/Mysql/Druid/Junit/Servlet/Jackson

###### SSM整合配置

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

11.     @Bean
12.     public DataSource dataSource(){
13.         DruidDataSource dataSource = new DruidDataSource();
14.         dataSource.setDriverClassName(driver);
15.         dataSource.setUrl(url);
16.         dataSource.setUsername(username);
17.         dataSource.setPassword(password);
18.         return dataSource;
19.     }

21.     @Bean
22.     public PlatformTransactionManager transactionManager(DataSource dataSource){
23.         DataSourceTransactionManager ds = new DataSourceTransactionManager();
24.         ds.setDataSource(dataSource);
25.         return ds;
26.     }
27. }

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
2.      protected Class&lt;?&gt;\[\] getRootConfigClasses() {
3.          return new Class\[\]{SpringConfig.class};
4.      }

6.      protected Class&lt;?&gt;\[\] getServletConfigClasses() {
7.          return new Class\[\]{SpringMvcConfig.class};
8.      }

10.     protected String\[\] getServletMappings() {
11.         return new String\[\]{"/"};
12.     }
13. }

还可以创建一个过滤器来处理中文表单提交乱码的过滤

###### 功能模块

创建实体类Book

1.  public class Book {
2.      private Integer id;
3.      private String type;
4.      private String name;
5.      private String description;

7.      @Override
8.      public String toString() {
9.          return "Book{" +
10.                 "id=" + id +
11.                 ", type='" + type + '\\'' +
12.                 ", name='" + name + '\\'' +
13.                 ", description='" + description + '\\'' +
14.                 '}';
15.     }

17.     public Integer getId() {
18.         return id;
19.     }

21.     public void setId(Integer id) {
22.         this.id = id;
23.     }

25.     public String getType() {
26.         return type;
27.     }

29.     public void setType(String type) {
30.         this.type = type;
31.     }

33.     public String getName() {
34.         return name;
35.     }

37.     public void setName(String name) {
38.         this.name = name;
39.     }

41.     public String getDescription() {
42.         return description;
43.     }

45.     public void setDescription(String description) {
46.         this.description = description;
47.     }
48. }

BookDao

1.  public interface BookDao {

3.  //    @Insert("insert into tbl_book values(null,#{type},#{name},#{description})")
4.      @Insert("insert into tbl_book (type,name,description) values(#{type},#{name},#{description})")
5.      public void save(Book book);

7.      @Update("update tbl_book set type = #{type}, name = #{name}, description = #{description} where id = #{id}")
8.      public void update(Book book);

10.     @Delete("delete from tbl_book where id = #{id}")
11.     public void delete(Integer id);

13.     @Select("select \* from tbl_book where id = #{id}")
14.     public Book getById(Integer id);

16.     @Select("select \* from tbl_book")
17.     public List&lt;Book&gt; getAll();
18. }

BookService

1.  public interface BookService {

3.      _/\*\*_
4.       \* 保存
5.       \* @param book
6.       \* @return
7.       \*/
8.      public boolean save(Book book);

10.     _/\*\*_
11.      \* 修改
12.      \* @param book
13.      \* @return
14.      \*/
15.     public boolean update(Book book);

17.     _/\*\*_
18.      \* 按id删除
19.      \* @param id
20.      \* @return
21.      \*/
22.     public boolean delete(Integer id);

24.     _/\*\*_
25.      \* 按id查询
26.      \* @param id
27.      \* @return
28.      \*/
29.     public Book getById(Integer id);

31.     _/\*\*_
32.      \* 查询全部
33.      \* @return
34.      \*/
35.     public List&lt;Book&gt; getAll();
36. }

BookServiceImpl

1.  @Service
2.  public class BookServiceImpl implements BookService {
3.      @Autowired
4.      private BookDao bookDao;

6.      public boolean save(Book book) {
7.          bookDao.save(book);
8.          return true;
9.      }

11.     public boolean update(Book book) {
12.         bookDao.update(book);
13.         return true;
14.     }

16.     public boolean delete(Integer id) {
17.         bookDao.delete(id);
18.         return true;
19.     }

21.     public Book getById(Integer id) {
22.         return bookDao.getById(id);
23.     }

25.     public List&lt;Book&gt; getAll() {
26.         return bookDao.getAll();
27.     }
28. }

出现bookDao爆红，是因为Spring中没有配bookDao的bean，使用的是mybatis自动代理，所以就没有对应的bean自动装配，但是这里不会影响程序的正常运行

可行的解决方案：

使用构造器注入或者直接忽略错误因为不会影响运行

BookController

1.  @RestController
2.  @RequestMapping("/books")
3.  public class BookController {

5.      @Autowired
6.      private BookService bookService;

8.      @PostMapping
9.      public boolean save(@RequestBody Book book) {
10.         return bookService.save(book);
11.     }

13.     @PutMapping
14.     public boolean update(@RequestBody Book book) {
15.         return bookService.update(book);
16.     }

18.     @DeleteMapping("/{id}")
19.     public boolean delete(@PathVariable Integer id) {
20.         return bookService.delete(id);
21.     }

23.     @GetMapping("/{id}")
24.     public Book getById(@PathVariable Integer id) {
25.         return bookService.getById(id);
26.     }

28.     @GetMapping
29.     public List&lt;Book&gt; getAll() {
30.         return bookService.getAll();
31.     }
32. }

使用RequestMapping配置公共映射

然后使用REST风格

###### 测试

业务层接口测试（整合JUnit）/表现层接口测试（Postman）

业务层（Service）测试

1.  @RunWith(SpringJUnit4ClassRunner.class)
2.  @ContextConfiguration(classes = SpringConfig.class)
3.  public class BookServiceTest {

5.      @Autowired
6.      private BookService bookService;

8.      @Test
9.      public void testGetById(){
10.         Book book = bookService.getById(1);
11.         System.out.println(book);
12.     }

14.     @Test
15.     public void testGetAll(){
16.         List&lt;Book&gt; all = bookService.getAll();
17.         System.out.println(all);
18.     }

20. }

表现层测试（Postman）

###### 添加事务管理

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

##### 表现层数据封装（前后端数据协议）

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

9.      public Result() {}

11.     public Result(Integer code,Object data) {
12.         this.data = data;
13.         this.code = code;
14.     }

16.     public Result(Integer code, Object data, String msg) {
17.         this.data = data;
18.         this.code = code;
19.         this.msg = msg;
20.     }

22.     public Object getData() {return data;}

24.     public void setData(Object data) {this.data = data;}

26.     public Integer getCode() {return code;}

28.     public void setCode(Integer code) {this.code = code;}

30.     public String getMsg() {return msg;}

32.     public void setMsg(String msg) {this.msg = msg;}
33. }

Controller-Code

1.  _//状态码_
2.  public class Code {
3.      public static final Integer SAVE_OK = 20011;
4.      public static final Integer DELETE_OK = 20021;
5.      public static final Integer UPDATE_OK = 20031;
6.      public static final Integer GET_OK = 20041;

8.      public static final Integer SAVE_ERR = 20010;
9.      public static final Integer DELETE_ERR = 20020;
10.     public static final Integer UPDATE_ERR = 20030;
11.     public static final Integer GET_ERR = 20040;
12. }

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

##### 异常处理器

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

##### 项目异常处理方案

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

5.      public Integer getCode() {
6.          return code;
7.      }

9.      public void setCode(Integer code) {
10.         this.code = code;
11.     }

13.     public BusinessException(Integer code, String message) {
14.         super(message);
15.         this.code = code;
16.     }

18.     public BusinessException(Integer code, String message, Throwable cause) {
19.         super(message, cause);
20.         this.code = code;
21.     }

23. }

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

12.     @ExceptionHandler(BusinessException.class)
13.     public Result doBusinessException(BusinessException ex){
14.         return new Result(ex.getCode(),null,ex.getMessage());
15.     }

17.     _//除了自定义的异常处理器，保留对Exception类型的异常处理，用于处理非预期的异常_
18.     @ExceptionHandler(Exception.class)
19.     public Result doOtherException(Exception ex){
20.         _//记录日志_
21.         _//发送消息给运维_
22.         _//发送邮件给开发人员,ex对象发送给开发人员_
23.         return new Result(Code.SYSTEM_UNKNOW_ERR,null,"系统繁忙，请稍后再试！");
24.     }
25. }

##### 案例：SSM整合前台标准开发

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

###### 列表页

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

###### 添加页

1.                  _//添加_
2.                  handleAdd () {
3.                      _//发送ajax请求_
4.                      axios.post("/books",this.formData).then((res)=>{
5.                          console.log(res.data);
6.                          _//如果操作成功，关闭弹层，显示数据_

8.                              this.dialogFormVisible = false;
9.                           this.getAll();
10.                     });
11.                 },

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

###### 弹出编辑窗口

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

1.  &lt;el-table-column label="操作" align="center"&gt;
2.      &lt;template slot-scope="scope"&gt;
3.          &lt;el-button type="primary" size="mini" @click="handleUpdate(scope.row)"&gt;编辑&lt;/el-button&gt;
4.          &lt;el-button type="danger" size="mini" @click="handleDelete(scope.row)"&gt;删除&lt;/el-button&gt;
5.      &lt;/template&gt;
6.  &lt;/el-table-column&gt;

Row对象来自于表格的 :data="dataList" 属性

###### 编辑

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

###### 删除

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

#### 拦截器

##### 拦截器概念

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

##### 入门案例

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

15.     @Override
16.     _//原始方法调用后执行的内容_
17.     public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
18.         System.out.println("postHandle...");
19.     }

21.     @Override
22.     _//原始方法调用完成后执行的内容_
23.     public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
24.         System.out.println("afterCompletion...");
25.     }
26. }

使用false可以终止原始操作的执行

配置拦截器的执行位置

SpringMvcSupport

1.  @Configuration
2.  public class SpringMvcSupport extends WebMvcConfigurationSupport {
3.      @Autowired
4.      private ProjectInterceptor projectInterceptor;

6.      @Override
7.  _//过滤静态资源_
8.      protected void addResourceHandlers(ResourceHandlerRegistry registry) {
9.          registry.addResourceHandler("/pages/\*\*").addResourceLocations("/pages/");
10.     }

12.     @Override
13.     protected void addInterceptors(InterceptorRegistry registry) {
14.         _//配置拦截器_
15.         registry.addInterceptor(projectInterceptor).addPathPatterns("/books","/books/\*");
16.     }
17. }

该拦截器在调用books 和 /books/\* 时拦截，路径可以通过可变参数设置多个

设置扫包

1.  @Configuration
2.  @ComponentScan({"com.itheima.controller"，com.itheima.config})
3.  @EnableWebMvc
4.  _//实现WebMvcConfigurer接口可以简化开发，但具有一定的侵入性_
5.  public class SpringMvcConfig implements WebMvcConfigurer {
6.      }
7.  }

###### 简化开发（侵入性强）

1.  @Configuration
2.  @ComponentScan({"com.itheima.controller"})
3.  @EnableWebMvc
4.  _//实现WebMvcConfigurer接口可以简化开发，但具有一定的侵入性_
5.  public class SpringMvcConfig implements WebMvcConfigurer {
6.      @Autowired
7.      private ProjectInterceptor projectInterceptor;
8.      @Autowired
9.      private ProjectInterceptor2 projectInterceptor2;

11.     @Override
12.     public void addInterceptors(InterceptorRegistry registry) {
13.         _//配置多拦截器_
14.         registry.addInterceptor(projectInterceptor).addPathPatterns("/books","/books/\*");
15.     }
16. }

##### 拦截器参数

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

##### 拦截器链

当配置多个拦截器时，形成拦截器链

拦截器链的运行顺序参照拦截器添加顺序为主

PreHandle：与配置顺序相同，必定运行

PostHandle：与配置顺序相反，可能不运行

AfterCompletion：与配置顺序相反，可能不运行

### Maven Advanced

#### 分模块开发

将原始模块按照功能拆分成若干个子模块，方便模块间的互相调用，接口共享

##### 创建Maven模块

##### 书写模块代码

Maven_02_ssm

1.      _&lt;!--依赖domain运行--&gt;_
2.      &lt;dependency&gt;
3.        &lt;groupId&gt;com.itheima&lt;/groupId&gt;
4.        &lt;artifactId&gt;maven_03_pojo&lt;/artifactId&gt;
5.        &lt;version&gt;1.0-SNAPSHOT&lt;/version&gt;
6.      &lt;/dependency&gt;

依赖domain运行

##### 通过maven指令安装模块到本地仓库（install）

使用install下载到仓库

团队内部开发需要发布模块功能到团队内部可共享的仓库中（私服）

#### 依赖管理

- 依赖指当前项目运行所需的jar，一个项目可以设置多个依赖，依赖具有传递性

##### 传递依赖

- 直接依赖：在当前项目中通过依赖配置建立的依赖关系
- 间接依赖：被以来的资源如果依赖其他资源，当前项目间接依赖其他资源

##### 依赖传递冲突问题

- 路径优先：当依赖中出现相同的资源时，层级越深，优先级越低，层级越浅，优先级越高
- 声明优先：当资源在相同层级被依赖时，配置顺序靠前（配置文件的顺序）的覆盖配置顺序靠后的
- 特殊优先：当同级配置了相同资源的不同版本，后配置的覆盖先配置的

##### 可选依赖与排除依赖

可选依赖-隐藏自己的依赖 对外隐藏当前所依赖的资源——不透明

1.          &lt;dependency&gt;
2.              &lt;groupId&gt;com.itheima&lt;/groupId&gt;
3.              &lt;artifactId&gt;maven_03_pojo&lt;/artifactId&gt;
4.              &lt;version&gt;1.0-SNAPSHOT&lt;/version&gt;
5.              &lt;!--可选依赖是隐藏当前工程所依赖的资源，隐藏后对应资源将不具有依赖传递性;--&gt;
6.              &lt;optional&gt;false&lt;/optional&gt;
7.          &lt;/dependency&gt;

- 排除依赖是隐藏当前资源对应的依赖关系-使用其他的资源时排除不用的依赖

主动断开以来的资源，被排除的资源无需指定版本——不需要

1.        &lt;exclusions&gt;
2.          &lt;exclusion&gt;
3.            &lt;groupId&gt;log4j&lt;/groupId&gt;
4.            &lt;artifactId&gt;log4j&lt;/artifactId&gt;
5.          &lt;/exclusion&gt;
6.          &lt;exclusion&gt;
7.            &lt;groupId&gt;org.mybatis&lt;/groupId&gt;
8.            &lt;artifactId&gt;mybatis&lt;/artifactId&gt;
9.          &lt;/exclusion&gt;
10.       &lt;/exclusions&gt;
11.     &lt;/dependency&gt;

排除依赖仅指定GA即可，无需指定V

#### 聚合与继承

##### 聚合

- 聚合：将多个模块组织成一个整体，同时进行项目构建的过程称为聚合
- 聚合工程：通常是一个不具有业务功能的空工程（有且仅有一个pom文件）
- 作用：使用聚合工程可以将多个工程编组，通过对聚合工程进行构建，实现对时所包含的模块进行同步构建
- 当工程中某个模块发生更新（变更）时，必须保障工程中与已更新模块关联的模块同步更新，此时可以使用聚合工程来解决批量模块同步构建的问题

新建maven_01_parent 设置打包类型为pom

1.      &lt;groupId&gt;com.itheima&lt;/groupId&gt;
2.      &lt;artifactId&gt;maven_01_parent&lt;/artifactId&gt;
3.      &lt;version&gt;1.0-RELEASE&lt;/version&gt;
4.      &lt;packaging&gt;pom&lt;/packaging&gt;

设置当前聚合工程所包含的子模块名称

1.      _&lt;!--设置管理的模块名称--&gt;_
2.      &lt;modules&gt;
3.          &lt;module&gt;../maven_02_ssm&lt;/module&gt;
4.          &lt;module&gt;../maven_03_pojo&lt;/module&gt;
5.          &lt;module&gt;../maven_04_dao&lt;/module&gt;
6.      &lt;/modules&gt;

启动compile后会先构建没有依赖的，交换module的顺序对编译过程不产生影响

##### 继承

- 描述的是两个工程间的关系，与java中的继承相似，子工程可以继承父工程中的配置信息，常见于依赖关系的继承
- 作用：简化配置/减少版本冲突
- 聚合继承一般同一个文件

Maven_02_ssm 在子工程中配置当前继承的夫工程

1.    &lt;parent&gt;
2.      &lt;groupId&gt;com.itheima&lt;/groupId&gt;
3.      &lt;artifactId&gt;maven_01_parent&lt;/artifactId&gt;
4.      &lt;version&gt;1.0-RELEASE&lt;/version&gt;
5.      &lt;relativePath&gt;../maven_01_parent/pom.xml&lt;/relativePath&gt;
6.    &lt;/parent&gt;

配置父工程GAV relativePath

父工程中可选依赖 配置子工程中可选的依赖关系

1.      _&lt;!--定义依赖管理--&gt;_
2.      &lt;dependencyManagement&gt;
3.          &lt;dependencies&gt;
4.              &lt;dependency&gt;
5.                  &lt;groupId&gt;junit&lt;/groupId&gt;
6.                  &lt;artifactId&gt;junit&lt;/artifactId&gt;
7.                  &lt;version&gt;4.12&lt;/version&gt;
8.                  &lt;scope&gt;test&lt;/scope&gt;
9.              &lt;/dependency&gt;
10.         &lt;/dependencies&gt;
11.     &lt;/dependencyManagement&gt;

子工程中使用父工程中的可选依赖时，仅需要提供群组id和项目id，无需提供版本，版本由父工程统一提供，避免版本冲突，子工程中还可以定义父工程中没有定义的依赖关系

##### 继承与聚合的区别

- 作用：聚合用于快速构建项目，配置用于快速配置
- 相同点：
- 聚合与继承的pom.xml文件打包方式均为pom，可以将两种关系制作到同一个pom文件中
- 聚合与继承均属于设计型模块，并无实际的模块内容
- 不同点：
- 聚合是在当前模块中配置关系，聚合可以感知到参与聚合的模块有哪些
- 继承是在子模块中配置关系，父模块无法感知哪些子模块继承了自己

#### 属性管理

##### 属性

1.      _&lt;!--定义属性--&gt;_
2.      &lt;properties&gt;
3.          &lt;spring.version&gt;5.2.10.RELEASE&lt;/spring.version&gt;
4.          &lt;junit.version&gt;4.12&lt;/junit.version&gt;
5.          &lt;mybatis-spring.version&gt;1.3.0&lt;/mybatis-spring.version&gt;
6.          _&lt;!--<jdbc.url&gt;jdbc:mysql://127.0.0.1:3306/ssm_db&lt;/jdbc.url&gt;-->_
7.      &lt;/properties&gt;

9.      _&lt;!--定义依赖管理--&gt;_
10.     &lt;dependencyManagement&gt;
11.         &lt;dependencies&gt;
12.             &lt;dependency&gt;
13.                 &lt;groupId&gt;junit&lt;/groupId&gt;
14.                 &lt;artifactId&gt;junit&lt;/artifactId&gt;
15.                 &lt;version&gt;${junit.version}&lt;/version&gt;
16.                 &lt;scope&gt;test&lt;/scope&gt;
17.             &lt;/dependency&gt;
18.         &lt;/dependencies&gt;
19.     &lt;/dependencyManagement&gt;

定义属性--引用属性

##### 配置文件加载属性

加载jdbc，定义属性

1.      _&lt;!--定义属性--&gt;_
2.      &lt;properties&gt;
3.          &lt;jdbc.url&gt;jdbc:mysql://127.0.0.1:3306/ssm_db&lt;/jdbc.url&gt;
4.      &lt;/properties&gt;

Jdbc.properties配置资源中引用属性

1.  jdbc.driver=com.mysql.jdbc.Driver
2.  jdbc.url=${jdbc.url}
3.  jdbc.username=root
4.  jdbc.password=root

设置资源目录

开启资源文件目录加载属性的过滤器

1.      &lt;build&gt;
2.          &lt;resources&gt;
3.              _&lt;!--设置资源目录，并设置能够解析${}--&gt;_
4.              &lt;resource&gt;
5.                  &lt;directory&gt;${project.basedir}/src/main/resources&lt;/directory&gt;
6.                  &lt;filtering&gt;true&lt;/filtering&gt;
7.              &lt;/resource&gt;
8.          &lt;/resources&gt;
9.      &lt;/build&gt;

${project.basedir}内置属性名

配置maven打jar包，忽略web.xml检查

1.        &lt;plugin&gt;
2.          &lt;groupId&gt;org.apache.maven.plugins&lt;/groupId&gt;
3.          &lt;artifactId&gt;maven-war-plugin&lt;/artifactId&gt;
4.          &lt;version&gt;3.2.3&lt;/version&gt;
5.          &lt;configuration&gt;
6.            &lt;failOnMissingWebXml&gt;false&lt;/failOnMissingWebXml&gt;
7.          &lt;/configuration&gt;
8.        &lt;/plugin&gt;

##### 版本管理

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

#### 多环境配置与应用

场景：生产环境需要一个数据库，开发环境需要一个数据库，测试环境需要一个数据库则需要配置多环境

##### 多环境开发

1.  _&lt;!--配置多环境--&gt;_
2.      &lt;profiles&gt;
3.          _&lt;!--开发环境--&gt;_
4.          &lt;profile&gt;
5.              &lt;id&gt;env_dep&lt;/id&gt;
6.              &lt;properties&gt;
7.                  &lt;jdbc.url&gt;jdbc:mysql://127.1.1.1:3306/ssm_db&lt;/jdbc.url&gt;
8.              &lt;/properties&gt;
9.              _&lt;!--设定是否为默认启动环境--&gt;_
10.             &lt;activation&gt;
11.                 &lt;activeByDefault&gt;true&lt;/activeByDefault&gt;
12.             &lt;/activation&gt;
13.         &lt;/profile&gt;
14.         _&lt;!--生产环境--&gt;_
15.         &lt;profile&gt;
16.             &lt;id&gt;env_pro&lt;/id&gt;
17.             &lt;properties&gt;
18.                 &lt;jdbc.url&gt;jdbc:mysql://127.2.2.2:3306/ssm_db&lt;/jdbc.url&gt;
19.             &lt;/properties&gt;
20.         &lt;/profile&gt;
21.         _&lt;!--测试环境--&gt;_
22.         &lt;profile&gt;
23.             &lt;id&gt;env_test&lt;/id&gt;
24.             &lt;properties&gt;
25.                 &lt;jdbc.url&gt;jdbc:mysql://127.3.3.3:3306/ssm_db&lt;/jdbc.url&gt;
26.             &lt;/properties&gt;
27.         &lt;/profile&gt;
28.     &lt;/profiles&gt;

选中执行指令，mvn install -p env_test 相当于携带test指令

##### 跳过测试

应用场景：功能更新中并且还没有开发完毕/快速打包/...

或者指令实现

mvn package -D skipTests

弊端：全部跳过，一个测试都不执行

配置文件实现跳过指定的测试部分/细粒度管理

1.      &lt;build&gt;
2.          &lt;plugins&gt;
3.              &lt;plugin&gt;
4.                  &lt;artifactId&gt;maven-surefire-plugin&lt;/artifactId&gt;
5.                  &lt;version&gt;2.12.4&lt;/version&gt;
6.                  &lt;configuration&gt;
7.                      &lt;skipTests&gt;false&lt;/skipTests&gt;
8.                      _&lt;!--排除掉不参与测试的内容--&gt;_
9.                      &lt;excludes&gt;
10.                         &lt;exclude&gt;\*\*/BookServiceTest.java&lt;/exclude&gt;
11.                     &lt;/excludes&gt;
12.                 &lt;/configuration&gt;
13.             &lt;/plugin&gt;
14.         &lt;/plugins&gt;
15.     &lt;/build&gt;

#### 私服

##### 私服简介

- 私服是一台独立的服务器，用于解决团队内部的资源共享与资源同步问题
- Nexus

Sonatype公司的一款maven私服产品

启动服务器：nexus.exe /run nexus

访问服务器：http：//localhost：8081

##### 私服仓库分类

|     |     |     |     |
| --- | --- | --- | --- |
| 仓库分类 | 英文名称 | 功能  | 关联操作 |
| 宿主仓库 | Hosted | 保存自主研发+第三方资源 | 上传  |
| 代理仓库 | Proxy | 代理连接中央仓库 | 下载  |
| 仓库组 | Group | 为仓库编组简化下载操作 | 下载  |

##### 资源上传

上传的位置（宿主地址）

|

Idea——本地仓库——私服

|

本地仓库配置访问私服的用户名/密码

下载的地址

1.  在Nexus中配置demo-release与demo-snapshot两个仓库

1.  Settings.xml中配置访问私服的权限
2.      _&lt;!-- 配置访问私服的权限 --&gt;_
3.      &lt;server&gt;
4.        &lt;id&gt;demo-snapshot&lt;/id&gt;
5.        &lt;username&gt;admin&lt;/username&gt;
6.        &lt;password&gt;admin&lt;/password&gt;
7.      &lt;/server&gt;
8.      &lt;server&gt;
9.        &lt;id&gt;demo-release&lt;/id&gt;
10.       &lt;username&gt;admin&lt;/username&gt;
11.       &lt;password&gt;admin&lt;/password&gt;
12.     &lt;/server&gt;

1.  找到group中的maven仓库作为仓库组

1.  移动demo-release与demo-snapshot得到maven-public管理

1.  配置私服的访问路径
2.       &lt;mirror&gt;
3.       _&lt;!-- 私服的访问路径 --&gt;_
4.        &lt;mirror&gt;
5.        &lt;id&gt;maven-public&lt;/id&gt;
6.        &lt;mirrorOf&gt;\*&lt;/mirrorOf&gt;
7.        &lt;url&gt;http://localhost:8081/repository/maven-public/&lt;/url&gt;
8.      &lt;/mirror&gt;
9.    &lt;/mirrors&gt;

这样本地仓库就与私服建立联系

1.  配置当前工程保存在私服中的具体位置
2.      _&lt;!--配置当前工程保存在私服中的具体位置--&gt;_
3.      &lt;distributionManagement&gt;
4.          &lt;repository&gt;
5.              &lt;id&gt;itheima-release&lt;/id&gt;
6.              &lt;url&gt;http://localhost:8081/repository/itheima-release/&lt;/url&gt;
7.          &lt;/repository&gt;
8.          &lt;snapshotRepository&gt;
9.              &lt;id&gt;itheima-snapshot&lt;/id&gt;
10.             &lt;url&gt;http://localhost:8081/repository/itheima-snapshot/&lt;/url&gt;
11.         &lt;/snapshotRepository&gt;
12.     &lt;/distributionManagement&gt;

1.  发布命令

Mvn deploy

### SpringBoot

#### SpringBoot简介

SpringBoot是由Pivotal团队提供的全新框架，其设计的是用来简化Spring应用的初始搭建以及开发过程

##### 入门案例

制作controller类

1.  @RestController
2.  @RequestMapping("/books")
3.  public class BookController {

5.      @GetMapping("/{id}")
6.      public String getById(@PathVariable Integer id){
7.          System.out.println("id ==> "+id);
8.          return "hello , spring boot!";
9.      }
10. }

Application类

1.  @SpringBootApplication
2.  public class Application {

4.      public static void main(String\[\] args) {
5.          SpringApplication.run(Application.class, args);
6.      }
7.  }

SpringBoot内嵌Tomcat已经能启动

##### SpringBoot与Spring对比

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

##### SpringBoot项目快速启动

1.  先对SpringBoot项目打包（执行Maven构建指令package）

1.  找到springboot_01_quickstart-0.0.1-SNAPSHOT文件，打开对应位置
2.  使用cmd打开输入java -jar springboot_01_quickstart-0.0.1-SNAPSHOT

（jar支持命令行启动，但需要依赖maven插件支持）

1.          &lt;plugins&gt;
2.              &lt;plugin&gt;
3.                  &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
4.                  &lt;artifactId&gt;spring-boot-maven-plugin&lt;/artifactId&gt;
5.              &lt;/plugin&gt;

成功快速启动

##### SpringBoot概述

简化Spring应用的初始搭建以及开发过程，自动配置，起步依赖，辅助功能（内置服务器）

Spring程序缺点：配置繁琐，依赖设置繁琐

起步依赖-一次性地写了若干个依赖。开发web程序所需要依赖

1.          &lt;dependency&gt;
2.  &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
3.              &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
4.              &lt;exclusions&gt;
5.                  &lt;exclusion&gt;
6.                     &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
7.                     &lt;artifactId&gt;spring-boot-starter-tomcat&lt;/artifactId&gt;
8.                  &lt;/exclusion&gt;
9.              &lt;/exclusions&gt;
10.         &lt;/dependency&gt;

Parent所有SpringBoot项目要继承的项目，定义若干个坐标版本号，以达到减少依赖冲突的目的

引导类

1.  @SpringBootApplication
2.  public class Application {

4.      public static void main(String\[\] args) {
5.          SpringApplication.run(Application.class, args);
6.      }
7.  }

SpringBoot的引导类是项目的入口，运行main方法就可以启动项目

更改Tomcat服务器

1.          &lt;dependency&gt;
2.              &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
3.              &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
4.              &lt;exclusions&gt;
5.                  &lt;exclusion&gt;
6.                     &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
7.                     &lt;artifactId&gt;spring-boot-starter-tomcat&lt;/artifactId&gt;
8.                  &lt;/exclusion&gt;
9.              &lt;/exclusions&gt;
10.         &lt;/dependency&gt;

12.         &lt;dependency&gt;
13.             &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
14.             &lt;artifactId&gt;spring-boot-starter-jetty&lt;/artifactId&gt;
15.         &lt;/dependency&gt;

需要先排除tomcat，更换jetty服务器（更轻量级，可扩展性更强）

#### 基础配置

##### 三种配置文件

application.properties #server.port=80

application.yaml/yml

1.  server:
2.    port: 82

主写yml文件

注：自动提示功能消失解决方案：

File-Project Structure-Facets-Spring-需要配的工程-追加配置文件（yaml/yml）

加载顺序：.properties > .yml > .yaml

##### Yaml

YAML 一种数据序列化格式，容易阅读，容易与脚本语言交互，以数据为核心，重数据轻格式

###### 语法规则

- 大小写敏感
- 属性层级关系使用多行描述，每行结尾使用冒号结束
- 使用缩进表示层级关系，同层级左侧对齐，只允许使用空格
- 属性值前添加空格（属性名与属性值之间使用冒号 + 空格作为风格）
- \# 表示注释
- 数组数据在数据书写的位置下方使用减号作为数据开始符号，每行书写一个数据，减号与数据间空格风格

###### Yaml数据读取方式

Application.yaml

1.  lesson: SpringBoot

3.  server:
4.    port: 80

6.  enterprise:
7.    name: itcast
8.    age: 16
9.    tel: 4006184000
10.   subject:
11.     - Java
12.     - 前端
13.     - 大数据

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

12.     @GetMapping("/{id}")
13.     public String getById(@PathVariable Integer id){
14.         System.out.println(lesson);
15.         System.out.println(port);
16.         System.out.println(subject_00);
17.         return "hello , spring boot!";
18.     }

20. }

方式二：使用Environment封装全配置数据

1.      _//使用Environment封装全配置数据_
2.      @Autowired
3.      private Environment environment;

1.          System.out.println("--------------------");
2.          System.out.println(environment.getProperty("lesson"));
3.          System.out.println(environment.getProperty("server.port"));
4.          System.out.println("---------------------");

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

##### 多环境启动

###### 配置

1.  在application.yaml中配置
2.  _#设置启用的环境_
3.  spring:
4.    profiles:
5.      active: dev

7.  \---
8.  _#开发_
9.  spring:
10.   config:
11.     activate:
12.       on-profile: dev
13. server:
14.   port: 80
15. \---
16. _#生产_
17. spring:
18.   profiles: pro
19. server:
20.   port: 81
21. \---
22. _#测试_
23. spring:
24.   profiles: test
25. server:
26.   port: 82
27. \---
28. 使用.properties配置

主启动配置文件application.properties

spring.profiles.active=pro

环境分类配置文件application-dev.properties

server.port=8080

环境分类配置文件application-pro.properties

server.port=8081

###### 多环境启动命令格式

先clean再package

带参数启动SpringBoot

Java -jar springboot.jar --spring.profile.active=test

###### 多环境开发兼容问题

Maven中设置多环境属性

1.  &lt;profiles&gt;
2.          _&lt;!--开发环境--&gt;_
3.          &lt;profile&gt;
4.              &lt;id&gt;dev&lt;/id&gt;
5.              &lt;properties&gt;
6.                  &lt;profile.active&gt;dev&lt;/profile.active&gt;
7.              &lt;/properties&gt;
8.          &lt;/profile&gt;
9.          _&lt;!--生产环境--&gt;_
10.         &lt;profile&gt;
11.             &lt;id&gt;pro&lt;/id&gt;
12.             &lt;properties&gt;
13.                 &lt;profile.active&gt;pro&lt;/profile.active&gt;
14.             &lt;/properties&gt;
15.             &lt;activation&gt;
16.                 &lt;activeByDefault&gt;true&lt;/activeByDefault&gt;
17.             &lt;/activation&gt;
18.         &lt;/profile&gt;
19.         _&lt;!--测试环境--&gt;_
20.         &lt;profile&gt;
21.             &lt;id&gt;test&lt;/id&gt;
22.             &lt;properties&gt;
23.                 &lt;profile.active&gt;test&lt;/profile.active&gt;
24.             &lt;/properties&gt;
25.         &lt;/profile&gt;
26.     &lt;/profiles&gt;

SpringBoot中应用Maven属性

1.  _#设置启用的环境_
2.  spring:
3.    profiles:
4.      active: ${profile.active}

Maven指令执行package指令，但没有编译，生成了对应的包，其中类参与编译，但是配置文件并没有编译，而是复制到包中

解决：对于源码中非java类对的操作要求加载Maven对应的属性，解析${}占位符

需要配置maven插件，对资源文件开启对默认占位符的解析

1.  &lt;plugin&gt;
2.                  &lt;groupId&gt;org.apache.maven.plugins&lt;/groupId&gt;
3.                  &lt;artifactId&gt;maven-resources-plugin&lt;/artifactId&gt;
4.                  &lt;version&gt;3.2.0&lt;/version&gt;
5.                  &lt;configuration&gt;
6.                      &lt;encoding&gt;UTF-8&lt;/encoding&gt;
7.                      &lt;useDefaultDelimiters&gt;true&lt;/useDefaultDelimiters&gt;
8.                  &lt;/configuration&gt;
9.              &lt;/plugin&gt;

##### 配置文件分类

SpringBoot中4级配置文件

1级：file：config/application.yml \[最高\] （在文件位置中）

2级：file：application.yml

3级：classpath：config/application.yml （在idea中）

4级：classpath：application.yml

1级与2级留做系统打包后设置通用属性

3级与4级留做系统开发阶段设置通用属性

#### 整合第三方技术

##### 整合Junit

Spring整合Junit

1.  _//设置类运行器_
2.  @RunWith(SpringJUnit4ClassRunner.class)
3.  _//设置Spring环境对应的配置类_
4.  @ContextConfiguration(classes = SpringConfig.class)
5.  public class AccountServiceTest {
6.      _//支持自动装配注入bean_
7.      @Autowired
8.      private AccountService accountService;

10.     @Test
11.     public void testFindById(){
12.         System.out.println(accountService.findById(1));
13.     }

15.     @Test
16.     public void testFindAll(){
17.         System.out.println(accountService.findAll());
18.     }
19. }

SpringBootTest整合

如果测试类在SpringBoot启动类的包或子包中，可以省略启动类的设置，也就是省略classes设定

1.  @SpringBootTest
2.  class Springboot07TestApplicationTests {

4.      @Autowired
5.      private BookService bookService;

7.      @Test
8.      public void save() {
9.          bookService.save();
10.     }

12. }

如果不放在同一包下，指定地址

1.  @SpringBootTest(classes = Springboot07TestApplication.class)

##### 整合mybatis

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

#### 案例：基于SpringBoot的SSM整合案例

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

### MyBatisPlus

#### MyBatisPlus简介

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

1.          &lt;dependency&gt;
2.              &lt;groupId&gt;com.baomidou&lt;/groupId&gt;
3.              &lt;artifactId&gt;mybatis-plus-boot-starter&lt;/artifactId&gt;
4.              &lt;version&gt;3.4.1&lt;/version&gt;
5.          &lt;/dependency&gt;

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

定义数据接口，继承BaseMapper&lt;User&gt;

1.  @Mapper
2.  public interface UserDao extends BaseMapper&lt;User&gt; {
3.  }

- MyBatisPlus特性
- 无侵入：只做增强不做改变，不会对现有工程产生影响
- 强大的CRUD操作，内置通用Mapper，少量配置即可实现单表CRUD操作
- 支持Lambda：编写查询条件无需担心字段写错
- 支持主键自动生成
- 内置分页插件

#### 标准数据层开发

##### 标准数据层CRUD功能

|     |     |     |
| --- | --- | --- |
| 功能  | 自定义接口 | MP接口 |
| 新增  | boolean save（T t） | Int insert（T t） |
| 删除  | boolean delete（int id） | Int deleteById（Serializable id） |
| 修改  | boolean update（T t） | Int updateById（T t） |
| 根据id查询 | T getById（int id） | T selectById（Serializable id） |
| 查询全部 | List&lt;T&gt; getAll（） | List&lt;T&gt; selectList（） |
| 分页查询 | PageInfo&lt;T&gt; getAll（int page,int size） | IPage&lt;T&gt; selectPage（Ipage&lt;T&gt; page） |
| 按条件查询 | List&lt;T&gt; getAll（Condition condition） | IPage&lt;T&gt; selectPage（Wrapper&lt;T&gt; queryWrapper） |

##### 快速开发实体类

导入坐标

1.          &lt;dependency&gt;
2.              &lt;groupId&gt;org.projectlombok&lt;/groupId&gt;
3.              &lt;artifactId&gt;lombok&lt;/artifactId&gt;
4.              &lt;version&gt;1.18.12&lt;/version&gt;
5.          &lt;/dependency&gt;

1.  @Data
2.  @NoArgsConstructor
3.  @AllArgsConstructor
4.  public class User {
5.      private Long id;
6.      private String name;
7.      private String password;
8.      private Integer age;
9.      private String tel;
10. }

1.  @Setter
2.  @Getter
3.  @ToString

等同@Data

##### 分页查询

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

1.  _# 开启mp的日志（输出到控制台）_
2.  mybatis-plus:
3.    configuration:
4.      log-impl: org.apache.ibatis.logging.stdout.StdOutImpl

#### DQL控制

##### 条件查询方式

MyBatisPlus将书写复杂的SQL查询条件进行了封装，使用编程的形式完成查询条件的组合

1.          _//方式一：按条件查询_
2.          QueryWrapper qw = new QueryWrapper();
3.          qw.lt("age",18);
4.          List&lt;User&gt; userList = userDao.selectList(qw);
5.          System.out.println(userList);

7.           _//方式二：lambda格式按条件查询_
8.          QueryWrapper&lt;User&gt; qw = new QueryWrapper&lt;User&gt;();
9.          qw.lambda().lt(User::getAge, 10);
10.         List&lt;User&gt; userList = userDao.selectList(qw);
11.         System.out.println(userList);

13.         _//方式三：lambda格式按条件查询_
14.         LambdaQueryWrapper&lt;User&gt; lqw = new LambdaQueryWrapper&lt;User&gt;();
15.         lqw.lt(User::getAge, 10);
16.         List&lt;User&gt; userList = userDao.selectList(lqw);
17.         System.out.println(userList);

链式编程

1.         LambdaQueryWrapper&lt;User&gt; lqw = new LambdaQueryWrapper&lt;User&gt;();
2.          _//并且关系：10到30岁之间_
3.          _//lqw.lt(User::getAge, 30).gt(User::getAge, 10);_
4.          _//或者关系：小于10岁或者大于30岁_
5.          lqw.lt(User::getAge, 10).or().gt(User::getAge, 30);
6.          List&lt;User&gt; userList = userDao.selectList(lqw);
7.          System.out.println(userList);

Null值处理

1.          LambdaQueryWrapper&lt;User&gt; lqw = new LambdaQueryWrapper&lt;User&gt;();
2.          _//先判定第一个参数是否为true，如果为true连接当前条件_
3.          lqw.lt(null != uq.getAge2(),User::getAge, uq.getAge2());
4.          lqw.gt(null != uq.getAge(),User::getAge, uq.getAge());

6.          List&lt;User&gt; userList = userDao.selectList(lqw);
7.          System.out.println(userList);

##### 查询投影

查询结果包含属性类中部分模型

1.          _//查询投影_
2.          LambdaQueryWrapper&lt;User&gt; lqw = new LambdaQueryWrapper&lt;User&gt;();
3.          lqw.select(User::getId,User::getName,User::getAge);
4.          List&lt;User&gt; userList = userDao.selectList(lqw);
5.          System.out.println(userList);

使用QueryWrapper

1.          QueryWrapper&lt;User&gt; lqw = new QueryWrapper&lt;User&gt;();
2.          lqw.select("id","name","age","tel");

查询结果包含模型类中未定义的属性

1.          QueryWrapper&lt;User&gt; lqw = new QueryWrapper&lt;User&gt;();
2.          lqw.select("count(\*) as count, tel");
3.          lqw.groupBy("tel");
4.          List&lt;Map<String, Object&gt;> userList = userDao.selectMaps(lqw);
5.          System.out.println(userList);

如果有不支持的，去UserDao中使用原生MyBatis

##### 查询条件设定

查询条件

精确查询，查询单个

1.          LambdaQueryWrapper&lt;User&gt; lqw = new LambdaQueryWrapper&lt;User&gt;();
2.          _//等同于=_
3.          lqw.eq(User::getName,"Jerry").eq(User::getPassword,"jerry");
4.          User loginUser = userDao.selectOne(lqw);
5.          System.out.println(loginUser);

范围查询

1.          LambdaQueryWrapper&lt;User&gt; lqw = new LambdaQueryWrapper&lt;User&gt;();
2.          _//范围查询 lt le gt ge eq between_
3.          lqw.between(User::getAge,10,30);
4.          List&lt;User&gt; userList = userDao.selectList(lqw);
5.          System.out.println(userList);

前面小值后面大值

模糊匹配

1.          LambdaQueryWrapper&lt;User&gt; lqw = new LambdaQueryWrapper&lt;User&gt;();
2.          _//模糊匹配 like_
3.          lqw.likeLeft(User::getName,"J");
4.          List&lt;User&gt; userList = userDao.selectList(lqw);
5.          System.out.println(userList);

##### 字段映射与表名映射

###### 问题一：表字段与编码属性设计不同步

@TableFiled 属性注解 模型类属性定义上方

设置当前属性对应的数据表中的字段关系

@TableField（value= “pwd”）

###### 问题二：编码中添加了数据库中未定义的属性

@TableFiled（exist = false）设置属性在数据库字段中是否存在，默认为true，此属性无法与value合并使用

###### 问题三：采用默认查询开放了更多的字段查看权限

@TableFiled（select = false）设置属性是否参与查询，与select（）映射配置不冲突

问题四：表名与编码开发设计不同步

@TableName（“”）设置当前类与表格的关系

#### DML控制

##### id生成策略控制

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

##### 多记录操作

###### 根据主键删除多条记录/根据主键查询多条记录

1.          _//删除指定多条数据_
2.          List&lt;Long&gt; list = new ArrayList<>();
3.          list.add(1402551342481838081L);
4.          list.add(1402553134049501186L);
5.          list.add(1402553619611430913L);
6.          userDao.deleteBatchIds(list);
7.          _//查询指定多条数据_
8.          List&lt;Long&gt; list = new ArrayList<>();
9.          list.add(1L);
10.         list.add(3L);
11.         list.add(4L);
12.         userDao.selectBatchIds(list);

###### 逻辑删除

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

###### 乐观锁

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

4.          _//1.先通过要修改的数据id将当前数据查询出来_
5.          User user = userDao.selectById(3L);     _//version=3_
6.          User user2 = userDao.selectById(3L);    _//version=3_

8.          user2.setName("Jock aaa");
9.          userDao.updateById(user2);              _//version=>4_

1.          user.setName("Jock bbb");
2.          userDao.updateById(user);               _//verion=3?条件不成立_
3.      }

使用乐观锁机制再修改前必须先获取到对应数据的version方可正常进行

#### 快速开发

代码生成器

模板：由MyBatisPlus提供

数据库相关配置：读取数据库获取信息

开发者自定义配置：手工配置

1.          _&lt;!--代码生成器--&gt;_
2.          &lt;dependency&gt;
3.              &lt;groupId&gt;com.baomidou&lt;/groupId&gt;
4.              &lt;artifactId&gt;mybatis-plus-generator&lt;/artifactId&gt;
5.              &lt;version&gt;3.4.1&lt;/version&gt;
6.          &lt;/dependency&gt;

8.          _&lt;!--velocity模板引擎--&gt;_
9.          &lt;dependency&gt;
10.             &lt;groupId&gt;org.apache.velocity&lt;/groupId&gt;
11.             &lt;artifactId&gt;velocity-engine-core&lt;/artifactId&gt;
12.             &lt;version&gt;2.3&lt;/version&gt;
13.         &lt;/dependency&gt;

Generator

1.  public class CodeGenerator {
2.      public static void main(String\[\] args) {
3.          _//1.获取代码生成器的对象_
4.          AutoGenerator autoGenerator = new AutoGenerator();

6.          _//设置数据库相关配置_
7.          DataSourceConfig dataSource = new DataSourceConfig();
8.          dataSource.setDriverName("com.mysql.cj.jdbc.Driver");
9.          dataSource.setUrl("jdbc:mysql://localhost:3306/mybatisplus_db?serverTimezone=UTC");
10.         dataSource.setUsername("root");
11.         dataSource.setPassword("root");
12.         autoGenerator.setDataSource(dataSource);

14.         _//设置全局配置_
15.         GlobalConfig globalConfig = new GlobalConfig();
16.         globalConfig.setOutputDir(System.getProperty("user.dir")+"/mybatisplus_04_generator/src/main/java");    _//设置代码生成位置_
17.         globalConfig.setOpen(false);    _//设置生成完毕后是否打开生成代码所在的目录_
18.         globalConfig.setAuthor("黑马程序员");    _//设置作者_
19.         globalConfig.setFileOverride(true);     _//设置是否覆盖原始生成的文件_
20.         globalConfig.setMapperName("%sDao");    _//设置数据层接口名，%s为占位符，指代模块名称_
21.         globalConfig.setIdType(IdType.ASSIGN_ID);   _//设置Id生成策略_
22.         autoGenerator.setGlobalConfig(globalConfig);

24.         _//设置包名相关配置_
25.         PackageConfig packageInfo = new PackageConfig();
26.         packageInfo.setParent("com.aaa");   _//设置生成的包名，与代码所在位置不冲突，二者叠加组成完整路径_
27.         packageInfo.setEntity("domain");    _//设置实体类包名_
28.         packageInfo.setMapper("dao");   _//设置数据层包名_
29.         autoGenerator.setPackageInfo(packageInfo);

31.         _//策略设置_
32.         StrategyConfig strategyConfig = new StrategyConfig();
33.         strategyConfig.setInclude("tbl_user");  _//设置当前参与生成的表名，参数为可变参数_
34.         strategyConfig.setTablePrefix("tbl_");  _//设置数据库表的前缀名称，模块名 = 数据库表名 - 前缀名  例如： User = tbl_user - tbl__
35.         strategyConfig.setRestControllerStyle(true);    _//设置是否启用Rest风格_
36.         strategyConfig.setVersionFieldName("version");  _//设置乐观锁字段名_
37.         strategyConfig.setLogicDeleteFieldName("deleted");  _//设置逻辑删除字段名_
38.         strategyConfig.setEntityLombokModel(true);  _//设置是否启用lombok_
39.         autoGenerator.setStrategy(strategyConfig);
40.         _//2.执行生成操作_
41.         autoGenerator.execute();
42.     }
43. }


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