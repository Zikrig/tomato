import psycopg2
from psycopg2 import Error

def person_gen(pgsdata, person_data):
    p = select_person(pgsdata, person_data[0])
    if len(p) == 0:
        put_person(pgsdata, person_data)
    else:
        alt_person(pgsdata, person_data)

def put_person(pgsdata, person_data):
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
        cursor.execute("INSERT INTO people(tg_person, name, phone, describe, photo) VALUES (%s, %s, %s, %s, %s)", person_data)
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

def alt_person(pgsdata, pd):
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
        cursor.execute(f"UPDATE people SET (name, phone, describe, photo) = ('{pd[1]}', '{pd[2]}', '{pd[3]}', '{pd[4]}') WHERE tg_person={str(pd[0])}")
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


def select_person(pgsdata, tg_id):
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
        
        cursor.execute(f"SELECT * FROM people WHERE tg_person={str(tg_id)}")
        # cursor.execute("SELECT * FROM people WHERE tg_person=%s", tg_id)
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


def select_all_person(pgsdata):
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
        
        cursor.execute(f"SELECT * FROM people")
        # cursor.execute("SELECT * FROM people WHERE tg_person=%s", tg_id)
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
