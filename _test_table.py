from config import *
from table.init.new_db_init import *
from table.work_with_database.put_data import *
from table.work_with_database.task_work import *

# init_people_table(pgsdata)
# init_task_table(pgsdata)

# person_data = (1000, 'name', 'phone', 'describe', 'photo')
# person_data2 = (1005, 'name', 'phone', 'describe', 'photo')
# person_data3 = (1002, 'name', 'phone', 'describe', 'photo')
# put_person(pgsdata, person_data)

# tg_person, date_of, time_of, descr_client, ready
# task_data = ('1000', '1999-01-08', '04:05', 'Describe', 'False')
# task_data2 = ('1001', '2025-07-19', '04:05', 'Describe', 'False')
# person_data3 = (1002, 'name', 'phone', 'describe', 'photo')
# put_task(pgsdata, task_data2)
print(select_all_tasks(pgsdata))

# person_gen(pgsdata, person_data)
# person_gen(pgsdata, person_data2)
# person_gen(pgsdata, person_data3)
# print(select_all_person(pgsdata)) 
# print(select_unready_tasks(pgsdata, '1001'))

# print(select_dates_onready(pgsdata, '1001'))