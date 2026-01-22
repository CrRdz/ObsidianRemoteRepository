- HTML（HyperText Markup Language）是一种语言，所有语言都是用HTML语言编写出来的
- 标记语言：由标签构成的语言
- HTML运行在浏览器上，HTML标签由浏览器来解析
- HTML标签都是预定义好的。例如：使用<img>展示图片
- W3C标准：网页主要由三部分组成
- 结构：HTML
- 表现：CSS
- 行为：JavaScript

# HTML快速入门

```html
  <html>
      <head>
          <title>hello html</title>
      </head>
      <body>
          <font color = "red">htmllllll</font>
      </body>
  </html>
```
效果：
  <html>
      <head>
          <title>hello html</title>
      </head>
      <body>
          <font color = "red">htmllllll</font>
      </body>
  </html>

HTML文件以.htm或.html为扩展名
HTML结构标签

- `<HTML>` 定义HTML文档
- `<head>` 定义关于文档的信息
- `<title>` 定义文档的标题
- `<body>` 定义文档的主题

1.  HTML标签不区分大小写
2.  HTML标签属性值 单双引皆可
3.  语法松散

# HTML标签

## 基础标签

`<h1>-<h6>` 定义标题，h1最大，h6最小
`<b>` 定义粗体文本
`<i>` 定义斜体文本 `<u>` 定义文本下划线
`<p>` 定义段落 `<center>` 定义文本居中
`<br>` 定义新行
`<hr>` 水平分割线

html表示颜色：

1.  英文单词：red,pink,blue..
2.  RGB表示（值1，值2，值3）取值范围0-255
3.  # 值1 # 值2 # 值3 ; 值的范围00~FF 十六进制表示

```html
 _<!-- html5 标识-->_
 <!DOCTYPE html>
 <html lang="en">
 <head>
     <!-- 页面的字符集-->
     <meta charset="UTF-8">
      <title>Title</title>
  </head>
  <body>
 <h1>我是标题 h1</h1>
 <h2>我是标题 h2</h2>
 <h3>我是标题 h3</h3>
 <h4>我是标题 h4</h4>
 <h5>我是标题 h5</h5>
 <h6>我是标题 h6</h6>
 <hr>
 <!--
     html 表示颜色：
         1. 英文单词：red,pink,blue...
         2. rgb(值1,值2,值3)：值的取值范围：0~255  rgb(255,0,0)
         3. #值1值2值3：值的范围：00~FF
-->
 <font face="楷体" size="5" color="#ff0000">hola</font>
 <hr>
 刚察草原绿草如茵，沙柳河水流淌入湖。藏族牧民索南才让家中，茶几上摆着馓子、麻花和水果，炉子上刚煮开的奶茶香气四溢……<br>
 6月8日下午，书记来到青海省海北藏族自治州刚察县沙柳河镇果洛藏贡麻村，走进牧民索南才让家中，看望慰问藏族群众。
 <hr>
 <p>
 刚察草原绿草如茵，沙柳河水流淌入湖。藏族牧民索南才让家中，茶几上摆着馓子、麻花和水果，炉子上刚煮开的奶茶香气四溢……
 </p>
 <p>6月8日下午，书记来到青海省海北藏族自治州刚察县沙柳河镇果洛藏贡麻村，走进牧民索南才让家中，看望慰问藏族群众。
 </p>
 <hr>
 沙柳河水流淌<br>
 
 <b>沙柳河水流淌</b><br>
 <i>沙柳河水流淌</i><br>
 <u>沙柳河水流淌</u><br>
 <hr>
 <center>
 <b>沙柳河水流淌</b>
 </center>
 </body>
 </html>
```
 
 效果：
<html lang="en">
 <head>
     _<!-- 页面的字符集-->_
     <meta charset="UTF-8">
      <title>Title</title>
  </head>
  <body>
 <h1>我是标题 h1</h1>
 <h2>我是标题 h2</h2>
 <h3>我是标题 h3</h3>
 <h4>我是标题 h4</h4>
 <h5>我是标题 h5</h5>
 <h6>我是标题 h6</h6>
 <hr>
 <!--_
     html 表示颜色：
         1. 英文单词：red,pink,blue...
         2. rgb(值1,值2,值3)：值的取值范围：0~255  rgb(255,0,0)
         3. #值1值2值3：值的范围：00~FF
 \-->
 <font face="楷体" size="5" color="#ff0000">hola</font>
 <hr>
 刚察草原绿草如茵，沙柳河水流淌入湖。藏族牧民索南才让家中，茶几上摆着馓子、麻花和水果，炉子上刚煮开的奶茶香气四溢……<br>
 6月8日下午，习近平总书记来到青海省海北藏族自治州刚察县沙柳河镇果洛藏贡麻村，走进牧民索南才让家中，看望慰问藏族群众。
 <hr>
 <p>
 刚察草原绿草如茵，沙柳河水流淌入湖。藏族牧民索南才让家中，茶几上摆着馓子、麻花和水果，炉子上刚煮开的奶茶香气四溢……
 </p>
 <p>6月8日下午，习近平总书记来到青海省海北藏族自治州刚察县沙柳河镇果洛藏贡麻村，走进牧民索南才让家中，看望慰问藏族群众。
 </p>
 <hr>
 沙柳河水流淌<br>
 
 <b>沙柳河水流淌</b><br>
 <i>沙柳河水流淌</i><br>
 <u>沙柳河水流淌</u><br>
 <hr>
 <center>
 <b>沙柳河水流淌</b>
 </center>
 </body>
 </html>
## 图片，音频，视频标签

<img> `<image>`定义图片
`<audio>` 定义音频
`<video>` 定义视频

1.  img：定义图片
	- Src: 规定显示图像的URL（统一资源定位符）
	- Height：定义图像的高度
	- Width：定义图像的宽度

```html
<img src="../img/a.jpg" width="300" height="400">
```
2.  audio：定义音频，支持的音频格式：MP3，WAV，OGG
	- Src：规定的音频的URL
	- Controls：显示播放控件

```html
<audio src="b.mp3" controls></audio>
```
2.  Video：定义视频，支持的视频格式：MP4,WebM,OGG
	- Src：规定视频的URL
	- Controls：显示播放控件

```html
<video src="c.mp4" controls width="500" height="300"></video>
```

注：资源路径：
1.  绝对路径：完整路径
2.  相对路径：相对位置关系

## 超链接标签

`<a>` 定义超链接
- Href：指定访问资源的URL
- Target：指定打开资源的方式
- \_self：默认值，在当前页面打开
- \_blank：在空白页面打开

```html
  <a href="https://www.itcast.cn" target="_blank">点我有惊喜</a>
```

## 列表标签

1.  有序列表（order list）
2.  无序列表（unorder list）

` <ol>`  定义有序列表
` <ul>`  定义无序列表
` <li>`  定义列表项

```html
  <ol type="A">
      <li>咖啡</li>
      <li>茶</li>
      <li>牛奶</li>
  </ol>
```

效果
  <ol type="A">
      <li>咖啡</li>
      <li>茶</li>
      <li>牛奶</li>
  </ol>

Type设置项目符号 不推荐使用

## 表格标签

`<table>` 定义有序列表
`<tr>` 定义行
`<td>` 定义单元格
`<th>` 定义表头单元格

1.  table：定义表格
	- Border：规定表格边框的宽度
	- Width：规定表格的宽度
	- Cellspacing：规定单元格之间的空白

2.  tr：定义行
	- Align：定义行的对齐方式

3.  td：定义单元格
	- rowspan：规定单元格可横跨的行数
	- colspan：规定单元格可横跨的列数

```html
 <table border="1" cellspacing="0" width="500">
     <tr>
        <th>序号</th>
         <th>品牌logo</th>
         <th>品牌名称</th>
         <th>企业名称</th>
     </tr>
     <tr align="center">
        <td>010</td>
         <td><img src="../img/三只松鼠.png" width="60" height="50"></td>
         <td>三只松鼠</td>
         <td>三只松鼠</td>
     </tr>
     <tr align="center">
         <td>009</td>
         <td><img src="../img/优衣库.png" width="60" height="50"></td>
         <td>优衣库</td>
         <td>优衣库</td>
     </tr>
     <tr align="center">
         <td>008</td>
         <td><img src="../img/小米.png" width="60" height="50"></td>
         <td>小米</td>
         <td>小米科技有限公司</td>
     </tr>
 </table>
```

对逐行进行编辑

## 布局标签

`<div>` 定义html文档中的一个区域部分，经常与CSS一起使用。用来布局网页
`<span>` 用来组合行内元素

## 表单标签

表单：在网页中主要负责数据采集功能，使用`<form>`标签定义表单

表单项（元素）：不同类型的input元素，下拉列表，文本域等

`<form>` 定义表单

`<input>` <input>定义表单项，通过type属性控制输入形式

`<label>` 为表单项定义标注

`<select>` 定义下拉列表

`<option>` 定义下拉列表的列表项

`<textarea>` 定义文本域

Form：定义表单

- action：规定当提交表单时向何处发送表单数据，URL
- method：规定用于发送表单数据的方式
- Get：浏览器会将数据附在表单的action URL之后，大小有限制
- Post：浏览器会将数据放到http请求协议的请求体中，大小无限制

```
    <form action="#" method="post/get">
          <input type="text" name="username">
          <input type="submit">
      </form>
```

type取值：

Text：默认值，定义单行的输入字段

Password：定义密码字段

Radio：定义单选按钮

Checkbox：定义复选框

File：定义文件上传按钮

Hidden：定义隐藏的输入字段

Submit：定义提交按钮，提交按钮会把表单数据发送到服务器

Reset：定义重置按钮，重置按钮会清除表单中的所有数据

Button：定义可点击按钮

```xml
 <form action="#" method="post">
     <input type="hidden" name="id" value="123">
     <label for="username">用户名：</label>
     <input type="text" name="username" id="username"><br>
     <label for="password">密码：</label>
     <input type="password" name="password" id="password"><br>
    性别：
    <input type="radio" name="gender" value="1" id="male"> <label for="male">男</label>
    <input type="radio" name="gender" value="2" id="female"> <label for="female">女</label>
     <br>
     爱好：
     <input type="checkbox" name="hobby" value="1"> 旅游
     <input type="checkbox" name="hobby" value="2"> 电影
     <input type="checkbox" name="hobby" value="3"> 游戏
     <br>
     头像：
     <input type="file"><br>
     城市:
     <select name="city">
         <option>北京</option>
         <option value="shanghai">上海</option>
         <option>广州</option>
     </select>
     <br>
     个人描述：
     <textarea cols="20" rows="5" name="desc"></textarea>
     <br>
     <br>
     <input type="submit" value="免费注册">
     <input type="reset" value="重置">
     <input type="button" value="一个按钮">
 </form>
```
