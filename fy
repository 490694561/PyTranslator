#!/usr/bin/env python
# encoding:utf8


import sys
import ConfigParser
import os


configParser = ConfigParser.SafeConfigParser()
configParser.read("/opt/fy/Config/config.conf")

defaultModule = configParser.get("Global", "defaultModule")


def printHelp():
    binName = sys.argv[0].split("/")[-1]
    print "Usage : "
    print "\t" + binName + " [word]"
    print "Example : "
    print "\t" + binName + " help"
    print "\t" + binName + " 帮助"
    print "\t" + binName + " \"help me\""


def getUserInput():
    if len(sys.argv) != 2:
        printHelp()
        exit(1)
    else:
        return sys.argv[1]


def checkConfig(ModuleName):
    global configParser
    if ModuleName == "YoudaoAPI":
        key = configParser.get("YoudaoAPI", "key")
        keyfrom = configParser.get("YoudaoAPI", "keyfrom")
        if key == "":
            print "Please config your key!",
            print "You can use Setup.py as a install guide"
            return False
        if keyfrom == "":
            print "Please config your keyfrom!",
            print "You can use Setup.py as a install guide"
            return False
        return True
    elif ModuleName == "BaiduAPI":
        key = configParser.get("BaiduAPI", "key")
        appid = configParser.get("BaiduAPI", "appid")
        if key == "":
            print "Please config your key!",
            print "You can use Setup.py as a install guide"
            return False
        if appid == "":
            print "Please config your appid!",
            print "You can use Setup.py as a install guide"
            return False
        return True
    elif ModuleName == "Spider":
        return True
    else:
        return False


def main():
    global defaultModule
    checkConfig(defaultModule)
    word = getUserInput()
    command = "python /opt/fy/Modules/" + defaultModule + ".py" + " \"" + word + "\""
    os.system(command)


if __name__ == '__main__':
    main()
