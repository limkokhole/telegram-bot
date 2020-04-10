from app import bot


def handle_msg(msg):
    text = msg.text
    chat_id = msg.chat.id

    bot.sendMessage(chat_id=chat_id, text=text)
