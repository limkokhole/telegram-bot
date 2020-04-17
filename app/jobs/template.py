from app import bot
from app import redis
from app.utils import logger


def init_job(key, first_page_func):
    if not redis.exists(key):
        # 不存在该键，说明是第一次订阅该博客
        for item in first_page_func():
            redis.hset(key, item['title'], item['url'])
    else:
        # 存在该键，检测是否有更新
        check_update(key, first_page_func)


def check_update(key, first_page_func):
    latest_item = first_page_func()[0]
    title, url = latest_item['title'], latest_item['url']

    if not redis.hexists(key, title):
        content = '您订阅的博客发布了新的文章《{}》，原文链接：\n{}'.format(title, url)
        logger.debug(content)
        bot.send_message(chat_id=1040935564, text=content)
        redis.hset(key, title, url)
    else:
        logger.debug('没更新')