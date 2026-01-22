# 1. JSP 概述

- **定义**：JavaServer Pages，Java 服务端页面。
    
- **特点**：一种动态的网页技术，其中既可以定义 HTML、JS、CSS 等静态内容，还可以定义 Java 代码的动态内容。
    
- **公式**：JSP = HTML + Java。
    
- **作用**：简化开发，避免了在 Servlet 中直接输出 HTML 标签。
    

## JSP 原理

- JSP 本质上是一个 Servlet。
    
- JSP 容器（Tomcat）会将 `.jsp` 文件转换成 `.java` 文件，再由 JSP 容器（Tomcat）将其编译，最终对外提供服务的其实就是这个字节码文件。
    

---

# 2. JSP 脚本

- **作用**：JSP 脚本用于在 JSP 页面内定义 Java 代码。
    
- **分类**：
    
    1. `<%...%>`：内容会直接放到 `_jspService()` 方法之中。
        
    2. `<%=...%>`：内容会放到 `out.print()` 方法中，作为 `out.print()` 的参数。
        
    3. `<%!...%>`：内容会放到 `_jspService()` 之外，被类直接包含。
        

## 案例：脚本与截断

```Java
<table border="1" cellspacing="0" width="800">
    <tr>
        <th>序号</th>
        <th>品牌名称</th>
        <th>企业名称</th>
        <th>排序</th>
        <th>品牌介绍</th>
        <th>状态</th>
        <th>操作</th>
    </tr>
    <%
        for (int i = 0; i < brands.size(); i++) {
            Brand brand = brands.get(i);
    %>

    <tr align="center">
        <td><%=brand.getId()%></td>
        <td><%=brand.getBrandName()%></td>
        <td><%=brand.getCompanyName()%></td>
        <td><%=brand.getOrdered()%></td>
        <td><%=brand.getDescription()%></td>

        <%
            if(brand.getStatus() == 1){
                //显示启用
        %>
            <td><%="启用"%></td>
        <%
            }else {
                // 显示禁用
        %>
            <td><%="禁用"%></td>
        <%
            }
        %>

        <td><a href="#">修改</a> <a href="#">删除</a></td>
    </tr>
    <%
        }
    %>
</table>
```

## JSP 的缺点

由于 JSP 页面内，既可以定义 HTML 标签，又可以定义 Java 代码，造成以下问题：

1. **书写麻烦**：特别是复杂的页面。
    
2. **阅读麻烦**。
    
3. **复杂度高**：运行需要依赖于各种环境，JRE，JSP 容器，JavaEE。
    
4. **占内存和磁盘**：JSP 会自动生成 `.java` 和 `.class` 文件占磁盘，运行的是 `.class` 文件占内存。
    
5. **调试困难**：出错后，需要找到自动生成的 `.java` 文件进行调试。
    
6. **不利于团队协作**。
    

**演变过程**：

> Servlet $\rightarrow$ JSP $\rightarrow$ Servlet+JSP $\rightarrow$ Servlet+html+ajax

- **Servlet + JSP 模式**：
    
    - JSP 只负责数据的展示而不负责数据的处理，不直接在 JSP 中写代码。
        
    - Servlet 负责逻辑处理与数据封装处理，转发到 JSP 中。
        

---

# 3. JSP 快速入门

1. **导入 JSP 坐标**
    
    ```    XML
    <dependency>
        <groupId>javax.servlet.jsp</groupId>
        <artifactId>jsp-api</artifactId>
        <version>2.2</version>
        <scope>provided</scope>
    </dependency>
    ```
    
2. **创建 JSP 文件**
    
3. **编写 HTML 标签和 Java 代码**
    
    ```    Java
    <h1>hello jsp</h1>
    <%
        System.out.println("hello,jsp~");
        int i = 3;
    %>
    ```
    

---

# 4. EL 表达式

- **概念**：Expression Language 表达式语言，用于简化 JSP 页面内的 Java 代码。
    
- **主要功能**：获取数据。
    
- **语法**：`${expression}`
    
    - 例如 `${brands}`：获取域中存储的 key 为 brands 的数据。
        

## 使用演示

**后端 Servlet:**

```Java
@Override
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    // 1. 准备数据
    List<Brand> brands = new ArrayList<Brand>();
    brands.add(new Brand(1,"三只松鼠","三只松鼠",100,"三只松鼠，好吃不上火",1));
    brands.add(new Brand(2,"优衣库","优衣库",200,"优衣库，服适人生",0));
    brands.add(new Brand(3,"小米","小米科技有限公司",1000,"为发烧而生",1));

    // 2. 存储到 request 域中
    request.setAttribute("brands",brands);
    request.setAttribute("status",1);

    // 3. 转发到 el-demo.jsp
    request.getRequestDispatcher("/el-demo.jsp").forward(request,response);
}
```

**前端 `el-demo.jsp`:**

```Java
${brands}
```

## JavaWeb 中的四大域对象

EL 表达式获取数据，会依次从这 4 个域中寻找，直到找到为止：

1. **Page**：当前页面有效
    
2. **Request**：当前请求有效
    
3. **Session**：当前会话有效
    
4. **Application**：当前应用有效
    

---

# 5. JSTL 标签

- **概念**：Jsp Standard Tag Library，JSP 标准标签库。使用标签取代 JSP 页面上的 Java 代码。
    
- **常用标签**：`<c:if>`, `<c:foreach>`。
    

## 5.1 JSTL 快速入门

1. **导入坐标**
    
    ```    XML
    <dependency>
        <groupId>jstl</groupId>
        <artifactId>jstl</artifactId>
        <version>1.2</version>
    </dependency>
    <dependency>
         <groupId>taglibs</groupId>
         <artifactId>standard</artifactId>
         <version>1.1.2</version>
    </dependency>
    ```
    
2. **在 JSP 页面上引入 JSTL 标签库**
    
    
    ```    Java
    <%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
    ```
    
3. **使用**：一般与 EL 表达式结合使用。
    

## 5.2 常用标签使用

**`<c:if>` 标签**

```Java
<c:if test="${status == 1}">
    启用
</c:if>

<c:if test="${status == 0}">
    禁用
</c:if>
```

**`<c:forEach>` 标签**

- 相当于 for 循环。
    
- `items`：被遍历的容器。
    
- `var`：遍历产生的临时变量。
    
- `varStatus`：生成序号（status 有两个属性：`index` 从 0 开始，`count` 从 1 开始）。
    

**案例代码 (`jstl-foreach.jsp`):**

```Java
<input type="button" value="新增"><br>
<hr>
<table border="1" cellspacing="0" width="800">
    <tr>
        <th>序号</th>
        <th>品牌名称</th>
        <th>企业名称</th>
        <th>排序</th>
        <th>品牌介绍</th>
        <th>状态</th>
        <th>操作</th>
    </tr>

    <c:forEach items="${brands}" var="brand" varStatus="status">
        <tr align="center">
            <%--<td>${brand.id}</td>--%>
            <td>${status.count}</td>
            <td>${brand.brandName}</td>
            <td>${brand.companyName}</td>
            <td>${brand.ordered}</td>
            <td>${brand.description}</td>
            <c:if test="${brand.status == 1}">
                <td>启用</td>
            </c:if>
            <c:if test="${brand.status != 1}">
                <td>禁用</td>
            </c:if>

            <td><a href="#">修改</a> <a href="#">删除</a></td>
        </tr>
    </c:forEach>
</table>
```

**普通 for 循环:**

```Java
<c:forEach begin="1" end="10" step="1" var="i">
    <a href="#">${i}</a>
</c:forEach>
```

_应用场景：分页进度条_

---

# 6. MVC 模式和三层架构

## MVC 模式

MVC 是一种分层开发的模式，其中：

- **M (Model)**：业务模型，处理业务 —— JavaBean
    
- **V (View)**：视图，界面展示 —— JSP
    
- **C (Controller)**：控制器，处理请求，调用模型和视图 —— Servlet
    

**MVC 好处**：

- 职责单一，互不影响
    
- 有利于分工协作
    
- 有利于组件重组
    

## 三层架构与三大框架 (SSM)

1. **表现层** (`com.org.web/controller`)
    
    - **框架**：SpringMVC / Struts2
        
    - **职责**：接收请求，封装数据，调用业务逻辑层，响应数据。
        
2. **业务逻辑层** (`com.org.service`)
    
    - **框架**：Spring
        
    - **职责**：对业务逻辑进行封装，组合数据访问层中基本功能，形成复杂的业务逻辑功能。
        
3. **数据访问层** (`com.org.dao/mapper`)
    
    - **框架**：MyBatis / Hibernate
        
    - **职责**：JDBC，MyBatis，对数据库的 CRUD 操作。
        

---

# 7. 案例：品牌增删改查

**技术栈**：Servlet / JSP / 三层架构

## 7.1 准备环境

- 创建新的模块 `brand_demo`，引入坐标：
    
    ```    XML
    <dependencies>
        </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.tomcat.maven</groupId>
                <artifactId>tomcat7-maven-plugin</artifactId>
                <version>2.2</version>
            </plugin>
        </plugins>
    </build>
    ```
    
- 创建三层架构的包结构。
    
- 数据库表 `tb_brand`，实体类 `Brand`。
    
- MyBatis 基础环境 (`Mybatis-config.xml`, `BrandMapper.xml`, `BrandMapper` 接口)。
    

## 7.2 查询所有

**1. Dao 层 (`BrandMapper.java`):**

```Java
/**
 * 查询所有
 * @return
 */
@ResultMap("brandResultMap")
@Select("select * from tb_brand")
List<Brand> selectAll();
```

- 注解 `@Select`
    
- 注解 `@ResultMap` 确定映射关系，解决驼峰命名与原变量的命名映射。
    

**Mapper XML (`BrandMapper.xml`):**

```XML
<resultMap id="brandResultMap" type="brand">
    <result column="brand_name" property="brandName"></result>
    <result column="company_name" property="companyName"></result>
</resultMap>
```

**2. Service 层 (`BrandService.java`):**

```Java
public class BrandService {
    SqlSessionFactory factory = SqlSessionFactoryUtils.getSqlSessionFactory();

    /**
     * 查询所有
     * @return
     */
    public List<Brand> selectAll() {
        // 1. 获取 SqlSession 对象
        SqlSession sqlSession = factory.openSession();
        // 2. 获取 brandMapper
        BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

        // 3. 调用方法
        List<Brand> brands = mapper.selectAll();

        sqlSession.close();
        return brands;
    }
}
```

**Utils 类 (`SqlSessionFactoryUtils.java`):**


```Java
public class SqlSessionFactoryUtils {
    private static SqlSessionFactory sqlSessionFactory;
    static {
        // 静态代码块会随着类的加载而自动执行，且只执行一次
        try {
            String resource = "mybatis-config.xml";
            InputStream inputStream = Resources.getResourceAsStream(resource);
            sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public static SqlSessionFactory getSqlSessionFactory(){
        return sqlSessionFactory;
    }
}
```

**3. Web 层 (`SelectAllServlet.java`):**


```Java
@WebServlet("/selectAllServlet")
public class SelectAllServlet extends HttpServlet {
    private BrandService service = new BrandService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // 1. 调用 BrandService 完成查询
        List<Brand> brands = service.selectAll();

        // 2. 将 brands 存入 request 域中
        request.setAttribute("brands", brands);

        // 3. 转发到 brand.jsp 页面
        request.getRequestDispatcher("/brand.jsp").forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
```

**4. 前端展示 (`brand.jsp`):**


```Java
<table border="1" cellspacing="0" width="800">
    <tr>
        <th>序号</th>
        <th>品牌名称</th>
        <th>企业名称</th>
        <th>排序</th>
        <th>品牌介绍</th>
        <th>状态</th>
        <th>操作</th>
    </tr>
    <c:forEach items="${brands}" var="brand" varStatus="status">
        <tr align="center">
            <td>${status.count}</td>
            <td>${brand.brandName}</td>
            <td>${brand.companyName}</td>
            <td>${brand.ordered}</td>
            <td>${brand.description}</td>
            <c:if test="${brand.status == 1}">
                <td>启用</td>
            </c:if>
            <c:if test="${brand.status != 1}">
                <td>禁用</td>
            </c:if>
            <td><a href="#">修改</a> <a href="#">删除</a></td>
        </tr>
    </c:forEach>
</table>
```

---

## 7.3 添加品牌

**1. Dao 层 (`BrandMapper.java`):**


```Java
@Insert("insert into tb_brand values (null,#{brandName},#{companyName},#{ordered},#{description},#{status})")
@ResultMap("brandResultMap")
void add(Brand brand);
```

**2. Service 层 (`BrandService.java`):**


```Java
public void add(Brand brand) {
    SqlSession sqlSession = factory.openSession();
    BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);
    
    mapper.add(brand);
    
    // 提交事务
    sqlSession.commit();
    sqlSession.close();
}
```

_注意：增删改行为需要提交事务_

**3. Web 层**

- **修改 `brand.jsp`**: 增加新增按钮并绑定事件。
    
    ```    HTML
    <input type="button" value="新增" id="add">
    <script>
        document.getElementById("add").onclick = function () {
            location.href = "/brand-demo/addBrand.jsp"
        }
    </script>
    ```
    
- **`AddServlet.java`**:
    
    ```    Java
    @WebServlet("/addServlet")
    public class AddServlet extends HttpServlet {
        private BrandService service = new BrandService();
    
        @Override
        protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
            // 1. 接收数据
            request.setCharacterEncoding("utf-8"); // 处理 post 请求乱码问题
            String brandName = request.getParameter("brandName");
            String companyName = request.getParameter("companyName");
            String description = request.getParameter("description");
            String ordered = request.getParameter("ordered");
            String status = request.getParameter("status");
    
            // 2. 封装数据
            Brand brand = new Brand();
            brand.setBrandName(brandName);
            brand.setCompanyName(companyName);
            brand.setDescription(description);
            brand.setOrdered(Integer.parseInt(ordered));
            brand.setStatus(Integer.parseInt(status));
    
            // 3. 调用 service 完成添加
            service.add(brand);
    
            // 转发到查询所有 Servlet
            request.getRequestDispatcher("/selectAllServlet").forward(request, response);
        }
    
        @Override
        protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
            this.doGet(request, response);
        }
    }
    ```
    
- **新增页面 `addBrand.jsp` (静态页面表单)**:
    
    ```    HTML
    <form action="/brand-demo/addServlet" method="post">
        品牌名称：<input name="brandName"><br>
        企业名称：<input name="companyName"><br>
        排序：<input name="ordered"><br>
        描述信息：<textarea rows="5" cols="20" name="description"></textarea><br>
        状态：
        <input type="radio" name="status" value="0">禁用
        <input type="radio" name="status" value="1">启用<br>
        <input type="submit" value="提交">
    </form>
    ```
    

---

## 7.4 修改 - 回显数据

**1. Dao 层 (`BrandMapper.java`):**


```    Java
@Select("select * from tb_brand where id=#{id}")
@ResultMap("brandResultMap")
Brand selectById(int id);
```

**2. Service 层 (`BrandService.java`):**

```Java
public Brand selectById(int id) {
    SqlSession sqlSession = factory.openSession();
    BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);
    
    Brand brand = mapper.selectById(id);
    
    sqlSession.close();
    return brand;
}
```

**3. Web 层 (`SelectByIdServlet.java`):**

```Java
@WebServlet("/selectByIdServlet")
public class SelectByIdServlet extends HttpServlet {
    private BrandService service = new BrandService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // 接受 id
        String id = request.getParameter("id");
        // 调用 service 查询
        Brand brand = service.selectById(Integer.parseInt(id));
        // 存储到 request 中
        request.setAttribute("brand", brand);
        // 转发到 update.jsp
        request.getRequestDispatcher("/update.jsp").forward(request, response);
    }
    // doPost 省略...
}
```

**4. 页面修改**:

- **`brand.jsp` 修改按钮**: `<td><a href="/brand-demo/selectByIdServlet?id=${brand.id}">修改</a>`
    
- **新建 `update.jsp` (回显数据)**:
    
    ```    Java
    <form action="/brand-demo/updateServlet" method="post">
        品牌名称：<input name="brandName" value="${brand.brandName}"><br>
        企业名称：<input name="companyName" value="${brand.companyName}"><br>
        排序：<input name="ordered" value="${brand.ordered}"><br>
        描述信息：<textarea rows="5" cols="20" name ="description">${brand.description}</textarea><br>
        状态：
        <c:if test="${brand.status == 1}">
            <input type="radio" name="status" value="1" checked>启用
            <input type="radio" name="status" value="0">禁用<br>
        </c:if>
        <c:if test="${brand.status == 0}">
            <input type="radio" name="status" value="0" checked>禁用
            <input type="radio" name="status" value="1">启用<br>
        </c:if>
        <input type="submit" value="提交">
    </form>
    ```
    

---

## 7.5 修改 - 修改数据

**1. Dao 层 (`BrandMapper.java`):**

```Java
@Update("update tb_brand set brand_name=#{brandName},company_name=#{companyName},ordered=#{ordered},description=#{description},status=#{status} where id=#{id}")
void update(Brand brand);
```

_注意：这里不需要使用 `@ResultMap`。`@Update` 操作没有返回值，MyBatis 不需要进行结果集映射。_

**2. Service 层 (`BrandService.java`):**

```java
public void update(Brand brand) {
    SqlSession sqlSession = factory.openSession();
    BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);
    
    mapper.update(brand);
    
    // 提交事务
    sqlSession.commit();
    sqlSession.close();
}
```

**3. Web 层 (`UpdateServlet.java`):**

```Java
@WebServlet("/updateServlet")
public class UpdateServlet extends HttpServlet {
    private BrandService service = new BrandService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // 1. 接收数据
        request.setCharacterEncoding("utf-8");
        String id = request.getParameter("id");
        String brandName = request.getParameter("brandName");
        // ... (其他参数接收同 AddServlet)
        
        // 2. 封装数据
        Brand brand = new Brand();
        brand.setId(Integer.parseInt(id));
        brand.setBrandName(brandName);
        // ... (其他参数设置)

        // 3. 调用 service 完成修改
        service.update(brand);

        // 转发到查询所有 Servlet
        request.getRequestDispatcher("/selectAllServlet").forward(request, response);
    }
    // doPost 省略...
}
```

4. 页面修改 (update.jsp):

需要在表单中添加隐藏域，用于提交 id：


```Java
<form action="/brand-demo/updateServlet" method="post">
    <%--隐藏域，提交 id--%>
    <input type="hidden" name="id" value="${brand.id}">
    
    品牌名称：<input name="brandName" value="${brand.brandName}"><br>
    ...
</form>
```

---

## 7.6 删除数据

- 见 `brand-demo`