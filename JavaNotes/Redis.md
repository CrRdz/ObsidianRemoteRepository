> 本部分主要基于黑马点评项目

## 基础篇

### NoSQL

非关系型数据库，非结构化，非关联的，非 SQL，事务管理上使用 BASE，并非 ACID。

* 2009年诞生，Remote Dictionary Server 远程词典服务器，是一个基于内存的键值型 NoSQL 数据库。
* **特征**：
* 键值（key-value）型，value 支持多种不同数据结构，功能丰富。
* 单线程，每个命令具备原子性。
* 低延迟，速度快（基于内存，IO 多路复用，良好的编码）。
* 支持数据持久化。



### 安装 Redis

#### 单机安装 Redis

**1. 安装 Redis 依赖**

Redis 是基于 C 语言编写，因此首先需要安装 Redis 所需要的 gcc 依赖：

```bash
yum install -y gcc tcl

```

**2. 上传安装包并解压**

上传到虚拟机 `/usr/local/src` 目录，并解压缩：

```bash
tar -xzf redis-6.2.6.tar.gz

```

解压后使用 cd 命令进入 redis 目录：

```bash
cd redis-6.2.6
```

运行编译命令：

```bash
make && make install
```

#### 启动 Redis

##### 默认启动

安装完成后，在任意目录输入 `redis-server` 命令即可启动 Redis：

```bash
redis-server
```

##### 指定配置启动

如果要让 Redis 以后台方式启动，则必须修改 Redis 配置文件，就在我们之前解压的 redis 安装包下（`/usr/local/src/redis-6.2.6`），名字叫 `redis.conf`。

先将这个配置文件备份一份：

```bash
cp redis.conf redis.conf.bck

```

然后修改 `redis.conf` 文件中的一些配置：

```conf
# 允许访问的地址，默认是127.0.0.1，会导致只能在本地访问
# 修改为0.0.0.0则可以在任意IP访问，生产环境不要设置为0.0.0.0
bind 0.0.0.0

# 守护进程，修改为yes后即可后台运行
daemonize yes 

# 密码，设置后访问Redis必须输入密码
requirepass 123321

```

> 注：使用 `/` 可以进行快速查找，使用 `i` 进入编辑模式，`:wq` 保存并退出。

启动 Redis：

```bash
# 进入redis安装目录
cd /usr/local/src/redis-6.2.6
# 启动
redis-server redis.conf

```

停止 Redis：

```bash
# 利用redis-cli来执行 shutdown 命令，即可停止 Redis 服务，
# 因为之前配置了密码，因此需要通过 -u 来指定密码
redis-cli -u 123321 shutdown

```

##### 开机自启动

新建一个系统服务文件：

```bash
vi /etc/systemd/system/redis.service

```

内容如下：

```ini
[Unit]
Description=redis-server
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/bin/redis-server /usr/local/src/redis-6.2.6/redis.conf
PrivateTmp=true

[Install]
WantedBy=multi-user.target

```

然后重载系统服务：

```bash
systemctl daemon-reload

```

现在可以使用命令来操作 Redis：

```bash
# 启动
systemctl start redis
# 停止
systemctl stop redis
# 重启
systemctl restart redis
# 查看状态
systemctl status redis
# 设置开机自启
systemctl enable redis

```

#### Redis 客户端

##### Redis 命令行客户端

Redis 安装成功后就自带命令行客户端，需要 cd 到指定目录 `/usr/local/bin/`。

```bash
redis-cli [options] [commands]

```

其中常见的 options 有：

* `-h 127.0.0.1`：指定要连接的 redis 节点的 IP 地址，默认是 127.0.0.1
* `-p 6379`：指定要连接的 redis 节点的端口，默认是 6379
* `-a 123321`：指定 redis 的访问密码

其中的 commands 就是 Redis 的操作命令，例如：

* `ping`：与 redis 服务端做心跳测试，服务端正常会返回 `pong`

##### 图形化桌面客户端

安装 RDM (Redis Desktop Manager)，左上角建立连接，在弹出的窗口中填写 Redis 服务信息，点击确定后即可建立连接了。Redis 默认有 16 个仓库，编号从 0 至 15。通过配置文件可以设置仓库数量，但是不超过 16，并且不能自定义仓库名称。

### Redis 命令

Redis 是一个 key-value 的数据库，key 一般是 String 类型，value 的类型多种多样：

* **基本类型**：String, Hash, List, Set, SortedSet
* **特殊类型**：GEO, BitMap, HyperLog

#### Redis 通用命令

通用指令是部分数据类型的，都可以使用的指令，常见的有：

* `KEYS`：查看符合模板的所有 key（**不建议在生产环境设备上使用**）。
* `DEL`：删除一个指定的 key。
* `EXISTS`：判断 key 是否存在。
* `EXPIRE`：给一个 key 设置有效期，有效期到期时该 key 会被自动删除。
* `TTL`：查看一个 key 的剩余有效期。

通过 `help [command]` 可以查看一个命令的具体用法。

#### String 类型

String 类型，也就是字符串类型，是 Redis 中最简单的存储类型。
其 value 是字符串，不过根据字符串的格式不同，又可以分为 3 类：

* `String`：普通字符串
* `int`：整数类型，可以做自增，自减操作
* `Float`：浮点类型，可以做自增，自减操作

不管是那种格式，底层都是字节数组形式存储，只不过编码方式不同，字符串类型的最大空间不超过 512mb。

**String 常见的命令：**

* `SET`：添加或者修改已经存在的一个 String 类型的键值对
* `GET`：根据 key 获取 String 类型的 value
* `MSET`：批量添加多个 String 类型的键值对
* `MGET`：根据多个 key 获取多个 String 类型的 value
* `INCR`：让一个整型的 key 自增 1
* `INCRBY`：让一个整型的 key 自增并指定步长（也有自减的效果）
* `INCRBYFLOAT`：让一个浮点类型的数字自增并指定步长

**组合命令：**

* `SETNX`：添加一个 String 类型的键值对，前提是这个 key 不存在，否则不执行
* `SETEX`：添加一个 String 类型的键值对，并且指定有效期

#### Key 的层级格式

Redis 中没有类似 MySQL 中的 table 概念，如何区分不同类型的 key？ —— **Key 结构**。
Redis 的 key 允许有多个单词形成层级结构，多个单词之间用 `:` 隔开，格式如下：
`项目名:业务名:类型:id`

如果 Value 是一个 Java 对象，例如一个 User 对象，则可以将对象序列化为 JSON 字符串存储：
`Heima:user:1 {"id":1, "name": "Jack", "age": 21}`

#### Hash 类型

Hash 类型也叫散列，其 value 是一个无序字典，类似于 Java 中 HashMap 结构。String 结构是对象序列化为 json 字符串存储，当需要修改对象某个字段是很不方便。

Hash 结构可以将对象中的每个字段独立存储，可以对单个字段做 CRUD。

| KEY | Field | Value |
| --- | --- | --- |
| heima:user:1 | Name | Jack |
|  | Age | 21 |
| heima:user:2 | Name | Rose |
|  | Age | 18 |

**Hash 的常见命令：**

* `HSET key field value`：添加或修改 hash 类型 key 的 field
* `HGET key field`：获取一个 hash 类型 key 的 field 的值
* `HMSET`：批量添加多个 hash 类型 key 的 field 的值
* `HMGET`：批量获取多个 hash 类型 key 的 field 的值
* `HGETALL`：获取一个 hash 类型的 key 中的所有 field 和 value
* `HKEYS`：获取一个 hash 类型的 key 中所有的 field
* `HVALS`：获取一个 hash 类型的 key 中所有的 value
* `HINCRBY`：让一个 hash 类型 key 的字段自增并指定步长
* `HSETNX`：添加一个 hash 类型的 key 的 field 值，前提是 field 不存在，否则不执行

#### List 类型

Redis 中的 list 与 Java 中的 LinkedList 类似，可以看作是一个双向链表结构，既可以支持正向检索和也可以支持反向检索。特征与 LinkedList 类似：有序，元素可以重复，插入和删除快，查询速度一般。

**List 常见命令：**

* `LPUSH key element...`：向列表左侧插入一个或多个元素（左可以看成顶）
* `LPOP key`：移除并返回列表左侧的第一个元素，没有则返回 nil
* `RPUSH key element...`：向列表右侧插入一个或多个元素
* `RPOP key`：移除并返回列表右侧的第一个元素
* `LRANGE key start end`：返回一段角标范围内所有元素
* `BLPOP` 和 `BRPOP`：与 LPOP 和 RPOP 类似，只不过在没有元素时的等待指定时间，而不是直接返回 nil

**使用场景：**

* 模拟一个栈（先进后出）：入口和出口在同一边
* 模拟一个队列（先进先出）：入口和出口在不同边
* 模拟一个阻塞队列：入口和出口在不同边，出队时采用 `BLPOP` 或 `BRPOP`

#### Set 类型

Redis 的 Set 结构与 Java 中的 HashSet 类似，可以看作是一个 value 为 null 的 HashMap，因为也是一个 hash 表，因此具备与 HashSet 类似的特征：无序/元素不可重复/查找快/支持交集，并集，差集等功能。

**Set 常见命令：**

* `SADD key member...`：向 set 中添加一个或多个元素
* `SREM key member...`：移除 set 中的指定元素
* `SCARD key`：返回 set 中元素的个数
* `SISMEMBER key member`：判断一个元素是否存在于 set 中
* `SMEMBERS`：获取 set 中所有的元素
* `SINTER key1 key2...`：求 key1 与 key2 的交集
* `SDIFF key1 key2...`：求 key1 与 key2 的差集
* `SUNION key1 key2...`：求 key1 和 key2 的并集

#### SortedSet 类型

Redis 的 SortedSet 是一个可排序的 set 集合，与 Java 中的 TreeSet 有些类似，但底层数据结构却差别很大。SortedSet 中的每一个元素都带有 score 属性，可以基于 score 属性对元素排序，底层的实现是一个跳表（SkipList）加 hash 表。SortedSet 具备下列特性：可排序/元素不重复/查询速度快，经常被用来做排行榜这样的功能。

**SortedSet 常见命令：**

* `ZADD key score member`：添加一个或多个元素到 sorted set，如果已经存在则更新其 score 值
* `ZREM key member`：删除 sorted set 中的一个指定元素
* `ZSCORE key member`：获取 sorted set 中的指定元素的 score 值
* `ZRANK key member`：获取 sorted set 中的元素排名
* `ZCOUNT key min max`：统计 score 在给定范围内所有元素的个数
* `ZINCRBY key increment member`：让 sorted set 中的指定元素自增，步长为指定的 increment 值
* `ZRANGE key min max`：按照 score 排序后，获取指定排名范围内的元素
* `ZDIFF`, `ZINTER`, `ZUNION`：求差集，交集，并集

**SortedSet 命令练习：**

将班级的下列学生得分存入 Redis 的 SortedSet 中：
Jack 85, Lucy 89, Rose 82, Tom 95, Jerry 78, Amy 92, Miles 76

```bash
ZADD stus 85 Jack 89 Lucy 82 Rose 95 Tom 78 Jerry 92 Amy 76 Miles

```

并实现下列功能：

```bash
# 删除Tom同学
ZREM stus Tom
# 获取Amy同学的分数
ZSCORE stus Amy
# 获取Rose同学的排名
ZREVRANK stus Rose
# 查询80分以下有几个学生
ZCOUNT stus 0 80
# 给Amy同学加2分
ZINCRBY stus 2 Amy
# 查出成绩前3名的同学
ZREVRANGE stus 0 2
# 查出成绩80分以下的所有同学
ZRANGEBYSCORE stus 0 80

```

### Redis 的 Java 客户端

* **Jedis**：以 Redis 命令作为方法名称，学习成本低，简单实用，但是 Jedis 实例是线程不安全的，多线程环境下需要基于连接池使用。
* **Lettuce**：基于 Netty 实现的，支持同步异步和响应式编程方式，并且是线程安全的，支持 Redis 的哨兵模式，集群模式和管道模式。
* **Redisson**：基于 Redis 实现的分布式，可伸缩地 Java 数据结构集合，包含了 Map，Queue，Lock，Semaphore，AtomicLong 等强大功能。

#### Jedis

##### 快速入门

**引入依赖**

```xml
<dependency>
    <groupId>com.heima</groupId>
    <artifactId>redis-demo</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>redis-demo</name>
</dependency>

```

**建立连接**

```java
private Jedis jedis;

@BeforeEach
void setup(){
    // 建立连接
    jedis = new Jedis("192.169.88.130", 6379);
    // 设置密码
    jedis.auth("123321");
    // 选择库
    jedis.select(0);
}

```

**测试 String, Hash**

```java
@Test
void testString(){
    // 存入数据
    String result = jedis.set("name","zhangsan");
    System.out.println("result=" + result);
    // 读取数据
    String name = jedis.get("name");
    System.out.println("name = " + name);
}

@Test
void testHash(){
    // 存入数据
    jedis.hset("user:1","zhangsan","Jack");
    jedis.hset("user:1","age","21");

    // 读取数据
    Map<String,String> map = jedis.hgetAll("user:1");
    System.out.println(map);
}

```

**释放资源**

```java
@AfterEach
void tearDown(){
    if(jedis != null){
        jedis.close(); 
    }  
}

```

##### Jedis 连接池

Jedis 本身是线程不安全的，并且频繁的创建和销毁连接会有性能损耗，因此推荐使用 Jedis 连接池代替 Jedis 的直连方式。

```java
public class JedisConnectionFactory {
    private static final JedisPool jedisPool;

    static {
        // 配置连接池
        JedisPoolConfig poolConfig = new JedisPoolConfig();
        poolConfig.setMaxTotal(8);
        poolConfig.setMaxIdle(8);
        poolConfig.setMinIdle(0);
        poolConfig.setMaxWaitMillis(1000);

        // 创建JedisPool连接池
        jedisPool = new JedisPool(poolConfig,
                "192.168.88.130", 6379, 1000, "123456");
    }

    public static Jedis getJedis() {
        return jedisPool.getResource();
    }
}

```

**修改建立连接方式**

```java
void setup(){
    // 建立连接
    // jedis = new Jedis("192.169.88.130",6379);
    jedis = JedisConnectionFactory.getJedis();
    // 设置密码
    jedis.auth("123321");
    // 选择库
    jedis.select(0);
}

```

#### SpringDataRedis

SpringData 是 Spring 中数据操作的模块，包含对各种数据库的集成，其中对 redis 的集成模块叫做 SpringDataRedis，提供了 RedisTemplate 统一 API 来操作 Redis，支持 Redis 的发布订阅模型/哨兵和集群，支持基于 Lettuce 的响应式编程。

##### SpringDataRedis 快速入门

SpringDataRedis 中提供了 RedisTemplate 工具类，其中封装了各种对 Redis 的操作，并且将不同数据类型的操作 API 封装到了不同的类型中。

| API | 返回值类型 | 说明 |
| --- | --- | --- |
| `redisTemplate.opsForValue()` | `ValueOperations` | 操作 String 类型的数据 |
| `redisTemplate.opsForHash()` | `HashOperations` | 操作 Hash 类型数据 |
| `redisTemplate.opsForList()` | `ListOperations` | 操作 List 类型数据 |
| `redisTemplate.opsForSet()` | `SetOperations` | 操作 Set 类型数据 |
| `redisTemplate.opsForZSet()` | `ZSetOperations` | 操作 SortedSet 类型数据 |
| `redisTemplate` |  | 通用的命令 |

SpringBoot 已经提供了对 SpringDataRedis 的支持，使用非常简单。

**引入依赖**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-pool2</artifactId>
</dependency>

```

**配置文件 application.yaml**

```yaml
spring:
  redis:
    host: 192.168.150.101
    port: 6379
    password: 123321
    lettuce:
      pool:
        max-active: 8
        max-idle: 8
        min-idle: 0
        max-wait: 100ms

```

**注入 RedisTemplate**

```java
@SpringBootTest
class RedisDemoApplicationTests {

    @Autowired
    private RedisTemplate<String,Object> redisTemplate;
}

```

**编写测试**

```java
@Test
void testString() {
    // 写入一条String数据
    redisTemplate.opsForValue().set("name", "虎哥");
    // 获取string数据
    Object name = redisTemplate.opsForValue().get("name");
    System.out.println("name = " + name);
}

@Test
void testSaveUser() {
    // 写入数据
    redisTemplate.opsForValue().set("user:100", new User("虎哥", 21));
    // 获取数据
    User o = (User) redisTemplate.opsForValue().get("user:100");
    System.out.println("o = " + o);
}

```

RedisTemplate 可以接收 Object 作为值，只不过写入前会把 Object 序列化为字节形式，默认是采用 JDK 序列化（虎哥会乱码），造成可读性差，内存占用较大。

##### 自定义 RedisTemplate

可以自定义 RedisTemplate 的序列化方式，使用 json 序列化。

**RedisConfig**

```java
@Configuration
public class RedisConfig {

    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory){
        // 创建RedisTemplate对象
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        // 设置连接工厂
        template.setConnectionFactory(connectionFactory);
        // 创建JSON序列化工具
        GenericJackson2JsonRedisSerializer jsonRedisSerializer = new GenericJackson2JsonRedisSerializer();
        // 设置Key的序列化
        template.setKeySerializer(RedisSerializer.string());
        template.setHashKeySerializer(RedisSerializer.string());
        // 设置Value的序列化
        template.setValueSerializer(jsonRedisSerializer);
        template.setHashValueSerializer(jsonRedisSerializer);
        // 返回
        return template;
    }
}

```

尽管 json 的序列化方式可以满足我们的要求，但依然存在一些问题，为了在反序列化时知道对象的类型，json 序列化器会将类的 class 类型写入 json 结果中，存入 Redis，会带来额外的内存开销。

为了节省内存空间，我们并不会使用 JSON 序列化器来处理 Value，而是统一使用 String 序列化器，要求只能存储 String 类型的 key 和 value，当需要存储 Java 对象时，手动完成对象的序列化和反序列化。

Spring 默认提供了一个 **StringRedisTemplate** 类，它的 key 和 value 的序列化默认就是 String 方式，省去自定义 RedisTemplate 的过程（需要手动完成对象的序列化与反序列化）。

```java
@SpringBootTest
class RedisStringTests {

    @Autowired
    private StringRedisTemplate stringRedisTemplate;
    
    @Test
    void testString() {
        // 写入一条String数据
        stringRedisTemplate.opsForValue().set("verify:phone:13600527634", "124143");
        // 获取string数据
        Object name = stringRedisTemplate.opsForValue().get("name");
        System.out.println("name = " + name);
    }

    private static final ObjectMapper mapper = new ObjectMapper();

    @Test
    void testSaveUser() throws JsonProcessingException {
        // 创建对象
        User user = new User("虎哥", 21);
        // 手动序列化
        String json = mapper.writeValueAsString(user);
        // 写入数据
        stringRedisTemplate.opsForValue().set("user:200", json);

        // 获取数据
        String jsonUser = stringRedisTemplate.opsForValue().get("user:200");
        // 手动反序列化
        User user1 = mapper.readValue(jsonUser, User.class);
        System.out.println("user1 = " + user1);
    }

    @Test
    void testHash() {
        stringRedisTemplate.opsForHash().put("user:400", "name", "虎哥");
        stringRedisTemplate.opsForHash().put("user:400", "age", "21");

        Map<Object, Object> entries = stringRedisTemplate.opsForHash().entries("user:400");
        System.out.println("entries = " + entries);
    }
}

```

---

## 实战篇-黑马点评

> 注：redis客户机开机时候输入
> `redis-cli -h 192.168.88.130 -p 6379 -a 050606`
> `config set requirepass ''`

### 短信登录

Redis 的共享 session 应用。

#### 导入黑马点评项目

用户表/用户详情表/商户信息表/商户类型表/用户日记表/用户关注表/优惠券表/优惠券的订单表。
导入项目源码，修改 `application.yaml` 中的 mysql redis 等地址信息。
启动项目后在浏览器中访问 `localhost:8081/shop-type/list`，如果可以看到数据则证明运行没有问题。

**运行前端项目**
在 nginx 所在目录下打开一个 CMD 窗口，输入命令：
`start nginx.exe`
打开 chrome 浏览器，在空白页面点击鼠标右键选择检查-打开开发者工具：打开手机模式：访问 `localhost:8080` 即可看到页面，且可以看到前后端已经实现通信。

#### 基于 Session 实现登录

##### 发送短信验证码

* 请求方式：POST
* 请求路径：`/user/code`
* 请求参数：phone，电话号码
* 返回值：无

**UserController**

```java
@PostMapping("code")
public Result sendCode(@RequestParam("phone") String phone, HttpSession session) {
    // 发送短信验证码并保存验证码
    return userService.sendCode(phone, session);
}

```

**IUserService**

```java
public interface IUserService extends IService<User> {
    Result sendCode(String phone, HttpSession session);
}

```

**UserServiceImpl 实现类：**

```java
@Override
public Result sendCode(String phone, HttpSession session) {
    //1.校验手机号
    if (RegexUtils.isPhoneInvalid(phone)) {
        //2.如果不符合，返回错误信息
        return Result.fail("手机号格式错误！");
    }
    //3.符合，生成验证码
    String code = RandomUtil.randomNumbers(6);

    //4.保存验证码到session
    session.setAttribute("code", code);
    //5.发送验证码
    log.debug("发送验证码成功，验证码：{}", code);
    //返回ok
    return Result.ok();
}

```

##### 短信验证码登录注册

**UserController**

```java
/**
 * 登录功能
 * @param loginForm 登录参数，包含手机号、验证码；或者手机号、密码
 */
@PostMapping("/login")
public Result login(@RequestBody LoginFormDTO loginForm, HttpSession session){
    // 实现登录功能
    return userService.login(loginForm , session);
}

```

**UserServiceImpl**

```java
@Override
public Result login(LoginFormDTO loginForm, HttpSession session) {
    //1.校验手机号
    String phone = loginForm.getPhone();
    if (RegexUtils.isPhoneInvalid(phone)) {
        //如果不符合，返回错误信息
        return Result.fail("手机号格式错误！");
    }
    //2.校验验证码
    Object cacheCode = session.getAttribute("code");
    String code = loginForm.getCode();
    if (cacheCode == null || !cacheCode.toString().equals(code)) {
        //3.不一致，报错
        return Result.fail("验证码错误");
    }

    //4.一致，根据手机号查询用户 select * from user where phone = ?
    User user = query().eq("phone", phone).one();

    //5.判断用户是否存在
    if (user == null) {
        //6.不存在创建新用户并保存
        user = createUserWithPhone(phone);
    }

    //7.保存用户信息到session中
    session.setAttribute("user", NamedObject.user);
    return null;
}

private User createUserWithPhone(String phone) {
    //1.创建用户
    User user = new User();
    user.setPhone(phone);
    user.setNickName(USER_NICK_NAME_PREFIX + RandomUtil.randomString(10));
    //2.保存用户
    save(user);
    return user;
}

```

##### 登录校验功能

由于多个控制器需要校验的登录状态，所以可以将其写到拦截器中。

**LoginInterceptor**

```java
public class LoginInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        //1.获取session
        HttpSession session = request.getSession();
        //2.获取session中的用户
        Object user = session.getAttribute("user");
        //3.判断用户是否存在
        if (user == null) {
            //4.不存在，拦截
            response.setStatus(401);
            return false;
        }
        //5.存在，保存用户信息到ThreadLocal
        UserHolder.saveUser((UserDTO) user);
        //6.放行
        return true;

    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        UserHolder.removeUser();
    }
}

```

**MvcConfig 配置拦截器的拦截对象**

```java
@Configuration
public class MvcConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LoginInterceptor())
                .excludePathPatterns(
                        "/user/code",
                        "/user/login",
                        "/blog/hot",
                        "/shop/**",
                        "/shop-type/**",
                        "/upload/**",
                        "/voucher/**"
                );
    }
}

```

**UserController 实现返回主页**

```java
@GetMapping("/me")
public Result me(){
    // 获取当前登录的用户并返回
    UserDTO user = UserHolder.getUser();
    return Result.ok(user);
}

```

##### UserDTO 实现用户敏感信息隐藏

```java
@Data
public class UserDTO {
    private Long id;
    private String nickName;
    private String icon;
}

```

**UserServiceImpl 修改：** 对保存到 session 中的内容进行隐藏。

```java
//7.保存用户信息到session中
session.setAttribute("user", BeanUtil.copyProperties(user, UserDTO.class));
return Result.ok();

```

#### 集群的 Session 共享问题

多台 Tomcat 并不共享 session 存储空间，当要求切换到不同 tomcat 服务时导致数据丢失的问题。
Session 的替代方案应该满足：数据共享，内存存储，key/value 结构。

#### 基于 Redis 实现共享 session 登录

校验登录状态：`LoginInterceptor`
短信验证码登录，注册：`UserServiceImpl`

不可以 code 作为 key，是因为每个用户浏览器都有不同的 session，存储本地，不会互相干扰，但是 redis 是共享机制，存储服务器，可能会覆盖，所以以 phone 作为 key，以手机号为 key 读取验证码。

Uuid 生成随机字符串 token，存储用户信息，登录注册返回 token 给客户端，然后校验登录状态的时候请求并携带 token 携带用户信息（鉴权）。前端将 token 写入 authorization 头中，如果直接将手机号作为键值保存在前端可能有泄露风险。

**UserServiceImpl**

```java
@Slf4j
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements IUserService {

    @Resource
    private StringRedisTemplate stringRedisTemplate;

    @Override
    public Result sendCode(String phone, HttpSession session) {
        //1.校验手机号
        if (RegexUtils.isPhoneInvalid(phone)) {
            //2.如果不符合，返回错误信息
            return Result.fail("手机号格式错误！");
        }
        //3.符合，生成验证码
        String code = RandomUtil.randomNumbers(6);

        //4.保存验证码到redis
        stringRedisTemplate.opsForValue().set(LOGIN_CODE_KEY + phone, code,LOGIN_CODE_TTL, TimeUnit.MINUTES);

        //5.发送验证码
        log.debug("发送验证码成功，验证码：{}", code);
        //返回ok
        return Result.ok();
    }
    
    @Override
    public Result login(LoginFormDTO loginForm, HttpSession session) {
        //1.校验手机号
        String phone = loginForm.getPhone();
        if (RegexUtils.isPhoneInvalid(phone)) {
            //如果不符合，返回错误信息
            return Result.fail("手机号格式错误！");
        }
        //2.从Redis中获取验证码并校验
        String cacheCode = stringRedisTemplate.opsForValue().get(LOGIN_CODE_KEY + phone);
        String code = loginForm.getCode();
        if (cacheCode == null || !cacheCode.equals(code)) {
            //3.不一致，报错
            return Result.fail("验证码错误");
        }

        //4.一致，根据手机号查询用户 select * from user where phone = ?
        User user = query().eq("phone", phone).one();

        //5.判断用户是否存在
        if (user == null) {
            //6.不存在创建新用户并保存
            user = createUserWithPhone(phone);
        }

        //7.保存用户信息到Redis中
        //7.1.随机生成token，作为登录令牌
        String token = UUID.randomUUID().toString(true);
        //7.2.将User对象转为HashMap存储
        UserDTO userDTO = BeanUtil.copyProperties(user, UserDTO.class);
        Map<String, Object> userMap = BeanUtil.beanToMap(userDTO, new HashMap<>(),
                CopyOptions.create()
                        .setIgnoreNullValue(true)
                        .setFieldValueEditor((fieldName,fieldValue) -> fieldValue.toString()));
        //7.3.存储
        String tokenKey = LOGIN_USER_KEY + token;
        stringRedisTemplate.opsForHash().putAll(tokenKey, userMap);
        stringRedisTemplate.expire(tokenKey , LOGIN_USER_TTL, TimeUnit.MINUTES);

        //8.返回token
        return Result.ok(token);
    }
}

```

**LoginInterceptor**

该系统采用无状态的 Token 认证机制，使用 Redis 作为用户会话存储，替代传统的 Session 机制。

* **核心流程**：
1. **发送验证码**：首先验证手机号格式是否正确，生成 6 位随机数字验证码。将验证码以 `login:code:{手机号}` 为键存储到 Redis 中，设置 5 分钟过期时间，记录日志并返回成功状态。
2. **用户登录**：验证手机号格式，从 Redis 中获取之前发送的验证码进行比对，验证码正确后，查询数据库中该手机号对应的用户，如果用户不存在，则自动创建新用户（设置默认昵称），生成唯一的 UUID 作为登录 Token，将用户信息转换为 Map 结构，存储到 Redis 中，键为 `login:token:{token}` 设置 Token 过期时间（30 分钟），实现自动登录超时，返回 Token 给前端用于后续身份认证。



```java
public class LoginInterceptor implements HandlerInterceptor {

    private StringRedisTemplate stringRedisTemplate;

    public LoginInterceptor(StringRedisTemplate stringRedisTemplate) {
        this.stringRedisTemplate = stringRedisTemplate;
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        //1.获取请求头中的token
        String token = request.getHeader("authorization");
        if(StrUtil.isBlank(token)){
            //不存在拦截，返回401状态码
            response.setStatus(401);
            return false;
        }
        //2.基于TOKEN获取Redis中的用户
        String key = RedisConstants.LOGIN_USER_KEY + token;
        Map<Object, Object> userMap = stringRedisTemplate.opsForHash()
                .entries(key);
        //3.判断用户是否存在
        if (userMap.isEmpty()) {
            //4.不存在，拦截
            response.setStatus(401);
            return false;
        }
        //5.将查询到的Hash数据转为UserDTO对象
        UserDTO userDTO = BeanUtil.fillBeanWithMap(userMap, new UserDTO(), false);

        //6..存在，保存用户信息到ThreadLocal
        UserHolder.saveUser(userDTO);

        //7.刷新token有效期
        stringRedisTemplate.expire(key, RedisConstants.LOGIN_USER_TTL, TimeUnit.MINUTES);

        //8.放行
        return true;

    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        UserHolder.removeUser();
    }
}

```

这段代码实现了一个登录拦截器，这里不能使用 resource 的方式注入，是因为这个类不是由 spring 创建的对象。

* **请求拦截验证**：从 HTTP 请求头中获取 "authorization" 字段作为 Token，如果 Token 为空或不存在，直接返回 401 未授权状态码，拒绝访问。
* **Redis 用户信息查询**：使用 Token 拼接 Redis 键前缀，通过 `opsForHash().entries(key)` 获取存储在 Redis 中的用户数据 Map。
* **用户信息处理**：使用 Hutool 工具的方法将 Redis 中存储的 Map 数据转换为 UserDTO 对象，保存到 ThreadLocal 中。
* **会话有效期管理**：每次成功验证后，通过 `expire()` 方法刷新 Token 在 Redis 中的过期时间。
* **资源清理**：在请求处理完成后，清理 ThreadLocal 中的用户信息，避免内存泄漏。

#### 登录拦截器的优化

现在拦截器作用（获取 token，查询 Redis 的用户不存在则拦截，存在则继续，保存到 ThreadLocal，刷新 token 有效期）的位置是需要登陆的路径，但是如果用户访问的是不需要登录的路径，那么拦截器不会成功拦截。在这之前在嵌套一个拦截一切路径的拦截器完成（获取 token，查询 redis 用户，保存到 ThreadLocal，刷新 token 有效期，放行），第二个拦截器（原来的拦截器）的功能变成了查询 Threadlocal 的用户，不存在则拦截，存在则继续。

**RefreshTokenInterceptor** 负责拦截全部

```java
public class RefreshTokenInterceptor implements HandlerInterceptor {

    private StringRedisTemplate stringRedisTemplate;

    public RefreshTokenInterceptor(StringRedisTemplate stringRedisTemplate) {
        this.stringRedisTemplate = stringRedisTemplate;
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        // 1.获取请求头中的token
        String token = request.getHeader("authorization");
        if (StrUtil.isBlank(token)) {
            return true;
        }
        // 2.基于TOKEN获取redis中的用户
        String key  = LOGIN_USER_KEY + token;
        Map<Object, Object> userMap = stringRedisTemplate.opsForHash().entries(key);
        // 3.判断用户是否存在
        if (userMap.isEmpty()) {
            return true;
        }
        // 5.将查询到的hash数据转为UserDTO
        UserDTO userDTO = BeanUtil.fillBeanWithMap(userMap, new UserDTO(), false);
        // 6.存在，保存用户信息到 ThreadLocal
        UserHolder.saveUser(userDTO);
        // 7.刷新token有效期
        stringRedisTemplate.expire(key, LOGIN_USER_TTL, TimeUnit.MINUTES);
        // 8.放行
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        // 移除用户
        UserHolder.removeUser();
    }
}

```

**LoginInterceptor**

```java
public class LoginInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        // 1.判断是否需要拦截（ThreadLocal中是否有用户）
        if (UserHolder.getUser() == null) {
            // 没有，需要拦截，设置状态码
            response.setStatus(401);
            // 拦截
            return false;
        }
        // 有用户，则放行
        return true;
    }
}

```

**MvcConfig**

```java
@Configuration
public class MvcConfig implements WebMvcConfigurer {

    @Resource
    private StringRedisTemplate stringRedisTemplate;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 登录拦截器
        registry.addInterceptor(new LoginInterceptor())
                .excludePathPatterns(
                        "/user/code",
                        "/user/login",
                        "/blog/hot",
                        "/shop/**",
                        "/shop-type/**",
                        "/upload/**",
                        "/voucher/**"
                ).order(1);
        // token刷新的拦截器
        registry.addInterceptor(new RefreshTokenInterceptor(stringRedisTemplate)).addPathPatterns("/**").order(0);
    }
}

```

配置 token，使用 `.order` 配置顺序。

### 商户查询缓存

企业的缓存使用技巧，缓存雪崩，穿透等问题解决。

#### 缓存概念

* 缓存就是数据交换的缓冲区（cache），是存贮数据的临时地方，一般读写性能较高。
* 浏览器缓存 - 应用层缓存 - 数据层缓存 - CPU 缓存 - 磁盘缓存。
* 缓存的作用：降低后端负载，提高读写效率，降低响应时间，应对高并发问题。
* 缓存的成本：数据一致性成本，代码维护成本，运维成本。

#### 添加 Redis 缓存

**ShopController**

```java
@GetMapping("/{id}")
public Result queryShopById(@PathVariable("id") Long id) {
    return shopService.queryById(id);
}

```

**IShopService**

```java
public interface IShopService extends IService<Shop> {
    Result queryById(Long id);
}

```

**ShopServiceImpl**

```java
@Service
public class ShopServiceImpl extends ServiceImpl<ShopMapper, Shop> implements IShopService {

    @Resource
    private StringRedisTemplate stringRedisTemplate;

    @Override
    public Result queryById(Long id) {
        String key = CACHE_SHOP_KEY + id;
        //1.从redis查询商铺缓存
        String shopJson = stringRedisTemplate.opsForValue().get(CACHE_SHOP_KEY+ id);
        //2.判断是否存在
        if (StrUtil.isNotBlank(shopJson)) {
            //3.存在，返回
            Shop shop = JSONUtil.toBean(shopJson, Shop.class);
            return Result.ok(shop);
        }
        //4.不存在，根据id查询数据库
        Shop shop = getById(id);
        //5.不存在，返回错误
        if (shop == null) {
            return Result.fail("店铺不存在");
        }
        //6.存在，写入redis
        stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(shop));
        //7.返回
        return Result.ok(shop);
    }
}

```

类型转换：这是因为 Redis 只能存储字符串类型的数据，而我们的应用程序需要使用 Java 对象。

#### 缓存更新策略

|  | 内存淘汰 | 超时剔除 | 主动更新 |
| --- | --- | --- | --- |
| **说明** | 不用自己维护，利用 redis 的内存淘汰机制，当内存不足时自动淘汰部分数据，下次查询时更新缓存 | 给缓存数据添加 TTL 时间，到期后自动删除缓存，下次查询时更新缓存 | 编写业务逻辑，在修改数据库的同时更新缓存 |
| **一致性** | 差 | 一般 | 好 |
| **维护成本** | 无 | 低 | 高 |

**业务场景：**

* 低一致性需求：存在内存淘汰机制，例如店铺类型的查询缓存。
* 高一致性需求：主动更新，并以超时剔除作为兜底方案，例如店铺详情查询的缓存。

##### 主动更新策略

1. **Cache Aside Pattern**：由缓存的调用者，在更新数据库的同时更新缓存。
2. **Read/Write Through Pattern**：缓存与数据库整合为一个服务，由服务来维持一致性，调用者调用该服务，无需关心缓存一致性问题。
3. **Write Behind Caching Pattern**：调用者只操作缓存，由其他线程异步的将缓存数据持久化到数据库，保证最终一致。

一般偏向于先操作数据库，再删除缓存。

##### 缓存更新策略的最佳方案

* **低一致性需求**：使用 Redis 自带的内存淘汰机制。
* **高一致性需求**：主动更新，并以超时剔除作为兜底方案。
* **读操作**：缓存命中则返回；缓存未命中则查询数据库，并写入缓存，设定超时时间。
* **写操作**：先写数据库，然后再删除缓存；要确保数据库与缓存操作的原子性。



##### 给查询商铺的缓存添加超时剔除和主动更新的策略

修改 ShopController 中的业务逻辑，满足下面要求：

* 根据 id 查询店铺时，如果缓存未命中，则查询数据库，将数据库结果写入缓存，并设置超时时间。
* 根据 id 修改店铺时，先修改数据库，再删除缓存。

#### 缓存穿透

缓存穿透是指客户端请求的数据在缓存中和数据库中都不存在，这样缓存永远不会生效，这些请求都会打到数据库。

常见的解决方案有两种：

1. **缓存空对象**：实现简单，维护方便，但有额外的内存消耗（设置短 ttl），可能造成短期的不一致。
2. **布隆过滤**：在客户端和 redis 之间加入布隆过滤器，先请求布隆过滤器，不存在则拒绝。内存占用较少，没有多余 key，但实现复杂，存在误判可能。

##### 使用缓存空对象

```java
@Override
public Result queryById(Long id) {
    String key = CACHE_SHOP_KEY + id;
    //1.从redis查询商铺缓存
    String shopJson = stringRedisTemplate.opsForValue().get(key);
    //2.判断是否存在
    if (StrUtil.isNotBlank(shopJson)) {
        //3.存在，返回
        Shop shop = JSONUtil.toBean(shopJson, Shop.class);
        return Result.ok(shop);
    }
    //判断命中的是否是空值
    if (shopJson != null){
        //返回错误信息
        return Result.fail("店铺不存在");
    }
    //4.不存在，根据id查询数据库
    Shop shop = getById(id);
    //5.不存在，返回错误
    if (shop == null) {
        //将空值写入redis中
        stringRedisTemplate.opsForValue().set(key,"",CACHE_NULL_TTL, TimeUnit.MINUTES);
        return Result.fail("店铺不存在");
    }
    //6.存在，写入redis
    stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(shop),CACHE_SHOP_TTL, TimeUnit.MINUTES);
    //7.返回
    return Result.ok(shop);
}

```

* `StrUtil.isNotBlank(shopJson)`: 当 shopJson 为 null 时返回 false；当 shopJson 为 "" (空字符串) 时返回 false；当 shopJson 为有效的 JSON 字符串时返回 true。
* `shopJson != null`: 当 shopJson 不为 null 时（即为 "" 空字符串），说明这是之前缓存的"不存在"标记；当 shopJson 为 null 时，说明 Redis 中没有这个键。

#### 缓存雪崩

* 缓存雪崩是指同一时段大量的缓存 key 同时失效或者 redis 服务宕机，导致大量请求到达数据库，带来巨大压力。
* **解决方案**：
* 给不同的 key 的 TTL 添加随机值。
* 利用 redis 集群提高服务的可用性。
* 给缓存业务添加降级限流策略。
* 给业务添加多级缓存。



#### 缓存击穿

缓存击穿问题也叫热点 key 问题，就是一个被高并发访问并且缓存重建业务较复杂的 key 突然失效了，无效的请求访问会在瞬间给数据库带来巨大的冲击。

**常见解决方案：**

* **互斥锁**：没有额外的内存消耗，保证一致性，实现简单；但线程需要等待，性能受影响，可能有死锁风险。
* **逻辑过期**：线程无需等待，性能较好；但不保证一致性，有额外内存消耗，实现复杂。

##### 基于互斥锁方式解决缓存击穿问题

需求：修改根据 id 查询商铺的业务，基于互斥锁方式来解决缓存击穿问题。

```java
@Override
public Result queryById(Long id) {
    //缓存穿透
    //Shop shop = queryWithPassThrough(id);

    //互斥锁解决缓存击穿
    Shop shop = queryWithMutex(id);
    if (shop == null) {
        return Result.fail("店铺不存在");
    }
    //返回
    return Result.ok(shop);
}

public Shop queryWithMutex(Long id){
    String key = CACHE_SHOP_KEY + id;
    //1.从redis查询商铺缓存
    String shopJson = stringRedisTemplate.opsForValue().get(key);
    //2.判断是否存在
    if (StrUtil.isNotBlank(shopJson)) {
        //3.存在，返回
        Shop shop = JSONUtil.toBean(shopJson, Shop.class);
        return shop;
    }
    //判断命中的是否是空值
    if (shopJson != null){
        //返回错误信息
        return null;
    }

    //4.实现缓存重建
    //4.1获取互斥锁
    String lockKey = "lock:shop:" + id;
    Shop shop = null;
    try {
        boolean isLock = tryLock(lockKey);
        //4.2判断是否获取成功
        if(!isLock){
            //4.3失败，则休眠并重试
            Thread.sleep(50);
            return queryWithMutex(id);
        }
        //4.4成功，根据id查询数据库
        shop = getById(id);
        //模拟重建的延迟
        Thread.sleep(200);
        //5.不存在，返回错误
        if (shop == null) {
            //将空值写入redis中
            stringRedisTemplate.opsForValue().set(key,"",CACHE_NULL_TTL, TimeUnit.MINUTES);
            return null;
        }
        //6.存在，写入redis
        stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(shop),CACHE_SHOP_TTL, TimeUnit.MINUTES);
    } catch (InterruptedException e) {
        throw new RuntimeException(e);
    }finally {
        //7.释放互斥锁
        unLock(lockKey);
    }
    //8返回
    return shop;
}

```

这种机制确保了在高并发场景下，当缓存失效时只有一个线程去查询数据库并重建缓存，其他线程等待后直接从缓存获取数据，有效防止了缓存击穿问题。

##### 基于逻辑过期方式解决缓存击穿问题

逻辑过期不是真正意义上的物理过期，所以保存到 redis 中的数据会永久有效。通过程序员手动的删除来取消，所以要进行缓存预热热点数据。

需求：修改根据 id 查询商铺的业务，基于逻辑过期方式来解决缓存击穿问题。

```java
public void saveShop2Redis(Long id, Long expireSeconds) throws InterruptedException {
    //1.查询店铺数据
    Shop shop = getById(id);
    Thread.sleep(200);
    //2.封装成逻辑过期
    RedisData redisData = new RedisData();
    redisData.setData(shop);
    redisData.setExpireTime(LocalDateTime.now().plusSeconds(expireSeconds));
    //3.写入Redis
    stringRedisTemplate.opsForValue().set(CACHE_SHOP_KEY + id, JSONUtil.toJsonStr(redisData));
}

public Shop queryWithLogicalExpire(Long id){
    String key = CACHE_SHOP_KEY + id;
    //1.从redis查询商铺缓存
    String shopJson = stringRedisTemplate.opsForValue().get(key);
    //2.判断是否存在
    if (StrUtil.isBlank(shopJson)) {
        //3.存在，返回
        return null;
    }
    //命中，需要先把json反序列化为对象
    RedisData redisData = JSONUtil.toBean(shopJson, RedisData.class);
    JSONObject data = (JSONObject) redisData.getData();
    Shop shop = JSONUtil.toBean(data, Shop.class);
    LocalDateTime expireTime = redisData.getExpireTime();

    //5.判断是否过期
    if(expireTime.isAfter(LocalDateTime.now())){
        //5.1未过期，直接返回店铺信息
        return shop;
    }

    //5.2已过期，需要缓存重建
    //6.缓存重建
    //6.1获取互斥锁
    String lockKey = LOCK_SHOP_KEY + id;
    boolean isLock = tryLock(lockKey);
    //6.2判断是否获取锁成功
    if (isLock) {
        //6.3成功，开启独立线程，实现缓存重建
        CACHE_REBUILD_EXECUTOR.submit(() -> {
            try {
                this.saveShop2Redis(id, 20L);
            } catch (Exception e) {
                throw new RuntimeException(e);
            } finally {
                //释放锁
                unLock(lockKey);
            }
        });
    }

    //6.4返回商铺信息
    return shop;
}

```

#### 缓存工具封装

基于 StringRedisTemplate 封装一个缓存工具类，满足下列需求：

* 将任意 java 对象序列化为 json 并存储在 string 类型的 key 中，并且可以设置 TTL 过期时间。
* 将任意 java 对象序列化为 json 并存储在 string 类型的 key 中，并且可以设置逻辑过期时间，用于处理缓存击穿问题。
* 根据指定的 key 查询缓存，并反序列化为指定类型，利用缓存空值的方式解决缓存穿透问题。
* 根据指定的 key 查询缓存，并反序列化为指定类型，需要利用逻辑过期解决缓存击穿问题。

**CacheClient**

```java
@Component
public class CacheClient {

    private StringRedisTemplate stringRedisTemplate;

    public CacheClient(StringRedisTemplate stringRedisTemplate) {
        this.stringRedisTemplate = stringRedisTemplate;
    }

    public void set(String key, Object value, Long time, TimeUnit unit) {
        stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(value), time, unit);
    }

    public void setWithLogicalExpire(String key, Object value, Long time, TimeUnit unit) {
        //设置逻辑过期
        RedisData redisData = new RedisData();
        redisData.setData(value);
        redisData.setExpireTime(LocalDateTime.now().plusSeconds(unit.toSeconds(time)));

        //写入redis
        stringRedisTemplate.opsForValue().set(key, JSONUtil.toJsonStr(redisData));
    }

    public <R,ID> R queryWithPassThrough(String keyPrefix,ID id , Class<R> type, Function<ID,R> dbFallback, Long time, TimeUnit unit){
        String key = keyPrefix + id;
        //1.从redis查询商铺缓存
        String json = stringRedisTemplate.opsForValue().get(key);
        //2.判断是否存在
        if (StrUtil.isNotBlank(json)) {
            //3.存在，返回
            Shop shop = JSONUtil.toBean(json, Shop.class);
            return JSONUtil.toBean(json,type);
        }
        //判断命中的是否是空值
        if (json != null){
            //返回错误信息
            return null;
        }
        //4.不存在，根据id查询数据库
        R r = dbFallback.apply(id);
        //5.不存在，返回错误
        if (r == null) {
            //将空值写入redis中
            stringRedisTemplate.opsForValue().set(key,"",CACHE_NULL_TTL, TimeUnit.MINUTES);
            return null;
        }
        //6.存在，写入redis
        this.set(key, r, time, unit);
        //7.返回
        return r;
    }

    private static final ExecutorService CACHE_REBUILD_EXECUTOR = Executors.newFixedThreadPool(10);

    public <R,ID> R queryWithLogicalExpire(
            String keyPrefix,ID id , Class<R> type, Function<ID,R> dbFallback, Long time, TimeUnit unit){
        String key = keyPrefix + id;
        //1.从redis查询商铺缓存
        String json = stringRedisTemplate.opsForValue().get(key);
        //2.判断是否存在
        if (StrUtil.isBlank(json)) {
            //3.存在，返回
            return null;
        }
        //命中，需要先把json反序列化为对象
        RedisData redisData = JSONUtil.toBean(json, RedisData.class);
        JSONObject data = (JSONObject) redisData.getData();
        R r = JSONUtil.toBean(data, type);
        LocalDateTime expireTime = redisData.getExpireTime();

        //5.判断是否过期
        if(expireTime.isAfter(LocalDateTime.now())){
            //5.1未过期，直接返回店铺信息
            return r;
        }

        //5.2已过期，需要缓存重建
        //6.缓存重建
        //6.1获取互斥锁
        String lockKey = keyPrefix + id;
        boolean isLock = tryLock(lockKey);
        //6.2判断是否获取锁成功
        if (isLock) {
            //6.3成功，开启独立线程，实现缓存重建
            CACHE_REBUILD_EXECUTOR.submit(() -> {
                try {
                    //查询数据库
                    R r1 = dbFallback.apply(id);
                    //写入redis
                    this.set(key, r1, time, unit);
                } catch (Exception e) {
                    throw new RuntimeException(e);
                } finally {
                    //释放锁
                    unLock(lockKey);
                }
            });
        }

        //6.4返回商铺信息
        return r;
    }
    
    private boolean tryLock(String key){
        Boolean flag = stringRedisTemplate.opsForValue().setIfAbsent(key, "1", 10, TimeUnit.SECONDS);
        return BooleanUtil.isTrue(flag);
    }

    private void unLock(String key){
        stringRedisTemplate.delete(key);
    }
}

```

### 优惠券秒杀

Redis 的计数器，Lua 脚本 Redis 分布式锁 Redis 三种消息队列。

#### 全局唯一 ID

##### 全局 ID 生成器

* 每个店铺都可以发布优惠券，当用户抢购时，就会生成订单并保存到 `tb_voucher_order` 这张表中，而订单表如果使用数据库自增 id 就存在一些问题：id 的规律性太明显，受单表数据量的限制。
* 全局 id 生成器，是一种在分布式系统下用来全局唯一 ID 的工具，一般要满足下列特性：唯一性/高可用/高性能/递增性/安全性。
* 为了增强 ID 的安全性，我们可以不直接使用 Redis 自增的数值，而是拼接一些其他信息。
* **符号位（1bit）+ 时间戳（31bit，以秒为单位） + 序列号（32bit 秒内的计数器）**

**RedisIdWorker 生成全局唯一 ID**

```java
@Component
public class RedisIdWorker {
    /**
     * 开始时间戳
     */
    private static final long BEGIN_TIMESTAMP = 1640995200L;
    /**
     * 序列号位数
     */
    private static final long COUNT_BITS = 32;

    @Resource
    private StringRedisTemplate stringRedisTemplate;

    public long nextId(String keyPrefix) {
        //1.生成时间戳
        LocalDateTime now = LocalDateTime.now();
        long nowSecond = now.toEpochSecond(ZoneOffset.UTC);
        long timestamp = nowSecond - BEGIN_TIMESTAMP;

        //2.生成序列号
        //2.1获取当前日期，精确到天
        String date = now.format(DateTimeFormatter.ofPattern("yyyyMMdd"));
        //2.2.自增长
        long count = stringRedisTemplate.opsForValue().increment("icr:" + keyPrefix + ":"+ date);

        //3.拼接返回
        return timestamp << COUNT_BITS | count ;
    }

}

```

#### 实现优惠券秒杀下单

每个店铺都可以发布优惠券，分为平价券和特价券，平价券可以任意购买，而特价券需要秒杀抢购。
表关系：`tb_voucher` 和 `tb_voucher_order`。

##### 准备优惠券秒杀的数据库功能

**VoucherServiceImpl**

```java
@Service
public class VoucherServiceImpl extends ServiceImpl<VoucherMapper, Voucher> implements IVoucherService {

    @Resource
    private ISeckillVoucherService seckillVoucherService;

    @Override
    public Result queryVoucherOfShop(Long shopId) {
        // 查询优惠券信息
        List<Voucher> vouchers = getBaseMapper().queryVoucherOfShop(shopId);
        // 返回结果
        return Result.ok(vouchers);
    }

    @Override
    @Transactional
    public void addSeckillVoucher(Voucher voucher) {
        // 保存优惠券
        save(voucher);
        // 保存秒杀信息
        SeckillVoucher seckillVoucher = new SeckillVoucher();
        seckillVoucher.setVoucherId(voucher.getId());
        seckillVoucher.setStock(voucher.getStock());
        seckillVoucher.setBeginTime(voucher.getBeginTime());
        seckillVoucher.setEndTime(voucher.getEndTime());
        seckillVoucherService.save(seckillVoucher);
    }
}

```

**VoucherController**

```java
@RestController
@RequestMapping("/voucher")
public class VoucherController {

    @Resource
    private IVoucherService voucherService;

    /**
     * 新增普通券
     * @param voucher 优惠券信息
     * @return 优惠券id
     */
    @PostMapping
    public Result addVoucher(@RequestBody Voucher voucher) {
        voucherService.save(voucher);
        return Result.ok(voucher.getId());
    }

    /**
     * 新增秒杀券
     * @param voucher 优惠券信息，包含秒杀信息
     * @return 优惠券id
     */
    @PostMapping("seckill")
    public Result addSeckillVoucher(@RequestBody Voucher voucher) {
        voucherService.addSeckillVoucher(voucher);
        return Result.ok(voucher.getId());
    }

    /**
     * 查询店铺的优惠券列表
     * @param shopId 店铺id
     * @return 优惠券列表
     */
    @GetMapping("/list/{shopId}")
    public Result queryVoucherOfShop(@PathVariable("shopId") Long shopId) {
       return voucherService.queryVoucherOfShop(shopId);
    }
}

```

##### 实现优惠券秒杀（不涉及 redis）

下单时需要判断两点：

1. 秒杀是否开始或结束，如果尚未开始，或已经结束则无法下单。
2. 库存是否充足，不足则无法下单。

```java
@Service
public class VoucherOrderServiceImpl extends ServiceImpl<VoucherOrderMapper, VoucherOrder> implements IVoucherOrderService {

    @Resource
    private ISeckillVoucherService seckillVoucherService;

    @Resource
    private RedisIdWorker redisIdWorker;

    @Override
    @Transactional
    public Result seckillVoucher(Long voucherId) {
        //1.查询优惠券
        SeckillVoucher voucher = seckillVoucherService.getById(voucherId);
        //2.判断秒杀是否开始
        if (voucher.getBeginTime().isAfter(LocalDateTime.now())) {
            //尚未开始
            return Result.fail("秒杀尚未开始!");
        }
        //3.判断秒杀是否已经结束
        if(voucher.getEndTime().isBefore(LocalDateTime.now())){
            return Result.fail("秒杀已经结束!");
        }
        //4.判断库存是否充足
        if (voucher.getStock() < 1) {
            //库存不足
            return Result.fail("库存不足!");
        }
        //5.扣减库存
        boolean success = seckillVoucherService.update()
                .setSql("stock = stock - 1")
                .eq("voucher_id", voucherId).update();
        if (!success) {
            //扣减库存失败
            return Result.fail("库存不足!");
        }
        //6.创建订单
        VoucherOrder voucherOrder = new VoucherOrder();
        //6.1订单id
        long orderId = redisIdWorker.nextId("order");
        voucherOrder.setId(orderId);
        //6.2用户id
        Long userId = UserHolder.getUser().getId();
        voucherOrder.setUserId(userId);
        //6.3代金券id
        voucherOrder.setVoucherId(voucherId);
        save(voucherOrder);

        //7.返回订单id
        return Result.ok(orderId);
    }
}

```

#### 超卖问题

* 超卖问题是典型的多线程安全问题，针对这一问题的常见解决方案就是加锁。
* **悲观锁**：认为线程安全问题一定会发生，因此在操作数据之前先获取锁，确保线程串行执行。
* **乐观锁**：认为线程安全问题不一定会发生，因此不加锁，只是在更新数据时去判断有没有其他线程对数据做了修改。
* **版本号法**：判断版本号有没有发生变化。
* **CAS 法**：compare and set，直接使用 stock 来判断。



**优化 SQL**：修改条件使得不用强制匹配 stock 等于，直接大于 stock 即可。

```java
//5.扣减库存
boolean success = seckillVoucherService.update()
        .setSql("stock = stock - 1")//set stock = stock - 1
        .eq("voucher_id", voucherId).gt("stock", 0)//where id = ? and stock > 0
        .update();

```

#### 一人一单

需求：修改秒杀业务，要求同一个优惠券，一个用户只能下一单。

```java
//5.一人一单
Long userId = UserHolder.getUser().getId();

//5.1查询订单
int count = query().eq("user_id", userId).eq("voucher_id", voucherId).count();
//5.2判断是否存在
if (count > 0) {
    //存在,用户已经购买过了
    return Result.fail("用户已经购买过一次!");
}

```

假设并发情况下数据库中完全没有订单数据，现在有 100 个订单，都来执行查询逻辑，查的 count 都是 0，都判断不成立，就会连续插入 n 条数据，但是这里查询新增数据不存在更新判断有无修改的逻辑，无法使用乐观锁，只能加悲观锁。

```java
@Transactional
public Result createVoucherOrder(Long voucherId) {
    //5.一人一单
    Long userId = UserHolder.getUser().getId();

    //5.1查询订单
    int count = query().eq("user_id", userId).eq("voucher_id", voucherId).count();
    //5.2判断是否存在
    if (count > 0) {
        //存在,用户已经购买过了
        return Result.fail("用户已经购买过一次!");
    }

    //6.扣减库存
    boolean success = seckillVoucherService.update()
            .setSql("stock = stock - 1")//set stock = stock - 1
            .eq("voucher_id", voucherId).gt("stock", 0)//where id = ? and stock > 0
            .update();
    if (!success) {
        //扣减库存失败
        return Result.fail("库存不足!");
    }
    //7.创建订单
    VoucherOrder voucherOrder = new VoucherOrder();
    //7.1订单id
    long orderId = redisIdWorker.nextId("order");
    voucherOrder.setId(orderId);
    //7.2用户id
    voucherOrder.setUserId(userId);
    //7.3代金券id
    voucherOrder.setVoucherId(voucherId);
    save(voucherOrder);

    //8.返回订单id
    return Result.ok(orderId);
}

```

**加锁细节**

如果锁整个方法 `createVoucherOrder`，来一个用户锁一个用户，性能不好，串行执行。如果锁用户 id，满足同一个用户用一把锁，不同用户不加锁。但是当 synchronize 释放锁，spring 提交 transaction 之间可以有线程进入，同样会出现并发安全问题，于是采用锁返回对象。

```java
synchronized (userId.toString().intern()) {
    //获取代理对象
    IVoucherOrderService proxy = (IVoucherOrderService) AopContext.currentProxy();
    return proxy.createVoucherOrder(voucherId);
}

```

#### 集群下的线程并发问题

通过加锁可以解决在单机情况下的一人一单安全问题，但是在集群模式下就不行了。
如果存在多个 JVM，每个 JVM 内部都有自己的锁，导致每一个锁都可以有一个线程获取，导致并行运行安全问题。
**解决**：让多个 JVM 都请求同一个锁（分布式锁）。

#### 分布式锁

满足分布式系统或集群模式下多进程可见并且互斥的锁。
特性：高可用、多进程可见、互斥、高性能、安全性。

|  | MySQL | Redis | Zookeeper |
| --- | --- | --- | --- |
| **互斥** | 利用 mysql 本身的互斥锁机制 | 利用 setnx 的互斥命令 | 利用节点的唯一性和有序性实现互斥 |
| **高可用** | 好 | 好 | 好 |
| **高性能** | 一般 | 好 | 一般 |
| **安全性** | 断开连接，自动释放锁 | 利用锁超时时间，到期释放 | 临时节点，断开连接自动释放 |

**实现分布式锁时需要实现的两个基本方法：**

* **获取锁**
* **互斥**：确保只能有一个线程获取锁（阻塞式）。`SET lock thread1 NX EX 10`
* **非阻塞**：尝试一次，成功返回 true，失败返回 false（避免死锁）。


* **释放锁**
* 手动释放（删除锁）。
* 超时释放（expire）：获取锁时添加一个超时时间。



##### 基于 Redis 实现分布式锁初级版本

需求：定义一个类，实现接口，利用 Redis 实现分布式锁功能。

```java
@Override
public Result seckillVoucher(Long voucherId) {
    //1.查询优惠券
    SeckillVoucher voucher = seckillVoucherService.getById(voucherId);
    //2.判断秒杀是否开始
    if (voucher.getBeginTime().isAfter(LocalDateTime.now())) {
        return Result.fail("秒杀尚未开始!");
    }
    //3.判断秒杀是否已经结束
    if(voucher.getEndTime().isBefore(LocalDateTime.now())){
        return Result.fail("秒杀已经结束!");
    }
    //4.判断库存是否充足
    if (voucher.getStock() < 1) {
        return Result.fail("库存不足!");
    }

    Long userId = UserHolder.getUser().getId();
    //创建锁对象
    SimpleRedisLock lock = new SimpleRedisLock("order:" + userId, stringRedisTemplate);
    //获取锁
    boolean isLock = lock.tryLock(1200);
    //判断获取锁成功
    if (!isLock) {
        //获取锁失败，返回错误或重试
        return Result.fail("不允许重复下单!");
    }
    try {
        //获取代理对象
        IVoucherOrderService proxy = (IVoucherOrderService) AopContext.currentProxy();
        //8.返回订单id
        return proxy.createVoucherOrder(voucherId);
    } finally {
        //释放锁
        lock.unLock();
    }
}

```

**SimpleRedisLock**

```java
public class SimpleRedisLock implements ILock{

    private String name;
    private StringRedisTemplate stringRedisTemplate;

    private static final String KEY_PREFIX = "lock:";

    public SimpleRedisLock(String name, StringRedisTemplate stringRedisTemplate) {
        this.name = name;
        this.stringRedisTemplate = stringRedisTemplate;
    }
    @Override
    public boolean tryLock(long timeoutSec) {
        //获取线程标识
        long threadId = Thread.currentThread().getId();
        // 获取锁
        Boolean success = stringRedisTemplate
                .opsForValue().setIfAbsent(KEY_PREFIX + name, threadId + "", timeoutSec, TimeUnit.SECONDS);
        return Boolean.TRUE.equals(success);
    }

    @Override
    public void unLock() {
        //释放锁
        stringRedisTemplate.delete(KEY_PREFIX + name);
    }
}

```

##### 基于 Redis 实现分布式锁，解决锁误删问题

**问题**：可能在极端情况下出现锁误删的情况。不同 JVM 中的线程 ID 可能会重复。

**修改代码**：在获取锁时存入线程标识（可用 uuid 表示），在释放锁时先获取锁中的线程标示，判断是否与当前线程表示一致，一致则释放锁，不一致则不释放锁。

```java
@Override
public boolean tryLock(long timeoutSec) {
    //获取线程标识
    String threadId = ID_PREFIX + Thread.currentThread().getId();
    // 获取锁
    Boolean success = stringRedisTemplate
            .opsForValue().setIfAbsent(KEY_PREFIX + name, threadId , timeoutSec, TimeUnit.SECONDS);
    return Boolean.TRUE.equals(success);
}

@Override
public void unLock() {
    //获取线程标识
    String threadId = ID_PREFIX + Thread.currentThread().getId();
    //获取锁中的标识
    String id = stringRedisTemplate.opsForValue().get(KEY_PREFIX + name);
    //判断标识是否一致
    if(threadId.equals(id)){
        //释放锁
        stringRedisTemplate.delete(KEY_PREFIX + name);
    }
}

```

##### Redis 的原子性问题（Lua 脚本）

Redis 提供了 Lua 脚本功能，在一个脚本中编写多条 Redis 命令，确保多条命令执行时的原子性。[[Javanotes|LuaScript]]

**Lua 脚本实现分布式锁的释放锁逻辑**

```lua
-- 这里的KEYS[1]就是锁的key，这里的ARGV就是当前线程标识
-- 获取锁中的标示，判断与当前线程标识一致
if (redis.call('GET', KEYS[1]) == ARGV[1]) then
  -- 一致，删除锁
  return redis.call('DEL', KEYS[1])
end
-- 不一致，则直接返回
return 0

```

**再次改进 Redis 的分布式锁**

```java
@Override
public void unLock() {
    //调用lua脚本
    stringRedisTemplate.execute(
            UNLOCK_SCRIPT,
            Collections.singletonList(KEY_PREFIX + name),
            ID_PREFIX + Thread.currentThread().getId());
}

private static final DefaultRedisScript<Long> UNLOCK_SCRIPT;
static {
    UNLOCK_SCRIPT = new DefaultRedisScript<>();
    UNLOCK_SCRIPT.setLocation(new ClassPathResource("unlock.lua"));
    UNLOCK_SCRIPT.setResultType(Long.class);
}

```

##### 基于 Redis 的分布式锁优化

基于 setnx 实现的分布式锁存在下面问题：

* **不可重入**：同一个线程无法多次获取同一把锁。
* **不可重试**：获取锁只尝试一次就返回 false，没有重试机制。
* **超时释放**：锁超时释放虽然可以避免死锁，但如果是业务执行耗时较长，也会导致锁释放，存在安全隐患。
* **主从一致性**：如果 redis 提供了主从集群，主从同步存在延迟。当主宕机时如果从同步主中锁数据，则会出现锁实现。

**Redisson**
Redisson 是一个在 Redis 的基础上实现的 Java 主内存数据网格，它不仅提供了一系列分布式的 Java 对象，还提供了许多分布式服务，其中就包含了各种分布式锁的实现，可重入锁，公平锁，联锁，红锁，读写锁。

##### Redisson 优化

引入依赖，配置 Redisson 客户端。

**使用 Redisson 的分布式锁**

```java
//创建锁对象
RLock lock = redissonClient.getLock("lock:order:" + userId);
//获取锁
boolean isLock = lock.tryLock();
//判断获取锁成功
if (!isLock) {
    //获取锁失败，返回错误或重试
    return Result.fail("不允许重复下单!");
}
try {
    //获取代理对象
    IVoucherOrderService proxy = (IVoucherOrderService) AopContext.currentProxy();
    //8.返回订单id
    return proxy.createVoucherOrder(voucherId);
} finally {
    //释放锁
    lock.unlock();
}

```

##### Redisson 可重入锁原理

Redisson 使用 Lua 脚本实现可重入锁，通过 Hash 结构记录线程标识和重入次数。

**获取锁的 Lua 脚本**

```lua
local key = KEYS[1]; -- 锁的key
local threadId = ARGV[1]; -- 线程唯一标识 
local releaseTime = ARGV[2]; -- 锁的自动释放时间 
-- 判断是否存在 
if(redis.call('exists', key) == 0) then
    -- 不存在, 获取锁
     redis.call('hset', key, threadId, '1'); 
    -- 设置有效期
     redis.call('expire', key, releaseTime);
     return 1; -- 返回结果
end; 
-- 锁已经存在，判断threadId是否是自己 
if(redis.call('hexists', key, threadId) == 1) then
    -- 不存在, 获取锁，重入次数+1
     redis.call('hincrby', key, threadId, '1'); 
    -- 设置有效期
    redis.call('expire', key, releaseTime);
    return 1; -- 返回结果 
end; 
return 0; -- 代码走到这里,说明获取锁的不是自己，获取锁失败

```

**释放锁的 Lua 脚本**

```lua
local key = KEYS[1]; -- 锁的key 
local threadId = ARGV[1]; -- 线程唯一标识 
local releaseTime = ARGV[2]; -- 锁的自动释放时间 

-- 判断当前锁是否还是被自己持有 
if (redis.call('HEXISTS', key, threadId) == 0) then
     return nil; -- 如果已经不是自己，则直接返回
end;
-- 是自己的锁，则重入次数-1 
local count = redis.call('HINCRBY', key, threadId, -1); 
-- 判断是否重入次数是否已经为0  
if (count > 0) then
     -- 大于0说明不能释放锁，重置有效期然后返回
     redis.call('EXPIRE', key, releaseTime);
     return nil;
else  -- 等于0说明可以释放锁，直接删除
     redis.call('DEL', key);
     return nil; 
end;

```

##### Redisson 的锁重试和 WatchDog 机制

* 利用信号量和 PubSub 功能实现等待，唤醒，获取锁失败的重试机制。
* 利用 **WatchDog** 延续锁时间，利用信号量控制锁重试等待。
* **看门狗机制**：加锁成功时，Redisson 会给这个锁设置一个默认 30 秒的过期时间（TTL）。同时启动一个后台定时任务（看门狗），每隔一段时间（比如 10 秒）检查锁是否还被当前线程持有。如果还持有，它就自动给这个锁“续命”，把过期时间重新刷新回 30 秒。

##### Redisson 的 multilock 机制

**联锁机制**：多个独立的 redis 节点，必须在所有节点都获取重入锁，才算获取锁成功。

#### Redis 优化秒杀

需求：

* 新增秒杀优惠券的同时，将优惠券信息保存到 Redis 中。
* 基于 Lua 脚本，判断秒杀库存，一人一单，决定用户是否抢购成功。

**VoucherServiceImpl**

```java
@Override
@Transactional
public void addSeckillVoucher(Voucher voucher) {
    // 保存优惠券
    save(voucher);
    // 保存秒杀信息
    SeckillVoucher seckillVoucher = new SeckillVoucher();
    seckillVoucher.setVoucherId(voucher.getId());
    seckillVoucher.setStock(voucher.getStock());
    seckillVoucher.setBeginTime(voucher.getBeginTime());
    seckillVoucher.setEndTime(voucher.getEndTime());
    seckillVoucherService.save(seckillVoucher);
    // 保存秒杀库存到Redis中
    stringRedisTemplate.opsForValue().set(SECKILL_STOCK_KEY + voucher.getId(), voucher.getStock().toString());
}

```

**Lua 脚本**

```lua
--1.参数列表
--1.1.优惠券id
local voucherId = ARGV[1]
--1.2.用户id
local userId = ARGV[2]

--2.定义数据key
--2.1.库存key
local stockKey = 'seckill:stock:' .. voucherId
--2.2.订单key
local orderKey = 'seckill:order:' .. voucherId

--3.脚本业务
--3.1.判断库存是否充足 get stockKey
if (tonumber(redis.call('get', stockKey)) <= 0 )then
    --3.2.库存不足，返回1
    return 1
end
--3.2.判断用户是否下单 sismember orderKey userId
if (redis.call('sismember', orderKey, userId) == 1) then
    --3.3.存在，用户已经下单，返回2
    return 2
end
--3.4.库存充足，用户未下单，下单成功，库存-1
redis.call('incrby', stockKey, -1)
--3.5.下单（保存用户） sadd orderKey userId
redis.call('sadd', orderKey, userId)
return 0

```

**VoucherOrderServiceImpl**

```java
@Override
public Result seckillVoucher(Long voucherId) {
    //获取用户id
    Long userId = UserHolder.getUser().getId();
    //1.执行lua脚本
    Long result = stringRedisTemplate.execute(
            SECKILL_SCRIPT,
            Collections.emptyList(),
            voucherId.toString(), userId.toString()
    );
    //2.判断结果是否为0
    int r = result.intValue();
    if(r != 0){
        //2.1.不为0，说明没有购买资格
        return Result.fail(r == 1 ? "库存不足" : "不能重复下单");
    }
    //2.2.为0，有购买资格，把下单信息保存到阻塞队列中
    //2.3.创建订单
    VoucherOrder voucherOrder = new VoucherOrder();
    //2.4.生成订单id
    long orderId = redisIdWorker.nextId("order");
    voucherOrder.setId(orderId);
    //2.5.获取当前用户
    voucherOrder.setUserId(userId);
    //2.6.获取代金券id
    voucherOrder.setVoucherId(voucherId);
    //2.6.保存阻塞队列
    orderTasks.add(voucherOrder);

    //3.获取代理对象（事务）
    proxy = (IVoucherOrderService) AopContext.currentProxy();

    //4.返回订单id
    return Result.ok(orderId);
}

```

**异步下单功能**

初始化阻塞队列，并不断从阻塞队列中获取信息。

```java
//创建阻塞队列
private BlockingQueue<VoucherOrder> orderTasks = new ArrayBlockingQueue<>(1024 * 1024);
private static final ExecutorService SECKILL_ORDER_EXECUTOR = Executors.newSingleThreadExecutor();

@PostConstruct
private void init(){
    SECKILL_ORDER_EXECUTOR.submit(new VoucherOrderHandler());
}

private class VoucherOrderHandler implements Runnable{
    @Override
    public void run(){
        while (true){
            try {
                //1.获取队列中的订单信息
                VoucherOrder voucherOrder = orderTasks.take();
                //2.创建订单
                handleVoucherOrder(voucherOrder);
            } catch (Exception e) {
               log.error("处理订单异常",e);
            }
        }
    }
}

```

```java
private void handleVoucherOrder(VoucherOrder voucherOrder) {
    //1.获取用户id 在线程池中使用userHolder获取不到用户id
    Long userId = voucherOrder.getUserId();
    //2.创建锁对象
    RLock lock = redissonClient.getLock("lock:order:" + userId);
    //获取锁
    boolean isLock = lock.tryLock();
    //是否获取锁成功
    if (!isLock) {
        //获取锁失败，返回错误或者重试
        log.error("不允许重复下单");
        return;
    }
    try {
        proxy.createVoucherOrder(voucherOrder);
    } finally {
        //释放锁
        lock.unlock();
    }
}

```

##### 基于阻塞队列的异步秒杀存在的问题

阻塞队列基于 JVM，所以可能存在内存溢出的情况，以及内存限制问题/数据安全问题。

#### Redis 消息队列实现异步秒杀

Redis 提供了三种不同的方式来实现消息队列：

1. **List 结构**：基于 List 结构模拟消息队列（LPUSH/BRPOP）。
2. **PubSub**：基本的点对点消息模型，无法持久化。
3. **Stream**：比较完善的消息队列模型（Redis 5.0 引入）。

##### 基于 Stream 的消息队列

* 发送消息 `XADD`
* 读取消息 `XREAD`
* **消费者组（Consumer Group）**
* **消息分流**：队列中的消息会分流给组内的不同消费者。
* **消息标识**：记录最后一个被处理的消息，确保不会被漏读。
* **消息确认**：通过 `XACK` 确认消息。


* 创建消费者组：`XGROUP CREATE key groupName ID [MKSTREAM]`

##### 基于 Redis 的 Stream 结构作为消息队列，实现异步秒杀下单

需求：

1. 创建一个 Stream 类型的消息队列，名为 `stream.orders`
```bash
XGROUP CREATE stream.orders g1 0 MKSTREAM

```


2. 修改之前的秒杀下单 Lua 脚本，在认定抢购资格之后，直接向 `stream.orders` 中添加消息。
3. 项目启动时，开启一个线程任务，尝试获取 `stream.orders` 中的消息，完成下单。

### 达人探店

#### 发布探店笔记

对应的表有两个：`tb_blog` (探店笔记表)，`tb_blog_comments` (评价表)。

##### 上传探店照片与信息

```java
@PostMapping("blog")
public Result uploadImage(@RequestParam("file") MultipartFile image) {
    try {
        // 获取原始文件名称
        String originalFilename = image.getOriginalFilename();
        // 生成新文件名
        String fileName = createNewFileName(originalFilename);
        // 保存文件
        image.transferTo(new File(SystemConstants.IMAGE_UPLOAD_DIR, fileName));
        // 返回结果
        log.debug("文件上传成功，{}", fileName);
        return Result.ok(fileName);
    } catch (IOException e) {
        throw new RuntimeException("文件上传失败", e);
    }
}

```

##### 保存探店用户

```java
@PostMapping
public Result saveBlog(@RequestBody Blog blog) {
    // 获取登录用户
    UserDTO user = UserHolder.getUser();
    blog.setUserId(user.getId());
    // 保存探店博文
    blogService.save(blog);
    // 返回id
    return Result.ok(blog.getId());
}

```

##### 实现查看发布探店笔记的接口

```java
@Override
public Result queryBlogById(Long id) {
    //1，查询blog
    Blog blog = getById(id);
    if (blog == null){
        return Result.fail("笔记不存在");
    }
    //2，查询blog有关的用户
    queryBlogUser(blog);
    return Result.ok(blog);
}

private void queryBlogUser(Blog blog) {
    Long userId = blog.getUserId();
    User user = userService.getById(userId);
    blog.setName(user.getNickName());
    blog.setIcon(user.getIcon());
}

```

#### 点赞

需求：同一个用户只能点赞一次，再次点击则取消点赞；如果当前用户已经点赞，则点赞高亮显示。

实现步骤：

1. 给 blog 类中添加一个 `isLike` 字段。
2. 修改点赞功能，利用 redis 的 set 判断是否点赞过。
3. 修改根据 id 查询 Blog 的业务，判断当前用户是否点赞过。

```java
@Override
public Result likeBlog(Long id) {
    //1.获取登录用户
    Long userId = UserHolder.getUser().getId();
    //2.判断当前登录用户是否已经点赞
    String key = BLOG_LIKED_KEY + id;
    Boolean isMember = stringRedisTemplate.opsForSet().isMember(key, userId.toString());
    if(BooleanUtil.isFalse(isMember)) {
        //3.如果未点赞，则点赞
        //3.1.数据库点赞数 + 1
        boolean isSuccess = update().setSql("liked = liked + 1").eq("id", id).update();
        //3.2.保存用户到redis的set集合
        if(isSuccess){
            stringRedisTemplate.opsForSet().add(key, userId.toString());
        }
    }else{
        //4.如果已点赞，则取消点赞
        //4.1.数据库点赞数-1
        boolean isSuccess = update().setSql("liked = liked - 1").eq("id", id).update();
        //4.2.把用户从redis的set集合移除
        stringRedisTemplate.opsForSet().remove(key, userId.toString());
    }
    return Result.ok();
}

```

#### 点赞排行榜

在探店笔记的详情页面，显示最早点赞的 TOP5 用户。
使用 **SortedSet** 进行存储（按 score 排序）。

**修改点赞逻辑**

```java
@Override
public Result likeBlog(Long id) {
    Long userId = UserHolder.getUser().getId();
    String key = BLOG_LIKED_KEY + id;
    Double score = stringRedisTemplate.opsForZSet().score(key, userId.toString());
    if(score == null) {
        //未点赞
        boolean isSuccess = update().setSql("liked = liked + 1").eq("id", id).update();
        if(isSuccess){
            // zadd key value score（时间戳）
            stringRedisTemplate.opsForZSet().add(key, userId.toString(),System.currentTimeMillis());
        }
    }else{
        //已点赞
        boolean isSuccess = update().setSql("liked = liked - 1").eq("id", id).update();
        stringRedisTemplate.opsForZSet().remove(key, userId.toString());
    }
    return Result.ok();
}

```

**查询博客的点赞排行榜信息**

```java
@Override
public Result queryBlogLikes(Long id) {
    String key = BLOG_LIKED_KEY + id;
    //1.查询top5的点赞用户 zrange key 0 4
    Set<String> top5 = stringRedisTemplate.opsForZSet().range(key, 0, 4);
    if(top5 == null || top5.isEmpty()){
        return Result.ok(Collections.emptyList());
    }
    //2.解析出其中的用户id
    List<Long> ids = top5.stream().map(Long::valueOf).collect(Collectors.toList());
    String idStr = StrUtil.join(",", ids);
    //3.根据用户id查询用户
    List<UserDTO> userDTOS = userService.query()
            .in("id", ids).last("ORDER BY FIELD(id," + idStr +")").list()
            .stream()
            .map(user -> BeanUtil.copyProperties(user, UserDTO.class))
            .collect(Collectors.toList());

    //4.返回
    return Result.ok(userDTOS);
}

```

### 好友关注

#### 关注和取关

```java
@Override
public Result follow(Long followUserId, Boolean isFollow) {
    //0.获取登录用户
    Long userId = UserHolder.getUser().getId();

    //1.判断是关注还是取关
    if(isFollow) {
        //2.关注，新增数据
        Follow follow = new Follow();
        follow.setUserId(userId);
        follow.setFollowUserId(followUserId);
        save(follow);
    }else{
        //3.取关，删除 delete from tb_follow where user_id = ? and follow_user_id = ?
        remove(new QueryWrapper<Follow>()
                .eq("user_id", userId).eq("follow_user_id", followUserId));
    }
    return Result.ok();
}

```

#### 共同关注

利用 Redis 中 **Set** 的交集功能。

```java
@Override
public Result followCommons(Long id) {
    //1.获取当前登录用户
    Long userId = UserHolder.getUser().getId();
    String key = "follows:" + userId;
    //2.求交集
    String key2 = "follows:" + id;
    Set<String> intersect = stringRedisTemplate.opsForSet().intersect(key, key2);
    if (intersect == null || intersect.isEmpty()) {
        //无交集
        return Result.ok(Collections.emptyList());
    }
    //3.解析id集合
    List<Long> ids = intersect.stream().map(Long::valueOf).collect(Collectors.toList());
    //4.查询用户
    List<UserDTO> users = userService.listByIds(ids)
            .stream()
            .map(user -> BeanUtil.copyProperties(user, UserDTO.class))
            .collect(Collectors.toList());
    return Result.ok(users);
}

```

#### 关注推送 (Feed 流)

采用 **TimeLine** 的模式，基于 **推模式** 实现。
修改新增探店笔记的业务，在保存 blog 到数据库的同时，推送到粉丝的收件箱（Redis ZSet，Score 为时间戳）。

```java
@Override
public Result saveBlog(Blog blog) {
    // 1.获取登录用户
    UserDTO user = UserHolder.getUser();
    blog.setUserId(user.getId());
    // 2.保存探店博文
    boolean isSuccess = save(blog);
    if (!isSuccess) {
        return Result.fail("新增笔记失败！");
    }
    // 3.查询笔记作者的所有粉丝
    List<Follow> follows = followService.query().eq("follow_user_id", user.getId()).list();
    // 4.推送笔记id给所有粉丝
    for (Follow follow : follows) {
        //4.1.获取粉丝id
        Long userId = follow.getUserId();
        //4.2.推送
        String key = FEED_KEY + userId;
        stringRedisTemplate.opsForZSet().add(key, blog.getId().toString(), System.currentTimeMillis());
    }
    // 5.返回id
    return Result.ok(blog.getId());
}

```

**滚动分页查询收件箱**

```java
@Override
public Result queryBlogOfFollow(Long max, Integer offset) {
    //1.获取当前用户
    Long userId = UserHolder.getUser().getId();
    //2.查询收件箱 ZREVRANGEBYSCORE key max min LIMIT offset count
    String key = FEED_KEY + userId;
    Set<ZSetOperations.TypedTuple<String>> typedTuples = stringRedisTemplate.opsForZSet()
            .reverseRangeByScoreWithScores(key, 0, max, offset, 2);
    //3.非空判断
    if (typedTuples == null || typedTuples.isEmpty()) {
        return Result.ok();
    }
    //4.解析数据：blogId，minTime（时间戳），offset
    List<Long> ids = new ArrayList<>(typedTuples.size());
    long minTime = 0;
    int os = 1;
    for(ZSetOperations.TypedTuple<String> tuple : typedTuples){
        //4.1.获取blog id
        String blogId = tuple.getValue();
        ids.add(Long.valueOf(blogId));
        //4.2.获取分数（时间戳）
        long time = tuple.getScore().longValue();
        if(time == minTime){
            os++;
        }else{
            minTime = time;
            os = 1;
        }
    }
    //5.根据id查询blog
    String idStr = StrUtil.join(",", ids);
    List<Blog> blogs = query().in("id", ids).last("ORDER BY FIELD(id," + idStr +")").list();

    for(Blog blog : blogs){
        queryBlogUser(blog);
        isBlogLiked(blog);
    }

    //6.封装并返回
    ScrollResult r = new ScrollResult();
    r.setList(blogs);
    r.setOffset(os);
    r.setMinTime(minTime);
    return Result.ok(r);
}

```

### 附近的商户

#### GEO 数据结构

* `GEOADD`：添加一个地理空间信息，包含：经度，纬度，值
* `GEODIST`：计算指定两个点之间的距离并返回
* `GEOHASH`：将指定 member 的坐标转为 hash 字符串形式并返回
* `GEOPOS`：返回指定 member 的坐标
* `GEOSEARCH`：在指定范围内搜索 member，并按照与指定点之间的距离排序后返回

#### 附近商户搜索

以 typeId 为 key 存入同一个 GEO 集合中。

```java
@Override
public Result queryShopByType(Integer typeId, Integer current, Double x, Double y) {
    // 1.判断是否需要根据坐标查询
    if (x == null || y == null) {
        // 不需要坐标查询，按数据库查询
        Page<Shop> page = query()
                .eq("type_id", typeId)
                .page(new Page<>(current, SystemConstants.DEFAULT_PAGE_SIZE));
        return Result.ok(page.getRecords());
    }

    // 2.计算分页参数
    int from = (current - 1) * SystemConstants.DEFAULT_PAGE_SIZE;
    int end = current * SystemConstants.DEFAULT_PAGE_SIZE;

    // 3.查询redis、按照距离排序、分页。结果：shopId、distance
    String key = SHOP_GEO_KEY + typeId;
    GeoResults<RedisGeoCommands.GeoLocation<String>> results = stringRedisTemplate.opsForGeo() 
            // GEOSEARCH key BYLONLAT x y BYRADIUS 10 WITHDISTANCE
            .search(
                    key,
                    GeoReference.fromCoordinate(x, y),
                    new Distance(5000),
                    RedisGeoCommands.GeoSearchCommandArgs.newGeoSearchArgs().includeDistance().limit(end)
            );
    // 4.解析出id
    if (results == null) {
        return Result.ok(Collections.emptyList());
    }
    List<GeoResult<RedisGeoCommands.GeoLocation<String>>> list = results.getContent();
    if (list.size() <= from) {
        // 没有下一页了，结束
        return Result.ok(Collections.emptyList());
    }
    // 4.1.截取 from ~ end的部分
    List<Long> ids = new ArrayList<>(list.size());
    Map<String, Distance> distanceMap = new HashMap<>(list.size());
    list.stream().skip(from).forEach(result -> {
        // 4.2.获取店铺id
        String shopIdStr = result.getContent().getName();
        ids.add(Long.valueOf(shopIdStr));
        // 4.3.获取距离
        Distance distance = result.getDistance();
        distanceMap.put(shopIdStr, distance);
    });
    // 5.根据id查询Shop
    String idStr = StrUtil.join(",", ids);
    List<Shop> shops = query().in("id", ids).last("ORDER BY FIELD(id," + idStr + ")").list();
    for (Shop shop : shops) {
        shop.setDistance(distanceMap.get(shop.getId().toString()).getValue());
    }
    // 6.返回
    return Result.ok(shops);
}

```

### 用户签到

Redis 的 **BitMap** 数据统计功能。
把每一个 bit 位对应当月的每一天，形成映射关系，用 0 和 1 标识业务状态。

#### 签到功能

```java
@Override
public Result sign() {
    //1.获取当前登录的用户
    Long userId = UserHolder.getUser().getId();
    //2.获取日期
    LocalDateTime now = LocalDateTime.now();
    //3.拼接key
    String keySuffix = now.format(DateTimeFormatter.ofPattern(":yyyyMM"));
    String key = USER_SIGN_KEY + userId + keySuffix;
    //4.获取今天是本月的第几天
    int dayOfMonth = now.getDayOfMonth();
    //5.写入Redis SET bitmap offset 1
    stringRedisTemplate.opsForValue().setBit(key, dayOfMonth - 1, true);
    return Result.ok();
}

```

#### 签到统计

统计当前用户截至当前时间在本月的连续签到天数。

```java
@Override
public Result signCount() {
    //1.获取当前登录用户
    Long userId = UserHolder.getUser().getId();
    //2.获取日期
    LocalDateTime now = LocalDateTime.now();
    //3.拼接key
    String keySuffix = now.format(DateTimeFormatter.ofPattern(":yyyyMM"));
    String key = USER_SIGN_KEY + userId + keySuffix;
    //4.获取今天是本月的第几天
    int dayOfMonth = now.getDayOfMonth();
    //5.获取本月截至今天位置所有的签到记录，返回的是一个十进制数字 BITFIELD key get u14 0
    List<Long> result = stringRedisTemplate.opsForValue().bitField(
            key,
            BitFieldSubCommands.create()
                    .get(BitFieldSubCommands.BitFieldType.unsigned(dayOfMonth)).valueAt(0)
    );
    if(result == null || result.isEmpty()){
        return Result.ok(0);
    }
    Long num = result.get(0);
    if(num == 0 || num == null) {
        return Result.ok(0);
    }
    //6.循环遍历，判断这个日期是否在连续签到中
    int count = 0;
    while(true){
        //6.1.让这个数字与1做与运算，得到数字的最后一个bit位
        //6.2.判断这个bit位是否为0
        if ((num & 1) == 0) {
            //6.3.如果是0，说明未签到，结束
            break;
        }else{
            //6.4.如果为1，说明已签到，继续，计数器 + 1
            count ++;
        }
        //把数字右移1位，抛弃最后一个bit位，继续判断下一个bit位
        num >>>= 1;
    }
    return Result.ok(count);
}

```

### UV 统计

Redis 的 **HyperLogLog** 的统计功能。

* **UV**：独立访客量。
* **HyperLogLog**：用于确定非常大的集合的基数，内存占用非常低（<16kb），有小于 0.81% 的误差。

#### 实现 UV 统计

```java
@Test
void testHyperLogLog() {
    String [] values = new String[1000];
    int j = 0;
    for(int i = 0; i < 1000000; i++){
        j = i % 1000;
        values[j] = "user_" + i;
        if(j == 999){
            //发送到redis
            stringRedisTemplate.opsForHyperLogLog().add("hl2", values);
        }
    }
    //统计数量
    Long count = stringRedisTemplate.opsForHyperLogLog().size("hl2");
    System.out.println("count = " + count);
}

```