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
## 结合操作命令
## 有序集合操作命令
## 通用命令