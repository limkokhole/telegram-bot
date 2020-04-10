from app import redis
from app import utils
import json


# 检测该用户是否在数据库中，如果没有则添加
def add_new_user(msg):
    chat_id = msg.chat.id
    if not redis.hget('telegram-users', chat_id):
        data = {
            'nickname': utils.get_nickname(msg.chat)
        }
        redis.hset('telegram-users', chat_id, json.dumps(data))


# 获取所有用户的 chat id
def get_all_user_id():
    ids = []
    for i in redis.hgetall('telegram-users'):
        ids.append(str(i, encoding='utf-8'))
    return ids


if __name__ == '__main__':
    print(get_all_user_id())
