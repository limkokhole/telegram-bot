from app import app
from app import jobs
import time
import threading
import schedule


# 订阅 azz.net 某一个用户的最新作品
def subscribe_azz_user(username):
    jobs.init_azz_net(username)
    schedule.every(1).days.do(jobs.azz_net_job, username)


def runnable():
    schedule.clear()
    # 爬取小谢尔顿最新一集
    schedule.every(6).hours.do(jobs.sheldon_job)

    subscribe_azz_user('wlop')
    subscribe_azz_user('void')
    subscribe_azz_user('BYJW')
    subscribe_azz_user('fleurdelys')

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    schedule_thread = threading.Thread(target=runnable)
    schedule_thread.start()

    app.run()
