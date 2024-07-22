import psycopg2
from psycopg2 import Error

def init_people_table(pgsdata):
    # print(pgsdata)
    try:
        conn = psycopg2.connect(
            dbname=pgsdata['dbname'],
            user=pgsdata['user'], 
            password=pgsdata['password'], 
            host=pgsdata['host'], 
            port=pgsdata['port']
            )
        conn.autocommit = True  # устанавливаем актокоммит
        
        cursor = conn.cursor()

        # cursor.execute("DROP TABLE people")
        cursor.execute("CREATE TABLE people (id SERIAL PRIMARY KEY, tg_person INT, name VARCHAR(50), phone VARCHAR(16), describe VARCHAR(300), photo VARCHAR(100))")

        conn.commit()  

        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        # cursor.close()
        # conn.close()
    finally:
        print(f"Создана таблица people")
        print("Соединение с PostgreSQL закрыто")


def init_task_table(pgsdata):
    # print(pgsdata)
    try:
        conn = psycopg2.connect(
            dbname=pgsdata['dbname'],
            user=pgsdata['user'], 
            password=pgsdata['password'], 
            host=pgsdata['host'], 
            port=pgsdata['port']
            )
        conn.autocommit = True  # устанавливаем актокоммит
        
        cursor = conn.cursor()
        # tg_id (связь с пользователем?)
        # Дата
        # Время
        # Особые обстоятельства
        # Отработана ли
        # cursor.execute("DROP TABLE people")
        cursor.execute("CREATE TABLE task(id SERIAL PRIMARY KEY, tg_person INT, date_of DATE, time_of TIME, descr_client VARCHAR(300), ready BOOL)")

        conn.commit()  

        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        # cursor.close()
        # conn.close()
    finally:
        print(f"Создана таблица people")
        print("Соединение с PostgreSQL закрыто")

