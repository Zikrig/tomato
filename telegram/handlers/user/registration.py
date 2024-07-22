from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram import html
from os import getcwd
import codecs

from aiogram.filters import Command
from telegram.keyboards.simple_row import *
# from aiogram.utils.keyboard import ReplyKeyboardBuilder
# import config

# from telegram.data.texts.use_text_data import td
# from db_stuff.questions import *
from telegram.handlers.not_handler_stuff import *
# from db_stuff.lan_alt import *
from config import *
import table.work_with_database.put_data as pd
# from config import pgsdata

router = Router()

# @router.message()
# async def main_menu(message: Message, state: FSMContext):
#     # message_data = {message}
#     print(message.photo)
#     await message.answer(
#         text = 'hi',
#         reply_markup = make_row_keyboard(['/start'])
#     )

@router.message(F.text =='Анкета')
async def little_cancel(message: Message, state: FSMContext):
    await state.set_state(Reg.noth)
    pers = pd.select_person(pgsdata, message.from_user.id)
    # print(pers)
    if len(pers) == 6:
        photo = FSInputFile(path=f"{avas_dir}/{pers[5]}")
        # print(photo)
        await message.answer_photo(
            photo=photo,
            caption = f'''Ваша анкета:
<b>Имя:</b>\t{pers[2]}
<b>Телефон:</b>\t{pers[3]}
<b>Описание:</b> \t{pers[4]}''',
            parse_mode = 'html',
            reply_markup = make_row_keyboard([
            'Изменить анкету',
            '❌'
            ])
        )
    else:
          await message.answer(
            text = "Мы пока не знакомы. Как насчет зарегистрироваться?",
            parse_mode = 'html',
            reply_markup = make_row_keyboard([
            'Изменить анкету',
            '❌'
            ])
        )

@router.message(F.text =='❌')
async def little_cancel(message: Message, state: FSMContext):
    await state.set_state(Reg.noth)
    await message.answer(
        text = 'Вы вернулись на главную.',
        reply_markup = main_menu()
    )

@router.message(F.text.in_(['/start','Изменить анкету']))
async def reg_start(message: Message, state: FSMContext):
        await state.set_state(SelectMode.user)
        await state.set_state(Reg.name)
        await message.answer(
            text = 'Как нам вас называть? Пожалуйста, введите свое имя',
            reply_markup = make_row_keyboard([
                '❌'
                ])
        )       

@router.message(Reg.name)  
async def reg_name(message: Message, state: FSMContext):
        if(len(message.text) < 4 or len(message.text) > 50):
            await message.answer(
                text = 'Нам нужно ваше имя, чтобы связаться с вами. Пожалуйста, укажите его.',
            )
        else:
            # user_name = message.text
            await state.update_data(user_name=message.text)
            await state.set_state(Reg.phone)
            await message.answer(
                text = 'Спасибо! Теперь, пожалуйста, укажите ваш контактный телефон, чтобы мы вам перезвонили.',
                reply_markup = make_row_keyboard([
                '❌'
                ])
            )
            
@router.message(Reg.phone)  
async def reg_describe(message: Message, state: FSMContext):
        if(len(message.text) < 7 or len(message.text) > 15):
            await message.answer(
                text = "Это не похоже на номер телефона. Пожалуйста, введите номер, чтобы мы смогли с вами связаться.",
            )
        else:
            # user_phone = message.text
            await state.update_data(user_phone=message.text)
            await state.set_state(Reg.describe)
            await message.answer(
                text = '''Нам нужно узнать о вас кое-что. Ответив на эти вопросы вы сильно сэкономите время телефонного разговора.\n
Сколько вам лет?
Сколько вы весите?
Какой у вас опыт катания?''',
                reply_markup = make_row_keyboard([
                    '❌'
                    ])
                )
            
@router.message(Reg.describe)  
async def reg_describe(message: Message, state: FSMContext):
        if(len(message.text) > 300):
            await message.answer(
                text = f"Простите, но у вас целых {len(message.text)} символов, а ограничение - 300 символов.",
            )
        else:
            # user_describe = message.text
            await state.update_data(user_describe=message.text)
            await state.set_state(Reg.photo)
            await message.answer(
                text = '''Пожалуйста, пришлите ваше фото''',
                reply_markup = make_row_keyboard([
                    '❌'
                    ])
                )
            
@router.message(Reg.photo)  
async def reg_describe(message: Message, state: FSMContext):
    if(message.photo == '' or message.photo == None):
        await message.answer(
            text = f"Вы не прислали фото. Пожалйста, пришлите фото",
        )
    else:
        # user_describe = message.text
        user_id = message.from_user.id
        ava_name = f"ava_{user_id}.jpg"
        photo_path = f"{avas_dir}/{ava_name}"
        await message.bot.download(
        message.photo[-1],
        destination=photo_path
        )
        data = await state.get_data()
        await state.set_state(Reg.noth)
        await message.answer(
            text = '''Большое спасибо за заполнение анкеты!''',
            reply_markup = main_menu()
            )
        person_data = (user_id, data['user_name'], data['user_phone'], data['user_describe'], ava_name)
        pd.person_gen(pgsdata, person_data)