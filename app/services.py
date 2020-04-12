from app import utils
from pathlib import Path
import re
import uuid
import requests
from lxml import etree
import plotly


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


def convert_tb_link(link):
    resp = requests.get(link).text
    return re.findall("var url = '(.*?)';", resp, re.S)[0]


def query_price(link):
    html = requests.get('http://p.zwjhl.com/price.aspx?url={}'.format(link)).text
    element = etree.HTML(html)

    # 该商品的最低价格
    lowest_price = utils.clean_text(element.xpath('//div[@class="bigwidth"]/span[1]/font[2]/text()')[0])
    # 该商品最低价格的日期
    lowest_price_date = element.xpath('//div[@class="bigwidth"]/span[1]/font[3]/text()')[0][1:-1]
    # 该商品当前价格
    cur_price = utils.clean_text(element.xpath('//div[@class="bigwidth"]/span[1]/text()')[-1])

    print(lowest_price, lowest_price_date, cur_price)

    temp = re.findall("<script type='text/javascript'>(.*?)</script>", html, re.S)[0]
    timestamp_list = []  # x 轴数据
    price_list = []  # y 轴数据

    # 填充 X 轴（时间线） 和 Y 轴（价格变化） 的数据
    result = re.findall("\[(.*?)\]", temp, re.S)
    for each in result:
        arr = each.split(",")
        timestamp_list.append(int(arr[0]))
        price_list.append(float(arr[1]))

    temp_id = str(uuid.uuid4())

    # 开始画图，并通过 Selenium 截图保存数据图
    plotly.offline.plot({'data': [{'x': timestamp_list, 'y': price_list}],
                         'layout': {'title': 'Price trend graph',
                                    'font': dict(size=12)}},
                        filename='temp/{}.html'.format(temp_id),
                        image='svg', auto_open=False, image_width=1000, image_height=500)
    # 获取当前工作路径
    path = '{}/temp/{}.html'.format(Path.cwd(), temp_id)
    print('save html to:', path)

    return utils.save_html_screenshot(temp_id, path)
