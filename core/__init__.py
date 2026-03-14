from. import analytics
import importlib
import os
import pkgutil
import time
import requests.exceptions
from telebot import types, TeleBot
import config

def _load_command_modules(bot: TeleBot) -> TeleBot:
    package_name = "core"
    package_path = os.path.dirname(__file__)

    for _, module_name, is_pkg in pkgutil.iter_modules([package_path]):
        if is_pkg:
            continue
        try:
            module = importlib.import_module(f"{package_name}.{module_name}")
            if hasattr(module, "register") and callable(module.register):
                module.register(bot)
                print(f"[INFO] Модуль команд '{module_name}' успешно зарегистрирован.")
            else:
                print(f"[WARNING] Модуль '{module_name}' не содержит функции register.")
        except Exception as exc:
            print(f"[ERROR] Ошибка при загрузке модуля '{module_name}': {exc}")

    return bot


def _configure_bot_commands(bot: TeleBot) -> TeleBot:
    private_commands = [
        types.BotCommand("registry", "Регистрация"),
        types.BotCommand("start", "Начать работу"),
        types.BotCommand("end", "Закончить работу"),
    ]
    bot.set_my_commands(
        private_commands,
        scope=types.BotCommandScopeAllPrivateChats()
    )
    return bot

def run(bot: TeleBot = config.bot) -> None:
    """
    Запускает телеграм-бота: регистрирует команды и запускает цикл polling.
    Обрабатывает ошибки, чтобы бот автоматически перезапускался.
    """

    bot = _load_command_modules(bot)
    bot = _configure_bot_commands(bot)

    while True:
        try:
            print(f"[INFO] Бот запущен. Ожидаем сообщения...")
            bot.polling(none_stop=True, interval=1)
        except requests.exceptions.ReadTimeout:
            print(f'[WARNING] ReadTimeout: restart...')
            bot.stop_polling()
            time.sleep(5)
        except requests.exceptions.ConnectionError:
            print(f'[WARNING] ConnectionError: restart...')
            bot.stop_polling()
            time.sleep(10)
        except KeyboardInterrupt:
            print(f"[INFO] Остановка бота по Ctrl+C.")
            bot.stop_polling()
            break
        except Exception as exc:
            print(f"[ERROR] Ошибка в работе бота: {exc}")
            bot.stop_polling()
            time.sleep(5)


if __name__ == "__main__":
    run()
