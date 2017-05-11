<?php
/*g_img.url*/

$bingHomepage = file_get_contents('http://www.bing.com/');
$gimgString = "g_img={url: \""
$gimgStringLength = strlen($gimgString); //im lazy
$gimgPos = strpos($bingHomepage, $gimgString);
$bingBackImageURL = $gimgPos + $gimgStringLength;

/*
files = glob.glob('%s/Downloads/*.xls'%Home)

newest = min(files, key=os.path.getctime)
os.system("gsettings get org.gnome.desktop.background picture-uri 'file:///%s/Downloads/%s'"% (Home, newest))*/

?>
