# -*- coding:utf-8 -*-
# __author__ = "shitou6"
# https://werobot.readthedocs.io/zh_CN/latest/
from werobot import WeRoBot

import xinfulanhai

robot=WeRoBot(token="shiluanzzzhahaha")
robot.config['APP_ID']="wx807f81802902b5dd"
robot.config['APP_ID']="e242257c7732823e03efbb6ef2e72940"

client = robot.client
client.create_menu({
    "button":[{
         "type": "click",
         "name": "会员场查询",
         "key": "button1"
    },{
         "type": "click",
         "name": "按钮2",
         "key": "button2"
    },{
         "type": "click",
         "name": "按钮3",
         "key": "button3"
    },
    ]
})
@robot.key_click("button1")
def button1(message):
    send_message=""
    now_data = xinfulanhai.find_vip_movie()
    send_message+="正在查询会员场电影信息"
    send_message = ""
    for each in now_data:
        ss = str(each).split('|')
        send_message += '电影名称:' + ss[0] + '\n'
        send_message += '时间：' + ss[1] + '\n'
        send_message += '信息：' + ss[2] + '\n'
        send_message += "---------------------------\n"
        send_message += "****打印完毕****"
    return send_message
@robot.key_click("button2")
def button1(message):
    return "点击 button2"
@robot.key_click("button3")
def button1(message):
    return "点击 button3"

@robot.text
def echo(message):
    return message.content

# @robot.image 修饰的 Handler 只处理图片消息
@robot.image
def img(message):
    return message.img


if __name__ == '__main__':
    robot.config['HOST'] = '0.0.0.0'
    robot.config['PORT'] = 8000
    robot.run()