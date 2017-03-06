#!/usr/bin/env python
# encoding:utf8
from __future__ import print_function
import requests
import sys
import json
import base64

reload(sys)
sys.setdefaultencoding('utf-8') 

q = ""

if sys.version_info[0] < 3:
    from ConfigParser import SafeConfigParser
    str = unicode
    bytes = str
else:
    from configparser import ConfigParser as SafeConfigParser

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


def getPath():
    return sys.path[0]

# 初始化，获取必要配置
def get_config():
    configParser = SafeConfigParser()
    configParser.read(getPath() + "/../Config/config.conf")
    key = configParser.get("YoudaoAPI", "key")
    keyfrom = configParser.get("YoudaoAPI", "keyfrom")
    url = configParser.get("YoudaoAPI", "url")
    url = "http://fanyi.youdao.com/openapi.do"
    doctype = configParser.get("YoudaoAPI", "doctype")
    return (key, keyfrom, url, doctype)

def printHelp():
    binName = sys.argv[0].split("/")[-1]
    print("Usage : ")
    print("\t {binName} [word]".format(binName=binName))
    print("Example : ")
    print("\t {binName} help".format(binName=binName))
    print("\t {binName} 帮助".format(binName=binName))
    print("\t {binName} \"help me\"".format(binName=binName))


def checkConfig(key, keyfrom):
    if not key:
        print("Please config your key!")
        print("You can use Setup.py as a install guide")
        exit(1)
    if not keyfrom:
        print("Please config your keyfrom!")
        print("You can use Setup.py as a install guide")
        exit(1)


def initUserInput():
    if len(sys.argv) != 2:
        printHelp()
        exit(1)


def getUrl(url, keyfrom, key, doctype, q):
    tempUrl = "{url}?keyfrom={keyfrom}" \
              "&key={key}&type=data&doctype={doctype}&version=1.1" \
              "&q={q}".format(url=url, keyfrom=keyfrom, 
                              key=key, doctype=doctype, q=q)
    return tempUrl

def getContent(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text.encode("UTF-8")
    except Exception, e:
        print(str(e))
        exit(1)

def getTranslation(jsonObj):
    result = ""
    translations = jsonObj['translation']
    for translation in translations:
        result += translation + "\r\n"
    return result[0:-2]


def getUSPhonetic(jsonObj):
    try:
        usPhonetic = jsonObj['basic']['us-phonetic']
    except:
        usPhonetic = ""
    return usPhonetic


def getPhonetic(jsonObj):
    try:
        phonetic = jsonObj['basic']['phonetic']
    except:
        phonetic = ""
    return phonetic


def getUKPhonetic(jsonObj):
    try:
        usPhonetic = jsonObj['basic']['uk-phonetic']
    except:
        usPhonetic = ""
    return usPhonetic


def getExplains(jsonObj):
    try:
        explain = jsonObj['basic']['explains']
        return explain
    except:
        print("[Err] : No result")
        exit(1)


def getWeb(jsonObj):
    return jsonObj['web']


def getMax(numbers):
    maxNumber = 0
    for number in numbers:
        if number > maxNumber:
            maxNumber = number
    return maxNumber


def teePrint(content):
    print(content)
    global q
    f = open(getPath() + "/../Cache/" + base64.b64encode(q), "a+")
    f.write((content + "\n").encode("utf-8"))
    f.close()


def getResult(translation, usPhonetic, phonetic, ukPhonetic, explains, webs):
    maxLength = 16
    teePrint("{separator}翻译{separator}".format(separator='-'*maxLength))
    teePrint(translation)
    teePrint("{separator}音标{separator}".format(separator='-'*maxLength))
    if phonetic:
        teePrint("[" + phonetic + "]")
    if usPhonetic:
        teePrint("[{" + usPhonetic + "] (US)")
    if ukPhonetic != "":
        teePrint("[" + ukPhonetic + "] (UK)")
    teePrint("{separator}解释{separator}".format(separator='-'*maxLength))
    for explain in explains:
        teePrint(explain)
    teePrint("{separator}网络{separator}".format(separator='-'*maxLength))
    for web in webs:
        teePrint(web['key'])
        values = web['value']
        for value in values:
            teePrint("    " + value)


def main():
    global q
    key, keyfrom, url, doctype = get_config()
    checkConfig(key, keyfrom)
    initUserInput()    
    q = sys.argv[1].strip()
    tempUrl = getUrl(url, keyfrom, key, doctype, q)
    content = getContent(tempUrl)
    jsonObj = json.loads(content)
    translation = getTranslation(jsonObj)
    usPhonetic = getUSPhonetic(jsonObj)
    phonetic = getPhonetic(jsonObj)
    ukPhonetic = getUKPhonetic(jsonObj)
    explains = getExplains(jsonObj)
    webs = getWeb(jsonObj)
    getResult(translation, usPhonetic, phonetic, ukPhonetic, explains, webs)

if __name__ == '__main__':
    main()
