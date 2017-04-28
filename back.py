import pyautogui as py
import time, sys, glob, os
from os.path import expanduser
from ghost import Ghost
Home=expanduser("~")

ghost = Ghost()
ghost.open('https://dl.dropboxusercontent.com/u/13991899/test/index.html')
js_variable, _ = ghost.evaluate('a', expect_loading=True)
print js_variable
time.sleep(3)

screenWidth, screenHeight = py.size()
py.click(screenWidth / 2, screenHeight / 2)

py.press('f12')

time.sleep(1)

py.typewrite("""var d = new Date();\n
var str = g_img.url;\n
var strstr = str.replace("//", "http://")\n
var a = document.createElement('a');\n
a.href = strstr;\n
a.download = d;\n
document.body.appendChild(a);\n
a.click();\n
document.body.removeChild(a);""")
py.press('enter')

time.sleep(1)


files = glob.glob('%s/Downloads/*.xls'%Home)

newest = min(files, key=os.path.getctime)
os.system("gsettings get org.gnome.desktop.background picture-uri 'file:///%s/Downloads/%s'"% (Home, newest))

