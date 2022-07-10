$(document).ready(function () {
    //鼠标移入地图区域通过滚轮缩放时禁止页面上下滚动
    $("#map").mousemove(function () {
        $(document).bind('mousewheel', function (event, delta) { return false; });
    });
    $("#map").mouseleave(function () {
        $(document).unbind('mousewheel');
    });
    //地图样式单选按钮事件绑定
    $("#btn-watercolor").on("click", function () {
        chgStamenMap("watercolor")
    })
    $("#btn-terrain").on("click", function () {
        chgStamenMap("terrain")
    })
    $("#btn-toner").on("click", function () {
        chgStamenMap("toner")
    })
});