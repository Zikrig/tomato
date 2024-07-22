from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from keyboards.simple_row import make_row_keyboard


from handlers.not_handler_stuff import *
import config
from data.texts.use_text_data import td
from db_stuff.lan_alt import *

router = Router()

@router.message(Command("help", "start"))
async def main_menu(message: Message, state: FSMContext):
    await message.answer(
        text = td.base_data[await right_lang(message, state)]['#intros']['#sec_hi'],
        reply_markup = make_row_keyboard(['🗺️', '📖', '❓', '⚙️'])
    )
    await state.set_state(SelectMode.base)

@router.message(F.text =='❌', SelectMode.read_articles)
async def little_cancel(message: Message, state: FSMContext):
    await message.answer(
        text = td.base_data[await right_lang(message, state)]['#intros']['#articles_back'],
        reply_markup = make_row_keyboard([itm for itm in td.lang_main['#art_by_lang'][await right_lang(message, state)]]+['❌'])
    )
    await state.set_state(SelectMode.sel_articles)

@router.message(F.text =='❌')
async def main_menu_cancel(message: Message, state: FSMContext):
    await message.answer(
        text = td.base_data[await right_lang(message, state)]['#intros']['#go_to_main'],
        reply_markup = make_row_keyboard(['🗺️', '📖', '❓', '⚙️'])
    )
    await state.set_state(SelectMode.base)
