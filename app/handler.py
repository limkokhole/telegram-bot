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
    elif text.startswith('BV') or text.startswith('bv') or text.startswith('https://b23.tv'):
        if text.startswith('https://b23.tv'):
            text = text[15:27]
        # 提取 B 站视频的封面图片
        pic_url = services.get_bilibili_cover_img(text)
        bot.send_photo(chat_id=chat_id, photo=pic_url)

    # 检测是否为淘口令
    elif text.find('https://m.tb.cn/') != -1:
        bot.sendMessage(chat_id=chat_id, text='正在为查询该商品的价格，请稍等哈！')
        # 从淘口令中提取短连接
        tb_id = re.findall('https://m\.tb\.cn/(.*?)\?sm=', text, re.S)[0]
        short_link = 'https://m.tb.cn/{}'.format(tb_id)
        # 通过短连接获取到淘宝真实的商品链接
        link = services.convert_tb_link(short_link)
        img_path = services.query_price(link)
        bot.send_photo(chat_id=msg.chat.id, photo=open(img_path, 'rb'))

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
