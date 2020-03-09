from utils import *


def routeQuery(beginTower,endTower):

    ret=judgeMapRouteIsExist(beginTower,endTower)
    mapRoute=[]
    if ret>=0:
        if ret==0:
            print('current navigationDestination no route')
            return mapRoute
        #TODO query map from db  and convert jsonStr to object
        pass
    else:
      if beginTower < endTower:
        flag = judgeTowerIsExist(beginTower, endTower)
        if flag == -2:
            print("Check again,and input right beingTowerSerialNumber and endTowerSerialNumber please!")
            return
        if flag == -1:
            print("Check again,and input right beingTowerSerialNumber please!")
            return
        if flag == 0:
            print("Check again,and input right endTowerSerialNumber please!")
            return
        # query all tower by input beginTower and endTower
        # difined a pre and bp list

        preTowerList = [beginTower]
        bpTowerList = [endTower]
        mapRoute = queryMiddleTower(preTowerList, bpTowerList)
        print("total circuits segment number is :", len(mapRoute))
      else:
       mapRoute=reverseMapQuery(beginTower,endTower)

    return mapRoute

#load mapdata from local sd
def offLineMapLoad(filePath):
    mapStr=loadMapDataFromFile(filePath)
    obj=parseJsonToObj(mapStr)
    return obj

#recify exist routeMap
def rectifyRoute():
    pass


def mapDownload(filePath,content=''):
    filePath=filePath+'/map.txt'
    saveFile(filePath,content)

def taskDownload():
    pass

def geographicMark():

    pass

def navigation():

    #get realtime robot  location information

    #query from mapData and calculate the location on  the map

    #navigation_tip

    pass

def mapUpdate():
    pass


mapLi=routeQuery(7,2)
backRouteMap(mapLi)
# jsonStr=parseObjToJson(mapLi)
# saveMapToDB(1,7,'second_map',jsonStr)
# parseJsonToObj(jsonStr)
#print(jsonStr)

#mapDownload('/home/lsf',jsonStr)
offLineMapLoad('/home/lsf/map.txt')
pass
