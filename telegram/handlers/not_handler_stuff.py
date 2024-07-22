from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

# import db_stuff.lan_alt

class SelectMode(StatesGroup):
    user = State()
    admin = State()

class Reg(StatesGroup):
    noth = State()
    name = State()
    phone = State()
    describe = State()
    photo = State()
    
class NewTask(StatesGroup):
    date = State()
    dateCalendar = State()
    descr = State()
    
class MyTasks(StatesGroup):
    selectTasks = State()
    task = State()
    alter = State()
    alterDate = State()
    alterDescr = State()
    zero = State()

class AlterAdmin(StatesGroup):
    alterGlobal = State()
    alterDescribe = State()
    alterCoords = State()
    alterPhotos = State()
    addPhoto = State()