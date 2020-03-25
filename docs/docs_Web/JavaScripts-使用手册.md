# JavaScrtipts 使用手册.md

## 插件列表

数据隐藏

- [tootik](https://eliortabeka.github.io/tootik/)

## 数据转换

JS 数据类型列表

- 数组 Array(0,1,2,3,4)
- 字符串
- Json 字符串
- 字典

本节主要描述常见数据格式相互转换的方法。

### 数组->字符串

数组转换为字符串

```js
// 需要将数组元素用某个字符连接成字符串
var a, b;
a = new Array(0, 1, 2, 3, 4);
b = a.join("-"); //"0-1-2-3-4"
```

### 字符串->数组

字符串转数组

```js
// 实现方法为将字符串按某个字符切割成若干个字符串，并以数组形式返回，示例代码如下：
var s = "abc,abcd,aaa";
ss = s.split(","); // 在每个逗号(,)处进行分解  ["abc", "abcd", "aaa"]
var s1 = "helloworld";
ss1 = s1.split(""); //["h", "e", "l", "l", "o", "w", "o", "r", "l", "d"]
```

### 对象->json 字符串

对象转为字符串

```js
const obj = {
  id: 0,
  name: "张三",
  age: 12
};
const objToStr = JSON.stringify(obj);
console.log("obj:", obj);
console.log("objToStr:", objToStr);
```

### json 字符串->对象

```js
// json字符串转为对象
const str = '{"id":0,"name":"张三","age":12}';
const strToObj = JSON.parse(str);
console.log("str:", str);
console.log("strToObj:", strToObj);
```

## 常用模块函数

### JS 判断对象是否相等

**说明:**

- 检查对象"值相等"是一个强大复杂的方法
- 需要依赖完善的测试库,包含各种边界类型情况.
- Underscore 和 Lo-Dash 有一个名为\_.isEqual()方法，用来比较好的处理深度对象的比较
- 参考链接: [Github-underscore](https://github.com/lessfish/underscore-analysis/blob/master/underscore-1.8.3.js/src/underscore-1.8.3.js#L1094-L1190)

**样例展示:**

```javascript
_.isEqual({'a':1},{'a':2})
false
_.isEqual({'a':1},{'a':2,'b':undefined})
false
_.isEqual({'a':1},{'a':1,'b':undefined})
false
```

### JS 数据类型转换

**功能说明:**

- 实现所有类型相互转换。小数、整数。字符串、数组、字典、布尔、json 等
- 实现类型 强转/非强转

TODO 待寻找组件

### JS 数组去重

**功能说明:**

- 支持数组去重
- 支持不同内部数组，例如数组中含字符串、字典、数组等等

```javascript
// 数组去重样例 - 利用hasOwnProperty
function unique(arr) {
    var obj = {};
    return arr.filter(function(item, index, arr){
        return obj.hasOwnProperty(typeof item + item) ? false : (obj[typeof item + item] = true)
    })
}

unique([1,2,3,1,{'a':1},{'a':1}])
[1, 2, 3, {'a':1}]
```

**参考资源:**

- 参考链接: [JavaScript数组去重(12种方法，史上最全)](https://segmentfault.com/a/1190000016418021)
- 本文附录: [JS去重方法大全](###附录1-JS去重方法大全)

## 其他函数

### 自动点击

js 自动点击 onclick js 自动触发 onclick 事件 定时延时执行

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

对于动态 ID,存在 ID 未赋值,但是函数已执行，导致找不到 ID 的情况.

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

### 获取 HTML 附带的参数值

```javascript
// href ?var1=sss&var2=sss&var3=asdsd
var param = window.location.href.split("?");
var pwd = param.length > 1 ? param[1] : "";
var pwd = param.length > 1 ? param[1] : "";
pwd = pwd.replace("?", "");
// 创建动态变量
for (dic_str of pwd.split("&")) {
  window[dic_str.split("=")[0]] = dic_str.split("=")[1];
}
```

### 删除 div

```javascript

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

[js 给节点添加或删除类名](http://www.bubuko.com/infodetail-2698446.html)

[html 设置层 DIV 的显示和隐藏](https://www.cnblogs.com/zyb2014/p/3669731.html)

### 根据 ID 修改元素

var oneDom = document.getElementById("one");
oneDom.className = "我很好"
oneDom.className +=" "+"我很好";

JavaScript 字符串转换成数字的三种方法

### js 动态创建变量名

window['xxx'] 动态创建变量

```javascript
function create_variable(num) {
  var name = "test_" + num; //生成变量名
  window[name] = 100;
  window["name"] = 200; //注意看中括号里的内容加引号和不加引号的区别
}

create_variable(2);
alert(test_2); // 100;
alert(name); //200;
```

### 保留指定位数小数

```javascript
var number = 1.23456789;
number = number.toFixed(4);
```

### JS 数组深拷贝

es6 克隆一个新的数组的方法：

```javascript
const a1 = [1, 2, 3];
// 写法一：
const a2 = [...a1];
// 写法2 ：
const [...a2] = a1;
```

### 字符串替换

```javascript
// 将 str 中的 a 替换为 A
var str = "abcabcabc";
var result = str.replace("a", "A");
console.log("result:" + result);

// 输出 result:Abcabcabc

// 将str 中所有的 a 替换为 A
var str = "abcabcabc";
var result = str.replace(/a/g, "A");
console.log("result:" + result);
```

## 附录

### 附录1-JS去重方法大全

```javascript
数组去重，一般都是在面试的时候才会碰到，一般是要求手写数组去重方法的代码。如果是被提问到，数组去重的方法有哪些？你能答出其中的10种，面试官很有可能对你刮目相看。
在真实的项目中碰到的数组去重，一般都是后台去处理，很少让前端处理数组去重。虽然日常项目用到的概率比较低，但还是需要了解一下，以防面试的时候可能回被问到。

注：写的匆忙，加上这几天有点忙，还没有非常认真核对过，不过思路是没有问题，可能一些小细节出错而已。

数组去重的方法
一、利用ES6 Set去重（ES6中最常用）
function unique (arr) {
  return Array.from(new Set(arr))
}
var arr = [1,1,'true','true',true,true,15,15,false,false, undefined,undefined, null,null, NaN, NaN,'NaN', 0, 0, 'a', 'a',{},{}];
console.log(unique(arr))
 //[1, "true", true, 15, false, undefined, null, NaN, "NaN", 0, "a", {}, {}]
不考虑兼容性，这种去重的方法代码最少。这种方法还无法去掉“{}”空对象，后面的高阶方法会添加去掉重复“{}”的方法。

二、利用for嵌套for，然后splice去重（ES5中最常用）
function unique(arr){            
        for(var i=0; i<arr.length; i++){
            for(var j=i+1; j<arr.length; j++){
                if(arr[i]==arr[j]){         //第一个等同于第二个，splice方法删除第二个
                    arr.splice(j,1);
                    j--;
                }
            }
        }
return arr;
}
var arr = [1,1,'true','true',true,true,15,15,false,false, undefined,undefined, null,null, NaN, NaN,'NaN', 0, 0, 'a', 'a',{},{}];
    console.log(unique(arr))
    //[1, "true", 15, false, undefined, NaN, NaN, "NaN", "a", {…}, {…}]     //NaN和{}没有去重，两个null直接消失了
双层循环，外层循环元素，内层循环时比较值。值相同时，则删去这个值。
想快速学习更多常用的ES6语法，可以看我之前的文章《学习ES6笔记──工作中常用到的ES6语法》。

三、利用indexOf去重
function unique(arr) {
    if (!Array.isArray(arr)) {
        console.log('type error!')
        return
    }
    var array = [];
    for (var i = 0; i < arr.length; i++) {
        if (array.indexOf(arr[i]) === -1) {
            array.push(arr[i])
        }
    }
    return array;
}
var arr = [1,1,'true','true',true,true,15,15,false,false, undefined,undefined, null,null, NaN, NaN,'NaN', 0, 0, 'a', 'a',{},{}];
console.log(unique(arr))
   // [1, "true", true, 15, false, undefined, null, NaN, NaN, "NaN", 0, "a", {…}, {…}]  //NaN、{}没有去重
新建一个空的结果数组，for 循环原数组，判断结果数组是否存在当前元素，如果有相同的值则跳过，不相同则push进数组。

四、利用sort()
function unique(arr) {
    if (!Array.isArray(arr)) {
        console.log('type error!')
        return;
    }
    arr = arr.sort()
    var arrry= [arr[0]];
    for (var i = 1; i < arr.length; i++) {
        if (arr[i] !== arr[i-1]) {
            arrry.push(arr[i]);
        }
    }
    return arrry;
}
     var arr = [1,1,'true','true',true,true,15,15,false,false, undefined,undefined, null,null, NaN, NaN,'NaN', 0, 0, 'a', 'a',{},{}];
        console.log(unique(arr))
// [0, 1, 15, "NaN", NaN, NaN, {…}, {…}, "a", false, null, true, "true", undefined]      //NaN、{}没有去重
利用sort()排序方法，然后根据排序后的结果进行遍历及相邻元素比对。

五、利用对象的属性不能相同的特点进行去重（这种数组去重的方法有问题，不建议用，有待改进）
function unique(arr) {
    if (!Array.isArray(arr)) {
        console.log('type error!')
        return
    }
    var arrry= [];
     var  obj = {};
    for (var i = 0; i < arr.length; i++) {
        if (!obj[arr[i]]) {
            arrry.push(arr[i])
            obj[arr[i]] = 1
        } else {
            obj[arr[i]]++
        }
    }
    return arrry;
}
    var arr = [1,1,'true','true',true,true,15,15,false,false, undefined,undefined, null,null, NaN, NaN,'NaN', 0, 0, 'a', 'a',{},{}];
        console.log(unique(arr))
//[1, "true", 15, false, undefined, null, NaN, 0, "a", {…}]    //两个true直接去掉了，NaN和{}去重
六、利用includes
function unique(arr) {
    if (!Array.isArray(arr)) {
        console.log('type error!')
        return
    }
    var array =[];
    for(var i = 0; i < arr.length; i++) {
            if( !array.includes( arr[i]) ) {//includes 检测数组是否有某个值
                    array.push(arr[i]);
              }
    }
    return array
}
var arr = [1,1,'true','true',true,true,15,15,false,false, undefined,undefined, null,null, NaN, NaN,'NaN', 0, 0, 'a', 'a',{},{}];
    console.log(unique(arr))
    //[1, "true", true, 15, false, undefined, null, NaN, "NaN", 0, "a", {…}, {…}]     //{}没有去重
七、利用hasOwnProperty
function unique(arr) {
    var obj = {};
    return arr.filter(function(item, index, arr){
        return obj.hasOwnProperty(typeof item + item) ? false : (obj[typeof item + item] = true)
    })
}
    var arr = [1,1,'true','true',true,true,15,15,false,false, undefined,undefined, null,null, NaN, NaN,'NaN', 0, 0, 'a', 'a',{},{}];
        console.log(unique(arr))
//[1, "true", true, 15, false, undefined, null, NaN, "NaN", 0, "a", {…}]   //所有的都去重了
利用hasOwnProperty 判断是否存在对象属性

八、利用filter
function unique(arr) {
  return arr.filter(function(item, index, arr) {
    //当前元素，在原始数组中的第一个索引==当前索引值，否则返回当前元素
    return arr.indexOf(item, 0) === index;
  });
}
    var arr = [1,1,'true','true',true,true,15,15,false,false, undefined,undefined, null,null, NaN, NaN,'NaN', 0, 0, 'a', 'a',{},{}];
        console.log(unique(arr))
//[1, "true", true, 15, false, undefined, null, "NaN", 0, "a", {…}, {…}]
九、利用递归去重
function unique(arr) {
        var array= arr;
        var len = array.length;

    array.sort(function(a,b){   //排序后更加方便去重
        return a - b;
    })

    function loop(index){
        if(index >= 1){
            if(array[index] === array[index-1]){
                array.splice(index,1);
            }
            loop(index - 1);    //递归loop，然后数组去重
        }
    }
    loop(len-1);
    return array;
}
 var arr = [1,1,'true','true',true,true,15,15,false,false, undefined,undefined, null,null, NaN, NaN,'NaN', 0, 0, 'a', 'a',{},{}];
console.log(unique(arr))
//[1, "a", "true", true, 15, false, 1, {…}, null, NaN, NaN, "NaN", 0, "a", {…}, undefined]
十、利用Map数据结构去重
function arrayNonRepeatfy(arr) {
  let map = new Map();
  let array = new Array();  // 数组用于返回结果
  for (let i = 0; i < arr.length; i++) {
    if(map .has(arr[i])) {  // 如果有该key值
      map .set(arr[i], true); 
    } else { 
      map .set(arr[i], false);   // 如果没有该key值
      array .push(arr[i]);
    }
  } 
  return array ;
}
 var arr = [1,1,'true','true',true,true,15,15,false,false, undefined,undefined, null,null, NaN, NaN,'NaN', 0, 0, 'a', 'a',{},{}];
    console.log(unique(arr))
//[1, "a", "true", true, 15, false, 1, {…}, null, NaN, NaN, "NaN", 0, "a", {…}, undefined]
创建一个空Map数据结构，遍历需要去重的数组，把数组的每一个元素作为key存到Map中。由于Map中不会出现相同的key值，所以最终得到的就是去重后的结果。

十一、利用reduce+includes
function unique(arr){
    return arr.reduce((prev,cur) => prev.includes(cur) ? prev : [...prev,cur],[]);
}
var arr = [1,1,'true','true',true,true,15,15,false,false, undefined,undefined, null,null, NaN, NaN,'NaN', 0, 0, 'a', 'a',{},{}];
console.log(unique(arr));
// [1, "true", true, 15, false, undefined, null, NaN, "NaN", 0, "a", {…}, {…}]
十二、[...new Set(arr)]
[...new Set(arr)] 
//代码就是这么少----（其实，严格来说并不算是一种，相对于第一种方法来说只是简化了代码）
PS：有些文章提到了foreach+indexOf数组去重的方法，个人觉得都是大同小异，所以没有写上去。

```