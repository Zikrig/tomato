import os
from local_data import LocalData

images_dir = os.path.abspath('').replace('\\', '/') + '/telegram/data/images'
avas_dir = images_dir+'/avas'
horseh_dir = images_dir+'/horseh'

textes_dir = os.path.abspath('').replace('\\', '/') + '/telegram/data/texts'

hh_files = {
    'coords':   '/coords.txt',
    'describe': '/describe.txt',
    'photos': '/photo_paths.txt'
}

pgsdata = {
    'dbname':"postgres",
    'user':"postgres",
    'password':"httphuggingfapaceTSAGITSArenamapuserpass",
    # 'password':'1234',
    'host':"127.0.0.1",
    'port':"5432"
}

lc = LocalData(hh_files, textes_dir, horseh_dir)