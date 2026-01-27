>仓库地址：[[git@github.com:CrRdz/sky-take-out.git]]

# 开发环境搭建
## 后端项目结构
**sky-common** 子模块存放一些公共类 可以供其他模块使用
**sky-pojo** 子模块存放的是一些entity DTO VO
- entity 实体 通常和数据库中的表对应
- DTO 数据传输对象 通常用于程序中各层之间传递数据
- VO 视图对象 为前端展示数据提供的对象
- POJO 普通Java对象 只有属性和对应的getter和setter
**Sky-server** 子模块中存放的是配置文件 配置类 拦截器 controller service mapper 启动类等
## 数据库环境搭建
详细表结构：[[数据库设计文档]]
## 前后端首次联调
后端的初始工程中已经实现了登陆功能 直接进行前后端联调测试即可
通过断点调试跟踪后端程序的执行过程 

Q:前端发送的请求 是如何请求到后端的
 前端请求地址：http://localhost/api/employee/login
 后端接口地址：http://localhost:8080/admin/employee/login
A： nginx 反向代理 将前端发送的动态请求由nginx转发到后端服务器
nginx反向代理的好处
- 提高访问速度
- 负载均衡：把大量的请求按照指定的方式均衡的分配给集群中的每台服务器
- 保证后端服务安全

nginx反向代理的配置方式
```xml
server {

	listen 8081;
	server_name localhost;

	# 反向代理,处理管理端发送的请求
	location /api/ {
		proxy_pass http://localhost:8080/admin/;
	}

}
```
# 完善登陆功能
问题：员工表中的密码是明文存储 安全性太低
解决思路：将密码加密后存储 提高安全性 使用MD5加密方式对明文密码加密
步骤：
1. 修改数据库中明文密码 改为MD5加密后的密文
2. 修改Java代码 前段提交的密码进行MD5加密后再跟
 ```java
//密码比对  
//对前段传来的明文密码进行md6加密处理  
password =  DigestUtils.md5DigestAsHex(password.getBytes());
 ```

