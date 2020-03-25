# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 00:23:22 2018

@author: bana-titech
"""

import json
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない

class Data:
    users = dict()
    require = 10000 #必要金額
    sum = 0; #募金総額
    path = 'lib/data.json' #データ保存用ファイル

#username:String money:int
def useradd(username,money):
    r = open(Data.path,"r",encoding="utf-8")
    Data.users = json.loads(r.read())
    if username not in Data.users:
        Data.users[username] = money
    else:
        Data.users[username] = Data.users[username] + money
    Data.sum = 0
    for user in Data.users:
        Data.sum = Data.sum + Data.users[user]
    w = open(Data.path,'w',encoding="utf-8")
    json.dump(Data.users,w)
    

@respond_to('(-?\d+)円寄付')
def add_func(message, something):
    send_user = message.channel._client.users[message.body['user']][u'name']
    if int(something)>0:
        useradd(send_user,int(something))
        message.reply(send_user+'により+{0}円します！ありがとう！'.format(something))
    elif int(something)<0:
        useradd(send_user,int(something))
        message.reply(send_user+'により{0}円します...悲しい...'.format(something))
    else:
        message.reply('？')
    message.reply('現在合計'+str(Data.sum)+'円です！')
    if Data.require > Data.sum:
    	message.reply('目標金額'+str(Data.require)+'円まであと'+str(Data.require-Data.sum)+'円')
    else:
        message.reply('目標金額達成！'+str(Data.sum-Data.require)+'円オーバーしてます!')

@respond_to('現在の寄付総額')
def sum_func(message):
    r = open(Data.path,"r",encoding="utf-8")
    Data.users = json.loads(r.read())
    for user in Data.users:
        message.reply(user+"さんが"+str(Data.users[user])+"円寄付")
    Data.sum = 0
    for user in Data.users:
        Data.sum = Data.sum + Data.users[user]
    message.reply("合計"+str(Data.sum)+"円寄付されています！")
    if Data.require > Data.sum:
    	message.reply('目標金額'+str(Data.require)+'円まであと'+str(Data.require-Data.sum)+'円')
    else:
        message.reply('目標金額達成！'+str(Data.sum-Data.require)+'円オーバーしてます!')

@respond_to('目標金額')
def require_func(message):
    message.reply('目標金額は'+str(Data.require)+'円です！')