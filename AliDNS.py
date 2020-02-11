from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient
import json
import time, datetime
import re
import requests
import random


class AliDNS :
    client = None
    domainname = 'aibeso.com'
    RR = 'wx'
    type = 'A'
    ali_ip = None
    record_id = None
    describe_request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    update_request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()


    def __init__(self):
        self.create_client(self.read_access_key())
        self.get_alidns_ip()

    # key = {"AccessKeyId": "111111", "AccessKeySecret": "1111111"}
    def read_access_key(self, file_name="./aliyundns.key"):
        # 读取文件内容到json变量中
        with open(file_name, 'r') as f:
            key = json.load(f)
            f.close()
            return key

    # key = {"AccessKeyId": "111111", "AccessKeySecret": "1111111"}
    def write_access_key(self, file_name, key):
        # 以json字符串格式写入文件中
        with open(file_name, 'w') as f:
           json.dump(key, f)
           f.close()

    # key = {"AccessKeyId": "111111", "AccessKeySecret": "1111111"}
    # 创建访问阿里云的客户端
    def create_client(self, key):
        self.client = AcsClient(key["AccessKeyId"], key["AccessKeySecret"])

    # 说明: 为什么用解析记录列表的api，而不是用获取解析记录信息的api
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
        print('recordid=' + self.record_id)
        print('aliyun_ip: ' + self.ali_ip)

    # 修改二级域名的解析IP
    def write_alidns_ip(self, ip):
        request = self.update_request
        request.set_RecordId(self.record_id)
        request.set_RR(self.RR)
        request.set_Type(self.type)
        request.set_Value(ip)
        res = self.client.do_action_with_exception(request)
        rec = json.loads(res.decode('utf-8'))
        if(rec.get('RecordId') == self.record_id):
            self.ali_ip = ip
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 更换IP:' + str(ip))
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
    flag = 1
    while(flag):
        url = random.choice(list(urls))
        key = urls.get(url)
        # print(key + url)
        res = get_html_text(url)
        if res != None:
            ip = ''
            if(key != 'None'):
                ip = eval(res).get(key)
            else:
                ip = res
            if(check_ip(ip)):
                return ip
        else:
            flag = flag + 1
            if flag % 3 == 0:
                print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "    网络请求连续出错：" + str(flag))
                time.sleep(60)

# 爬取网页内容
def get_html_text(url):
    try:
        response = requests.get(url, timeout=10)
        rec = response.text
        if rec and response.status_code == 200:
            return rec
        else:
            return None
    except:
        print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "    网络请求出错：" + url)
        return None

# 正则检查IP是否正确
def check_ip(ip):
    regx = re.compile(r'(\d{1,3}.){3}(\d{1,3})$')
    res = regx.match(ip)
    if not res:
        return False
    else:
        return True

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    alinds = AliDNS()
    print('local_IP：' + get_local_ip())
    while(1):
        ip = get_local_ip()
        if alinds.ali_ip != ip:
            try:
                alinds.write_alidns_ip(ip)
                d = datetime.datetime.now() - start_time
                print(str(d.days) + 'D  ' + str(d.seconds // 3600) + ':' + str(d.seconds % 3600 // 60))
                start_time = datetime.datetime.now()
            except Exception as ex:
                print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "    " + ex)
        else:
            # 每隔10分钟输出一次IP地址()
            if datetime.datetime.now().minute % 10 == 0:
                print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '    当前IP：' + alinds.ali_ip)
            # 休眠59秒时间，不用频繁的消耗资源
            time.sleep(59)

