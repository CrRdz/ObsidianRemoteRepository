
- JavaScript 是一门跨平台、面向对象的脚本语言，用来控制网页行为，它能使网页可交付。
    
- JavaScript 和 Java 是完全不同的语言，不论是概念还是设计，但是基础语法类似。

# 1. JavaScript 引入方式

## 内部脚本

将 JS 代码定义在 HTML 页面中。

在 HTML 中，JavaScript 代码必须位于 <script> 与 </script> 标签之间。

> **注**：在 HTML 文档中可以在任意位置放置任意数量的 `<script>`。一般把脚本置于 `<body>` 元素的底部，可改善显示速度，不会因为脚本执行而拖慢显示。

```HTML
<script>
    alert("hello js1");
</script>
```

## 外部脚本

将 JS 代码定义在外部 JS 文件中，然后引入到 HTML 页面中。

```HTML
<script src="../js/demo.js"></script>
```

> **注**：外部脚本不能包含 `<script>` 标签，`<script>` 标签不能自闭合。

# 2. JavaScript 基础语法

## 书写语法

- **区分大小写**：与 Java 一样，变量名、函数名以及其他一切东西都是区分大小写的。
    
- **分号**：每行结尾的分号可有可无。
    
- **代码块**：大括号表示代码块。
    

## 输出语句

- `window.alert()`：写入警告框。
    
- `document.write()`：写入 HTML 输出。
    
- `console.log()`：写入浏览器控制台。
    

## 变量

- JavaScript 中用 `var` 关键字（variable 的缩写）来声明变量。
    
- **Var 作用域**：全局变量，变量可以重复定义。
    
- JavaScript 是一门弱类型语言，变量可以存放不同类型的值。
    
- **命名规则**：
    
    - 组成字符可以是任何字母、数字、下划线或美元符号。
        
    - 数字不能开头。
        
    - 建议使用驼峰命名。
        
- **ES6 新特性**：
    
    - `let`：用法类似于 `var`，但是声明的变量只在 `let` 关键字所在的代码块内有效，且不允许重复声明。
        
    - `const`：用来声明一个只读的常量。一旦声明，常量的值就不能改变。
        

## 数据类型

JavaScript 中分为：**原始类型** 和 **引用类型**。

**5 种原始类型：**

1. **Number**：数字（整数、小数、NaN）。
    
2. **String**：字符、字符串，单双引皆可。
    
3. **Boolean**：布尔，true/false。
    
4. **Null**：对象为空（特殊）。
    

    ```js
    var obj = null;
    alert(typeof obj); // object
    ```
    
5. **Undefined**：当声明的变量未初始化时，该变量的默认值是 undefined。
    

使用 `typeof` 运算符可以获取数据类型。

## 运算符

同 Java。

**`===` 与 `==` 的区别：**

- `==`：判断类型是否一样，如果不一样，则进行类型转换，再去比较其值。
    
- `===`：判断类型是否一样，如果不一样，则直接返回 false。
    

**其他类型转为 Number：**

- **String**: 按照字符串的字面值转为数字。如果字面值不是数字，则转为 NaN。一般使用 `parseInt` 或者在字符串前使用一个 `+`。
    
    JavaScript
    
    ```js
    var str = "20";
    alert(parseInt(str) + 1);
    ```
    
- **Boolean**: true 转为 1，false 转为 0。
    

**其他类型转为 Boolean：**

1. **Number**: `0` 和 `NaN` 转为 false，其他的数字转为 true。
    
2. **String**: 空字符串 `""` 转为 false，其他的字符串转为 true。
    
3. **Null**: false。
    
4. **Undefined**: false。
    

## 流程控制语句

同 Java 语言：`if`, `switch`, `for`, `while`, `do...while`。

## 函数

函数是被设计为执行特定任务的代码块。JavaScript 函数通过 `function` 关键词进行定义。

**定义方式一：**

JavaScript

```js
function functionName(参数1, 参数2){
    // 要执行的代码
}
```

- 形式参数不需要类型，因为 JavaScript 是弱类型语言。
    
- 返回值也不需要定义类型，可以在函数内部直接使用 `return` 返回即可。
    

**调用：** `函数名称(实际参数列表)`

```JavaScript
function add(a, b){
    return a + b;
}
var result = add(1, 2);
alert(result);
```

**定义方式二：**

```JavaScript
var functionName = function(参数列表){
    // 要执行的代码
}

var add = function(a, b){
    return a + b;
}
```

> **注**：JS 中，函数调用可以传递任意个数参数，函数只接收需要数量的参数。

# 3. JavaScript 对象

## Array (数组)

JS Array 对象用于定义数组。

**定义：**

```JavaScript
var arr1 = new Array(元素列表); // 方式一
var arr2 = [元素列表]; // 方式二
```

**访问：**

```js
arr[索引] = 值;
```

索引从 0 开始。JavaScript 数组**变长、变类型**。

**属性与方法：**

- `length`：数组长度。
    
- `push()`：添加元素。
    
    ```js
    var arr5 = [1, 2, 3];
    arr5.push(10);
    alert(arr5); // 输出 1, 2, 3, 10
    ```
    
- `splice()`：删除元素。
    
    ```js
    arr5.splice(0, 1); // 从索引0开始删除1个元素
    alert(arr5); // 输出 2, 3, 10
    ```
    

## String (字符串)

**定义：**

```js
var str1 = new String("s"); // 方式一
var str2 = "s"; // 方式二
```

**属性与方法：**

- `length`：字符串长度。
    
- `charAt()`：返回指定索引出的字符。
    
- `indexOf()`：检索字符串。
    
- `trim()`：去除字符串前后两端的空白字符。
    

## 自定义对象

```js
var 对象名称 = {
    属性名称: 属性值1,
    属性名称: 属性值2,
    // ...
    函数名称: function(形参列表){}
    // ...
};
```

# 4. BOM (浏览器对象模型)

BOM (Browser Object Model) 将浏览器的各个组成部分封装为对象。

**组成：**

- **Window**：浏览器窗口对象。
    
- **Navigator**：浏览器对象。
    
- **Screen**：屏幕对象。
    
- **History**：历史记录对象。
    
- **Location**：地址栏对象。
    

## Window 对象

获取：直接使用 `window`，其中 `window.` 可省略。

**属性（获取其他 BOM 对象）：**

- `history`：对 History 对象的只读引用。
    
    - `back()`：加载 history 列表中前一个 URL。
        
    - `forward()`：加载 history 列表中的下一个 URL。
        
- `navigator`：对 Navigator 对象的只读引用。
    
- `screen`：对 Screen 对象的只读引用。
    
- `location`：用于窗口或框架的 Location 对象。
    
    - `href`：设置或返回完整的 URL。
        
    - 示例：3秒跳转到首页
        
        ```js
        document.write("3秒跳转到首页...");
        setTimeout(function(){
            location.href = "https://www.baidu.com"
        }, 3000);
        ```
        

**方法：**

- `alert()`：显示一段消息和一个确认按钮的警告框。
    
- `confirm()`：显示带有一段消息以及确认按钮和取消按钮的对话框。
    
    ```js
    // 点击确定按钮返回true，点击取消按钮返回false
    var flag = confirm("确认删除？");
    if(flag){
        // 删除逻辑
    }
    ```
    
- `setInterval()`：按照指定的周期（以毫秒计）来调用函数或计算表达式（循环执行）。
    
- `setTimeout()`：在指定的毫秒数后调用函数或计算表达式（只执行一次）。
    

**定时器示例：**

```js
setTimeout(function(){
    alert("hehe");
}, 3000); // 3秒后执行一次

setInterval(function(){
    alert("hehe");
}, 2000); // 每2秒执行一次
```

**案例：交替开关灯**

```HTML
<body>
    <input type="button" onclick="on()" value="开灯">
    <img id="myImage" border="0" src="../imgs/off.gif" style="text-align:center;">
    <input type="button" onclick="off()" value="关灯">

    <script>
        function on(){
            document.getElementById('myImage').src='../imgs/on.gif';
        }

        function off(){
            document.getElementById('myImage').src='../imgs/off.gif'
        }
        
        var x = 0;
        // 根据一个变化的数字，产生固定个数的值； 2  x % 2     3   x % 3
        // 定时器
        setInterval(function (){
            if(x % 2 == 0){
                on();
            } else {
                off();
            }
            x++;
        }, 1000);
    </script>
</body>
```

# 5. DOM (文档对象模型)

^e157a0

DOM (Document Object Model) 定义了访问 HTML 和 XML 文档的标准，将标记语言的各个组成部分封装为对象。

**组成：**

- **Document**：整个文档对象。
    
- **Element**：元素对象。
    
- **Attribute**：属性对象。
    
- **Text**：文本对象。
    
- **Comment**：注释对象。
    

## 获取 Element 对象

使用 Document 对象的方法来获取：

```HTML
<img id="light" src="../imgs/off.gif"> <br>
<div class="cls">传智教育</div>   <br>
<div class="cls">黑马程序员</div> <br>
<input type="checkbox" name="hobby"> 电影
<input type="checkbox" name="hobby"> 旅游
<input type="checkbox" name="hobby"> 游戏
```

1. **getElementById**：根据 id 属性值获取，返回一个 Element 对象。
    
    ```    JavaScript
    var img = document.getElementById("light");
    alert(img);
    ```
    
2. **getElementsByTagName**：根据标签名称获取，返回 Element 对象数组。

    ```JavaScript
    var divs = document.getElementsByTagName("div");
    for (let i = 0; i < divs.length; i++) {
        alert(divs[i]);
    }
    ```
    
3. **getElementsByName**：根据 name 属性值获取，返回 Element 对象数组。

    ```JavaScript
    var hobbys = document.getElementsByName("hobby");
    for (let i = 0; i < hobbys.length; i++) {
        alert(hobbys[i]);
    }
    ```
    
4. **getElementsByClassName**：根据 class 属性值获取，返回 Element 对象数组。
    
    ```    JavaScript
    var clss = document.getElementsByClassName("cls");
    for (let i = 0; i < clss.length; i++) {
        alert(clss[i]);
    }
    ```
    

## 常见 HTML Element 对象的使用

- `<img>`: `src` 改变图片属性。
    
- `<div>`: `style` 设置元素 css 样式；`innerHTML` 设置元素内容。
    
- `<checkbox>`: `checked` 设置或返回 checkbox 是否被选中（true--被选中）。
    

# 6. 事件监听

事件：HTML 事件是发生在 HTML 元素上的事情。比如：按钮被点击、鼠标移动到元素之上、按下键盘按键。

事件监听：JavaScript 可以在事件被侦测到时执行代码。

## 事件绑定

**方式一：通过 HTML 标签中的属性进行绑定**

```HTML
<input type="button" value="点我" onclick="on()">
<script>
    function on(){
        alert("我被点了");
    }
</script>
```

**方式二：通过 DOM 元素属性绑定**

```HTML
<input type="button" value="再点我" id="btn">
<script>
    document.getElementById("btn").onclick = function (){
        alert("我被点了");
    }
</script>
```

## 常见事件

| **事件**        | **描述**       |
| ------------- | ------------ |
| `onclick`     | 鼠标单击事件       |
| `onblur`      | 元素失去焦点       |
| `onfocus`     | 元素获得焦点       |
| `onload`      | 某个页面或图像被完成加载 |
| `onsubmit`    | 当表单提交时触发该事件  |
| `onkeydown`   | 某个键盘的键被按下    |
| `onmouseover` | 鼠标被移到某元素之上   |
| `onmouseout`  | 鼠标从某元素移开     |

**表单提交事件示例：**

```HTML
<form id="register" action="#" >
    <input type="text" name="username" />
    <input type="submit" value="提交">
</form>

<script>
    document.getElementById("register").onsubmit = function (){
        // onsubmit 返回true，则表单会被提交，返回false，则表单不提交
        return true;
    }
</script>
```

## 案例：表单验证逻辑

1. 当输入框失去焦点时 (`onblur`)，验证输入内容是否符合要求。
    
2. 获取表单输入：`document.getElementById("username")`。
    
3. 获取输入内容：`usernameInput.value.trim()`。
    
4. 判断是否符合规则（使用正则表达式）。
    
5. 如果不符合规则，则显示错误提示信息。
    
6. 当点击注册按钮时 (`onsubmit`)，判断所有输入框的内容是否都符合要求，如果不符合则阻止表单提交。
    

# 7. 正则表达式

正则表达式定义了字符串组成的规则。

**定义：**

1. **直接量**（注意不要加引号）：
    
    ```    JavaScript
    var reg = /^\w{6,12}$/;
    ```
    
1. **创建 RegExp 对象**：
    
    ```    JavaScript
    var reg = new RegExp("^\\w{6,12}$");
    ```
    

**方法：**

- `test(str)`：判断指定字符串是否符合规则，返回 true 或 false。
    

**语法符号：**

- `^`：表示开始。
    
- `$`：表示结束。
    
- `[]`：代表某个范围内的单个字符，比如 `[0-9]` 单个数字字符。
    
- `.`：代表任意单个字符，除了换行和结束符。
    
- `\w`：代表单词字符：字母、数字、下划线 `_`。
    
- `\d`：代表数字字符，相当于 `[0-9]`。
    

**量词：**

- `+`：至少一个。
    
- `*`：两个或多个（原文如此，通常 `*` 代表零个或多个，但此处按原文整理）。
    
- `?`：零个或一个。
    
- `{x}`：x 个。
    
- `{m,}`：至少 m 个。
    
- `{m,n}`：至少 m 个，至多 n 个。
    

**示例：**

```JavaScript
// 判断手机号是否符合规则：长度 11，数字组成，第一位是1
var reg = /^[1]\d{10}$/;
```

---

# APPENDIX: 表单验证完整案例

```HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>欢迎注册</title>
    <link href="../css/register.css" rel="stylesheet">
</head>
<body>

<div class="form-div">
    <div class="reg-content">
        <h1>欢迎注册</h1>
        <span>已有账号？</span> <a href="#">登录</a>
    </div>
    <form id="reg-form" action="#" method="get">
        <table>
            <tr>
                <td>用户名</td>
                <td class="inputs">
                    <input name="username" type="text" id="username">
                    <br>
                    <span id="username_err" class="err_msg" style="display: none">用户名不太受欢迎</span>
                </td>
            </tr>
            <tr>
                <td>密码</td>
                <td class="inputs">
                    <input name="password" type="password" id="password">
                    <br>
                    <span id="password_err" class="err_msg" style="display: none">密码格式有误</span>
                </td>
            </tr>
            <tr>
                <td>手机号</td>
                <td class="inputs"><input name="tel" type="text" id="tel">
                    <br>
                    <span id="tel_err" class="err_msg" style="display: none">手机号格式有误</span>
                </td>
            </tr>
        </table>
        <div class="buttons">
            <input value="注 册" type="submit" id="reg_btn">
        </div>
        <br class="clear">
    </form>
</div>

<script>
    //1. 验证用户名是否符合规则
    //1.1 获取用户名的输入框
    var usernameInput = document.getElementById("username");

    //1.2 绑定onblur事件 失去焦点
    usernameInput.onblur = checkUsername;

    function checkUsername() {
        //1.3 获取用户输入的用户名
        var username = usernameInput.value.trim();

        //1.4 判断用户名是否符合规则：长度 6~12,单词字符组成
        var reg = /^\w{6,12}$/;
        var flag = reg.test(username);

        //var flag = username.length >= 6 && username.length <= 12;
        if (flag) {
            //符合规则
            document.getElementById("username_err").style.display = 'none';
        } else {
            //不符合规则
            document.getElementById("username_err").style.display = '';//设置css的style文件
        }

        return flag;
    }

    //1. 验证密码是否符合规则
    //1.1 获取密码的输入框
    var passwordInput = document.getElementById("password");

    //1.2 绑定onblur事件 失去焦点
    passwordInput.onblur = checkPassword;

    function checkPassword() {
        //1.3 获取用户输入的密码
        var password = passwordInput.value.trim();

        //1.4 判断密码是否符合规则：长度 6~12
        var reg = /^\w{6,12}$/;
        var flag = reg.test(password);

        //var flag = password.length >= 6 && password.length <= 12;
        if (flag) {
            //符合规则
            document.getElementById("password_err").style.display = 'none';
        } else {
            //不符合规则
            document.getElementById("password_err").style.display = '';
        }

        return flag;
    }

    //1. 验证手机号是否符合规则
    //1.1 获取手机号的输入框
    var telInput = document.getElementById("tel");

    //1.2 绑定onblur事件 失去焦点
    telInput.onblur = checkTel;

    function checkTel() {
        //1.3 获取用户输入的手机号
        var tel = telInput.value.trim();

        //1.4 判断手机号是否符合规则：长度 11，数字组成，第一位是1
        //var flag = tel.length == 11;
        var reg = /^[1]\d{10}$/;
        var flag = reg.test(tel);
        if (flag) {
            //符合规则
            document.getElementById("tel_err").style.display = 'none';
        } else {
            //不符合规则
            document.getElementById("tel_err").style.display = '';
        }

        return flag;
    }

    //1. 获取表单对象
    var regForm = document.getElementById("reg-form");

    //2. 绑定onsubmit 事件
    regForm.onsubmit = function () {
        //挨个判断每一个表单项是否都符合要求，如果有一个不符合，则返回false
        var flag = checkUsername() && checkPassword() && checkTel();
        return flag;
    }
</script>
</body>
</html>
```