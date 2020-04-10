import os
from flask import Flask
import telegram
from telegraph import Telegraph
import redis as py_redis

app = Flask(__name__)

bot = telegram.Bot(token=os.environ.get('TELEGRAM_BOT_TOKEN'))

telegraph = Telegraph()

redis = py_redis.Redis(host='localhost', port=6379)

from . import apis
