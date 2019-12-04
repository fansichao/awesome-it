#! coding:utf-8

import pdfkit
import requests
from bs4 import BeautifulSoup
url = 'http://python3-cookbook.readthedocs.io/zh_CN/latest/'
wb_data = requests.get(url)
wb_data.encoding = 'utf-8'
 
all_urls = []



# 找到所有书URL
if wb_data.ok:
    soup = BeautifulSoup(wb_data.text,'html.parser')
    div = soup.select('.toctree-l2')
    for i in div:
        temp_url = i.contents[0]['href']
        if '#' in temp_url:
            if temp_url.split('#')[0] not in all_urls:
                all_urls.append(temp_url.split('#')[0])
        else:
            all_urls.append(temp_url)


# 测试页面是否Ok
cnt = 0
print(len(all_urls))
for i in all_urls:
    wb_data = requests.get(url + i)
    if wb_data.ok:
        print(cnt+1)


# 分析正文内容
f = open('python cookbook 第三版.html','w',encoding='utf-8')
for i in all_urls:
    print(i)
    wb_data = requests.get(url + i)
    if wb_data.ok:
        wb_data.encoding = 'utf-8'
        soup = BeautifulSoup(wb_data.text,'html.parser')
        div = soup.select('.document')[0]
 
        for i in div:
            f.write(str(i))
f.close()


# 手动微调生成html的内容,删掉所有的特殊标记
#f = open('torch.html','r',encoding='utf-8')
f = open('torch.html','r')
#pdfkit.from_file(f,'torch_guide.pdf',options={'encoding':'utf-8'})
pdfkit.from_file(f,'torch_guide.pdf')


