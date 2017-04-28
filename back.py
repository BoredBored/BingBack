from os.path import expanduser
from ghost import Ghost
Home=expanduser("~")

ghost = Ghost()
ghost.open('https://www.bing.com')
js_variable, _ = ghost.evaluate('g_img.url', expect_loading=True)
print js_variable

"""
files = glob.glob('%s/Downloads/*.xls'%Home)

newest = min(files, key=os.path.getctime)
os.system("gsettings get org.gnome.desktop.background picture-uri 'file:///%s/Downloads/%s'"% (Home, newest))"""

