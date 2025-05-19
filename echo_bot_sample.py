import os
import asyncio

from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram import filters

bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher()

@dp.message(filters.Command("start"))
async def send_welcome(message: types.Message) -> None:
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram and ME.")


@dp.message()
async def echo(message: types.Message) -> None:
    assert message.text is not None
    await message.reply(message.text)

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
