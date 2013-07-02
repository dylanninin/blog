#写在前面的话

继9月30号作好[本站创建和维护计划](http://www.dylanninin.com/blog/2012/09/my-linode-vps-and-movable-type.html)后，经过这两天的折腾，总算完成了一个博客系统的雏形，而且是一个十分朴素的雏形。

在这两天，主要熟悉了MTOS的博客管理，自定义了几个模版或小工具，添加了几个插件，定义了页首、页尾的的Contact和About信息，添加了HTTP请求常见的几个错误跳转页面，最后确定了博客当前的布局和功能，也就是现在看到的这个样子。若没有异常情况，本站很长一段时间内将保持当前布局和功能；这段时间以后，我会将更多的精力放在如何提高博客质量上。

现在稍稍总结下这两天的工作，也记下生活流水，以作备忘。

#博客管理

MTOS的博客管理功能确实是十分强大，博客、模版、小工具等均有版本记录，在编辑的过程中，若异常关闭浏览器，再次打开时还可以进行恢复。在折腾过程中，不知道是我心太急，还是带宽有限，每一次编辑、发布就感觉系统的响应越来越慢，本以为十一假期大家都会在高速公路上拥堵不堪，没想到互联网也是如此。无奈之下，Chrome都Oops不响应了，只好关闭重启，好在MTOS有自动恢复功能，这样我就减少了许多体力劳动，不然还真会像某位急躁哥从车窗探出身子非常淡定地凝望这十分拥堵的traffic line，而且一凝望就是两小时。

#模版和小工具

##1. 相关文章

在博客系统中，相关文章是一个十分重要的功能，这些文章或在分类上相同，或在标签上相同，使分散的文章在一定层次上进行了聚合，更具有知识性和传播性。当用户阅读完一篇博客时，若饶有兴致，就可以根据列出的相关文章进行衍生阅读，很方便。

在网上搜索时，找到一篇关于不使用插件列出具有相同标签文章的博客，只需添加几行代码到文章模版中即可。

本站采用的方式是新建一个模版tag_related_entries，代码如下：
	
	<mt:EntryIfTagged>
	<mt:SetVarBlock name="curentry"><mt:EntryID /></mt:SetVarBlock>
	<mt:SetVarBlock name="relatedtags"><mt:EntryTags glue=" OR "><mt:TagName /></mt:EntryTags></mt:SetVarBlock>
	<mt:SetVarBlock name="listitems"><mt:Entries tags="$relatedtags" unique="1" lastn="10"><mt:SetVarBlock name="listentry"><mt:EntryID /></mt:SetVarBlock><mt:Unless name="listentry" eq="$curentry"><li><a href="<mt:EntryPermaLink />"><mt:EntryTitle /></a></li></mt:Unless></mt:Entries></mt:SetVarBlock>
	<mt:If name="listitems">
	<div class="my_related_entries">
	<h4>Related Entries<span class="delimiter">:</span></h4>
	<ul>
	<mt:Var name="listitems">
	</ul>
	</div>
	</mt:If>
	</mt:EntryIfTagged>

保存后，在模版Entry中需要添加相关文章的位置导入该模版即可。

##2. 文章信息

看到互联网上很多博客在文章末尾会注上文章的版权信息，永久链接等，MTOS默认没有生成这些信息，所以利用MTOS的标签自定义了一个模版entry_info，代码如下：

	<div class="my_entry_info">
	<h4>Entry Info<span class="delimiter">:</span></h4>
	<ul type="circle">
	<li>Name<span class="delimiter">:</span><a href="<$mt:EntryPermalink$>"><$mt:EntryTitle$></a></li>
	<li>Link<span class="delimiter">:</span><a href="<$mt:EntryPermalink$>"><$mt:EntryPermalink$></a></li>
	<li>Author<span class="delimiter">:</span>By <$mt:EntryAuthorLink show_hcard="1"$> on <$mt:EntryDate format="%x %X"$></li>
	</ul>
	</div>

在Entry模版的文章末尾处，导入该模版即可。

##3. 友情链接

为了让大家知道我经常阅读的一些博客，自定义了一个小工具friend_links，根据博客的布局样式，在合适的位置拖入这个小工具即可。本站使用的是三栏式结构，友情链接添加在副侧边栏的最后。

##4. 分享和订阅

为了方便分享和订阅本站，对比了一些常见的社会化分享工具，如[addthis](http://addthis.org.cn/)，[jiathis](http://www.jiathis.com/)，[bShare](http://www.bshare.cn/)，在分享服务、自定义、数据统计、性能等方面各有长短，并未做十分仔细的对比和分析，因addthis在社会化分享的同时，还提供了订阅按钮，为了保证本站页面的一致性，最终选择addthis。

这里仍然采用创建模版或小工具的方式来添加自定义的分享和订阅代码，同样在Entry模版合适的位置导入该模版或插件即可，最终效果见本站。

##5. 社会化评论

MTOS自动的评论系统因带有防Spam功能，响应比较慢，不是很友好。同样，为了提高响应速度和友好性，对比了一些常见的社会化评论系统，如[disqus](http://disqus.com/),[多说](http://duoshuo.com/)等。这些评论系统均有常用的评论功能，不同的是还支持微博等多账户登录；评论内容由第三方平台托管，支持邮件通知、评论统计、评论的导入导出等。对于评论负荷较重的主机，可以采用社会化评论系统取代自带的评论功能。多说比较适合国内的博客，在国外可能disqus使用得更为广泛，因本站VPS在国外，以及并没有将MTOS中文化的计划，所以本站采用disqus。

disqus安装比较简单，注册后，根据向导设置网站，拷贝生成的评论代码，并创建模版，同样在Entry模版合适的位置导入该模版即可，最终效果见本站。

#插件

MTOS自带的Web编辑器不太好用，尤其是添加图片和代码片段时。在官方网站中，找到了一个所见即所得的Web编辑器CKEditor，进行配置后，只适用于Excerpt的编辑，而在Body编辑时，没有CKeditor的踪影，不知是版本不正确，还是设置出了纰漏，目前尚未处理。

粘贴代码片段时，一款代码格式化和高亮插件，可以让代码更易读，博客也更整洁干净，目前尚未处理。

#常用页面

##1. Contact

[联系页面](http://www.dylanninin.com/blog/pages/message.html)，大家若有任何意见和建议，可以在这里留言，或者发邮件。

##2. About

[关于本站](http://www.dylanninin.com/blog/pages/about.html)，提供站点、站长的基本信息，有助于理解和交流。

##3. 404

[Not Found](http://www.dylanninin.com/foo/bar.html)，当访问不存在的资源时，会提示资源找不到。

##4. 403

[Forbidden](http://www.dylanninin.com/blog/errors)，当访问链接存在但由于某些原因服务器拒绝请求时，会提示禁止访问。

##5. 500

当然，除了404,403页面，还有一个500页面，但用户正常访问时，最好不要出现此页面。

#参考

* [MT之旅](http://www.ezloo.com/mt/manual/entry_tag_entries.html)