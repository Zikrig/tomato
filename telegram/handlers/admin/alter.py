from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram import html

from aiogram.types import Message,FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from os import getcwd
from datetime import datetime

from aiogram.filters import Command
from aiogram_calendar import SimpleCalendar, get_user_locale, DialogCalendarCallback, DialogCalendar, SimpleCalendarCallback


from telegram.keyboards.simple_row import *
# from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import lc, horseh_dir

# from telegram.data.texts.use_text_data import td
# from db_stuff.questions import *
from telegram.handlers.not_handler_stuff import *
from roles import *

router = Router()

@router.message(F.text == 'Изменить описание',  SelectMode.admin)
async def admd1(message: Message, state: FSMContext):
    await state.set_state(AlterAdmin.alterGlobal)
    await message.answer(
        text = 'Вот как выглядит анкета прямо сейчас. Что именно вы хотите поменять или добавить?',
        reply_markup = make_row_keyboard([
            'Описание',
            'Координаты',
            'Фото',
            '❌'
            ])
    )
    if(len(lc.imgs)>0):
        album_builder = MediaGroupBuilder(
        caption=lc.describe
        )
        for photo_id in lc.imgs:
            album_builder.add(
                type="photo",
                media=FSInputFile(photo_id)
            )

        await message.answer_media_group(
            media=album_builder.build(), 
            caption=lc.describe,
            # reply_markup = make_row_keyboard([
            #     '❌'
            # ])
        )
    else:
            await message.answer(
            text=lc.describe,
            # reply_markup = make_row_keyboard([
            #     '❌'
            # ])
        )
    if(not lc.coord1 is None):
        await message.answer_location(latitude=lc.coord1, longitude=lc.coord2)


@router.message(F.text == 'Описание', AlterAdmin.alterGlobal)
async def opis(message: Message, state: FSMContext):
    await state.set_state(AlterAdmin.alterDescribe)
    await message.answer(
        text = 'Введите новое описание. Вы можете использовать функционал телеграма - курсив и прочее.',
        parse_mode='html',
        reply_markup = make_row_keyboard([
            '❌'
            ])
    )

@router.message(AlterAdmin.alterDescribe)
async def opis2(message: Message, state: FSMContext):
    await state.set_state(SelectMode.admin)
    lc.set_descr(message.text)
    # print(lc.descr)
    await message.answer(
        text = 'Описание изменено!',
        parse_mode='html',
        reply_markup = admin_menu()
    )

@router.message(F.text == 'Координаты', AlterAdmin.alterGlobal)
async def opis3(message: Message, state: FSMContext):
    await state.set_state(AlterAdmin.alterCoords)
    await message.answer(
        text = 'Введите новые координаты на отдельных строках без посторонних симоволов, например:\n45.422\n25.44332',
        # parse_mode='html',
        reply_markup = make_row_keyboard([
            '❌'
            ])
    )

@router.message(AlterAdmin.alterCoords)
async def opis4(message: Message, state: FSMContext):
    await state.set_state(SelectMode.admin)
    lc.set_coords(message.text)
    await message.answer(
        text = 'Координаты изменены!',
        # parse_mode='html',
        reply_markup = admin_menu()
    )

@router.message(F.text =='❌', AlterAdmin)
async def little_cancel(message: Message, state: FSMContext):
    # await state.set_state(SelectMode.admin)
    await message.answer(
        text = 'Вы вернулись на главную.',
        reply_markup = admin_menu()
    )

@router.message(F.text == 'Фото', AlterAdmin.alterGlobal)
async def opis(message: Message, state: FSMContext):
    await state.set_state(AlterAdmin.alterPhotos)
    await message.answer(
        text = 'Вы можете удалить или добавить фото',
        parse_mode='html',
        reply_markup = make_row_keyboard([f"{i+1} ❌" for i in range(len(lc.imgs))]+['➕','❌'])
    )

@router.message(AlterAdmin.alterPhotos, F.text == '➕')
async def al(message: Message, state: FSMContext):
    await state.set_state(AlterAdmin.addPhoto)
    await message.answer(
        text = 'Отправьте новое фото',
        reply_markup = make_row_keyboard([f"{i+1} ❌" for i in range(len(lc.imgs))]+['➕','❌'])
    )

@router.message(AlterAdmin.addPhoto)
async def al(message: Message, state: FSMContext):
    if(message.photo == '' or message.photo == None):
        await message.answer(
            text = f"Вы не прислали фото. Пожалуйста, пришлите фото",
        )
    else:
        # user_describe = message.text
        await state.set_state(AlterAdmin.alterPhotos)
        user_id = message.from_user.id
        horseh_name = f"horse_{user_id}_{str(datetime.now().time()).replace('.', '').replace(':', '')}.jpg"
        photo_path = f"{horseh_dir}/{horseh_name}"
        await message.bot.download(
        message.photo[-1],
        destination=photo_path
        )

    lc.add_photo_to_file(horseh_name)
    await message.answer(
        text = 'Большое спасибо добавление нового фото!',
        reply_markup = make_row_keyboard([f"{i+1} ❌" for i in range(len(lc.imgs))]+['➕','❌'])
    )

@router.message(AlterAdmin.alterPhotos)
async def al(message: Message, state: FSMContext):
    num, _ = message.text.split()
    lc.del_photo_by_num(int(num)-1)
    await message.answer(
        text = 'Фото успешно удалено',
        reply_markup = make_row_keyboard([f"{i+1} ❌" for i in range(len(lc.imgs))]+['➕','❌'])
    )