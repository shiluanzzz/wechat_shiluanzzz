# -*- coding:utf-8 -*-
# __author__ = "shitou6"
# https://werobot.readthedocs.io/zh_CN/latest/
import xinfulanhai
import werobot

robot=werobot.WeRoBot(token="shiluanzzzhahaha")
robot.config['APP_ID']="wx807f81802902b5dd"
robot.config['APP_SECRET']="e242257c7732823e03efbb6ef2e72940"

client=robot.client

@robot.text
def button1(message):
    if "会员" in message.content:
        try:
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
        except:
            return "会员查询功能出错QAQ"
    elif "测试" in message.content:
        msg="message_id:{}\n" \
            "target:{}\n" \
            "source:{}\n" \
            "content:{}\n".format(message.message_id,message.target,message.source,message.content)
        return msg
    else:
        return "目前只开放会员查询功能~"
# @robot.image 修饰的 Handler 只处理图片消息
@robot.image
def img(message):
    return message.img


if __name__ == '__main__':
    robot.config['HOST'] = '0.0.0.0'
    robot.config['PORT'] = 8000
    robot.run()
