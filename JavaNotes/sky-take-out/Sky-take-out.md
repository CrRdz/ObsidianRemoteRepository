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