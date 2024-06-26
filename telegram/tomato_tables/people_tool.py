import psycopg2
from psycopg2 import Error

# from settings import *

from tomato_tables.create_tables import *
from tomato_tables.text_tool import *

import datetime
 
def add_person(tg_id, fruits):
    # print(tg_id)
    fruits_arglist = ','.join(fruits)
    fruits_meaning = ','.join(['True' for i in range(len(fruits))])
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # устанавливаем актокоммит
        
        cursor = conn.cursor()
        # horsehouse_id INTEGER REFERENCES horsehouse (id) ON DELETE CASCADE ON UPDATE CASCADE
        cursor.execute(f"INSERT INTO {table_people_name}(tg_id,{fruits_arglist}) VALUES ({tg_id},{fruits_meaning});")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        print("Человек добавлен")
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")

def alt_person(tg_id, fruits):
    del_person(tg_id)
    add_person(tg_id, fruits)
    # fruits_arglist = ','.join(fruits)
    # fruits_meaning = ','.join(['True' for i in range(len(fruits))])
    # try:
    #     conn  = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    #     conn.autocommit = True  # устанавливаем актокоммит
        
    #     cursor = conn.cursor()
    #     cursor.execute(f"DELETE FROM {table_people_name} WHERE tg_id='{tg_id}'")
    #     cursor.execute(f"INSERT INTO {table_people_name}(tg_id,{fruits_arglist}) VALUES ({tg_id},{fruits_meaning});")
    # except (Exception, Error) as error:
    #     print("Ошибка при работе с PostgreSQL", error)
    # finally:
    #     print("Фрукт удален")
    #     if conn:
    #         cursor.close()
    #         conn.close()
    #         print("Соединение с PostgreSQL закрыто")

def del_person(tg_id):
    try:
        conn  = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # устанавливаем актокоммит
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_people_name} WHERE tg_id='{tg_id}'")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        print("Фрукт удален")
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")


# Получить список всех фруктов, где date_of < start и date_of>finish
def check_date(date_of):
    try:
        res = []
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # устанавливаем актокоммит
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_fruits_name} WHERE start<=\'{date_of}\' AND finish>=\'{date_of}\' ORDER BY name")
        res = cursor.fetchall()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        print("Фрукты получены")
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
    return res

# Получить список всех фруктов, где date_of+7>start  и date_of<finish
def check_date_soon(date_of):
    try:
        res = []
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # устанавливаем актокоммит
        cursor = conn.cursor()
        print(f'Ищем фрукты, где {date_of} >= start и <= finish')
        cursor.execute(f"SELECT * FROM {table_fruits_name} WHERE start-7<=\'{date_of}\' AND finish>=\'{date_of}\' AND start>=\'{date_of}\' ORDER BY name")
        res = cursor.fetchall()
        print(res)
        print('нашли')
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        print("Фрукты получены")
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
    return res

def get_person_by_id(tg_id):

    try:
        res = []
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # устанавливаем актокоммит

        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_people_name} WHERE tg_id={tg_id}")
        res = cursor.fetchone()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        print("Заголовки таблицы людей получены")
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
    return res

# Получить данные по фруктам, интересующим конкретного человека
def rap_ready(tg_id):
    # print(tg_id)
    pers_r = get_person_by_id(tg_id)
    # print(pers_r)
    pers = pers_r[1:]
    fruits = get_fruits_from_file()
    now_fruits = get_fruits(fruits_now_file)
    next_fruits = get_fruits(fruits_next_file)
    # print(now_fruits)
    # print(next_fruits)
    # print(fruits)
    now_keys = now_fruits.keys()
    next_keys = next_fruits.keys()
    res1 = 'Скоро пора сажать:\n'
    res2 = 'Уже пора сажать:\n'
    cnt1, cnt2 = 0,0
    # print(fruits)
    # print(now_keys)
    # print(next_keys)
    for i in range(len(fruits)):
        if not pers[i]:
            # print(f'Пропускаем {i} ({pers[i]})')
            continue
        if(fruits[i][1] in now_keys):
            res2 += now_fruits[fruits[i][1]]
            cnt2 += 1
        elif(fruits[i][1] in next_keys):
            res1 += next_fruits[fruits[i][1]]
            cnt1 += 1
    #     else:
    #         print(fruits[i][1])
    #         print('Не обнаружен в списках')
    # print(res1)
    # print(res2)
    if cnt1 == 0 and cnt2 == 0:
        res = 'Похоже, пока сажать нечего'
    elif cnt1 == 0:
        res = res2[:-1]
    elif cnt2 == 0:
        res = res1[:-1]
    else:
        res = res1[:-1] + '\n' + res2[:-1]
    
    # print(res)
    return res


def date_dig_to_text(dd):
    # print(str(dd))
    y, m, d = str(dd).split('-')
    meses = [
        'января',
        'февраля',
        'марта',
        'апреля',
        'мая',
        'июня',
        'июля',
        'августа',
        'сентября',
        'октября',
        'ноября',
        'декабря'
    ]
    
    return str(int(d)) + ' ' + meses[int(m)-1]

def create_now_list(next_fruits):
    day_fruits = check_date(next_fruits)
    res = {}
    for nd in day_fruits:
        res[nd[2]] = f'{nd[1]} - c {date_dig_to_text(nd[3])} по {date_dig_to_text(nd[4])} \n'
    return res
    
def create_next_list(today_fruits):
    next_day_fruits = check_date_soon(today_fruits)
    res = {}
    for nd in next_day_fruits:
        res[nd[2]] = f'{nd[1]} - c {date_dig_to_text(nd[3])} по {date_dig_to_text(nd[4])} \n'
    return res

def daily_fruits(today = datetime.date.today().isoformat()):
    next_fruits = create_next_list(today)
    next_fruits_save(next_fruits)
    now_fruits = create_now_list(today)
    actual_fruits_save(now_fruits)