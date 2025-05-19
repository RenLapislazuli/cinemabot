import aiogram
from aiogram import filters, types

router = aiogram.Router()

class BadCommandFilter(filters.BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.text is None or message.text[0] == '/'

@router.message(filters.Command(commands=["help"]))
async def help_command_executor(message: types.Message) -> None:
    command_help = {
        "/start": "   Начать работу с ботом ",
        "[название фильма]": " Найти фильм по названию ",
        "/history": "Посмотреть историю поиска ",
        "/stats": "    Посмотреть статистику показа фильмов ",
        "/help": "      Посмотреть список команд с их описанием. *(Вы здесь)*",
    }

    command_help_text = ";\n\n".join(map(lambda x: f"`{x[0]}`: {x[1]}", command_help.items()))

    await message.answer(
        f"Список команд:\n\n {command_help_text}",
        parse_mode="markdown",
    )

@router.message(BadCommandFilter())
async def unknown_command_help_executor(message: types.Message) -> None:
    await message.reply(
        f"""Неизвестная команда '{message.text}'.\n\n"""
        "Список доступных команд доступен по команде '/help',", 
    parse_mode="markdown")
