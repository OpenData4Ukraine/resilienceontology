var sourceLayer;
$(document).ready(function () {
    // 获取矢量地图数据并加载（可修改url以从后台地址获取）
    $.ajax({
        url: '../data/geojson/Ukraine.geojson',
        success: function (data, status) {
            addGeoJSON(data);
        }
    });

    //读取maphub数据
    $.ajax({
        url: '../data/geojson/russian-ukraine-monitor.geojson',//可改为后台url获取自定义数据
        success: function (data, status) {
            let features = data.geojson.features;
            let sourceVector = new ol.source.Vector({});
            features.forEach(ele => {
                let featureObject = createFeatureObject(ele)
                sourceVector.addFeature(featureObject);

                //构建分组-要素关系数据结构-用于createFeatureList()
                const groupId = String(ele.properties.group)
                !fgi[groupId] ? fgi[groupId] = [] : true
                fgi[groupId].push(ele)
            });
            sourceLayer = new ol.layer.Vector({
                source: sourceVector,
                // style: getStyle('#333333') //统一设置图层样式（即所有要素使用相同图标样式）
            });
            map.addLayer(sourceLayer);

            createFeatureList(data.geojson.groups);
        }
    });
})

//创建要素对象
function createFeatureObject(f) {
    let feature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat(f.geometry.coordinates))
    });
    feature.setId(f.id)
    for (key in f.properties) {
        feature.set(key, f.properties[key])
    }
    feature.setStyle(getStyle(f.properties["marker-color"])) //要素图标填充对应的颜色
    return feature
}

// 加载矢量图层方法
function addGeoJSON(src) {
    //矢量地图层
    let clipLayer = new ol.layer.Vector({
        source: new ol.source.Vector({
            features: (new ol.format.GeoJSON()).readFeatures(src, {  // 用readFeatures方法可以自定义坐标系
                dataProjection: 'EPSG:4326',    // 设定JSON数据使用的坐标系
                featureProjection: 'EPSG:3857' // 设定当前地图使用的feature的坐标系
            })
        }),
        style: new ol.style.Style({
            stroke: new ol.style.Stroke({ //轮廓
                color: '#3c77d4',
                width: 3
            })
        })
    });

    //除矢量图层区域，其它区域风格化处理
    clipLayer.getSource().on("addfeature", function () {
        base.setExtent(clipLayer.getSource().getExtent());
    });

    const style = new ol.style.Style({
        fill: new ol.style.Fill({
            color: "black",
        }),
    });

    base.on("postrender", function (e) {
        const vectorContext = ol.render.getVectorContext(e);
        e.context.globalCompositeOperation = "destination-in";
        clipLayer.getSource().forEachFeature(function (feature) {
            vectorContext.drawFeature(feature, style);
        });
        e.context.globalCompositeOperation = "source-over";
    });

    //加入
    map.addLayer(clipLayer);
}

//要素样式定义
function getStyle(color) {
    //png图标+颜色填充（16进制颜色#FFFFFF）
    return new ol.style.Style({
        image: new ol.style.Icon({
            anchor: [0.55, 0.9],//图标锚点位置，单位由anchorXUnits和anchorYUnits确定
            anchorXUnits: 'fraction',//缺省为百分比（fraction），可选像素点（pixels）
            anchorYUnits: 'fraction',
            color: hexToRgba(color, 1),
            src: '../images/position_48.png',
            scale: 0.8,//缩放比例
        }),
    })
    //矢量图形+填充色
    // var highAlpColor = ol.color.asArray(color); // hex -> rgb
    // highAlpColor = highAlpColor.slice();  
    // highAlpColor[3] = 0.5; // rgba
    // return new ol.style.Style({
    //     image: new ol.style.Circle({ //圆
    //         radius: 5,
    //         fill: new ol.style.Fill({
    //             color: highAlpColor
    //         })
    //     })
    // })
}

//hex -> rgba
function hexToRgba(hex, opacity) {
    return 'rgba(' + parseInt('0x' + hex.slice(1, 3)) + ',' + parseInt('0x' + hex.slice(3, 5)) + ','
        + parseInt('0x' + hex.slice(5, 7)) + ',' + opacity + ')';
}

//分组-要素关系
var fgi = {};

//创建要素分组及要素清单页面元素
function createFeatureList(groups) {
    let html = '<div class="panel-group" id="accordion">'
    groups.forEach(group => {
        let groupId = String(group.id)
        const fs = fgi[groupId]
        if (fs && fs.length > 0) {
            html = html + '<div class="panel panel-default panel-group-head">'
            // 组
            html = html + '<div class="panel-heading">'
            html = html + '<i class="bi bi-eye-fill" id="groupicon' + groupId + '" onclick="toggGroupShow(' + groupId + ')" data-toggle="tooltip" title="show/hide"></i>'
            html = html + '<span class="group-title" data-toggle="collapse" data-parent="#accordion" href="#groupid' + groupId + '" data-toggle="tooltip" title="' + group.title + '">' + group.title + '</span>'
            html = html + '</div>'
            html = html + '<div id="groupid' + groupId + '" class="panel-collapse collapse out">'
            html = html + '<div class="panel-body feature-panel">'
            // 要素列表
            fs.forEach(f => {
                html = html + '<div class="tree-node">'
                html = html + '<span class="node-color" style="background-color:' + f.properties["marker-color"] + ';"></span>'
                html = html + '<i class="bi bi-geo-alt node-icon"></i>'
                html = html + '<span class="node-title" onclick="findFeature(' + JSON.stringify(f).replace(/"/g, '&quot;') + ')" data-toggle="tooltip" title="' + f.properties.title + '">' + f.properties.title + '</span>'
                html = html + '</div>'
            })
            html = html + '</div></div></div>'
        }
    })
    html = html + "</div>"
    $("#feature-list").html(html)
}

//点击清单中的要素按钮后触发，定位到地图并弹框
function findFeature(feature) {
    popupOverlay.setPosition(undefined);
    let position = ol.proj.fromLonLat(feature.geometry.coordinates)//经纬度转换为地图坐标
    feature.properties["id"] = feature.id//设置id，下载时作为文件名
    //（动画）定位&缩放（先缩小再放大）
    map.getView().animate({
        center: position,
        zoom: 8,
        duration: 1000
    })
    setTimeout(function () {
        map.getView().animate({
            center: position,
            zoom: 12,
            duration: 1000
        })
        //显示弹框
        showPopup(feature.properties, position)
    }, 1100)
    //直接定位&缩放
    // let view = map.getView();
    // view.setZoom(10);
    // view.setCenter(ol.proj.fromLonLat(feature.geometry.coordinates));

}

var fgit = {}//手动隐藏的组
//切换一组要素[隐藏/显示]
function toggGroupShow(groupId) {
    let gigid = "#groupicon" + groupId //组图标ID
    // console.log(sourceLayer.getSource().getFeatures())
    const fs = fgi[groupId]
    if (!fgit[groupId]) {
        fgit[groupId] = true
        //删除一组要素
        fs.forEach(f => {
            let featureObject = sourceLayer.getSource().getFeatureById(f.id)
            sourceLayer.getSource().removeFeature(featureObject)
        })
        //组图标修改为不显示
        $(gigid).removeClass("bi-eye-fill").addClass("bi-eye-slash")
    } else {
        fgit[groupId] = false
        //添加一组要素
        fs.forEach(f => {
            let featureObject = createFeatureObject(f)
            sourceLayer.getSource().addFeature(featureObject);
        })
        //组图标修改为显示
        $(gigid).removeClass("bi-eye-slash").addClass("bi-eye-fill")
    }
    // map.removeLayer(sourceLayer)
}
