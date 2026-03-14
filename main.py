import sys
import json
import os
import threading
import time
import schedule
import core
import calendar
import datetime

def scheduled_tasks():
    """Настраивает расписание для автоматического запуска команд."""

    def run_month_if_last_day():
        """Запуск месячного отчёта только в последний день месяца"""
        now = datetime.datetime.now()
        last_day = calendar.monthrange(now.year, now.month)[1]

        if now.day == last_day:
            core.analytics.run("month")

    # каждый будний день
    schedule.every().monday.at("18:00").do(core.analytics.run, "today")
    schedule.every().tuesday.at("18:00").do(core.analytics.run, "today")
    schedule.every().wednesday.at("18:00").do(core.analytics.run, "today")
    schedule.every().thursday.at("18:00").do(core.analytics.run, "today")
    schedule.every().friday.at("18:00").do(core.analytics.run, "today")

    # каждую пятницу
    schedule.every().friday.at("18:05").do(core.analytics.run, "week")

    # каждый день проверяем не последний ли день месяца
    schedule.every().day.at("18:10").do(run_month_if_last_day)

    while True:
        schedule.run_pending()
        time.sleep(1)


def run():
    # фоновый поток для планировщика
    threading.Thread(target=scheduled_tasks, daemon=True).start()

    threading.Thread(target=core.run, daemon=True).start()

    print("[INFO] Проект запущен")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        raise


if __name__ == "__main__":
    run()