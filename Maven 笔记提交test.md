---
topic: Maven 笔记提交test
created: 2026-02-07 12:35
modified: 2026-02-07 14:26
tags: [Java, Spring, MySQL, Maven, 私服]
---

- Maven是专门用于管理和构建Java项目的工具
- 提供一套标准化的项目结构
- 提供一套标准化的构建流程（编译，测试，打包，发布）
- 提供一套依赖（第三方资源 插件 jar包）管理机制
- 测试 测试提交触发
- test for update

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

# Maven Advanced

## 分模块开发

将原始模块按照功能拆分成若干个子模块，方便模块间的互相调用，接口共享。

### 创建 Maven 模块

### 书写模块代码

**Maven_02_ssm**

依赖 domain 运行：

```XML
<dependency>
    <groupId>com.itheima</groupId>
    <artifactId>maven_03_pojo</artifactId>
    <version>1.0-SNAPSHOT</version>
</dependency>
```

### 通过 Maven 指令安装模块到本地仓库（install）

- 使用 `install` 下载到仓库。
    
- 团队内部开发需要发布模块功能到团队内部可共享的仓库中（私服）。
    

---

## 依赖管理

依赖指当前项目运行所需的 jar，一个项目可以设置多个依赖，依赖具有传递性。

### 传递依赖

- **直接依赖**：在当前项目中通过依赖配置建立的依赖关系。
    
- **间接依赖**：被依赖的资源如果依赖其他资源，当前项目间接依赖其他资源。
    

### 依赖传递冲突问题

- **路径优先**：当依赖中出现相同的资源时，层级越深，优先级越低；层级越浅，优先级越高。
    
- **声明优先**：当资源在相同层级被依赖时，配置顺序靠前（配置文件的顺序）的覆盖配置顺序靠后的。
    
- **特殊优先**：当同级配置了相同资源的不同版本，后配置的覆盖先配置的。
    

### 可选依赖与排除依赖

#### 可选依赖

隐藏自己的依赖，对外隐藏当前所依赖的资源——不透明。

```XML
<dependency>
    <groupId>com.itheima</groupId>
    <artifactId>maven_03_pojo</artifactId>
    <version>1.0-SNAPSHOT</version>
    <optional>false</optional>
</dependency>
```

#### 排除依赖

隐藏当前资源对应的依赖关系——使用其他的资源时排除不用的依赖。

主动断开依赖的资源，被排除的资源无需指定版本。


```XML
<exclusions>
    <exclusion>
        <groupId>log4j</groupId>
        <artifactId>log4j</artifactId>
    </exclusion>
    <exclusion>
        <groupId>org.mybatis</groupId>
        <artifactId>mybatis</artifactId>
    </exclusion>
</exclusions>
```

> **注意**：排除依赖仅指定 GA 即可，无需指定 V（版本）。

---

## 聚合与继承

### 聚合

- **聚合**：将多个模块组织成一个整体，同时进行项目构建的过程称为聚合。
    
- **聚合工程**：通常是一个不具有业务功能的空工程（有且仅有一个 pom 文件）。
    
- **作用**：使用聚合工程可以将多个工程编组，通过对聚合工程进行构建，实现对所包含的模块进行同步构建。
    
- **场景**：当工程中某个模块发生更新（变更）时，必须保障工程中与已更新模块关联的模块同步更新，此时可以使用聚合工程来解决批量模块同步构建的问题。
    

**新建 maven_01_parent 设置打包类型为 pom**

```XML
<groupId>com.itheima</groupId>
<artifactId>maven_01_parent</artifactId>
<version>1.0-RELEASE</version>
<packaging>pom</packaging>
```

**设置当前聚合工程所包含的子模块名称**

```XML
<modules>
    <module>../maven_02_ssm</module>
    <module>../maven_03_pojo</module>
    <module>../maven_04_dao</module>
</modules>
```

> 启动 compile 后会先构建没有依赖的，交换 module 的顺序对编译过程不产生影响。

### 继承

- **描述**：两个工程间的关系，与 Java 中的继承相似，子工程可以继承父工程中的配置信息，常见于依赖关系的继承。
    
- **作用**：简化配置 / 减少版本冲突。
    
- **注意**：聚合继承一般在同一个文件。
    

**Maven_02_ssm 在子工程中配置当前继承的父工程**

```XML
<parent>
    <groupId>com.itheima</groupId>
    <artifactId>maven_01_parent</artifactId>
    <version>1.0-RELEASE</version>
    <relativePath>../maven_01_parent/pom.xml</relativePath>
</parent>
```

配置父工程 GAV 及 `relativePath`。

**父工程中配置可选依赖（Dependency Management）**

父工程配置子工程中可选的依赖关系：

```XML
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.12</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

> 子工程中使用父工程中的可选依赖时，仅需要提供群组 ID 和项目 ID，无需提供版本，版本由父工程统一提供，避免版本冲突。子工程中还可以定义父工程中没有定义的依赖关系。

### 继承与聚合的区别

- **作用**：聚合用于快速构建项目，继承用于快速配置。
    
- **相同点**：
    
    - 聚合与继承的 `pom.xml` 文件打包方式均为 `pom`，可以将两种关系制作到同一个 `pom` 文件中。
        
    - 聚合与继承均属于设计型模块，并无实际的模块内容。
        
- **不同点**：
    
    - **聚合**是在当前模块中配置关系，聚合可以感知到参与聚合的模块有哪些。
        
    - **继承**是在子模块中配置关系，父模块无法感知哪些子模块继承了自己。
        

---

## 属性管理

### 属性定义与引用

```XML
<properties>
    <spring.version>5.2.10.RELEASE</spring.version>
    <junit.version>4.12</junit.version>
    <mybatis-spring.version>1.3.0</mybatis-spring.version>
    </properties>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### 配置文件加载属性

**1. 定义属性**

```XML
<properties>
    <jdbc.url>jdbc:mysql://127.0.0.1:3306/ssm_db</jdbc.url>
</properties>
```

**2. 在 jdbc.properties 配置资源中引用属性**

Properties

```xml
jdbc.driver=com.mysql.jdbc.Driver
jdbc.url=${jdbc.url}
jdbc.username=root
jdbc.password=root
```

**3. 开启资源文件目录加载属性的过滤器**


```XML
<build>
    <resources>
        <resource>
            <directory>${project.basedir}/src/main/resources</directory>
            <filtering>true</filtering>
        </resource>
    </resources>
</build>
```

> `${project.basedir}` 为内置属性名。

**配置 Maven 打 jar 包，忽略 web.xml 检查**

```XML
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-war-plugin</artifactId>
    <version>3.2.3</version>
    <configuration>
        <failOnMissingWebXml>false</failOnMissingWebXml>
    </configuration>
</plugin>
```

---

## 版本管理

### 工程版本

- **SNAPSHOT（快照版本）**
    
    - 项目开发过程中临时输出的版本，称为快照版本。
        
    - 快照版本会随着开发的进展不断更新。
        
- **RELEASE（发布版本）**
    
    - 项目开发到进入阶段里程碑后，向团队外部发布较为稳定的版本。
        
    - 这种版本所对应的构建是稳定的，即便进行功能的后续开发，也不会改变当前发布版本内容。
        

### 版本分类

- Alpha 版
    
- Beta 版
    
- 纯数字版
    

---

## 多环境配置与应用

**场景**：生产环境、开发环境、测试环境需要不同的数据库配置。

### 多环境开发配置

```XML
<profiles>
    <profile>
        <id>env_dep</id>
        <properties>
            <jdbc.url>jdbc:mysql://127.1.1.1:3306/ssm_db</jdbc.url>
        </properties>
        <activation>
            <activeByDefault>true</activeByDefault>
        </activation>
    </profile>
    <profile>
        <id>env_pro</id>
        <properties>
            <jdbc.url>jdbc:mysql://127.2.2.2:3306/ssm_db</jdbc.url>
        </properties>
    </profile>
    <profile>
        <id>env_test</id>
        <properties>
            <jdbc.url>jdbc:mysql://127.3.3.3:3306/ssm_db</jdbc.url>
        </properties>
    </profile>
</profiles>
```

使用指令：

mvn install -p env_test (相当于携带 test 环境指令)

### 跳过测试

**应用场景**：功能更新中并且还没有开发完毕 / 快速打包等。

方式一：指令实现

mvn package -D skipTests

> **弊端**：全部跳过，一个测试都不执行。

**方式二：配置文件实现（细粒度管理）**


```XML
<build>
    <plugins>
        <plugin>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>2.12.4</version>
            <configuration>
                <skipTests>false</skipTests>
                <excludes>
                    <exclude>**/BookServiceTest.java</exclude>
                </excludes>
            </configuration>
        </plugin>
    </plugins>
</build>
```

---

## 私服

### 私服简介

- **私服**：是一台独立的服务器，用于解决团队内部的资源共享与资源同步问题。
    
- **Nexus**：Sonatype 公司的一款 Maven 私服产品。
    
    - 启动服务器：`nexus.exe /run nexus`
        
    - 访问服务器：`http://localhost:8081`
        

### 私服仓库分类

|**仓库分类**|**英文名称**|**功能**|**关联操作**|
|---|---|---|---|
|**宿主仓库**|Hosted|保存自主研发 + 第三方资源|上传|
|**代理仓库**|Proxy|代理连接中央仓库|下载|
|**仓库组**|Group|为仓库编组简化下载操作|下载|

### 资源上传与下载

#### 上传流程

**Idea ——> 本地仓库 ——> 私服**

#### 配置步骤

1. 在 Nexus 中配置仓库

配置 demo-release 与 demo-snapshot 两个仓库。

**2. 在 settings.xml 中配置访问私服的权限**

```XML
<server>
    <id>demo-snapshot</id>
    <username>admin</username>
    <password>admin</password>
</server>
<server>
    <id>demo-release</id>
    <username>admin</username>
    <password>admin</password>
</server>
```

3. 配置仓库组

找到 group 中的 maven 仓库作为仓库组，移动 demo-release 与 demo-snapshot 到 maven-public 管理。

4. 配置私服的访问路径 (settings.xml)

这样本地仓库就与私服建立了联系。

```XML
<mirrors>
    <mirror>
        <id>maven-public</id>
        <mirrorOf>*</mirrorOf>
        <url>http://localhost:8081/repository/maven-public/</url>
    </mirror>
</mirrors>
```

**5. 配置当前工程保存在私服中的具体位置 (项目 pom.xml)**


```XML
<distributionManagement>
    <repository>
        <id>itheima-release</id>
        <url>http://localhost:8081/repository/itheima-release/</url>
    </repository>
    <snapshotRepository>
        <id>itheima-snapshot</id>
        <url>http://localhost:8081/repository/itheima-snapshot/</url>
    </snapshotRepository>
</distributionManagement>
```

6. 发布命令

```
mvn deploy
```