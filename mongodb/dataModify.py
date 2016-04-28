__author__ = 'xiaxuan'
# coding:utf-8
import pymongo

online = {
    "host": '10.10.50.57',
    "port": 27017,
    "database": 'files',
    "username": '',
    "password": ''
}

test = {
    "host": '103.235.225.39',
    "port": 27021,
    "database": "files",
    "username": '',
    "password": ''
}

config = test
mongo = pymongo.MongoClient(config.get('host'), int(config.get('port')))
database = mongo.files


# 获取数据库
def getdatabase():
    return database


# 关闭mongo连接
def closemongoclent():
    mongo.close()

