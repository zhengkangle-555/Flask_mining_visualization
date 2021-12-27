# **基于Flask的Python全国招聘岗位就业可视化系统**

## **1 开发环境**
- [x] 1 系统：Window 10 家庭中文版。
- [x] 2 语言：Python（3.8.5）、MySQL（5.5）。
- [x] 3 Python所需的库：flask、pymysql、pandas、numpy、time、datetime、requests、etree、jieba、re、json、decimal（没有的话pip或conda安装一下~）。
- [x] 4 编辑器：jupyter Lab（jupyter notebook）、Pycharm（主用）、Navicat。

## **2 运行说明**
本项目下面有五个.py的文件，下面分别阐述各个文件所对应的功能：<br>
- [x] 1 data_collection：分别从前程无忧网站和猎聘网上以关键词`job_name`爬取相关数据。其中，前程无忧爬取的数据主要用来进行相关图表的绘制；而猎聘网上主要为岗位要求文本数据，这部分进行词云的可视化展示。
- [x] 2 data_clean：对爬取到的数据进行清洗，包括去重去缺失值、变量重编码、特征字段创造、文本分词等。
- [x] 3 data_store：将清洗后的数据全部储存到`MySQL`中，其中对文本数据使用`jieba.analyse`下的`extract_tags`来获取文本中的关键词和权重大小，方便绘制词云。
- [x] 4 utils：大多为app调用MySQL数据库中的工具类函数；同时，里面也有引用data_collection、data_clean、data_store等函数，我们也主要使用该工具类进行岗位数据的爬取、清洗和存储。
- [x] 5 app：使用`Python`一个小型轻量的`Flask`框架来进行`Web`可视化系统的搭建，在static中有css和js文件，js中大多为百度开源的[ECharts](https://echarts.apache.org/examples/zh/index.html)，再通过自定义`controller.js`来使用ajax调用flask已设定好的路由，将数据异步刷新到templates下的`main.html`中。
- [x] 6 如何运行：先运行utils，提前进行数据采集、数据清洗、数据存储操作，之后更改app修改好`datatable`和`job_name`，这部分信息务必与utils中输入的保持一致（因为发现app一运行的话就会直接给出网页，所以没法在控制台上同步将变量赋值过去*_*）。
- [x] 7 温馨提示：由于我在数据采集部分使用了一个用redis搭建的代理IP池，所以一开始运行的话需要将里面的proxies删掉，使用time.sleep即可（使用代理池能防止被封IP，同时可以更快爬取数据，实现可视化操作）。

## **3 你将会学到**
- [x] 1 Python爬虫：盗亦有道，掌握requests和xpath的相关用法。
- [x] 2 数据清洗：能详细知道项目中数据预处理的步骤，包括去重去缺失值、变量重编码、特征字段创造和文本数据预处理，玩转pandas、numpy相关用法。
- [x] 3 数据库知识：select、insert等操作，掌握pymysql相关用法。
- [x] 4 前后端知识：了解到HTML、JQuery、JavaScript、Ajax的相关用法。
- [x] 5 Flask知识：能快速建立起一个轻量级的Web框架，利用Python实现前后端交互。

## **4 效果图**
**4.1 未同步数据的前端页面**<br>
![效果图1](https://bcn.135editor.com/files/users/562/5623890/202109/fu37rvCA_EfEM.png '可视化系统效果图1')<br>
**4.2 同步数据的前端页面**<br>
![效果图2](https://bcn.135editor.com/files/users/562/5623890/202109/EQr7RpJv_DH7T.png '可视化系统效果图2')

## **5 心得体会**
> 整个项目从构思到开发完毕大概花费了我6天时间，虽然这段时间发生了不少插曲，也遭受到了不少打击，但只要能受到周围人对我的认可和承认，就觉得特别开心，这也是一直支撑着我传播知识的原因。如果有机会的话，我想，我会一直这样坚持下去~(　＾∀＾)

不过，眼前尚有一道需要跨越的坎，这段时间得把精力都放在上面了。如果最后仍达不到我的目标，那时候应该会特别难受，不过都是后话了，先江湖再见咯Σ(ＴωＴ)努力--

## **6 其他**
- [x] 1 灵感来源：B站UP主东方瑞通，点击可查看视频[Python爬取疫情实战：Flask搭建web/Echarts可视化大屏/MySQL数据库/Linux项目部署与任务定时调度](https://www.bilibili.com/video/BV177411j7qJ?p=19)
- [x] 2 代码开发者：欢迎点击我的[知乎首页](https://www.zhihu.com/people/zkl66)。
- [x] 3 一点干货：如果想学习数据分析或者数据挖掘的，推荐查看我在[和鲸社区](https://www.heywhale.com/mw/project/61342a57c9c30f001878d043)上线的项目，[Github](https://github.com/zhengkangle-555/ConsumersProfile)上也有资源。
- [x] 4 备注：运行flask得到web链接时，在修改代码后想同步到web前端时一般需要将flask的debug功能打开，而且刷新时建议直接使用`ctrl+F5`强制刷新，因为浏览器在接收到本地主机部署的数据包后会存放在缓存中，方便下次加载时能快速呈现出来。
- [x] 5 系统改进：之后可以尝试部署到网络中，同时，可以对自定义词典进行改进，增加更多岗位的分词信息；另外，也可以设置定时定点爬取数据，增加登录注册页面，让多台主机同时进行工作，实现数据的快速传递和更新。
