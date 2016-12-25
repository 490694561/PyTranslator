---
####项目说明 : 
在linux终端下有时候遇到一个想查询的英语单词 , 但是不想打开浏览器去谷歌或者百度去搜索 , 因此就写了这个基于爬虫的单词翻译工具 , 实现原理很简单 , 基本开发已经完成 ,总共有三个分支 , 分别对应 : 爬虫/BaiduAPI/YoudaoAPI , 感觉在有时候读代码变量命名不太懂的时候还是挺有用的 , 毕竟比打开浏览器去访问翻译网站方便多了
> [项目地址](https://coding.net/u/yihangwang/p/PyTranslater/git/tree/youdaoAPI/)

---
####安装方法 : 
```
git clone https://git.coding.net/yihangwang/PyTranslater.git
cd PyTranslater
git checkout youdaoAPI
sudo mv ./fy /usr/local/sbin/
```

---
####使用方法 : 
```
Usage : 
  fy [Your words]
Example : 
  fy help
  fy 帮助
  fy "Help me"
```

---
####悄悄话 : 
其实只用一句shell命令就可以在linux下面完成翻译工作 , 需要用到`curl`, `grep`和`tr`命令
```
curl http://dict.cn/[Your word] | grep "<li><strong>" | tr -d "\t"
curl http://dict.cn/help | grep "<li><strong>" | tr -d "\t"
```
T_T由于不会正则...只能用这种比较low的方法 , 不知道怎么过滤掉流中的字符串 ... 所以输出格式还是有点问题

---
####截图展示 : 

![图片.png](http://upload-images.jianshu.io/upload_images/2355077-4cd7a598e8911c32.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
####TODO : 
> 
1. 将结果保存在本地 , 当用户多次查找的时候减轻服务器的压力
2. 添加命令行参数 , 让用户可以自己定义都需要返回什么数据 , 
   比如说有的时候就只需要知道单词的意思 , 但是有的时候就需要深入学习这个单词
   这个时候就需要用户使用参数来获取更加详细的信息
3. 帮助文档
4. ~~汉译英功能~~
5. 自动补全功能
6. ~~短语查询功能~~
7. 整句翻译功能
5. ~~做成一个小项目 , 可以直接给别人用的那种~~