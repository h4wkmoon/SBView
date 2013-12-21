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
import urllib2
from traceback import print_exc

__settings__ = xbmcaddon.Addon(id='plugin.video.sbview')
language = __settings__.getLocalizedString

handle = int(sys.argv[1])
dateFormat = "%I:%M %p %a %d %b %Y" 
#"%a %I:%M %p %Y/%m/%d"

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

def addDirectoryItem(name, isFolder=True, parameters={}, totalItems=1, thumbnail=""):
    
    if(thumbnail == ""):
        li = xbmcgui.ListItem(name)
    else:
        li = xbmcgui.ListItem(name, thumbnailImage=thumbnail)
    
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
        
    #log("Adding Directory Item: " + name + " totalItems:" + str(totalItems))
    
    #dirItem = DirectoryItem()
    
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li, isFolder=isFolder, totalItems=totalItems)

def show_root_menu():

    addDirectoryItem(name=language(30111), parameters={ PARAMETER_KEY_MODE: MODE_VIEW_FUTURE }, isFolder=True)
    addDirectoryItem(name=language(30112), parameters={ PARAMETER_KEY_MODE: MODE_VIEW_HISTORY }, isFolder=True)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def get_sb_url():

    prot = xbmcplugin.getSetting(handle, "prot")
    if(prot == "0"):
        sbUrl = "http://"
    elif(prot == "1"):
        sbUrl = "https://"
        
    host = xbmcplugin.getSetting(handle, "host")
    sbUrl += host
    
    port = xbmcplugin.getSetting(handle, "port")
    sbUrl += ":" + port    
    
    sbUrl += "/api/"
    
    guid = xbmcplugin.getSetting(handle, "guid")
    
    sbUrl += guid + "/"
    
    #xbmc.log(sbUrl, 2)
    
    return sbUrl
    
def get_thumbnail_url(show_id):
 
    sbUrl = get_sb_url()
    sbUrl += "?cmd=show.getposter&tvdbid=" + str(show_id)
    
    return sbUrl
    
def view_future():

    sbUrl = get_sb_url()
    sbUrl += "future"
    
    apiResponce = urllib2.urlopen(sbUrl)
    apiDataString = apiResponce.read()
    apiResponce.close()
    #xbmc.log(apiDataString, 2)
    
    result = eval(apiDataString)
    
    data = result.get('data')
    if(data == None):
        data = []
    
    # process the missed
    missed = data.get('missed')
    if(missed == None):
        missed = []

    for item in missed:
        airDate = str(item["airdate"]) + " " + str(item["airs"])
        airTime = time.strptime(airDate, "%Y-%m-%d %A %I:%M %p")
        airTimeString = time.strftime(dateFormat, airTime)
        nameString = "Missed - " + str(item["show_name"]) + " " + str(item["season"]) + "x" + str(item["episode"]) + " - " + str(airTimeString)
        thumbnailUrl = get_thumbnail_url(item["tvdbid"])
        addDirectoryItem(nameString, parameters={ PARAMETER_KEY_MODE: MODE_VIEW_FUTURE }, isFolder=True, thumbnail=thumbnailUrl)
        
    # process the soon
    soon = data.get('soon')
    if(soon == None):
        soon = []

    for item in soon:
        airDate = str(item["airdate"]) + " " + str(item["airs"])
        airTime = time.strptime(airDate, "%Y-%m-%d %A %I:%M %p")
        airTimeString = time.strftime(dateFormat, airTime)
        nameString = "Soon - " + str(item["show_name"]) + " " + str(item["season"]) + "x" + str(item["episode"]) + " - " + str(airTimeString)
        thumbnailUrl = get_thumbnail_url(item["tvdbid"])
        addDirectoryItem(nameString, parameters={ PARAMETER_KEY_MODE: MODE_VIEW_FUTURE }, isFolder=True, thumbnail=thumbnailUrl)
        
    # process the soon
    later = data.get('later')
    if(later == None):
        later = []

    for item in later:
        airDate = str(item["airdate"]) + " " + str(item["airs"])
        airTime = time.strptime(airDate, "%Y-%m-%d %A %I:%M %p")
        airTimeString = time.strftime(dateFormat, airTime)
        nameString = "Later - " + str(item["show_name"]) + " " + str(item["season"]) + "x" + str(item["episode"]) + " - " + str(airTimeString)
        thumbnailUrl = get_thumbnail_url(item["tvdbid"])
        addDirectoryItem(nameString, parameters={ PARAMETER_KEY_MODE: MODE_VIEW_FUTURE }, isFolder=True, thumbnail=thumbnailUrl)

    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
    
def view_history():

    sbUrl = get_sb_url()
    sbUrl += "history/?limit=20"
    
    apiResponce = urllib2.urlopen(sbUrl)
    apiDataString = apiResponce.read()
    apiResponce.close()
    #xbmc.log(apiDataString, 2)
    
    result = eval(apiDataString)

    data = result.get('data')
    if(data == None):
        data = []

    for item in data:
        nameString = str(item["date"]) + " - " + str(item["show_name"]) + " " + str(item["season"]) + "x" + str(item["episode"]) + " - " + str(item["status"])
        thumbnailUrl = get_thumbnail_url(item["tvdbid"])
        addDirectoryItem(nameString, parameters={ PARAMETER_KEY_MODE: MODE_VIEW_HISTORY }, isFolder=True, thumbnail=thumbnailUrl)

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

