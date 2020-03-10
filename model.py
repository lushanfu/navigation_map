from enum import Enum,unique
import sqlhelper


class Tower:
    def __init__(self):
        self.serialNum=-1
        self.title=None
        self.towerType=-1
        self.longitude=-1
        self.latitude=-1
        self.preTower=-1
        self.nextTower=-1
        self.crossLineType=-1
        self.preLine=-1
        self.nextLine=-1
        self.towerHeight=-1
        self.branch01=-1
        self.branch02=-1
        self.branch03=-1
    def __repr__(self):
        return repr(self.serialNum,self.title,self.towerType,self.longitude,self.latitude,self.preTower,self.nextTower,self.crossLineType,self.preLine,self.nextLine,self.towerHeight,self.branch01,self.branch02,self.branch03)

class LineTool:
    def __init__(self,serialNumber,title = None,type=-1,longitude=-1,latitude=-1,lineSerialNum=-1,preTower=-1,nextTower=-1,preObstacle=-1,nextObstacle=-1,length=-1,cruiseFlag=-1):
        self.serialNumber = serialNumber
        self.title = title
        self.type=type
        self.longitude=longitude
        self.latitude=latitude
        self.lineSerialNum=lineSerialNum
        self.preTower=preTower
        self.nextTower=nextTower
        self.preObstacle=preObstacle
        self.nextObstacle=nextObstacle
        self.length=length
        self.cruiseFlag=cruiseFlag
    def __repr__(self):
        return repr(self.serialNumber,self.title,self.type,self.longitude,self.latitude,self.lineSerialNum,self.preTower,self.nextTower,self.preObstacle,self.nextObstacle,self.length,self.cruiseFlag)

class PointTool:
    def __init__(self):
        self.serialNumber = None
        self.title = None
        self.type = None
        self.longitude = None
        self.latitude = None
        self.lineSerialNum = None
        self.preTower = None
        self.nextTower = None
        self.preObstacle = None
        self.nextObstacle = None
        self.relativeCoord01=None
        self.relativeCoord02 = None
    def __repr__(self):
        return repr(self.serialNumber,self.title,self.type,self.longitude,self.latitude,self.lineSerialNum,self.preTower,self.nextTower,self.preObstacle,self.nextObstacle,self.relativeCoord01,self.relativeCoord02)

class Circuit:
    def __init__(self,serialNumber=-1,title = None,type = -1,preTower=-1,nextTower=-1,obstacleNum=0,directionAngle=0,relativeCoord01=-1,relativeCoord02=-1):
        self.serialNumber = serialNumber
        self.title    = title
        self.type     = type
        self.preTower = preTower
        self.nextTower= nextTower
        self.obstacleNum     =obstacleNum
        self.directionAngle  =directionAngle
        self.relativeCoord01 =relativeCoord01
        self.relativeCoord02 =relativeCoord02
    def __repr__(self):
        return repr(self.serialNumber,self.title,self.type,self.preTower,self.nextTower,self.obstacleNum,self.directionAngle,self.relativeCoord01,self.relativeCoord02)

#special navigation route
class RouteMap:
    def __init__(self,serialNumber=None,title=None,routeIsExist=None,beginTower=None,endTower=None,mapData=None,distance=0,towerNum=0,powerNum=0,obstacleNum=0):
        self.serialNumber=serialNumber
        self.title=title
        self.routeIsExist=routeIsExist
        self.beginTower=beginTower
        self.endTower=endTower
        self.mapData=mapData
        self.distance=distance
        self.towerNum=towerNum
        self.powerNum=powerNum
        self.obstacleNum=obstacleNum
    def __repr__(self):
        return repr(self.serialNumber,self.title,self.beginTower,self.endTower,self.mapData,self.distance,self.towerNum,self.powerNum,self.obstacleNum)

class CompoundCircuit:
    def __init__(self,circuit):
        self.circuit=circuit
        self.toolList=self.setAllTools()
    def __repr__(self):
        return repr(self.circuit,self.toolList)
    def setAllTools(self):
        circuitSerialNum=self.circuit.serialNumber
        toolsList=[]
        if circuitSerialNum!=-1 or circuitSerialNum!=None:
            dbOp=sqlhelper.dbcrud()
            condition='lineSerialNum='+str(circuitSerialNum)+' order by serialNumber asc'
            data =dbOp.queryData('lineTools','serialNumber,title,type,longitude,latitude,lineSerialNum,preTower,nextTower,preObstacle,nextObstacle,length,cruiseFlag',condition);
            if len(data)>0:
                for i in data:
                    tool=LineTool(serialNumber=i[0],title=i[1],type=i[2],longitude=i[3],latitude=i[4],lineSerialNum=i[5],preTower=i[6],nextTower=i[7],preObstacle=i[8],nextObstacle=i[9],length=i[10],cruiseFlag=i[11])
                    toolsList.append(tool)
        return toolsList

class CompoundMapSegment:
    def __init__(self,preTower,nextTower,compoundCircuit):
        self.preTower=preTower
        self.nextTower=nextTower
        self.compoundCircuit=compoundCircuit
        self.number=self.compoundCircuit.circuit.serialNumber

    def __repr__(self):
        return repr(self.preTower,self.nextTower,self.compoundCircuit)
#task type enum value
class TaskType(Enum):
    one=0
    two=1
    three=2
    four=3
    five=4
    six=5
    seven=6


class ObjType(Enum):
    tower=0
    lineTool01=1
    lineTool02=2
    pointTool=3


class JSONObject:
    def __init__(self, d):
     self.__dict__ = d

# GPS位置数据类型
class LocationMsg:
    def __init__(self,longitude=-1,latitude=-1):
        self.longitude=longitude
        self.latitude=latitude
    def __repr__(self):
        return repr(self.longitude,self.latitude)

#TODO GPS卫星数据类型
class GPSMsg:
    def __init__(self,GPGSV,GPGLL,GORMC,GPVTG,GPGGA,GPGSA):
        pass


class MapSegWidget:
    def __init__(self,type,name,serialNum,longitude,latitude,preObj=-1,nextObj=-1,length=-1,isPassed=False):

        self.name=name
        self.type=type
        self.serialNum=serialNum
        self.longitude=longitude
        self.latitude=latitude
        self.preObj=preObj
        self.nextObj=nextObj
        self.length=length
        self.isPassed=isPassed

#TODO 设置导航提醒的距离枚举
class NavigationRemidDis(Enum):
    arrive=0
    close=1
    near=2





