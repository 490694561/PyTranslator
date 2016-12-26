#!/usr/bin/env python
# encoding:utf8
import requests
import sys
import json
import hashlib
import random
import ConfigParser
# 刚才在百度上查询了一些资料, 发现百度有开放的翻译接口 , 还有有道翻译也是有的 , 这些接口都需要自己去注册帐号并申请一个应用
# 然后就可以使用API的功能了 , 这里将两者的地址都贴出来
# 使用API的好处就是不需要对DOM进行解析 , 获得的结果直接就是我们需要的JSON , 对数据提取显示就可以了
# http://api.fanyi.baidu.com/api/trans/product/index
# (每月翻译字符数低于200万，享免费服务 , 现价￥49.00/百万字符，原价￥70.00/百万字符)
# http://fanyi.youdao.com/openapi
# (使用API key 时，请求频率限制为每小时1000次，超过限制会被封禁。)
# 这里为了方便实用起见, 就不使用爬虫这种方式了 , 直接使用现成的API接口
# 直接去查询API的帮助文档 , 看看都需要发送什么数据
# http://api.fanyi.baidu.com/api/trans/product/apidoc
# Init-start
configParser = ConfigParser.SafeConfigParser()
configParser.read("../Config/config.conf")
# Init-end
# define-start
url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
from_ = "auto"
appid = ""
key = ""
methods = ['zh', 'en']
methods += ['yue', 'wyw', 'jp', 'kor', 'fra', 'spa', 'th', 'ara']
methods += ['ru', 'pt', 'de', 'it', 'el', 'nl', 'pl', 'bul', 'est']
methods += ['dan', 'fin', 'cs', 'rom', 'slo', 'swe', 'hu', 'cht', 'vie']
# define-end
def getRandomString(length):
    result = ""
    for i in range(length):
        result += chr(random.randint(ord('a'), ord('z')))
    return result
def getMd5(src):
    md5 = hashlib.md5()
    md5.update(src)
    return md5.hexdigest()
def getSign(appid, q, salt, key):
    return getMd5(appid + q + salt + key)
def printHelp():
    print "Usage : python " + sys.argv[0] + " [zh(Default)/en/yue/wyw/\
        jp/kor/fra/spa/th/ara/ru/pt/de/it/el/nl/\
        pl/bul/est/dan/fin/cs/rom/slo/swe/hu/cht/vie] [word]"
    print "Example : python " + sys.argv[0] + " ch \"help\""
    print "Example : python " + sys.argv[0] + " en \"帮助\""
def getResult(jsonContent):
    jsonObj = json.loads(jsonContent)
    return jsonObj['trans_result'][0]['dst']
def initUserInput():
    global methods
    if len(sys.argv) == 2:
        return "zh"
    if len(sys.argv) != 3:
        printHelp()
        exit(1)
    method = sys.argv[1]
    for method in methods:
        if method == sys.argv[1]:
            return method
    print "Method Error!"
    exit(1)
def getUrl(url, q, from_, to, appid, salt, sign):
    tempUrl = "%s?q=%s&from=%s&to=%s&appid=%s&salt=%s&sign=%s" % \
        (url, q, from_, to, appid, salt, sign)
    return tempUrl
def getContent(url):
    return requests.get(url).text.encode("UTF-8")
def main():
    initUserInput()
    global url
    global from_
    global appid
    global key
    if len(sys.argv) == 2:
        to = "zh"
        q = sys.argv[1]
    else:
        to = sys.argv[1]
        q = sys.argv[2]
    salt = getRandomString(8)
    sign = getSign(appid, q, salt, key)
    tempUrl = getUrl(url, q, from_, to, appid, salt, sign)
    content = getContent(tempUrl)
    print getResult(content)
if __name__ == '__main__':
    main()

