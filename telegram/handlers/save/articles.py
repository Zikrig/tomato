from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile

from keyboards.simple_row import *

from handlers.chandles import SelectMode
import config
from data.texts.use_text_data import td
from handlers.not_handler_stuff import *
from db_stuff.lan_alt import *
router = Router()

# Вход в раздел статьи
@router.message(F.text =='📖')
async def get_article(message: Message, state: FSMContext):
    await message.answer(
        text = td.base_data[await right_lang(message, state)]['#intros']["#articles"],
        reply_markup =  keyboard_proto([itm for itm in td.lang_main['#art_by_lang'][await right_lang(message, state)]]+['❌']),
        parse_mode='html'
    )
    await state.set_state(SelectMode.sel_articles)

# Вход в блок со статьями (например СВЕЧИ)
@router.message(F.text.in_(td.lang_main['#all_art_blocks']), SelectMode.sel_articles)
async def articles_next(message: Message, state: FSMContext):
    await state.update_data(art1=message.text)
    await message.answer(
        text=td.base_data[await right_lang(message, state)]['#articles'][message.text]['#describe'],
        reply_markup = keyboard_proto([itm for itm in td.base_data[await right_lang(message, state)]['#articles'][message.text]['#articles']]+['❌']),
        parse_mode='html'
    )
    await state.set_state(SelectMode.read_articles)

# Просмотр статьи (например ЖИДКАЯ СВЕЧА)
@router.message(F.text.in_(td.lang_main['#all_articles']), SelectMode.read_articles)
async def articles_fin(message: Message, state: FSMContext):
    data = await state.get_data()
    article1 = data.get("art1", "<something unexpected>")
    
    await state.set_state(SelectMode.read_articles)
    if '#photo_paths' in td.base_data[await right_lang(message, state)]['#articles'][article1] and message.text in td.base_data[await right_lang(message, state)]['#articles'][article1]['#photo_paths']:
        pht = FSInputFile(config.images_dir + '/' + td.base_data[await right_lang(message, state)]['#articles'][article1]['#photo_paths'][message.text])
        await message.answer_photo(
            photo = pht,
            caption = td.base_data[await right_lang(message, state)]['#articles'][article1]['#articles'][message.text],
            parse_mode='html'
            )
    else:
        await message.answer(
            text=td.base_data[await right_lang(message, state)]['#articles'][article1]['#articles'][message.text],
            parse_mode='html'
            )