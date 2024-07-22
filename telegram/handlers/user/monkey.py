from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram import html

from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from os import getcwd
from datetime import datetime

from aiogram_calendar import SimpleCalendar, get_user_locale, DialogCalendarCallback, DialogCalendar, SimpleCalendarCallback

from telegram.keyboards.simple_row import *
from telegram.handlers.not_handler_stuff import *

router = Router()

@router.message(Command('admin'),  SelectMode.user)
async def adm1(message: Message, state: FSMContext):
        await state.set_state(SelectMode.admin)
        await message.answer(
            text = 'Добро пожаловать в режим админа',
            reply_markup = admin_menu()
        )

@router.message(Command('admin'))  
async def adm2(message: Message, state: FSMContext):      
        await state.set_state(SelectMode.user)
        await message.answer(
            text = 'Добро пожаловать в режим юзера',
            reply_markup = main_menu()
        )

@router.message(StateFilter(default_state))
async def default_mode(message: Message, state: FSMContext):
        await state.set_state(SelectMode.user)
        await message.answer(
            text = 'Бот был перезагружен, возвращаемся в главное меню',
            reply_markup = main_menu()
        )
