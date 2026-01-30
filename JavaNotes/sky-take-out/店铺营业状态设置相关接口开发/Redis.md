Redis是基于内存的key-value结构数据库
- 基于内存存储 读写性能高
- 适合存储热点数据（热点商品 资讯 新闻）
---
# Redis 5种常用数据类型
## string

普通字符串 Redis中最简单的数据类型
## Hash

也叫散列，类似于Java中的HashMap结构

| field1 | value1 |
| ------ | ------ |
| field2 | value2 |

## list

按照插入顺序排序 可以有重复元素 类似于Java中的LinkedList

| a   | b   | c   | d   |
| --- | --- | --- | --- |
## set

无序集合 没有重复与阿叔 类似于Java中的HashSet
## sorted set /zset

有序集合 集合中的每个元素关联一个分数（score） 根据分数的升序排序 没有重复元素（排行榜）
# Reids常用命令
## 字符串操作命令
`SET key value` 设置指定key的值
`GET key` 获取指定key的值
`SETEX key seconds value` 设置指定key的值 并将key的过期时间设为seconds 秒
`SETNX key value` 只有在key不存在时设置key的值（分布式锁）
## Hash操作命令
key - field1 ｜ value1
`HSET key field value` 将哈希表key中的字段field的值设为value
`HGET key field` 获取存储在哈希表中指定字段的值
`HDEL key field` 删除存储在哈希表中的指定字段
`HKEYS key` 获取哈希表中所有字段
`HVALS key` 获取哈希表中所有值
## 列表操作命令
`LPUSH key value1 [value2]` 将一个值或多个值插入到列表头部
`LRANGE key start stop` 获取列表指定范围内的元素
`RPOP key` 移除并获取列表最后一个元素
`LLEN key` 获取列表长度
## 集合操作命令
Redis set是string类型的无序集合 集合成员是唯一的 集合中不能出现重复的数据 常用命令
`SADD key member1  [member2] ` 向集合添加一个或多个成员
`SMEMBERS key` 返回集合中的所有成员
`SCARD key` 获取集合的陈元素
`SINTER key1 [key2]` 返回给定所有集合的交集
`SUNION key1 [key2]` 返回所有给定集合的并集
`SREM key member1 [member2]` 删除集合中一个或多个成员
## 有序集合操作命令
Redis有序集合是string类型元素的集合 且不允许有重复成员 每个元素都会关联一个double类型的分数 
`ZADD key score1 member1 [score2 member2]` 向有序集合添加一个或多个成员
`ZRANGE key start stop [WITHSCORES]` 通过索引区间返回有序集合中指定区间内的成员
`ZINCRBY key increment member` 有序集合中对指定成员的分数加上增量increment
`ZREM key member [member ...]` 移除有序集合中的一个或多个成员
## 通用命令
Redis的通用命令是不分数据类型的 都可以使用的命令
`KEYS pattern` 查找所有符合给定模式（pattern）的key
`EXISTS key` 检查给定key是否存在
`TYPE key` 返回key所储存的值的类型
`DEL key` 该命令用于在key存在时删除key
# 在java中操作redis
## Spring Data Redis使用方法
- 导入Spring Data Redis的maven坐标
```xml
<dependency>  
    <groupId>org.springframework.boot</groupId>  
    <artifactId>spring-boot-starter-data-redis</artifactId>  
</dependency>
```
- 配置Redis数据源
- 编写配置类 创建RedisTemplate对象
- 通过RedisTemplate对象操作Redis