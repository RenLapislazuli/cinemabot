import aiogram
from aiogram import filters, types

router = aiogram.Router()

@router.message(filters.Command("start"))
async def start_command_executor(message: types.Message) -> None:
    await message.reply("Привет!\nЯ Cinemabot!\nДля поиска фильма или сериала отправь его название в сообщение.\n")
