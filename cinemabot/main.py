import asyncio

# import aiohttp
# import aiogram
# from aiogram.types import BotCommand

from cinemabot import dependencies, background

async def main() -> None:
    dp, bot = await dependencies.get_dispatcher_and_bot()
    await dp.start_polling(bot)

if __name__ == '__main__':
    background.keep_alive()
    asyncio.run(main())
