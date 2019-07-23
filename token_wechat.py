# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import hashlib
import logging
import time
import traceback

from flask import Flask,g,request,make_response
import hashlib
import xml.etree.ElementTree as ET

import wechat_api

app = Flask(__name__)

logger=logging.getLogger(__name__) # 设置日志名称
logger.setLevel(logging.INFO) #设置日志打印等级
handler=logging.FileHandler("log.txt") # 创建日志文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')# 设置日志的打印格式
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.route("/test")
def test():
    logger.info("test成功！")
    return "test page!"


@app.route("/",methods = ["GET", "POST"])
def index():
    if request.method == "GET":  # 判断请求方式是GET请求
        my_signature = request.args.get('signature')  # 获取携带的signature参数
        my_timestamp = request.args.get('timestamp')  # 获取携带的timestamp参数
        my_nonce = request.args.get('nonce')  # 获取携带的nonce参数
        my_echostr = request.args.get('echostr')  # 获取携带的echostr参数
        token = 'shiluanzzzhahaha'  # 一定要跟刚刚填写的token一致
        # 进行字典排序
        data = [token, my_timestamp, my_nonce]
        data.sort()
        # 拼接成字符串
        temp = ''.join(data)
        temp = temp.encode('utf8')
        # 进行sha1加密
        try:
            mysignature = hashlib.sha1(temp).hexdigest()
        # 加密后的字符串可与signature对比，标识该请求来源于微信
        except:
            logger.info(traceback.format_exc())
        if my_signature == mysignature:
            logger.info("调用成功")
            return my_echostr
        else:
            logger.info("调用失败")
            return "error"
    else:
        pass
    """
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        if xml_rec.find('MsgType').text =="link":
            url = xml_rec.find('Url').text
            wechat_api.do_url(url)
            return_content = "后台已经开始代理访问链接,默认访问30次，每次随机间隔 1-10 s 。访问结果可能要一段时间后才显示。"
            xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
            response = make_response(xml_rep % (fromu, tou, str(int(time.time())), return_content))
            response.content_type = 'application/xml'
            return response
        elif xml_rec.find('MsgType').text =="text":
            content = xml_rec.find('Content').text
            if "www.maimemo.com/share/page" in content:
                wechat_api.do_url(content)
                return_content = "后台已经开始代理访问链接,默认访问30次，每次随机间隔 1-10 s 。访问结果可能要一段时间后才显示。"
            xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
            response = make_response(xml_rep % (fromu, tou, str(int(time.time())), return_content))
            response.content_type = 'application/xml'
            return response
        else:
            return_content = "出现错误~~QAQ"
            xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
            response = make_response(xml_rep % (fromu, tou, str(int(time.time())), return_content))
            response.content_type = 'application/xml'
            return response
    """
if __name__ == "__main__":
    app.run(port="8080")