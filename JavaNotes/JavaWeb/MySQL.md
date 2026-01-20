- 存储数据的仓库，数据是有组织地进行存储
- 数据管理系统DBMS：管理数据库的大型软件
- SQL: Structured Query language 结构化查询语言，操作数据库的编程语言

关系型数据库

建立在关系模型基础上的数据库，由多张能相互连接的二维表组成。

1.  都是使用表结构，格式一致，易于维护。
2.  使用通用的SQL语言操作，使用方便，可用于复杂查询。
3.  数据存储在磁盘中，安全。

# SQL语法

SQL可以单行或者多行书写，以分号结尾，不区分大小写（关键词建议使用大写）

## 注释

单行注释： --注释内容 或 # 注释内容 （MySQL特有）

多行注释： /\*注释\*/ 同java

## DDL（数据定义语言）
查询

```SQL
SHOW DATABASES；
```
 
创建

```SQL
CREATE DATABASE IF NOT EXISTS 数据库名称
```

删除

```SQL
DROP DATABASES IF EXISTS 数据库名称；
```

使用数据库

```SQL
SELECT DATABASE(); --查询当前使用的数据库

USE 数据库名称；--使用数据库
```

查询表 （Retrive）

```sql
SHOW TABLES； --查询当前数据库下所有表的名称

DESC 表名称； --查询表结构
```

创建表 (Create)
```sql
CREATE TABLE 表名（
       字段名1 数据类型1，
       字段名2 数据类型2，--字符串VARCHAR（最大位数）
       字段名3 数据类型3，
       ...
       字段名n 数据类型n  --最后一行末尾不能加逗号
）；
```

删除表 (Delete)
```sql
DROP TABLE IF EXISTS 表名；
```

修改表 

- 修改表名

```sql
ALTER TABLE 表名 RENAME TO 新的表名；
```

- 添加一列

```sql
ALTER TABLE 表名 ADD 列名 数据类型；
```

- 修改数据类型

```sql
ALTER TABLE 表名 MODIFY 列名 新数据类型；
```

- 修改列名和数据类型

```sql
ALTER TABLE 表名 CHANGE 列名 新列名 新数据类型
```

- 删除列

```sql
ALTER TABLE 表名 DROP 列名；
```

注：数值类型

一般字符串使用VARCHAR可变长度 且 保证性能 过大的使用文件服务器保存路径

Double（总长度，小数点后保留的位数）

## DML（数据操纵语言）

对表中数据进行增删改

1.  添加数据

- 给指定列添加数据

```sql
INSERT INTO 表名（列名1，列名2，...）VALUES（值1，值2，...）
```

- 给全部列添加数据

```sql
INSERT INTO 表名 VALUES（值1，值2）
```

- 批量添加数据

```sql
INSERT INTO 表名（列名1，列名2，...）
VALUES（值1，值2，...）,（值1，值2，...）... ;

INSERT INTO 表名 
VALUES（值1，值2，...）,（值1，值2，...）,（值1，值2...）...;
```

2.  修改数据

```sql
UPDATE 表名 SET 列名1 = 值1，列名2 = 值2，...[WHERE 条件]；
```

如果update语句没有加where条件，则将表中所有数据全部修改

3.  删除数据

```
DELETE FROM表名 [WHERE 条件]；
```

## DQL（数据查询语言）

对表中的数据进行查询

1.  基础查询

- 查询多个字段

```sql
SELECT 字段列表 FROM 表；
SELECT * FROM 表名；--查询所有数据
```

- 去除重复记录

```sql
SELECT DISTINCT 字段列表 FROM 表名；
```

- 起别名

	AS：As也可以省略

2.  条件查询

```sql
SELECT 字段列表 FROM 表名 WHERE 条件；
```

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

3.  排序查询（ORDER BY）

```sql
SELECT 字段列表 FROM 表名 

ORDER BY 排序字段名1 \[排序方式1\] ，排序字段2 \[排序方式2\]  

--- ASC：升序排列（默认值） DESC：降序排列
```

如果有多个排序条件，当前边的条件值一样时才会根据第二条件进行排序

4.  分组查询（GROUP BY）

```sql
SELECT 字段列表 FROM 表名 

[WHERE 分组前条件限定] 

GROUP BY 分组字段名 

[HAVING 分组后条件过滤]
```

WHERE和HAVING区别：执行时机不一样，WHERE是分组之前限定，不满足WHERE条件，则不参与分组，而HABVING是分组之后对结果进行过滤

执行顺序：where>聚合函数>having

注：

聚合函数：将一组数据作为一个整体，进行纵向计算

聚合函数分类：

Count（列名）：统计行数量 取值：主键/\* count(\*) 返回所有行的数量

Max（列名），min（列名），sum（列名） AVG（列名）

5.  分页查询（LIMIT）

```sql
SELECT 字段列表 FROM 表名 LIMIT 起始索引，查询条目数
```

起始索引从0开始 起始索引 = （当前页码 - 1） \* 每页显示的条数

## DCL（数据控制语言）

对数据库进行权限控制

# 约束

约束是作用于表上 列的规则，用于限制加入表的数据
约束的存在保证了数据库中数据的正确性，完整性和有效性

---
- 非空约束 保证列中所有数据不能有null值 NOT NULL
- 唯一约束 保证列中所有数据各不相同 UNIQUE
- 主键约束 主键是一行数据的唯一标识 要求非空且唯一 PRIMARY KEY
- 检查约束 保证列中的值满足其某一条件 CHECK（MySQL不支持）
- 默认约束 保存数据时，未指定值则采用默认值 NULL属于指定值 DEFAULT
- 外键约束 外键用来让两个表之间的数据建立连接 FOREIGN KEY
- 自动增长 auto_increment

外键约束

外键用来让两个表的数据之间建立链接，保证数据的一致性和完整性

添加约束：

（--创建表时添加外键约束）

```sql
CREATE TABLE 表名（
列名 数据类型
 ...
[CONSTRAINT][外键名称] FOREIGN KEY（外键列名）REFERENCES 主表（主表列名）
）
```

（--建完表后添加外键约束）

```sql
ALTER TABLE 表名 ADD CONSTRAINT 外键名称 
FOREIGN KEY（外键字段名称）
REFERENCE 主表名称（主表列名称）
```

删除约束：

```sql
ALTER TABLE 表名 DROP FOREIGN KEY 外键名称；
```

# 数据库设计

## 数据库设计概念

建立数据库中的表结构以及表与表之间的关联关系的过程

有哪些表? 表中有哪些字段? 表和表之间有什么关系？

设计的步骤：

1.  需求分析（数据，数据的属性）
2.  逻辑分析（ER图对数据库进行逻辑建模 不需要考虑选用的dbms）
3.  物理设计（根据数据库自身特点把逻辑设计转换为物理设计）
4.  维护设计（对新的需求进行建表 表优化

## 表关系

1.  一对一：用户和用户详情

	实现方式：在任意一方加入外键，关联另一方主键，并且设置外键为唯一（UNIQUE）

2.  一对多：部门和员工 一个部门有多个员工 一个员工对应一个部门

	实现方式：在多的乙方建立外键，指向一的一方的主键

3.  多对多：商品和订单 一个商品对应多个订单 一个订单包含多个商品

	实现方式：建立第三层中间表，中间表至少把含两个外键，分别关联两个主键

## 数据库设计案例

音乐软件: 抽象成四个表，曲目 专辑 用户 短评

专辑-曲目 一对多 |

用户-短评 一对多 |

专辑-短评 一对多 | 字段分析……

用户-专辑 多对多 |

# 多表查询

## 笛卡儿积

从多张表查询数据 返回多张表所有的可能集合

## 连接查询

1.  内连接：查询AB交集数据

隐式内连接

```sql
SELECT 字段列表 FROM 表1，表2... WHERE 条件；
```

显式内连接

```sql
SELECT 字段列表 FROM 表1 \[INNER\] JOIN 表2 ON 条件；
```

2.  外连接：
左外连接：相当于查询A表（左表）所有数据和交集部分数据

```sql
SELECT 字段列表 FROM 表1  LEFT [OUTER] JOIN 表2 ON 条件
```

右外连接：相当于查询B表（右表）所有数据和交集部分数据

```sql
SELECT 字段列表 FROM 表1  RIGHT [OUTER] JOIN 表2 ON 条件
```

## 子查询

子查询根据查询结果不同 作用不通过

1.  单行单列：作为条件值，使用 = ！ = > < 等进行条件判断

```sql
SELECT 字段列表 FROM 表 WHERE 字段名 = （子查询）；
```

2.  多行多列：作为条件值，使用in等关键词进行条件判断

```sql
SELECT 字段列表 FROM 表 WHERE 字段名 in （子查询）；
```

3.  多行多列：作为虚拟表 多表查询

```sql
SELECT 字段列表 FROM （子查询）WHERE 条件；
```

## 多表查询示例

```sql
-- 部门表
CREATE TABLE dept (
  id INT PRIMARY KEY PRIMARY KEY, -- 部门id
  dname VARCHAR(50), -- 部门名称
  loc VARCHAR(50) -- 部门所在地
);

-- 职务表，职务名称，职务描述
CREATE TABLE job (
  id INT PRIMARY KEY,
  jname VARCHAR(20),
  description VARCHAR(50)
);

-- 员工表
CREATE TABLE emp (
    id INT PRIMARY KEY, -- 员工id
    ename VARCHAR(50), -- 员工姓名
    job_id INT, -- 职务id
    mgr INT , -- 上级领导
    joindate DATE, -- 入职日期
    salary DECIMAL(7,2), -- 工资
    bonus DECIMAL(7,2),-- 奖金
    dept_id INT, -- 所在部门编号
    CONSTRAINT emp_jobid_ref_job_id_fk FOREIGN KEY (job_id) REFERENCES job (id),
    CONSTRAINT emp_deptid_ref_dept_id_fk FOREIGN KEY (dept_id) REFERENCES dept (id)
);

-- 工资等级表
CREATE TABLE salarygrade (
  grade INT PRIMARY KEY,   -- 级别
  losalary INT,  -- 最低工资
  hisalary INT -- 最高工资
);

-- 添加4个部门
INSERT INTO dept(id,dname,loc) VALUES 
(10,'教研部','北京'),
(20,'学工部','上海'),
(30,'销售部','广州'),
(40,'财务部','深圳');

-- 添加4个职务
INSERT INTO job (id, jname, description) VALUES
(1, '董事长', '管理整个公司，接单'),
(2, '经理', '管理部门员工'),
(3, '销售员', '向客人推销产品'),
(4, '文员', '使用办公软件');

-- 添加员工
INSERT INTO emp(id,ename,job_id,mgr,joindate,salary,bonus,dept_id) VALUES 
(1001,'孙悟空',4,1004,'2000-12-17','8000.00',NULL,20),
(1002,'卢俊义',3,1006,'2001-02-20','16000.00','3000.00',30),
(1003,'林冲',3,1006,'2001-02-22','12500.00','5000.00',30),
(1004,'唐僧',2,1009,'2001-04-02','29750.00',NULL,20),
(1005,'李逵',4,1006,'2001-09-28','12500.00','14000.00',30),
(1006,'宋江',2,1009,'2001-05-01','28500.00',NULL,30),
(1007,'刘备',2,1009,'2001-09-01','24500.00',NULL,10),
(1008,'猪八戒',4,1004,'2007-04-19','30000.00',NULL,20),
(1009,'罗贯中',1,NULL,'2001-11-17','50000.00',NULL,10),
(1010,'吴用',3,1006,'2001-09-08','15000.00','0.00',30),
(1011,'沙僧',4,1004,'2007-05-23','11000.00',NULL,20),
(1012,'李逵',4,1006,'2001-12-03','9500.00',NULL,30),
(1013,'小白龙',4,1004,'2001-12-03','30000.00',NULL,20),
(1014,'关羽',4,1007,'2002-01-23','13000.00',NULL,10);

-- 添加5个工资等级_
INSERT INTO salarygrade(grade,losalary,hisalary) VALUES 
(1,7000,12000),
(2,12010,14000),
(3,14010,20000),
(4,20010,30000),
(5,30010,99990);
```

Q&A

```sql
-- 1.查询所有员工信息。查询员工编号，员工姓名，工资，职务名称，职务描述
SELECT emp.id,emp.ename,emp.salary,job.jname,job.description 
FROM job,emp WHERE emp.job_id =job.id

-- 2.查询员工编号，员工姓名，工资，职务名称，职务描述，部门名称，部门位置
SELECT emp.id,emp.ename,emp.salary,job.jname,job.description,dept.dname,dept.loc 
FROM emp,job,dept
WHERE emp.job_id =job.id and dept.id =emp.dept_id;

-- 3.查询员工姓名，工资，工资等级
SELECT emp.ename,emp.salary,salarygrade.\* FROM emp,salarygrade
WHERE emp.salary>= salarygrade.losalary AND emp.salary <= salarygrade.hisalary

-- 4.查询员工姓名，工资，职务名称，职务描述，部门名称，部门位置，工资等级
SELECT emp.ename,emp.salary,job.jname,job.description,dept.dname,dept.loc,salarygrade.grade 
FROM emp,job,dept,salarygrade
WHERE emp.salary>= salarygrade.losalary 
AND emp.salary <= salarygrade.hisalary 
AND emp.job_id =job.id and dept.id =emp.dept_id;

-- 5.查询出部门编号、部门名称、部门位置、部门人数
SELECT dept.id,dept.dname,dept.loc,t1.count 
FROM dept,
(SELECT dept_id, count(\*)count from emp GROUP BY dept_id) t1 
WHERE dept.id = t1.dept_id
```

# 事务

事务是一种机制，一个操作序列，包含一组数据库操作命令，把所有的命令作为一个整体一起向系统提交或撤销操作请求，这一组数据库命令要么同时失败，要么同时成功。事务是一个不可分割的工作逻辑单元。

## 事务操作

```sql
-- 开启事务
START TRANSACTION；
BEGIN
-- 提交事务
COMMIT；
-- 回滚事务 回滚到事务开始的时候_
ROLLBACK；
```

## 事务四大特征

原子性（Atomicity）事务是不可分割的最小操作单位要么同时成功，要么同时失败

一致性（Consistency）事务完成时，必须使所有的数据都保持一致状态

隔离性（Isolation）多个事务之间，操作的可见性

持久性（Durability）事务一旦提交或者回滚，它对数据库中的数据的更改就是永久的

MySQL默认自动提交
