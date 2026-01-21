css是一门语言，用于控制网页表现，Cacading Style Sheet：层叠样式表

# CSS导入方式

CSS导入HTML有三种方式：

1.  内联样式：在标签内部使用style属性，属性值是css属性键值对
2.  内部样式：定义`<style>`标签，在标签内部定义css样式
3.  外部样式：定义link标签，导入外部的css文件
```css
 <head>
     <meta charset="UTF-8">
     <title>Title</title>
     <style> --内部样式
         span{
             color: #ff0000;
         }
     </style>
     <link href="../css/demo.css" rel="stylesheet">--外部样式
 </head>
 <body>
     <div style="color: red">hello css</div>--内联样式
     <span>hello css </span>
     <p>hello css</p>
```
# CSS选择器

选择器是选取需设置的元素（标签）

1.  元素选择器
2.  Id选择器 --id要唯一
3.  类选择器 --可选择多个元素

\--谁选择的范围越小 谁就生效

```css
<head>
     <meta charset="UTF-8">
     <title>Title</title>
     <style>
         div{
             color: red;
         }
        #name{
            color: blue;
         }
         .cls{
             color: pink;
         }
     </style>
 </head>

 <body>
 <div>div1</div>
 <div id="name">div2</div
 <div class="cls">div3</di

<span class="cls">span</span>
```
