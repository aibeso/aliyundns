# 调用阿里云域名解析的API接口实现动态DNS
通过阿里云域名解析实现动态dns并访问家庭内网
## 前提
阿里云的二级域名
阿里云DNS API的访问
宽带有公网ip，（电信的没有公网ip可以打电话让运营商设置）
光猫或者路由器（看拨号的设置）可以开放外网端口
内网中有可以运行程序的条件（列入树莓派）
## 关于阿里云域名解析
域名解析免费版TTL值为10分钟，已满足家庭宽带公网ip的变换速度（基本几天才变一次）
## Python版本
Python3
##使用
保存key方法1 : 直接在同级文件夹下新建一个aliyundns.key
文件并写入 key = {"AccessKeyId": "替换你的keyid", "AccessKeySecret": "替换你的keysecret"}
保存key方法2  打开aliDNS.py，找到if __name__ == '__main__':一行的后面依照说明
#启动方法
命令行执行：python AliDNS.py

