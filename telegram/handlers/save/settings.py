from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import html

from keyboards.simple_row import make_row_keyboard

from data.texts.use_text_data import td
from handlers.not_handler_stuff import *
# from db_stuff.lan_alt import *

router = Router()

@router.message(F.text =='⚙️')
async def shopping(message: Message, state: FSMContext):
    await message.answer(
        text="⚙️",
        reply_markup=make_row_keyboard(['🏴🔄🏳️']+['❌'])
    )
    await state.set_state(SelectMode.settings)

@router.message(F.text =='🏴🔄🏳️', SelectMode.settings)
async def little_cancel(message: Message, state: FSMContext):
    await message.answer(
        text=td.base_data[await right_lang(message, state)]['#intros']["#select_language"],
        reply_markup=make_row_keyboard(list(td.lang_main['#flags'].keys()) + ['❌'])
    )
    await state.set_state(SelectMode.sel_articles)

@router.message(F.text.in_(td.lang_main['#flags']))
async def res_of_hello(message: Message, state: FSMContext):
    lang = td.lang_main['#flags'][message.text]
    set_new_lang(message.from_user.id, lang)
    await state.update_data(lang=lang)
    em = message.text
    prelang = ' ' + em + td.base_data[lang]['#main_data']["#name"] + em
    await message.answer(
        reply_markup=make_row_keyboard(["🗺️", "📖", "❓", "⚙️"]),
        text=td.base_data[lang]['#intros']["#new_language"] + prelang
    )    
    
