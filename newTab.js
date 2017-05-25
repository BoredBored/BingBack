var bingUrl = "https://www.bing.com/chrome/newtab?origin=ext&pc=U470";
function setNewTabPage(online) {
    var newTabFrame = document.getElementById("ntp-frame");
    newTabFrame.src = bingUrl;
}
