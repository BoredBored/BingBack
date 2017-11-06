# -*- coding: UTF-8 -*-
from subprocess import call
from os.path import expanduser
from os.path import isdir
from os.path import isfile
from datetime import datetime
from datetime import date
from os import chdir
from os import mkdir
from urllib2 import urlopen
from urllib2 import Request
from json import loads

SeeDebugMessages = False
SetDestopWallpaper = False
home = expanduser('~')
folder = "Pictures"
BingBackFolder = "%s/%s/BingDailyImages" % (home, folder) #change to "" if you don't care
LogPath = "%s/BING_BACK_LOG.txt" % (BingBackFolder)
PrintedDateInLog = False
now = datetime.now()
todaydate = "%s\%s\%s"%(now.month, now.day, now.year)
def log(str):
    if SeeDebugMessages == True:
        print("%s ERROR: %s"%(todaydate, str))
    with open(LogPath, "a+") as f:
        try: 
            f.write("%s ERROR: %s"%(todaydate, str))
        except:
            f.close()
            print("%s ERROR: LOGGING INTERRUPTED"%(todaydate))
            quit()
        f.close()
        quit()

def makeFolder(str):
    #str = str.replace("/", "\\") #comment out if recursively creating folders
    if str == "":
        if SeeDebugMessages == True:
            print("ERROR: Please specify a folder name -- \"\"/NULL is not a folder name")
        return 2
    elif isdir(str) == False:
        if SeeDebugMessages == True:
            print("Creating folder \'%s\'" % (str))
        mkdir(str)
        return 0
    else:
        if SeeDebugMessages == True:
            print("Folder \'%s\' already exists" % (str))
        return 1

def downloadPic(url, str): #str = name
    if str == "":
        if SeeDebugMessages == True:
            print("ERROR: Please specify a file name for your picture -- \"\"/NULL is not a file name")
        return 1
    elif isfile(str) == False:
        if SeeDebugMessages == True:
            print("Downloading picture from: %s\nSaving pic as: %s" % (url, str))
        with open(str,'wb')as f:
            f.write(urlopen(url).read())
            f.close()
        return 0
    else:
        if SeeDebugMessages == True:
            print("File \'%s\' already exists" % (str))
        return 1


def ImgPathFunc():
    #make request to get the image json
    req = Request("http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US")
    ImgJSON = ""
    res = ""
    try:
        res = urlopen(req)
    except:
        print("Error")

    data = res.read()

    #parse json to get the image url
    ImgJSON = loads(data)

    return ImgJSON['images'][0]['url']

def GETName(str): #str = ImgPath
    #check if it is the right path
    if ("/az/hprichbg/rb/" in str) is False:
        log("String \'/az/hprichbg/rb/\' not in string \'%s\'" % (str))
    else:
        return str.replace("/az/hprichbg/rb/", "")

def BingImg():
    ImgPath = ImgPathFunc()
    #               ImgURL                          ImgName            
    return "http://www.bing.com%s"%(ImgPath), GETName(ImgPath)

def BingFolder():
    makeFolder(BingBackFolder)
    #todayfolder = "%s/%s" %(BingBackFolder, todaydate)

    #makeFolder(todayfolder)
    chdir(BingBackFolder)#change to chdir(todayfolder) if you want to download images in the folder of the day

def printArr(arr):
  print ' '.join(arr)

def change_wallpaper_win(SPISETDESKWALLPAPER, WALLPAPER_PATH):
    import struct
    import ctypes
    #not tested
    sys_parameters_info = ctypes.windll.user32.SystemParametersInfoW if struct.calcsize('P') * 8 == 64 else ctypes.windll.user32.SystemParametersInfoA
    r = sys_parameters_info(SPISETDESKWALLPAPER, 0, WALLPAPER_PATH, 3)

    # When the SPI_SETDESKWALLPAPER flag is used,
    # SystemParametersInfo returns TRUE
    # unless there is an error (like when the specified file doesn't exist).
    if not r:
        print(ctypes.WinError())
	return False
    return True

def set_wallpaper_windows(ab_path):
  change_wallpaper_win(20, ab_path)
def set_wallpaper_linux(file_loc, debug):
        # Note: There are two common Linux desktop environments where 
        # I have not been able to set the desktop background from 
        # command line: KDE, Enlightenment
        from platform import linux_distribution
        from subprocess import Popen as ex
        from sys import stderr
        desktop_env = linux_distribution()
        if debug == True: 
            print ("Desktop_env = %s"%(str(desktop_env)))
            print (file_loc)
        try:
            if ["gnome", "unity", "cinnamon"] in desktop_env:
                uri = "\"file://%s\"" % file_loc
                if debug == True: print ("Gnome/Unity/Cinnamon detected")
                #try: from gi.repository import Gio
                #except: 
                #    stderr.write("Please install PyGObject (https://python-gtk-3-tutorial.readthedocs.io/en/latest/install.html)\n")
                #    return False
                try:
                    from gi.repository import Gio
                    SCHEMA = "org.gnome.desktop.background"
                    KEY = "picture-uri"
                    gsettings = Gio.Settings.new(SCHEMA)
                    gsettings.set_string(KEY, uri)
                except:
                    args = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri]
                    printArr(args)
                    ex(args)
            elif desktop_env=="gnome2": # Not tested
                if debug == True: print ("Gnome2 detected")
                args = ["gconftool-2","-t","string","--set","/desktop/gnome/background/picture_filename", '"%s"' %file_loc]
                printArr(args)
                ex(args)
            elif desktop_env in ["kde3", "trinity"]:
                if debug == True: print ("KDE3/Trinity detected")
                args = 'dcop kdesktop KBackgroundIface setWallpaper 0 "%s" 6' % file_loc
                printArr(args)
                ex(args, shell=True)
            elif "LinuxMint" in desktop_env:
                uri = "\"file://%s\"" % file_loc
                args = ["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", uri]
                if debug == True: printArr(args)
                ex(args)
            else:
                stderr.write("Warning: Failed to set wallpaper. Your desktop environment is not supported.\n")
                stderr.write("You can try to manually to set your wallpaper to \'%s\'\n" % file_loc)
                return False
            return True
        except:
            stderr.write("ERROR: Failed to set wallpaper. There might be a bug.\n")
            return False

def setWallMain(pathy):
  from platform import system
  ostype = system()
  if debug == True: print ("OS type: %s"%(ostype))
  if ostype == "Linux":
    return set_wallpaper_linux(pathy, debug)
  elif ostype == "Windows":
    return set_wallpaper_windows(pathy)
  else:
    stderr.write("ERROR: Failed to set wallpaper. There might be a bug.\n")
    return False

def setWallpaper(path, debug):
  from os.path import isfile
  from os.path import isabs
  from os import getcwd
  from sys import stderr
  pathy = path
  if isfile(pathy) == False:
    stderr.write("ERROR: \"%s\" is not a file\n"%(pathy))
    return False
  if isabs(pathy) == False:
    pathy = "%s/%s"%(getcwd(), path) # change to absolute path
    if debug == True: print ("Changed \'%s\' to %s"%(path, pathy))
  setWallMain(pathy)
  

def main():
    ImgURL, ImgN = BingImg()

    BingFolder() # Comment out if you just want to download in your current working dir

    downloadPic(ImgURL, ImgN)
	
    if SetDestopWallpaper == True:
        print("~ Setting as wallpaper ~")
        setWallpaper(ImgN, SeeDebugMessages)
        
main()
