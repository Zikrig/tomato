import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from telegram.handlers.user import monkey, registration, task_user, my_tasks, get_horsehold_data
from telegram.handlers.admin import alter
# from telegram.handlers import last
# from local_data import LocalData
# from config import *
from telegram.checker.check import check
import os


# td = TD(os.getcwd()+'/telegram/data/texts/new_texts')
# os.chdir('C:/Users/user/Desktop/cool_things/chandles/chandles_grizik_test_docker/')

# Запуск бота
async def main():
    bot = Bot(token="365179646:AAHNK8e3HH6VJ9yMnWdy_LbIlN9SM_06vyk")
    dp = Dispatcher()

    dp.include_routers(monkey.router, registration.router, task_user.router, my_tasks.router, get_horsehold_data.router)
    dp.include_routers(alter.router)
    # dp.include_router(last.router)
    await dp.start_polling(bot)
    
async def checkercheck():
    # Корутина бота
    task = asyncio.create_task(main())
    
    while True:
        await asyncio.sleep(10)
        print('проспали еще 10 секунд')
        # Раз в пять секунд проверяем файл
        # Если там лежит 1 - останавливаем бота.
        if check():
            # Не сработало
            # was_cancelled = task.cancel()
            was_cancelled = task.result()
            print(was_cancelled)


if __name__ == "__main__":
    asyncio.run(checkercheck())