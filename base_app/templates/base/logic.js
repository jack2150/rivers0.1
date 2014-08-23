function menu_init() {
    // tree do not use sync, tree use load
    $$("menu_links").select(current_path);
    $$("menu_links").open($$("menu_links").getParentId(current_path));

    $$('menu_links').attachEvent("onAfterSelect", function() {
        var url = $$("menu_links").getSelectedId();

        if (isNaN(url)) {
            webix.send(url, null, "GET");
        }
    })
}