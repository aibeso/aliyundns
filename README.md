# 调用阿里云域名解析的API接口实现动态DNS
通过阿里云域名解析实现动态dns并访问家庭内网
## 食用
安装依赖包(安装不上依赖的请自行解决)  
pip install -r requirements.txt  
文件依赖(否则无法通知)
__init__.py
sendNotify.py
qinglong 拉库命令：ql repo https://github.com/aibeso/aliyundns.git "Ali" "" "__init__|sendNotify|requirements" "ql"  
青龙拉库无法自动添加定时任务，自行修改
定时参数  
*/5 * * * *  
环境设置 参数  
export DNS_AKIDID = 'LTAI5t6...'      # 阿里云 AccessKey ID  
export DNS_AKSECRET = 'F3cLQb9...'    # 阿里云 AccessKey Secret  
export DNS_DOMAINNAME = 'baidu.com'   # 域名  
export DNS_RR = 'www'                 # 主机记录  
export DNS_TYPE = 'A'                 # 解析记录类型格式 ：A：IPv4地址格式  
环境设置 通知服务  
export BARK=''                   # bark服务,苹果商店自行搜索;  
export SCKEY=''                  # Server酱的SCKEY;  
export TG_BOT_TOKEN=''           # tg机器人的TG_BOT_TOKEN;  
export TG_USER_ID=''             # tg机器人的TG_USER_ID;  
export TG_API_HOST=''            # tg 代理api  
export TG_PROXY_IP=''            # tg机器人的TG_PROXY_IP;  
export TG_PROXY_PORT=''          # tg机器人的TG_PROXY_PORT;  
export DD_BOT_TOKEN=''           # 钉钉机器人的DD_BOT_ACCESS_TOKEN;  
export DD_BOT_SECRET=''          # 钉钉机器人的DD_BOT_SECRET;  
export QQ_SKEY=''                # qq机器人的QQ_SKEY;  
export QQ_MODE=''                # qq机器人的QQ_MODE;  
export QYWX_AM=''                # 企业微信；http://note.youdao.com/s/HMiudGkb  
export PUSH_PLUS_TOKEN=''        # 微信推送Plus+ ；  
