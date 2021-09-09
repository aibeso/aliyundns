#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
'''
[task_local]
# 阿里云DDNS
# qinglong 无法识别定时任务，自行添加
 */2 * * * * AliDNS.py
 cron "*/2 * * * *"
 cron: "*/2 * * * *"
 new Env('DDNS');

Env环境设置 参数
export DNS_AKIDID = 'LTAI5t6...'  # 阿里云 AccessKey ID
export DNS_AKSECRET = 'F3cLQb9...'  # 阿里云 AccessKey Secret
export DNS_DOMAINNAME = 'baidu.com'  # 域名
export DNS_RR = 'www'  # 主机记录
export DNS_TYPE = 'A'  # 解析记录类型格式 ：A：IPv4地址格式
Env环境设置 通知服务
export BARK=''                   # bark服务,苹果商店自行搜索;
export SCKEY=''                  # Server酱的SCKEY;
export TG_BOT_TOKEN=''           # tg机器人的TG_BOT_TOKEN;
export TG_USER_ID=''             # tg机器人的TG_USER_ID;
export TG_API_HOST=''            # tg 代理api
export TG_PROXY_IP=''            # tg机器人的TG_PROXY_IP;
export TG_PROXY_PORT=''          # tg机器人的TG_PROXY_PORT;
export DD_BOT_TOKEN=''           # 钉钉机器人的DD_BOT_TOKEN;
export DD_BOT_SECRET=''          # 钉钉机器人的DD_BOT_SECRET;
export QQ_SKEY=''                # qq机器人的QQ_SKEY;
export QQ_MODE=''                # qq机器人的QQ_MODE;
export QYWX_AM=''                # 企业微信；http://note.youdao.com/s/HMiudGkb
export PUSH_PLUS_TOKEN=''        # 微信推送Plus+ ；
'''

import os
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient
from time import *
import json
import datetime
import re
import requests
import random

class AliDNS :

    AccessKeyId = None
    AccessKeySecret = None
    domainname = 'baidu.com'  # 顶级域名
    RR = 'www'  # 主机记录
    type = 'A'  # 解析记录类型格式 ：A：IPv4地址格式

    describe_request = None
    update_request = None
    client = None
    record_id = None  # 解析记录的ID
    ali_ip = None  # 正在解析到的ip
    local_ip = None  # 本地ip地址

    def __init__(self):
        # 读取系统配置参数
        if "DNS_AKIDID" in os.environ and os.environ["DNS_AKIDID"]:
            self.AccessKeyId = os.environ["DNS_AKIDID"]

        if "DNS_AKSECRET" in os.environ and os.environ["DNS_AKSECRET"]:
            self.AccessKeySecret = os.environ["DNS_AKSECRET"]

        if "DNS_DOMAINNAME" in os.environ and os.environ["DNS_DOMAINNAME"]:
            self.domainname = os.environ["DNS_DOMAINNAME"]

        if "DNS_RR" in os.environ and os.environ["DNS_RR"]:
            self.RR = os.environ["DNS_RR"]

        if "DNS_TYPE" in os.environ and os.environ["DNS_TYPE"]:
            self.type = os.environ["DNS_TYPE"]
        #  初始化
        self.describe_request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        self.update_request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        try:
            self.client = AcsClient(self.AccessKeyId, self.AccessKeySecret)
        except:
            print("阿里云AccessKey没有配置或配置不正确！")

    # 说明: 用为什么用解析记录列表的api，而不是获取解析记录信息的api
    # 因为后面使用的recordid需要从API中获取，无法从阿里云控制台直接查询到
    # 解析记录列表的api可以得到recordid，在修改解析记录信息的时候需要使用
    # 而获取解析记录信息的api需要recordid
    #
    # 获取二级域名的解析IP=
    def get_alidns_ip(self):
        # 获取阿里云dns的解析列表
        request = self.describe_request
        request.set_RRKeyWord(self.RR)
        request.set_DomainName(self.domainname)
        res = self.client.do_action_with_exception(request)
        rec = json.loads(res.decode('utf-8'))
        self.ali_ip = rec['DomainRecords']['Record'][0]['Value']
        self.record_id = rec['DomainRecords']['Record'][0]['RecordId']
        print('原ddns解析IP是: ' + self.ali_ip)

    # 修改二级域名的解析IP
    def write_alidns_ip(self):
        request = self.update_request
        request.set_RecordId(self.record_id)
        request.set_RR(self.RR)
        request.set_Type(self.type)
        request.set_Value(self.local_ip)
        res = self.client.do_action_with_exception(request)
        rec = json.loads(res.decode('utf-8'))
        if(rec.get('RecordId') == self.record_id):
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "域名：" + self.RR + "." + self.domainname + "\n更换IP:" + str(ip))
            try:
                from sendNotify import Send
                msg = Send()
                message = "域名：" + self.RR + "." + self.domainname + "\nIP更换：" +self.ali_ip + " --> " + self.local_ip + '\n\n开源免费By: https://github.com/aibeso/aliyundns/tree/ql';
                msg.send("DDNS解析变更通知", "域名：" + message)
            except:
                print("发起通知失败！")
        else:
            print("未知错误，请检查当前域名解析地址是否正确！")

# 前提：宽带是公网ip
# 获取当前宽带的外网IP
def get_local_ip():
    # url链接 : 获取的json文本中的key， None表示直接返回的时IP地址字符串
    urls = {
        'http://ip.42.pl/raw': 'None',
        'https://api.ipify.org/': 'None',
        'http://httpbin.org/ip': 'origin',
        'http://jsonip.com': 'ip'
    }
    for i in range(4):
        url = random.choice(list(urls))
        key = urls.get(url)
        try:
            response = requests.get(url, timeout=10)
            rec = response.text
            if rec and response.status_code == 200:
                ip = ''
                if (key != 'None'):
                    ip = eval(rec).get(key)
                else:
                    ip = rec

                regx = re.compile(r'(\d{1,3}.){3}(\d{1,3})$')
                res = regx.match(ip)
                if res:
                    return ip
        except:
            print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "第" + (i+1) +"次获取公网IP请求出错：" + url)

    return None




if __name__ == '__main__':
    start_time = time()
    print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " 开始运行DDNS")
    ddns = AliDNS()
    ddns.get_alidns_ip()
    ip = get_local_ip()
    if ddns.ali_ip != ip:
        ddns.local_ip = ip
        ddns.write_alidns_ip()
    print("本次运行结束：耗时： " + str(time() - start_time))
