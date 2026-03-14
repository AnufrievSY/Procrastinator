from pydantic import BaseModel, Field

class TelegramConfig(BaseModel):
    """Конфигурация Telegram."""
    name: str = Field(..., description="Имя бота")
    token: str = Field(..., description="Токены для доступа к ботам Telegram")

class BaseConfig(BaseModel):
    Telegram: TelegramConfig = Field(..., description="Конфигурация Telegram")
