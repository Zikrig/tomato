from keyboards.simple_row import make_row_keyboard
import keyboards.tomato_keyboard as kb
from tomato_tables.text_tool import *
from tomato_tables.people_tool import *
from tomato_tables.create_tables import *
from telegram.tomato_tables.settings import *

# create_people_table()
# print(get_fruits_cols())
# print(get_fruits())


# today = '2000-05-06'
# # # функция работает с готовыми списками фруктов
# next_fruits = create_next_list(today)
# # next_fruits_save(next_fruits)
# now_fruits = create_now_list(today)
# # actual_fruits_save(now_fruits)

# add_fruit('Горох', 'Peas', 5,1,5,14)
# add_fruit('Фасоль', 'Beans', 5,1,5,14)
# add_fruit('Редис', 'Radish', 4,15,8,15)
# add_fruit('Свекла', 'Beetroot', 4,25,5,10)
# add_fruit('Капуста', 'Cabbage', 4,25,5,10)
# add_fruit('Морковь', 'Carrot', 4,25,5,5)
# add_fruit('Кабачок', 'Zucchini', 4,15,5,10)
# add_fruit('Картофель', 'Potato', 4,15,5,10)
# add_fruit('Чеснок яровой', 'Spring_garlic', 3, 25,4,10)
# add_fruit('Чеснок озимый', 'Winter_garlic', 9, 25,10,15)
# add_fruit('Лук', 'Onion', 4,25,5,5)
add_fruit('Укроп и петрушка', 'Parsley', 5,1,5,10)
# add_fruit('Огурцы', 'Cucumbers', 5,10,5,20)
# add_fruit('Томат', 'Tomato', 5,15,5,5)
# add_fruit('Бансай', 'Bonsai', 3,1,5,1)
# add_fruit('Дерево', 'Tree', 4,15,11,15)
# add_fruit('Пшеница', 'Wheat', 3,15,6,15)
# add_fruit('Рожь', 'Rye', 8,15,10,15)
# delete_fruit('Parsley')
daily_fruits('2000-05-13')