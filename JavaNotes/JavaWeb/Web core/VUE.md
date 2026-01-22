Vue 是一套前端框架，免除原生 JavaScript 中的 **[[JavaScript#^e157a0|DOM]]** 操作。
# 为什么使用 Vue？

## 原生 JS 的 DOM 操作痛点
在上一节 [[AJAX]] 案例中，我们需要频繁操作 DOM，代码繁琐。例如：

```javascript
// 1. 将表单数据转为json
var formData = {
    brandName: "",
    companyName: "",
    ordered: "",
    description: "",
    status: "",
};

// 2. 获取表单数据并设置
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
    if (status[i].checked) {
        formData.status = status[i].value;
    }
}
```

## MVVM 思想

基于 **MVVM (Model-View-ViewModel)** 思想，实现数据的双向绑定。

- 将编程的关注点放在数据上。
    
- 当 ViewModel 中的数据发生变化时，数据绑定会自动更新 View 中绑定到这些数据的部分，反之亦然。
    

---

# Vue 快速入门

## 1. 引入 Vue.js

新建 HTML 页面，引入 Vue.js 文件：

HTML

```
<script src="js/vue.js"></script>
```

## 2. 创建 Vue 核心对象

在 JS 代码区域，创建 Vue 核心对象，进行数据绑定：

```JavaScript
new Vue({
    el: "#app", // element 用来指定 vue 的作用范围，这里使用 id 选择器，选定 id=app
    data() {
        return {
            username: ""
        }
    }
});
```

## 3. 编写视图

```HTML
<div id="app">
    <input v-model="username">
    {{username}}
</div>
```

---

# Vue 常用指令

指令是 HTML 标签上带有 `v-` 前缀的特殊属性，不同指令具有不同含义。

## 1. v-bind

作用：为 HTML 标签绑定属性值，如设置 href，css 样式等。

简化书写：直接在属性名前加 : 即可。

**示例代码**：

```HTML
<div id="app">
    <a v-bind:href="url">点击一下</a>
    <a :href="url">点击一下</a>
    
    <input v-model="url">
</div>

<script src="js/vue.js"></script>
<script>
    // 创建 Vue 核心对象
    new Vue({
        el: "#app",
        data() {
            return {
                username: "",
                url: "[https://www.baidu.com](https://www.baidu.com)"
            }
        }
    });
</script>
```

## 2. v-model

**作用**：在表单元素上创建双向数据绑定。

## 3. v-on

作用：为 HTML 标签绑定事件。

简化书写：@

**示例代码**：

```HTML
<div id="app">
    <input type="button" value="一个按钮" v-on:click="show()"><br>
    <input type="button" value="一个按钮" @click="show()">
</div>

<script src="js/vue.js"></script>
<script>
    new Vue({
        el: "#app",
        data() {
            return {
                username: "",
                url: "[https://www.baidu.com](https://www.baidu.com)"
            }
        },
        methods: {
            show() {
                alert("我被点了...");
            }
        }
    });
</script>
```

## 4. v-if 与 v-show

**作用**：

- **v-if**：条件性地渲染某元素。判断为 `true` 时渲染，否则不渲染（DOM 中不存在）。
    
- **v-show**：根据条件展示某元素。区别在于切换的是 CSS 的 `display` 属性的值。
    

**示例代码**：

```HTML
<div id="app">
    <div v-if="count == 3">div1</div>
    <div v-else-if="count == 4">div2</div>
    <div v-else>div3</div>
    <hr>
    <div v-show="count == 3">div v-show</div>
    <br>
    <input v-model="count">
</div>

<script src="js/vue.js"></script>
<script>
    new Vue({
        el: "#app",
        data() {
            return {
                username: "",
                url: "[https://www.baidu.com](https://www.baidu.com)",
                count: 3
            }
        },
        methods: {
            show() {
                alert("我被点了...");
            }
        }
    });
</script>
```

## 5. v-for

作用：列表渲染，遍历容器的元素和对象的属性。

说明：i 表示索引，从 0 开始。

**示例代码**：

```HTML
<div id="app">
    <div v-for="addr in addrs">
        {{addr}} <br>
    </div>
    <hr>
    <div v-for="(addr, i) in addrs">
        {{i+1}}--{{addr}} <br>
    </div>
</div>

<script src="js/vue.js"></script>
<script>
    new Vue({
        el: "#app",
        data() {
            return {
                username: "",
                url: "[https://www.baidu.com](https://www.baidu.com)",
                count: 3,
                addrs: ["北京", "上海", "西安"]
            }
        },
        methods: {
            show() {
                alert("我被点了...");
            }
        }
    });
</script>
```

---

# Vue 生命周期

Vue 实例在生命周期的八个阶段中，每触发一个生命周期事件，会自动执行对应的生命周期方法。

- **beforeCreate**: 创建前
    
- **created**: 创建后
    
- **beforeMount**: 载入前
    
- **mounted**: 挂载完成。Vue 初始化完成，HTML 页面渲染完成。**通常在此发送异步请求加载数据**。
    
    - _注：在这之前通常使用 `window.onload` 来实现页面加载完成发送异步请求，现在可以使用 `mounted` 来代替。_
        
- **beforeUpdate**: 更新前
    
- **updated**: 更新后
    
- **beforeDestroy**: 销毁前
    
- **destroyed**: 销毁后
    

**mounted 示例**：

```JavaScript
new Vue({
    el: "#app",
    data() {
        return {
            // ...数据
        }
    },
    methods: {
        // ...方法
    },
    mounted() {
        alert("加载完成...");
    }
});
```

---

# 案例：品牌列表管理

**需求**：使用 Vue 简化品牌列表数据查询和添加功能。

## 1. 查询所有

HTML (brand.html)

使用 v-for 遍历 tr，并且使用插值表达式来取数据，展示到对应的表格中。

```HTML
<div id="app">
    <a href="addBrand.html"><input type="button" value="新增"></a><br>
    <hr>
    <table id="brandTable" border="1" cellspacing="0" width="100%">
        <tr>
            <th>序号</th>
            <th>品牌名称</th>
            <th>企业名称</th>
            <th>排序</th>
            <th>品牌介绍</th>
            <th>状态</th>
            <th>操作</th>
        </tr>
        <tr v-for="(brand, i) in brands" align="center">
            <td>{{i + 1}}</td>
            <td>{{brand.brandName}}</td>
            <td>{{brand.companyName}}</td>
            <td>{{brand.ordered}}</td>
            <td>{{brand.description}}</td>
            <td>{{brand.statusStr}}</td>
            <td><a href="#">修改</a> <a href="#">删除</a></td>
        </tr>
    </table>
</div>
<script src="js/axios-0.18.0.js"></script>
<script src="js/vue.js"></script>
```

JavaScript

在 mounted 中指定一个函数，页面加载完成后，发送异步请求查询数据。

```JavaScript
new Vue({
    el: "#app",
    data() {
        return {
            brands: []
        }
    },
    mounted() {
        // 页面加载完成后，发送异步请求，查询数据
        var _this = this;
        axios({
            method: "get",
            url: "http://localhost:8080/brand-demo/selectAllServlet"
        }).then(function(resp) {
            _this.brands = resp.data;
        })
    }
})
```

关于 _this 的说明：

在发送 axios 请求后的回调函数中，我们需要将响应回来的数据 resp.data 赋值给模型中的 brands。

- 如果在回调函数中直接使用 `this.brands`，这里的 `this` 指向的是 `window` 对象，而不是 Vue 对象。
    
- 所以需要在 axios 外面定义一个变量 `var _this = this;` 来保存 Vue 对象的引用，以便在回调函数中使用。
    

## 2. 添加品牌

**HTML**

```HTML
<div id="app">
    <h3>添加品牌</h3>
    <form action="" method="post">
        品牌名称：<input id="brandName" v-model="brand.brandName" name="brandName"><br>
        企业名称：<input id="companyName" v-model="brand.companyName" name="companyName"><br>
        排序：<input id="ordered" v-model="brand.ordered" name="ordered"><br>
        描述信息：<textarea rows="5" cols="20" id="description" v-model="brand.description" name="description"></textarea><br>
        状态：
        <input type="radio" name="status" v-model="brand.status" value="0">禁用
        <input type="radio" name="status" v-model="brand.status" value="1">启用<br>

        <input type="button" id="btn" @click="submitForm" value="提交">
    </form>
</div>
<script src="js/axios-0.18.0.js"></script>
<script src="js/vue.js"></script>
```

JavaScript

按钮上绑定单击事件 @click，在 Vue 中定义 submitForm 方法发送异步请求。

```JavaScript
new Vue({
    el: "#app",
    data() {
        return {
            brand: {}
        }
    },
    methods: {
        submitForm() {
            // 发送 ajax 请求，添加
            var _this = this;
            axios({
                method: "post",
                url: "http://localhost:8080/brand-demo/addServlet",
                data: _this.brand
            }).then(function(resp) {
                // 判断响应数据是否为 success
                if (resp.data == "success") {
                    location.href = "http://localhost:8080/brand-demo/brand.html";
                }
            })
        }
    }
})
```

与原生 JS 对比：

在之前的原生 JS 案例中，我们需要手动获取表单数据并封装成 JSON 对象（如下所示）。而在 Vue 框架下，我们定义一个 brand 模型进行双向绑定，axios 直接传入 _this.brand 即可。

```JavaScript
// 原生 JS 写法（Vue 中不需要）
document.getElementById("btn").onclick = function() {
    var formData = {
        brandName: "",
        companyName: "",
        ordered: "",
        description: "",
        status: "",
    };
    // ...后续获取值逻辑
}
```