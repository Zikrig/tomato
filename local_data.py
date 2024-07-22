from config import *
import os.path, os

# for obj in hh_files:
#     print(hh_files[obj])

class LocalData:
    def __init__(self, hh_files, textes_dir, horseh_dir):
        # print('ИНИЦИАЛИЗАЦИЯ')
        self.hh_files = hh_files
        self.horseh_dir = horseh_dir
        self.textes_dir = textes_dir
        
        self.imgs = []
        self.imgs_clear = []

        if('coords' in self.hh_files):
            if(os.path.exists(textes_dir+self.hh_files['coords'])):
                self.init_coords()
        if('describe' in self.hh_files):
            if(os.path.exists(textes_dir+self.hh_files['describe'])):
                self.init_describe()

        if('photos' in self.hh_files):
            self.init_photos()

    def init_coords(self):
        f = open(self.textes_dir+self.hh_files['coords'], 'r')
        t = f.read()
        f.close()
        coords = t.split('\n')
        if(len(coords)>1):
            self.coord1 = float(coords[0]) 
            self.coord2 = float(coords[1])
    
    def init_describe(self):
        f = open(self.textes_dir+self.hh_files['describe'], 'r', encoding='utf-8')
        t = f.read()
        f.close()
        self.describe = t

    def init_photos(self):
        f = open(self.textes_dir+self.hh_files['photos'], 'r', encoding='utf-8')
        t = f.read()
        f.close()
        imgs = t.split('\n')
        # print(imgs)
        for st in imgs:
            posint = self.horseh_dir + st
            # print(posint)
            if(os.path.exists(posint)):
                self.imgs.append(posint)
                self.imgs_clear.append(st)

    def set_descr(self, descr):
        self.describe = descr
        f = open(self.textes_dir+self.hh_files['describe'], 'w', encoding='utf-8')
        f.write(descr)
        f.close

    def set_coords(self, crds):
        all_coords = crds.split('\n')
        if(not len(all_coords)>1):
            return False
        self.coord1, self.coord2 = float(all_coords[0]), float(all_coords[1])
        f = open(self.textes_dir+self.hh_files['coords'], 'w', encoding='utf-8')
        f.write(crds)
        f.close

    def del_photo_by_num(self, num):
        if num > len(self.imgs)-1:
            return True
        imgpath = self.imgs[num]
        if(not os.path.exists(imgpath)):
            return True
        self.imgs_clear.pop(num)
        self.imgs.pop(num)
        os.remove(imgpath)
        f = open(self.textes_dir+self.hh_files['photos'], 'w', encoding='utf-8')
        f.write('\n'.join(self.imgs_clear))
        f.close()
        
    def add_photo_to_file(self, name):
        self.imgs.append(self.horseh_dir+'/'+name)
        self.imgs_clear.append('/'+name)
        f = open(self.textes_dir+'/'+self.hh_files['photos'], 'w', encoding='utf-8')
        f.write('\n'.join(self.imgs_clear))
        f.close()