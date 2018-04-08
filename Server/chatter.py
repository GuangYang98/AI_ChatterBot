#!/usr/bin/python
# -*- coding: utf-8 -*-
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


chatbot.set_trainer(ListTrainer)
# import list trainers dataset
fd = open('reply.txt', 'r')
my_dataset = []
while True:
   line = fd.readline()
   if not line:
     break
   else:
     line = line[:-1]
     my_dataset.append(line)
     print(line)
 # 使用中文语料库训练它
chatbot.train(my_dataset)
 

while True:
  q = raw_input('')
  response = chatbot.get_response(q)
  print(response)
