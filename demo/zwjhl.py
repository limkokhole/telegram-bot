import requests
import re
from lxml import etree
import plotly
import plotly.graph_objs as go
from selenium import webdriver
from pathlib import Path
from app import services


def clean_text(s):
    return s.replace('\r', '').replace('\n', '').replace(' ', '')


url = 'https://detail.tmall.com/item.htm?id=601586916186&spm=a1z09.2.0.0.3cc12e8dvhpEeA&_u=c2jk22qr3701'

html = requests.get('http://p.zwjhl.com/price.aspx?url={}'.format(url)).text

element = etree.HTML(html)

lowest_price = float(clean_text(element.xpath('//div[@class="bigwidth"]/span[1]/font[2]/text()')[0]))
lowest_price_date = element.xpath('//div[@class="bigwidth"]/span[1]/font[3]/text()')[0][1:-1]
cur_price = float(clean_text(element.xpath('//div[@class="bigwidth"]/span[1]/text()')[-1]).replace('\xa0当前价：', ''))

print('最低价格：', lowest_price, '最低价格日期：', lowest_price_date, '当前价格：', cur_price)

script = re.findall("<script type='text/javascript'>(.*?)</script>", html, re.S)[0]

dates = []  # x 轴数据
prices = []  # y 轴数据

result = re.findall("\[(.*?)\]", script, re.S)
for each in result:
    arr = each.split(",")
    dates.append(int(arr[0]))
    prices.append(float(arr[1]))

services.get_buy_suggestion(cur_price, lowest_price, prices)

# plotly.offline.plot({'data': [{'x': x_data, 'y': y_data}],
#                      'layout': {'title': '哈哈哈哈哈',
#                                 'font': dict(size=12)}},
#                     image='svg', auto_open=False, image_width=1000, image_height=500)
#
# path = '{}/temp-plot.html'.format(Path.cwd())
#
# options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')
# # options.add_argument('--headless')
# options.add_argument("--start-maximized")
#
# driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver.exe')
# driver.get(path)
# driver.save_screenshot('../temp/my_plot.png')
# driver.close()



