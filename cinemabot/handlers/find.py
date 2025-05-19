from typing import Any

import aiogram
from aiogram import types

from cinemabot import dependencies, database
from cinemabot.infrastructure.clients import kinopoisk

router = aiogram.Router()


async def search_kinopoisk(film_name: str) -> dict[str, Any]:
    client = dependencies.get_kinopoisk_client()
    return await client.search_film_with_keyword(film_name)

async def search_google_watch(film_name) -> list[str]:
    client = dependencies.get_google_client()
    search_res = await client.search_google(f"{film_name} смотреть")
    return [res["link"] for res in search_res["items"]]

async def get_poster_size(film_info: dict[str, Any]) -> dict[str, Any]:
    client = dependencies.get_kinopoisk_client()
    film_info.update({"poster_size": await client.get_image_size(film_info["poster"]["url"])})
    return film_info

def select_optimal_link(ls: list[str]) -> str:
    for x in ls:
        if "rutube" in x:
            return x
        if "youtube" in x:
            return x
    for x in ls:
        if "kinogo" not in x:
            return x
    return ls[0]

@router.message()
async def find_command_executor(message: types.Message) -> None:
    search_name = message.text
    assert search_name is not None
    try:
        film_info = await search_kinopoisk(search_name)
    except kinopoisk.FilmNotFoundError:
        await message.answer(f"Не удалось найти фильм с названием '{search_name}'")
        return

    user = message.from_user
    assert user is not None
    user = user.username
    assert user is not None
    await database.insert(
        user_name=user, 
        message_text=search_name, 
        res_kinopoisk_id=film_info["id"], 
        film_name=film_info["name"]
    )
    
    film_name = film_info["name"]
    release_year = film_info["year"]
    genres = film_info["genres"]
    kp_rating = film_info["rating"]["kp"]
    imdb_rating = film_info["rating"]["imdb"]
    description = film_info["description"]
    links = await search_google_watch(film_info["name"])


    caption = f"""
*{film_name} [{release_year}]*\n
_Жанры_: {', '.join([genre["name"] for genre in genres]) if genres is not None else "Нет данных"}\n
_Рейтинг_: Кинопоиск: {f"{kp_rating}/10" if kp_rating != 0 else "Нет данных"}, IMDb: {f"{imdb_rating}/10" if imdb_rating != 0 else "Нет данных"}\n
_Описание_:\n{description if description else "Нет данных"}\n
_Смотреть_:\n{select_optimal_link(links)}\n
"""

    if (film_info["poster"]["url"] is not None):
        await message.answer_photo(
            photo=film_info["poster"]["url"],
            caption=caption,
            parse_mode="markdown",
        )
    else:
        await message.answer(
            text=caption,
            parse_mode="markdown",
        )


