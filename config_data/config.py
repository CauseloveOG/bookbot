from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str # Токен для доступа к ТГ боту
    admin_ids: list[int] # Список id админов

@dataclass
class Config:
    tg_bot: TgBot

# Создание функции, которая читает файл .env и возвращает
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None=None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        )
    )