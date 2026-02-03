Spring Cache 是一个框架 实现了基于注解的缓存功能 只需要简单的加一个注解 就能实现缓存功能
Spring Cache提供了一层抽象 底层可以切换不同的缓存实现 例如：
- EHCache
- Caffeine
- Redis
```xml
<dependency>  
    <groupId>org.springframework.boot</groupId>  
    <artifactId>spring-boot-starter-cache</artifactId>  
</dependency>
```
底层指定不需要冗余操作 只需要导入redis java客户端的maven坐标
# 常用注解

| 注解             | 说明                                                         |
| -------------- | ---------------------------------------------------------- |
| @EnableCaching | 开启缓存注解功能 通常还在启动类上                                          |
| @Cacheable     | 在方法执行前查询缓存中是否有数据 如果有数据 则直接返回缓存数据 如果没有缓存数据 调用方法并将方法返回值放到缓存中 |
| @CachePut      | 将方法的返回值放到缓存中                                               |
| @CacheEvict    | 将一条或多条数据从缓存中删除                                             |
