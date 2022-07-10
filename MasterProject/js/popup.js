// 弹出框
var container = document.getElementById('popup');
var title = document.getElementById('popup-title');
var content = document.getElementById('popup-content');
var closer = document.getElementById('popup-closer');

// 创建一个overlay, 绑定html元素container
var popupOverlay = new ol.Overlay(({
    //设置弹出框的容器
    element: container,
    //是否自动平移使弹出框完全可见
    autoPan: true,
    autoPanMargin: 200,
    positioning: 'top-right',
    autoPanAnimation: {
        duration: 250 //当Popup超出地图边界时，为了Popup全部可见，移动地图的速度
    }
}));

// X 点击关闭弹窗
closer.addEventListener('click', function (event) {
    popupOverlay.setPosition(undefined);
    //阻止事件冒泡防止页面跳到上面去
    event.stopPropagation();
    event.preventDefault();
    return false;
});

//将popupOverlay添加到map
map.addOverlay(popupOverlay);

//监听map点击事件&获取要素&显示弹框
map.on('singleclick', function (e) {
    // 获取当前点击坐标
    // var coordinate = e.coordinate;
    // 转换经纬
    // var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(coordinate, 'EPSG:3857', 'EPSG:4326'));
    // 设置弹框内容
    // content.innerHTML = '<p>You clicked here:</p><code>' + hdms + '</code>';
    // 设置popupOverlay的位置，从而显示在鼠标点击处
    // popupOverlay.setPosition(coordinate);

    // 点击其它位置关闭弹框
    popupOverlay.setPosition(undefined);

    // 获取点击要素
    /*参考示例数据kyivFeature.json
        feature要素定义时，除lon、lat、style以外。其余数据都会加入（注意要素中还会自动加入geometry属性）
        {
            "lon": "34.48797",
            "lat": "50.05548",
            "style": "orange",
            "name": "TEST1",
            "date": "15/03/2022",
            "remark": "VIOLENCE LEVEL: 1"
        }, 
    */
    map.forEachFeatureAtPixel(e.pixel, function (feature, layer) {
        // 坐标
        var coordinate = ol.extent.getCenter(feature.getGeometry().getExtent());
        var coordinateStr = ol.coordinate.toStringHDMS(ol.proj.transform(coordinate, 'EPSG:3857', 'EPSG:4326'));
        // 要素属性
        var property = feature.getProperties();

        // 弹框标题定义(取自name)
        title.innerHTML = property["name"]; //or feature.get("name")
        // 弹框内容定义
        var hdms = "";
        for (key in property) {
            if (key !== "name" && key !== "geometry") { //排除要素中的geometry
                hdms = hdms + "<b>" + key.toUpperCase() + "</b>: " + property[key] + "<br/>";
            }
        }
        // 坐标
        hdms = hdms + "<b>COORDINATE</b>: " + coordinateStr;
        content.innerHTML = '<p>' + hdms + '</p>';

        // 设置弹框位置，从而显示在鼠标点击处
        popupOverlay.setPosition(coordinate);

    })

});
