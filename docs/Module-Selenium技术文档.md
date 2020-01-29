# Selenium技术文档.md

## 简介说明


## 安装部署

### 常用下网站

- [FirexDriver-geckodriver下载](https://github.com/mozilla/geckodriver/releases)
- [chromedriver下载](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- [查看Chrome浏览器版本](chrome://settings/help)
- [geckodriver-Selenium-Firefox版本支持表](https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html#supported-platforms)


 


## 问题


### selenium.common.exceptions.WebDriverException: Message: newSession

参考链接：https://blog.csdn.net/qq_29012939/article/details/86591383

解决方法：

```bash
1、我用的浏览器是火狐浏览器，主要原因是geckodriver的版本太低，而浏览器的版本是64.0。

更新为v0.23.0：https://github.com/mozilla/geckodriver/releases

将下载下来的geckodriver.exe放入python安装路径下的Scripts文件夹内
```

### selenium.common.exceptions.InvalidSessionIdException: Message: Tried to run command without establishing a connection

解决方法

```bash
去掉browser.close()即可
```



## 案例-模拟淘宝登录


[Python模拟登录]https://blog.csdn.net/u014044812/article/details/99584382

参考链接: 


```python
#!/usr/bin/python
#-*-coding:utf-8-*-
from selenium import webdriver  
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import urllib2
import json
import traceback
import sys

#dcap = dict(DesiredCapabilities.PHANTOMJS)
#dcap["phantomjs.page.settings.userAgent"] = (
#    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
#)
#driver = webdriver.PhantomJS(executable_path='/home/sevencm/phantomjs/bin/phantomjs',desired_capabilities=dcap)  
#profiledir='/home/sevencm/.mozilla/firefox/miinxjat.default'
#profile=webdriver.FirefoxProfile(profiledir)
#option=webdriver.ChromeOptions()
#option.add_argument('--user-data-dir=/home/sevencm/.config/google-chrome/Default')
#driver = webdriver.Chrome()  
driver = webdriver.Firefox()  
#driver.viewportSize={'width':1024,'height':800}
#driver.maximize_window()
 
#driver.delete_all_cookies()
driver.get("https://login.taobao.com/member/login.jhtml?from=taobaoindex&f=top&style=&sub=true&redirect_url=https%3A%2F%2Fmyseller.taobao.com%2Fseller_admin.htm")
 #load the switch
element=WebDriverWait(driver,60).until(lambda driver : driver.find_element_by_xpath("//*[@id='J_Quick2Static']"))
element.click()
driver.implicitly_wait(20)
sleep(1)
username=driver.find_element_by_name("TPL_username")
if not username.is_displayed:
    driver.implicitly_wait(20)
    driver.find_element_by_xpath("//*[@id='J_Quick2Static']").click()
driver.implicitly_wait(20)
sleep(2)


name = "643566992@qq.com"
passwd = "flzf5177@46"


username.send_keys(name)
username.send_keys(Keys.TAB)
driver.implicitly_wait(20)
sleep(2)
pwc=driver.find_element_by_name("TPL_password")
pwc.send_keys(passwd)
sleep(1)
driver.save_screenshot('login-screeshot-1.png')
sleep(2)
while True:
    try:
        #定位滑块元素,如果不存在，则跳出循环
        show=driver.find_element_by_xpath("//*[@id='nocaptcha']")
        showval=show.value_of_css_property("display")
        if not show.is_displayed():
            break        
        source=driver.find_element_by_xpath("//*[@id='nc_1_n1z']")  
        sleep(3)
        #定义鼠标拖放动作
        #ActionChains(driver).drag_and_drop_by_offset(source,400,0).perform()
        #driver.save_screenshot('login-screeshot-11.png')
        action = ActionChains(driver)
        sleep(1)
        action.click_and_hold(source).perform()
        for index in range(20):
          try:
             action.move_by_offset(2, 0).perform() #平行移动鼠标
             driver.save_screenshot('login-screeshot-i-'+str(index)+'.png')
          except Exception as e:
             print(e) 
             break
          if(index==19):
           action.release()
           sleep(1)
           driver.save_screenshot('login-screeshot-i-'+str(index)+'.png')
          else: 
           sleep(0.01) #等待停顿时间
        sleep(0.1)
        #print(show.get_attribute("outerHTML"))
        sleep(2)
        driver.save_screenshot('login-screeshot-0.png')
            #查看是否认证成功，获取text值 //*[@id="nc_1__scale_text"]/span
        text=driver.find_element_by_xpath("//*[@id='nc_1__scale_text']/span")
        if text.text.startswith(u'验证通过'):
            print('成功滑动')
            break
        if text.text.startswith(u'请点击'):
            print('成功滑动')
            break
        if text.text.startswith(u'请按住'):
            continue
    except Exception as e:
        print(traceback.format_exc())
        print(e) 
        print "111111111111111111111"
        import time
        time.sleep(10)
        #driver.find_element_by_xpath("//div[@id='nocaptcha']/div/span/a").click()
        
driver.find_element_by_xpath("//*[@id='J_SubmitStatic']").click()
sleep(2)
driver.save_screenshot('login-screeshot-2.png')
#以下是获得cookie代码
cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
cookiestr = ';'.join(item for item in cookie)
#print cookiestr
data={
'cookie':cookiestr
}
print(data)
#post cookie到接口
try:
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url='http://127.0.0.1:8080/update/taobao/cookie', headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)
    print(response.read())
except Exception as e:
    print(e) 
#driver.close()
driver.quit()
sys.exit(0)
```













## 案例-模拟B站登录

https://blog.csdn.net/qq_36853469/article/details/100579355


## 附件

### 参考链接


[selenium变速移动验证码滑块](https://www.cnblogs.com/gaoyukun/p/9717166.html)