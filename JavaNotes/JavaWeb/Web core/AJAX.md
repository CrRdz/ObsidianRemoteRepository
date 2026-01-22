# 1. AJAX 概述

- **概念**：Asynchronous JavaScript And XML（异步的 JavaScript 和 XML）。
    
- **作用**：
    
    - **与服务器进行数据交换**：通过 AJAX 可以给服务器发送请求，并获取服务器响应的数据。
        
    - **异步交互**：可以在不重新加载整个页面的情况下，与服务器交换数据，并更新部分网页的技术（如：搜索联想、用户名是否可用校验等）。
        
- **演变**：
    
    - **以往方式**：通过 Servlet 查询数据 $\rightarrow$ 将数据存到域对象中 $\rightarrow$ 转发到 JSP 展示数据（将 JSP 当作视图，对浏览器做响应）。
        
    - **AJAX 方式**：使用 AJAX 和服务器进行通信，就可以使用 HTML+AJAX 来替换 JSP 页面了。
        
    - **优势**：实现前后端分离，前端负责 HTML+AJAX，后端负责数据提交逻辑处理。
        

---

# 2. AJAX 快速入门（原生代码开发）

## 开发步骤

1. 编写 `AjaxServlet`，并使用 `response` 输出字符串。
    
2. 创建 `XMLHttpRequest` 对象：用于和服务器交换数据。
    
3. 向服务器发送请求。
    
4. 获取服务器响应数据。
    

## 代码示例

```JavaScript
var xhttp;
// 1. 创建核心对象
if (window.XMLHttpRequest) {
    xhttp = new XMLHttpRequest();
} else {
    // code for IE6, IE5
    xhttp = new ActiveXObject("Microsoft.XMLHTTP");
}

// 2. 向服务器发送请求 (写全路径)
xhttp.open("GET", "http://localhost:8080/ajax-demo/ajaxServlet");
xhttp.send();

// 3. 获取服务器响应数据
xhttp.onreadystatechange = function() {
    // readyState：保存了 XMLhttpRequest 的状态
    // 0：请求未初始化
    // 1：服务器连接已建立
    // 2：请求已接收
    // 3：正在处理请求
    // 4：请求已完成且响应已就绪
    if (this.readyState == 4 && this.status == 200) {
        alert(this.responseText);
    }
};
```

---

# 3. 案例：使用 AJAX 验证用户名是否存在

**需求**：在完成用户注册时，当用户名输入框失去焦点时，校验用户名是否在数据库已存在。

## 后端代码：`SelectUserServlet.java`


```Java
@WebServlet("/selectUserServlet")
public class SelectUserServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // 1. 接收用户名
        String username = request.getParameter("username");

        // 2. 调用 service 查询 User 对象 (此处模拟)
        boolean flag = true; 

        // 3. 响应标记
        response.getWriter().write("" + flag);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
```

## 前端代码：`Register.html`

```HTML
<script>
    // 1. 给用户名输入框绑定失去焦点事件
    document.getElementById("username").onblur = function () {
        // 2. 发送 ajax 请求
        // 获取用户名的值
        var username = this.value;

        // 2.1. 创建核心对象
        var xhttp;
        if (window.XMLHttpRequest) {
            xhttp = new XMLHttpRequest();
        } else {
            // code for IE6, IE5
            xhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }

        // 2.2. 发送请求
        xhttp.open("GET", "http://localhost:8080/ajax-demo/selectUserServlet?username=" + username);
        xhttp.send();

        // 2.3. 获取响应
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                // alert(this.responseText);
                // 判断
                if(this.responseText == "true"){
                    // 用户名存在，显示提示信息
                    document.getElementById("username_err").style.display = '';
                } else {
                    // 用户名不存在，清除提示信息
                    document.getElementById("username_err").style.display = 'none';
                }
            }
        };
    }
</script>
```

---

# 4. Axios 异步框架

Axios 对原生的 AJAX 进行封装，简化书写。

> 参考：[Axios-中文](https://www.axios-http.cn/)

## 4.1 引入 JS 文件

在 webapp 中创建一个 js 包，用来存放所有的 js 文件，这里存入 axios 源码：

```HTML
<script src="js/axios-0.18.0.js"></script>
```

## 4.2 基础使用

**后端：`AxiosServlet.java`**

```Java
@WebServlet("/axiosServlet")
public class AxiosServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println("get...");
        // 1. 接收请求参数
        String username = request.getParameter("username");
        System.out.println(username);
        // 2. 响应数据
        response.getWriter().write("hello Axios~");
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println("post...");
        this.doGet(request, response);
    }
}
```

**前端：`axios-demo.html`**

**方式一：通用方式**

```JavaScript
<script>
    // 1. get
    axios({
        method: "get",
        url: "http://localhost:8080/ajax-demo/axiosServlet?username=zhangsan"
    }).then(function (resp) {
        // 通过 .then 获取对应的响应，方法被执行时，resp 就有响应数据
        alert(resp.data);
    });

    // 2. post
    axios({
        method: "post",
        url: "http://localhost:8080/ajax-demo/axiosServlet",
        data: "username=zhangsan"
    }).then(function (resp) {
        alert(resp.data);
    });
</script>
```

方式二：请求方式别名

Axios 为所有支持的请求方法提供了别名（简化但是阅读性不如原生书写格式）：

- `axios.get(url[,config])`
    
- `axios.post(url[,data[,config]])`
    
```JavaScript
// Get 请求
axios.get("http://localhost:8080/ajax-demo/axiosServlet?username=zhangsan")
    .then(function (resp) {
        alert(resp.data);
    });

// Post 请求
axios.post("http://localhost:8080/ajax-demo/axiosServlet", "username=zhangsan")
    .then(function (resp) {
        alert(resp.data);
    });
```

## 4.3 案例重写：验证用户名是否存在 (Axios 版)


```JavaScript
// 给用户名输入框绑定失去焦点事件
document.getElementById("username").onblur = function () {
    // 获取用户名的值
    var username = this.value;

    // 使用 axios 发送 GET 请求
    axios.get('http://localhost:8080/ajax-demo/selectUserServlet?username=zhangsan')
    .then(function (response) {
        // 处理响应结果
        if (response.data === "true") {
            // 用户名存在，显示提示信息
            document.getElementById("username_err").style.display = '';
        } else {
            // 用户名不存在，隐藏提示信息
            document.getElementById("username_err").style.display = 'none';
        }
    });
}
```

---

# 5. JSON (JavaScript Object Notation)

## 概述

- **定义**：JavaScript Object Notation，JavaScript 对象表示法。
    
- **特点**：由于语法简单，层次结构鲜明，多用于数据载体，在网络中进行数据传输。
    

## JSON 基础语法

```JavaScript
var 变量名 = {
    "key1": value1,
    "key2": value2,
    ...
};
```

- **Value 的数据类型**：数字（整数/浮点数）、字符串（在双引号中）、逻辑值（true/false）、数组（在方括号中）、对象（在花括号中）、Null。
    
- **获取数据**：`变量名.key` 或 `Json.name`。
    

## JSON 数据和 Java 对象转换

- **请求数据**：JSON 字符串转为 Java 对象。
    
- **响应数据**：Java 对象转为 JSON 字符串。
    
- **工具**：**Fastjson**（一个 Java 语言编写的高性能功能完善的 JSON 库，可以实现 Java 和 JSON 字符串的相互转换）。
    

**1. 导入坐标**

```XML
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>fastjson</artifactId>
    <version>1.2.62</version>
</dependency>
```

**2. 使用方法**

- **Java 对象转 JSON**：`String jsonStr = JSON.toJSONString(obj);`
    
- **JSON 字符串转 Java 对象**：`User user = JSON.parseObject(jsonStr, User.class);`
    

---

# 6. 综合案例：品牌管理

**需求**：完成品牌列表查询和添加（使用 Axios + JSON）。

## 6.1 查询所有品牌

**后端：Service 层**

```Java
/**
 * 查询所有
 * @return
 */
public List<Brand> selectAll(){
    // 1. 获取 SqlSession
    SqlSession sqlSession = factory.openSession();
    // 2. 获取 BrandMapper
    BrandMapper mapper = sqlSession.getMapper(BrandMapper.class);

    // 3. 调用方法
    List<Brand> brands = mapper.selectAll();

    sqlSession.close();
    return brands;
}
```

**后端：`SelectAllServlet.java`**

```Java
@WebServlet("/selectAllServlet")
public class SelectAllServlet extends HttpServlet {
    private BrandService brandService = new BrandService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // 1. 调用 Service 查询
        List<Brand> brands = brandService.selectAll();

        // 2. 将集合转换为 JSON 数据 (序列化)
        String jsonString = JSON.toJSONString(brands);

        // 3. 响应数据，响应到对应页面上
        response.setContentType("text/json;charset=utf-8");
        response.getWriter().write(jsonString);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
```

**前端：`Brand.html` (数据渲染)**

```JavaScript
<script>
    // 1. 当页面加载完成后，发送 ajax 请求
    window.onload = function () {
        // 2. 发送 ajax 请求
        axios({
            method: "get",
            url: "http://localhost:8080/brand-demo/selectAllServlet"
        }).then(function (resp) {
            // 获取数据 (resp.data 是服务器返回的实际数据)
            let brands = resp.data;
            
            // 表头
            let tableData = " <tr>\n" +
                "        <th>序号</th>\n" +
                "        <th>品牌名称</th>\n" +
                "        <th>企业名称</th>\n" +
                "        <th>排序</th>\n" +
                "        <th>品牌介绍</th>\n" +
                "        <th>状态</th>\n" +
                "        <th>操作</th>\n" +
                "    </tr>";

            // 遍历数据并拼接 HTML
            for (let i = 0; i < brands.length ; i++) {
                let brand = brands[i];
                tableData += "\n" +
                    "    <tr align=\"center\">\n" +
                    "        <td>"+(i+1)+"</td>\n" +
                    "        <td>"+brand.brandName+"</td>\n" +
                    "        <td>"+brand.companyName+"</td>\n" +
                    "        <td>"+brand.ordered+"</td>\n" +
                    "        <td>"+brand.description+"</td>\n" +
                    "        <td>"+brand.status+"</td>\n" +
                    "\n" +
                    "        <td><a href=\"#\">修改</a> <a href=\"#\">删除</a></td>\n" +
                    "    </tr>";
            }

            // 设置表格数据
            document.getElementById("brandTable").innerHTML = tableData;
        })
    }
</script>
```

## 6.2 新增品牌

> **关于 `resp` 对象的说明**：
> 
> - `resp` 是 axios 发起的 HTTP 请求成功返回后，传递给 `.then()` 回调函数的响应对象。
>     
> - `resp.data`: 实际从服务器返回的数据（通常是 JSON 格式）。
>     
> - `resp.status`: HTTP 状态码，如 200 表示请求成功。
>     
> - `resp.headers`: 响应头信息。
>     
> - `resp.config`: 当前请求的配置信息。
>     

前端：addBrand.html

注意：增删改一般建议使用 post 的请求方式。var formData 操作是为了创建 json 对象。console.log 用于在控制台输出任何类型的信息。

```JavaScript
<script>
    // 1. 给按钮绑定单击事件
    document.getElementById("btn").onclick = function () {
        // 将表单数据转为 json
        var formData = {
            brandName:"",
            companyName:"",
            ordered:"",
            description:"",
            status:"",
        };
        
        // 获取表单数据并设置到 json 对象中
        let brandName = document.getElementById("brandName").value;
        formData.brandName = brandName;

        let companyName = document.getElementById("companyName").value;
        formData.companyName = companyName;

        let ordered = document.getElementById("ordered").value;
        formData.ordered = ordered;

        let description = document.getElementById("description").value;
        formData.description = description;

        let status = document.getElementsByName("status");
        for (let i = 0; i < status.length; i++) {
            if(status[i].checked){
                formData.status = status[i].value;
            }
        }

        console.log(formData);

        // 2. 发送 ajax 请求
        axios({
            method: "post",
            url: "http://localhost:8080/brand-demo/addServlet",
            data: formData
        }).then(function (resp) {
            // 判断响应数据是否为 success
            if(resp.data == "success"){
                location.href = "http://localhost:8080/brand-demo/brand.html";
            }
        })
    }
</script>
```

**后端：`addServlet.java`**

> **注意**：`request.getParameter` 不能接收 JSON 数据，需要通过 `request.getReader()` 获取请求体数据，并把 JSON 字符转为 Java 对象。因为 `application/x-www-form-urlencoded` 是 Post 请求默认的请求体内容类型，也是 form 表单默认的类型，Servlet API 规范中对该类型的请求内容提供了 `request.getParameter()` 方法。但当请求内容不是该类型时（如 JSON），需要调用 `request.getInputStream()` 或 `request.getReader()` 方法来获取请求内容值。

```Java

@WebServlet("/addServlet")
public class AddServlet extends HttpServlet {

    private BrandService brandService = new BrandService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        
        // 1. 接收数据, request.getParameter 不能接收 json 的数据
        /* String brandName = request.getParameter("brandName");
           System.out.println(brandName);*/

        // 获取请求体数据
        BufferedReader br = request.getReader();
        String params = br.readLine();

        // 将 JSON 字符串转为 Java 对象
        Brand brand = JSON.parseObject(params, Brand.class);

        // 2. 调用 service 添加
        brandService.add(brand);

        // 3. 响应成功标识
        response.getWriter().write("success");
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
}
```