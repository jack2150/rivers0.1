var positions = {
    id: "1",
    open: false,
    value: "Positions",
    data: [
        { id:"{% url 'pos_view_app_index' %}", value:"Default Views" },
        { id:"{% url 'pos_import_app_index' %}", value:"Import Files" }
    ]
};

var spreads = {
    id: "2",
    open: false,
    value: "Spreads",
    data: [
        { id:"21", value:"Not Yet" }
    ]
};


var menu_links = {
    id: "menu_links",
    view: "tree",
    activeTitle: true,
    select: true,
    width: 300,
    data: [
        positions,
        spreads
    ]
};
