import requests
from lxml import etree


def query_ip(ip):
    resp = requests.get('http://ip.yimao.com/{}.html'.format(ip))
    result = etree.HTML(resp.text).xpath('//*[@id="yimaos"]/form/ul[2]/li[2]/text()')

    if len(result) == 0:
        return '未知'
    else:
        return result[0]


def get_bilibili_cover_img(bv):
    resp = requests.get('https://www.bilibili.com/video/{}'.format(bv))
    result = etree.HTML(resp.text).xpath('/html/head/meta[11]/@content')

    if len(result) == 0:
        return '未知'
    else:
        return result[0]


def query_price(link):
    pass


if __name__ == '__main__':
    print(get_bilibili_cover_img('BV1UK4y1C71B'))
