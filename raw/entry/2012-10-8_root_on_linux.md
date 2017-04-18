## 写在前面的话

root是Unix/Linux的超级用户，拥有绝对的权力。拥有root权限，你尽可以随心所欲而不逾矩：你既是"矩"的制定者，也是"矩"的拥护者，当然稍有不慎，你也可能是"矩"的破坏者、毁灭者，因为若被滥用，则会引发异常崩溃，甚至导致绝对的腐败。

所以很多Unix/Linux教程都花了很大篇幅讲解系统权限，并强烈建议慎用root，而代之以普通用户，如anybody。这样当anybody试图做某些逾矩的操作时，会提示Permission Denied并无法执行，此时root制定的规则已经生效，并得到遵守，不管你是情愿，还是被迫。当然，若有需要，anybody也可以切换为root身份，前提是需要知道root的口令。

根据以上信息，我们至少可以从三个方面增强root安全。

### 1. 高强度口令

为root用户设置一个高强度的口令，大小写字母 + 数字 + 特殊字符，而且还要保证有足够的位数。

去年国内几大网站相继出现[明文口令泄露事件](http://coolshell.cn/articles/6193.html)，有很多可供引以为戒。但我相信，很多用户依然还没有引起重视，不信可以去测试下你的密码强度：[How Security Is My Password](http://howsecureismypassword.net/)

### 2. 创建普通用户

使用root登录，新增用户anybody，并为anybody设置一定强度的密码。

	useradd anybody
	passwd anybody

注：创建修改用户需要root权限。

### 3. 限制su/sudo

在Unix/Linux系统中，要获取其他用户的权限有两种方式，一是使用su(switch user)，切换成为某用户，这样就拥有了该用户的所有权限，直到退出该用户；另外一种是sudo(do as another user)，以另外一个用户的身份执行某些操作，此时在短时间内你获取该用户的权限，直到超时。

当然，su/sudo的细节可以由root进行控制。

#### 限制只有wheel组的用户可以使用su

编辑/etc/pam.d/su文件，启用用户组认证：

	# Uncomment the following line to require a user to be in the "wheel" group.
	
	auth            required        pam_wheel.so use_uid

将普通用户anybody添加到wheel组，wheel的gid为10

	usermod -G 10 anybody

这样就只有该用户和root可以使用su。

#### 限制普通用户使用sudo

sudo主要配置在/etc/sudoers，新增加的用户默认没有添加到sudoers中，若有需要，可以参照配置中说明更改。

比较通用的做法是定制一些可以执行或禁止执行的命令集，而允许执行的命令集足以完成系统的日常维护工作，禁止执行的命令集可能会使系统暴露不够安全，然后将这些命令集授权给该用户，这样既分配适当权限，又作特殊限制。

当然，root涉及到系统安全远不止这些，以上仅是本站使用的一些策略，更详细的信息有待进一步理解和实践。

## 延伸阅读

* [Linux系统安全(一):安装与设置](http://www.ibm.com/developerworks/cn/linux/security/l-ossec/part1/)
* [权限安全使用和密码管理](http://www.ibm.com/developerworks/cn/linux/l-cn-rootadmin2/index.html)
* [了解和配置PAM](http://www.ibm.com/developerworks/cn/linux/l-pam/)
* [充分发挥sudo的作用](http://www.ibm.com/developerworks/cn/aix/library/au-sudo/
