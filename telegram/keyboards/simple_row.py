from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

def keyboard_proto(items: list[str]) -> ReplyKeyboardMarkup:
    if(len(items) <=2):
        row = [KeyboardButton(text=item) for item in items]
        return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=True)
    
    rows = []
    for ii in range(len(items)//2 + 1):
        rows.append([KeyboardButton(text=item) for item in items[ii*2:ii*2+2]])
    # print(items)
    # print(rows)
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

def main_menu():
    return make_row_keyboard([
                'Анкета',
                'Новая поездка',
                'Мои поездки',
                'Конюшня'
                ])

def admin_menu():
    return make_row_keyboard([
                'Заявки на поездки',
                'Изменить описание'
                ])