import psycopg2
from psycopg2 import Error
from settings import *
# from text_tool import *
from tomato_tables.text_tool import *

def create_tomato_table():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # устанавливаем актокоммит
        cursor = conn.cursor()
        
        # cursor.execute("DROP TABLE tomato")
        cursor.execute(f"CREATE TABLE {table_fruits_name} (id SERIAL PRIMARY KEY, name VARCHAR(300), colname VARCHAR(300), start DATE, finish DATE)")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        print("Таблица создана")
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
    

def create_people_table():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # устанавливаем актокоммит
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE TABLE {table_people_name} (id SERIAL PRIMARY KEY, tg_id INT PRIMARY KEY);")
        # ALTER TABLE users ADD PRIMARY KEY
        # cursor.execute(f"ALTER TABLE {table_people_name} ADD PRIMARY KEY (tg_id)")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        print("Таблица создана")
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")

def add_fruit(name, colname, start_m, start_d, finish_m, finish_d):
    if not pre_moderate_addfruit(name, colname, start_m, start_d, finish_m, finish_d):
        print(f"Фрукт {name} не проходит")
        return False
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # устанавливаем актокоммит
        cursor = conn.cursor()
        
        cursor.execute(f"ALTER TABLE {table_people_name} ADD COLUMN {colname} BOOLEAN DEFAULT FALSE")
        cursor.execute(f"INSERT INTO {table_fruits_name}(name, colname, start, finish) VALUES ('{name}', '{colname}', make_date(2000, {start_m}, {start_d}), make_date(2000, {finish_m}, {finish_d}));")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        print("Данные добавлены")
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
            
        make_write_file(get_fruits_cols())
    

def delete_fruit(colname):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # устанавливаем актокоммит
        cursor = conn.cursor()
        # horsehouse_id INTEGER REFERENCES horsehouse (id) ON DELETE CASCADE ON UPDATE CASCADE
        cursor.execute(f"ALTER TABLE {table_people_name} DROP COLUMN {colname}")
        cursor.execute(f"DELETE FROM {table_fruits_name} WHERE colname='{colname}'")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        print("Фрукт удален")
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")

        make_write_file(get_fruits_cols())

def get_fruits():
    try:
        res = []
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # устанавливаем актокоммит
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT * FROM {table_fruits_name}")
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

def get_fruits_cols():
    try:
        res = []
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # устанавливаем актокоммит
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT (name, colname) FROM {table_fruits_name}")
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

def get_people_fruits():
    try:
        res = []
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # устанавливаем актокоммит
    
        cursor = conn.cursor()
        cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_people_name}' ORDER BY ordinal_position")
        res = cursor.fetchall()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        print("Заголовки таблицы людей получены")
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
    return res

def get_people():
    try:
        res = []
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # устанавливаем актокоммит
        
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT * FROM {table_people_name}")
        res = cursor.fetchall()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        print("Все люди получены")
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")

    return res

def pre_moderate_addfruit(name, colname, start_m, start_d, finish_m, finish_d):
    if(len(name) == 0):
        return False
    
    if(len(colname) == 0):
        return False
    
    if(start_m > finish_m):
        return False
    if(start_m <= finish_m):
        return True
    if(start_d > finish_d):
        return False
    
# print(get_people())