from app import app
from app import jobs
import time
import threading
import schedule


# 订阅 azz.net 某一个用户的最新作品
def subscribe_azz_user(username):
    jobs.init_azz_net(username)
    schedule.every(1).days.do(jobs.azz_net_job, username)


def subscribe_meituan_blog():
    key = jobs.blog_key('meituan')
    func = jobs.get_meituan_first_page

    jobs.init_job(key, func)
    schedule.every(1).days.do(jobs.check_update, key, func)


def subscribe_taobao_blog():
    key = jobs.blog_key('taobao')
    func = jobs.get_taobao_first_page

    jobs.init_job(key, func)
    schedule.every(1).days.do(jobs.check_update, key, func)


def runnable():
    schedule.clear()
    # 爬取小谢尔顿最新一集
    schedule.every(6).hours.do(jobs.sheldon_job)

    # 订阅 azz.net 用户
    subscribe_azz_user('wlop')
    subscribe_azz_user('void')
    subscribe_azz_user('BYJW')
    subscribe_azz_user('fleurdelys')

    # 订阅博客
    subscribe_meituan_blog()
    subscribe_taobao_blog()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    schedule_thread = threading.Thread(target=runnable)
    schedule_thread.start()

    app.run()
