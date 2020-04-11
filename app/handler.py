from app import bot
from app.utils import logger
from app import utils, services


def handle_msg(msg):
    text = msg.text
    chat_id = msg.chat.id

    if utils.check_ip(text):
        # 查询 IP 地址
        addr = services.query_ip(text)
        response = '该 IP 所处位置为： {}'.format(addr)
    elif text.startswith('BV') or text.startswith('bv'):
        # 提取 B 站视频的封面图片
        pic_url = services.get_bilibili_cover_img(text)
        response = pic_url
    elif text.startswith('/'):
        # 处理类似 /help 命令的文本
        command = text[1:]
        response = handle_command(command)
    else:
        response = text
    bot.sendMessage(chat_id=chat_id, text=response)


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
