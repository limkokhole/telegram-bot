from app import utils
from pathlib import Path
from app.utils import logger
from datetime import datetime
import re
import uuid
import requests
import plotly
from lxml import etree
from you_get.extractors.bilibili import site, download

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}


def http_get(url):
    return requests.get(url, headers=headers)


def bilibili_url(bv):
    return 'https://www.bilibili.com/video/{}'.format(bv)


def query_ip(ip):
    resp = http_get('http://ip.yimao.com/{}.html'.format(ip))
    result = etree.HTML(resp.text).xpath('//*[@id="yimaos"]/form/ul[2]/li[2]/text()')

    if len(result) == 0:
        return '未知'
    else:
        return result[0]


def get_bilibili_cover_img(bv):
    resp = http_get(bilibili_url(bv))
    result = etree.HTML(resp.text).xpath('/html/head/meta[11]/@content')

    if len(result) == 0:
        return '未知'
    else:
        return result[0]


def download_bilibili_video(bv):
    download(bilibili_url(bv), output_dir='/download', merge=True)
    return site.title


# 通过 https://www.zhihu.com/zvideo/{id} 获取 https://www.zhihu.com/video/{id} 的链接
def get_zhihu_video_link(zvideo_id):
    resp = http_get('https://www.zhihu.com/zvideo/{}'.format(zvideo_id))
    video_url = etree.HTML(resp.text).xpath('//iframe/@src')[0]

    return get_zhihu_video_download_url(video_url)


# 通过 https://www.zhihu.com/video/{id} 链接获取 https://vdn2.vzuu.com 视频下载链接
def get_zhihu_video_download_url(video_url):
    page_source = utils.get_page_source(video_url)
    src = etree.HTML(page_source).xpath('//*[@id="player"]/div/div/div[1]/video/@src')
    if len(src) == 0:
        logger.error('没有发现视频链接')
        return None
    return src[0]


def get_download_list_by_question_url(question_url):
    resp = http_get(question_url)
    elements = etree.HTML(resp.text).xpath('//div[@class="Card AnswerCard"]/div/div/div[2]/div[1]/span/a')

    result = []
    for e in elements:
        redirect_url = e.xpath('@href')[0]
        if not redirect_url.startswith('https://link.zhihu.com/?target=https%3A//www.zhihu.com/video/'):
            continue
        video_id = re.findall('/video/(.*?)$', redirect_url, re.S)[0]

        result.append({
            'title': e.xpath('@data-name')[0],
            'video_id': video_id
        })
    return result


# 查询价格变化趋势
def query_price(link):
    html = http_get('http://p.zwjhl.com/price.aspx?url={}'.format(link)).text
    if html.find('该商品暂未收录') != -1:
        return None, None

    element = etree.HTML(html)

    # 该商品的最低价格
    lowest_price = float(utils.clean_text(element.xpath('//div[@class="bigwidth"]/span[1]/font[2]/text()')[0]))
    # 该商品最低价格的日期
    lowest_price_date = element.xpath('//div[@class="bigwidth"]/span[1]/font[3]/text()')[0][1:-1]
    # 该商品当前价格
    cur_price = float(
        utils.clean_text(element.xpath('//div[@class="bigwidth"]/span[1]/text()')[-1]).replace('\xa0当前价：', ''))

    logger.debug('最低价格： {}；最低价格日期： {}；当前价格：{}'.format(lowest_price, lowest_price_date, cur_price))

    temp = re.findall("<script type='text/javascript'>(.*?)</script>", html, re.S)[0]
    timestamp_list = []  # x 轴数据
    price_list = []  # y 轴数据

    # 填充 X 轴（时间线） 和 Y 轴（价格变化） 的数据
    result = re.findall("\[(.*?)\]", temp, re.S)
    for each in result:
        arr = each.split(",")
        timestamp_list.append(datetime.fromtimestamp(int(arr[0]) / 1000).strftime('%Y-%m-%d'))
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
    logger.debug('save html to: {}'.format(path))

    suggestion = get_buy_suggestion(cur_price, lowest_price, price_list)
    return utils.save_html_screenshot(temp_id, path), '小关觉得{}'.format(suggestion)


# 通过价格的对比获取购买建议（是否是最佳的购买时期）
# 1. 历史最低， 非常建议购买
# 2. 最低价格，可以购买
# 3. 当前价格大于最低价格，不建议购买
def get_buy_suggestion(cur_price, lowest_price, history_prices):
    # 比较是不是历史最低
    lower_than_history = True
    for each in history_prices:
        if cur_price >= each:
            lower_than_history = False

    if lower_than_history:
        result = '发现当前为历史最低价格，非常建议购买！！！'
    else:
        if cur_price > lowest_price:
            result = '现在不是最佳时刻！最低价格为：{}'.format(lowest_price)
        else:
            result = '现在是最佳时刻'

    logger.debug('购买意见为： {}'.format(result))
    return result
