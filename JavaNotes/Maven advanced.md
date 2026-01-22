## Maven Advanced

### 分模块开发

将原始模块按照功能拆分成若干个子模块，方便模块间的互相调用，接口共享

#### 创建Maven模块

#### 书写模块代码

Maven_02_ssm

1.      _<!--依赖domain运行-->_
2.      <dependency>
3.        <groupId>com.itheima</groupId>
4.        <artifactId>maven_03_pojo</artifactId>
5.        <version>1.0-SNAPSHOT</version>
6.      </dependency>

依赖domain运行

#### 通过maven指令安装模块到本地仓库（install）

使用install下载到仓库

团队内部开发需要发布模块功能到团队内部可共享的仓库中（私服）

### 依赖管理

- 依赖指当前项目运行所需的jar，一个项目可以设置多个依赖，依赖具有传递性

#### 传递依赖

- 直接依赖：在当前项目中通过依赖配置建立的依赖关系
- 间接依赖：被以来的资源如果依赖其他资源，当前项目间接依赖其他资源

#### 依赖传递冲突问题

- 路径优先：当依赖中出现相同的资源时，层级越深，优先级越低，层级越浅，优先级越高
- 声明优先：当资源在相同层级被依赖时，配置顺序靠前（配置文件的顺序）的覆盖配置顺序靠后的
- 特殊优先：当同级配置了相同资源的不同版本，后配置的覆盖先配置的

#### 可选依赖与排除依赖

可选依赖-隐藏自己的依赖 对外隐藏当前所依赖的资源——不透明

1.          <dependency>
2.              <groupId>com.itheima</groupId>
3.              <artifactId>maven_03_pojo</artifactId>
4.              <version>1.0-SNAPSHOT</version>
5.              <!--可选依赖是隐藏当前工程所依赖的资源，隐藏后对应资源将不具有依赖传递性;-->
6.              <optional>false</optional>
7.          </dependency>

- 排除依赖是隐藏当前资源对应的依赖关系-使用其他的资源时排除不用的依赖

主动断开以来的资源，被排除的资源无需指定版本——不需要

1.        <exclusions>
2.          <exclusion>
3.            <groupId>log4j</groupId>
4.            <artifactId>log4j</artifactId>
5.          </exclusion>
6.          <exclusion>
7.            <groupId>org.mybatis</groupId>
8.            <artifactId>mybatis</artifactId>
9.          </exclusion>
10.       </exclusions>
11.     </dependency>

排除依赖仅指定GA即可，无需指定V

### 聚合与继承

#### 聚合

- 聚合：将多个模块组织成一个整体，同时进行项目构建的过程称为聚合
- 聚合工程：通常是一个不具有业务功能的空工程（有且仅有一个pom文件）
- 作用：使用聚合工程可以将多个工程编组，通过对聚合工程进行构建，实现对时所包含的模块进行同步构建
- 当工程中某个模块发生更新（变更）时，必须保障工程中与已更新模块关联的模块同步更新，此时可以使用聚合工程来解决批量模块同步构建的问题

新建maven_01_parent 设置打包类型为pom

1.      <groupId>com.itheima</groupId>
2.      <artifactId>maven_01_parent</artifactId>
3.      <version>1.0-RELEASE</version>
4.      <packaging>pom</packaging>

设置当前聚合工程所包含的子模块名称

1.      _<!--设置管理的模块名称-->_
2.      <modules>
3.          <module>../maven_02_ssm</module>
4.          <module>../maven_03_pojo</module>
5.          <module>../maven_04_dao</module>
6.      </modules>

启动compile后会先构建没有依赖的，交换module的顺序对编译过程不产生影响

#### 继承

- 描述的是两个工程间的关系，与java中的继承相似，子工程可以继承父工程中的配置信息，常见于依赖关系的继承
- 作用：简化配置/减少版本冲突
- 聚合继承一般同一个文件

Maven_02_ssm 在子工程中配置当前继承的夫工程

1.    <parent>
2.      <groupId>com.itheima</groupId>
3.      <artifactId>maven_01_parent</artifactId>
4.      <version>1.0-RELEASE</version>
5.      <relativePath>../maven_01_parent/pom.xml</relativePath>
6.    </parent>

配置父工程GAV relativePath

父工程中可选依赖 配置子工程中可选的依赖关系

1.      _<!--定义依赖管理-->_
2.      <dependencyManagement>
3.          <dependencies>
4.              <dependency>
5.                  <groupId>junit</groupId>
6.                  <artifactId>junit</artifactId>
7.                  <version>4.12</version>
8.                  <scope>test</scope>
9.              </dependency>
10.         </dependencies>
11.     </dependencyManagement>

子工程中使用父工程中的可选依赖时，仅需要提供群组id和项目id，无需提供版本，版本由父工程统一提供，避免版本冲突，子工程中还可以定义父工程中没有定义的依赖关系

#### 继承与聚合的区别

- 作用：聚合用于快速构建项目，配置用于快速配置
- 相同点：
- 聚合与继承的pom.xml文件打包方式均为pom，可以将两种关系制作到同一个pom文件中
- 聚合与继承均属于设计型模块，并无实际的模块内容
- 不同点：
- 聚合是在当前模块中配置关系，聚合可以感知到参与聚合的模块有哪些
- 继承是在子模块中配置关系，父模块无法感知哪些子模块继承了自己

### 属性管理

#### 属性

1.      _<!--定义属性-->_
2.      <properties>
3.          <spring.version>5.2.10.RELEASE</spring.version>
4.          <junit.version>4.12</junit.version>
5.          <mybatis-spring.version>1.3.0</mybatis-spring.version>
6.          _<!--<jdbc.url>jdbc:mysql://127.0.0.1:3306/ssm_db</jdbc.url>-->_
7.      </properties>

8.      _<!--定义依赖管理-->_
9.     <dependencyManagement>
10.         <dependencies>
11.             <dependency>
12.                 <groupId>junit</groupId>
13.                 <artifactId>junit</artifactId>
14.                 <version>${junit.version}</version>
15.                 <scope>test</scope>
16.             </dependency>
17.         </dependencies>
18.     </dependencyManagement>

定义属性--引用属性

#### 配置文件加载属性

加载jdbc，定义属性

1.      _<!--定义属性-->_
2.      <properties>
3.          <jdbc.url>jdbc:mysql://127.0.0.1:3306/ssm_db</jdbc.url>
4.      </properties>

Jdbc.properties配置资源中引用属性

1.  jdbc.driver=com.mysql.jdbc.Driver
2.  jdbc.url=${jdbc.url}
3.  jdbc.username=root
4.  jdbc.password=root

设置资源目录

开启资源文件目录加载属性的过滤器

1.      <build>
2.          <resources>
3.              _<!--设置资源目录，并设置能够解析${}-->_
4.              <resource>
5.                  <directory>${project.basedir}/src/main/resources</directory>
6.                  <filtering>true</filtering>
7.              </resource>
8.          </resources>
9.      </build>

${project.basedir}内置属性名

配置maven打jar包，忽略web.xml检查

1.        <plugin>
2.          <groupId>org.apache.maven.plugins</groupId>
3.          <artifactId>maven-war-plugin</artifactId>
4.          <version>3.2.3</version>
5.          <configuration>
6.            <failOnMissingWebXml>false</failOnMissingWebXml>
7.          </configuration>
8.        </plugin>

#### 版本管理

- 工程版本：
- SNAPSHOT（快照版本）

项目开发过程中临时输出的版本，称为快照版本

快照版本会随着开发的进展不断更新

- RELEASE（发布版本）

项目开发到进入阶段里程碑后，向团队外部发布较为稳定的版本，这种版本所对应的构建是稳定的，即便进行功能的后续开发，也不会改变当前发布版本内容

- 发布版本
- Alpha版
- Beta版
- 纯数字版

### 多环境配置与应用

场景：生产环境需要一个数据库，开发环境需要一个数据库，测试环境需要一个数据库则需要配置多环境

#### 多环境开发

1.  _<!--配置多环境-->_
2.      <profiles>
3.          _<!--开发环境-->_
4.          <profile>
5.              <id>env_dep</id>
6.              <properties>
7.                  <jdbc.url>jdbc:mysql://127.1.1.1:3306/ssm_db</jdbc.url>
8.              </properties>
9.              _<!--设定是否为默认启动环境-->_
10.             <activation>
11.                 <activeByDefault>true</activeByDefault>
12.             </activation>
13.         </profile>
14.         _<!--生产环境-->_
15.         <profile>
16.             <id>env_pro</id>
17.             <properties>
18.                 <jdbc.url>jdbc:mysql://127.2.2.2:3306/ssm_db</jdbc.url>
19.             </properties>
20.         </profile>
21.         _<!--测试环境-->_
22.         <profile>
23.             <id>env_test</id>
24.             <properties>
25.                 <jdbc.url>jdbc:mysql://127.3.3.3:3306/ssm_db</jdbc.url>
26.             </properties>
27.         </profile>
28.     </profiles>

选中执行指令，mvn install -p env_test 相当于携带test指令

#### 跳过测试

应用场景：功能更新中并且还没有开发完毕/快速打包/...

或者指令实现

mvn package -D skipTests

弊端：全部跳过，一个测试都不执行

配置文件实现跳过指定的测试部分/细粒度管理

1.      <build>
2.          <plugins>
3.              <plugin>
4.                  <artifactId>maven-surefire-plugin</artifactId>
5.                  <version>2.12.4</version>
6.                  <configuration>
7.                      <skipTests>false</skipTests>
8.                      _<!--排除掉不参与测试的内容-->_
9.                      <excludes>
10.                         <exclude>\*\*/BookServiceTest.java</exclude>
11.                     </excludes>
12.                 </configuration>
13.             </plugin>
14.         </plugins>
15.     </build>

### 私服

#### 私服简介

- 私服是一台独立的服务器，用于解决团队内部的资源共享与资源同步问题
- Nexus

Sonatype公司的一款maven私服产品

启动服务器：nexus.exe /run nexus

访问服务器：http：//localhost：8081

#### 私服仓库分类

|     |     |     |     |
| --- | --- | --- | --- |
| 仓库分类 | 英文名称 | 功能  | 关联操作 |
| 宿主仓库 | Hosted | 保存自主研发+第三方资源 | 上传  |
| 代理仓库 | Proxy | 代理连接中央仓库 | 下载  |
| 仓库组 | Group | 为仓库编组简化下载操作 | 下载  |

#### 资源上传

上传的位置（宿主地址）

|

Idea——本地仓库——私服

|

本地仓库配置访问私服的用户名/密码

下载的地址

1.  在Nexus中配置demo-release与demo-snapshot两个仓库

2.  Settings.xml中配置访问私服的权限
3.      _<!-- 配置访问私服的权限 -->_
4.      <server>
5.        <id>demo-snapshot</id>
6.        <username>admin</username>
7.        <password>admin</password>
8.      </server>
9.      <server>
10.        <id>demo-release</id>
11.       <username>admin</username>
12.       <password>admin</password>
13.     </server>

14.  找到group中的maven仓库作为仓库组

15.  移动demo-release与demo-snapshot得到maven-public管理

16.  配置私服的访问路径
17.       <mirror>
18.       _<!-- 私服的访问路径 -->_
19.        <mirror>
20.        <id>maven-public</id>
21.        <mirrorOf>\*</mirrorOf>
22.        <url>http://localhost:8081/repository/maven-public/</url>
23.      </mirror>
24.    </mirrors>

这样本地仓库就与私服建立联系

1.  配置当前工程保存在私服中的具体位置
2.      _<!--配置当前工程保存在私服中的具体位置-->_
3.      <distributionManagement>
4.          <repository>
5.              <id>itheima-release</id>
6.              <url>http://localhost:8081/repository/itheima-release/</url>
7.          </repository>
8.          <snapshotRepository>
9.              <id>itheima-snapshot</id>
10.             <url>http://localhost:8081/repository/itheima-snapshot/</url>
11.         </snapshotRepository>
12.     </distributionManagement>

13.  发布命令

Mvn deploy
