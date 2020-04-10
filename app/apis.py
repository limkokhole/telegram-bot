from app import app, bot
from app import models
from app.handler import handle_msg
from flask import request
import telegram


@app.route('/', methods=['GET'])
def index_get():
    return 'ok'


@app.route('/', methods=['POST'])
def index_post():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    msg = update.message

    try:
        handle_msg(msg)
        models.add_new_user(msg)
    except Exception:
        bot.sendMessage(chat_id=msg.chat.id, text='未知错误')
    return 'ok'


