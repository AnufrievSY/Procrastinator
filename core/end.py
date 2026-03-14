from telebot import TeleBot, types
from config import DATA
import datetime


def register(bot: TeleBot) -> None:
    """Регистрирует обработчик команды /end"""

    @bot.message_handler(commands=["end"])
    def handle_end_command(message: types.Message) -> None:
        """Фиксирует начало прокрастинации"""
        user_id = message.from_user.id

        fp = DATA / f"{user_id}.txt"

        if not fp.exists():
            bot.send_message(message.chat.id, "Вы еще не зарегистрированы.")
            return

        dt = datetime.datetime.now()
        dt = dt.strftime("%d.%m.%Y %H:%M:%S")
        bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id,
                                 reaction=[types.ReactionTypeEmoji(emoji="👌")]
                                 )
        with open(fp, "a") as f:
            f.write(f"end={dt}\n")

