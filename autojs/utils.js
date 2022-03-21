/*
* 不能点击的控件，通过坐标点击
* @param {*} uiSelector
*/
function clickUiBounds(ui) {
    if (ui.exists()) {
        var a = ui.findOnce();
        if (a) {
            var b = a.bounds();
            if (b) {
                click(b.centerX(), b.centerY());
                return true;
            }
        }
    }
    return false;
}

/*
* 通过强制结束进程关闭 app
* @param {*} packageName
*/
function stopApp(packageName) {
    var name = getPackageName(packageName);
    if(!name){
        if(getAppName(packageName)){
            name = packageName;
        }else{
            return false;
        }
    }
    app.openAppSetting(name);
    text(app.getAppName(name)).waitFor();
    let is_sure = textMatches(/(.*强.*|.*停.*|.*结.*|.*行.*)|Force stop/).findOne();
    if (is_sure.enabled()) {
        textMatches(/(.*强.*|.*停.*|.*结.*|.*行.*)|Force stop/).findOne().click();
        textMatches(/(.*确.*|.*定.*)|OK/).findOne().click();
        log(app.getAppName(name) + "应用已被关闭");
        sleep(1000);
        back();
    } else {
        log(app.getAppName(name) + "应用不能被正常关闭或不在后台运行");
        back();
    }
}

/*
* 先关闭 app, 再启动，确保操作流程是从 app 首页开始
* @param {*} packageName
*/
function startApp(packageName) {
    this.stopApp(packageName)
    app.launch(packageName)
}

module.exports = {
    startApp: startApp,
    stopApp: stopApp,
    click: clickUiBounds,
    clickUiBounds: clickUiBounds
}
