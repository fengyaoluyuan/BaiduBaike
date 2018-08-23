import requests
from lxml import etree

url = 'https://baike.baidu.com/item/%E5%90%B4%E5%8F%8B%E4%B8%89'
headers ={
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'BAIDUID=96F210D125FFEA683BC188D43379C92C',
    'Host': 'baike.baidu.com',
    'Referer': 'https',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    response.encoding = 'utf-8'
html = etree.HTML(response.text)
print(type(html))
title = html.xpath('.//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()')[0]
article = html.xpath('.//div[@class="main-content"]/div')
for item in article:
    ele = item.findtext('人物生平')
    item_text = ele.text()
    print(item_text)
