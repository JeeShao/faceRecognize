#!/usr/bin/env python
#  -- coding:utf-8 --
# #@Time  : 2017/3/22
# #@Author: Jee
'''
Created on 2017年5月7日

@author: Jee
'''

from . import config
import json
import csv
import codecs

class UserManager(object):
    '''
    classdocs
    '''
    users = []
    userIds = []
    userNames = []
    fieldNames = ['userName', 'id']
    ZhFieldNames = ['ZhName','EngName']
    
    __CSVFile = config.USERS_CSV_FILE
    __ZhCsvFile = config.ZHUSERS_CSV_FILE

    def __init__(self, csvFile=None):
        '''
        Constructor
        '''
        if csvFile != None:
            self.__CSVFile = csvFile
            self.__ZhCsvFile = __ZhCsvFile
        
    def hasUser(self, user):
        if type(user) is str:
            userNames = self.getAllUserName()
            if userNames.__contains__(user):
                return True
        elif type(user) is int:
            userIds = self.getAllUserId()
            if userIds.__contains__(str(user)):
                return True
            
        return False
                
    def addUser(self, name):
        if self.hasUser(name):
            return False
        else:
            userIds = self.getAllUserId()
            if userIds == []:
                newId = 1
            else:
                userIds.sort()
                newId = int(userIds[len(userIds)-1]) + 1
            newUser = {'userName':name, 'id':str(newId)}
            self.users.append(newUser)
            
            self.writeCSV(newUser)
            
            return newId
        
#         
    def changeUserName(self, old, new):
        if self.hasUser(old):
            userNames = self.getAllUserName()
            index = userNames.index(old)
            self.users[index]['userName'] = str(new)
            self.writeCSV(self.users)
            return True
        else:
            return False
#         
    def setCSVFile(self, fileName):
        self.__CSVFile = fileName
#         
    def getUserByName(self, name):
        self.readCSV()
        for user in self.users:
            if user['userName'] == name:
                return user
#         
    def getUserById(self, id):
        self.readCSV()
        for user in self.users:
            if int(user['id']) == id:
                return user

    def getAllUser(self):
        self.readCSV()
        return self.users
#         
    def getAllUserName(self):
        self.readCSV()
        return self.userNames
#         
    def getAllUserId(self):
        self.readCSV()
        return self.userIds
            
    def readCSV(self):
        self.csvIn = open(self.__CSVFile, 'rb')
        self.reader = csv.DictReader(codecs.iterdecode(self.csvIn, 'utf-8'), self.fieldNames)
        self.users = []
        self.userIds = []
        self.userNames = []
        for row in self.reader:
            self.users.append(row)
            self.userIds.append(int(row['id']))
            self.userNames.append(row['userName'])
        self.csvIn.close()

    def writeCSV(self, data):
        if type(data) is list:
            self.csvOut = open(self.__CSVFile, 'w', newline='')
            self.writer = csv.DictWriter(self.csvOut, self.fieldNames)
            self.writer.writerows(data)
            self.csvOut.close()
            
        elif type(data) is dict:
            self.csvOut = open(self.__CSVFile, 'a',newline='')
            self.writer = csv.DictWriter(self.csvOut, self.fieldNames)
            # print('user append')
            self.writer.writerow(data)
            self.csvOut.close()
        
    def __readJSON(self):
        self.jsonIn = open(self.__JSONFile, 'rb')
        self.users = json.loads(self.jsonIn.read())

    def __writeJSON(self, data):
        if type(data) is list:
            self.jsonOut = open(self.__CSVFile, 'wb')

        elif type(data) is dict:
            pass

    #一下函数处理中文用户名的csv文件
    def readZhCSV(self):
        self.zhCsvIn = open(self.__ZhCsvFile, 'rb')
        self.reader = csv.DictReader(codecs.iterdecode(self.zhCsvIn, 'gbk'), self.ZhFieldNames)
        self.ZhUsers = []
        self.userZhName = []
        self.userEngName = []
        for row in self.reader:
            self.ZhUsers.append(row)
            self.userZhName.append(row['ZhName'])
            self.userEngName.append(row['EngName'])
        self.zhCsvIn.close()

    def writeZhCSV(self, data):
        if type(data) is list:
            self.csvOut = open(self.__ZhCsvFile, 'w', newline='')
            self.writer = csv.DictWriter(self.csvOut, self.ZhFieldNames)
            self.writer.writerows(data)
            self.csvOut.close()

        elif type(data) is dict:
            self.csvOut = open(self.__ZhCsvFile, 'a', newline='')
            self.writer = csv.DictWriter(self.csvOut, self.ZhFieldNames)
            # print('user append')
            self.writer.writerow(data)
            self.csvOut.close()

    def addZhUser(self, name):
        if self.hasZhUser(name):
            return False
        else:
            userEngNames = self.getAllZhUserEngName()
            if userEngNames == []:
                newId = "%02d"%1
            else:
                userEngNames.sort(key=lambda x:int(x.split('_')[1]))
                newId = "%02d"%(int(userEngNames[len(userEngNames)-1].split('_')[1])+1)
            newZhUser = {'ZhName': name, 'EngName': str('zh_%s'%newId)}
            self.ZhUsers.append(newZhUser)

            self.writeZhCSV(newZhUser)
            return str('zh_%s'%newId)

    def hasZhUser(self, user):
        zhUserNames = self.getAllZhUserZhName()
        if zhUserNames.__contains__(user):
            return True
        else:
            return False

    def getAllZhUser(self):
        self.readZhCSV()
        return self.ZhUsers

    def getAllZhUserZhName(self):  #获取所有中文名
        self.readZhCSV()
        return self.userZhName

    def getAllZhUserEngName(self): #获取所有英文名
        self.readZhCSV()
        return self.userEngName

    def getZhNamebyEngName(self,EngName):  #通过英文名获取中文名
        self.readZhCSV()
        for ZhUser in self.ZhUsers:
            if ZhUser['EngName'] == EngName:
                return ZhUser['ZhName']

    def getEngNamebyZhName(self, ZhName):  # 通过中文名获取英文
        self.readZhCSV()
        for ZhUser in self.ZhUsers:
            if ZhUser['ZhName'] == ZhName:
                return ZhUser['EngName']
