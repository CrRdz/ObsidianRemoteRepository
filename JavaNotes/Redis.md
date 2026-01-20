# Redis

本部分主要基于黑马点评

## 基础篇

### NoSQL

非关系型数据库，非结构化，非关联的，非SQL，事务管理上使用BASE，并非ACID

- 2009年诞生，Remote Dictionary Server 远程词典服务器，是一个基于内存的键值型NoSQL数据库
- 特征
- 键值（key-value）型，value支持多种不同数据结构，功能丰富
- 单线程，每个命令具备原子性
- 低延迟，速度快（基于内存，IO多路复用，良好的编码）
- 支持数据持久化

### 安装Redis

#### 单机安装Redis

安装Redis依赖：

1.  Redis是基于C语言编写，因此首先需要安装Redis所需要的gcc依赖

```linux
yum install -y gcc tcl
```

1.  上传安装包并解压

上传到虚拟机 /usr/local/src目录

解压缩

tar -xzf redis-6.2.6.tar.gz

解压后使用cd命令进入redis目录

cd redis-6.2.6

运行编译命令：

make && make install

#### 启动redis

##### 默认启动

安装完成后，在任意目录输入redis-server命令即可启动Redis

redis-server

##### 指定配置启动

如果要让Redis以后台方式启动，则必须修改Redis配置文件，就在我们之前解压的redis安装包下（\`/usr/local/src/redis-6.2.6\`），名字叫redis.conf

先将这个配置文件备份一份：

cp redis.conf redis.conf.bck

然后修改redis.conf文件中的一些配置：
```zsh
# 允许访问的地址，默认是127.0.0.1，会导致只能在本地访问
   修改为0.0.0.0则可以在任意IP访问，生产环境不要设置为0.0.0.0
bind 0.0.0.0
# 守护进程，修改为yes后即可后台运行
daemonize yes 
# 密码，设置后访问Redis必须输入密码
requirepass 123321
```
注：使用/可以进行快速查找 使用i进入编辑模式 ：wq保存并退出

启动redis
```zsh
# 进入redis安装目录
cd /usr/local/src/redis-6.2.6
# 启动
redis-server redis.conf
```
停止redis
```
# 利用redis-cli来执行 shutdown 命令，即可停止 Redis 服务，
# 因为之前配置了密码，因此需要通过 -u 来指定密码
redis-cli -u ？？？？？？ shutdown
```
##### 开机自启动

新建一个系统服务文件：

vi /etc/systemd/system/redis.service

内容如下：
```zsh
[Unit]
Description=redis-server
After=network.target​

[Service]
Type=forking
ExecStart=/usr/local/bin/redis-server /usr/local/src/redis-6.2.6/redis.conf
PrivateTmp=true​

[Install]
WantedBy=multi-user.target
```
然后重载系统服务

systemctl daemon-reload

现在可以使用命令来操作redis
```zsh
# 启动
systemctl start redis
# 停止
systemctl stop redis
# 重启
systemctl restart redis
# 查看状态
systemctl status redis
# 设置开机自启
systemctl enable redis
```
#### Redis客户端

##### Redis命令行客户端

Redis安装成功后就自带命令行客户端 需要cd到指定目录cd /usr/local/bin/

`redis-cli [options] [commands]`

其中常见的options有：

\-h 127.0.0.1：指定要连接的redis节点的IP地址，默认是127.0.0.1

\-p 6379：指定要连接的redis节点的端口，默认是6379

\-a 123321：指定redis的访问密码

其中的commonds就是Redis的操作命令，例如：

\- ping：与redis服务端做心跳测试，服务端正常会返回\`pong\`

##### 图形化桌面客户端

安装rdm，左上角建立连接，在弹出的窗口中填写Redis服务信息，点击确定后即可建立连接了。Redis默认有16个仓库，编号从0至15. 通过配置文件可以设置仓库数量，但是不超过16，并且不能自定义仓库名称。

### Redis命令

Redis是一个key-value的数据库，key一般是String类型，value的额类型多种多样：

基本类型：String/Hash/List/Set/SortedSet

特殊类型：GEO/BitMap/HyperLog

#### Redis通用命令

通用指令是部分数据类型的，都可以使用的指令，常见的有：

- KEYS：查看符合模板的所有key 不建议在生产环境设备上使用
- DEL：删除一个指定的key
- EXISTS：判断key是否存在
- EXPIRE：给一个key设置有效期，有效期到期时该key会被自动删除
- TTL：查看一个key的剩余有效期

通过help\[command\] 可以查看一个命令的具体用法

#### String类型

- Sting类型，也就是字符串类型，是redis中最简单的存储类型
- 其value是字符串，不过根据字符串的格式不同，又可以分为3类：
- String：普通字符串
- int：整数类型，可以做自增，自减操作
- Float：浮点类型，可以做自增，自减操作

不管是那种格式，底层都是字节数组形式存储，只不过编码方式不同，字符串类型的最大空间不超过512mb

String常见的命令
- SET：添加或者修改已经存在的一个String类型的键值对
- GET：根据key获取String类型的value
- MSET：批量添加多个String类型的键值对
- MGET：根据多个key获取多个String类型的value
- INCR：让一个整型的key自增1
- INCRBY：让一个整型的key自增并指定步长（也有自减的效果）
- INCRBYFLOAT：让一个浮点类型的数字自增并指定步长

（组合命令）

- SETNX：添加一个String类型的键值对，前提是这个key不存在，否则不执行
- SETEX：添加一个String类型的键值对，并且指定有效期

#### Key的层级格式

Redis中没有类似MySQL中的table概念，如何区分不同类型的key—key结构

- Redis的key允许有多个单词形成层级结构，多个单词之间用：隔开，可用：

项目名：业务名：类型：id 类似风格

如果Value是一个java对象，例如一个User对象，则可以将对象序列化为JSON字符串存储

`Heima:user:1 {“id”:1, ”name”: ”Jack”, “age”: 21}`

#### Hash类型

Hash类型也叫散列，其value是一个无序字典，类似于Java中HashMap结构，String结构是对象序列化为json字符串存储，当需要修改对象某个字段是很不方便

| KEY          | VALUE                      |
| ------------ | -------------------------- |
| heima：user：1 | {name”: ”Jack”, “age”: 21} |
| heima：user：2 | {name”: ”Rose”, “age”: 18} |

Hash结构可以将对象中的每个字段独立存储，可以对单个字段做CRUD

| KEY          | VALUE |      |
| ------------ | ----- | ---- |
| Field        | Value |      |
| heima：user：1 | Name  | Rose |
| Age          | 21    |      |
| heima：user：2 | Name  | Rose |
| Age          | 18    |      |

- Hash的常见命令
- HSET key field value：添加或修改hash类型key的field
- HGET key field：获取一个hash类型key的field的值
- HMSET：批量添加多个hash类型key的field的值
- HMGET：批量获取多个hash类型key的field的值
- HGETAALL：获取一个hash类型的key中的所有field和value
- HKEYS：获取一个hash类型的key中所有的field
- HVALS：获取一个hash类型的key中所有的value
- HINCRBY：让一个hash类型key的字段自增并指定步长
- HSETNX：添加一个hash类型的key的field值，前提是field不存在，否则不执行

#### List类型

Redis中的list与Java中的LinkedList类似，可以看作是一个双向链表结构，既可以支持正向检索和也可以支持反向检索。特征业余LinkedList类似：有序，元素可以重复，插入和删除快，查询速度一般

- List常见命令：
- LPUSH key element... :向列表左侧插入一个或多个元素 按照顺序推（左可以看成顶）
- LPOP key：移除并返回列表左侧的第一个元素，没有则返回nil
- RPUSH key element... ：向列表右侧插入一个或多个元素
- RPOP key：移除并返回列表左侧的第一个元素
- LRANGE key star end：返回一段角标范围内所有元素
- BLPOP和BRPOP：与LPOP和RPOP类似，只不过在没有元素时的等待指定时间，而不是直接返回nil

使用List结构模拟一个栈（先进后出）

\-入口和出口在同一边

利用List模拟一个队列（先进先出）

\-入口和出口在不同边

如何利用List结构模拟一个阻塞队列

\-入口和出口在不同边

\-出队时采用BLPOP或BRPOP

#### Set类型

Redis的Set结构与java中的HashSet类似，可以看作是一个value为null的HashMap，因为也是一个hash表，因此具备与HashSet类似的特征：无序/元素不可重复/查找快/支持交集，并集，差集等功能

- Set常见命令：
- SADD key member... ：向set中添加一个或多个元素
- SERM key member... ：移除set中的指定元素
- SCARD key：返回set中元素的个数
- SISMEMBER key member：判断一个元素是否存在于set中
- SMEMBERS：获取set中所有的元素
- SINTER key1 key2... ：求key1与key2的交集
- SDIFF key1 key2...：求key1与key2的差集
- SUNION key1 key2...：求key1和key2的并集

#### SortedSet类型

Redis的SortedSet是一个可排序的set集合，与java中的TreeSet有些类似，但底层数据结构却差别很大。SortedSet中的每一个元素都带有score属性，可以基于score属性对元素排序，底层的实现是一个调表（SkipList）加hash表。SortedSet具备下列特性：可排序/元素不重复/查询速度快，经常被用来排行榜这样的功能

- SortedSet常见命令：
- ZADD key score member：添加一个或多个元素到sorted set，如果已经存在则更新其score值
- ZREM key member：删除sorted set中的一个指定元素
- ZSCORE key member：获取sorted set中的指定元素的score值
- ZRANK key member：获取sorted set中的元素个数
- ZCOUNT key min max：统计score在给定范围内所有元素的个数
- ZINCRBY key increment member：让sorted set中的指定元素自增，步长为指定的increment值
- ZRANGE key min max：按照score排序后，获取指定score范围内的元素
- ZDIFF，ZINTER，ZUNION：求差集，交集，并集
- SortedSet命令练习

将班级的下列学生得分存入Redis的SortedSet中：

Jack 85, Lucy 89, Rose 82, Tom 95, Jerry 78, Amy 92, Miles 76

ZADD stus 85 Jack 89 Lucy 82 Rose 95 Tom 78 Jerry 92 Amy 76 Miles

并实现下列功能：

删除Tom同学

ZREM stus Tom

获取Amy同学的分数

ZSCORE stus Amy

获取Rose同学的排名

ZREVRANK stus Rose

查询80分以下有几个学生

ZCOUNT stus 0 80

给Amy同学加2分

ZINCRBY stus 2 Amy

查出成绩前3名的同学

ZREVRANGE stus 0 2

查出成绩80分以下的所有同学

ZRANGEBYSCORE stus 0 80

### Redis的Java客户端

Jedis，以Redis命令作为方法名称，学习成本低，简单实用，但是Jedis实例是线程不安全的，多线程环境下需要基于连接池使用

Lettuce，基于Netty实现的，支持同步异步和响应式编程方式，并且是线程安全的，支持Redis的哨兵模式，集群模式和管道模式

Redisson，基于Redis实现的分布式，可伸缩地Java数据结构集合，包含了Map，Queue，Lock，Semaphore，AtomicLong等强大功能

#### Jedis

##### 快速入门

引入依赖

1.  &lt;dependency&gt;    
2.      &lt;groupId&gt;com.heima&lt;/groupId&gt;
3.      &lt;artifactId&gt;redis-demo&lt;/artifactId&gt;
4.      &lt;version&gt;0.0.1-SNAPSHOT&lt;/version&gt;
5.      &lt;name&gt;redis-demo&lt;/name&gt;
6.  &lt;/dependency&gt;

建立依赖

1.  private Jedis jedis;

2.  @BeforeEach
3.  void setup(){
4.       _//建立连接_
5.       jedis = new Jedis("192.169.88.130"，6379)；
6.       _//设置密码_
7.       jedis.auth("123321");
8.       _//选择库_
9.      jedis.select(0);
10. }

测试String,Hash

1.  @Test
2.  void testString(){
3.       _//存入数据_
4.       String result = jedis.set("name","zhangsan");
5.       System.out.println("result=" + result);
6.       _//读取数据_
7.       String name = jedis.get("name");
8.       System.out.println("name = " + name);
9.  }

10. @Test
11. void testHash(){
12.      _//存入数据_
13.      jedis.hset("user:1","zhangsan","Jack");
14.      jedis.hset("user:1","age","21");

15.      _//读取数据_
16.      Map&lt;String,String&gt; map = jedis.hgetAll("user:1");
17.      System.out.println(map);
18. }

释放资源

1.  @AfterEach
2.  void tearDown(){
3.      if(jedis != null){
4.          jedis.close(); 
5.      }  
6.  }

##### Jedis连接池

Jedis本身是线程不安全的，并且频繁的创建和销毁连接会有性能损耗，因此推荐使用Jedis连接池代替Jedis的直连方式

1.  public class JedisConnectionFactory {
2.      private static final JedisPool jedisPool;

3.      static {
4.          _// 配置连接池_
5.          JedisPoolConfig poolConfig = new JedisPoolConfig();
6.          poolConfig.setMaxTotal(8);
7.          poolConfig.setMaxIdle(8);
8.          poolConfig.setMinIdle(0);
9.         poolConfig.setMaxWaitMillis(1000);

10.         _// 创建JedisPool连接池_
11.         jedisPool = new JedisPool(poolConfig,
12.                 "192.168.88.130", 6379, 1000, "123456");
13.     }

14.     public static Jedis getJedis() {
15.         return jedisPool.getResource();
16.     }
17. }

修改建立连接方式

1.      void setup(){
2.          _//建立连接_
3.          _//jedis = new Jedis("192.169.88.130",6379);_
4.          jedis = JedisConnectionFactory.getJedis();
5.          _//设置密码_
6.          jedis.auth("123321");
7.          _//选择库_
8.          jedis.select(0);
9.      }

#### SpringDataRedis

SpringData是Spring中数据操作的模块，包含对各种数据库的集成，其中对redis的集成模块叫做SpringDataRedis，提供了RedisTemplate统一API来操作Redis，支持Redis的发布订阅模型/哨兵和集群，支持基于Lettuce的响应式编程

##### SpringDataRedis快速入门

SpringDataRedis中提供了RedisTemplate工具类，其中封装了各种对Redis的操作，并且将不同数据类型的操作API封装到了不同的类型中

|     |     |     |
| --- | --- | --- |
| **API** | **返回值类型** | **说明** |
| redisTemplate.opsForValue() | ValueOperations | 操作String类型的数据 |
| redisTemplate.opsForHash() | HashOperations | 操作Hash类型数据 |
| redisTemplate.opsForList() | ListOperations | 操作List类型数据 |
| redisTemplate.opsForSet() | SetOperations | 操作Set类型数据 |
| redisTemplate.opsForZSet() | ZSetOperations | 操作SortedSet类型数据 |
| redisTemplate |     | 通用的命令 |

SpringBoot已经提供了对SpringDataRedis的支持，使用非常简单

引入依赖

1.          _&lt;!--redis依赖--&gt;_
2.          &lt;dependency&gt;
3.              &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
4.              &lt;artifactId&gt;spring-boot-starter-data-redis&lt;/artifactId&gt;
5.          &lt;/dependency&gt;
6.          _&lt;!--common-pool--&gt;_
7.          &lt;dependency&gt;
8.              &lt;groupId&gt;org.apache.commons&lt;/groupId&gt;
9.              &lt;artifactId&gt;commons-pool2&lt;/artifactId&gt;
10.         &lt;/dependency&gt;

配置文件 application.yaml

1.  spring:
2.    redis:
3.      host: 192.168.150.101
4.      port: 6379
5.      password: 123321
6.      lettuce:
7.        pool:
8.          max-active: 8
9.          max-idle: 8
10.         min-idle: 0
11.         max-wait: 100ms

注入RedisTemplate

1.  @SpringBootTest
2.  class RedisDemoApplicationTests {

3.      @Autowired
4.      private RedisTemplate&lt;String,Object&gt; redisTemplate;
5.  }

编写测试

1.   @Test
2.      void testString() {
3.          _// 写入一条String数据_
4.          redisTemplate.opsForValue().set("name", "虎哥");
5.          _// 获取string数据_
6.          Object name = redisTemplate.opsForValue().get("name");
7.          System.out.println("name = " + name);
8.      }

9.     @Test
10.     void testSaveUser() {
11.         _// 写入数据_
12.         redisTemplate.opsForValue().set("user:100", new User("虎哥", 21));
13.         _// 获取数据_
14.         User o = (User) redisTemplate.opsForValue().get("user:100");
15.         System.out.println("o = " + o);
16.     }

RedisTemplate可以接收Object作为值，只不过写入前会把Object序列化为字节形式，默认是采用JDK序列化（虎哥会乱码），造成可读性差，内存占用较大

##### 自定义RedisTemplate

可以自定义RedisTemplate的序列化方式，使用json序列化

RedisConfig

1.  @Configuration
2.  public class RedisConfig {

3.      @Bean
4.      public RedisTemplate&lt;String, Object&gt; redisTemplate(RedisConnectionFactory connectionFactory){
5.          _// 创建RedisTemplate对象_
6.          RedisTemplate&lt;String, Object&gt; template = new RedisTemplate<>();
7.          _// 设置连接工厂_
8.          template.setConnectionFactory(connectionFactory);
9.         _// 创建JSON序列化工具_
10.         GenericJackson2JsonRedisSerializer jsonRedisSerializer = new GenericJackson2JsonRedisSerializer();
11.         _// 设置Key的序列化_
12.         template.setKeySerializer(RedisSerializer.string());
13.         template.setHashKeySerializer(RedisSerializer.string());
14.         _// 设置Value的序列化_
15.         template.setValueSerializer(jsonRedisSerializer);
16.         template.setHashValueSerializer(jsonRedisSerializer);
17.         _// 返回_
18.         return template;
19.     }
20. }

尽管json的序列化方式可以满足我们的要求，但依然存在一些问题，为了在反序列化时知道对象的类型，json序列化器会将类的class类型写入json结果中，存入Redis，会带来额外的内存开销

为了节省内存空间，我们并不会使用JSON序列化器来处理Value，而是统一使用String序列化器，要求只能存储String类型的key和value，当需要存储Java对象时，手动完成对象的序列化和反序列化

Spring默认提供了一个StringRedisTemplate类，它的key和value的序列化默认就是String方式，省去自定义RedisTemplate的过程（需要手动完成对象的序列化与反序列化）

1.  @SpringBootTest
2.  class RedisStringTests {

3.      @Autowired
4.      private StringRedisTemplate stringRedisTemplate;
5.      @Test
6.      void testString() {
7.          _// 写入一条String数据_
8.          stringRedisTemplate.opsForValue().set("verify:phone:13600527634", "124143");
9.         _// 获取string数据_
10.         Object name = stringRedisTemplate.opsForValue().get("name");
11.         System.out.println("name = " + name);
12.     }

13.     private static final ObjectMapper mapper = new ObjectMapper();

14.     @Test
15.     void testSaveUser() throws JsonProcessingException {
16.         _// 创建对象_
17.         User user = new User("虎哥", 21);
18.         _// 手动序列化_
19.         String json = mapper.writeValueAsString(user);
20.         _// 写入数据_
21.         stringRedisTemplate.opsForValue().set("user:200", json);

22.         _// 获取数据_
23.         String jsonUser = stringRedisTemplate.opsForValue().get("user:200");
24.         _// 手动反序列化_
25.         User user1 = mapper.readValue(jsonUser, User.class);
26.         System.out.println("user1 = " + user1);
27.     }

28.     @Test
29.     void testHash() {
30.         stringRedisTemplate.opsForHash().put("user:400", "name", "虎哥");
31.         stringRedisTemplate.opsForHash().put("user:400", "age", "21");

32.         Map&lt;Object, Object&gt; entries = stringRedisTemplate.opsForHash().entries("user:400");
33.         System.out.println("entries = " + entries);
34.     }

35.     @Test
36.     void name() {
37.     }
38. }

## 实战篇-黑马点评

注：redis客户机开机时候输入

redis-cli -h 192.168.88.130 -p 6379 -a 050606

config set requirepass ''

### 短信登录

Redis的共享session应用

#### 导入黑马点评项目

用户表/用户详情表/商户信息表/商户类型表/用户日记表/用户关注表/优惠券表/优惠券的订单表

导入项目源码，修改application.yaml中的mysql redis等地址信息

启动项目后在浏览器中访问[localhost:8081/shop-type/list](http://localhost:8081/shop-type/list)，如果可以看到数据则证明运行没有问题

运行前端项目

在nginx所在目录下打开一个CMD窗口，输入命令：

Start nginx.exe

打开chrome浏览器，在空白页面点击鼠标右键选择检查-打开开发者工具：打开手机模式：访问localhost:8080即可看到页面，且可以看到前后端已经实现通信

#### 基于Session实现登录

##### 发送短信验证码

请求方式：POST

请求路径：/user/code

请求参数：phone，电话号码

返回值：无

UserController

1.      @PostMapping("code")
2.      public Result sendCode(@RequestParam("phone") String phone, HttpSession session) {
3.          _// 发送短信验证码并保存验证码_
4.          return userService.sendCode(phone, session);
5.      }

控制层发送验证码并保存验证码

IUserService

1.  public interface IUserService extends IService&lt;User&gt; {

2.      Result sendCode(String phone, HttpSession session);
3.  }

实现类：

UserServiceImpl

1.      @Override
2.      public Result sendCode(String phone, HttpSession session) {
3.          _//1.校验手机号_
4.          if (RegexUtils.isPhoneInvalid(phone)) {
5.              _//2.如果不符合，返回错误信息_
6.              return Result.fail("手机号格式错误！");
7.          }
8.          _//3.符合，生成验证码_
9.          String code = RandomUtil.randomNumbers(6);

10.         _//4.保存验证码到session_
11.         session.setAttribute("code", code);
12.         _//5.发送验证码_
13.         log.debug("发送验证码成功，验证码：{}", code);
14.         _//返回ok_
15.         return Result.ok();
16.     }
17. }

##### 短信验证码登录注册

UserController

1.      _/\*\*_
2.       \* 登录功能
3.       \* @param loginForm 登录参数，包含手机号、验证码；或者手机号、密码
4.       \*/
5.      @PostMapping("/login")
6.      public Result login(@RequestBody LoginFormDTO loginForm, HttpSession session){
7.          _// 实现登录功能_
8.          return userService.login(loginForm , session);
9.      }

IUserService

1.  Result login(LoginFormDTO loginForm, HttpSession session);

UserServiceImpl

1.      @Override
2.      public Result login(LoginFormDTO loginForm, HttpSession session) {
3.          _//1.校验手机号_
4.          String phone = loginForm.getPhone();
5.          if (RegexUtils.isPhoneInvalid(phone)) {
6.              _//如果不符合，返回错误信息_
7.              return Result.fail("手机号格式错误！");
8.          }
9.          _//2.校验验证码_
10.         Object cacheCode = session.getAttribute("code");
11.         String code = loginForm.getCode();
12.         if (cacheCode == null || !cacheCode.toString().equals(code)) {
13.             _//3.不一致，报错_
14.             return Result.fail("验证码错误");
15.         }

16.         _//4.一致，根据手机号查询用户 select \* from user where phone = ?_
17.         User user = query().eq("phone", phone).one();

18.         _//5.判断用户是否存在_
19.         if (user == null) {
20.             _//6.不存在创建新用户并保存_
21.             user = createUserWithPhone(phone);
22.         }

23.         _//7.保存用户信息到session中_
24.         session.setAttribute("user", NamedObject.user);
25.         return null;
26.     }

27.     private User createUserWithPhone(String phone) {
28.         _//1.创建用户_
29.         User user = new User();
30.         user.setPhone(phone);
31.         user.setNickName(USER_NICK_NAME_PREFIX + RandomUtil.randomString(10));
32.         _//2.保存用户_
33.         save(user);
34.         return user;
35.     }

##### 登录校验功能

由于多个控制器需要校验的登录状态，所以可以将其写到拦截器中

LoginInterceptor

1.  public class LoginInterceptor implements HandlerInterceptor {

2.      @Override
3.      public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
4.          _//1.获取session_
5.          HttpSession session = request.getSession();
6.          _//2.获取session中的用户_
7.          Object user = session.getAttribute("user");
8.          _//3.判断用户是否存在_
9.         if (user == null) {
10.             _//4.不存在，拦截_
11.             response.setStatus(401);
12.             return false;
13.         }
14.         _//5.存在，保存用户信息到ThreadLocal_
15.         UserHolder.saveUser((UserDTO) user);
16.         _//6.放行_
17.         return true;

18.     }

19.     @Override
20.     public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
21.         UserHolder.removeUser();
22.     }
23. }

MvcConfig 配置拦截器的拦截对象

1.  @Configuration
2.  public class MvcConfig implements WebMvcConfigurer {

3.      @Override
4.      public void addInterceptors(InterceptorRegistry registry) {
5.          registry.addInterceptor(new LoginInterceptor())
6.                  .excludePathPatterns(
7.                          "/user/code",
8.                          "/user/login",
9.                         "/blog/hot",
10.                         "/shop/\*\*",
11.                         "/shop-type/\*\*",
12.                         "/upload/\*\*",
13.                         "/voucher/\*\*"
14.                 );
15.     }
16. }

UserController 实现返回主页

1.      @GetMapping("/me")
2.      public Result me(){
3.          _// 获取当前登录的用户并返回_
4.          UserDTO user = UserHolder.getUser();
5.          return Result.ok(user);
6.      }

##### UserDTO实现用户敏感信息隐藏

1.  @Data
2.  public class UserDTO {
3.      private Long id;
4.      private String nickName;
5.      private String icon;
6.  }

UserServiceImpl 修改 对保存到session中的内容进行隐藏

1.      @Override
2.      public Result login(LoginFormDTO loginForm, HttpSession session) {
3.  ...
4.          _//7.保存用户信息到session中_
5.          session.setAttribute("user", BeanUtil.copyProperties(user, UserDTO.class));
6.          return Result.ok();
7.      }

#### 集群的Session共享问题

多台Tomcat并不共享session存储空间，当要求切换到不同tomcat服务时导致数据丢失的问题

Session的替代方案应该满足：数据共享，内存存储，key/value结构

#### 基于Redis实现共享session登录

校验登录状态：LoginInterceptor

短信验证码登录，注册:UserServiceImpl

不可以 以code作为key，是因为每个用户浏览器都有不同的session，存储本地，不会互相干扰，但是redis是共享机制，存储服务器，可能会覆盖，所以以phone作为key，以手机号为key读取验证码

Uuid生成随机字符串token，存储用户信息，登录注册返回token给客户端，然后校验登录状态的时候请求并携带token 携带用户信息（鉴权） 前端将token写入authorization头中，如果直接将手机号作为键值保存在前端可能有泄露风险

登录拦截校验

UserServiceImpl

1.  @Slf4j
2.  @Service
3.  public class UserServiceImpl extends ServiceImpl&lt;UserMapper, User&gt; implements IUserService {

4.      @Resource
5.      private StringRedisTemplate stringRedisTemplate;

6.      @Override
7.      public Result sendCode(String phone, HttpSession session) {
8.         _//1.校验手机号_
9.         if (RegexUtils.isPhoneInvalid(phone)) {
10.             _//2.如果不符合，返回错误信息_
11.             return Result.fail("手机号格式错误！");
12.         }
13.         _//3.符合，生成验证码_
14.         String code = RandomUtil.randomNumbers(6);

15.         _//4.保存验证码到redis_
16.         stringRedisTemplate.opsForValue().set(LOGIN_CODE_KEY + phone, code,LOGIN_CODE_TTL, TimeUnit.MINUTES);

17.         _//5.发送验证码_
18.         log.debug("发送验证码成功，验证码：{}", code);
19.         _//返回ok_
20.         return Result.ok();
21.     }
22.     @Override
23.     public Result login(LoginFormDTO loginForm, HttpSession session) {
24.         _//1.校验手机号_
25.         String phone = loginForm.getPhone();
26.         if (RegexUtils.isPhoneInvalid(phone)) {
27.             _//如果不符合，返回错误信息_
28.             return Result.fail("手机号格式错误！");
29.         }
30.         _//2.从Redis中获取验证码并校验_
31.         String cacheCode = stringRedisTemplate.opsForValue().get(LOGIN_CODE_KEY + phone);
32.         String code = loginForm.getCode();
33.         if (cacheCode == null || !cacheCode.equals(code)) {
34.             _//3.不一致，报错_
35.             return Result.fail("验证码错误");
36.         }

37.         _//4.一致，根据手机号查询用户 select \* from user where phone = ?_
38.         User user = query().eq("phone", phone).one();

39.         _//5.判断用户是否存在_
40.         if (user == null) {
41.             _//6.不存在创建新用户并保存_
42.             user = createUserWithPhone(phone);
43.         }

44.         _//7.保存用户信息到Redis中_
45.         _//7.1.随机生成token，作为登录令牌_
46.         String token = UUID.randomUUID().toString(true);
47.         _//7.2.将User对象转为HashMap存储_
48.         UserDTO userDTO = BeanUtil.copyProperties(user, UserDTO.class);
49.         Map&lt;String, Object&gt; userMap = BeanUtil.beanToMap(userDTO, new HashMap<>(),
50.                 CopyOptions.create()
51.                         .setIgnoreNullValue(true)
52.                         .setFieldValueEditor((fieldName,fieldValue) -> fieldValue.toString()));
53.         _//7.3.存储_
54.         String tokenKey = LOGIN_USER_KEY + token;
55.         stringRedisTemplate.opsForHash().putAll(tokenKey, userMap);
56.         stringRedisTemplate.expire(tokenKey , LOGIN_USER_TTL, TimeUnit.MINUTES);

57.         _//8.返回token_
58.         return Result.ok(token);
59.     }

LoginInterceptor

该系统采用无状态的Token认证机制，使用Redis作为用户会话存储，替代传统的Session机制。

核心流程1. 发送验证码流程：首先验证手机号格式是否正确，生成6位随机数字验证码

将验证码以"login:code:{手机号}"为键存储到Redis中，设置5分钟过期时间，记录日志并返回成功状态 2. 用户登录流程：验证手机号格式，从Redis中获取之前发送的验证码进行比对，验证码正确后，查询数据库中该手机号对应的用户，如果用户不存在，则自动创建新用户（设置默认昵称），生成唯一的UUID作为登录Token，将用户信息转换为Map结构，存储到Redis中，键为"login:token:{token}"设置Token过期时间（30分钟），实现自动登录超时，返回Token给前端用于后续身份认证

1.  public class LoginInterceptor implements HandlerInterceptor {

2.      private StringRedisTemplate stringRedisTemplate;

3.      public LoginInterceptor(StringRedisTemplate stringRedisTemplate) {
4.          this.stringRedisTemplate = stringRedisTemplate;
5.      }

6.      @Override
7.     public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
8.         _//1.获取请求头中的token_
9.         String token = request.getHeader("authorization");
10.         if(StrUtil.isBlank(token)){
11.             _//不存在拦截，返回401状态码_
12.             response.setStatus(401);
13.             return false;
14.         }
15.         _//2.基于TOKEN获取Redis中的用户_
16.         String key = RedisConstants.LOGIN_USER_KEY + token;
17.         Map&lt;Object, Object&gt; userMap = stringRedisTemplate.opsForHash()
18.                 .entries(key);
19.         _//3.判断用户是否存在_
20.         if (userMap.isEmpty()) {
21.             _//4.不存在，拦截_
22.             response.setStatus(401);
23.             return false;
24.         }
25.         _//5.将查询到的Hash数据转为UserDTO对象_
26.         UserDTO userDTO = BeanUtil.fillBeanWithMap(userMap, new UserDTO(), false);

27.         _//6..存在，保存用户信息到ThreadLocal_
28.         UserHolder.saveUser(userDTO);

29.         _//7.刷新token有效期_
30.         stringRedisTemplate.expire(key, RedisConstants.LOGIN_USER_TTL, TimeUnit.MINUTES);

31.         _//8.放行_
32.         return true;

33.     }

34.      @Override
35.      public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
36.          UserHolder.removeUser();
37.  }
38.  }

这段代码实现了一个登录拦截器，这里不能使用resouce的方式注入，是因为这个类不是有spring创建的对象，用于验证用户身份并管理用户会话状态。该拦截器基于Token机制实现用户身份验证，通过Redis存储用户信息，使用ThreadLocal保存当前线程的用户数据。主要作用是查询redis用户是否还活跃

请求拦截验证

\- 从HTTP请求头中获取"authorization"字段作为Token

\- 如果Token为空或不存在，直接返回401未授权状态码，拒绝访问

\- 使用Token拼接Redis键前缀，构建完整的Redis键

Redis用户信息查询

\- 使用Redis的Hash数据结构查询用户信息

\- 通过\`opsForHash().entries(key)\`获取存储在Redis中的用户数据Map

\- 如果查询结果为空，说明Token无效或已过期，返回401状态码

用户信息处理

\- 使用Hutool工具的方法将Redis中存储的Map数据转换为UserDTO对象

\- 将转换后的用户信息保存到ThreadLocal中，供当前请求线程随时获取用户信息

会话有效期管理

\- 每次成功验证后，刷新Token在Redis中的过期时间

\- 通过\`expire()\`方法重新设置Redis键的生存时间，实现会话续期功能

资源清理

\- 在请求处理完成后，通过方法清理ThreadLocal中的用户信息

\- 避免内存泄漏，确保线程安全

#### 登录拦截器的优化

现在拦截器作用（获取token，查询Redis的用户不存在则拦截，存在则继续，保存到ThreadLocal，刷新token有效期）的位置是需要登陆的路径，但是如果用户访问的是不需要登录的路径，那么拦截器不会成功拦截，在这之前在嵌套一个拦截一切路径的拦截器完成（获取token，查询redis用户，保存到ThreadLocal，刷新token有效期，放行），第二个拦截器（原来的拦截器）的功能变成了查询Threadlocal的用户，不存在则拦截，存在则继续

RefreshTokenInterceptor 负责拦截全部

1.  public class RefreshTokenInterceptor implements HandlerInterceptor {

2.      private StringRedisTemplate stringRedisTemplate;

3.      public RefreshTokenInterceptor(StringRedisTemplate stringRedisTemplate) {
4.          this.stringRedisTemplate = stringRedisTemplate;
5.      }

6.      @Override
7.     public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
8.         _// 1.获取请求头中的token_
9.         String token = request.getHeader("authorization");
10.         if (StrUtil.isBlank(token)) {
11.             return true;
12.         }
13.         _// 2.基于TOKEN获取redis中的用户_
14.         String key  = LOGIN_USER_KEY + token;
15.         Map&lt;Object, Object&gt; userMap = stringRedisTemplate.opsForHash().entries(key);
16.         _// 3.判断用户是否存在_
17.         if (userMap.isEmpty()) {
18.             return true;
19.         }
20.         _// 5.将查询到的hash数据转为UserDTO_
21.         UserDTO userDTO = BeanUtil.fillBeanWithMap(userMap, new UserDTO(), false);
22.         _// 6.存在，保存用户信息到 ThreadLocal_
23.         UserHolder.saveUser(userDTO);
24.         _// 7.刷新token有效期_
25.         stringRedisTemplate.expire(key, LOGIN_USER_TTL, TimeUnit.MINUTES);
26.         _// 8.放行_
27.         return true;
28.     }

29.     @Override
30.     public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
31.         _// 移除用户_
32.         UserHolder.removeUser();
33.     }
34. }

LoginInterceptor

1.  public class LoginInterceptor implements HandlerInterceptor {

2.      @Override
3.      public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
4.          _// 1.判断是否需要拦截（ThreadLocal中是否有用户）_
5.          if (UserHolder.getUser() == null) {
6.              _// 没有，需要拦截，设置状态码_
7.              response.setStatus(401);
8.              _// 拦截_
9.             return false;
10.         }
11.         _// 有用户，则放行_
12.         return true;
13.     }
14. }

判断ThreadLocal中是否有用户

MvcConfig

1.  @Configuration
2.  public class MvcConfig implements WebMvcConfigurer {

3.      @Resource
4.      private StringRedisTemplate stringRedisTemplate;

5.      @Override
6.      public void addInterceptors(InterceptorRegistry registry) {
7.          _// 登录拦截器_
8.         registry.addInterceptor(new LoginInterceptor())
9.                 .excludePathPatterns(
10.                         "/user/code",
11.                         "/user/login",
12.                         "/blog/hot",
13.                         "/shop/\*\*",
14.                         "/shop-type/\*\*",
15.                         "/upload/\*\*",
16.                         "/voucher/\*\*"
17.                 ).order(1);
18.         _// token刷新的拦截器_
19.         registry.addInterceptor(new RefreshTokenInterceptor(stringRedisTemplate)).addPathPatterns("/\*\*").order(0);
20.     }
21. }

配置token，使用.order配置顺序

### 商户查询缓存

企业的缓存使用技巧，缓存雪崩，穿透等问题解决

#### 缓存概念

- 缓存就是数据交换的缓冲区（cache），是存贮数据的临时地方，一般读写性能较高
- 浏览器缓存-应用层缓存-数据层缓存-CPU缓存-磁盘缓存
- 缓存的作用-降低后端负载，提高读写效率，降低响应时间，应对高并发问题
- 缓存的成本-数据一致性成本，代码维护成本，运维成本

#### 添加Redis缓存

ShopController

1.      _/\*\*_
2.       \* 根据id查询商铺信息
3.       \* @param id 商铺id
4.       \* @return 商铺详情数据
5.       \*/
6.      @GetMapping("/{id}")
7.      public Result queryShopById(@PathVariable("id") Long id) {
8.          return shopService.queryById(id);
9.      }

IShopService

1.  public interface IShopService extends IService&lt;Shop&gt; {
2.      Result queryById(Long id);
3.  }

ShopServiceImpl

1.  @Service
2.  public class ShopServiceImpl extends ServiceImpl&lt;ShopMapper, Shop&gt; implements IShopService {

3.      @Resource
4.      private StringRedisTemplate stringRedisTemplate;

5.      @Override
6.      public Result queryById(Long id) {
7.          String key = CACHE_SHOP_KEY + id;
8.         _//1.从redis查询商铺缓存_
9.         String shopJson = stringRedisTemplate.opsForValue().get(CACHE_SHOP_KEY+ id);
10.         _//2.判断是否存在_
11.         if (StrUtil.isNotBlank(shopJson)) {
12.             _//3.存在，返回_
13.             Shop shop = JSONUtil.toBean(shopJson, Shop.class);
14.             return Result.ok(shop);
15.         }
16.         _//4.不存在，根据id查询数据库_
17.         Shop shop = getById(id);
18.         _//5.不存在，返回错误_
19.         if (shop == null) {
20.             return Result.fail("店铺不存在");
21.         }
22.         _//6.存在，写入redis_
23.         stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(shop));
24.         _//7.返回_
25.         return Result.ok(shop);
26.     }
27. }

类型转换：这是因为Redis只能存储字符串类型的数据，而我们的应用程序需要使用Java对象。

#### 缓存更新策略

|     |     |     |     |
| --- | --- | --- | --- |
|     | 内存淘汰 | 超时剔除 | 主动更新 |
| 说明  | 不用自己维护，利用redis的内存淘汰机制，当内存不足时自动淘汰部分数据，下次查询时更新缓存 | 给缓存数据添加TTL时间，到期后自动删除缓存，下次查询时更新缓存 | 编写业务逻辑，在修改数据库的同时更新缓存 |
| 一致性 | 差   | 一般  | 好   |
| 维护成本 | 无   | 低   | 高   |

业务场景：

低一致性需求：存在内存淘汰机制，例如店铺类型的查询缓存

高一致性需求：主动更新，并以超时剔除作为兜底方案，例如店铺详情查询的缓存

##### 主动更新策略

Cache Aside Pattern-由缓存的调用者，在更新数据库的同时更新缓存

Read/write Through Pattern 缓存与数据库整合为一个服务，由服务来维持一致性，调用者调用该服务，无需关心缓存一致性问题

Write Behind Caching Pattern 调用者只操作缓存，由其他线程异步的将缓存数据持久化到数据库，保证最终一致

一般偏向于先操作数据库，再删除缓存

##### 缓存更新策略的最佳方案

- 低一致性需求：使用Redis自带的内存淘汰机制
- 高一致性需求：主动更新，并以超时剔除作为兜底方案
- 读操作：
- 缓存命中则返回
- 缓存未命中则查询数据库，并写入缓存，设定超时时间
- 写操作：
- 先写数据库，然后再删除缓存
- 要确保数据库与缓存操作的原子性

##### 给查询商铺的缓存添加超时剔除和主动更新的策略

修改ShopController中的业务逻辑，满足下面要求：

- 根据id查询店铺时，如果缓存未命中，则查询数据库，将数据库结果写入缓存，并设置超时时间
- 根据id修改店铺时，先修改数据库，再删除缓存

#### 缓存穿透

缓存穿透是指客户端请求的数据在缓存中和数据库中都不存在，这样缓存永远不会生效，这些请求都会打到数据库，常见的解决方案有两种：

缓存空对象（实现简单，维护方便，额外的内存消耗（设置短ttl），可能造成短期的不一致）布隆过滤（在客户端和redis之间加入布隆过滤器，先请求布隆过滤器，不存在则拒绝）

|

内存占用较少，没有多余key

实现复杂，存在误判可能

##### 使用缓存空对象

1.      @Override
2.      public Result queryById(Long id) {
3.          String key = CACHE_SHOP_KEY + id;
4.          _//1.从redis查询商铺缓存_
5.          String shopJson = stringRedisTemplate.opsForValue().get(key);
6.          _//2.判断是否存在_
7.          if (StrUtil.isNotBlank(shopJson)) {
8.              _//3.存在，返回_
9.              Shop shop = JSONUtil.toBean(shopJson, Shop.class);
10.             return Result.ok(shop);
11.         }
12.         _//判断命中的是否是空值_
13.         if (shopJson != null){
14.             _//返回错误信息_
15.             return Result.fail("店铺不存在");
16.         }
17.         _//4.不存在，根据id查询数据库_
18.         Shop shop = getById(id);
19.         _//5.不存在，返回错误_
20.         if (shop == null) {
21.             _//将空值写入redis中_
22.             stringRedisTemplate.opsForValue().set(key,"",CACHE_NULL_TTL, TimeUnit.MINUTES);
23.             return Result.fail("店铺不存在");
24.         }
25.         _//6.存在，写入redis_
26.         stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(shop),CACHE_SHOP_TTL, TimeUnit.MINUTES);
27.         _//7.返回_
28.         return Result.ok(shop);
29.     }

StrUtil.isNotBlank(shopJson):

当 shopJson 为 null 时，返回 false

当 shopJson 为 "" (空字符串) 时，返回 false

当 shopJson 为有效的JSON字符串时，返回 true

shopJson != null:

当 shopJson 不为 null 时（即为 "" 空字符串），说明这是之前缓存的"不存在"标记

当 shopJson 为 null 时，说明Redis中没有这个键

#### 缓存雪崩

- 缓存雪崩是指同一时段大量的缓存key同时失效或者redis服务宕机，导致大量请求到达数据库，带来巨大压力

- 解决方案：
- 给不同的key的TTL添加随机值
- 利用redis集群提高服务的可用性
- 给缓存业务添加降级限流策略
- 给业务添加多级缓存

#### 缓存击穿

缓存击穿问题也叫热点key问题，就是一个被高并发访问并且缓存重建业务较复杂的key突然失效了，无效的请求访问会在瞬间给数据库带来巨大的冲击

常见解决方案：

互斥锁

没有额外的内存消耗，保证一致性，实现简单

线程需要等待，性能受影响，可能有死锁风险

逻辑过期

线程无需等待，性能较好

不保证一致性，有额外内存消耗，实现复杂

##### 基于互斥锁方式解决缓存击穿问题

需求：修改根据id查询商铺的业务，基于互斥锁方式来解决缓存击穿问题

1.  @Override
2.      public Result queryById(Long id) {
3.          _//缓存穿透_
4.          _//Shop shop = queryWithPassThrough(id);_

5.          _//互斥锁解决缓存击穿_
6.          Shop shop = queryWithMutex(id);
7.          if (shop == null) {
8.              return Result.fail("店铺不存在");
9.         }
10.         _//返回_
11.         return Result.ok(shop);
12.     }
13.     public Shop queryWithMutex(Long id){
14.         String key = CACHE_SHOP_KEY + id;
15.         _//1.从redis查询商铺缓存_
16.         String shopJson = stringRedisTemplate.opsForValue().get(key);
17.         _//2.判断是否存在_
18.         if (StrUtil.isNotBlank(shopJson)) {
19.             _//3.存在，返回_
20.             Shop shop = JSONUtil.toBean(shopJson, Shop.class);
21.             return shop;
22.         }
23.         _//判断命中的是否是空值_
24.         if (shopJson != null){
25.             _//返回错误信息_
26.             return null;
27.         }

28.         _//4.实现缓存重建_
29.         _//4.1获取互斥锁_
30.         String lockKey = "lock:shop:" + id;
31.         Shop shop = null;
32.         try {
33.             boolean isLock = tryLock(lockKey);
34.             _//4.2判断是否获取成功_
35.             if(!isLock){
36.                 _//4.3失败，则休眠并重试_
37.                 Thread.sleep(50);
38.                 return queryWithMutex(id);
39.             }
40.             _//4.4成功，根据id查询数据库_
41.             shop = getById(id);
42.             _//模拟重建的延迟_
43.             Thread.sleep(200);
44.             _//5.不存在，返回错误_
45.             if (shop == null) {
46.                 _//将空值写入redis中_
47.                 stringRedisTemplate.opsForValue().set(key,"",CACHE_NULL_TTL, TimeUnit.MINUTES);
48.                 return null;
49.             }
50.             _//6.存在，写入redis_
51.             stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(shop),CACHE_SHOP_TTL, TimeUnit.MINUTES);
52.         } catch (InterruptedException e) {
53.             throw new RuntimeException(e);
54.         }finally {
55.             _//7.释放互斥锁_
56.             unLock(lockKey);
57.         }
58.         _//8返回_
59.         return shop;
60.     }

这种机制确保了在高并发场景下，当缓存失效时只有一个线程去查询数据库并重建缓存，其他线程等待后直接从缓存获取数据，有效防止了缓存击穿问题。

先从Redis查询缓存，如果有有效数据则直接返回，如果是空值（之前查询过但不存在）则返回null，锁键生成：为每个店铺ID创建唯一的锁键 "lock:shop:" + id，获取锁：使用 tryLock(lockKey) 尝试获取锁，获取失败处理：如果获取锁失败，线程休眠50ms后递归重试，查询数据库获取店铺信息，如果不存在，写入空值到Redis防止穿透，如果存在，将数据写入Redis缓存，无论操作成功与否，在finally块中都会释放锁，确保不会出现死锁。

##### 基于逻辑过期方式解决缓存击穿问题

逻辑过期不是真正意义上的物理过期，所以保存到redis中的数据会永久有效。通过程序员手动的删除来取消，所以要进行缓存预热热点数据

需求：修稿根据id查询商铺的业务，基于逻辑过期方式来解决缓存击穿问题

1.      public void saveShop2Redis(Long id, Long expireSeconds) throws InterruptedException {
2.          _//1.查询店铺数据_
3.          Shop shop = getById(id);
4.          Thread.sleep(200);
5.          _//2.封装成逻辑过期_
6.          RedisData redisData = new RedisData();
7.          redisData.setData(shop);
8.          redisData.setExpireTime(LocalDateTime.now().plusSeconds(expireSeconds));
9.          _//3.写入Redis_
10.         stringRedisTemplate.opsForValue().set(CACHE_SHOP_KEY + id, JSONUtil.toJsonStr(redisData));
11.     }

12.      public Shop queryWithLogicalExpire(Long id){
13.          String key = CACHE_SHOP_KEY + id;
14.          _//1.从redis查询商铺缓存_
15.          String shopJson = stringRedisTemplate.opsForValue().get(key);
16.          _//2.判断是否存在_
17.          if (StrUtil.isBlank(shopJson)) {
18.              _//3.存在，返回_
19.              return null;
20.          }
21.         _//命中，需要先把json反序列化为对象_
22.         RedisData redisData = JSONUtil.toBean(shopJson, RedisData.class);
23.         JSONObject data = (JSONObject) redisData.getData();
24.         Shop shop = JSONUtil.toBean(data, Shop.class);
25.         LocalDateTime expireTime = redisData.getExpireTime();

26.         _//5.判断是否过期_
27.         if(expireTime.isAfter(LocalDateTime.now())){
28.             _//5.1未过期，直接返回店铺信息_
29.             return shop;
30.         }

31.         _//5.2已过期，需要缓存重建_
32.         _//6.缓存重建_
33.         _//6.1获取互斥锁_
34.         String lockKey = LOCK_SHOP_KEY + id;
35.         boolean isLock = tryLock(lockKey);
36.         _//6.2判断是否获取锁成功_
37.         if (isLock) {
38.             _//6.3成功，开启独立线程，实现缓存重建_
39.             CACHE_REBUILD_EXECUTOR.submit(() -> {
40.                 try {
41.                     this.saveShop2Redis(id, 20L);
42.                 } catch (Exception e) {
43.                     throw new RuntimeException(e);
44.                 } finally {
45.                     _//释放锁_
46.                     unLock(lockKey);
47.                 }
48.             });
49.         }

50.         _//6.4返回商铺信息_
51.         return shop;
52.     }

#### 缓存工具封装

基于StringRedisTemplate封装一个缓存工具类，满足下列需求：

将任意java对象序列化为json并存储在string类型的key中，并且可以设置TTL过期时间

将任意java对象序列化为json并存储在string类型的key中，并且可以设置逻辑过期时间，用于处理缓存击穿问题

根据指定的key查询缓存，并反序列化为指定类型，利用缓存空值的方式解决缓存穿透问题

根据指定的key查询缓存，并反序列化为指定类型，需要利用逻辑过期解决缓存击穿问题

使用工具类来封装 使用泛型作为对象

1.  @Component
2.  public class CacheClient {

3.      private StringRedisTemplate stringRedisTemplate;

4.      public CacheClient(StringRedisTemplate stringRedisTemplate) {
5.          this.stringRedisTemplate = stringRedisTemplate;
6.      }

7.     public void set(String key, Object value, Long time, TimeUnit unit) {
8.         stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(value), time, unit);
9.     }

10.     public void setWithLogicalExpire(String key, Object value, Long time, TimeUnit unit) {
11.         _//设置逻辑过期_
12.         RedisData redisData = new RedisData();
13.         redisData.setData(value);
14.         redisData.setExpireTime(LocalDateTime.now().plusSeconds(unit.toSeconds(time)));

15.         _//写入redis_
16.         stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(redisData));
17.     }

18.     public &lt;R,ID&gt; R queryWithPassThrough(String keyPrefix,ID id , Class&lt;R&gt; type, Function&lt;ID,R&gt; dbFallback, Long time, TimeUnit unit){
19.         String key = keyPrefix + id;
20.         _//1.从redis查询商铺缓存_
21.         String json = stringRedisTemplate.opsForValue().get(key);
22.         _//2.判断是否存在_
23.         if (StrUtil.isNotBlank(json)) {
24.             _//3.存在，返回_
25.             Shop shop = JSONUtil.toBean(json, Shop.class);
26.             return JSONUtil.toBean(json,type);
27.         }
28.         _//判断命中的是否是空值_
29.         if (json != null){
30.             _//返回错误信息_
31.             return null;
32.         }
33.         _//4.不存在，根据id查询数据库_
34.         R r = dbFallback.apply(id);
35.         _//5.不存在，返回错误_
36.         if (r == null) {
37.             _//将空值写入redis中_
38.             stringRedisTemplate.opsForValue().set(key,"",CACHE_NULL_TTL, TimeUnit.MINUTES);
39.             return null;
40.         }
41.         _//6.存在，写入redis_
42.         this.set(key, r, time, unit);
43.         _//7.返回_
44.         return r;
45.     }

46.     private static final ExecutorService CACHE_REBUILD_EXECUTOR = Executors.newFixedThreadPool(10);

47.     public &lt;R,ID&gt; R queryWithLogicalExpire(
48.             String keyPrefix,ID id , Class&lt;R&gt; type, Function&lt;ID,R&gt; dbFallback, Long time, TimeUnit unit){
49.         String key = keyPrefix + id;
50.         _//1.从redis查询商铺缓存_
51.         String json = stringRedisTemplate.opsForValue().get(key);
52.         _//2.判断是否存在_
53.         if (StrUtil.isBlank(json)) {
54.             _//3.存在，返回_
55.             return null;
56.         }
57.         _//命中，需要先把json反序列化为对象_
58.         RedisData redisData = JSONUtil.toBean(json, RedisData.class);
59.         JSONObject data = (JSONObject) redisData.getData();
60.         R r = JSONUtil.toBean(data, type);
61.         LocalDateTime expireTime = redisData.getExpireTime();

62.         _//5.判断是否过期_
63.         if(expireTime.isAfter(LocalDateTime.now())){
64.             _//5.1未过期，直接返回店铺信息_
65.             return r;
66.         }

67.         _//5.2已过期，需要缓存重建_
68.         _//6.缓存重建_
69.         _//6.1获取互斥锁_
70.         String lockKey = keyPrefix + id;
71.         boolean isLock = tryLock(lockKey);
72.         _//6.2判断是否获取锁成功_
73.         if (isLock) {
74.             _//6.3成功，开启独立线程，实现缓存重建_
75.             CACHE_REBUILD_EXECUTOR.submit(() -> {
76.                 try {
77.                     _//查询数据库_
78.                     R r1 = dbFallback.apply(id);
79.                     _//写入redis_
80.                     this.set(key, r1, time, unit);
81.                 } catch (Exception e) {
82.                     throw new RuntimeException(e);
83.                 } finally {
84.                     _//释放锁_
85.                     unLock(lockKey);
86.                 }
87.             });
88.         }

100.        _//6.4返回商铺信息_
101.        return r;
102.    }
103.    private boolean tryLock(String key){
104.        Boolean flag = stringRedisTemplate.opsForValue().setIfAbsent(key, "1", 10, TimeUnit.SECONDS);
105.        return BooleanUtil.isTrue(flag);
106.    }

108.    private void unLock(String key){
109.        stringRedisTemplate.delete(key);
110.    }
111.}

### 优惠券秒杀

Redis的计数器，Lua脚本Redis 分布式锁 Redis三种消息队列

#### 全局唯一ID

##### 全局ID生成器

- 每个店铺都可以发布优惠券，当用户抢购时，就会生成订单并保存到tb_voucher_order这张表中，而订单表如果使用数据库自增id就存在一些问题：id的规律性太明显，受单表数据量的限制
- 全局id生成器，是一种在分布式系统下用来全局唯一ID的工具，一般要满足下列特性：

唯一性/高可用/高性能/递增性/安全性

- 为了增强ID的安全性，我们可以不直接使用Redis自增的数值，而是拼接一些其他信息
- 符号位（1bit）+ 时间戳（31bit，以秒为单位） + 序列号（32bit 秒内的计数器）

RedisIdWorker 生成全局唯一ID

1.  @Component
2.  public class RedisIdWorker {
3.      _/\*\*_
4.       \* 开始时间戳
5.       \*/
6.      private static final long BEGIN_TIMESTAMP = 1640995200L;
7.      _/\*\*_
8.       \* 序列号位数
9.       \*/
10.     private static final long COUNT_BITS = 32;

11.     @Resource
12.     private StringRedisTemplate stringRedisTemplate;

13.     public long nextId(String keyPrefix) {
14.         _//1.生成时间戳_
15.         LocalDateTime now = LocalDateTime.now();
16.         long nowSecond = now.toEpochSecond(ZoneOffset.UTC);
17.         long timestamp = nowSecond - BEGIN_TIMESTAMP;

18.         _//2.生成序列号_
19.         _//2.1获取当前日期，精确到天_
20.         String date = now.format(DateTimeFormatter.ofPattern("yyyyMMdd"));
21.         _//2.2.自增长_
22.         long count = stringRedisTemplate.opsForValue().increment("icr:" + keyPrefix + ":"+ date);

23.         _//3.拼接返回_
24.         return timestamp << COUNT_BITS | count ;
25.     }

26. }

#### 实现优惠券秒杀下单

每个店铺都可以发布优惠券，分为平价券和特价券，平价券可以任意购买，而特价券需要秒杀抢购

表关系：tb_voucher 和 tb_voucher_order

##### 准备优惠券秒杀的数据库功能

VoucherServiceImpl

1.  @Service
2.  public class VoucherServiceImpl extends ServiceImpl&lt;VoucherMapper, Voucher&gt; implements IVoucherService {

3.      @Resource
4.      private ISeckillVoucherService seckillVoucherService;

5.      @Override
6.      public Result queryVoucherOfShop(Long shopId) {
7.          _// 查询优惠券信息_
8.         List&lt;Voucher&gt; vouchers = getBaseMapper().queryVoucherOfShop(shopId);
9.         _// 返回结果_
10.         return Result.ok(vouchers);
11.     }

12.     @Override
13.     @Transactional
14.     public void addSeckillVoucher(Voucher voucher) {
15.         _// 保存优惠券_
16.         save(voucher);
17.         _// 保存秒杀信息_
18.         SeckillVoucher seckillVoucher = new SeckillVoucher();
19.         seckillVoucher.setVoucherId(voucher.getId());
20.         seckillVoucher.setStock(voucher.getStock());
21.         seckillVoucher.setBeginTime(voucher.getBeginTime());
22.         seckillVoucher.setEndTime(voucher.getEndTime());
23.         seckillVoucherService.save(seckillVoucher);
24.     }
25. }

Mybatis保存到数据库的一系列逻辑

VoucherController

1.  @RestController
2.  @RequestMapping("/voucher")
3.  public class VoucherController {

4.      @Resource
5.      private IVoucherService voucherService;

6.      _/\*\*_
7.       \* 新增普通券
8.      \* @param voucher 优惠券信息
9.      \* @return 优惠券id
10.      \*/
11.     @PostMapping
12.     public Result addVoucher(@RequestBody Voucher voucher) {
13.         voucherService.save(voucher);
14.         return Result.ok(voucher.getId());
15.     }

16.     _/\*\*_
17.      \* 新增秒杀券
18.      \* @param voucher 优惠券信息，包含秒杀信息
19.      \* @return 优惠券id
20.      \*/
21.     @PostMapping("seckill")
22.     public Result addSeckillVoucher(@RequestBody Voucher voucher) {
23.         voucherService.addSeckillVoucher(voucher);
24.         return Result.ok(voucher.getId());
25.     }

26.     _/\*\*_
27.      \* 查询店铺的优惠券列表
28.      \* @param shopId 店铺id
29.      \* @return 优惠券列表
30.      \*/
31.     @GetMapping("/list/{shopId}")
32.     public Result queryVoucherOfShop(@PathVariable("shopId") Long shopId) {
33.        return voucherService.queryVoucherOfShop(shopId);
34.     }
35. }

##### 实现优惠券秒杀（不涉及redis）

下单时需要判断两点：

秒杀是否开始或结束，如果尚未开始，或已经结束则无法下单

库存是否充足，不足则无法下单

1.  @Service
2.  public class VoucherOrderServiceImpl extends ServiceImpl&lt;VoucherOrderMapper, VoucherOrder&gt; implements IVoucherOrderService {

3.      @Resource
4.      private ISeckillVoucherService seckillVoucherService;

5.      @Resource
6.      private RedisIdWorker redisIdWorker;

7.     @Override
8.     @Transactional
9.     public Result seckillVoucher(Long voucherId) {
10.         _//1.查询优惠券_
11.         SeckillVoucher voucher = seckillVoucherService.getById(voucherId);
12.         _//2.判断秒杀是否开始_
13.         if (voucher.getBeginTime().isAfter(LocalDateTime.now())) {
14.             _//尚未开始_
15.             return Result.fail("秒杀尚未开始!");
16.         }
17.         _//3.判断秒杀是否已经结束_
18.         if(voucher.getEndTime().isBefore(LocalDateTime.now())){
19.             return Result.fail("秒杀已经结束!");
20.         }
21.         _//4.判断库存是否充足_
22.         if (voucher.getStock() < 1) {
23.             _//库存不足_
24.             return Result.fail("库存不足!");
25.         }
26.         _//5.扣减库存_
27.         boolean success = seckillVoucherService.update()
28.                 .setSql("stock = stock - 1")
29.                 .eq("voucher_id", voucherId).update();
30.         if (!success) {
31.             _//扣减库存失败_
32.             return Result.fail("库存不足!");
33.         }
34.         _//6.创建订单_
35.         VoucherOrder voucherOrder = new VoucherOrder();
36.         _//6.1订单id_
37.         long orderId = redisIdWorker.nextId("order");
38.         voucherOrder.setId(orderId);
39.         _//6.2用户id_
40.         Long userId = UserHolder.getUser().getId();
41.         voucherOrder.setUserId(userId);
42.         _//6.3代金券id_
43.         voucherOrder.setVoucherId(voucherId);
44.         save(voucherOrder);

45.         _//7.返回订单id_
46.         return Result.ok(orderId);
47.     }
48. }

通过之前的redisIdWorker来创建id 实现秒杀逻辑

#### 超卖问题

- 超卖问题是典型的多线程安全问题，针对这一问题的常见解决方案就是加锁
- 悲观锁-认为线程安全问题一定会发生，因此在操作数据之前先获取锁，确保线程串行执行
- 乐观锁-认为线程安全问题不一定会发生，因此不加锁，只是在更新数据时去判断有没有其他线程对数据做了修改

如果没有修改则认为自己是安全的，自己才更新数据

如果已经被其它线程修改说明发生了安全问题，此时可以重试或异常

- 乐观锁的关键是判断之前查询得到的数据是否被修改过，常见的方式有两种：
- 版本号法：判断版本号有没有发生变化

- CAS法 compare and set，直接使用stock来判断

1.          //5.扣减库存
2.          boolean success = seckillVoucherService.update()
3.                  .setSql("stock = stock - 1")//set stock = stock - 1
4.                  .eq("voucher_id", voucherId).eq("stock", voucher.getStock())//where id = ? and stock = ?
5.                  .update();

但是失败率高

修改条件使得不用强制匹配stock等于，直接大于stock即可

#### 一人一单

需求：修改秒杀业务，要求同一个优惠券，一个用户只能下一单

1.          //5.一人一单
2.          Long userId = UserHolder.getUser().getId();

3.          //5.1查询订单
4.          int count = query().eq("user_id", userId).eq("voucher_id", voucherId).count();
5.          //5.2判断是否存在
6.          if (count > 0) {
7.              //存在,用户已经购买过了
8.              return Result.fail("用户已经购买过一次!");
9.         }

假设并发情况下数据库中完全没有订单数据，现在有100个订单，都来执行查询逻辑，查的count都是0，都判断不成立，就会连续插入n条数据，但是这里查询新增数据不存在更新判断有无修改的逻辑，无法使用乐观锁，只能加悲观锁，那么将一人一单到扣减库存到创建订单封装成一个方法

1.      @Transactional
2.      public Result createVoucherOrder(Long voucherId) {
3.          //5.一人一单
4.          Long userId = UserHolder.getUser().getId();

5.          //5.1查询订单
6.          int count = query().eq("user_id", userId).eq("voucher_id", voucherId).count();
7.          //5.2判断是否存在
8.          if (count > 0) {
9.             //存在,用户已经购买过了
10.             return Result.fail("用户已经购买过一次!");
11.         }

12.         //6.扣减库存
13.         boolean success = seckillVoucherService.update()
14.                 .setSql("stock = stock - 1")//set stock = stock - 1
15.                 .eq("voucher_id", voucherId).gt("stock", 0)//where id = ? and stock > 0
16.                 .update();
17.         if (!success) {
18.             //扣减库存失败
19.             return Result.fail("库存不足!");
20.         }
21.         //7.创建订单
22.         VoucherOrder voucherOrder = new VoucherOrder();
23.         //7.1订单id
24.         long orderId = redisIdWorker.nextId("order");
25.         voucherOrder.setId(orderId);
26.         //7.2用户id
27.         voucherOrder.setUserId(userId);
28.         //7.3代金券id
29.         voucherOrder.setVoucherId(voucherId);
30.         save(voucherOrder);

31.         //8.返回订单id
32.         return Result.ok(orderId);
33.     }

交给事务管理

1.          synchronized (userId.toString().intern()) {
2.              _//获取代理对象_
3.              IVoucherOrderService proxy = (IVoucherOrderService) AopContext.currentProxy();
4.              return proxy.createVoucherOrder(voucherId);
5.          }

悲观锁的细节：如果锁整个方法createVoucherOrder，来一个用户锁一个用户，性能不好，串行执行，如果锁用户id，满足同一个用户用一把锁，不同用户不加锁，但是当synchronize释放锁，spring提交transaction之间可以有线程进入，同样会出现并发安全问题，于是采用锁返回对象，因为在同一个类中，一个带有 @Transactional 注解的方法（createVoucherOrder）被另一个方法（seckillVoucher）直接调用。由于 Spring 的代理机制，这种“自调用”不会触发事务管理，导致事务失效。所以要获取对应的代理对象，操作pom.xml,HmDianpingApplication, IVoucherOrderService

##### 集群下的线程并发问题

通过加锁可以解决在单机情况下的一人一单安全问题，但是在集群模式下就不行了

如果存在多个JVM，每个JVM内部都有自己的锁，导致每一个锁都可以有一个线程获取，导致并行运行安全问题

解决-让多个JVM都请求同一个锁（分布式锁）

#### 分布式锁-保证同一用户不能同时并发下单

满足分布式系统或集群模式下多进程可见并且互斥的锁

高可用-多进程可见-互斥-高性能-安全性

|     |     |     |     |
| --- | --- | --- | --- |
|     | MySQL | Redis | Zookeeper |
| 互斥  | 利用mysql本身的互斥锁机制 | 利用setnx的互斥命令 | 利用节点的唯一性和有序性实现互斥 |
| 高可用 | 好   | 好   | 好   |
| 高性能 | 一般  | 好   | 一般  |
| 安全性 | 断开连接，自动释放锁 | 利用锁超时时间，到期释放 | 临时节点，断开连接自动释放 |

实现分布式锁时需要实现的两个基本方法：

- 获取锁
- 互斥：确保只能有一个线程获取锁（阻塞式）

SET lock thread1 NX EX 10 （EX设置超时时间 NX是互斥）

\== SETNX lock thread1

EXPIRE lock 10

- 非阻塞：尝试一次，成功返回true，失败返回false（避免死锁）
- 释放锁
- 手动释放（删除锁）
- 超时释放（expire）：获取锁时添加一个超时时间

##### 基于Redis实现分布式锁初级版本

需求：定义一个类，实现接口，利用Redis实现分布式锁功能

1.      @Override
2.      public Result seckillVoucher(Long voucherId) {
3.          _//1.查询优惠券_
4.          SeckillVoucher voucher = seckillVoucherService.getById(voucherId);
5.          _//2.判断秒杀是否开始_
6.          if (voucher.getBeginTime().isAfter(LocalDateTime.now())) {
7.              _//尚未开始_
8.              return Result.fail("秒杀尚未开始!");
9.          }
10.         _//3.判断秒杀是否已经结束_
11.         if(voucher.getEndTime().isBefore(LocalDateTime.now())){
12.             return Result.fail("秒杀已经结束!");
13.         }
14.         _//4.判断库存是否充足_
15.         if (voucher.getStock() < 1) {
16.             _//库存不足_
17.             return Result.fail("库存不足!");
18.         }

19.         Long userId = UserHolder.getUser().getId();
20.         _//创建锁对象_
21.         SimpleRedisLock lock = new SimpleRedisLock("order:" + userId, stringRedisTemplate);
22.         _//获取锁_
23.         boolean isLock = lock.tryLock(1200);
24.         _//判断获取锁成功_
25.         if (!isLock) {
26.             _//获取锁失败，返回错误或重试_
27.             return Result.fail("不允许重复下单!");
28.         }
29.         try {
30.             _//获取代理对象_
31.             IVoucherOrderService proxy = (IVoucherOrderService) AopContext.currentProxy();
32.             _//8.返回订单id_
33.             return proxy.createVoucherOrder(voucherId);
34.         } finally {
35.             _//释放锁_
36.             lock.unLock();
37.         }
38.     }

SimpleRedisLock

1.  public class SimpleRedisLock implements ILock{

2.      private String name;
3.      private StringRedisTemplate stringRedisTemplate;

4.      private static final String KEY_PREFIX = "lock:";

5.      public SimpleRedisLock(String name, StringRedisTemplate stringRedisTemplate) {
6.          this.name = name;
7.         this.stringRedisTemplate = stringRedisTemplate;
8.     }
9.     @Override
10.     public boolean tryLock(long timeoutSec) {
11.         _//获取线程标识_
12.         long threadId = Thread.currentThread().getId();
13.         _// 获取锁_
14.         Boolean success = stringRedisTemplate
15.                 .opsForValue().setIfAbsent(KEY_PREFIX + name, threadId + "", timeoutSec, TimeUnit.SECONDS);
16.         return Boolean.TRUE.equals(success);
17.     }

18.     @Override
19.     public void unLock() {
20.         _//释放锁_
21.         stringRedisTemplate.delete(KEY_PREFIX + name);
22.     }
23. }

测试：

在 VoucherOrderServiceImpl 第 67 行的打断点，使用同一个用户在 postman 中发送秒杀优惠券请求，检查断点返回的 isLock 数据是否相同，正常函数应为一个 true 和另一个 false

在simpleRedisLock中创建tryLock与unLock方法，tryLock中设置锁的键名，使用KEY_PREFIX + name的方式（KEY_PREFIX 为lock：），锁的值是线程id，后面设置锁的过期时间防止死锁，在VoucherOrederServiceImpl中，抛弃之前的Synchronize，创建锁对象，接收name为"order:" + userId，所以锁的key会变成lock：order：userId

##### 基于Redis实现分布式锁，解决锁误删问题

问题：可能在极端情况下出现锁误删的情况

不同JVM中的线程ID可能会重复（线程ID在单个JVM内唯一，但不同机器上的JVM可能有相同的线程ID）

在分布式系统中，多个应用实例可能运行在不同机器上，线程ID可能相同

修改代码使得满足：在获取锁时存入线程标识（可用uuid表示），在释放锁时先获取锁中的线程标示，判断是否与房前线程表示一致，一致则释放锁，不一致则不释放锁

1.      @Override
2.      public boolean tryLock(long timeoutSec) {
3.          _//获取线程标识_
4.          String threadId = ID_PREFIX + Thread.currentThread().getId();
5.          _// 获取锁_
6.          Boolean success = stringRedisTemplate
7.                  .opsForValue().setIfAbsent(KEY_PREFIX + name, threadId , timeoutSec, TimeUnit.SECONDS);
8.          return Boolean.TRUE.equals(success);
9.      }

10.     @Override
11.     public void unLock() {
12.         _//获取线程标识_
13.         String threadId = ID_PREFIX + Thread.currentThread().getId();
14.         _//获取锁中的标识_
15.         String id = stringRedisTemplate.opsForValue().get(KEY_PREFIX + name);
16.         _//判断标识是否一致_
17.         if(threadId.equals(id)){
18.             _//释放锁_
19.             stringRedisTemplate.delete(KEY_PREFIX + name);
20.         }

判断标识

##### Redis的原子性问题

##### Redis的Lua脚本

Redis提供了Lua脚本功能，在一个脚本中编写多条Redis命令，确保多条命令执行时的原子性，Lua是一种编程语言

Redis提供了调用函数 redis call（‘命令名称’,’key’,）

调用脚本的命令：EVAL script numkeys key \[key ...\] arg \[arg ..\]

EVAL “return redis.call(‘set’,’name’,’Jack’)” 0

|

脚本需要的key类型的参数个数

Key类型会放入KEYS数组，其他参数会放入ARGV数组，数组中的起始是从1开始

EVAL “return redis.call(‘set’,KEYS\[1\]’,’ARGV\[1\]’)” 1 name heihei

Lua脚本实现分布式锁的释放锁逻辑

1.  _\--这里的KEYS\[1\]就是锁的key，这里的ARGV就是当前线程标识_
2.  _\--获取锁中的标示，判断与当前线程标识一致_
3.  if (redis,call('GET',KEYS\[1\] == ARGV\[1\])) then
4.    _\--一致，删除锁_
5.    return redis.call('DEL',KEYS\[1\])
6.  end
7.    _\--不一致，则直接返回_
8.  return 0

##### 再次改进Redis的分布式锁

1.      @Override
2.      public void unLock() {
3.          _//调用lua脚本_
4.          stringRedisTemplate.execute(
5.                  UNLOCK_SCRIPT,
6.                  Collections.singletonList(KEY_PREFIX + name),
7.                  ID_PREFIX + Thread.currentThread().getId());
8.      }

9.      private static final DefaultRedisScript&lt;Long&gt; UNLOCK_SCRIPT;
10.      static {
11.          UNLOCK_SCRIPT = new DefaultRedisScript<>();
12.          UNLOCK_SCRIPT.setLocation(new ClassPathResource("unlock.lua"));
13.          UNLOCK_SCRIPT.setResultType(Long.class);
14.      }

调用lua脚本，保证锁不误删，原子性

##### 基于Redis的分布式锁优化

- 基于setnx实现的分布式锁存在下面问题：
- 不可重入：同一个线程无法多次获取同一把锁
- 不可重试：获取锁只尝试一次就返回false，没有重试机制
- 超时释放：锁超时释放虽然可以避免死锁，但如果是业务执行耗时较长，也会导致锁释放，存在安全隐患
- 主从一致性：如果redis提供了主从集群，主从同步存在延迟。当主宕机时如果从同步主中锁数据，则会出现锁实现
- Redisson

redisson是一个在Redis的基础上实现的Java主内存数据网格，开源框架，它不仅提供了一系列分布式的Java对象，还提供了许多分布式服务，其中就包含了各种分布式锁的实现，可重入锁，公平锁，联锁，红锁，读写锁

##### Redisson优化

引入依赖

配置redisson客户端

使用redisson的分布式锁

1.          _//创建锁对象_
2.  _//        SimpleRedisLock lock = new SimpleRedisLock("order:" + userId, stringRedisTemplate);_
3.          RLock lock = redissonClient.getLock("lock:order:" + userId);
4.          _//获取锁_
5.          boolean isLock = lock.tryLock();
6.          _//判断获取锁成功_
7.          if (!isLock) {
8.              _//获取锁失败，返回错误或重试_
9.              return Result.fail("不允许重复下单!");
10.         }
11.         try {
12.             _//获取代理对象_
13.             IVoucherOrderService proxy = (IVoucherOrderService) AopContext.currentProxy();
14.             _//8.返回订单id_
15.             return proxy.createVoucherOrder(voucherId);
16.         } finally {
17.             _//释放锁_
18.             lock.unlock();
19.         }
20.     }

可以完全代替分布式锁的前部分

##### Redisson可重入锁原理

由于setnx的局限性，redisson不可重入

假设你家的大门用的是一种特殊的智能锁（这就是我们的可重入锁）。

你第一次回家：用钥匙（lock.lock()）打开门，进去后把门关上了。此时，锁记录“户主A已经进入1次”。

你在家里，想进书房：书房是里屋，也有一把同款的锁。神奇的是，因为你已经在大门验证过身份了，书房锁识别出“哦，户主A已经在家了”，就直接让你进去了，不需要你再找书房的钥匙。此时，锁记录“户主A已经进入2次”。

你从书房出来：相当于释放了书房的锁（lock.unlock()），锁记录减为1次，但你人还在家里（大门锁还占着呢）。

你从家大门出去：最后用钥匙把大门锁打开（再次lock.unlock()），锁记录清零。这时，别人才可以进你家门。

获取锁的Lua脚本

1.  local key = KEYS\[1\]; -- 锁的key
2.  local threadId = ARGV\[1\]; -- 线程唯一标识 
3.  local releaseTime = ARGV\[2\]; -- 锁的自动释放时间 
4.  \-- 判断是否存在 
5.  if(redis.call('exists', key) == 0) then
6.      -- 不存在, 获取锁
7.       redis.call('hset', key, threadId, '1'); 
8.      -- 设置有效期
9.       redis.call('expire', key, releaseTime);
10.      return 1; -- 返回结果
11. end; 
12. \-- 锁已经存在，判断threadId是否是自己 
13. if(redis.call('hexists', key, threadId) == 1) then
14.     -- 不存在, 获取锁，重入次数+1
15.      redis.call('hincrby', key, threadId, '1'); 
16.     -- 设置有效期
17.     redis.call('expire', key, releaseTime);
18.     return 1; -- 返回结果 
19. end; 
20. return 0; -- 代码走到这里,说明获取锁的不是自己，获取锁失败

释放锁的lua脚本

1.  local key = KEYS\[1\]; -- 锁的key 
2.  local threadId = ARGV\[1\]; -- 线程唯一标识 
3.  local releaseTime = ARGV\[2\]; -- 锁的自动释放时间 

4.  \-- 判断当前锁是否还是被自己持有 
5.  if (redis.call('HEXISTS', key, threadId) == 0) then
6.       return nil; -- 如果已经不是自己，则直接返回
7.  end;
8.  \-- 是自己的锁，则重入次数-1 
9. local count = redis.call('HINCRBY', key, threadId, -1); 
10. \-- 判断是否重入次数是否已经为0  
11. if (count > 0) then
12.      -- 大于0说明不能释放锁，重置有效期然后返回
13.      redis.call('EXPIRE', key, releaseTime);
14.      return nil;
15. else  -- 等于0说明可以释放锁，直接删除
16.      redis.call('DEL', key);
17.      return nil; 
18. end;

##### Redisson的锁重试和WatchDog机制

利用信号量和PubSub功能实现等待，唤醒，获取锁失败的重试机制

利用watchDog延续锁时间，利用信号量控制锁重试等待，缺陷redis宕机引起锁失效问题

为了解决死锁问题，Redisson 给锁加了一个 “看门狗” 机制。

加锁成功时：Redisson 会给这个锁设置一个默认30秒的过期时间（TTL）。同时，它会启动一个后台定时任务（看门狗）。看门狗的工作：这个定时任务会每隔一段时间（比如10秒），去检查一下这个锁是否还被当前线程持有。如果还持有，它就自动给这个锁“续命”，把过期时间重新刷新回30秒。正常情况：只要你的业务代码还在正常运行，看门狗就会不断地给锁续期，保证锁不会因为超时而被意外释放。

异常情况：如果服务器宕机了，看门狗线程也挂了，自然就没人去续期了。30秒后，Redis 会自动删除这个过期的 myLock Key，锁就被释了，从而避免了死锁。

、

##### Redisson的multilock机制

联锁机制：多个独立的redisi节点，必须在所有节点都获取重入锁，才算获取锁成功，运维成本高，实现复杂

[一篇文章弄懂Redission可重入、重试锁以及MultiLock原理_redission可重入锁-CSDN博客](https://blog.csdn.net/weixin_53891720/article/details/142940284)

#### Redis优化秒杀

之前的效率

改进秒杀业务提高并发性能，需求：

- 新增秒杀优惠券的同时，将优惠券信息保存到Redis中

1.      @Override
2.      @Transactional
3.      public void addSeckillVoucher(Voucher voucher) {
4.          _// 保存优惠券_
5.          save(voucher);
6.          _// 保存秒杀信息_
7.          SeckillVoucher seckillVoucher = new SeckillVoucher();
8.          seckillVoucher.setVoucherId(voucher.getId());
9.          seckillVoucher.setStock(voucher.getStock());
10.         seckillVoucher.setBeginTime(voucher.getBeginTime());
11.         seckillVoucher.setEndTime(voucher.getEndTime());
12.         seckillVoucherService.save(seckillVoucher);
13.         _// 保存秒杀库存到Redis中_
14.         stringRedisTemplate.opsForValue().set(SECKILL_STOCK_KEY + voucher.getId(), voucher.getStock().toString());
15.     }

- 基于Lua脚本，判断秒杀库存，一人一单，决定用户是否抢购成功

Lua脚本：

1.  _\--1.参数列表_
2.  _\--1.1.优惠券id_
3.  local voucherId = ARGV\[1\]
4.  _\--1.2.用户id_
5.  local userId = ARGV\[2\]

6.  _\--2.定义数据key_
7.  _\--2.1.库存key_
8.  local stockKey = 'seckill:stock:' .. voucherId
9. _\--2.2.订单key_
10. local orderKey = 'seckill:order:' .. voucherId

11. _\--3.脚本业务_
12. _\--3.1.判断库存是否充足 get stockKey_
13. if (tonumber(redis.call('get', stockKey)) <= 0 )then
14.     _\--3.2.库存不足，返回1_
15.     return 1
16. end
17. _\--3.2.判断用户是否下单 sismember orderKey userId_
18. if (redis.call('sismember', orderKey, userId) == 1) then
19.     _\--3.3.存在，用户已经下单，返回2_
20.     return 2
21. end
22. _\--3.4.库存充足，用户未下单，下单成功，库存-1_
23. redis.call('incrby', stockKey, -1)
24. _\--3.5.下单（保存用户） sadd orderKey userId_
25. redis.call('sadd', orderKey, userId)
26. return 0

VoucherOrderServiceImpl

1.      @Override
2.      public Result seckillVoucher(Long voucherId) {
3.          _//获取用户id_
4.          Long userId = UserHolder.getUser().getId();
5.          _//1.执行lua脚本_
6.          Long result = stringRedisTemplate.execute(
7.                  SECKILL_SCRIPT,
8.                  Collections.emptyList(),
9.                  voucherId.toString(), userId.toString()
10.         );
11.         _//2.判断结果是否为0_
12.         int r = result.intValue();
13.         if(r != 0){
14.             _//2.1.不为0，说明没有购买资格_
15.             return Result.fail(r == 1 ? "库存不足" : "不能重复下单");
16.         }
17.         _//2.2.为0，有购买资格，把下单信息保存到阻塞队列中_
18.         long orderId = redisIdWorker.nextId("order");
19.         _//TODO 保存阻塞队列_

20.         _//3.返回订单id_
21.         return Result.ok(orderId);
22.     }

吞吐量明显上升

- 如果抢购成功，将优惠券id和用户id封装后存入阻塞队列

主方法：

1.  @Override
2.      public Result seckillVoucher(Long voucherId) {
3.          _//获取用户id_
4.          Long userId = UserHolder.getUser().getId();
5.          _//1.执行lua脚本_
6.          Long result = stringRedisTemplate.execute(
7.                  SECKILL_SCRIPT,
8.                  Collections.emptyList(),
9.                  voucherId.toString(), userId.toString()
10.         );
11.         _//2.判断结果是否为0_
12.         int r = result.intValue();
13.         if(r != 0){
14.             _//2.1.不为0，说明没有购买资格_
15.             return Result.fail(r == 1 ? "库存不足" : "不能重复下单");
16.         }
17.         _//2.2.为0，有购买资格，把下单信息保存到阻塞队列中_
18.         _//2.3.创建订单_
19.         VoucherOrder voucherOrder = new VoucherOrder();
20.         _//2.4.生成订单id_
21.         long orderId = redisIdWorker.nextId("order");
22.         voucherOrder.setId(orderId);
23.         _//2.5.获取当前用户_
24.         voucherOrder.setUserId(userId);
25.         _//2.6.获取代金券id_
26.         voucherOrder.setVoucherId(voucherId);
27.         _//2.6.保存阻塞队列_
28.         orderTasks.add(voucherOrder);

29.         _//3.获取代理对象_
30.         _// 获取代理对象（事务）_
31.         proxy = (IVoucherOrderService) AopContext.currentProxy();

32.         _//4.返回订单id_
33.         return Result.ok(orderId);
34.     }

先执行lua脚本，判断是否只下一单以及库存是否充足，如果都通过为拥有购买资格，创建订单对象voucherOrder，内部存储全局id生成器生成的订单id与当前用户id，代金券id，将此对象保存到阻塞队列中，最终返回订单id给前端

1.  private void handleVoucherOrder(VoucherOrder voucherOrder) {
2.          _//1.获取用户id 在线程池中使用userHolder获取不到用户id_
3.          Long userId = voucherOrder.getUserId();
4.          _//2.创建锁对象_
5.          RLock lock = redissonClient.getLock("lock:order:" + userId);
6.          _//获取锁_
7.          boolean isLock = lock.tryLock();
8.          _//是否获取锁成功_
9.          if (!isLock) {
10.             _//获取锁失败，返回错误或者重试_
11.             log.error("不允许重复下单");
12.             return;
13.         }
14.         try {
15.             proxy.createVoucherOrder(voucherOrder);
16.         } finally {
17.             _//释放锁_
18.             lock.unlock();
19.         }
20.     }

createVoucherOrder

1.  @Transactional
2.      public void createVoucherOrder(VoucherOrder voucherOrder) {
3.          //5.一人一单
4.          Long userId = voucherOrder.getUserId();
5.          //5.1.查询订单
6.          int count = query().eq("user_id", userId).eq("voucher_id", voucherOrder.getVoucherId()).count();
7.          //5.2.判断是否存在
8.          if(count > 0){
9.              //用户已经购买过了
10.             log.error("用户已经购买过一次！");
11.             return;
12.         }

13.         //6.扣减库存
14.         boolean success = seckillVoucherService.update()
15.                 .setSql("stock = stock - 1") //set stock = stock - 1
16.                 .eq("voucher_id", voucherOrder.getVoucherId()).gt("stock", 0)// where id = ? and stock > 0
17.                 .update();
18.         if(!success){
19.             //扣减失败
20.             log.error("库存不足");
21.             return;
22.         }

23.         //7.创建订单
24.         save(voucherOrder);
25.     }

实际上这里handleVoucherOrder操作中的加锁操作是冗余的，因为在主方法seckillVoucher中已经执行了保证原子性的鉴定购买资格的lua脚本，handleVoucherOrder最终指向createVoucherOrder方法，而createVoucherOrder方法中对一人一单的判定以及判定通过后的扣减库存也算是冗余的，最终指向myBatisPlus执行的save（VoucherOrder）命令

- 开启线程任务，不断从阻塞队列中获取信息，实现异步下单功能

初始化阻塞队列，并不断从阻塞队列中获取信息

1.      _//创建阻塞队列 当队列为空时，获取元素的操作会被阻塞；当队列满时，存储元素的操作会被阻塞。_
2.      private BlockingQueue&lt;VoucherOrder&gt; orderTasks = new ArrayBlockingQueue<>(1024 \* 1024);

3.      private static final ExecutorService SECKILL_ORDER_EXECUTOR = Executors.newSingleThreadExecutor();

4.      @PostConstruct
5.      private void init(){
6.          SECKILL_ORDER_EXECUTOR.submit(new VoucherOrderHandler());
7.      }

8.     private class VoucherOrderHandler implements Runnable{

9.         @Override
10.         public void run(){
11.             while (true){
12.                 try {
13.                     _//1.获取队列中的订单信息_
14.                     VoucherOrder voucherOrder = orderTasks.take();
15.                     _//2.创建订单_
16.                     handleVoucherOrder(voucherOrder);
17.                 } catch (Exception e) {
18.                    log.error("处理订单异常",e);
19.                 }
20.             }
21.         }
22.     }

##### 基于阻塞队列的异步秒杀存在的问题

阻塞队列基于JVM，所以可能存在内存溢出的情况

内存限制问题/数据安全问题

#### Redis消息队列实现异步秒杀

- 消息队列（message queue）字面意思就是存放消息的队列，最简单的消息队列模型包括3个角色：
- 消息队列：存储和管理消息，也被称为消息代理
- 生产者：发送消息到消息队列
- 消费者：从消息队列获取消息并处理消息
- Redis提供了三种不同的方式来实现消息队列：
- List结构：基于List结构模拟消息队列
- PubSub：基本的点对点消息模型
- Stream：比较完善的消息队列模型

##### 基于List结构模拟消息队列

- 消息队列（Message Queue），字面意思就是存放消息的队列，而Redis的list数据结构是一个双向链表，很容易模拟出队列的效果
- 队列是入口和出口不在一边，因此我们可以利用：LPUSH和RPOP，或者RPUSH结合LPOP来实现
- 不过要注意的是，当队列中没有信息时RPOP或LPOP会返回null，并不像JVM的阻塞队列那样会阻塞并等待消息，因此我们应该使用BRPOP或BLPOP来实现阻塞效果

生产者-Message-消费者

- 基于List的消费队列的优点：
- 利用Redis存储，不受限于JVM内存上限
- 基于Redis的持久化机制，数据安全性有保证
- 可以满足消息有序性
- 缺点：
- 无法避免消息丢失
- 只支持单消费者

##### 基于PubSub消息队列

- PubSub（发布订阅）是Redis2.0版本引入的消息传递模型，消费者可以订阅一个或多个channel，生产者向对应channel发布消息后，所有订阅者都能收到相关信息
- SUBSCRIBE channel \[channel\]：订阅一个或多个频道
- PUBLISH channel msg：向一个频道发送消息
- PSUBSCRIBE pattern\[pattern\]：订阅与pattern格式匹配（模式匹配）的所有频道
- 优点：采用发布订阅模型，支持多生产，多消费
- 缺点：不支持数据持久化，无法避免消息丢失，消息堆积有上线，超出时数据丢失，可靠性并不高

##### 基于Stream的消息队列

Stream是Redis5.0引入的一种新数据类型，可以实现一个功能非常完善的消息队列

- 发送消息XADD

- 读取消息XREAD

当指定起始ID为$时候，代表读取最新的消息，如果我们处理一条消息的过程中，又有超过1条以上的消息到达队列，则下次获取时们也只能获取到最新的一条，会出现漏读消息的情况

- STREAM类型消息队列的XREAD命令特点
- 消息可回溯
- 一个消息可以被多个消费者读取
- 可以阻塞读取
- 有消息漏读的风险

##### 基于Stream的消息队列-消费者组

- 消费者组（Consumer Group）：将多个消费者划分到一个组中，监听同一个队列，具备下列特点：
- 消息分流：队列中的消息会分流给组内的不同消费者，而不是重复消费，从而加快消息处理的速度
- 消息标识：消费者组会维护一个标识，记录最后一个被处理的消息，哪怕消费者宕机重启，还会从标识之后读取消息，确保每个消息都会被消费-确保不会被漏读
- 消息确认：消费者获取消息后，消息处于一个pending状态，并存入pending状态，并存入一个pending-list。当处理完成后，需要通过XACK来确认消息，标记消息为已处理，才会从pending-list移除-确保所有的消息都要消费一次
- 创建消费者组

XGROUP CREATE key groupName ID \[MKSTREAM\]

Key：队列消息

groupName：消费者组名称

ID：起始ID标识，$标识队列中的最后一个消息，0则代表队列中的第一个消息

MKSTREAM：队列不存在时自动创建队列

如果创建消费者组时消费者不存在，消费者会被自动创建

- 从消费者组读取消息

- STEAM类型消息队列的XREADGROUP命令特点：
- 消息可回溯
- 可以多消费者争抢消息，加快消息速度
- 可以阻塞读取
- 没有消息漏读的风险
- 有消息确认机制，保证消息至少被消费一次

##### 基于Redis的Stream结构作为消息队列，实现异步秒杀下单

需求：

- 创建一个Stream类型的消息队列，名为stream.orders

XGROUP CREATE stream.orders g1 0 MKSTREAM

- 修改之前的秒杀下单Lua脚本，在认定抢购资格之后，直接向stream.orders中添加消息，内容包含voucherId，userId，orderId
- 项目启动时，开启一个线程任务，尝试获取stream.orders中的消息，完成下单

### 达人探店

#### 发布探店笔记

探店笔记类似点评网站的评价，往往是图文结合，对应的表有两个：

tb_blog:探店笔记表，包含笔记中的标题，文字，图片等

tb_blog_comments:其他用户对探店笔记的评价

##### 上传探店照片与信息

1.      @PostMapping("blog")
2.      public Result uploadImage(@RequestParam("file") MultipartFile image) {
3.          try {
4.              _// 获取原始文件名称_
5.              String originalFilename = image.getOriginalFilename();
6.              _// 生成新文件名_
7.              String fileName = createNewFileName(originalFilename);
8.              _// 保存文件_
9.              image.transferTo(new File(SystemConstants.IMAGE_UPLOAD_DIR, fileName));
10.             _// 返回结果_
11.             log.debug("文件上传成功，{}", fileName);
12.             return Result.ok(fileName);
13.         } catch (IOException e) {
14.             throw new RuntimeException("文件上传失败", e);
15.         }
16.     }

##### 保存探店用户

1.      @PostMapping
2.      public Result saveBlog(@RequestBody Blog blog) {
3.          _// 获取登录用户_
4.          UserDTO user = UserHolder.getUser();
5.          blog.setUserId(user.getId());
6.          _// 保存探店博文_
7.          blogService.save(blog);
8.          _// 返回id_
9.          return Result.ok(blog.getId());
10.     }

##### 实现查看发布探店笔记的接口

点击首页的探店笔记，会进入详情页面，实现该页面的查询接口

请求方式：GET 请求路径/blog/{id} 请求参数 id：blog的id 返回值 Blog：笔记信息，包含用户信息

1.      @Override
2.      public Result queryBlogById(Long id) {
3.          _//1，查询blog_
4.          Blog blog = getById(id);
5.          if (blog == null){
6.              return Result.fail("笔记不存在");
7.          }
8.          _//2，查询blog有关的用户_
9.          queryBlogUser(blog);
10.         return Result.ok(blog);
11.     }

12.     private void queryBlogUser(Blog blog) {
13.         Long userId = blog.getUserId();
14.         User user = userService.getById(userId);
15.         blog.setName(user.getNickName());
16.         blog.setIcon(user.getIcon());
17.     }

#### 点赞

需求：

同一个用户只能点赞一次，再次点击则取消点赞

如果当前用户已经点赞，则点赞高亮显示（前端已实现，判断字段Blog类的isLike属性）

实现步骤：

- 给blog类中添加一个isLike字段，标识是否被当前用户点赞
- 修改点赞功能，利用redis的set判断是否点赞过，为点赞过则点赞数+1,已点赞过的则点赞数-1

1.      @Override
2.      public Result likeBlog(Long id) {
3.          _//1.获取登录用户_
4.          Long userId = UserHolder.getUser().getId();
5.          _//2.判断当前登录用户是否已经点赞_
6.          String key = BLOG_LIKED_KEY + id;
7.          Boolean isMember = stringRedisTemplate.opsForSet().isMember(key, userId.toString());
8.          if(BooleanUtil.isFalse(isMember)) {
9.              _//3.如果未点赞，则点赞_
10.             _//3.1.数据库点赞数 + 1_
11.             boolean isSuccess = update().setSql("liked = liked + 1").eq("id", id).update();
12.             _//3.2.保存用户到redis的set集合_
13.             if(isSuccess){
14.                 stringRedisTemplate.opsForSet().add(key, userId.toString());
15.             }
16.         }else{
17.             _//4.如果已点赞，则取消点赞_
18.             _//4.1.数据库点赞数-1_
19.             boolean isSuccess = update().setSql("liked = liked - 1").eq("id", id).update();
20.             _//4.2.把用户从redis的set集合移除_
21.             stringRedisTemplate.opsForSet().remove(key, userId.toString());
22.         }
23.         return Result.ok();
24.     }

- 修改根据id查询Blog的业务，判断当前用户是否点赞过，赋值给isLike字段
- 修改分页查询Blog业务，判断当前登录用户是否点赞过，赋值给isLike字段

1.      private void isBlogLiked(Blog blog) {
2.          _//1.获取登录用户_
3.          Long userId = UserHolder.getUser().getId();
4.          _//2.判断当前登录用户是否已经点赞_
5.          String key = BLOG_LIKED_KEY + blog.getId();
6.          Boolean isMember = stringRedisTemplate.opsForSet().isMember(key, userId.toString());
7.          blog.setIsLike(BooleanUtil.isTrue(isMember));
8.      }

设置字段值

#### 点赞排行榜

在探店笔记的详情页面，应该把给该笔记点赞的人显示出来，比如最早点赞的TOP5，形成点赞排行榜

请求方式：GET

请求路径 /blog/likes/{id}

请求参数：id：blog的id

返回值List&lt;UserDTO&gt;给这个笔记点赞的TopN用户集合

|     |     |     |     |
| --- | --- | --- | --- |
|     | **List** | **Set** | **SortedSet** |
| **排序方式** | 按添加顺序排序 | 无法排序 | 根据score值排序 |
| **唯一性** | 不唯一 | 唯一  | 唯一  |
| **查找方式** | 按索引查找<br><br>或首尾查找 | 根据元素查找 | 根据元素查找 |

使用sortedSet进行存储

1.      @Override
2.      public Result likeBlog(Long id) {
3.          _//1.获取登录用户_
4.          Long userId = UserHolder.getUser().getId();
5.          _//2.判断当前登录用户是否已经点赞_
6.          String key = BLOG_LIKED_KEY + id;
7.          Double score = stringRedisTemplate.opsForZSet().score(key, userId.toString());
8.          if(score == null) {
9.              _//3.如果未点赞，则点赞_
10.             _//3.1.数据库点赞数 + 1_
11.             boolean isSuccess = update().setSql("liked = liked + 1").eq("id", id).update();
12.             _//3.2.保存用户到redis的set集合 zadd key value score（时间戳）_
13.             if(isSuccess){
14.                 stringRedisTemplate.opsForZSet().add(key, userId.toString(),System.currentTimeMillis());
15.             }
16.         }else{
17.             _//4.如果已点赞，则取消点赞_
18.             _//4.1.数据库点赞数-1_
19.             boolean isSuccess = update().setSql("liked = liked - 1").eq("id", id).update();
20.             _//4.2.把用户从redis的set集合移除_
21.             stringRedisTemplate.opsForZSet().remove(key, userId.toString());
22.         }
23.         return Result.ok();
24.     }

修改存储数据结构

查询博客的点赞排行榜信息

1.  @Override
2.      public Result queryBlogLikes(Long id) {
3.          String key = BLOG_LIKED_KEY + id;
4.          _//1.查询top5的点赞用户 zrange key 0 4_
5.          Set&lt;String&gt; top5 = stringRedisTemplate.opsForZSet().range(key, 0, 4);
6.          if(top5 == null || top5.isEmpty()){
7.              _//如果无点赞数据，返回一个空列表_
8.              return Result.ok(Collections.emptyList());
9.          }
10.         _//2.解析出其中的用户id_
11.         List&lt;Long&gt; ids = top5.stream().map(Long::valueOf).collect(Collectors.toList());
12.         String idStr = StrUtil.join(",", ids);
13.         _//3.根据用户id查询用户_
14.         List&lt;UserDTO&gt; userDTOS = userService.query()
15.                 .in("id", ids).last("ORDER BY FIELD(id," + idStr +")").list()
16.                 .stream()
17.                 .map(user -> BeanUtil.copyProperties(user, UserDTO.class))
18.                 .collect(Collectors.toList());

19.         _//4.返回_
20.         return Result.ok(userDTOS);
21.     }

### 好友关注

基于Set集合的关注，取关，共同关注，消息推送功能

#### 关注和取关

需求：基于该表结构，实现两个接口

关注和取关接口

1.  @Override
2.      public Result follow(Long followUserId, Boolean isFollow) {
3.          //0.获取登录用户
4.          Long userId = UserHolder.getUser().getId();

5.          //1.判断是关注还是取关
6.          if(isFollow) {
7.              //2.关注，新增数据
8.              Follow follow = new Follow();
9.             follow.setUserId(userId);
10.             follow.setFollowUserId(followUserId);
11.             save(follow);
12.         }else{
13.             //3.取关，删除 delete from tb_follow where user_id = ? and follow_user_id = ?
14.             remove(new QueryWrapper&lt;Follow&gt;()
15.                     .eq("user_id", userId).eq("follow_user_id", followUserId));
16.         }
17.         return Result.ok();
18.     }

判断是否关注的接口

1.     @Override
2.      public Result isFollow(Long followUserId) {
3.          //0.获取登录用户
4.          Long userId = UserHolder.getUser().getId();

5.          //1.查询是否关注 select count（\*） from tb_follow where user_id = ? and follow_user_id = ?
6.          Integer count = query().eq("user_id", userId).eq("follow_user_id", followUserId).count();
7.          //2.判断
8.          return Result.ok(count > 0);
9.     }

关注是User之间的关系，是博主与粉丝的关系，数据库中有tb_follow表来标识

#### 共同关注

需求：利用redis中恰当的数据结构，实现共同关注功能，在博主个人页面展现出当前用户与博主的共同好友

1.      @Override
2.      public Result followCommons(Long id) {
3.          _//1.获取当前登录用户_
4.          Long userId = UserHolder.getUser().getId();
5.          String key = "follows:" + userId;
6.          _//2.求交集_
7.          String key2 = "follows:" + id;
8.          Set&lt;String&gt; intersect = stringRedisTemplate.opsForSet().intersect(key, key2);
9.          if (intersect == null || intersect.isEmpty()) {
10.             _//无交集_
11.             return Result.ok(Collections.emptyList());
12.         }
13.         _//3.解析id集合_
14.         List&lt;Long&gt; ids = intersect.stream().map(Long::valueOf).collect(Collectors.toList());
15.         _//4.查询用户_
16.         List&lt;UserDTO&gt; users = userService.listByIds(ids)
17.                 .stream()
18.                 .map(user -> BeanUtil.copyProperties(user, UserDTO.class))
19.                 .collect(Collectors.toList());
20.         return Result.ok(users);
21.     }

对之前保存数据库之后追加保存到redis的set存储

1.      @Override
2.      public Result follow(Long followUserId, Boolean isFollow) {
3.          _//0.获取登录用户_
4.          Long userId = UserHolder.getUser().getId();
5.          String key = "follows:" + userId;
6.          _//1.判断是关注还是取关_
7.          if(isFollow) {
8.              _//2.关注，新增数据_
9.              Follow follow = new Follow();
10.             follow.setUserId(userId);
11.             follow.setFollowUserId(followUserId);
12.             boolean isSuccess = save(follow);
13.             if (isSuccess){
14.                 _//把关注用户的id放入redis的set集合 sadd key value_
15.                 stringRedisTemplate.opsForSet().add(key,followUserId.toString());
16.             }
17.         }else{
18.             _//3.取关，删除 delete from tb_follow where user_id = ? and follow_user_id = ?_
19.             boolean isSuccess = remove(new QueryWrapper&lt;Follow&gt;()
20.                     .eq("user_id", userId).eq("follow_user_id", followUserId));
21.             _//把关注用户的id从redis集合中移除_
22.             if(isSuccess) {
23.                 stringRedisTemplate.opsForSet().remove(key, followUserId.toString());
24.             }
25.         }
26.         return Result.ok();
27.     }

#### 关注推送

- 关注推送也叫Feed流，通过无限下拉刷新获取新的信息，Feed流产品有两种常见模式
- TimeLine：不做内容筛选，简单的按照内容发布时间排序，常用于好友或关注，例如朋友圈

优点：信息全面，不会有缺失，并且实现也相对简单

缺点：信息噪音较多，用户不一定感兴趣，内容获取效率到底

- 智能排序：利用智能算法屏蔽掉违规的，用户不感兴趣的内容，推送用户感兴趣来吸引用户

优点：投喂用户感兴趣的信息，用户粘度高，容易沉迷

缺点：如果算法不精准，可能起到反作用

- 本例中的个人页面，是基于关注的好友来做Feed流，因此采用TimeLine的模式，该模式的实现方案有三种
- 拉模式：也叫读扩散

节省内存，但是读写延迟高 写比例低，但是读比例高 使用场景少

- 推模式

延迟低，但是通信代价大

- 推拉结合

也叫的读写混合，兼具推和拉两种模式的优点

##### 基于推模式实现关注推送功能

需求：

- 修改新增探店笔记的业务，在保存blog到数据库的同时，推送到粉丝的收件箱
- 收件箱满足可以根据时间戳排序，必须用Redis的数据结构实现

1.      @Override
2.      public Result saveBlog(Blog blog) {
3.          _// 1.获取登录用户_
4.          UserDTO user = UserHolder.getUser();
5.          blog.setUserId(user.getId());
6.          _// 2.保存探店博文_
7.          boolean isSuccess = save(blog);
8.          if (!isSuccess) {
9.              return Result.fail("新增笔记失败！");
10.         }
11.         _// 3.查询笔记作者的所有粉丝_ 
12. _//select \* from tb_follow where follow_user_id = ?_
13.         List&lt;Follow&gt; follows = followService.query().eq("follow_user_id", user.getId()).list();
14.         _// 4.推送笔记id给所有粉丝_
15.         for (Follow follow : follows) {
16.             _//4.1.获取粉丝id_
17.             Long userId = follow.getUserId();
18.             _//4，2.推送_
19.             String key = FEED_KEY + userId;
20.             stringRedisTemplate.opsForZSet().add(key, blog.getId().toString(), System.currentTimeMillis());
21.         }
22.         _// 5.返回id_
23.         return Result.ok(blog.getId());
24.     }

- 查询收件箱数据时，可以实现分页查询

由于Feed流中的数据不断更新，所以数据的角标也在不断变化，因此不能使用传统的分页模式，采用滚动分页

滚动分页查询参数：

max：当前时间戳 | 上一次查询的最小时间戳

Min：0（固定）

Offset：0 | 在上一次结果中与最小值一样的元素的个数

Count：3（与前端协定一页展示几个）

1.  @Override
2.      public Result queryBlogOfFollow(Long max, Integer offset) {
3.          _//1.获取当前用户_
4.          Long userId = UserHolder.getUser().getId();
5.          _//2.查询收件箱 ZREVRANGEBYSCORE key max min LIMIT offset count_
6.          String key = FEED_KEY + userId;
7.          Set&lt;ZSetOperations.TypedTuple<String&gt;> typedTuples = stringRedisTemplate.opsForZSet()
8.                  .reverseRangeByScoreWithScores(key, 0, max, offset, 2);
9.          _//3.非空判断_
10.         if (typedTuples == null || typedTuples.isEmpty()) {
11.             return Result.ok();
12.         }
13.         _//4.解析数据：blogId，minTime（时间戳），offset_
14.         List&lt;Long&gt; ids = new ArrayList<>(typedTuples.size());
15.         long minTime = 0;
16.         int os = 1;
17.         for(ZSetOperations.TypedTuple&lt;String&gt; tuple : typedTuples){
18.             _//4.1.获取blog id_
19.             String blogId = tuple.getValue();
20.             ids.add(Long.valueOf(blogId));
21.             _//4.2.获取分数（时间戳）_
22.             long time = tuple.getScore().longValue();
23.             if(time == minTime){
24.                 os++;
25.             }else{
26.                 minTime = time;
27.                 os = 1;
28.             }
29.         }
30.         _//5.根据id查询blog_
31.         String idStr = StrUtil.join(",", ids);
32.         List&lt;Blog&gt; blogs = query().in("id", ids).last("ORDER BY FIELD(id," + idStr +")").list();

33.         for(Blog blog : blogs){
34.             _//查询blog有关的用户_
35.             queryBlogUser(blog);
36.             _//2.查询blog是否被点赞_
37.             isBlogLiked(blog);
38.         }

39.         _//6.封装并返回_
40.         ScrollResult r = new ScrollResult();
41.         r.setList(blogs);
42.         r.setOffset(os);
43.         r.setMinTime(minTime);
44.         return Result.ok(r);
45.     }

之前将博文id推送到redis的粉丝收件箱存储，现在通过ZREVRANGEBYSCORE查询，判断非空后遍历tuple，获取用户的id以及时间戳，让时间戳先初始化为0，在遍历中不断获取新的时间戳，如果最新的时间与前一个时间戳相同时，将偏移量+1，反之则将偏移量重置为1，最后根据id查询blog以及与blog相关的用户与点赞信息，最终封装并返回偏移量，最小时间戳给前端

### 附近的商户

Redis的GeoHash的应用

#### GEO数据结构

- GEOloaction，代表地理坐标，redis在3.2版本加入对GEO的支持，允许存储地理坐标信息，帮助我们根据经纬度来检索数据
- GEOADD：添加一个地理空间信息，包含：经度，纬度，值
- GEODIST：计算指定两个点之间的距离并返回
- GEOHASH：将指定member的坐标转为hash字符串形式并返回
- GEOPOS：返回指定member的坐标
- GEORADIUS：指定圆心，半径，找到该圆内所有包含的member，并按照与圆心之间的距离排序后返回，6.2后已弃用
- GEOSEARCH：在指定范围内搜索member，并按照与指定点之间的距离排序后返回，范围可以是圆心或矩形
- GEOSEARCHSTORE：与GEOSEARCH功能一致，不过可以把结果存储到一个指定的key

#### 附近商户搜索

在首页中点击某个频道，即可看到频道下的商户，按照商户类型做分组，类型相同的商户作为同一组，以typeId为key存入同一个GEO集合中即可

请求方式：GET

请求路径：/shop/of/type

请求参数：

typeId：商户类型

Current：页码滚动查询

X：经度

Y：维度

返回值：List&lt;Shop&gt;:符合要求的商户信息

1.   @Override
2.      public Result queryShopByType(Integer typeId, Integer current, Double x, Double y) {
3.          _// 1.判断是否需要根据坐标查询_
4.          if (x == null || y == null) {
5.              _// 不需要坐标查询，按数据库查询_
6.              Page&lt;Shop&gt; page = query()
7.                      .eq("type_id", typeId)
8.                      .page(new Page<>(current, SystemConstants.DEFAULT_PAGE_SIZE));
9.              _// 返回数据_
10.             return Result.ok(page.getRecords());
11.         }

12.         _// 2.计算分页参数_
13.         int from = (current - 1) \* SystemConstants.DEFAULT_PAGE_SIZE;
14.         int end = current \* SystemConstants.DEFAULT_PAGE_SIZE;

15.         _// 3.查询redis、按照距离排序、分页。结果：shopId、distance_
16.         String key = SHOP_GEO_KEY + typeId;
17.         GeoResults&lt;RedisGeoCommands.GeoLocation<String&gt;> results = stringRedisTemplate.opsForGeo() _// GEOSEARCH key BYLONLAT x y BYRADIUS 10 WITHDISTANCE_
18.                 .search(
19.                         key,
20.                         GeoReference.fromCoordinate(x, y),
21.                         new Distance(5000),
22.                         RedisGeoCommands.GeoSearchCommandArgs.newGeoSearchArgs().includeDistance().limit(end)
23.                 );
24.         _// 4.解析出id_
25.         if (results == null) {
26.             return Result.ok(Collections.emptyList());
27.         }
28.         List&lt;GeoResult<RedisGeoCommands.GeoLocation<String&gt;>> list = results.getContent();
29.         if (list.size() <= from) {
30.             _// 没有下一页了，结束_
31.             return Result.ok(Collections.emptyList());
32.         }
33.         _// 4.1.截取 from ~ end的部分_
34.         List&lt;Long&gt; ids = new ArrayList<>(list.size());
35.         Map&lt;String, Distance&gt; distanceMap = new HashMap<>(list.size());
36.         list.stream().skip(from).forEach(result -> {
37.             _// 4.2.获取店铺id_
38.             String shopIdStr = result.getContent().getName();
39.             ids.add(Long.valueOf(shopIdStr));
40.             _// 4.3.获取距离_
41.             Distance distance = result.getDistance();
42.             distanceMap.put(shopIdStr, distance);
43.         });
44.         _// 5.根据id查询Shop_
45.         String idStr = StrUtil.join(",", ids);
46.         List&lt;Shop&gt; shops = query().in("id", ids).last("ORDER BY FIELD(id," + idStr + ")").list();
47.         for (Shop shop : shops) {
48.             shop.setDistance(distanceMap.get(shop.getId().toString()).getValue());
49.         }
50.         _// 6.返回_
51.         return Result.ok(shops);

- 使用Redis GEO功能进行地理搜索：
- 构造Redis GEO键名：SHOP_GEO_KEY + typeId
- 执行GEO搜索：以(x,y)为中心点，搜索5000米范围内的店铺
- 包含距离信息，限制返回结果数量为end

查询结果实例

1.  GeoResult {
2.      content: GeoLocation {
3.        name: "1002",
4.        point: Point {
5.          x: 116.410,
6.          y: 39.920
7.        }
8.      },
9.      distance: Distance {
10.       value: 2345.67
11.     }

- 检查搜索结果是否为空，如果为空返回空列表。
- 获取结果列表内容，如果结果数量小于起始位置，说明没有更多数据，返回空列表。
- 处理分页和数据提取：
- 跳过前面from条数据（实现分页）
- 遍历当前页的数据，提取店铺ID和距离信息
- 将店铺ID存入ids列表，将ID和距离的映射关系存入distanceMap
- 根据ID列表查询店铺完整信息：
- 使用MyBatis Plus的in查询获取店铺信息
- 使用ORDER BY FIELD保持与Redis GEO搜索结果相同的顺序
- 为每个店铺设置距离值

### 用户签到

Redis的BitMap数据统计功能

#### BitMap用法

我们按月来统计用户签到信息，签到记录为1，未签到则记录为0，把每一个bit位对应当月的每一天，形成映射关系，用0和1标识业务状态，这种思路就被称为位图

Redis中使用string类型数据结构实现BitMap，因此最大上限是512M，转换为bit则是2的32次方位

BitMap的操作命令有

SETBIT：向指定位置（offset）存入一个0或1

GETBIT：获取指定位置（offset）的bit值

BITCOUNT：统计BitMap中值为1的bit为的数量他

BITFIELD：操作（查询，修改，自增）BitMap中bit数组中的指定位置（offset）中的值

BITFIELD_RO：获取BitMap中Bit数组，并以10进制形式返回

BITOP：将多个BitMap的结果做位运算（与，或，亦或）

BITOS：查找bit数组中指定范围内第一个0或1出现的位置

#### 签到功能

需求：实现签到接口，将当前用户当前签到信息保存到Redis中

请求方式：Post

请求路径：/user/sign

请求参数：无

返回值：无

1.     @Override
2.      public Result sign() {
3.          _//1.获取当前登录的用户_
4.          Long userId = UserHolder.getUser().getId();
5.          _//2.获取日期_
6.          LocalDateTime now = LocalDateTime.now();
7.          _//3.拼接key_
8.          String keySuffix = now.format(DateTimeFormatter.ofPattern(":yyyyMM"));
9.          String key = USER_SIGN_KEY + userId + keySuffix;
10.         _//4.获取今天是本月的第几天_
11.         int dayOfMonth = now.getDayOfMonth();
12.         _//5.写入Redis SET bitmap offset 1_
13.         stringRedisTemplate.opsForValue().setBit(key, dayOfMonth - 1, true);
14.         return Result.ok();
15.     }

#### 签到统计

- 从最后一次签到开始向前统计，知道遇到最后一次未签到为止，计算总的签到次数，就是连续签到天数
- 与1做与运算，就能得到最后一个bit位，随后右移1位，下一个bit位就变成了最后一个bit位
- 需求：实现下面接口，统计当前用户截至当前时间在本月的连续签到天数
- 请求方式：GET
- 请求路径：/user/sign/count
- 请求参数：无
- 返回值：连续签到天数

1.      @Override
2.      public Result signCount() {
3.          _//1.获取当前登录用户_
4.          Long userId = UserHolder.getUser().getId();
5.          _//2.获取日期_
6.          LocalDateTime now = LocalDateTime.now();
7.          _//3.拼接key_
8.          String keySuffix = now.format(DateTimeFormatter.ofPattern(":yyyyMM"));
9.          String key = USER_SIGN_KEY + userId + keySuffix;
10.         _//4.获取今天是本月的第几天_
11.         int dayOfMonth = now.getDayOfMonth();
12.         _//5.获取本月截至今天位置所有的签到记录，返回的是一个十进制数字 BITFIELD key get u14 0_
13.         List&lt;Long&gt; result = stringRedisTemplate.opsForValue().bitField(
14.                 key,
15.                 BitFieldSubCommands.create()
16.                         .get(BitFieldSubCommands.BitFieldType.unsigned(dayOfMonth)).valueAt(0)
17.         );
18.         if(result == null || result.isEmpty()){
19.             _//没有任何签到结果_
20.             return Result.ok(0);
21.         }
22.         Long num = result.get(0);
23.         if(num == 0 || num == null) {
24.             return Result.ok(0);
25.         }
26.         _//6.循环遍历，判断这个日期是否在连续签到中_
27.         int count = 0;
28.         while(true){
29.             _//6.1.让这个数字与1做与运算，得到数字的最后一个bit位_
30.             _//6.2.判断这个bit位是否为0_
31.             if ((num & 1) == 0) {
32.                 _//6.3.如果是0，说明未签到，结束_
33.                 break;
34.             }else{
35.                 _//6.4.如果为1，说明已签到，继续，计数器 + 1_
36.                 count ++;
37.             }
38.             _//把数字右移1位，抛弃最后一个bit位，继续判断下一个bit位_
39.             num >>>= 1;
40.         }
41.         return Result.ok(count);
42.     }

### UV统计

Redis的HyperLog的统计功能

#### HyperLogLog用法

- UV（Unique Vistitor）也叫独立访客量，是指通过互联网访问浏览这个网页的自然人，1天内同一个用户多次访问该网站，只记录1此
- PV（Page View）也叫页面访问量或点击量，用户每访问网站的一个页面，记录1次PV，用户多次打开页面，则记录多次PV，往往用来衡量网站的流量
- UV统计在服务端做会比较麻烦，因为要判断该用户是否已经统计过了，需要将统计过的用户信息保存，但是如果每个访问的用户都保存到Redis中，数据量会非常恐怖
- HyperLoglog是从loglog算法派生的概率算法，用于确定非常大的集合的技术，而不需要存储其所有制
- Redis中的HLL是基于string结构实现的，单个HLL的内存永远小于16kb，内存占用非常低，但是作为代价，其测量结果是有概率性的，有小于0.81%的误差，不过对于UV统计来说这完全可以忽略

#### 实现UV统计

直接利用单元测试，向HyperLogLog中添加100万条数据，看看内存占用和统计效果

1.      @Test
2.      void testHyperLogLog() {
3.          String \[\] values = new String\[1000\];
4.          int j = 0;
5.          for(int i = 0; i < 1000000; i++){
6.              j = i % 1000;
7.              values\[j\] = "user_" + i;
8.              if(j == 999){
9.                  _//发送到redis_
10.                 stringRedisTemplate.opsForHyperLogLog().add("hl2", values);
11.             }
12.         }
13.         _//统计数量_
14.         Long count = stringRedisTemplate.opsForHyperLogLog().size("hl2");
15.         System.out.println("count = " + count);
16.     }
