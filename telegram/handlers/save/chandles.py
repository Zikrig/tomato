from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import html
from os import getcwd

from keyboards.simple_row import *
# from aiogram.utils.keyboard import ReplyKeyboardBuilder
import config

from data.texts.use_text_data import td
from db_stuff.questions import *
from handlers.not_handler_stuff import *
from db_stuff.lan_alt import *

router = Router()

@router.message(F.text =='🗺️')
async def map_work(message: Message, state: FSMContext):
    await message.answer(
        text=td.base_data[await right_lang(message, state)]['#intros']["#geo"],
        reply_markup=keyboard_proto([itm for itm in td.base_data[await right_lang(message, state)]['#geo_spots']]+['❌']),
        parse_mode='html'
    )
    await state.set_state(SelectMode.get_geo)

@router.message(F.text.in_(td.lang_main['#all_spots']), SelectMode.get_geo)
async def get_geo(message: Message, state: FSMContext):
    await message.answer(
        text = td.base_data[await right_lang(message, state)]['#geo_spots'][message.text]['#describe'],
        parse_mode='html'
    )

    await message.answer_location(
        latitude = td.base_data[await right_lang(message, state)]['#geo_spots'][message.text]['#latitude'],
        longitude = td.base_data[await right_lang(message, state)]['#geo_spots'][message.text]['#longitude']
    )
    

@router.message(SelectMode.question, F.text == '❓')
async def ask_a_question(message: Message, state: FSMContext):
    await message.answer(
        text=td.base_data[await right_lang(message, state)]['#intros']["#quest"],
        reply_markup=make_row_keyboard(['❓', '❌'])
    )
    await state.set_state(SelectMode.question)

@router.message(F.text == '❓')
async def ask_a_question_intro(message: Message, state: FSMContext):
    await message.answer(
        text=td.base_data[await right_lang(message, state)]['#intros']["#quest_hi"],
        reply_markup=make_row_keyboard(['❓', '❌'])
    )
    await state.set_state(SelectMode.question)

@router.message(SelectMode.question, F.text != '❌')
async def get_geo(message: Message, state: FSMContext):
    add_question(message.from_user.id, message.text)
    await message.answer(
        text = td.base_data[await right_lang(message, state)]['#intros']["#quest_res"],
        reply_markup=make_row_keyboard(['🗺️', '📖', '❓', '⚙️'])
    )
    await state.set_state(SelectMode.base)