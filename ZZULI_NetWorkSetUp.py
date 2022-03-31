# -- coding: utf-8 --
import re
import json
import requests
import urllib.request
from urllib.parse import urlencode
from urllib.request import Request
# 尝试并连接wifi
from os import system
import pywifi
import time

def FileWrite(name, word):
    file = open(name, mode='a+')
    file.write(word)
    file.close()

def WifiConnect():
    wifi = pywifi.PyWiFi()  # 创建一个无线对象
    ifaces = wifi.interfaces()[0]  # 取一个无限网卡
    print(ifaces.name())  # 输出无线网卡名称
    ifaces.disconnect()  # 断开网卡连接
    time.sleep(0.5)  # 缓冲0.5秒

    profile = pywifi.Profile()  # 配置文件
    profile.ssid = "zzuli-student"  # wifi名称
    # ifaces.remove_all_network_profiles()  # 删除其他配置文件
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件
    ifaces.connect(tmp_profile)  # 连接
    time.sleep(0.5)  # 等待0.5秒后看下是否成功连接了
    while(not isConnected(ifaces)):
        time.sleep(5)  # 若未成功，等待5秒后再看下是否成功连接了
        if not isConnected(ifaces):
            # 若未成功，重连
            WifiConnect()

def isConnected(ifaces):
    if ifaces.status() == pywifi.const.IFACE_CONNECTED:
        print("成功连接")
        return True
    else:
        print("失败")
        return False

WifiConnect()

try:
    with open("data.json", 'r', encoding='UTF-8') as f:
        load_dict = json.load(f)
    userName = load_dict.get("username")
    passwd = load_dict.get("password")
    LSP_ = load_dict.get("LSP")
except FileNotFoundError:
    userName = input("请输入你的账号：\n")
    passwd= input("请输入你的密码：\n")
    LSP_ = input("请输入你的校园网类型：\nTip：联通填写@unicom 移动@cmcc 单宽@others 校园网@zzulis\n")
    datajson = {
        "username": userName,
        "password": passwd,
        "LSP": LSP_
    }
    FileWrite('data.json', json.dumps(datajson,ensure_ascii=False))
    print("已创建data.json文件,下次打开时不需要再次输入")

class MyRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, hdrs):
        return fp

myHandler = MyRedirectHandler()
opener = urllib.request.build_opener(myHandler)
req = Request('http://1.1.1.1')
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0')
res = opener.open(req)

r = res.getheaders()[4][1]
wlanuserIP = (re.search('wlanuserip=.*?&', r, flags=0)).group()[:-1]
WlanUserIpNum = (re.search('wlanuserip=.*?&', r, flags=0)).group()[11:-1]
print('[200]WlanUserIP GET' + " (" + WlanUserIpNum + ")" + '\n')
POSTurl = 'http://10.168.6.10:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=10.168.6.10&iTermType=1&' + wlanuserIP + '&wlanacip=10.168.6.9&mac=00-00-00-00-00-00&ip=' + WlanUserIpNum + '&enAdvert=0&queryACIP=0&loginMethod=1'
print('[200]POSTurl Structed' + '\n')

datas = {
    "DDDDD": ",0," + userName + LSP_,
    "upass": passwd,
    "R1": "0",
    "R2": "0",
    "R3": "0",
    "R6": "0",
    "para": "00",
    "0MKKey": "123456",
    "buttonClicked": "",
    "redirect_url": "",
    "err_flag": "",
    "username": "",
    "password": "",
    "user": "",
    "cmd": "",
    "Login": "",
}
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
    'Host': "10.168.6.10:801",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://www.zzuli.edu.cn',
    'Connection': 'close',
    'Referer': 'http://www.zzuli.edu.cn',
    'Upgrade-Insecure-Requests': '1',
}
cookies = {
    "program": "new",
    "vlan": "0",
    "ip": WlanUserIpNum,
    "ssid": "null",
    "areaID": "null",
}
data_utf8 = urlencode(datas, encoding='utf-8')
print("[200]Data Packed" + '\n')
r = requests.post(POSTurl, headers=header, data=data_utf8, cookies=cookies)
if '认证成功页' in r.text:
    print("[200]Network Connection Successful")
else:
    print("[403]AC认证失败,请检查账号是否正确")

system("pause")