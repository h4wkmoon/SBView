import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib
import json
import os
import time
import datetime
import xbmcaddon
from traceback import print_exc

__settings__ = xbmcaddon.Addon(id='plugin.video.sbview')
language = __settings__.getLocalizedString

handle = int(sys.argv[1])

# plugin modes
MODE_VIEW_FUTURE = 10
MODE_VIEW_HISTORY = 20

# parameter keys
PARAMETER_KEY_MODE = "mode"

def log(line):
    print "MMS : " + line#repr(line)
        
    #xbmc.log(line, 2)
    #xbmc.log("Test", 0) #Debug
    #xbmc.log("text", 1) #Info
    #xbmc.log("Test", 2) #Notive

def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                log("Param " + paramSplits[0] + "=" + paramSplits[1])
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

def addDirectoryItem(name, isFolder=True, parameters={}, totalItems=1):
    li = xbmcgui.ListItem(name)
    
    commands = []
    #commands.append(( "Info", "XBMC.Action(Info)", ))
    #commands.append(( "Scan", "XBMC.updatelibrary(video, '" + name + "')", ))
    #commands.append(( 'TEST', 'ActivateWindow(videolibrary, '" + name "')', ))
    #commands.append(( 'runme', 'XBMC.RunPlugin(plugin://video/myplugin)', ))
    #commands.append(( 'runother', 'XBMC.RunPlugin(plugin://video/otherplugin)', ))
    #commands.append(( "Scan", "ActivateWindow(videofiles, Movies)", ))#, '" + name + "')", ))
    li.addContextMenuItems(commands, replaceItems = True)
    
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)

    if not isFolder:
        url = name
        
    log("Adding Directory Item: " + name + " totalItems:" + str(totalItems))
    
    #dirItem = DirectoryItem()
    
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li, isFolder=isFolder, totalItems=totalItems)

def show_root_menu():

    addDirectoryItem(name=language(30111), parameters={ PARAMETER_KEY_MODE: MODE_VIEW_FUTURE }, isFolder=True)
    addDirectoryItem(name=language(30112), parameters={ PARAMETER_KEY_MODE: MODE_VIEW_HISTORY }, isFolder=True)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def view_future():
    addDirectoryItem("Future Stuff", parameters={ PARAMETER_KEY_MODE: MODE_VIEW_FUTURE }, isFolder=True)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
    
def view_history():
    addDirectoryItem("History Stuff", parameters={ PARAMETER_KEY_MODE: MODE_VIEW_FUTURE }, isFolder=True)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
    
# set up all the variables
params = parameters_string_to_dict(sys.argv[2])
mode = int(urllib.unquote_plus(params.get(PARAMETER_KEY_MODE, "0")))

# Depending on the mode do stuff
if not sys.argv[2]:
    ok = show_root_menu()
elif mode == MODE_VIEW_FUTURE:
    ok = view_future()
elif mode == MODE_VIEW_HISTORY:
    ok = view_history()

