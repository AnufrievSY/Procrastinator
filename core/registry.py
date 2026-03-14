from telebot import TeleBot, types
from config import DATA


def register(bot: TeleBot) -> None:
    """Регистрирует обработчик команды /registry"""

    @bot.message_handler(commands=["registry"])
    def handle_registry_command(message: types.Message) -> None:
        """
        - Проверяет регистрацию
        - Если нет — спрашивает данные
        """
        user_id = message.from_user.id

        fp = DATA / f"{user_id}.txt"

        if fp.exists():
            bot.send_message(message.chat.id, "Регистрация уже завершена.")
            return

        msg = bot.send_message(
            message.chat.id,
            "Укажи свою месячную зарплату (в рублях):"
        )
        bot.register_next_step_handler(msg, ask_salary, user_id)


    def ask_salary(message: types.Message, user_id: int) -> None:
        """Получаем зарплату"""

        try:
            salary = float(message.text.replace(" ", "").replace(",", "."))
        except ValueError:
            msg = bot.send_message(message.chat.id, "Введи число. Например: 120000")
            bot.register_next_step_handler(msg, ask_salary, user_id)
            return

        msg = bot.send_message(
            message.chat.id,
            "Сколько часов в месяц ты работаешь?"
        )
        bot.register_next_step_handler(msg, ask_hours, user_id, salary)


    def ask_hours(message: types.Message, user_id: int, salary: float) -> None:
        """Получаем количество часов и сохраняем"""

        try:
            hours = float(message.text.replace(",", "."))
        except ValueError:
            msg = bot.send_message(message.chat.id, "Введи число. Например: 160")
            bot.register_next_step_handler(msg, ask_hours, user_id, salary)
            return

        fp = DATA / f"{user_id}.txt"

        with open(fp, "w", encoding="utf-8") as f:
            f.write(f"salary={salary};hours={hours}\n")

        bot.send_message(
            message.chat.id,
            f"Регистрация завершена."
        )