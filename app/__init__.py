import config
from flask import Flask
import telegram
from telegraph import Telegraph
import redis as py_redis

app = Flask(__name__)
app.config.from_object(config)

bot = telegram.Bot(token=config.TELEGRAM_BOT_TOKEN)

telegraph = Telegraph()

redis = py_redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

from . import apis
