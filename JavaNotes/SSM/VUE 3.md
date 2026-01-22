# 基础篇
## 1. 前端基础回顾

- **HTML**：负责网页的结构（标签：`form`/`table`/`a`/`div`/`span`）
    
- **CSS**：负责网页的表现（样式：`color`/`font`/`background`/`height`）
    
- **JavaScript**：负责网页的行为（交互效果）
    

### JavaScript 导入导出

JS 提供的导入导出机制，可以实现按需导入。导入和导出的时候，可以使用 `as` 重命名。

---

## 2. 局部使用 Vue

Vue 是一款用于构建用户界面的渐进式 JavaScript 框架，提供声明式渲染、组件系统、客户端路由、状态管理、构建工具等功能。

### 快速入门

#### 准备工作

1. 准备 HTML 页面，并引入 Vue 模块（官方提供）。
    
2. 创建 Vue 程序的实例。
    
3. 准备元素（如 `div`），被 Vue 控制。
    

#### 构建用户界面

1. 准备数据。
    
2. 通过插值表达式 `{{ }}` 渲染页面。
    

**代码示例：**

```HTML
<body>
    <div id="app">
        <h1>{{msg}}</h1>
    </div>

    <div>
        <h1>{{msg}}</h1>
    </div>

    <script type="module">
        import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
        
        /* 创建 vue 的应用实例 */
        createApp({
            data() {
                return {
                    // 定义数据
                    msg: 'hello vue3'
                }
            }
        }).mount("#app");
    </script>
</body>
```

---

## 3. 常用指令

指令：HTML 标签上带有 `v-` 前缀的特殊属性，不同的指令具有不同的含义，可以实现不同的功能。

### v-for

作用：列表渲染，遍历容器的元素或者对象的属性。

语法：v-for="(item, index) in items"

**参数说明**：

- `items`: 遍历的数组
    
- `item`: 遍历出来的元素
    
- `index`: 索引/下标（从 0 开始；可以省略）
    
- 省略 index 语法：`v-for="item in items"`
    

**代码示例：**

```HTML
<script type="module">
    // 导入 vue 模块
    import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'
    
    // 创建应用实例
    createApp({
        data() {
            return {
                // 定义数据
                articleList: [
                    {
                        title: "医疗反腐绝非砍医护收入",
                        category: "时事",
                        time: "2023-09-5",
                        state: "已发布"
                    },
                    {
                        title: "中国男篮缘何一败涂地？",
                        category: "篮球",
                        time: "2023-09-5",
                        state: "草稿"
                    },
                    {
                        title: "华山景区已受大风影响阵风达7-8级，未来24小时将持续",
                        category: "旅游",
                        time: "2023-09-5",
                        state: "已发布"
                    }
                ]
            }
        }
    }).mount("#app") // 控制页面元素
</script>

<div id="app">
    <table border="1 solid" colspan="0" cellspacing="0">
        <tr>
            <th>文章标题</th>
            <th>分类</th>
            <th>发表时间</th>
            <th>状态</th>
            <th>操作</th>
        </tr>
        <tr v-for="(article, index) in articleList">
            <td>{{article.title}}</td>
            <td>{{article.category}}</td>
            <td>{{article.time}}</td>
            <td>{{article.state}}</td>
            <td>
                <button>编辑</button>
                <button>删除</button>
            </td>
        </tr>
    </table>
</div>
```

### v-bind

作用：为 HTML 绑定属性值，如设置 href、css 样式等。

语法：v-bind:属性名="属性值"

简化：:属性名="属性值"

> 注意：v-bind 所绑定的数据，必须在 `data` 中定义。

**代码示例：**

```HTML
<body>
    <div id="app">
        <a :href="url">黑马官网</a>
    </div>

    <script type="module">
        import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'
        
        createApp({
            data() {
                return {
                    url: 'https://www.itheima.com'
                }
            }
        }).mount("#app")
    </script>
</body>
```

### v-if / v-else-if / v-else / v-show

**作用**：条件性地渲染某元素。

#### v-if

- **语法**：`v-if="表达式"`（表达式值为 true 显示，false 隐藏）。
    
- **特点**：判定为 true 时渲染，否则不渲染（从 DOM 中移除）。
    
- **场景**：要么显示，要么不显示，不频繁切换的场景。
    
- **链式调用**：可以配合 `v-else-if` / `v-else` 使用。
    

#### v-show

- **语法**：`v-show="表达式"`（表达式值为 true 显示，false 隐藏）。
    
- **原理**：基于 CSS 样式 `display` 来控制显示与隐藏。
    
- **场景**：频繁切换显示隐藏的场景。
    

**代码示例：**

```HTML
<body>
    <div id="app">
        手链价格为: 
        <span v-if="customer.level >= 0 && customer.level <= 1">9.9</span>
        <span v-else-if="customer.level >= 2 && customer.level <= 4">19.9</span>
        <span v-else>29.9</span>

        <br/>
        
        手链价格为: 
        <span v-show="customer.level >= 0 && customer.level <= 1">9.9</span>
        <span v-show="customer.level >= 2 && customer.level <= 4">19.9</span>
        <span v-show="customer.level >= 5">29.9</span>
    </div>

    <script type="module">
        import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'

        createApp({
            data() {
                return {
                    customer: {
                        name: '张三',
                        level: 2
                    }
                }
            }
        }).mount("#app")
    </script>
</body>
```

### v-on

作用：为 HTML 标签绑定事件。

语法：v-on:事件名="函数名"

简写：@事件名="函数名"

**代码示例：**

```HTML
<body>
    <div id="app">
        <button v-on:click="money">点我有惊喜</button>
        <button @click="love">再点更惊喜</button>
    </div>

    <script type="module">
        import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'

        createApp({
            data() {
                return {}
            },
            methods: {
                money: function() {
                    alert('送你钱100')
                },
                love: function() {
                    alert('爱你一万年')
                }
            }
        }).mount("#app");
    </script>
</body>
```

### v-model

作用：在表单元素上使用，实现双向数据绑定。

语法：v-model="变量名"

效果：用户输入内容时，数据会自动更新；数据变化时，输入框内容也会自动变化。

> 注意：v-model 中绑定的变量，必须在 `data` 中定义。

**代码示例：**

```HTML
<div id="app">
    文章分类: <input type="text" v-model="searchConditions.category"/> 
    <span>{{searchConditions.category}}</span>

    发布状态: <input type="text" v-model="searchConditions.state"/> 
    <span>{{searchConditions.state}}</span>

    <button>搜索</button>
    <button v-on:click="clear">重置</button>
    
    </div>
```

---

## 4. 生命周期

定义：指一个对象从创建到销毁的整个过程。

八个阶段：每个阶段会自动执行一个生命周期钩子，让开发者有机会在特定的阶段执行自己的代码。

- **mounted**：在页面加载完毕时触发。常用于发起异步请求，加载数据，渲染页面。
    

---

## 5. Axios

简介：Axios 对原生 Ajax 进行了封装，简化书写，快速开发。

参数说明：

- `Method`: 请求方式 (GET/POST)
    
- `Url`: 请求路径
    
- `Data`: 请求数据
    

### 基础用法

**发送 GET 请求：**

```JavaScript
axios({
    method: 'get',
    url: 'http://localhost:8080/article/getAll'
}).then(result => {
    // 成功的回调
    // result.data 代表的是接口响应的核心数据
    console.log(result.data);
}).catch(err => {
    // 失败的回调
    console.log(err);
});
```

**发送 POST 请求：**

```JavaScript
let article = {
    title: '明天会更好',
    category: '生活',
    time: '2000-01-01',
    state: '草稿'
}

axios({
    method: 'post',
    url: 'http://localhost:8080/article/add',
    data: article
}).then(result => {
    console.log(result.data);
}).catch(err => {
    console.log(err);
});
```

### 请求别名

为了方便起见，Axios 为所有支持的请求方法提供了别名。

语法：axios.请求方式(url [, data [, config]])

```JavaScript
// 别名的方式发送请求
axios.get('http://localhost:8080/article/getAll').then(result => {
    console.log(result.data);
}).catch(err => {
    console.log(err);
});
```

---

## 6. Vue 综合案例 (局部模式)

**需求**：

1. 钩子函数 `mounted` 中，获取所有的文章数据。
    
2. 使用 `v-for` 指令，把数据渲染到表格上。
    
3. 使用 `v-model` 指令，完成表单数据的双向绑定。
    
4. 使用 `v-on` 指令为搜索按钮绑定单击事件。
    

**完整代码：**

```HTML
<body>
    <div id="app">
        文章分类: <input type="text" v-model="searchConditions.category">
        发布状态: <input type="text" v-model="searchConditions.state">
        <button v-on:click="search">搜索</button>
        <br /><br />
        
        <table border="1 solid" colspan="0" cellspacing="0">
            <tr>
                <th>文章标题</th>
                <th>分类</th>
                <th>发表时间</th>
                <th>状态</th>
                <th>操作</th>
            </tr>
            <tr v-for="(article, index) in articleList">
                <td>{{article.title}}</td>
                <td>{{article.category}}</td>
                <td>{{article.time}}</td>
                <td>{{article.state}}</td>
                <td>
                    <button>编辑</button>
                    <button>删除</button>
                </td>
            </tr>
        </table>
    </div>

    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    
    <script type="module">
        import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
        
        createApp({
            data() {
                return {
                    articleList: [],
                    searchConditions: {
                        category: '',
                        state: ''
                    }
                }
            },
            methods: {
                search: function() {
                    // 发送请求, 完成搜索, 携带搜索条件
                    axios.get('http://localhost:8080/article/search?category=' + this.searchConditions.category + '&state=' + this.searchConditions.state)
                        .then(result => {
                            this.articleList = result.data
                        }).catch(err => {
                            console.log(err);
                        });
                }
            },
            // 钩子函数 mounted 中, 获取所有文章数据
            mounted: function() {
                axios.get('http://localhost:8080/article/getAll').then(result => {
                    this.articleList = result.data;
                }).catch(err => {
                    console.log(err);
                });
            }
        }).mount('#app');
    </script>
</body>
```

---

## 7. 整站使用 Vue（Vue 工程化）

### 介绍

- **create-vue**：Vue 官方提供的最新脚手架工具，用于快速生成一个工程化的 Vue 项目。
    
- **功能**：统一的目录结构、本地部署、热部署、单元测试、集成打包。
    
- **依赖环境**：NodeJS (NPM: Node Package Manager)。
    

### 项目创建和启动

1. 创建项目
    
    执行以下命令，将会安装并执行 create-vue：
    
    ```    Bash
    npm init vue@latest
    ```
    
2. 安装依赖
    
    进入项目目录，执行命令安装当前项目的依赖（需要联网）：
    
    ```    Bash
    npm install
    ```
    
3. **启动项目**
    
    ```    Bash
    npm run dev
    ```
    
4. 访问项目
    
    打开浏览器访问 http://localhost:5173。
    

### 开发流程与 SFC

- **SFC (Single-File Component)**：Vue 的单文件组件，后缀为 `.vue`。
    
- 它将一个组件的逻辑 (**JS**)、模板 (**HTML**) 和样式 (**CSS**) 封装在同一个文件里。
    

### API 风格

Vue 组件有两种不同的风格：**选项式 API** 和 **组合式 API**。

1. **选项式 API**：使用包含多个选项的对象来描述组件的逻辑，如 `data`, `methods`, `mounted`。
    
2. **组合式 API (Recommended)**：
    
    - 在 `<script>` 上添加 `setup` 标识。
        
    - **ref()**：接收一个内部值，返回一个响应式的 ref 对象（通过 `.value` 访问）。
        
    - **onMounted()**：组合式 API 中的钩子方法。
        

**代码示例 (组合式 API)：**

```HTML
<script setup>
    import { ref, onMounted } from 'vue';
    
    // 调用 ref 函数, 定义响应式数据
    const msg = ref('西安');
    
    // 声明响应式数据，一般需要把数据定义为响应式数据
    const count = ref(0); 

    // 声明函数
    function increment() {
        count.value++;
    }

    // 声明钩子函数 onMounted
    onMounted(() => {
        console.log('vue 已经挂载完毕了...');
    });
    
    // 导入子组件
    import ApiVue from './Api.vue'
</script>
```

---

## 8. 工程化案例与 Axios 封装

### 案例需求

与局部模式类似：在 mounted 中获取数据、渲染表格、双向绑定表单、绑定搜索事件。

在工程化开发中，通常会提取 Article.vue，并将接口调用逻辑封装。

### Axios 拦截器

在请求或响应被 `then` 或 `catch` 处理前拦截它们。通常用于统一处理 token 或 错误提示。

**封装示例 (request.js)：**

```JavaScript

// 导入 axios
import axios from 'axios';

// 定义公共前缀 baseURL
const baseURL = 'http://localhost:8080';
const instance = axios.create({baseURL});

// 添加响应拦截器
instance.interceptors.response.use(
    result => {
        return result.data;
    },
    err => {
        alert('服务异常');
        return Promise.reject(err); // 异步的状态转化成失败的状态
    }
)

export default instance;
```

---

## 9. Element Plus

介绍：Element Plus 是饿了么团队研发的，基于 Vue 3，面向设计师和开发者的组件库。

组件：组成网页的部件，例如超链接、按钮、图片、表格、表单、分页条等。

### 准备工作

1. 创建一个工程化的 Vue 项目。
    
2. 参照官方文档，安装 Element Plus 组件库：
    
    ```    Bash
    npm install element-plus --save
    ```
    
3. 在 `main.js` 中引入 Element Plus 组件库（参照官方文档）。
    

### 常用组件

- Table (表格)
    
- Pagination (分页条)
    
- Form (表单)
    
- Card (卡片)
    

**参考文档**：[一个 Vue 3 UI 框架 | Element Plus](https://element-plus.org/zh-CN/)
# 实战篇-前端篇

> 接[[SpringBoot 3#^cc174a|大事件后端]]

## 1. 环境准备

### 初始化项目

- **创建 Vue 工程**：
    
    ```    Bash
    npm init vue@latest
    ```
    
- **安装依赖**：
    
    - Element-Plus：`npm install element-plus --save`
        
    - Axios：`npm install axios`
        
    - Sass：`npm install sass -D`
        

### 目录与文件调整

1. **目录调整**：删除 `components` 下面自动生成的内容。
    
2. **新建目录**：`api`, `utils`, `views`。
    
3. **静态资源**：将资料中的静态资源拷贝到 `assets` 目录下。
    
4. **App.vue**：删除 `App.vue` 中自动生成的内容。
    

---

## 2. 注册功能开发

### 开发步骤

1. **搭建页面**：HTML 标签 / CSS 样式。
    
2. **绑定数据与事件**：表单校验。
    
3. **调用后台接口**：接口文档 -> `src/api/xx.js` 封装 -> 页面函数中调用。
    

### 页面搭建与前端校验

使用 `el-form` 组件：

- `el-form` 标签通过 `rules` 属性绑定校验规则。
    
- `el-form-item` 标签通过 `prop` 属性指定校验项（对应 `rules` 中的键名）。
    

**代码示例 (Login.vue script 部分):**

```JavaScript
import { ref } from 'vue'

// 定义数据模型
const registerData = ref({
    username: '',
    password: '',
    rePassword: ''
})

// 定义确认密码的校验函数
const checkRePassword = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('请再次输入密码'));
    } else if (value !== registerData.value.password) {
        callback(new Error('两次输入密码不一致!'));
    } else {
        callback();
    }
}

// 定义表单校验规则
const rules = {
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 5, max: 16, message: '长度在 5 到 16 个非空字符', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 5, max: 16, message: '长度在 5 到 16 个非空字符', trigger: 'blur' }
    ],
    rePassword: [
        { validator: checkRePassword, trigger: 'blur' },
    ]
}
```

**代码示例 (Template 部分):**


```HTML
<el-form-item prop="username">
    <el-input :prefix-icon="User" placeholder="请输入用户名" v-model="registerData.username"></el-input>
</el-form-item>
<el-form-item>
     <el-button type="primary" @click="register">注册</el-button>
</el-form-item>
```

### 接口对接

> **说明**：`application/x-www-form-urlencoded` 是一种常见的数据编码格式，将表单数据编码为键值对（类似 URL 查询参数）。

**API 封装 (`src/api/user.js`):**

```JavaScript
// 导入 request.js 请求工具
import request from '@/utils/request.js'

// 提供调用注册接口的函数
export const userRegisterService = (registerData) => {
    // 借助于 URLSearchParams 对象来处理参数 (x-www-form-urlencoded)
    const params = new URLSearchParams();
    // 遍历对象的每一个属性
    for (let key in registerData) {
        params.append(key, registerData[key]);
    }
    return request.post('/user/register', params);
}
```

**页面逻辑 (`Login.vue`):**

```JavaScript
// 调用后台接口完成注册
import { userRegisterService } from '@/api/user.js'
import { ElMessage } from 'element-plus'

const register = async () => {
    // registerData 是一个响应式对象，如果要获取值，需要 .value
    let result = await userRegisterService(registerData.value);
    // 这里假设 request.js 已经处理了响应数据，如果没有统一拦截，需自行判断 result.code
    if (result.code === 0) {
        ElMessage.success(result.msg ? result.msg : '注册成功');
    } else {
        ElMessage.error('注册失败');
    }
}
```

### 跨域问题解决

由于浏览器的同源策略限制，向不同源（不同协议/不同域名/不同接口）发送 Ajax 请求会失败。

**配置代理 (`vite.config.js`):**

```JavaScript
export default defineConfig({
    server: {
        proxy: {
            '/api': {
                target: 'http://localhost:8080', // 后台服务器地址
                changeOrigin: true, // 是否更改请求头中的 Origin 字段
                rewrite: (path) => path.replace(/^\/api/, '') // 重写路径 将 /api 替换为空
            }
        }
    }
})
```

---

## 3. 登录功能开发

### 业务逻辑

1. 绑定数据（复用注册表单的数据模型）。
    
2. 表单数据校验。
    
3. 调用后台登录接口。
    

**API 封装 (`src/api/user.js`):**

```JavaScript
// 提供调用登录接口的函数
export const userLoginService = (loginData) => {
    const params = new URLSearchParams();
    for (let key in loginData) {
        params.append(key, loginData[key]);
    }
    return request.post('/user/login', params);
}
```

**页面逻辑 (`Login.vue`):**

```JavaScript
import { userLoginService } from '@/api/user.js'

// 登录函数
const login = async () => {
    let result = await userLoginService(registerData.value);
    if (result.code === 0) {
        ElMessage.success(result.msg ? result.msg : '登录成功');
        // 保存 token 等后续操作...
    } else {
        ElMessage.error('登录失败');
    }
}

// 定义函数，清空数据模型数据 (切换注册/登录时调用)
const clearRegisterData = () => {
    registerData.value.username = '';
    registerData.value.password = '';
    registerData.value.rePassword = '';
}
```

### 优化 Axios 响应拦截器

在 `src/utils/request.js` 中统一处理业务状态码和错误提示。

```JavaScript
import { ElMessage } from 'element-plus'
import axios from 'axios'
// ... 创建 instance ...

// 添加响应拦截器
instance.interceptors.response.use(
    result => {
        // 判断业务状态码
        if (result.data.code === 0) {
            return result.data;
        }
        // 操作失败
        ElMessage.error(result.data.msg ? result.data.msg : '服务异常');
        // 异步操作的状态转为失败
        return Promise.reject(result.data);
    },
    err => {
        ElMessage.error('服务异常');
        return Promise.reject(err); // 异步的状态转化成失败的状态
    }
)
```

---

## 4. 主页面搭建与路由

### 路由基础

- **Vue Router**: Vue 官方路由。
    
- **安装**: `npm install vue-router@4`
    

**配置路由 (`src/router/index.js`):**

```JavaScript
import { createRouter, createWebHistory } from 'vue-router'

// 导入组件
import LoginVue from '@/views/Login.vue'
import LayoutVue from '@/views/Layout.vue'

// 定义路由关系
const routes = [
    { path: '/login', component: LoginVue },
    { path: '/', component: LayoutVue }
]

// 创建路由器
const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

// 导出路由
export default router
```

**登录成功后跳转:**

```JavaScript
import { useRouter } from 'vue-router'
const router = useRouter();

const login = async () => {
    // ... 登录成功逻辑 ...
    router.push('/') // 路由完成跳转
}
```

### 二级路由 (子路由)

为菜单项 `el-menu-item` 设置 `index` 属性，设置点击后的路由路径。

**更新路由配置 (`src/router/index.js`):**

```JavaScript
import ArticleCategoryVue from '@/views/article/ArticleCategory.vue'
import ArticleManageVue from '@/views/article/ArticleManage.vue'
import UserAvatarVue from '@/views/user/UserAvatar.vue'
import UserInfoVue from '@/views/user/UserInfo.vue'
import UserResetPassword from "@/views/user/UserResetPassword.vue";

const routes = [
    { path: '/login', component: LoginVue },
    {
        path: '/',
        component: LayoutVue,
        redirect: '/article/manage', // 重定向
        children: [
            { path: '/article/category', component: ArticleCategoryVue },
            { path: '/article/manage', component: ArticleManageVue },
            { path: '/user/info', component: UserInfoVue },
            { path: '/user/avatar', component: UserAvatarVue },
            { path: '/user/resetPassword', component: UserResetPassword }
        ]
    }
]
```

---

## 5. 文章分类列表与 Pinia 状态管理

### Pinia 状态管理库

**背景**：登录后获取的 Token 需要在其他组件（如文章列表）的请求头中使用，Pinia 可实现跨组件共享状态。

1. **安装**: `npm install pinia`
    
2. **创建 Store (`src/stores/token.js`):**
    

```JavaScript
import { defineStore } from 'pinia'
import { ref } from "vue";

/* 第一个参数：名字，唯一性
  第二个参数：函数，函数的内部可以定义状态的所有内容
*/
export const useTokenStore = defineStore('token', () => {
    // 1. 定义响应式变量
    const token = ref('');

    // 2. 定义函数，修改 token
    const setToken = (newToken) => {
        token.value = newToken;
    }

    // 3. 定义函数，移除 token
    const removeToken = () => {
        token.value = '';
    }

    return {
        token,
        setToken,
        removeToken
    }
}, { persist: true }); // 持久化存储配置
```

3. **登录页存入 Token (`Login.vue`):**
    

```JavaScript
import { useTokenStore } from "@/stores/token.js";
const tokenStore = useTokenStore();

const login = async () => {
    let result = await userLoginService(registerData.value);
    // 将 token 存储到 pinia
    tokenStore.setToken(result.data); 
    router.push('/')
}
```

### Axios 请求拦截器 (统一注入 Token)

为了避免每次请求都手动设置 `Authorization`，配置请求拦截器。

**`src/utils/request.js`:**

```JavaScript
import { useTokenStore } from '@/stores/token.js'

// 添加请求拦截器
instance.interceptors.request.use(
    (config) => {
        // 请求前的回调
        const tokenStore = useTokenStore();
        // 如果有 token，添加到请求头
        if (tokenStore.token) {
            config.headers['Authorization'] = tokenStore.token;
        }
        return config;
    },
    (err) => {
        Promise.reject(err)
    }
)
```

### Pinia 持久化 (Persist)

Pinia 默认是内存存储，刷新会丢失。使用 `pinia-persistedstate-plugin` 插件。

1. **安装**: `npm install pinia-persistedstate-plugin`
    
2. **配置 (`main.js`):**
    

```JavaScript
import { createPinia } from 'pinia'
import { createPersistedState } from "pinia-persistedstate-plugin";

const pinia = createPinia()
const persist = createPersistedState();
pinia.use(persist);
app.use(pinia)
```

### 未登录统一处理 (401 拦截)

在响应拦截器中处理 401 状态码，跳转回登录页。

**`src/utils/request.js`:**

```JavaScript
import router from '@/router'

// ... interceptors.response.use ...
err => {
    // 判断响应状态码，如果为 401，跳转登录
    if (err.response.status === 401) {
        ElMessage.error("请先登录");
        router.push('/login');
    } else {
        ElMessage.error('服务异常');
    }
    return Promise.reject(err);
}
```

> Q: 为什么不用重定向，而是用路由跳转？
> 
> A: 重定向是路由配置中的静态规则（如访问 / 跳到 /home）。而未登录校验是运行时根据状态判断的，需要代码逻辑控制，所以使用 router.push。

---

## 6. 文章分类管理功能

### 文章分类列表

**API (`src/api/article.js`):**

```JavaScript
export const articleCategoryListService = () => {
    return request.get('/category')
}
```

**页面逻辑 (`ArticleCategory.vue`):**

```JavaScript
const categorys = ref([])
const articleCategoryList = async () => {
    let result = await articleCategoryListService();
    categorys.value = result.data;
}
articleCategoryList();
```

### 添加文章分类

**数据模型与校验:**

```JavaScript
const dialogVisible = ref(false)
const categoryModel = ref({
    categoryName: '',
    categoryAlias: ''
})
const rules = {
    categoryName: [{ required: true, message: '请输入分类名称', trigger: 'blur' }],
    categoryAlias: [{ required: true, message: '请输入分类别名', trigger: 'blur' }]
}
```

**添加逻辑:**

```JavaScript
const addCategory = async () => {
    let result = await articleCategoryAddService(categoryModel.value);
    ElMessage.success(result.msg ? result.msg : '添加成功');
    articleCategoryList(); // 刷新列表
    dialogVisible.value = false;
}
```

### 修改文章分类

通过 `title` 变量复用同一个弹窗。

**API (`src/api/article.js`):**

```JavaScript
export const articleCategoryUpdateService = (categoryData) => {
    return request.put('/category', categoryData);
}
```

**页面逻辑:**

```JavaScript
const title = ref('')

// 展示编辑弹窗
const showDialog = (row) => {
    dialogVisible.value = true;
    title.value = '编辑分类';
    // 数据拷贝
    categoryModel.value.categoryName = row.categoryName;
    categoryModel.value.categoryAlias = row.categoryAlias;
    // 扩展 id 属性，用于后台修改
    categoryModel.value.id = row.id;
}

// 按钮逻辑：根据 title 判断是添加还是修改
// <el-button type="primary" @click="title === '添加分类' ? addCategory() : updateCategory()">确认</el-button>
```

### 删除文章分类

使用 `ElMessageBox` 确认框。

```JavaScript
const deleteCategory = (row) => {
    ElMessageBox.confirm('你确认删除该分类信息吗？', '温馨提示', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(async () => {
        await articleCategoryDeleteService(row.id)
        ElMessage.success('删除成功')
        articleCategoryList();
    }).catch(() => {
        ElMessage.info('用户取消了删除')
    })
}
```

---

## 7. 文章列表与新增文章

### 文章列表查询

需要处理分页参数和数据转换（categoryId 转 categoryName）。

```JavaScript
const articleList = async () => {
    let params = {
        pageNum: pageNum.value,
        pageSize: pageSize.value,
        categoryId: categoryId.value ? categoryId.value : null,
        state: state.value ? state.value : null
    }
    let result = await articleListService(params);

    total.value = result.data.total;
    articles.value = result.data.items;

    // 前端映射分类名称 (如果后端未返回名称)
    for (let i = 0; i < articles.value.length; i++) {
        let article = articles.value[i];
        for (let j = 0; j < categorys.value.length; j++) {
            if (article.categoryId === categorys.value[j].id) {
                article.categoryName = categorys.value[j].categoryName;
            }
        }
    }
}
```

### 新增文章 (封面上传)

使用 `el-upload` 组件。

```HTML
<el-form-item label="文章封面">
    <el-upload 
        class="avatar-uploader" 
        :auto-upload="true" 
        :show-file-list="false"
        action="/api/upload"
        name="file"
        :headers="{'Authorization': tokenStore.token}"
        :on-success="uploadSuccess"
    >
        <img v-if="articleModel.coverImg" :src="articleModel.coverImg" class="avatar" />
        <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
    </el-upload>
</el-form-item>
```

发布逻辑:

调用 addArticle('已发布') 或 addArticle('草稿') 给状态赋值。

---

## 8. 用户信息管理

### 获取用户信息与 Store

**Store (`src/stores/userInfo.js`):**

```JavaScript
import { defineStore } from "pinia";
import { ref } from "vue";

const useUserInfoStore = defineStore('userInfo', () => {
    const info = ref({})
    const setInfo = (newInfo) => { info.value = newInfo }
    const removeInfo = () => { info.value = {} }
    return { info, setInfo, removeInfo }
}, { persist: true });

export default useUserInfoStore;
```

**获取信息逻辑:**

```JavaScript
const getUserInfo = async () => {
    let result = await userInfoService()
    userInfoStore.setInfo(result.data)
}
getUserInfo()
```

### 退出登录

在下拉菜单 (`el-dropdown`) 中处理 `@command` 事件。

```JavaScript
const handleCommand = (command) => {
    if (command === 'logout') {
        ElMessageBox.confirm('你确认要退出吗？', '温馨提示', { type: 'warning' })
            .then(async () => {
                // 1. 清除 Pinia 中的 token 和用户信息
                tokenStore.removeToken();
                userInfoStore.removeInfo();
                // 2. 跳转到登录页面
                router.push('/login')
                ElMessage.success('退出登录成功')
            })
    } else {
        // 路由跳转
        router.push('/user/' + command)
    }
}
```

### 基本资料修改

表单绑定 `userInfo` 数据，提交修改后更新 Store。

```JavaScript
const updateUserInfo = async () => {
    let result = await userInfoUpdateService(userInfo.value);
    ElMessage.success(result.msg ? result.msg : "修改成功");
    // 更新 store 中的用户信息
    userInfoStore.setInfo(userInfo.value);
}
```

### 用户头像修改

实现头像回显、图片上传、头像地址更新。

```JavaScript
// 图片上传成功的回调
const uploadSuccess = (result) => {
    imgUrl.value = result.data;
}

// 头像修改提交
const updateAvatar = async () => {
    let result = await userAvatarUpdateService(imgUrl.value);
    ElMessage.success(result.msg ? result.msg : "头像修改成功")
    // 修改 pinia 中的数据
    userInfoStore.info.userPic = imgUrl.value;
}
```

**CSS 样式 (使用 `:deep()` 穿透):**

```CSS
<style lang="scss" scoped>
.avatar-uploader {
    :deep() {
        .avatar {
            width: 278px;
            height: 278px;
            display: block;
        }
        .el-upload {
            border: 1px dashed var(--el-border-color);
            /* ...其他样式... */
        }
    }
}
</style>
```