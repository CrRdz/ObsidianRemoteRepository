- Maven是专门用于管理和构建Java项目的工具
- 提供一套标准化的项目结构
- 提供一套标准化的构建流程（编译，测试，打包，发布）
- 提供一套依赖（第三方资源 插件 jar包）管理机制

# Maven简介

项目管理和构建工具，基于项目对象模型的概念，通过一小段描述信息来管理项目的构建，报告和文档

## 仓库（repository）分类

本地仓库：自己计算机上的一个目录

中央仓库：有Maven团队维护的全球唯一的仓库

远程仓库（私服）：一般由公司团队搭建的私有仓库

当项目中使用坐标引入对应依赖jar包，首先会查找本地仓库中是否有对应的jar包：

如果有，则在项目中直接引用

如果没有，则去中央仓库中下载对应的jar包到本地仓库

# Maven基本使用

## Maven常用命令

mvn compile 编译

mvn clean 清理

mvn test 测试

mvn package 打包

mvn install 安装

## Maven生命周期

Maven构建项目生命周期描述的是一次构建过程经历了多少个事件

Maven对项目构建的生命周期划分为3套

同一生命周期内，执行后边的命令，前边的所有命令会自动执行

- Clean：清理工作

Preclean-clean-postclean

- default：核心工作，编译测试打包安装

compile-test-package-install

- Site：产生报告，发布站点

presite-site-postsite

## Maven坐标

Maven中的坐标是资源的唯一标识

使用坐标来定义项目或引入项目中需要的依赖

Maven坐标主要组成

1.  groupid：定义当前Maven项目隶属组织名称（通常域名反写）
2.  Artifactid：定义当前Maven项目名称（通常是模块名称，例如order-service）
3.  Version：定义当前版本号

## 使用坐标导入jar包

1.  在pom.xml中编写&lt;dependencies&gt;标签
2.  在&lt;dependencies&gt;标签中，使用&lt;dependencies&gt;引入坐标
3.  定义坐标的groupId,artifactId,version //_Alt+Insert_ 如果本地仓库有 模板生成
4.  点击刷新按钮，使坐标生效

## 依赖管理

通过设置坐标的依赖范围（scope），可以设置对应jar包的作用范围：编译环境，测试环境，运行环境

依赖范围取值：  
compile；
test；
provided；
runtime；
system；
import

Idea实用插件：Maven Helper