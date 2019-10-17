# JavaScrtipts使用手册.md






## 插件列表

数据隐藏
tootik https://eliortabeka.github.io/tootik/




# 常用命令

## 数据转换

**JS数据类型列表**
- 数组 Array(0,1,2,3,4)
- 字符串 
- Json字符串 
- 字典

本节主要描述常见数据格式相互转换的方法。

### 数组->字符串

**数组转换为字符串**
```js
// 需要将数组元素用某个字符连接成字符串
var a, b;
a = new Array(0,1,2,3,4);
b = a.join("-");      //"0-1-2-3-4"
```
### 字符串-数组

 
**字符串转数组**
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







