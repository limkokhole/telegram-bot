from app import bot
from app.utils import logger
from app import utils, services
import re


def handle_msg(msg):
    text = msg.text
    chat_id = msg.chat.id

    # 正则匹配 IP 地址
    if utils.check_ip(text):
        # 查询 IP 地址
        addr = services.query_ip(text)
        bot.sendMessage(chat_id=chat_id, text='该 IP 所处位置为： {}'.format(addr))

    # 检测是否为包含 BV 号
    elif text.startswith('BV') or text.startswith('bv') or text.startswith('https://b23.tv') or text.find(
            'www.bilibili.com/video') != -1:
        bv = text
        if text.startswith('https://b23.tv'):
            bv = text[15:27]
        if text.find('www.bilibili.com/video') != -1:
            bv = re.findall('www.bilibili.com/video/(.*?)\?', text, re.S)[0]

        print(bv)

        # 提取 B 站视频的封面图片
        pic_url = services.get_bilibili_cover_img(bv)
        bot.send_photo(chat_id=chat_id, photo=pic_url)

    # 检测是否为淘口令、京东链接等
    elif text.find('https://m.tb.cn/') != -1 or text.startswith('https://item.m.jd.com/product'):
        bot.sendMessage(chat_id=chat_id, text='正在为您查询该商品的价格哦，请稍等哈！')

        if text.find('https://m.tb.cn/') != -1:
            # 从淘口令中提取短连接
            tb_id = re.findall('https://m\.tb\.cn/(.*?)\?sm=', text, re.S)[0]
            item_link = 'https://m.tb.cn/{}'.format(tb_id)
        elif text.startswith('https://item.m.jd.com/product'):
            item_link = text
        else:
            logger.error('无效的商品链接： {}'.format(text))
            bot.sendMessage(chat_id=msg.chat.id, text='无效的商品链接')
            return

        img_path, suggestion = services.query_price(item_link)
        if not img_path and not suggestion:
            # 暂未收录该商品
            bot.sendMessage(chat_id=msg.chat.id, text='该商品暂未被收录哦！')
        else:
            bot.send_photo(chat_id=msg.chat.id, photo=open(img_path, 'rb'))
            bot.sendMessage(chat_id=msg.chat.id, text=suggestion)

    # 处理类似 /help 命令的文本
    elif text.startswith('/'):
        command = text[1:]
        bot.sendMessage(chat_id=chat_id, text=handle_command(command))
    else:
        bot.sendMessage(chat_id=chat_id, text=text)


def handle_command(cmd):
    logger.info("handle /{} command".format(cmd))

    if cmd == 'start':
        return start_handler()
    elif cmd == 'help':
        return help_handler()
    else:
        return '未知命令'


def start_handler():
    return '该机器人目前可支持查询 IP 所在位置和提取 B 站指定 BV 号视频的封面图片链接'


def help_handler():
    with open('./help.txt') as f:
        return f.read()
