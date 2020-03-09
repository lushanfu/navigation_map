import mysql.connector
import model
import re

class sqlObj():
    def __init__(self,host='localhost',port='3306',user='root',password='123',database='navigationMap'):
        self.__host=host
        self.__port=port
        self.__user=user
        self.__password=password
        self.__database=database

    def sqlConn(self):
        conn=mysql.connector.connect(host=self.__host,port=self.__port,user=self.__user,password=self.__password,database=self.__database)
        return conn


class sqlHelper():
    def __init__(self,dbobject):
        self.__conn=dbobject
        self.__cursor=self.__conn.cursor()
    def addData(self,sql):
        self.__cursor.execute(sql)
        self.__conn.commit()

    def deleteData(self,sql):
        


        pass
    def updateData(self,sql):
        pass
    def queryData(self,sql):
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()
    def __del__(self):
        pass
        # self.__cursor.close()
        # self.__conn.close()
        #print('xigou')

class dbcrud():
    def __init__(self):
        self.sqlO=sqlObj()
        self.sqlH=sqlHelper(self.sqlO.sqlConn())

    def insert2Towers(self,tower):
        sql='insert into towers (serialNumber,title,towerType,longitude,latitude,nextTower,crossLineType,nextLine,towerHeight,preTower) values('+str(tower.serialNum)+','+"'"+tower.title+"'"+','+str(tower.towerType)+','+str(tower.longitude)+','+str(tower.latitude)+','+str(tower.nextTower)+','+str(tower.crossLineType)+','+str(tower.nextLine)+','+str(tower.towerHeight)+','+str(tower.preTower)+')'
        self.sqlH.addData(sql)


    def insert2Circuits(self,circuit):
        sql = "insert into circuits(serialNumber,title,type,preTower,nextTower,obstacleNum,directionAngle) values("+str(circuit.serialNumber)+','+"'"+circuit.title+"',"+str(circuit.type)+','+str(circuit.preTower)+','+str(circuit.nextTower)+','+str(circuit.obstacleNum)+','+str(circuit.directionAngle)+")"
        self.sqlH.addData(sql)


    def insert2LineTools(self,lineTool):
        sql="insert into lineTools(serialNumber,title,type,longitude,latitude,lineSerialNum,preTower,nextTower,preObstacle,nextObstacle,length,cruiseFlag) value("+str(lineTool.serialNumber)+','+"'"+lineTool.title+"',"+str(lineTool.type)+','+str(lineTool.longitude)+','+str(lineTool.latitude)+','+str(lineTool.lineSerialNum)+','+str(lineTool.preTower)+','+str(lineTool.nextTower)+','+str(lineTool.preObstacle)+','+str(lineTool.nextObstacle)+','+str(lineTool.length)+','+str(lineTool.cruiseFlag)+")"
        self.sqlH.addData(sql)

    def insert2RouteMaps(self,routeMap):
        s=routeMap.mapData
        s=re.sub("\"","\\\"",s)
        routeMap.mapData=s
        sql="insert into routeMaps(serialNumber,title,routeIsExist,beginTower,endTower,mapData,distance,obstacleNum,towerNum,powerNum) value("+str(routeMap.serialNumber)+','+"'"+routeMap.title+"',"+str(routeMap.routeIsExist)+','+str(routeMap.beginTower)+','+str(routeMap.endTower)+','+"'"+str(routeMap.mapData)+"',"+str(routeMap.distance)+','+str(routeMap.obstacleNum)+','+str(routeMap.towerNum)+','+str(routeMap.powerNum)+")"
        self.sqlH.addData(sql)

    def updateTowers(self,tower,condition):
        pass
    def deleteTowers(self):
        pass
    def queryData(self,table,query=None,condition=None):
        queryCol='*'
        con='1=1'
        if query!=None:
            queryCol=query
        if condition!=None:
            con=condition
        sql='select '+queryCol+ ' from '+table+' where '+con
        return self.sqlH.queryData(sql)









