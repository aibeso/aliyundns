# -*- coding: utf8 -*-
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient
import re, time, datetime
import requests, json
import random


# 说明为什么用解析记录列表的api，而不是用获取解析记录信息的api
# 因为后面使用的recordid需要从API中获取，无法从阿里云控制台直接查询到
# 解析记录列表的api可以得到recordid，在修改解析记录信息的时候需要使用
# 而获取解析记录信息的api需要recordid
# 获取二级域名的解析IP
def get_alidns_ip(vals):
    # 获取阿里云dns的解析列表
    req = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    req.set_RRKeyWord(vals["RR"])
    req.set_DomainName(vals["domainname"])
    res = client.do_action_with_exception(req)

    rec = json.loads(res.decode('utf-8'))
    ip = rec['DomainRecords']['Record'][0]['Value']
    recordid = rec['DomainRecords']['Record'][0]['RecordId']
    print('recordid=' + recordid)
    print('aliyun_ip: ' + ip)
    return ip, recordid


# 修改二级域名的解析IP
def write_alidns_ip(vals):
    req = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    req.set_RecordId(vals["recordId"])
    req.set_RR(vals["RR"])
    req.set_Type(vals["type"])
    req.set_Value(vals["ip"])
    res = client.do_action_with_exception(req)
    rec = json.loads(res.decode('utf-8'))
    print(rec)
    return rec


def open_url(url):
    response = requests.get(re, timeout=10)
    code = response.status_code
    rec = response.text
    if rec and response.status_code == 200:
        return rec


# 前提：宽带是公网ip
# 获取当前宽带的外网IP
def get_now_ip():
    urls = {
        'url1': 'http://ip.42.pl/raw',
        'url2': 'https://api.ipify.org/',
        'url3': 'http://httpbin.org/ip',
        'url4': 'http://jsonip.com'
    }
    i = random.randint(1, 4)
    print('i' + str(i))
    if i == 1:
        try:
            response = requests.get(urls.get('url1'), timeout=10)
            ip = response.text
            if ip and response.status_code == 200:
                return ip
        except:
            print('url1 timeour')
            i = i + 1

    if i == 2:
        try:
            response = requests.get(urls.get('url2'), timeout=10)
            ip = response.text
            if ip and response.status_code == 200:
                return ip
        except:
            print('url2 timeour')
            i = i + 1
    if i == 3:
        try:
            response = requests.get(urls.get('url3'), timeout=10)
            ip = eval(response.text).get('origin')
            if ip and response.status_code == 200:
                return ip
        except:
            print('url3 timeour')
            i = i + 1

    if i == 4:
        i = 0
        try:
            response = requests.get(urls.get('url3'), timeout=10)
            ip = eval(response.text).get('ip')
            if ip and response.status_code == 200:
                return ip
        except:
            print('url4 timeour')
            return None


if __name__ == '__main__':
    # https: // ram.console.aliyun.com / users
    # 需要从阿里云控制台创建用户AccessKey并设置RAM访问控制授权，建议只设置dns的管理权，
    # 获取的AccessKey填入key的json变量中
    # 建议用json格式写入文件中，需要时从文件中读取
    key = {"AccessKeyId": "111111", "AccessKeySecret": "1111111"}
    file = "./aliyundns.key"
    # 以json字符串格式写入文件中
    # with open(file, 'w') as f:
    #    json.dump(key, f)
    #    f.close()
    # 读取文件内容到json变量中
    with open(file, 'r') as f:
        key = json.load(f)
        f.close()
    # 云解析 DNS文档链接
    # https://help.aliyun.com/product/29697.html?spm=a2c4g.11186623.6.540.21ff8dca7WMg1L
    client = AcsClient(key["AccessKeyId"], key["AccessKeySecret"])
    # 通过阿里云控制台设置二级域名，https://dns.console.aliyun.com，并获取一下参数
    # vals = {"domainname": 域名,"RR": 二级域名前缀,"type": "A","ip": "本地宽带公网IP，通过其他网站实时获取", "recordId": "解析记录的ID ，此参数在添加解析时会返回，在获取域名解析列表时会返回"}
    vals = {
        "domainname": "aibeso.com",
        "RR": "me",
        "type": "A",
        "ip": "",
        "recordId": ""
    }
    error = False
    regx = re.compile(r'(\d{1,3}.){3}(\d{1,3})$')
    print('初始ip: ' + str(get_now_ip()))
    vals['ip'], vals['recordId'] = get_alidns_ip(vals)

    while (1):
        time.sleep(2)
        new_ip = get_now_ip()
        if new_ip == None:
            time.sleep(100)
            continue
        res = regx.match(new_ip)
        if not res:
            continue

        print(new_ip)

        if new_ip != vals['ip']:
            try:
                vals['ip'] = new_ip
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 更换IP')
                write_alidns_ip(vals)
                vals['ip'], vals['recordId'] = get_alidns_ip(vals)
            except:
                print('error')
                error = True
                time.sleep(10)

        if not error:
            error = False
            time.sleep(100)