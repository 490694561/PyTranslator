---
####项目说明 : 
在linux终端下有时候遇到一个想查询的英语单词 , 但是不想打开浏览器去谷歌或者百度去搜索 , 因此就写了这个基于爬虫的单词翻译工具 , 实现原理很简单 , 基本开发已经完成 ,总共有三个分支 , 分别对应 : 爬虫/BaiduAPI/YoudaoAPI , 感觉在有时候读代码变量命名不太懂的时候还是挺有用的 , 毕竟比打开浏览器去访问翻译网站方便多了
> [项目地址](https://coding.net/u/yihangwang/p/PyTranslater/git/tree/release/) 有兴趣的小伙伴儿咱们可以一起写  : D

---
####安装方法 :
1. [申请有道翻译Key](http://fanyi.youdao.com/openapi?path=data-mode)
```
需要填写一下邮箱和应用名称 , 然后邮箱中会收到Key , 在第三步会用到
```
2. 安装Python第三方库
```
安装第三方python库
sudo apt-get install python-pip
sudo pip install requests
sudo pip install bs4
``` 
3. 克隆项目
```
git clone https://git.coding.net/yihangwang/PyTranslater.git
cd PyTranslater
git checkout release
```
4. 进行安装 
```
sudo python Setup.py
按照Setup.py中的指引就可以完成安装
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
这里非常感谢[@左蓝](http://www.jianshu.com/users/e213f00c7c35/latest_articles)同学提供shell命令 : 
```
curl -s http://dict.cn/help | grep "<li><strong>" | tr -d '\t' | sed 's/<li><strong>//g' | sed 's/<\/li>//g' | sed 's/<\/strong>//g'
```
![图片.png](http://upload-images.jianshu.io/upload_images/2355077-271f0edb26b25e17.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
####截图展示 : 

![图片.png](http://upload-images.jianshu.io/upload_images/2355077-4cd7a598e8911c32.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---
####~~原理 : (使用爬虫进行实现 , 对应git仓库的master分支)~~

使用爬虫技术 , 将用户输入作为关键字发送HTTP请求到在线翻译网站(http://dict.cn/)
解析返回HTML页面 , 提取有用的信息 , 将结果呈现给用户

首先需要分析目标网站是如何处理用户参数的
使用浏览器访问该网站 , 任意查询某单词 , 例如`help`
发现跳转到新的结果页面以后 , url 就变成了 : `http://dict.cn/help`
说明我们可以访问这样的url就可以得到查询结果 : 
`http://dict.cn/[word]`

> 这样的话 , 我们的脚本就需要做这几件事情
1. 接受用户输入的单词
2. 拼接url
3. 访问该url得到返回页面
4. 解析页面 , 提取我们感兴趣的信息

这样的话 , 前三步都应该不会很难 , 
重要的是我们如何从返回页面中提取出我们感兴趣的信息
首先我们分析一下结果页面中都包含哪些有效的数据 ?
经过分析得到 :

```

1. 音标
2. 简意
---
3. 详尽释义
4. 英英释义
5. 行业释义
6. 双解释义
---
7. 例句
8. 常见句型
9. 常用短语
10. 词汇搭配
11. 经典引文
---
12. 词语用法
13. 词义辨析
14. 常见错误
15. 词源解说
---
16. 近反义词
17. 缩略词
18. 互动百科
19. 临近单词
```

这个时候 , 我们需要对结果页面的代码结构进行分析 , 我们需要分析这些信息都具有什么样的特征可以供我们进行提取
分析之后得到 : 

```

1. 音标 # <ul class="phonetic">...</ul>
2. 简意 # <ul class="dict-basic-ul">...</ul>
<!-- 3. 含义分布 # <ul id="highcharts-0" class="highcharts-container">...</ul> -->
---
3. 详尽释义 # <ul lass="layout detail">...</ul>
4. 英英释义 # <ul class="layout dual">...</ul>
5. 行业释义 # <ul class="layout hhsy">...</ul>
6. 双解释义 # <ul class="layout en">...</ul>
---
7. 例句 # <ul class="layout sort">...</ul>
<!-- 8. 常词性分布 # <ul id="highcharts-2" class="highcharts-container">...</ul> -->
8. 常见句型 # <ul layout patt>...</ul>
9. 常用短语 # <ul class="layout phrase">...</ul>
10. 词汇搭配 # <ul class="layout coll">...</ul>
11. 经典引文 # <ul class="layout auth">...</ul>
---
12. 词语用法 # <ul class="layout ess">...</ul>
13. 词义辨析 # <ul class="layout discrim">...</ul>
14. 常见错误 # <ul class="layout comn">...</ul>
15. 词源解说 # <ul class="layout etm">...</ul>
---
16. 近反义词 # <ul class="layout nfw">...</ul>
17. 缩略词 # <ul class="layout abbr">...</ul>
18. 互动百科 # <ul class="layout baike">...</ul>
19. 临近单词 # <ul class="layout nwd">...</ul>
```

总共有这么多的属性 , 我们这里先做一个比较简单的功能 , 就是将用户输入单词的简单意思输出
这样的话 , 可能我们只需要用到第二个属性 : `简意 # <ul class="dict-basic-ul">...</ul>`
这样我们解析了返回页面的DOM节点之后就可以查找对应的节点

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
8. 相对路径和绝对路径的BUG , 不应该使用os.system函数去调用 , 而是应该使用python的模块
