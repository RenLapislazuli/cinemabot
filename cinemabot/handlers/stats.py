import aiogram
from aiogram import types, filters

from cinemabot import database


router = aiogram.Router()

@router.message(filters.Command("stats"))
async def start_command_executor(message: types.Message) -> None:
    user = message.from_user
    assert user is not None
    user = user.username
    assert user is not None
    ls = await database.get_user_history(user)

    counters: dict[int, int] = {qr[3]: 0 for qr in ls}
    names: dict[int, int] = {qr[3]: qr[4] for qr in ls}
    for qr in ls:
        counters[qr[3]] += 1
    ls_ord = sorted(list(counters.items()), key=lambda x: x[1], reverse=True)
    kinids = [x[0] for x in ls_ord]

    await message.reply(
            f"*Статистика Запросов*\n\n"+
            "\n".join(
                f"""_{names[kinid]}_ - {counters[kinid]} запрос"""
            for kinid in kinids),
            parse_mode="markdown"
        )
