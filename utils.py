import model
import sqlhelper
import json
import os

def parseJsonToObj(jsonStr):
    obj=json.loads(jsonStr,object_hook=model.JSONObject)
    return  obj

def parseObjToJson(obj):
    json_str = json.dumps(obj, default=lambda o: o.__dict__, sort_keys=False, indent=4)
    return json_str

def saveFile(filePath,content):
    try:
        with open(filePath,encoding='utf-8',mode='w') as f:
            f.write(content)
            f.close()
    except FileNotFoundError:
        os.mknod(filePath)
        f=open(filePath,'w')
        f.write(content)
        f.close()

def loadMapDataFromFile(filePath):
     with open(filePath,mode='r') as f:
            mapStr=f.read()
            return mapStr

def judgeTowerIsExist(beginTower,endTower):
    dbOp=sqlhelper.dbcrud()
    ret1=dbOp.queryData('towers','id','serialNumber='+str(beginTower))
    ret2=dbOp.queryData('towers','id','serialNumber='+str(endTower))
    if len(ret1)==0 and len(ret2)==0:
        return -2
    if len(ret1)==0:
        return -1
    if len(ret2)==0:
        return 0
    return 1

def judgeMapRouteIsExist(beginTower,endTower):
    dbOp=sqlhelper.dbcrud()
    condition='beginTower='+str(beginTower)+' and endTower='+str(endTower)
    data=dbOp.queryData('routeMaps','routeIsExist',condition)
    if len(data)>0:
        if data[0][0]<0:
            return 0
        return 1
    return -1

def preQueryMiddleTower(begin, end, preTowerList):
    dbOp = sqlhelper.dbcrud()
    towerData=[]
    counter=begin
    while(True):

        data=dbOp.queryData('towers', 'nextTower,branch01,branch02,branch03,towerType,longitude,latitude,crossLineType,serialNumber,title', 'serialNumber='+str(counter))[0]
        t = model.Tower()
        t.serialNum=data[8]
        t.nextTower=data[0]
        t.branch01=data[1]
        t.branch02=data[2]
        t.branch03=data[3]
        t.towerType=data[4]
        t.longitude=data[5]
        t.latitude=data[6]
        t.crossLineType=data[7]
        t.title=data[9]
        towerData.append(t)
        counter = data[0]
        if counter==-1:
            preTowerList.append(end)
        elif (data[1]==None):
            preTowerList.append(counter)

        if counter==-1 or data[0]==end or data[1]!=None:
            if data[1]!=None:
                break
            data = dbOp.queryData('towers',
                                  'nextTower,branch01,branch02,branch03,towerType,longitude,latitude,crossLineType,serialNumber,title',
                                  'serialNumber=' + str(end))
            data=data[0]
            t = model.Tower()
            t.serialNum = data[8]
            t.nextTower = data[0]
            t.branch01 = data[1]
            t.branch02 = data[2]
            t.branch03 = data[3]
            t.towerType = data[4]
            t.longitude = data[5]
            t.latitude = data[6]
            t.crossLineType = data[7]
            t.title=data[9]

            towerData.append(t)
            break
    return towerData

def bpQueryMiddleTower(begin, end, bpTowerList):
    dbOp = sqlhelper.dbcrud()
    towerData=[]
    counter = end
    while (True):
        data = dbOp.queryData('towers', 'preTower,branch01,branch02,branch03,towerType,longitude,latitude,crossLineType,serialNumber,title', 'serialNumber=' + str(counter))[0]
        t = model.Tower()
        t.serialNum = data[8]
        t.preTower = data[0]
        t.branch01 = data[1]
        t.branch02 = data[2]
        t.branch03 = data[3]
        t.towerType = data[4]
        t.longitude = data[5]
        t.latitude = data[6]
        t.crossLineType = data[7]
        t.title=data[9]
        towerData.append(t)
        counter = data[0]
        if counter==-1:
            bpTowerList.append(begin)
        elif data[1]==None:
            bpTowerList.append(counter)

        if data[0] == begin or data[1] != None:
            if data[1]!=None:
                break
            data = dbOp.queryData('towers',
                                  'preTower,branch01,branch02,branch03,towerType,longitude,latitude,crossLineType,serialNumber,title',
                                  'serialNumber=' + str(begin))[0]
            t = model.Tower()
            t.serialNum = data[8]
            t.nextTower = data[0]
            t.branch01 = data[1]
            t.branch02 = data[2]
            t.branch03 = data[3]
            t.towerType = data[4]
            t.longitude = data[5]
            t.latitude = data[6]
            t.crossLineType = data[7]
            t.title=data[9]
            towerData.append(t)
            break
    return towerData

def genMapSeg(towerData):
    dbOp=sqlhelper.dbcrud()
    begin=towerData[0].serialNum
    mapList=[]
    for i in range(1,len(towerData)):
        next=towerData[i].serialNum
        print("circuit  segments is consisted of tower:{0},{1}".format(begin, next))
        #query circuit by pre and next tower
        condition='(preTower='+str(begin)+' and nextTower='+str(next)+') or ( preTower='+str(next)+' and nextTower='+str(begin)+')'
        data=dbOp.queryData('circuits','serialNumber,title,type,obstacleNum,directionAngle,relativeCoord01,relativeCoord02,preTower,nextTower',condition)[0]


        #use compoundCircuit object to load
        circuit=model.Circuit(serialNumber=data[0],title=data[1],type=data[2],obstacleNum=data[3],directionAngle=data[4],relativeCoord01=data[5],relativeCoord02=data[6],preTower=data[7],nextTower=data[8])

        compoundCircuit=model.CompoundCircuit(circuit)
        mapSegment=model.CompoundMapSegment(preTower=towerData[i-1],nextTower=towerData[i],compoundCircuit=compoundCircuit)
        mapList.append(mapSegment)
        begin = next
    return mapList

def queryMiddleTower(preTowerList, bpTowerList):

    begin=preTowerList[0]
    end=bpTowerList[0]
    towerData=[]
    towerData1=preQueryMiddleTower(begin,end,preTowerList)

    #TODO will start new thread
    towerData2=bpQueryMiddleTower(begin,end,bpTowerList)
    preTowerList.reverse()

    if preTowerList==bpTowerList:
        towerData=towerData1
        print('No branch,tower query complete')
    bpTowerList.reverse()
    if preTowerList[0]==bpTowerList[0]:

        towerData2.pop()
        towerData2.reverse()
        towerData=towerData1+towerData2
        
    #construct mapSegment
    return genMapSeg(towerData)

def saveMapToDB(beginNum,endNum,title,mapData):
    serialNum=str(beginNum)+'2020'+str(endNum)
    serialNum=int(serialNum)

    routeMap=model.RouteMap(serialNumber=serialNum,title=title,beginTower=beginNum,endTower=endNum,routeIsExist=1,mapData=mapData)
    dbOp=sqlhelper.dbcrud()

    data=dbOp.queryData('routeMaps','id','serialNumber='+str(serialNum))
    if len(data)>0:
        print('current routeMap  has already exist!')
        return
    dbOp.insert2RouteMaps(routeMap)
    print('save routeMap success!')
    return

def reverseMapQuery(beginTower,endTower):
    #beginTower>endTower

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

    preTowerList = [endTower]
    bpTowerList = [beginTower]
    mapRoute = queryMiddleTower(preTowerList, bpTowerList)
    print("total circuits segment number is :", len(mapRoute))
    return backRouteMap(mapRoute)

def backRouteMap(mapLi):
    mapLi.reverse()
    for i in mapLi:
        temp=i.preTower
        i.preTower=i.nextTower
        i.nextTower=temp
        i.compoundCircuit.toolList.reverse()
    return mapLi

#get gps message from rk3399
def getGpsMsg():
    pass

#parse gps message from gps databag
def gpsMsgParse():
    pass

def calculateDisByGps():
    pass



def buildContext(objList):
    l=len(objList)
    for i in range(0,l):
        if i==0:
            objList[0].preObj=-1
            objList[0].nextObj=objList[1]
            continue
        if i==l-1:
            objList[i].preObj=objList[i-1]
            objList[i].nextObj=-1
            continue
        else:
            objList[i].preObj=objList[i-1]
            objList[i].nextObj=objList[i+1]







