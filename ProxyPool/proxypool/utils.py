import requests
from requests.exceptions import ConnectionError
from lxml import etree

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_page(url, options={}):
    """
    抓取代理
    :param url:
    :param options:
    :return:
    """
    headers = dict(base_headers, **options)
    print('正在抓取', url)
    try:
        response = requests.get(url, headers=headers)
        print('抓取成功', url, response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('抓取失败', url)
        return None

def get_content(html):
    response = etree.HTML(html)
    result = response.xpath('//*[@id="services"]/div/div[2]/div/div/div/table/tbody/tr/child::*')
    content_total = []
    content_list = []
    for items in result:
        for item in items:
            content = item.text
            content_list.append(content)
        content_total.append(content_list)
        content_list = []
    return content_total

def get_ip(content_total):
    for content in content_total:
        if len(content) > 9:
            content.insert(-2, ':')
            ip = ''
            for num in content:
                if num:
                    ip += num
            print(ip)

url = 'http://www.goubanjia.com/'

def main():
    html = get_page(url, options={})
    content_total = get_content(html)
    get_ip(content_total)

if __name__ == '__main__':
    main()
