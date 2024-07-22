import psycopg2
from psycopg2 import Error
# Функционал работы с заявками.

# Юзер может Добавить заявку
# Удалить заявку

# конюшня может отметить заявку как выполненную

# Параметры заявки:
# tg_id (связь с пользователем?)
# Дата
# Время
# Особые обстоятельства
# Отработана ли

def put_task(pgsdata, person_data):
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
        cursor.execute("INSERT INTO task(tg_person, date_of, time_of, descr_client, ready) VALUES (%s, %s, %s, %s, %s)", person_data)
        conn.commit()  

        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        # cursor.close()
        # conn.close()
    finally:
        print("Добавлены данные в таблицу")
        print("Соединение с PostgreSQL закрыто")

def alt_task(pgsdata, pd):
    try:
        conn = psycopg2.connect(
            dbname=pgsdata['dbname'],
            user=pgsdata['user'], 
            password=pgsdata['password'], 
            host=pgsdata['host'], 
            port=pgsdata['port']
            )
        conn.autocommit = True  # устанавливаем актокоммит
        print(pd)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE task SET (date_of, time_of, descr_client, ready) = ('{pd[1]}', '{pd[2]}', '{pd[3]}', '{pd[4]}') WHERE tg_person={str(pd[0])}")
        conn.commit()  

        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        # cursor.close()
        # conn.close()
    finally:
        print("Обновлены данные в таблице")
        print("Соединение с PostgreSQL закрыто")


def select_task(pgsdata, tg_id):
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
        
        cursor.execute(f"SELECT * FROM task WHERE tg_person={str(tg_id)}")
        # cursor.execute("SELECT * FROM task WHERE tg_person=%s", tg_id)
        person = cursor.fetchone()
        # print(person)

        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        # cursor.close()
        # conn.close()
    finally:
        if(person):
            print('данные успешно получены')
        else:
            print('не нашли нужных данных')
            person = ()
        
        print("Соединение с PostgreSQL закрыто")
        return person


def select_all_tasks(pgsdata):
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
        
        cursor.execute(f"SELECT * FROM task")
        # cursor.execute("SELECT * FROM task WHERE tg_person=%s", tg_id)
        person = cursor.fetchall()
        # print(person)

        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        # cursor.close()
        # conn.close()
    finally:
        if(person):
            print('данные успешно получены')
        else:
            print('не нашли нужных данных')
            person = []
        
        print("Соединение с PostgreSQL закрыто")
        return person

def select_unready_tasks(pgsdata, tg_id):
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
        
        cursor.execute(f"SELECT COUNT(*) FROM task WHERE tg_person={str(tg_id)} AND date_of::date >= CURRENT_DATE")
        # cursor.execute("SELECT * FROM task WHERE tg_person=%s", tg_id)
        person = cursor.fetchone()
        # print(person)

        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        # cursor.close()
        # conn.close()
    finally:
        print("Соединение с PostgreSQL закрыто")
        return person[0]
    

def select_dates_onready(pgsdata, tg_id):
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
        
        cursor.execute(f"SELECT id, date_of FROM task WHERE tg_person={str(tg_id)} AND date_of::date >= CURRENT_DATE")
        # cursor.execute("SELECT * FROM task WHERE tg_person=%s", tg_id)
        person = cursor.fetchall()
        # print(person)

        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        # cursor.close()
        # conn.close()
    finally:
        print("Соединение с PostgreSQL закрыто")
        return person
    
def select_task_by_id(pgsdata, id):
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
        
        cursor.execute(f"SELECT * FROM task WHERE id={str(id)}")
        # cursor.execute("SELECT * FROM task WHERE tg_person=%s", tg_id)
        person = cursor.fetchone()
        # print(person)

        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        # cursor.close()
        # conn.close()
    finally:
        print("Соединение с PostgreSQL закрыто")
        return person
    
def delete_by_id(pgsdata, id):
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
        
        cursor.execute(f"DELETE FROM task WHERE id={str(id)}")
        # person = cursor.fetchone()
        # print(person)

        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        # cursor.close()
        # conn.close()
    finally:
        print("Соединение с PostgreSQL закрыто")
        # return person
    

def alt_task_date(pgsdata, id, date):
    try:
        conn = psycopg2.connect(
            dbname=pgsdata['dbname'],
            user=pgsdata['user'], 
            password=pgsdata['password'], 
            host=pgsdata['host'], 
            port=pgsdata['port']
            )
        conn.autocommit = True  # устанавливаем актокоммит
        # print(pd)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE task SET date_of='{date}' WHERE id={id}")
        conn.commit()  

        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        # cursor.close()
        # conn.close()
    finally:
        print("Обновлены данные в таблице")
        print("Соединение с PostgreSQL закрыто")

def alt_task_descr(pgsdata, id, descr):
    try:
        conn = psycopg2.connect(
            dbname=pgsdata['dbname'],
            user=pgsdata['user'], 
            password=pgsdata['password'], 
            host=pgsdata['host'], 
            port=pgsdata['port']
            )
        conn.autocommit = True  # устанавливаем актокоммит
        # print(pd)
        cursor = conn.cursor()
        print("Обновляем столбец ")
        print("UPDATE task SET descr_client = '444' WHERE id=17")
        print(f"UPDATE task SET descr_client = '{descr}' WHERE id={id}")
        cursor.execute(f"UPDATE task SET descr_client = '{descr}' WHERE id={id}")
        conn.commit()  

        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        # cursor.close()
        # conn.close()
    finally:
        print("Обновлены данные в таблице")
        print("Соединение с PostgreSQL закрыто")