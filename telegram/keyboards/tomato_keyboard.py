from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

class keyboard_state:
    def __init__(self, btns):
        self.btns = [[btn[0],btn[1]] for btn in btns]
        self.btns_state = {}
        for btn in self.btns:
            self.btns_state[btn[1].replace('fr-', '')] = False

    def alt_btn_state(self, btn):
        btn = btn.replace('fr-', '')
        self.btns_state[btn] = not self.btns_state[btn]

    def create_list(self):
        # res = []
        self.lat_fruits = []
        # self.ru_fruits = []
        for btn in self.btns_state:
            if self.btns_state[btn] == True:
                self.lat_fruits.append(btn)
        return self.lat_fruits
        

    # def really_big(self):
    #     # print(self.btns_state)
    #     inline_kb_full = [[]]
    #     for btn in self.btns:
    #         pre_text = '✅' if self.btns_state[btn[1].replace('fr-', '')] else '❌'
    #         inline_kb_full[0].append(InlineKeyboardButton(text=pre_text + ' ' + btn[0], callback_data=btn[1]))
    #     inline_kb_full[0].append(InlineKeyboardButton(text='Отправить', callback_data='fr-CLOSE'))

    #     return InlineKeyboardMarkup(inline_keyboard=inline_kb_full)
    
    def really_big(self):
        res = InlineKeyboardBuilder()
        # inline_kb_full = [[]]
        for btn in self.btns:
            pre_text = '✅' if self.btns_state[btn[1].replace('fr-', '')] else '❌'
            # inline_kb_full[0].append(InlineKeyboardButton(text=pre_text + ' ' + btn[0], callback_data=btn[1]))
            res.row(InlineKeyboardButton(text=pre_text + ' ' + btn[0], callback_data=btn[1]))
        res.row(InlineKeyboardButton(text='Отправить', callback_data='fr-CLOSE'))
        # inline_kb_full[0].append(InlineKeyboardButton(text='Отправить', callback_data='fr-CLOSE'))

        return res.as_markup(row_width=1)
    