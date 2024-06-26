
from tomato_tables.settings import *

import json

def make_write_file(cols):
    fruits = [fr[0] for fr in cols]
    f = open(fruits_list, 'w')
    f.write(json.dumps(fruits, indent=4))
    f.close()


def get_fruits_from_file():
    f = open(fruits_list)
    pre_res = json.loads(f.read())
    f.close()

    res = []
    for fr in pre_res:
        # print(fr)
        prom_fr = fr[1:-1].replace('\"', '')
        res.append(prom_fr.split(','))
    # print(res)/
    return res
    # return fruits[:-1]

def actual_fruits_save(fruits):
    f = open(fruits_now_file, 'w')
    f.write(json.dumps(fruits, indent=4))
    f.close()


def next_fruits_save(fruits):
    f = open(fruits_next_file, 'w')
    f.write(json.dumps(fruits, indent=4))
    f.close()

def get_fruits(fruits_path):
    f = open(fruits_path)
    res = json.loads(f.read())
    f.close()
    return res

# print(get_fruits_from_file())
# # print(next_fruits)
# import os, sys
# curDir = os.getcwd()
# sys.path.append(curDir)
# print(sys.path)