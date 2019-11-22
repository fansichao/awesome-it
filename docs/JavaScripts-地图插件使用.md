# JS-地图插件使用

tags: JavaScript 2019年 地图 插件 百度地图API

TODO 写的更细？图文并茂？？

## 地图JavaScript插件对比

**JS_地图插件对比**
![JS_地图插件对比](images/../../images/JS_地图插件对比_20191028.png)

- [几款JS地图插件比较](https://blog.csdn.net/liangyixin19800304/article/details/12462917)

## 百度地图API使用

百度地图**官方API, 不完整，不易于使用**.

官方链接

- [百度地图开放平台开发者注册](http://lbsyun.baidu.com/apiconsole/key?application=key)
- [百度地图API](http://lbsyun.baidu.com/jsdemo.htm#a1_2)
- [DrawingManager工具栏官网](http://api.map.baidu.com/library/DrawingManager/1.4/docs/symbols/BMapLib.DrawingManager.html#setDrawingMode)
- [百度拾取坐标系统](http://api.map.baidu.com/lbsapi/getpoint/index.html)
- [输入地址查询](http://lbsyun.baidu.com/jsdemo.htm#a6_2)

博客链接

- [百度地图添加可拖拽点+信息窗口提交表单](https://blog.csdn.net/damionew/article/details/80651224)
- [百度地图javascript开发，删除指定覆盖物方法](https://blog.csdn.net/opengps/article/details/80827663)
- [百度地图 -- 鼠标绘制工具DrawingManager](https://blog.csdn.net/weixin_38122772/article/details/89517774)
- [实现可以拖动地图上的标识来选点，并返回选择点的地址和坐标等信息](http://itnoteshare.com/note/183/publicNoteDetail.htm)

### 代码样例

详见 【GIS原型页面】, 代码可做工具书参考。

```JavaScript
/*
 >>>>>>>>>>>>>>> 基础函数 <<<<<<<<<<<<<<<<
*/

// 获取 Input 框输入值
var getInputValue = function (input_id) {

    if (document.getElementById(input_id) == null) {
        console.log(input_id + "的div为空")
        return null
    }
    var inputValue = document.getElementById(input_id).value;
    return inputValue
}

// 设置 Input 框输入值
var SetInputValue = function (input_id, ivalue) {
    $('#' + input_id).val(ivalue);
}

// 校验经度 - 校验经度是否符合规范
function checkLong(lng) {
    var longrg = /^(\-|\+)?(((\d|[1-9]\d|1[0-7]\d|0{1,3})\.\d{0,6})|(\d|[1-9]\d|1[0-7]\d|0{1,3})|180\.0{0,6}|180)$/;
    if (!longrg.test(lng)) {
        //return '经度整数部分为0-180,小数部分为0到6位!';
        swal("提示!", '经度整数部分为0-180,小数部分为0到6位!', "warning")
        return false
    }
    return true;
}

// 检验纬度 - 校验纬度是否符合规范
function checkLat(lat) {
    var latreg = /^(\-|\+)?([0-8]?\d{1}\.\d{0,6}|90\.0{0,6}|[0-8]?\d{1}|90)$/;
    if (!latreg.test(lat)) {
        // return '纬度整数部分为0-90,小数部分为0到6位!';
        swal("提示!", '纬度整数部分为0-90,小数部分为0到6位!', "warning")
        return false
    }
    return true;
}

// 数组去重
function unique(arr) {
    return Array.from(new Set(arr))
}
/*
 >>>>>>>>>>>>>>> 地图底层函数 <<<<<<<<<<<<<<<<
 */

// 添加覆盖物-圆
function add_circle(point, radius, styleOptions) {
    // 点位置(经纬度) 半径(数字) 图样式
    var circle = new BMap.Circle(point, radius, styleOptions); //创建圆
    map.addOverlay(circle);         // 增加圆
    return circle
}

// 添加覆盖物-矩形
function add_rectangle(points, styleOptions) {
    var rectangle = new BMap.Polygon(points, styleOptions);
    map.addOverlay(rectangle);
    return rectangle
}

// 添加覆盖物-折线
function add_polyline(points, styleOptions) {
    var polyline = new BMap.Polyline(points, styleOptions)

    map.addOverlay(polyline);
    return polyline
}

// 添加覆盖物-点
function add_marker(point, styleOptions) {
    var marker = new BMap.Marker(point);
    map.addOverlay(marker);
    return marker
}

// 添加覆盖物-多边形
function add_polygon(points, styleOptions) {
    var polygon = new BMap.Polygon(points, styleOptions)
    map.addOverlay(polygon);
    return polygon
}

// 设置点的弹跳动画
function SetAnimation(marker) {
    marker.setAnimation(BMAP_ANIMATION_BOUNCE);
}

// 删除所有覆盖物
function clearAll() {
    for (var i = 0; i < overlays.length; i++) {
        map.removeOverlay(overlays[i]);
    }
    overlays.length = 0
    map.clearOverlays();
}

// 显示所有覆盖物
function showAll() {
    for (var i = 0; i < overlays.length; i++) {
        overlays[i].show()
    }
}

// 隐藏所有覆盖物
function hideAll() {
    var allOverlay = map.getOverlays();
    for (var i = 0; i < allOverlay.length; i++) {
        overlays[i].hide()
    }
}

/*
 >>>>>>>>>>>>>>> 地图中层函数 <<<<<<<<<<<<<<<<
*/

// TODO 隐藏 弹出信息框 未使用
var HideInfoWindow = function (marker) {
    if (marker.isInfoWindowShown()) {
        marker.hideInfoWindow();//这个是隐藏infowindow窗口的方法
    }
}

// 工具栏-切换 DrawingMode
function switchDrawingMode(drawing_type) {
    // BMAP_DRAWING_HANDER BMAP_DRAWING_MARKER...
    if (typeof(drawingManager) != "undefined" && drawingManager) {
        // drawingManager.getDrawingMode()
        drawingManager.setDrawingMode(drawing_type)
        drawingManager.close()
        if (drawing_type != BMAP_DRAWING_HANDER) {
            drawingManager.open()
        }
    }
}

/* 根据查询项 查询匹配的data数据
    功能:
        根据查询项 查询匹配的data数据
        根据输入search_str,过滤数据,模糊匹配

    :param string key: 查询列key
    :param string search_str: 查询的字符串
    :param array data: 数据
        exp: [{'name':'王二'}]

    exp:
       输入 [{'name':'王二'}] 'name' '王'  会返回数据 [{'name':'王二'}]

    TODO 命中标红
    TODO 多层嵌套不支持 例如. val为数组or字典等
*/
var SearchTableData = function (data, key, search_str) {
    if (typeof(search_str) == "undefined" || search_str == "") {
        const newdata = [...data];
        return newdata
    }

    var newdata = [];
    search_str = search_str.toString()
    for (dic of data) {
        if (!dic.hasOwnProperty(key)) {
            break
        }
        if (dic[key].indexOf(search_str) >= 0) {
            newdata.push(dic)
        }
    }
    return newdata
}

// 右键菜单-删除标记
var menuRemoveMarker = function (e, ee, marker) {
    map.removeOverlay(marker);
}

// 定位到当前地址
function ToLocation() {
    // 添加带有定位的导航控件
    var navigationControl = new BMap.NavigationControl({
        // 靠左上角位置
        anchor: BMAP_ANCHOR_TOP_LEFT,
        // LARGE类型
        type: BMAP_NAVIGATION_CONTROL_LARGE,
        // 启用显示定位
        enableGeolocation: true
    });
    map.addControl(navigationControl);
// 添加定位控件
    var geolocationControl = new BMap.GeolocationControl();
    geolocationControl.addEventListener("locationSuccess", function (e) {
        // 定位成功事件
        var address = '';
        address += e.addressComponent.province;
        address += e.addressComponent.city;
        address += e.addressComponent.district;
        address += e.addressComponent.street;
        address += e.addressComponent.streetNumber;
    });
    geolocationControl.addEventListener("locationError", function (e) {
        // 定位失败事件
        alert(e.message);
    });
    map.addControl(geolocationControl);

}
// 用经纬度设置地图中心点
function theLocation() {
    if (document.getElementById("longitude").value != "" && document.getElementById("latitude").value != "") {
        map.clearOverlays();
        var new_point = new BMap.Point(document.getElementById("longitude").value, document.getElementById("latitude").value);
        var marker = new BMap.Marker(new_point);  // 创建标注
        map.addOverlay(marker);              // 将标注添加到地图中
        map.panTo(new_point);
    }
}

// 根据地址查询经纬度
function searchlnglatByStationName(address) {
    var localSearch = new BMap.LocalSearch(map);
    /*
    localSearch.setSearchCompleteCallback(function (searchResult) {
        var poi = searchResult.getPoi(0);
        document.getElementById("atm_input_lng").value = poi.point.lng;
        document.getElementById("atm_input_lat").value = poi.point.lat;
        map.centerAndZoom(poi.point, 13);
        var marker = new BMap.Marker(new BMap.Point(poi.point.lng, poi.point.lat));  // 创建标注，为要查询的地方对应的经纬度
        map.addOverlay(marker);


        var content = document.getElementById("text_").value + "<br/><br/>经度：" + poi.point.lng + "<br/>纬度：" + poi.point.lat;
        var infoWindow = new BMap.InfoWindow("<p style='font-size:14px;'>" + content + "</p>");
        marker.addEventListener("click", function () {
            this.openInfoWindow(infoWindow);
        });
        marker.setAnimation(BMAP_ANIMATION_BOUNCE); //跳动的动画
    });
    localSearch.search(address);
    */
    localSearch.setSearchCompleteCallback(function (searchResult) {
        var poi = searchResult.getPoi(0);
        document.getElementById("atm_input_lng").value = poi.point.lng;
        document.getElementById("atm_input_lat").value = poi.point.lat;
    });
    localSearch.search(address);
}

// 获取点信息 TODO 直接return不行 使用val赋值获取
var getPointInfo = function (point) {
    var gc = new BMap.Geocoder();
    gc.getLocation(point, function (rs) {
        var addComp = rs.addressComponents;

        var mapAddress = addComp.province + addComp.city + addComp.district + addComp.street + addComp.streetNumber;
        $("#enemy_address").val(mapAddress)
        $("#address").val(mapAddress)
        $("#city").val(addComp.city)

    })
}
// 生成OverlayID
var generateRandomOverlayID = function (overlay_type) {
    /*
        @param overlay_type: 覆盖物类型 atm or overlay
     */
    if (overlay_type == "atm") {
        for (var dic of MARKDATA) {
            var dic_num = dic['overlay_id'].split('atm')[1]
            if (!max_atm_num) {
                max_atm_num = dic_num
            } else {
                if (max_atm_num < dic_num) {
                    max_atm_num = dic_num
                }
            }
        }
        max_atm_num = max_atm_num + 1
        var overlay_id = "atm" + (max_atm_num).toString()
    } else {
        for (var dic of ENEMY_DATA) {
            var dic_num = dic['overlay_id'].split('atm')[1]
            if (!max_enemy_num) {
                max_enemy_num = dic_num
            } else {
                if (max_enemy_num < dic_num) {
                    max_enemy_num = dic_num
                }
            }
        }
        max_enemy_num = max_enemy_num + 1
        var overlay_id = "enemy" + (max_enemy_num).toString()
    }
    current_overlay_id = overlay_id
    return overlay_id
}

// 根据覆盖物ID 获取覆盖物
function getMapOverlay(overlay_id) {
    /*  
        示例中，所有的Marker属性都是用  marker.overlay_id = overlay_id; 的方式为Marker对象赋值了一个id
        因此，我的写法是：
        先获取全部覆盖物：
        然后判断覆盖物是否是Marker类型：
        然后判断是否是我要删除的id(imei)：
        然后拿到目标对象，执行删除操作
  */

    var reMarker = null;
    var allOverlay = map.getOverlays();
    for (var i = 0; i < allOverlay.length; i++) {
        if (allOverlay[i].overlay_id == overlay_id) {
            reMarker = allOverlay[i];
            break;
        }
    }
    return reMarker;
}

// 删除工具栏按钮 TODO 待寻找更好方法
function delTools() {
    var parent_class = "BMapLib_Drawing BMap_noprint anchorTR";
    if (typeof(document.getElementsByClassName(parent_class)[0]) != "undefined") {
        for (var tmp of document.getElementsByClassName(parent_class)) {
            tmp.classList.remove("BMapLib_Drawing", "BMap_noprint", "anchorTR");
        }
        // document.getElementsByClassName(parent_class)[0].classList.remove("BMapLib_Drawing", "BMap_noprint", "anchorTR");
    }
    var parent_class = "BMapLib_Drawing_panel";
    if (typeof(document.getElementsByClassName(parent_class)[0]) != "undefined") {
        for (var tmp of document.getElementsByClassName(parent_class)) {
            tmp.classList.remove("BMapLib_Drawing_panel");
        }
        //document.getElementsByClassName(parent_class)[0].classList.remove("BMapLib_Drawing_panel");
    }
}


```

## 附件

### 参考链接

参考链接:

- [高德地图API](https://lbs.amap.com/api/javascript-api/example/calcutation/ring-area)
