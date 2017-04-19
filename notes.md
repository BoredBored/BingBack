# Notes
In order to get the background url you need to parse for `g_img={url: `. It should look like

`g_img={url: "/az/hprichbg/rb/BristleconePine_EN-US9234523201_1920x1080.jpg",id:'bgDiv',d:'200',cN:'_SS',crN:'bIm',hash: "202",del: 50}`

So all BB needs to do to get the bing image is

backUrl = "https://www.bing.com%s"%url
