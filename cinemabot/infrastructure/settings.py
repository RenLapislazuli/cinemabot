import os
from dataclasses import dataclass

@dataclass
class BotSettings:
    token: str

@dataclass
class KinopoiskSettings:
    api_key: str
    base_url: str = "https://api.kinopoisk.dev/"

@dataclass
class GoogleSettings:
    api_key: str
    search_engine_id: str
    base_url: str = "https://www.googleapis.com/"


@dataclass
class Settings:
    bot: BotSettings
    kinopoisk: KinopoiskSettings
    google: GoogleSettings

def GetSettings():
    bot_token = os.environ.get("BOT_TOKEN")
    assert bot_token is not None, "environmental variable BOT_TOKEN is not set"

    kinopoisk_api_key = os.environ.get("KINOPOISK_API_KEY")
    assert kinopoisk_api_key is not None, "environmental variable KINOPOISK_API_KEY is not set"

    google_api_key = os.environ.get("GOOGLE_API_KEY")
    assert google_api_key is not None, "environmental variable GOOGLE_API_KEY is not set"

    google_search_engine_id = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")
    assert google_search_engine_id is not None, "environmental variable GOOGLE_API_KEY is not set"

    return Settings(
        bot=BotSettings(
            token=bot_token,
        ),
        kinopoisk=KinopoiskSettings(
            api_key=kinopoisk_api_key,
        ),
        google=GoogleSettings(
            api_key=google_api_key,
            search_engine_id=google_search_engine_id,
        ),
    )
