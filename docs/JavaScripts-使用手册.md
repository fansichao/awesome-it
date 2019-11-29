# JavaScrtipts使用手册.md

## 插件列表

数据隐藏

- [tootik](https://eliortabeka.github.io/tootik/)

## 常用命令


## 字符串

### 字符串替换

```javascript
// 将 str 中的 a 替换为 A
var str = 'abcabcabc';
var result = str.replace('a', 'A');
console.log('result:' + result);  

// 输出 result:Abcabcabc

// 将str 中所有的 a 替换为 A
var str = 'abcabcabc';
var result = str.replace(/a/g, 'A');
console.log('result:' + result); 
```

## 数组

### JS数组深拷贝

es6克隆一个新的数组的方法：

```javascript
const a1 = [1,2,3];
// 写法一：
const a2 = [...a1];
// 写法2 ：
const [...a2] = a1;
```

### JS数组对象去重

## 数值处理

### 保留指定位数小数

```javascript
var number = 1.23456789;
number = number.toFixed(4);
```

## 变量

### js 动态创建变量名

window['xxx'] 动态创建变量

```javascript
function create_variable(num){
    var name = "test_"+num;   //生成变量名
    window[name] = 100;
    window['name'] = 200;   //注意看中括号里的内容加引号和不加引号的区别
    }

    create_variable(2);
    alert(test_2);  // 100;
    alert(name); //200;
```


## 数据转换

JS数据类型列表

- 数组 Array(0,1,2,3,4)
- 字符串
- Json字符串
- 字典

本节主要描述常见数据格式相互转换的方法。

### 数组->字符串

数组转换为字符串

```js
// 需要将数组元素用某个字符连接成字符串
var a, b;
a = new Array(0,1,2,3,4);
b = a.join("-");      //"0-1-2-3-4"
```

### 字符串->数组

字符串转数组

```js
// 实现方法为将字符串按某个字符切割成若干个字符串，并以数组形式返回，示例代码如下：
var s = "abc,abcd,aaa";
ss = s.split(",");// 在每个逗号(,)处进行分解  ["abc", "abcd", "aaa"]
var s1 = "helloworld";
ss1 = s1.split('');  //["h", "e", "l", "l", "o", "w", "o", "r", "l", "d"]
```

### 对象->json字符串

对象转为字符串

```js
const obj = {
     id: 0,
     name: '张三',
     age: 12
}
const objToStr = JSON.stringify(obj)
console.log('obj:', obj)
console.log('objToStr:', objToStr)
```

### json字符串->对象

```js
// json字符串转为对象
const str = '{"id":0,"name":"张三","age":12}'
const strToObj = JSON.parse(str)
console.log('str:', str)
console.log('strToObj:', strToObj)
```

## 模块功能

### js自动点击onclick js自动触发onclick事件 定时延时执行

```javascript
<script type="text/javascript">
// 两秒后模拟点击
setTimeout(function() {
    // IE
    if(document.all) {
        document.getElementById("clickMe").click();
    }
    // 其它浏览器
    else {
        var e = document.createEvent("MouseEvents");
        e.initEvent("click", true, true);
        document.getElementById("clickMe").dispatchEvent(e);
    }
}, 2000);
</script>
  
<a href="http://www.sinmeng.net" id="clickMe" οnclick="alert('clicked');">触发onclick</a>
```

### 页面加载完毕后再执行函数

对于动态ID,存在ID未赋值,但是函数已执行，导致找不到ID的情况.

所以需要最后加载函数.

```javascript
<script type="text/javascript">
    // window.onload 页面加载完毕后再执行函数
    window.onload=function(){
        document.getElementById('btn1').onclick=function(){
            alert('helleo');
        };
    };
</script>
```

### 获取HTML附带的参数值

```javascript
// href ?var1=sss&var2=sss&var3=asdsd
var param = window.location.href.split('?');
var pwd = param.length>1? param[1]:'';
var pwd = param.length>1? param[1]:'';
pwd=pwd.replace('?','');
// 创建动态变量
for(dic_str of pwd.split('&')){
    window[dic_str.split('=')[0]]=dic_str.split('=')[1]
}
```

### JS删除div

```javascipt

// js js中的话要通过获取该元素的父级元素，再调用..removeChild(要删除的元素);
var removeObj = document.getElementById('reducedLine').getElementsByName('mlt24')[0];
removeObj.parentNode.removeChild(removeObj);

//jquery
$('#divID').remove();
```

### 模糊查询(模糊匹配)

https://www.cnblogs.com/sxxya/p/10911623.html
https://www.jianshu.com/p/4cd4f74a0b20  

前端开发工具箱
https://www.html.cn/tool/html2js/


[js给节点添加或删除类名](http://www.bubuko.com/infodetail-2698446.html)  



[html设置层DIV的显示和隐藏](https://www.cnblogs.com/zyb2014/p/3669731.html)

## 根据ID修改元素


var oneDom = document.getElementById("one");
oneDom.className = "我很好"
oneDom.className +=" "+"我很好";
