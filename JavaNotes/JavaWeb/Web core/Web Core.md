* **JavaWeb 技术栈**
* **B/S 架构**：Browser/Server（浏览器/服务器）架构模式。
    * **特点**：客户端只需要浏览器，应用程序的逻辑和数据都存储在服务器端。浏览器只需要请求服务器，获取 Web 资源，服务器把 Web 资源发送给浏览器即可。
    * **好处**：易于维护升级。服务端升级后，客户端无需任何部署就可以使用到新的版本。

**核心组件：**
* **静态资源**：HTML，CSS，JavaScript，图片等。负责页面展现。
* **动态资源**：[[Servlet]]，[[JSP]] 等。负责逻辑处理。
* **数据库**：负责存储管理。
* **HTTP 协议**：定义通信规则。
* **Web 服务器（[[Tomcat]]）**：负责解析 [[HTTP]] 协议，解析请求数据，并发送响应数据。
---
Web Core/

├─ [[HTTP]]

├─ [[Tomcat|Web 服务器-Tomcat]]

├─ [[Servlet]]

├─ [[Request and Response]]

├─ [[JSP]]

├─ Frontend/

│ ├─ [[CSS]]

│ ├─ [[HTML]]

│ ├─ [[JavaScript]]

├─ [[会话跟踪技术]]

├─ [[Filter & Listener]]

├─ [[AJAX]]

├─ [[VUE]]

└─  [[ElementUI]]

---
# 综合案例

完成品牌数据的增删改查，批量删除，分页查询，条件查询。

技术栈：前端 Vue + Element UI + 后端 MyBatis + Servlet

---

# 1. 查询所有

## 1.1 后端代码

Mapper - BrandMapper.java

由于 Brand 实体类中的名称与数据库表中字段不匹配，需要使用 ResultMap 进行映射。

```Java
@Select("select * from tb_brand")
@ResultMap("brandResultMap")
List<Brand> selectAll();
```

**Resources - BrandMapper.xml**

```XML
<mapper namespace="com.itheima.mapper.BrandMapper">
    <resultMap id="brandResultMap" type="brand">
        <result property="brandName" column="brand_name" />
        <result property="companyName" column="company_name" />
    </resultMap>
</mapper>
```

Service - BrandService.java

创建一个接口，在接口中写方法。

```Java
List<Brand> selectAll();
```

**Service Impl - BrandServiceImpl.java**

```Java
public class BrandServiceImpl implements BrandService {
    // 1.创建sqlSessionFactory
    SqlSessionFactory sqlSessionFactory = SqlSessionFactoryUtils.getSqlSessionFactory();

    @Override
    public List<Brand> selectAll() {
        // 2.获取SqlSession对象
        SqlSession sqlSession = sqlSessionFactory.openSession();

        // 3.获取BrandMapper
        BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

        List<Brand> brands = mapper.selectAll();

        // 5.释放资源
        sqlSession.close();
        return brands;
    }
}
```

_注：通过接口-实现类，通过一些框架设计 web 层和 service 层可以解耦合。_

**Web - SelectAllServlet.java**

```Java
@WebServlet("/selectAllServlet")
public class SelectAllServlet extends HttpServlet {

    private BrandService brandService = new BrandServiceImpl();

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // 1. 调用service查询
        List<Brand> brands = brandService.selectAll();

        // 2.转为json
        String jsonString = JSON.toJSONString(brands);

        // 3.写数据
        response.setContentType("text/json;charset=utf-8");
        response.getWriter().write(jsonString);
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
```

> **测试**：启动 Tomcat 程序，访问 `selectAllServlet`，看到一系列的 JSON 数据则后台接收数据无误。

## 1.2 前端代码

brand.html (Vue Logic)

当页面加载完成时候，发送异步请求来获取数据。通过 then 回调，获取响应，绑定 function 函数，resp.data 就是列表数据，传到表格数据的模型上。

```JavaScript
new Vue({
    el: "#app",
    mounted() {
        // 当页面加载完成后，发送异步请求
        var _this = this;

        axios({
            method: "get",
            url: "http://localhost:8080/brand-case/selectAllServlet"
        }).then(function(resp) {
            _this.tableData = resp.data;
        })
    }
})
```

---

# 2. 新增品牌

## 2.1 后端代码

**Mapper - BrandMapper.java**

```Java
@Insert("insert into tb_brand values (null,#{brandName},#{companyName},#{ordered},#{description},#{status})")
void add(Brand brand);
```

**Service - BrandService.java**

```Java
void add(Brand brand);
```

**Service Impl - BrandServiceImpl.java**

```Java
@Override
public void add(Brand brand) {
    // 2.获取SqlSession对象
    SqlSession sqlSession = sqlSessionFactory.openSession();

    // 3.获取BrandMapper
    BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

    mapper.add(brand);

    // 4.提交事务
    sqlSession.commit();

    // 5.释放资源
    sqlSession.close();
}
```

Web - AddServlet.java

数据以 JSON 格式提交，使用 request.getReader 来获取消息体数据。

```Java
@WebServlet("/addServlet")
public class AddServlet extends HttpServlet {

    private BrandService brandService = new BrandServiceImpl();

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // 1.接收品牌数据
        BufferedReader br = request.getReader();
        String params = br.readLine(); // json字符串

        // 2.转为brand对象
        Brand brand = JSON.parseObject(params, Brand.class);

        // 3.调用service添加
        brandService.add(brand);

        // 4.响应结果
        response.getWriter().write("success");
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
```

## 2.2 前端代码

Element UI 表单

静态页面表单的按键绑定，将按钮绑定单击事件 addBrand。

```HTML
<el-form-item>
    <el-button type="primary" @click="addBrand">提交</el-button>
    <el-button @click="dialogVisible = false">取消</el-button>
</el-form-item>
```

brand.html (Vue Logic)

为了方便调用 selectAll 来展示数据，直接将 selectAll 封装成一个方法。

mounted 中调用：mounted() { this.selectAll(); }

```JavaScript
addBrand() {
    // console.log(this.brand);
    var _this = this;

    // 发送ajax异步请求
    axios({
        method: "post",
        url: "http://localhost:8080/brand-case/addServlet",
        data: _this.brand
    }).then(function (resp) {
        // 添加成功
        if(resp.data == "success"){
            // 关闭窗口
            _this.dialogVisible = false;

            // 重新查询数据
            _this.selectAll();

            // 消息提示
            _this.$message({
                message: '添加成功',
                type: 'success'
            });
        }
    })
}
```

---

# 3. 修改品牌与删除品牌

...

---

# 4. Servlet 代码优化 (BaseServlet)

**优化目标：**

- Web 层的 Servlet 个数太多，不利于管理和编写。
    
- 将 Servlet 进行归类，对于同一个实体的操作方法，写到一个 Servlet 中，比如 `BrandServlet`, `UserServlet`。
    
- 不能继承 `HttpServlet`，需自定义 `Servlet`，使用请求路径进行方法分发。
    

BaseServlet.java (反射调用)

一个通用的 HttpServlet 替代类，用于根据 URL 路径动态调用子类中的方法。

```Java
/**
 * 替换HttpServlet，根据请求的最后一段路径来进行方法分发
 */
public class BaseServlet extends HttpServlet {
    @Override
    protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 1.获取请求路径
        String uri = req.getRequestURI(); //例如: /brand-case/brand/selectAll

        // 2.获取最后一段路径，方法名
        int index = uri.lastIndexOf('/'); //获取最后一个/的位置
        String methodName = uri.substring(index + 1);

        // 3.获取BrandServlet/UserServlet 字节码对象 class
        // 谁调用我（this所在的方法），我（this）调用谁，这里的this指BrandServlet(baseServlet的子类们)，而不是Httpservlet
        Class<? extends BaseServlet> cls = this.getClass();

        // 4.获取方法Method对象
        try {
            Method method = cls.getMethod(methodName, HttpServletRequest.class, HttpServletResponse.class);
            // 执行方法
            method.invoke(this, req, resp);
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            throw new RuntimeException(e);
        } catch (IllegalAccessException e) {
            throw new RuntimeException(e);
        }
    }
}
```

**BrandServlet 优化后结构**



```Java
@WebServlet("/brand/*")
public class BrandServlet extends BaseServlet {
    private BrandService brandService = new BrandServiceImpl();

    public void selectAll(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {}

    public void add(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {}
}
```

---

# 5. 批量删除

## 5.1 后端代码

Mapper - BrandMapper.java

@Param("ids") 表示将方法参数 int[] ids 命名为 "ids"，以便在对应的 SQL 语句中引用。



```Java
void deleteByIds(@Param("ids") int[] ids);
```

Resources - BrandMapper.xml

SQL 语句复杂，使用配置文件编写。

```XML
<delete id="deleteByIds">
    delete from tb_brand where id in
    <foreach item="id" collection="ids" separator="," open="(" close=")">
        #{id}
    </foreach>
</delete>
```

**Service - BrandService.java**

```Java
void deleteByIds(int[] ids);
```

**Service Impl - BrandServiceImpl.java**

```Java
@Override
public void deleteByIds(int[] ids) {
    // 2.获取SqlSession对象
    SqlSession sqlSession = sqlSessionFactory.openSession();
    // 3.获取BrandMapper
    BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

    mapper.deleteByIds(ids);

    // 4.提交事务
    sqlSession.commit();
    // 5.释放资源
    sqlSession.close();
}
```

**Web - BrandServlet.java**

```Java
public void deleteByIds(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    // 1.接收id数组 [1,2,3]
    BufferedReader br = request.getReader();
    String params = br.readLine(); // json字符串

    // 2.转为int数组
    int[] ids = JSON.parseObject(params, int[].class);

    // 3.调用service删除
    brandService.deleteByIds(ids);

    // 4.响应结果
    response.getWriter().write("success");
}
```

## 5.2 前端代码

**HTML Button**

```HTML
<el-button type="danger" plain @click="deleteByIds">批量删除</el-button>
```

Vue Logic

在 data 中新建一个 selectedIds 模型，当 id 被选中，数组值发生变化，提交数据时提交数组到后台。

selectedIds: []

```JavaScript
// 批量删除
deleteByIds() {
    // 弹出确认提示框
    this.$confirm('此操作将删除该数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
        // 用户点击确认按钮

        // 1. 创建id数组 [1,2,3], 从 this.multipleSelection 获取即可
        for (let i = 0; i < this.multipleSelection.length; i++) {
            let selectionElement = this.multipleSelection[i];
            this.selectedIds[i] = selectionElement.id;
        }

        // 2. 发送AJAX请求
        var _this = this;

        // 发送ajax请求，删除数据
        axios({
            method: "post",
            url: "http://localhost:8080/brand-case/brand/deleteByIds",
            data: _this.selectedIds
        }).then(function (resp) {
            if(resp.data == "success"){
                // 删除成功
                // 重新查询数据
                _this.selectAll();
                // 弹出消息提示
                _this.$message({
                    message: '恭喜你，删除成功',
                    type: 'success'
                });
            }
        })
    }).catch(() => {
        // 用户点击取消按钮
        this.$message({
            type: 'info',
            message: '已取消删除'
        });
    });
}
```

---

# 6. 分页查询

**原理：**

- **LIMIT 参数**：参数1=开始索引，参数2=查询的条目数 (`SELECT * FROM tb_brand LIMIT 0,5`)
    
- **参数传递**：前端传递当前页码 `currentPage` 与 每页查询的条目数 `pageSize`。
    
- **返回数据**：后台返回当前页数据 `List` 与 总记录数 `totalCount`。
    
- **计算公式**：开始索引 = `(currentPage - 1) * pageSize`。
    

## 6.1 后端代码

POJO - PageBean.java

实体类中定义 Bean，泛型声明 T 让代码通用。

```Java
// 分页查询的JavaBean
public class PageBean<T> {
    // 总记录数
    private int totalCount;
    // 当前页数据
    private List<T> rows;

    public int getTotalCount() { return totalCount; }
    public void setTotalCount(int totalCount) { this.totalCount = totalCount; }
    public List<T> getRows() { return rows; }
    public void setRows(List<T> rows) { this.rows = rows; }
}
```

**Mapper - BrandMapper.java**

```Java
/**
 * 分页查询
 * @param begin
 * @param size
 * @return
 */
@Select("select * from tb_brand limit #{begin} , #{size}")
@ResultMap("brandResultMap")
List<Brand> selectByPage(@Param("begin") int begin, @Param("size") int size);

/**
 * 查询总记录数
 * @return
 */
@Select("select count(*) from tb_brand ")
@ResultMap("brandResultMap")
int selectTotalCount();
```

**Service - BrandService.java**

```Java
PageBean<Brand> selectByPage(int currentPage, int pageSize);
```

**Service Impl - BrandServiceImpl.java**

```Java
@Override
public PageBean<Brand> selectByPage(int currentPage, int pageSize) {
    SqlSession sqlSession = factory.openSession();
    BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

    // 4. 计算开始索引
    int begin = (currentPage - 1) * pageSize;
    // 计算查询条目数
    int size = pageSize;

    // 5. 查询当前页数据
    List<Brand> rows = mapper.selectByPage(begin, size);

    // 6. 查询总记录数
    int totalCount = mapper.selectTotalCount();

    // 7. 封装PageBean对象
    PageBean<Brand> pageBean = new PageBean<>();
    pageBean.setRows(rows);
    pageBean.setTotalCount(totalCount);

    // 8. 释放资源
    sqlSession.close();

    return pageBean;
}
```

Web - BrandServlet.java

请求中接收的类型是 String 类型，而查询中需要的为 int 类型，所以需要强制转换。

```Java
public void selectByPage(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    // 1. 接收 当前页码 和 每页展示数  url?currentPage=1&pageSize=5
    String _currentPage = request.getParameter("currentPage");
    String _pageSize = request.getParameter("pageSize");

    int currentPage = Integer.parseInt(_currentPage);
    int pageSize = Integer.parseInt(_pageSize);

    // 2. 调用service查询
    PageBean<Brand> pageBean = brandService.selectByPage(currentPage, pageSize);

    // 3. 转为JSON
    String jsonString = JSON.toJSONString(pageBean);

    // 4. 写数据
    response.setContentType("text/json;charset=utf-8");
    response.getWriter().write(jsonString);
}
```

## 6.2 前端代码

**HTML - 分页工具条**

```HTML
<el-pagination
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    :current-page="currentPage"
    :page-sizes="[5, 10, 15, 20]"
    :page-size="5"
    layout="total, sizes, prev, pager, next, jumper"
    :total="totalCount">
</el-pagination>
```

Vue Logic

修改 selectAll，URL 直接使用拼字符串的方式。totalCount 处展示总记录数。

Data 模型设置：pageSize: 5, totalCount: 100, currentPage: 1。

```JavaScript
// 动态分页
handleSizeChange(val) {
    // console.log(`每页 ${val} 条`);
    // 重新设置每页显示的条数
    this.pageSize = val;
    this.selectAll();
},
handleCurrentChange(val) {
    // console.log(`当前页: ${val}`);
    // 重新设置当前页码
    this.currentPage = val;
    this.selectAll();
},
selectAll() {
    var _this = this;
    axios({
        method: "post",
        url: "http://localhost:8080/brand-case/brand/selectByPage?currentPage=" + _this.currentPage + "&pageSize=" + _this.pageSize,
    }).then(function(resp){
        _this.tableData = resp.data.rows;
        _this.totalCount = resp.data.totalCount;
        console.log(resp.data);
    })
}
```

---

# 7. 条件查询

需要完成条件查询，并且按照分页的形式展示。

## 7.1 后端代码

Mapper - BrandMapper.java

使用 Integer 作为返回值，即使查询结果为空，MyBatis 也能安全地返回 null。

```Java
List<Brand> selectByPageAndCondition(@Param("begin") int begin, @Param("size") int size, @Param("brand") Brand brand);

Integer selectTotalCountByCondition(Brand brand);
```

Resources - BrandMapper.xml

动态 SQL 编写，使用 like 进行模糊匹配。

```XML

<select id="selectByPageAndCondition" resultMap="brandResultMap">
    select * from tb_brand
    <where>
        <if test="brandName != null and brandName != ''">
            and brand_name like #{brandName}
        </if>
        <if test="companyName != null and companyName != ''">
            and company_name like #{companyName}
        </if>
        <if test="status != null">
            and status = #{status}
        </if>
    </where>
    limit #{begin}, #{size}
</select>

<select id="selectTotalCountByCondition" resultMap="brandResultMap">
    select count(*) from tb_brand
    <where>
        <if test="brandName != null and brandName != ''">
            and brand_name like #{brandName}
        </if>
        <if test="companyName != null and companyName != ''">
            and company_name like #{companyName}
        </if>
        <if test="status != null">
            and status = #{status}
        </if>
    </where>
</select>
```

Service Impl - BrandServiceImpl.java

处理 brand 对象，对用户的输入封装成模糊表达式的形式（如 %name%）。

```Java
@Override
public PageBean<Brand> selectByPageAndCondition(int currentPage, int pageSize, Brand brand) {
    SqlSession sqlSession = factory.openSession();
    BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

    int begin = (currentPage - 1) * pageSize;
    int size = pageSize;

    // 处理brand条件，模糊表达式
    String brandName = brand.getBrandName();
    if(brandName != null && brandName.length() > 0){
        brand.setBrandName("%" + brandName + "%");
    }

    String companyName = brand.getCompanyName();
    if(companyName != null && companyName.length() > 0){
        brand.setCompanyName("%" + companyName + "%");
    }

    // 4.查询当前页数据
    List<Brand> rows = mapper.selectByPageAndCondition(begin, size, brand);

    // 5.查询总记录数
    int totalCount = mapper.selectTotalCountByCondition(brand);

    PageBean<Brand> pageBean = new PageBean<>();
    pageBean.setRows(rows);
    pageBean.setTotalCount(totalCount);

    sqlSession.close();
    return pageBean;
}
```

Web - BrandServlet.java

Brand 的数据通过前端传递（POST data），currentPage 和 pageSize 使用 URL 传递。

```Java
public void selectByPageAndCondition(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    // 1. 接收两个参数 currentPage pageSize
    String _currentPage = request.getParameter("currentPage");
    String _pageSize = request.getParameter("pageSize");

    // 获取查询条件对象
    BufferedReader br = request.getReader();
    String params = br.readLine(); // json字符串

    Brand brand = JSON.parseObject(params, Brand.class);

    int currentPage = Integer.parseInt(_currentPage);
    int pageSize = Integer.parseInt(_pageSize);

    PageBean<Brand> pageBean = brandService.selectByPageAndCondition(currentPage, pageSize, brand);

    // 转为json
    String json = JSON.toJSONString(pageBean);
    response.setContentType("text/json;charset=utf-8");
    response.getWriter().write(json);
}
```

## 7.2 前端代码

Vue Logic (优化后)

将请求改为 POST 形式，并使用 data 将 brand 传入 selectAll 中。

优化：使用箭头函数 => 替代 var _this = this。

```JavaScript
// 查询所有（含条件）
selectAll() {
    axios({
        method: "post",
        url: "http://localhost:8080/brand-case/brand/selectByPageAndCondition?currentPage=" + this.currentPage + "&pageSize=" + this.pageSize,
        data: this.brand
    }).then(resp => {
        // 设置表格数据
        this.tableData = resp.data.rows; // {rows:[], totalCount:100}
        // 设置总记录数
        this.totalCount = resp.data.totalCount;
    })
},
onSubmit() {
    console.log(this.brand);
    this.selectAll();
}
```









