# Web 服务器 - Tomcat

* Web 服务器是一个应用程序，对 HTTP 协议的操作进行封装，使得程序员不必直接对协议进行操作，让 Web 开发更加便捷。主要功能是“提供网上信息浏览服务”。
* **Tomcat**：轻量级的 Web 服务器，支持 Servlet/JSP 少量 JavaEE 规范。Tomcat也被称为 Web 服务器、Servlet 容器。Servlet 需要依赖 Tomcat 才能运行。
* **JavaEE**：Java 企业级开发的技术规范总和。

## 基本使用

1.  **启动**
    * 双击：`bin\startup.bat`
    * **控制台中文乱码解决**：修改 `conf/logging.properties`，将 `UTF-8` 改为 `GBK`。
2.  **关闭**
    * 强制关闭：直接点击窗口关闭按钮。
    * 脚本关闭：双击 `shutdown.bat`。
    * 快捷键关闭：黑窗口中按 `Ctrl+C`。
3.  **配置**
    * **修改启动端口号**：修改 `conf/server.xml`。
    * *注*：HTTP 协议默认端口号为 80。如果将 Tomcat 端口号改为 80，则访问 Tomcat 时将不用输入端口号。
4.  **启动时可能出现的问题**
    * **端口号冲突**：找到对应程序，将其关闭。
    * **启动窗口一闪而过**：[Tomcat双击startup.bat闪退](https://zhuanlan.zhihu.com/p/353404326) / `JAVA_HOME` 没有正确配置。
5.  **部署项目**
    * **直接部署**：将项目放置到 `webapps` 目录下，即部署完成。
    * **WAR 包部署**：一般将 JavaWeb 项目打包成 WAR 包，然后放到 `webapps` 目录下，Tomcat 会自动解压缩 WAR 文件。

## IDEA 中创建 Maven Web 项目

### 1. Web 项目结构
* 编译后的 Java 字节码文件和 `resources` 的资源文件，放到 `WEB-INF` 下的 `classes` 目录下。
* `pom.xml` 中依赖坐标对应的 jar 包，放入 `WEB-INF` 下的 `lib` 目录下。
* *注*：在 package 过程中可以自动完成这些过程。

### 2. 使用骨架 (Archetype)
* 创建项目时选择 Archetype。
* 自动补齐缺失的目录结构：`webapp`。

### 3. 不使用骨架
* 创建标准 Maven 项目。
* 在 `File` -> `Project Structure` -> `Facets` 中添加 Web 目录。

### 4. 在 Tomcat 中运行
* 通过 `<packaging>war</packaging>` 打包成 WAR 包，移动到 `webapps` 目录下，即可自动解压。
* **将本地 Tomcat 集成到 IDEA 中**，然后进行项目部署即可。

### 5. 使用 Maven Tomcat 插件
在 `pom.xml` 中添加 Tomcat 插件，然后右键文件选择 `Run Maven` -> `tomcat7:run`。

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.tomcat.maven</groupId>
            <artifactId>tomcat7-maven-plugin</artifactId>
            <version>2.2</version>
            <configuration>
                <port>80</port>
                <path>/</path>
            </configuration>
        </plugin>
    </plugins>
</build>
```