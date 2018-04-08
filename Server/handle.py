# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree

import binascii

save=[];

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
chatbot = ChatBot("ChineseChatBot",
    logic_adapters={
       "chatterbot.logic.MathematicalEvaluation",
        "chatterbot.logic.TimeLogicAdapter",
        'chatterbot.logic.BestMatch'
    },
    database='./db.sqlite3')

class Handle(object):

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "rabbit2018" #请按照公众平台官网\基本配置中信息填写
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def POST(self):        
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        if msgType == 'event':
            if xml.find("Event").text == 'subscribe':#关注的时候的欢迎语
                return self.render.reply_text(fromUser, toUser, int(time.time()), u"你好，我是AIQuiz，在这里你可以直接向我提问通信电子线路的问题~")
        if msgType == 'text':
            content = xml.find("Content").text#获取学生发来的消息
            response=chatbot.get_response(content)#从聊天机器人获取回复
            print(response.confidence)#显示对于回复的自信程度
            if response.confidence<0.2:#如果不自信
                f=open('question.txt','a')#追加问题到文本中
                f.write(content)
                f.write('\n')
                f.close()
                return self.render.reply_text(fromUser, toUser, int(time.time()), u"啊列~这道题我不会，我帮你去问老师吧~要不你明天再来问问试试？")
                #return self.render.reply_text("oDvpr1u1filxU2aUotUOQI04MGDg", toUser, int(time.time()), u"有人不会做题，快去回答~")
            else:
                return self.render.reply_text(fromUser, toUser, int(time.time()), response)
