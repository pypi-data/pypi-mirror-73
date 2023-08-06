import os
import sys
import time
import re
import glob
import shutil
import numpy as np
import matplotlib.pyplot as plt
# pytorch package
import torch

from .misc import load_data

class Loader:
    def __init__(
        self,
        src_root_path,
        dst_root_path='./vectors',
        ischeck=True,
        filemode='copy',
        marked_sub_keys=None,
        mask=None
    ):
        # initiate property
        self.src_root_path = src_root_path
        self.dst_root_path = dst_root_path if dst_root_path is not None else src_root_path
        self.ischeck = ischeck
        self.filemode = filemode
        self.marked_sub_keys = marked_sub_keys
        self.data_mask = mask

        self.initiate_marked_sub_keys()
        self.initiate_filemode()

        # check folder
        if self.ischeck:
            self.check_folder()
    
    def initiate_filemode(self):
        if self.filemode == 'copy':
            self.filehandle = shutil.copy
        elif self.filemode == 'move':
            self.filehandle = shutil.move
        else:
            raise KeyError('Invalid filemode ', self.filemode)
    
    def initiate_marked_sub_keys(self):
        initiate_flag = False
        if not isinstance(self.marked_sub_keys, dict):
            initiate_flag = True
        elif self._check_keywords(self.default_marked_sub_keys.keys(), self.marked_sub_keys.keys()):
            initiate_flag = True
        else:
            initiate_flag = False
        if initiate_flag:
            self.marked_sub_keys = self.default_marked_sub_keys

    @ property
    def default_marked_sub_keys(self):
        return {
            'train_data': 'traindata',
            'train_label': 'trainlabel',
            'val_data': 'valdata',
            'val_label': 'vallabel'
        }
    
    def _check_keywords(self, keywords, obj):
        if not isinstance(obj, list):
            obj = list(obj)
        if not isinstance(keywords, list):
            keywords = list(keywords)
        if all([item in obj for item in keywords]):
            return True
        return False
    
    def check_folder(self):
        root_path = self.dst_root_path
        def check_dir(path, sub_folder):
            sub_path = os.path.join(path, sub_folder)
            if os.path.exists(sub_path):
                print("delete {}!".format(sub_path))
                shutil.rmtree(sub_path)
            os.makedirs(sub_path)
            return sub_path
        def move_list(vector_list, keyword, src_path, dst_path):
            sub_list = [item for item in vector_list if keyword in item]
            for item in sub_list:
                src_item = os.path.join(src_path, item)
                epoch = re.findall(r"\d+", item)[0]
                dst_item = os.path.join(dst_path, epoch + '.npy')
                self.filehandle(src_item, dst_item)
        # initiate
        vector_list = os.listdir(self.src_root_path)
        train_data_path = check_dir(root_path, 'train_data')
        train_label_path = check_dir(root_path, 'train_label')
        val_data_path = check_dir(root_path, 'val_data')
        val_label_path = check_dir(root_path, 'val_label')
        # move the data
        move_list(vector_list, self.marked_sub_keys['train_data'], self.src_root_path, train_data_path)
        move_list(vector_list, self.marked_sub_keys['train_label'], self.src_root_path, train_label_path)
        move_list(vector_list, self.marked_sub_keys['val_data'], self.src_root_path, val_data_path)
        move_list(vector_list, self.marked_sub_keys['val_label'], self.src_root_path, val_label_path)
        print('done!')   

    # ===================================

    def merge_data(self, root):
        # read the list
        data_list = os.listdir(root)
        index_list = [int(re.findall('\d+', item)[0]) for item in data_list]
        data_dict = {item[0]:item[1] for item in zip(index_list, data_list)}
        # load the data
        data, index = [], {}
        start = 0
        N = len(data_list)
        for i in range(N):
            # stack cur data
            cur_data = load_data(data_dict[i+1], root, self.data_mask)
            data.append(cur_data)
            # save index
            cur_len = len(cur_data)
            index[i+1] = (start, start+cur_len)
            start += cur_len
        data = np.vstack(data)
        return data, index

    def merge_label(self, root):
        # read the list
        data_list = os.listdir(root)
        index_list = [int(re.findall('\d+', item)[0]) for item in data_list]
        data_dict = {item[0]:load_data(item[1], root, self.data_mask) for item in zip(index_list, data_list)}
        return data_dict
    
    def merge_data_label(self, phase='train'):
        data_path = os.path.join(self.dst_root_path, phase + '_data')
        label_path = os.path.join(self.dst_root_path, phase + '_label')
        data, index = self.merge_data(data_path)
        label_dict = self.merge_label(label_path)
        return {
            'data': (data, index),
            'label': label_dict
        }

    def split_data(self, data, index):
        split = {}
        for k, v in index.items():
            split[k] = data[v[0]:v[1], :]
        return split


if __name__ == '__main__':
    loader = Loader(
        src_root_path='/home/zwz/zbr/experiments/5_generate_embedding/Test50_50_Partitions4_0/saved_models/', 
        dst_root_path='/home/zwz/zbr/code/epoch_visualizer/demo/vectors', 
        ischeck=True, 
        marked_sub_keys=None
    )