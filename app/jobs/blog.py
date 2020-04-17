from app import utils
import requests
from lxml import etree


def get_meituan_first_page():
    url = 'https://tech.meituan.com/tags/%E5%90%8E%E5%8F%B0.html'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    element = etree.HTML(resp.text)

    result = []
    for e in element.xpath('//h2[@class="post-title"]/a'):
        result.append({
            'title': e.xpath('text()')[0],
            'url': e.xpath('@href')[0]
        })
    return result


def get_taobao_first_page():
    url = 'http://jm.taobao.org/'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    element = etree.HTML(resp.text)

    result = []
    for e in element.xpath('//a[@class="post-title-link"]'):
        result.append({
            'title': utils.clean_text(e.xpath('text()')[0]),
            'url': 'http://jm.taobao.org{}'.format(e.xpath('@href')[0])
        })
    return result


if __name__ == '__main__':
    print(get_taobao_first_page())
