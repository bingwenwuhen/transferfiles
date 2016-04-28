__author__ = 'xiaxuan'
# coding:utf-8
from mongodb import dataModify
import requests
from greenlet import greenlet
from rabbitmq import message
import time


config = {
    'url': 'http://static.weibangong.com/files/'
}

cfg = config
database = dataModify.getdatabase()


# 将成功的写到文件中
def writesuccess(data):
    f = open('./download.txt', 'a')
    f.write(str(data.get('_id')) + '\n')
    f.close()


# 将失败的写到文件中
def writefailed(data):
    f = open('./failed.txt', 'a')
    f.write(str(data.get('_id')) + '\n')
    f.close()


# 将成功的url发送到消息队列中
def sendmessage(url):
    message.send(body=str(url))


# 用于检测失败的文件中url
def checkfailed():
    f = open('./failed.txt', 'r+')
    list = f.readlines()
    # 每次需要清空文件
    f.truncate()
    for data in list:
        r = requests.get(cfg.get('url') + str(data.get('_id')))
        if r.status_code != 200:
            grfailed = greenlet(writefailed)
            grfailed.switch(data)
        else:
            grsuccess = greenlet(writesuccess)
            grsuccess.switch(data)
            grsend = greenlet(sendmessage)
            grsend.switch(str(data.get('_id')))
            print str(data.get('_id')) + ' done'
        time.sleep(2)
    f.close()


file = open('./count.txt', 'r+')
start = file.readline()
num = 200000

if start == '':
    start = 0
    file.write(str(200000))
else:
    start = int(start)
    file.write(str(start + 200000))
file.close()

# 先检测failed.txt文件中是否有内容
checkfailed()

count = database.FileMetaData.find().count()
if start < count:
    try:
        list = database.FileMetaData.find().skip(start).limit(num)
        for data in list:
            r = requests.get(cfg.get('url') + str(data.get('_id')))
            if r.status_code != 200:
                grfailed = greenlet(writefailed)
                grfailed.switch(data)
            else:
               grsuccess = greenlet(writesuccess)
               grsuccess.switch(data)
               grsend = greenlet(sendmessage)
               grsend.switch(str(data.get('_id')))
               print str(data.get('_id')) + ' done'
            time.sleep(2)
    except Exception as err:
        print err
    finally:
        message.close()

