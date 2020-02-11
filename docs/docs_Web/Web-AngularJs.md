# AnjularJS 使用手册

[toc]

### `$watch`多个变量监听

参考链接 : https://blog.csdn.net/u010451286/article/details/50635839

```javascript
$scope.count=1;
$scope.$watch('count+count2',function(){ ... ),true);
```

### bootstrap 的 modal 如何不通过 data-dismiss 关闭

去掉 data-dismiss，在 handleSave()校验成功后用

```javascript
$("#createTask").modal("hide");
```

标签 ： web angularjs html

**记录不怎么熟悉的语法**

[toc]

---

# AngularJS 教程

## AngularJS Scope(作用域)

\$rootScope

```js
$rootScope : 根作用域,所有 controller 都可以调用，类似于项目级别的全局变量
js赋值 : $rootScope.lastname = "Refsnes";
html调用 : $root.lastname
```

\$scope 作用域

```js
之间无法互相访问
Scope(作用域) 是应用在 HTML (视图) 和 JavaScript (控制器)之间的纽带。
Scope 是一个对象，有可用的方法和属性。
Scope 可应用在视图和控制器上
```

## AngularJS 控制器

```
AngularJS 控制器 控制 AngularJS 应用程序的数据。 AngularJS 控制器是常规的 JavaScript 对象。

ng-controller
ng-controller 指令定义了应用程序控制器
        
ng-controller="myCtrl" 属性是一个 AngularJS 指令。用于定义一个控制器。 myCtrl 函数是一个 JavaScript 函数。
    
JS引用

        
<script src="personController.js"></script>    
多个controller
js文件中 定义一个app    
之后可以定义多个controller    
HTML中也可以对应多个controller
```

多个 controller 控制器

```
var app = angular.module('myApp', []);
app.controller('myCtrl1', function($scope) {
    $scope.firstName = "Johns";
    $scope.lastName = "Doef";
});
    app.controller('myCtrl2', function($scope) {
    $scope.firstName = "Tom";
    $scope.lastName = "kkk";
});
```

## AngularJS 过滤器

### 过滤器

过滤器可以使用一个管道字符（|）添加到表达式和指令中。
AngularJS 过滤器可用于转换数据

currency   格式化数字为货币格式

filter   从数组项中选择一个子集。

lowercase   格式化字符串为小写。

orderBy   根据某个表达式排列数组

uppercase   格式化字符串为大写

过滤输入

输入过滤器可以通过一个管道字符（|）和一个过滤器添加到指令中，该过滤器后跟一个冒号和一个模型名称。

````
<p><input type="text" ng-model="test"></p>
<ul>
  <li ng-repeat="x in names | filter:test | orderBy:'country'">
    {{ (x.name | uppercase) + ', ' + x.country }}
  </li>
</ul>
```    

        

    
### 自定义过滤器

        
以下实例自定义一个过滤器 reverse，将字符串反转
```html
<!DOCTYPE html>
<html>
<meta charset="utf-8">
<script src="https://cdn.bootcss.com/angular.js/1.4.6/angular.min.js"></script>
<body>
<div ng-app="myApp" ng-controller="myCtrl">
姓名: {{ msg | reverse }}
</div>
<script>
var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope) {
    $scope.msg = "Runoob";
});
app.filter('reverse', function() { //可以注入依赖
    return function(text) {
        return text.split("").reverse().join("");
    }
});
</script>  
</body>
</html>
````

uppercase，lowercase 大小写转换

### AngularJS 服务(Service)

[AngularJS 服务(Service)](https://www.runoob.com/angularjs/angularjs-services.html)

AngularJS 中你可以创建自己的服务，或使用内建服务。
在 AngularJS 中，服务是一个函数或对象，可在你的 AngularJS 应用中使用。

#### \$location

$location 需要先在controller注入
$location.absUrl(); 內建 service，获取当前页面的 url 地址

#### \$http 服务

\$http 是 AngularJS 应用中最常用的服务。 服务向服务器发送请求，应用响应服务器传送过来的数据。

#### \$timeout 服务

$interval 服务 AngularJS $interval 服务对应了 JS window.setInterval 函数。

$timeout 可用于设置单次或多次延时服务;
$interval 可用于设置始终运行的延时服务。

#### 创建自定义服务

要使用自定义服务，需要在定义控制器的时候独立添加，设置依赖关系:
当你创建了自定义服务，并连接到你的应用上后，你可以在控制器，指令，过滤器或其他服务中使用它。

```
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.bootcss.com/angular.js/1.4.6/angular.min.js"></script>
</head>
<body>
<div ng-app="myApp" ng-controller="myCtrl">

<p>255 的16进制是:</p>

<h1>{{hex}}</h1>

</div>

<p>自定义服务，用于转换16进制数：</p>

<script>
var app = angular.module('myApp', []);

app.service('hexafy', function() {
    this.myFunc = function (x) {
        return x.toString(16);
    }
});
app.controller('myCtrl', function($scope, hexafy) {
  $scope.hex = hexafy.myFunc(255);
});
</script>

</body>
</html>
```

### AngularJS XMLHttpRequest

\$http 请求

- \$http.get
- \$http.head
- \$http.post
- \$http.put
- \$http.delete
- \$http.jsonp
- \$http.patch

简单 get/post 请求

```
// 简单的 GET 请求，可以改为 POST
$http({
    method: 'GET',
    url: '/someUrl'
}).then(function successCallback(response) {
        // 请求成功执行代码
    }, function errorCallback(response) {
        // 请求失败执行代码
});

$http.get('/someUrl', config).then(successCallback, errorCallback);
$http.post('/someUrl', data, config).then(successCallback, errorCallback);
```

### AngularJS Select(选择框)

AngularJS 可以使用数组或对象创建一个下拉列表选项。

ng-option 指令来创建一个下拉列表，列表项通过对象和数组循环输出
\$scope.names = ["Google", "Runoob", "Taobao"];
<select ng-init="selectedName = names[0]" ng-model="selectedName" ng-options="x for x in names">
</select>

设置下拉框初始值

方法 1 $scope.selectedCar = $scope.cars.car02;  //设置第 2 个为初始值；
方法 2  <select ng-init="selectPerson=persons['caohui']" ng-model="selectPerson" ng-options="x for (x,y) in persons">

// 列表合并
    //[].concat(METADATA).concat(CUSTACCT_METADATA).concat(CUST_METADATA),
