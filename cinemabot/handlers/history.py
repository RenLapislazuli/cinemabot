import aiogram
from aiogram import types, filters

from cinemabot import database


router = aiogram.Router()

@router.message(filters.Command("history"))
async def start_command_executor(message: types.Message) -> None:
    user = message.from_user
    assert user is not None
    user = user.username
    assert user is not None
    ls = await database.get_user_history(user)
    await message.reply(
            f"*Последние 10 Запросов*\n\n"+
            "\n".join(f"{i}: {ls[-i][2]}" for i in range(1, min(11, len(ls) + 1))),
            parse_mode="markdown"
        )
