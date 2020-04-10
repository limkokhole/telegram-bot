from app import app
from app.jobs import sheldon
import time
import threading
import schedule


def runnable():
    schedule.clear()
    # 爬取小谢尔顿最新一集
    schedule.every(1).hours.do(sheldon)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    schedule_thread = threading.Thread(target=runnable)
    schedule_thread.start()

    app.run()
