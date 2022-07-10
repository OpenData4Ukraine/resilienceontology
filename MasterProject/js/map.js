// 弹出框定义
var container = document.getElementById('popup');
var title = document.getElementById('popup-title');
var content = document.getElementById('popup-content');
var closer = document.getElementById('popup-closer');
var btn = document.getElementById('popup-btn');

// 创建一个overlay, 绑定html元素container
var popupOverlay = new ol.Overlay(({
  //设置弹出框的容器
  element: container,
  //是否自动平移使弹出框完全可见
  autoPan: true,
  autoPanMargin: 200,
  positioning: 'top-right',
  autoPanAnimation: {
    duration: 500 //当Popup超出地图边界时，为了Popup全部可见，移动地图的速度
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

//Ukraine地图拖动范围限制（左上、右下 经纬度）
const UkraineExtent = ol.proj.transformExtent(
  [22.13, 52.0, 40.22, 45.35],
  "EPSG:4326",
  "EPSG:3857"
);

//背景层-加载Stamen Map
const background = new ol.layer.Tile({
  className: "stamen",
  source: new ol.source.Stamen({
    layer: "watercolor",//toner炭笔轮廓//terrain地形//watercolor水彩
  }),
});
//基础地图层-加载OpenStreetMap
const base = new ol.layer.Tile({
  source: new ol.source.OSM(),
});

//创建地图
var map = new ol.Map({
  target: "map",
  layers: [
    background,
    base,
    // clipLayer
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([31.4, 48.9]), //默认地图中心[30.52, 50.44]
    zoom: 5,
    minZoom: 5,
    extent: ol.extent.buffer(UkraineExtent, 200000), //拖动范围限制，余量200km
    showFullExtent: true,
  }),
});

//将popupOverlay添加到map
map.addOverlay(popupOverlay);

//监听map点击事件&获取要素&显示弹框
map.on('singleclick', function (e) {
  // 点击地图任意位置先关闭弹框
  popupOverlay.setPosition(undefined);
  // 获取要素
  let coordinate
  let propertys
  map.forEachFeatureAtPixel(e.pixel, function (feature, layer) {
    if (!coordinate && !propertys) {//取第一条匹配要素，其余忽略
      coordinate = ol.extent.getCenter(feature.getGeometry().getExtent());//地图坐标
      propertys = feature.getProperties();// 要素属性
      propertys["id"] = feature.getId()//设置id，下载时作为文件名
    }
  })
  //若获取到要素则显示弹框&放大地图
  if (coordinate && propertys) {
    //因拖动范围限制，若地图缩放比例太小则适当放大地图以防弹出框无法全部显示
    if (map.getView().getZoom() < 10) {
      map.getView().animate({
        center: coordinate,
        zoom: 10,
        duration: 1000
      })
    }
    //显示弹框
    showPopup(propertys, coordinate)
  }
});

/**
 * 设置弹框内容&显示弹框
 * 参考示例数据russian-ukraine-monitor.geojson
 * @param {*} property 要素属性
 * @param {*} position 地图坐标
 */
function showPopup(propertys, position) {
  // 弹框标题定义
  title.innerHTML = propertys.title;
  title.title = propertys.title;
  // 弹框内容定义(弹框容器配合css样式“white-space:pre-line”以自动换行)
  let hdms = "<p>" + propertys.description + "</p>";

  // 以下注释部分为读取Demo数据kyivFeature.json的格式解析显示
  // title.innerHTML = propertys["name"];
  // let hdms = "";
  // for (key in propertys) {
  //     if (key !== "name" && key !== "geometry") { //排除要素中的geometry
  //         hdms = hdms + "<b>" + key.toUpperCase() + "</b>: " + propertys[key] + "<br/>";
  //     }
  // }

  // 地图坐标转经纬度
  let coordinates = ol.proj.transform(position, 'EPSG:3857', 'EPSG:4326')
  let coordinateStr = ol.coordinate.toStringHDMS(coordinates);
  content.innerHTML = hdms + "<b>COORDINATE</b>: " + coordinateStr;
  // 下载事件
  btn.innerHTML = '<i class="bi bi-cloud-download" onclick="downloadFeature(' + JSON.stringify(propertys).replace(/"/g, '&quot;') + ')"></i>'
  // 设置弹框位置，从而显示在鼠标点击处
  popupOverlay.setPosition(position);
}

// 鼠标指向要素显示手图标
map.on('pointermove', function (e) {
  let pixel = map.getEventPixel(e.originalEvent);
  let hit = map.hasFeatureAtPixel(pixel);
  map.getTargetElement().style.cursor = hit ? 'pointer' : '';
});

// 下载要素信息到本地
function downloadFeature(propertys) {
  var textFileAsBlob = new Blob([propertys.title + "\n" + propertys.description], { type: 'text/plain' });
  var downloadLink = document.createElement("a");
  downloadLink.download = propertys.id + ".txt";
  downloadLink.href = URL.createObjectURL(textFileAsBlob);
  downloadLink.click();
}

// 切换Stamen地图风格
function chgStamenMap(layer) {
  console.log(layer)
  background.setSource(new ol.source.Stamen({
    layer: layer,
  }))
}