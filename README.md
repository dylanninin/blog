# 设计思路

传统的博客程序，一般都有后台数据库。当新发布一篇博客时，基本步骤就需要：1.登陆->2.新建博客-3.填写标题-4.复制内容-5.填写关键字-6.选择分类-7.点击发布等，过程十分繁琐。

前段时间正好看到轻量级博客[Letterpress](https://github.com/an0/Letterpress)中提到的想法：直接上传markdown格式的博客原文，让程序自动去处理和渲染。这样一来发布博客确实可省去很多体力活；另外，作为python新手，也想动手实践下，至于实现好坏暂且不表。

主要思路：

* 页面模板：

	* 去年10月起折腾过Movable Type 5，虽博客写得少，但还是看过官方的文档；以及近来流行的Bootstrap项目，也动手进行过一些定制化，Movable Type后台的模板设计很值得学习和借鉴，所以照搬过来。

	* 博客主要采用典型的三栏设计，据此对模板进行抽象和分类，即可分为主模板、layout、modules、widgets和misc等，模板之间可以相互引用。这些模板根据URL请求获取处理后的参数，完成最终渲染并响应给用户。

* 核心逻辑：

	* 初始化。EntryService读取指定路径下的markdown文件，进行初始化，以`2013-7-3_github_tips.md`为例：

		* 1.生成URL，即根据文件名生成URL。如 `2013-7-3_github_tips.md` -> `/blog/2013/07/03/github_tips.html`，对应的raw文件URL则为`/raw/2013/07/03/github_tips.md`。
		* 2.获取时间，优先从文件名中提取，否则获取文件的创建或者更新时间，这里暂未处理好。
	    * 3.获取内容，包括markdown原文内容，以及经过markdown到html转换后的内容。
		* 4.其他初始化，如tag, category, calendar, archive等。
		* 5.存储博客： url(key) -> entry(value) 为一一对一个关系，这里使用dict将entry保存在内存中。

	* 响应请求。当浏览器客户端进行访问时，Web.py应用根据URL路由到指定的Controller，并由EntryService处理逻辑（包括搜索、查看博客、查博客的Raw内容、博客和Raw归档等），返回响应参数（针对模板，该参数也创建了数据模型，可以简化参数传递）；再由控制器根据响应参数判断渲染的模板文件，响应给用户。若请求博客的Raw内容，则直接返回文本内容不用模板渲染。

    * 动态监听。使用pyinotify监听文件系统中的指定博客路径，当该路径下有新增、修改、删除博客的操作时，触发监听事件，并通知EntryService进行相应的新增、修改、删除操作，以更新内存中的博客内容。在本项目中，仅搭建了一个可用的模型，pyinotify使用了一个单独的线程，EntryService在整个程序运行过程，仅有一个实例。

# 项目结构

	blog/
	├── __init__.py            #初始化文件，主要加载pyinotify，监听blog/raw/entry路径下md的新增、修改、删除
	├── blog.py                #博客程序入口，运行： $ cd blog; python blog.py > blog.log 2>&1 &
	├── config.py			   #博客配置，主要是站点、文件系统路径、博客URL路由以及全局环境的配置
	├── controller.py		   #控制器模块，分发URL请求，并响应响应的视图
	├── service.py			   #服务模块，初始化博客系统，处理URL请求逻辑
	├── model.py			   #模型模块，针对博客系统的Entry,Page,Tag,Category等设置的数据模型，以及模板中的参数模型
	├── tool.py				   #工具类，如自动提取关键字，将字典转换为对象等，待完善
	├── README.md
	├── raw					   #raw格式文件路径，主要是markdown文件
	│   ├── entry			   #博客文件
	│   ├── page			   #页面文件，相对于博客而言，页面处理简单很多
	│   └── tweet				
	├── static				   #静态文件，web.py框架的要求，此路径下的文件可以有web.py当做静态文件处理
	│   ├── css
	│   ├── favicon.ico
	│   ├── img
	│   └── js
	└─── template			   #模板库，主要参考Movable Type 5的设计。layout,misc,modules,widgets为子模板。
	    ├── index.html	       #首页模板
	    ├── search.html		   #搜索模板
	    ├── entry.html		   #Entry/Page详情模板
	    ├── archive.html	   #归档模板
	    ├── atom.xml		   #RSS订阅模板
	    ├── error.html		   #错误页面模板
	    ├── layout			   #布局模板，这里采用 `AA|B|C`的三栏布局，AA放博客主要内容，B、C作为右侧边栏显示widgets
	    │   ├── footer.html
	    │   ├── header.html
	    │   ├── navbar.html
	    │   ├── three
	    │   │   ├── primary.html
	    │   │   └── secondary.html
	    │   └── two
	    ├── misc			  #杂项资源
	    │   ├── ads
	    │   │   └── ad.html
	    │   └── analytics.html
		├── modules			   #模板模板，在AA布局中使用
		│   ├── archive.html
		│   ├── category.html
		│   ├── comment.html
		│   ├── entry.html
		│   ├── error.html
		│   ├── excerpt.html
		│   ├── info.html
		│   ├── pager.html
		│   ├── related.html
		│   ├── search.html
		│   └── tag.html
		└── widgets           #小工具模板，在B、C侧边栏中使用
		    ├── about.html
		    ├── archive.html
		    ├── calendar.html
		    ├── category.html
		    ├── link.html
		    ├── powered.html
		    ├── recently.html
		    └── tag.html

# 要求

* 仅限于Linux平台。因使用[pyinotify](https://github.com/seb-m/pyinotify)有平台限制。Pyinotify监听指定路径，即可自动处理新增、更新以及删除的博客。详见[pyinotify](https://github.com/seb-m/pyinotify)。

* Markdown。将markdown格式文件渲染成HTML，详见[markdown](https://github.com/waylan/Python-Markdown)。

* Web.py。使用的Web框架，由已故的[Aaron Swartz](http://www.aaronsw.com/)开发，详见[Web.py](http://webpy.org)。

* Python 2.7.5。本博客程序仅在Python 2.7.5下测试通过。

# 运行

克隆博客代码

	$ cd ~

	$ git clone https://github.com/dylanninin/blog.git

切换路径

	$ cd blog

启动博客

	$ python blog.py > blog.log 2>&1 &  #Listen on 0.0.0.0:8080 default


# 博客

环境准备

	$ ln -s ~/blog/raw/entry  entry

	$ cd entry

发布博客

	$ rz 				# use ZMODEM (Batch) file receive tool to send your local markdown file
						# to blog server. md format is usually yyyy-mm-dd_file_name.md

删除博客

	$ rm 2013-07-02_github_tips.md

# 效果

 * Online Demo: [http://dylanninin.com:8080/](http://dylanninin.com:8080)
 * Movable Type 5：[http://dylanninin.com/](http://dylanninin.com/)

# 计划

* 自动提取关键字

* 自动摘要

* 自动查找相关博客

* 功能完善和bug排除

* 代码重构

# 更新

## 2017-06-18

- 部署到 [Heroku](https://www.heroku.com/)

## 2016-03-06

- 增加 [requirements.txt](./requirements.txt)

## 2015-09-17

- 格式化代码

## 2013-11-23

本计划使用[TF-IDF](http://en.wikipedia.org/wiki/Tf%E2%80%93idf)以及[Jieba](https://github.com/fxsjy/jieba)，自动提取博客的关键字、摘要以及相似文章，但效果并不理想。

这里模仿 Githuh Pages中的做法，在博客的开始声明一些属性：

	---
	title: the title, default None if it's empty
	category: category, default Uncategorised if it's empty.
	tags: [tag1, tag2], default [Untagged] if it's empty.
	---

因使用[YAML](http://en.wikipedia.org/wiki/Yaml)解析，需要新增[PyYAML](http://pyyaml.org/)包。

另外，此博客的在线[demo](https://webpy-blog.herokuapp.com/)。


* 阮一峰的网络日志—— TF-IDF与余弦相似性的应用系列：[自动提取关键字](http://www.ruanyifeng.com/blog/2013/03/tf-idf.html)；[找出相似文章](http://www.ruanyifeng.com/blog/2013/03/cosine_similarity.html)；[自动摘要](http://www.ruanyifeng.com/blog/2013/03/automatic_summarization.html)
* Python 中文分词[Jieba](https://github.com/fxsjy/jieba)

# 参考

* [Web.py](http://webpy.org)
* [pyinotify](https://github.com/seb-m/pyinotify)
* [Bootstrap](http://twitter.github.com/bootstrap)
* [Movable Type](http://dylanninin.com)
