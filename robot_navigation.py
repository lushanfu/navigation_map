from utils import *
mapLi=[]

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

def navigation(navigationFlag):
    global mapLi

    #get realtime robot  location information
    L=len(mapLi)
    if L < 1:
        print("navigation_map is empty,please generator corresponding map data")
        return -1
    i=0
    passedObj=[]
    while(navigationFlag):

        mapSeg=mapLi[i]#type
        objList=[]
        if(len(mapSeg.compoundCircuit.toolList)<1):
            pre = model.MapSegWidget(type=model.ObjType.tower, name=mapSeg.preTower.title,serialNum=mapSeg.preTower.serialNum,
                                     longitude=mapSeg.preTower.longitude, latitude=mapSeg.preTower.latitude)  #

            end = model.MapSegWidget(type=model.ObjType.tower, name=mapSeg.nextTower.title,serialNum=mapSeg.endTower.serialNum,
                                     longitude=mapSeg.nextTower.longitude, latitude=mapSeg.nextTower.latitude)
            objList.append(pre)
            objList.append(end)
        else:
            pre = model.MapSegWidget(type=model.ObjType.tower, name=mapSeg.preTower.title,serialNum=mapSeg.preTower.serialNum,
                                     longitude=mapSeg.preTower.longitude, latitude=mapSeg.preTower.latitude)

            end = model.MapSegWidget(type=model.ObjType.tower, name=mapSeg.nextTower.title,serialNum=mapSeg.nextTower.serialNum,
                                     longitude=mapSeg.nextTower.longitude, latitude=mapSeg.nextTower.latitude)
            objList.append(pre)
            for i in mapSeg.compoundCircuit.toolList:
                if i.type==3:
                    obj = model.MapSegWidget(type=model.ObjType.pointTool, name=i.title, serialNum=i.serialNumber,
                                             longitude=mapSeg.preTower.longitude, latitude=mapSeg.preTower.latitude,
                                             preObj=-1,
                                             nextObj=mapSeg.compoundCircuit.toolList[0], length=-1)
                elif i.type==2:
                    obj = model.MapSegWidget(type=model.ObjType.lineTool02, name=i.title, serialNum=i.serialNumber,
                                             longitude=mapSeg.preTower.longitude, latitude=mapSeg.preTower.latitude,
                                             preObj=-1,
                                             nextObj=mapSeg.compoundCircuit.toolList[0], length=-1)
                else:
                    obj = model.MapSegWidget(type=model.ObjType.lineTool01, name=i.title, serialNum=i.serialNumber,
                                             longitude=mapSeg.preTower.longitude, latitude=mapSeg.preTower.latitude,
                                             preObj=-1,
                                             nextObj=mapSeg.compoundCircuit.toolList[0], length=-1)

                objList.append(obj)
            objList.append(end)
        buildContext(objList)
        for obj in range(0,len(objList)):
            if obj==0:
                passedObj.append(objList[obj])
                continue
            #calculate distance of robot  and object
            while(True):
                robotLoc=gpsMsgParse()
                dis=calculateDisByGps()
                if dis<=2:#当机器人与障碍物的距离小于两米的时候，交由视觉来处理。
                    #TODO 当机器人与障碍物距离到达一定阈值时候，进行视觉辅助，导航不再处理（通知下个障碍物的距离，及三米范围为障碍物的个数）。
                    break



        i+=1





    #query from mapData and calculate the location on  the map

    #navigation_tip

    pass

def mapUpdate():
    pass


mapLi=routeQuery(7,2)
navigation(True)

offLineMapLoad('/home/lsf/map.txt')
pass
