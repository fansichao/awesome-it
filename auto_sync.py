u""" Github文章 自动推送

Github文章自动推送
---------------------------
1. 简书
2. CSDN

---------------------------
# 简书文章下载 https://www.jianshu.com/p/850147cfa046
pip install js2x
python js2x.py post_url
# 例如：python js2x.py http://www.jianshu.com/p/7017bfd4dd56

"""

import jianshuAPI

JIANSHU_CONFIG = {
    'user_home': 'https://www.jianshu.com/u/2599498ff83f',
    # 使用浏览器复制来的cookies，来进行免账号密码登陆操作你的简书
    'cookies_str': '',
}

CONFIG = JIANSHU_CONFIG 

def check_params(config, need_keys=[]):
    u""" 参数检查
    """
    

    pass
    

def sync():
    u""" 自动推送同步文章
    """

    pass
    


def jianshu_sync():
    pass


#这个浏览器控制器是所有操作的基础，必须先初始化好它，才可以进行后面的操作
driver=jianshuAPI.add_browser_cookies_str(CONFIG['cookies_str'],CONFIG['user_home'],jianshuAPI.driver)
#或使用豆瓣登录简书获得driver
#driver=jianshuAPI.login_jianshu_by_douban('豆瓣账号','豆瓣账号登录密码') 

##获取你的所有文集列表，并打印所有的文集名，这个文集列表包含文集的索引，后面的操作需要用到它
anthologies=jianshuAPI.list_anthology(driver)
for i in anthologies:
    print (i[0])

##添加一个名叫“hello world”的文集
jianshuAPI.add_anthology('hello world',driver)

##重命名一个文集，将‘hello world’重命名为"你好世界。。。"
#获取最新的文集列表
anthologies=jianshuAPI.list_anthology(driver)
print(anthologies[0][0])#打印第一个文集的文集名
#进行重命名操作
jianshuAPI.rename_anthology(anthologies[0],'你好世界。。。',driver)

##向文集“你好世界。。。”添加名为“hello world”的文章
text='不管你爱不爱我，我依旧是你最好的小心肝，是吧，我美美的小世界。。。'
jianshuAPI.add_article(anthologies[0],'hello world',text,driver)

##修改指定文集“你好世界。。。”的文章“hello wrold”的文本
#获得“你好世界。。。”文集的的所有文章并打印所有的文章名，得到文章的索引
articles=jianshuAPI.list_article(anthologies[0],driver)
for i in articles:
    print(i[0])
text="this is a test demo."
jianshuAPI.edit_article(anthologies[0],articles[0],text,driver)

##获取文集“你好世界。。。”文章“hello world”的文本内容
get_text=jianshuAPI.get_article(anthologies[2],articles[0],driver)
print(get_text)

##删除文集“你好世界。。。”文章“hello world”
jianshuAPI.delete_article(anthologies[0],articles[0],driver)
  
##删除文集“你好世界。。。”
jianshuAPI.delete_anthology(anthologies[0],driver)  


