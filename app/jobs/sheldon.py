from app import bot, models
from app.utils import logger
import requests
from lxml import etree

sheldon_old_episode = None


def sheldon_job():
    global sheldon_old_episode

    resp = requests.get('https://91mjw.com/video/2248.htm')
    element = etree.HTML(resp.text)

    episodes = element.xpath('//*[@id="video_list_li"]/div/a')
    last_episode = episodes[-1].xpath('text()')[0]

    if not sheldon_old_episode:
        # 初始化
        sheldon_old_episode = last_episode

    if sheldon_old_episode != last_episode:
        sheldon_old_episode = last_episode
        # 有新的一集更新了，获取新的一集视频链接
        video_id = episodes[-1].xpath('@id')[0]
        video_link = 'https://91mjw.com/vplay/{}.html'.format(video_id)
        logger.info('更新了： {}'.format(video_link))
        # 推送给所有用户
        ids = models.get_all_user_id()
        print(ids)
        for user_id in ids:
            bot.sendMessage(chat_id=user_id, text=video_link)
    else:
        logger.info('未更新')
