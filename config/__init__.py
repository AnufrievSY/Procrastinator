from pathlib import Path
from utils.readers import load_yaml
from .models import BaseConfig

# --- Пути проекта ---
# Общий путь
ROOT: Path = Path(__file__).parent.parent
# Путь к хранилищу с временными файлами
DATA: Path = ROOT / "data"
DATA.mkdir(exist_ok=True)

# --- Загрузка конфигурации ---
settings = BaseConfig(**load_yaml(file_path=ROOT / "config" / "config.yaml"))

# --- Telegram-бот ---
import telebot
bot: telebot.TeleBot = telebot.TeleBot(token=settings.Telegram.token, threaded=False)