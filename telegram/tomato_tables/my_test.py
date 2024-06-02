# from main.settings import *
from create_tables import *
from people_tool import *

# Создание таблицы с людьми
# Поля (id, tg_id)
# create_people_table()

# Создание таблицы с фруктами
# Поля (id, name, colname, start, finish)
# create_tomato_table()

# Добавляет в таблицу с фруктами все значения.
# А в таблицу с людьми столбец с названием из второго аргумента
# add_fruit('Тыква', 'pumpkin', 2,2,5,7)
# add_fruit('Банан', 'banane', 1,1,6,6)
# add_fruit('Томат', 'tomate', 1,1,8,8)
# add_fruit('Апельсин', 'orange', 2,2,9,9)

# Получает все имеющиеся фрукты
# print(get_fruits())

# Получает все имеющиеся столбцы с фруктами в таблице с людьми (отладочное)
# print(get_people())

# Удаляет фрукт из обоих таблиц по названию
# delete_fruit('banane')

# # добавление человека с набором фруктов
# tg_id = 99
# fruits = ("tomate", "banane")

# add_person(tg_id, fruits)
# print(get_people())
    
# # Изменение этого человека
# fruits = ("tomate")
# alt_person(tg_id, fruits)
# print(get_people())

# # Удаление этого человека
# del_person(tg_id)

# Подготовка оповещения для всего набора фрутктов
# print(check_date('2000-05-06'))

# Сеять на следующей неделе
# print(check_date_soon('2000-05-06'))

# Заготовка для рапорта
# today = '2000-05-06'
# # функция работает с готовыми списками фруктов
# next_fruits = create_next_list(today)
# next_fruits_save(next_fruits)
# now_fruits = create_now_list(today)
# actual_fruits_save(now_fruits)

# Подготовка рапорта по id при рассылке (экономно)
# for tg_id in 99, 100:
#     print(f"С точки зрения {tg_id}")
#     r = rap_ready(tg_id)
#     print(r)


# print(get_person_by_id(tg_id))
# Массовая рассылка