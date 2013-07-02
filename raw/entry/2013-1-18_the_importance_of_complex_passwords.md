#写在前面的话
很早以前就在使用[Lastpass](https://lastpass.com)进行密码管理，如自动生成复杂密码，Web页面自动填写和登陆；并且在去年开始付费（目前仅支付一年，主要是因为Android移动平台上lastpass免费版使用时间有限，仅16天）。

自[CSDN明文密码泄露](http://coolshell.cn/articles/6193.html)后，密码管理进一步加强，主要是加强密码复杂度，并且定期更换密码。很不幸的是，那是我的CSDN账户也在公布之列，后来一度想找回，无奈CSDN博客的ID已经从dylanninin变为dylan_ninin，心中还是稍有不悦。

最近在一些项目的测试过程中，发现复杂的密码其实有助于测试用户认证模块中很容易被忽视的小问题，尤其是在调用操作系统的命令时。

目前因密码包含特殊字符(如`&`)导致认证异常的情况，已经遇到过两例。

第一例，是在使用Java构建基于Samba文件共享的搜索系统时，因调用Windows系统的`net use \\samba_server_ip password /user:username`时，`password`没有加引号，导致密码复杂时无法成功认证。

第二例，也是因少了引号，在Linux平台上同步修改LDAP和Samba密码，PHP调用`rtrim(shell_exec("/usr/bin/mkntpwd -N $new_pwd"));`，如果`new_pwd`包含`&`符号，`mkntpwd`就只能在后台运行，密码也就从`&`处截断了。

想想这些问题其实很简单，但也很容易被忽视。当然了，从发现这些问题的测试来看，一定复杂度的密码确实起到不少作用，至少一个很容易被忽视的死角马上就暴露出来了。

#程序
因在日常工作中，有一部分是负责用户账号和权限分配，使用Lastpass自动生成密码容易导致密码繁多难以管理，且也有泄露的危险。于是动手写了一个简单的自动生成密码工具，主要使用Python的random和string标准库。

程序主要配置在`passwdgen.py`的`config`中，可以自定义：

	"""password generator config"""
	config={
	  'min':8,			#密码最小长度
	  'max':32,			#密码最大长度
	  'length':8,		#生成密码长度
	  'cs':2,			#字符character最小个数
	  'ds':2,			#数字digit最小个数
	  'ps':2,			#特殊字符punctuation最小个数
	  'users':[			#待生成密码的用户列表
	     'dylanninin',
		 'dylan',
		 'ninin'
	  ],
	  'log':{
	     'file':'passwdgen.log',
	     'format':'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	   }
	}
	

运行效果如下：
	
	$python passwdgen.py
	USERNAME  	PASSWORD  
	dylanninin	U'13Dz/m  
	dylan     	`9K7x\yJ  
	ninin     	8x%df-06  

为避免清空控制台导致生成的密码忘记，已经做了日志记录，`passwdgen.log`：

	2013-01-17 20:37:25,937 - root - INFO - password generation started ... ...
	2013-01-17 20:37:25,937 - root - INFO - USERNAME  	PASSWORD  
	2013-01-17 20:37:25,937 - root - INFO - dylanninin	U'13Dz/m  
	2013-01-17 20:37:25,937 - root - INFO - dylan     	`9K7x\yJ  
	2013-01-17 20:37:25,937 - root - INFO - ninin     	8x%df-06  
	2013-01-17 20:37:25,937 - root - INFO - password generation ended ... ...

源代码：[utils/passwdgen.py on github](https://github.com/dylanninin/utils/blob/master/passwdgen.py)

#参考
* [如何管理并设计你的口令](如何管理并设计你的口令)
* [CSDN明文口令泄露的启示](http://coolshell.cn/articles/6193.html)
* [CSDN明文密码 dylanninin@gmail.com](https://dazzlepod.com/csdn/?email=dylanninin%40gmail.com)
* [破解你的口令](http://coolshell.cn/articles/3801.html)