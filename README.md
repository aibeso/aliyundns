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
