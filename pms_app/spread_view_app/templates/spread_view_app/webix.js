var stock_ui2 = {
    id: "stock_ui",
    view: "dataview",
    type:{
        width: 260,
        height: 90,
        template:"http->{{ STATIC_URL }}pms_app/spread_view_app/stock_ui.html"
    }
};

var ui_body = {
    view:"accordion",
    rows: [
        stock_ui2
    ]
};