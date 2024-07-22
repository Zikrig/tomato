from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram import html

from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from os import getcwd
from datetime import datetime, timedelta

from aiogram.filters import Command
from aiogram_calendar import SimpleCalendar, get_user_locale, DialogCalendarCallback, DialogCalendar, SimpleCalendarCallback

from config import *
from telegram.keyboards.simple_row import *

# from telegram.data.texts.use_text_data import td
from telegram.handlers.not_handler_stuff import *

import table.work_with_database.task_work as tw
# import locale
# locale.setlocale(locale.LC_ALL, 'ru_RU')

router = Router()

@router.message(F.text.lower() == 'новая поездка')  
async def new_task(message: Message, state: FSMContext):    
    await state.set_state(NewTask.date)
    await message.answer(
        text = 'Выберите, когда желаете покататься!',
        reply_markup = make_row_keyboard(['Сегодня', 'Завтра', 'Другое', '❌'])
    )

@router.message(F.text.in_(['Сегодня', 'Завтра']), NewTask.date)  
async def days(message: Message, state: FSMContext):    
    if(message.text == 'Сегодня'):
        print(datetime.today())
        date = datetime.today()
    elif(message.text == 'Завтра'):
        date = datetime.today() + timedelta(days=1)
    await state.set_state(NewTask.descr)
    await state.update_data(date_of=date.strftime("%Y-%m-%d"))
    await message.answer(
        f'''Вы выбрали дату {date.strftime("%d.%m.%Y")}. Теперь, пожалуйста, опишите особые обстоятельства поездки
Например: \n "Мы будем всей семьей, два взрослых и два ребенка, опыт катания есть только у меня"\nили "Мне обязательно нужно успеть до 20:00, но можно перенести на завтра"''',
        reply_markup=make_row_keyboard(['❌'])
    )

@router.message(F.text.lower() == 'другое', NewTask.date)  
async def calend(message: Message, state: FSMContext):    
    await state.set_state(NewTask.dateCalendar)
    calendar = await SimpleCalendar(locale = await get_user_locale(message.from_user)).start_calendar()
    await message.answer(
        text = 'Выберите, когда желаете покататься!',
        reply_markup = calendar
    )
        

@router.callback_query(SimpleCalendarCallback.filter(), NewTask.dateCalendar)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData,  state: FSMContext):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2024, 1, 1), datetime(2030, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    
    calendar = await SimpleCalendar(locale = await get_user_locale(callback_query.from_user)).start_calendar()
    if selected:
        if(date < datetime.today()):
            await callback_query.message.answer(
                text='Похоже, вы планируете поездку на прошедшее время. Пожалуйста, выберите дату в будущем)',
                reply_markup = calendar
            )
        elif(date-timedelta(days=60) > datetime.today()):
            await callback_query.message.answer(
                text='Похоже, вы планируете поездку более чем на два месяца вперед. Укажите пожалуйста более близкую дату.',
                reply_markup = calendar
            )
        else:
            await state.update_data(date_of=date.strftime("%Y-%m-%d"))
            await state.set_state(NewTask.descr)
            await callback_query.message.answer(
                f'''Вы выбрали дату {date.strftime("%d.%m.%Y")}. Теперь, пожалуйста, опишите особые обстоятельства поездки
Например: \n "Мы будем всей семьей, два взрослых и два ребенка, опыт катания есть только у меня"\nили "Мне обязательно нужно успеть до 20:00, но можно перенести на завтра"''',
                reply_markup=make_row_keyboard(['❌'])
            )

@router.message(NewTask.descr)  
async def descr(message: Message, state: FSMContext): 
    describe = message.text
    if(len(describe) > 300):
        await message.answer(
            text = f'Длина вашего описания составила {len(describe)} знаков! Пожалуйста, постарайтесь уложиться в 300 знаков.'
        )
    else:
        tasks = tw.select_unready_tasks(pgsdata, message.from_user.id)
        if(tasks > 2): 
            await message.answer(
                text = f'''Извините, вы не можете иметь более трех заявок! Вы можете удалить или изменить те заявки, что у вас уже есть''',
                reply_markup = main_menu()
        )
        else:

            await state.set_state(NewTask.date)
            data = await state.get_data()
            date = data['date_of']
            await message.answer(
                text = f'''Отлично, вы создали заявку! Мы постараемся перезвонить вам в ближайшее время.
Если не получится, мы попытаемся связаться в телеграме. Обязательно дождитесь обратной связи!
Если вы ошиблись в своей заявке или передумали, вы можете изменить или удалить ее в разделе "мои заявки".
Приятного катания!
Ваша заявка на {date} с текстом {describe}''',
                reply_markup = main_menu()
            )

            task_data = [
                    message.from_user.id,
                    date,
                    '00:00',
                    describe,
                    'False'
            ]
            
            tw.put_task(pgsdata, task_data)
        