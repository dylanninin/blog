#写在前面的话
SSH (Secure Shell)可以说是每一台Unix/Linux主机的必备软件和服务，既可以用于远程主机登录，也可以直接在远程主机上执行操作。

对于系统管理员来说，SSH就更显重要了。因为这意味着，当要进行服务器维护工作时，你可以通过SSH在办公区直接管理服务器，而不必跑到机房，或者偏远的IDC。正如本站一样，建站时即使用Xshell客户端远程登录到刚购买的Linode VPS，进行博客环境的搭建以及主机基础安全防护工作；而无需翻山越岭跨不远万里地跑到Linode的某个数据中心。

SSH确实为我们开启了一扇方便之门，但使用不慎也会带来一些安全隐患。当你的主机暴露在互联网上而不加任何防护，那么它很有可能就是某个好事者的下一道小菜。在开启SSH服务时，我们可以适当更改某些设置，提高SSH服务的安全性，降低被攻击的可能性。

##1. 使用公钥私钥

使用公钥私钥对进行连接，而不需要输入口令，这样可以减少暴力破解的可能性。前提是需要将私钥保护好。

###客户端

使用ssh-keygen命令，产生密钥对，并将公钥上传至服务端。

也可以使用shell客户端自带的Key管理工具来生成，本站即使用Xshell生成2048位的RSA密钥对，并将公钥id_rsa.pub上传到服务端。

###服务端

在用户anybody下创建.ssh文件夹，并拷贝id_rsa.pub到~/.ssh/authorized_keys

	cd  /home/anybody
	mkdir .ssh
	cat id_rsa.pub >> .ssh/authorized_keys

	chown -R anybody:anybody .ssh

	chmod 700 .ssh
	chmod 600 .ssh/authorized_keys

注：~/.ssh/authorized_keys是ssh的默认配置，详情见/etc/ssh/sshd_config

##2. 修改默认端口

编号为1024以下的端口都是一些周知端口，SSH默认的端口号为22，更改SSH端口为非常规端口，可以在一定程度上减少端口扫描的信息量，如改为5555，攻击者不一定能够很快猜测到这个端口就是SSH服务，具有一定的不确定性。

更改配置 /etc/ssh/sshd_config：

	Port 5555

##3. 禁止root直接登录

root用户权限太大，直接使用root登录进行操作，稍有不慎就可能会引发意想不到的问题，详见[root用户介绍和基础安全防护](http://www.dylanninin.com/blog/2012/10/root-info-and-basic-security.html)。在SSH中禁用root登录：

	PermitRootLogin no

##4. 取消密码认证

前面已经通过ssh-key或SSH客户端工具生成了密钥对，就已经可以使用密钥进行登录认证了；如果还留有密码认证，这显然会是好事者喜欢的盲点。在SSH中取消密码认证：

	PasswordAuthentication no

##5. 登录提醒

在用户成功登录后，sshd会进行一些的动作，其中可能会执行~/.ssh/rc和/etc/ssh/sshrc脚本。利用这个特性，可以制定sshrc脚本，当有用户SSH远程登录时，发送邮件提醒，利于尽早发现异常。

	echo "http://whatismyipaddress.com/ip/${SSH_CLIENT%% *}" | mail -s "$USER login from ${SSH_CLIENT%% *}" dylanninin@139.com

以上是本站使用SSH的一些基础安全防护策略。SSH的设计和功能很好很强大，Xshell也是一款十分值得推荐的客户端，更多信息，可以参考延伸阅读。

#延伸阅读

* [SSH安全性和配置入门](http://www.ibm.com/developerworks/cn/aix/library/au-sshsecurity/index.html)
* [SSH原理与运用(一)](http://www.ruanyifeng.com/blog/2011/12/ssh_remote_login.html)
* [SSH原理与运用(二)](http://www.ruanyifeng.com/blog/2011/12/ssh_port_forwarding.html)
* [与你潇洒人生路：SSH配置](http://www.cnblogs.com/shuaixf/archive/2012/05/25/2517947.html)
* [A挨个搞： Xshell十大技巧](http://actgod.com/archives/86/)