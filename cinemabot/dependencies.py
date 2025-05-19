import aiogram
from aiogram.types import BotCommand

from cinemabot import handlers
from cinemabot.infrastructure import settings
from cinemabot.infrastructure.clients import kinopoisk, google

_settings: settings.Settings | None = None
_dispatcher: aiogram.Dispatcher | None = None
_bot: aiogram.Bot | None = None
_kinopoisk_client: kinopoisk.KinopoiskClient | None = None
_google_client: google.GoogleClient | None = None

def get_settings() -> settings.Settings:
    global _settings
    if _settings is None:
        _settings = settings.GetSettings()
    return _settings

async def get_dispatcher_and_bot() -> tuple[aiogram.Dispatcher, aiogram.Bot]:
    global _dispatcher, _bot
    if not _dispatcher or not _bot:
        settings = get_settings()
        _bot = aiogram.Bot(token=settings.bot.token)
        _dispatcher = aiogram.Dispatcher()  # TODO: add storage storage=RedisStorage2(host="cinemabot_redis")

        _dispatcher.include_router(handlers.start_router)
        _dispatcher.include_router(handlers.history_router)
        _dispatcher.include_router(handlers.stats_router)
        _dispatcher.include_router(handlers.help_router)
        _dispatcher.include_router(handlers.find_router)

        commands = [
            BotCommand(command="/start", description="Начать работу с ботом"),
            BotCommand(command="/stats", description="Посмотреть статистику показа фильмов"),
            BotCommand(command="/history", description="Посмотреть историю поиска"),
            BotCommand(command="/help", description="Посмотреть список команд"),
        ]
        await _bot.set_my_commands(commands)
    return _dispatcher, _bot


def get_kinopoisk_client() -> kinopoisk.KinopoiskClient:
    global _kinopoisk_client
    if _kinopoisk_client is None:
        settings = get_settings()
        _kinopoisk_client = kinopoisk.KinopoiskClient(
            base_url=settings.kinopoisk.base_url,
            api_key=settings.kinopoisk.api_key,
        )
    return _kinopoisk_client

def get_google_client() -> google.GoogleClient:
    global _google_client
    if _google_client is None:
        settings = get_settings()
        _google_client= google.GoogleClient(
            base_url=settings.google.base_url,
            api_key=settings.google.api_key,
            search_engine_key=settings.google.search_engine_id,
        )
    return _google_client
