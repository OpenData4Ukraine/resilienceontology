//批量添加地图要素方法
function addFeature(data) {
    // console.log(data)
    // let features = []
    var sourceVector = new ol.source.Vector({});
    for (var i = 0; i < data.length; i++) {
        const obj = data[i];
        let feature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat([obj.lon, obj.lat])),
            // name: obj.name,
        });
        // 用feature.set(key, value)方法进行动态赋值
        for (key in obj) {
            if (key !== "lon" && key !== "lat" && key !== "style") {//排除基础元素：坐标、样式
                feature.set(key, obj[key])
            }
        }
        // 设置要素样式
        feature.setStyle(getStyle(obj.style))
        // features.push(feature)
        sourceVector.addFeature(feature);
    }
    // let sourceVector = new ol.source.Vector({
    //   features: features
    // });
    const sourceLayer = new ol.layer.Vector({
        source: sourceVector,
        // style: getStyle('red') //统一设置图层样式（即所有要素使用相同图标样式）
    });

    map.addLayer(sourceLayer);
}

//获取自定义地图要素（此处为自定义格式：基本数据为：经纬坐标（必须），名称（对应弹框标题），图标样式，其它数据元素：日期，备注等可按需扩充）
$.ajax({
    url: '../data/feature/demoFeature.json',//可改为后台url获取自定义数据
    success: function (data, status) {
        addFeature(data.features);
    }
});