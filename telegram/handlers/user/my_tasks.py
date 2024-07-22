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

router = Router()

@router.message(F.text.lower() == 'мои поездки')  
async def get_tasks(message: Message, state: FSMContext):    
    await state.set_state(MyTasks.selectTasks)
    # print(state.get_state.)
    tasks = tw.select_dates_onready(pgsdata, message.from_user.id)
    # print(tasks)
    # print(tasks[0][0])
    # print(tasks[0][1].strftime("%Y.%m.%d"))
    tklav_raw = [[tasks[n][1].strftime("%d"), tasks[n][1].strftime("%m")]  for n in range(len(tasks))]
    tklav = [f"{tk+1}. {tklav_raw[tk][0]} {create_mounth_from_num(tklav_raw[tk][1])}" for tk in range(len(tklav_raw))] 

    ids = [tt[0]  for tt in tasks]
    
    await state.update_data(tasks_ids=ids)

    await message.answer(
        text = 'Выберите нужную поездку',
        reply_markup = make_row_keyboard(tklav + ['❌'])
    )

def create_mounth_from_num(num):
    months  = ('Января' , 'Февраля' , 'Марта' , 'Апреля' , 'Мая' , 'Июня' , 'Июля' , 'Августа' , 'Сентября' , 'Октября' , 'Ноября' , 'Декабря')
    return months[int(num) - 1].lower()

@router.message(MyTasks.selectTasks, F.text != '❌')
async def get_task(message: Message, state: FSMContext):    
    data =  await state.get_data()
    ids = data['tasks_ids']
    select_raw = int(message.text.split('.')[0]) - 1
    id_for = ids[select_raw]
    await state.update_data(task_id=id_for)
    await state.set_state(MyTasks.task)

    task_from_date = tw.select_task_by_id(pgsdata, id_for)
    if len(task_from_date) == 0:
        return 0
    # print(res)
    mm, dd = task_from_date[2].month, task_from_date[2].day
    if(not task_from_date[-1]):
        await message.answer(
            text = f'''Активная заявка на поездку на {dd} {create_mounth_from_num(mm)}.
Данное вами описание:
<i>{task_from_date[-2]}</i>
Мы скоро с вами свяжемся.''',
            parse_mode='html',
            reply_markup = make_row_keyboard(['Изменить', 'Удалить', '❌'])
        )
    else:
        await message.answer(
            text = f'''Запланированная поездка на {dd} {create_mounth_from_num(mm)}.
Начало поездки:
{task_from_date[3].strftime("%H:%M")}
''',
            parse_mode='html',
            reply_markup = make_row_keyboard(['Отменить', '❌'])
        )


@router.message(MyTasks.task, F.text == 'Удалить')
async def del_task(message: Message, state: FSMContext):    
    data =  await state.get_data()
    state.set_state(MyTasks.zero)
    id = data['task_id']
    tw.delete_by_id(pgsdata, id)
    await message.answer(
        text = "Поездка успешно удалена",
        reply_markup = main_menu()
    )

@router.message(MyTasks.task, F.text == 'Изменить')
async def alter_what(message: Message, state: FSMContext):  
    await state.set_state(MyTasks.alter)
    data =  await state.get_data()
    id = data['task_id']
    await message.answer(
        text = "Что именно вы хотите изменить в поездке?",
        reply_markup = make_row_keyboard(['Дата', 'Описание', '❌'])
    )

@router.message(MyTasks.alter, F.text == 'Дата')
async def alter_c(message: Message, state: FSMContext):  
    await state.set_state(MyTasks.alterDate)
    data =  await state.get_data()
    calendar = await SimpleCalendar(locale = await get_user_locale(message.from_user)).start_calendar()
    await message.answer(
        text = 'Выберите новую дату.',
        reply_markup = calendar
    )

@router.message(MyTasks.alter, F.text == 'Описание')
async def alter_d(message: Message, state: FSMContext):  
    await state.set_state(MyTasks.alterDescr)
    await message.answer(
        text = "Укажите новое описание",
        reply_markup = make_row_keyboard(['❌'])
    )

@router.message(MyTasks.alterDescr)
async def new_descr(message: Message,  state: FSMContext):
    data =  await state.get_data()
    id = data['task_id']
    tw.alt_task_descr(pgsdata, id, message.text)
    await state.set_state(MyTasks.zero)
    await message.answer(
            text = "Ваше новое описание сохранено",
            reply_markup = main_menu()
        )


@router.callback_query(SimpleCalendarCallback.filter(), MyTasks.alterDate)
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
            await callback_query.message.answer(
                f'''Вы выбрали дату {date.strftime("%d.%m.%Y")}. Теперь поездка запланирована на нее.''',
                reply_markup=main_menu()
            )
            await state.set_state(MyTasks.zero)
            data =  await state.get_data()
            id = data['task_id']
            tw.alt_task_date(pgsdata, id, date.strftime("%Y-%m-%d"))
