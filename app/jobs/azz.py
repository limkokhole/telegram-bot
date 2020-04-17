import requests
from lxml import etree
from app import bot, redis, models
from app.utils import logger


def key(username):
    return 'telegram:jobs:history:azz_{}'.format(username)


def get_first_page_urls(username):
    resp = requests.get('https://azz.net/{}'.format(username))
    return etree.HTML(resp.text).xpath('//div[@class="post-item-content"]/p/img/@data-src')


# ----------------------- public method -----------------------

# 初始化历史数据，将第一页所有的图片 urls 存储到 redis 集合中
def init_azz_net(username):
    for url in get_first_page_urls(username):
        redis.sadd(key(username), url)


# 轮询任务，检测是否发布了新的作品
def azz_net_job(username):
    latest_pic_url = get_first_page_urls(username)[0]
    # 判断最新一张是否在历史中，如果不在说明为新的作品
    if not redis.sismember(key(username), latest_pic_url):
        # 发现新的作品，推送：
        logger.info('检测到 {} 有新的作品发布'.format(username))
        for user_id in models.get_all_user_id():
            content = '{} 发布了新的作品，图片链接为： \n{}'.format(username, latest_pic_url)
            bot.send_message(chat_id=user_id, text=content)
        redis.sadd(key(username), latest_pic_url)
