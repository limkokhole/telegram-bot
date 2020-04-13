from app import app, bot
from app import models
from app.handler import handle_msg, handle_callback_query
from app.utils import logger
from flask import request
import telegram


@app.route('/', methods=['GET'])
def index_get():
    return 'ok'


@app.route('/', methods=['POST'])
def index_post():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message:
        msg = update.message
        try:
            handle_msg(msg)
            models.add_new_user(msg)
        except Exception as e:
            logger.error(e)
            bot.sendMessage(chat_id=msg.chat.id, text='未知错误')

    elif update.callback_query:
        try:
            handle_callback_query(update.callback_query)
        except Exception as e:
            logger.error(e)
            chat_id = update.callback_query.message.chat.id
            bot.sendMessage(chat_id=chat_id, text='未知错误')
    return 'ok'


@app.route('/test', methods=['POST'])
def index_post2():
    return 'ok'


@app.route('/test')
def test():
    return 'ok'
