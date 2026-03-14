import yaml
from functools import wraps
from pathlib import Path
from typing import Callable, Any


def has_extension(ext: str, raise_not_found: bool = False):
    """Проверяет, относится ли файл к указанному расширению."""
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(**kwargs):
            file_path = kwargs.get('file_path')
            if not file_path:
                raise ValueError("Аргумент 'file_path' не найден.")
            if Path(file_path).suffix[1:] != ext:
                raise ValueError(f"Файл {file_path} имеет неверное расширение. Ожидалось {ext}")
            if not Path(file_path).exists() and raise_not_found:
                raise FileNotFoundError(f"Файл {file_path} не найден.")
            return func(**kwargs)
        return wrapper
    return decorator

@has_extension(ext="yaml", raise_not_found=True)
def load_yaml(file_path: Path) -> dict:
    """Загружает YAML-файл и возвращает его содержимое как словарь"""
    with open(file_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data:
        raise ValueError(f"Файл {file_path} пуст или повреждён.")
    return data