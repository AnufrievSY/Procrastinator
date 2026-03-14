import datetime
from typing import Literal
import random
from config import DATA, bot


def parse_file(user_id: int | str):
    fp = DATA / f"{user_id}.txt"
    if not fp.exists():
        raise FileNotFoundError(fp)

    with open(fp, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # --- первая строка (метаданные)
    meta = {}
    for part in lines[0].split(";"):
        k, v = part.split("=")
        meta[k] = float(v)

    # --- интервалы времени
    periods = []
    start = None

    for line in lines[1:]:
        k, v = line.split("=")
        dt = datetime.datetime.strptime(v, "%d.%m.%Y %H:%M:%S")

        if k == "start":
            start = dt
        elif k == "end" and start:
            periods.append((start, dt))
            start = None

    return meta, periods


def filter_today(periods):
    """Интервалы за текущий день"""
    now = datetime.datetime.now()
    start_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = start_day + datetime.timedelta(days=1)

    return [
        (s, e)
        for s, e in periods
        if s >= start_day and s < end_day
    ]


def filter_week(periods):
    """Интервалы за текущую неделю"""
    now = datetime.datetime.now()

    start_week = now - datetime.timedelta(days=now.weekday())
    start_week = start_week.replace(hour=0, minute=0, second=0, microsecond=0)

    end_week = start_week + datetime.timedelta(days=7)

    return [
        (s, e)
        for s, e in periods
        if s >= start_week and s < end_week
    ]


def filter_month(periods):
    """Интервалы за текущий месяц"""
    now = datetime.datetime.now()

    start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    if start_month.month == 12:
        end_month = start_month.replace(year=start_month.year + 1, month=1)
    else:
        end_month = start_month.replace(month=start_month.month + 1)

    return [
        (s, e)
        for s, e in periods
        if s >= start_month and s < end_month
    ]


def calc_hours(periods):
    """
    Считает общее количество часов по интервалам.

    periods:
        [
            (start_datetime, end_datetime),
            ...
        ]

    Возвращает:
        float — количество часов
    """

    total_seconds = 0

    for start, end in periods:
        total_seconds += (end - start).total_seconds()

    return total_seconds / 3600


def run(mode: Literal["today", "week", "month"]):
    func = {
        "today": filter_today,
        "week": filter_week,
        "month": filter_month,
    }
    ui_mode = {
        "today": "сегодня",
        "week": "эту неделю",
        "month": "этот месяц",
    }

    answers = [
        "Неплохо, но потенциал ещё есть.",
        "Результат достойный, но рекорд впереди.",
        "Двигаешься в правильном направлении.",
        "Хороший старт, но это только начало.",
        "Выглядит солидно, но есть куда расти.",
        "Почти идеально — осталось чуть-чуть.",
        "Неплохо, но можно ещё эффективнее.",
        "Уже радует, но предел выше.",
        "Работодатель пока терпит.",
        "Сжигание бюджета идёт по плану.",
        "Финансовый ущерб в допустимых пределах.",
        "Есть прогресс в освоении зарплаты.",
        "Стабильно осваиваешь рабочие часы.",
        "Темп хороший, но рекорды ещё впереди.",
    ]
    for fp in DATA.glob("*.txt"):
        user_id = int(fp.stem)
        meta, periods = parse_file(user_id)
        if not periods:
            bot.send_message(user_id, f"За {ui_mode[mode]} - 0 рублей!\nВы очень плохо постарались")
            continue
        periods = func[mode](periods)
        cost = calc_hours(periods) * (meta["salary"] / meta["hours"])
        cost = round(cost, 2)
        bot.send_message(user_id, f"За {ui_mode[mode]} - {cost} рублей!\n{random.choice(answers)}")

if __name__ == "__main__":
    def patch(*args, **kwargs):
        print(*args, **kwargs)
    bot.send_message = patch
    run(mode="today")