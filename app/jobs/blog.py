from app import utils
import requests
from lxml import etree


# 美团技术博客
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


# 淘宝中间件博客
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


# 阮一峰博客
def get_ryf_first_page():
    url = 'http://www.ruanyifeng.com/blog/archives.html'
    resp = requests.get(url).text
    resp = resp.encode('ISO-8859-1').decode('utf-8')
    element = etree.HTML(resp)

    result = []
    for e in element.xpath('//div[@id="alpha-inner"]/div/div/ul/li/a'):
        result.append({
            'title': e.xpath('text()')[0],
            'url': e.xpath('@href')[0]
        })
    return result


def get_program_think_first_page():
    url = 'https://program-think.blogspot.com/'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    element = etree.HTML(resp.text)

    result = []
    idx = 0
    for e in element.xpath('//*[@id="Blog1"]/div[1]/div/h1/a'):
        if idx > 10:
            break
        result.append({
            'title': e.xpath('text()')[0],
            'url': e.xpath('@href')[0]
        })
        idx += 1
    return result


if __name__ == '__main__':
    print(get_program_think_first_page())
