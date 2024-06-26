import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from handlers.fruits import select_fruits, raport, mn

# Запуск бота
async def main():
    bot_commands = [
        BotCommand(command="/start", description="Отметить, что нужно сеять"),
        BotCommand(command="/raport", description="Получить информацию по посевам"),
    ]

    bot = Bot(token="7047861632:AAExHAlgPXYKxYtWql6ruaM0eMjMPbrcsIQ")
    dp = Dispatcher()

    dp.include_routers(select_fruits.router, raport.router, mn.router)

    # await bot.set_my_commands(bot_commands)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())