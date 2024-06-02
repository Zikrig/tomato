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
# import sys, os
# curDir = os.getcwd()
# sys.path.append(curDir)
# print(sys.path)
from keyboards.simple_row import make_row_keyboard
import keyboards.tomato_keyboard as kb
from tomato_tables.text_tool import *
from tomato_tables.people_tool import *
from tomato_tables.create_tables import *
from settings import *

router = Router()

# @router.message()
# async def process_raport_command(message: Message):
#     # print(rap_ready(tg_id))
#     await message.answer(
#         text='f',
#         reply_markup=make_row_keyboard(['/start', '/raport'])
#         )
    