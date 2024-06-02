from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram import html
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter

# from re import fullmatch
import sys, os
# curDir = os.getcwd()
# sys.path.append(curDir)
# print(sys.path)
from keyboards.simple_row import make_row_keyboard
import keyboards.tomato_keyboard as kb
from tomato_tables.text_tool import *
from tomato_tables.people_tool import *

router = Router()

class GetFruits(StatesGroup):
    chose_fruits = State()
    fruits_end = State()


# Создаем объект инлайн-клавиатуры
# arg = [
#         ['Апельсин', 'fr-Orange'],
#         ['Банан', 'fr-Banane'],
#         ['Малина', 'fr-Raspberry'],
#     ]

pre_fruits = get_fruits_from_file()#[ff[1:-1].split(',') for ff in get_fruits_from_file()]

for fr in range(len(pre_fruits)):
    pre_fruits[fr][1] = 'fr-'+pre_fruits[fr][1]
# print(pre_fruits)

# keybrd = kb.really_big(arg)
kb_ex = kb.keyboard_state(pre_fruits)
keybrd = kb_ex.really_big()

# , F.data.startswith('🌱')
@router.message(CommandStart())
# @router.message(F.data.startswith('🌱'))
async def process_start_command(message: Message, state: FSMContext):
    kb_ex = kb.keyboard_state(pre_fruits)
    await state.clear()
    user_data = await state.get_data()
    # if(not 'mid' in user_data):
    await message.answer(
        text='Выберите, что будем сажать!',
        # reply_markup=keybrd
        reply_markup=kb_ex.really_big()
        )
    await state.update_data(kb_ex=kb_ex, mid=message.message_id)
    await state.set_state(GetFruits.chose_fruits)

@router.callback_query(F.data.startswith('fr-'))
async def alt_fruit(callback: CallbackQuery, state: FSMContext):
    callback_data = callback.data
    user_data = await state.get_data()
    # print(user_data)
    mid = user_data['mid']
    # print(callback.message.message_id)
    if(mid == callback.message.message_id-1):
        if(callback_data == 'fr-CLOSE'):
            # print(callback.message.from_user.id)
            # print(user_data['kb_ex'].create_list())
            user_data['kb_ex'].create_list()
            # print(callback.message.from_user.id,
            #     user_data['kb_ex'].lat_fruits)
            alt_person(
                callback.message.chat.id%10000,
                user_data['kb_ex'].lat_fruits
            )
            await callback.message.answer(text="Ваши праметры приняты!")
            await state.set_state(GetFruits.fruits_end)
            await callback.message.delete_reply_markup()
        else:
            user_data = await state.get_data()
            kb_ex = user_data['kb_ex']
            kb_ex.alt_btn_state(callback_data)
            keybrd = kb_ex.really_big()
            await callback.message.edit_reply_markup(
                reply_markup=keybrd
            )
            await state.update_data(kb_ex=kb_ex)