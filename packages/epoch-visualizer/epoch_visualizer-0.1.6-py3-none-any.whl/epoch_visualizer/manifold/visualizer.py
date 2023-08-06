import os
import sys
import time
import re
import glob
import shutil
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import cv2
# notebook environ
from IPython.display import clear_output, Image, display, HTML
# pytorch package
import torch
# tsnecuda
from tsnecuda import TSNE
from .mds import MDS, mds_fit
from .minkowski import minkowski_pairs

class ShowImg:
    def __init__(
        self,
        environ='notebook',
        output_path='./output',
        fps=2
    ):
        self.environ = environ
        self.output_path = output_path
        self.fps = fps
        self.img_path = os.path.join(self.output_path, 'img')
        self.video_path = os.path.join(self.output_path, 'video')

        self.initiate()
    
    def initiate(self):
        # initiate folder
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)
        os.makedirs(self.output_path)
        os.makedirs(self.img_path)
        os.makedirs(self.video_path)
        # initiate environ
        pass

    def during_hook(self, data, label, k):
        plt.figure(figsize=(6, 6))
        plt.scatter(data[:, 0], data[:, 1], c=label.reshape(-1).tolist())
        save_path = os.path.join(self.img_path, '{}.png'.format(k))
        plt.savefig(save_path)
        plt.show()

    def end_hook(self):
        N = len(os.listdir(self.img_path))
        # load img
        img_list = []
        for i in range(N):
            k = i+1
            load_path = os.path.join(self.img_path, '{}.png'.format(k))
            img = cv2.imread(load_path)
            img_list.append(img)
        # to video
        self.to_video(img_list)
        self.notebook_video_show(img_list)
    
    def to_video(self, img_list):
        fps = self.fps
        size = (1280, 720)
        save_path = os.path.join(self.video_path, 'video.mp4') 
        videowriter = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
        for img in img_list:
            videowriter.write(img)
        print('Video generated!')

    def notebook_video_show(self, img_list):
        index = 0
        N = len(img_list)
        while(True):
            try:
                index = index % N
                img = img_list[index]
                clear_output(wait=True)
                plt.figure(figsize=(6, 6))
                plt.axis('off') 
                plt.imshow(img)
                plt.title('Epoch: {}'.format(index))
                plt.show()
                index += 1
                time.sleep(1 / self.fps)
            except KeyboardInterrupt:
                return

class Visualizer:
    def __init__(
        self,
        loader,
        phase='train',
        parameters=None,
        method='tsne',
        environ='notebook',
        output_path='./output'
    ):
        self.loader = loader
        self.phase = phase
        self.method = method
        self.parameters = {} if parameters is None else parameters
        self.shower = ShowImg(environ=environ, output_path=output_path)
        
        self.initiate_method()
    
    def initiate_method(self):
        if self.method == 'tsne':
            self.decomposer = TSNE(**self.parameters)
            self.decom_handle = self.decomposer.fit_transform
        elif self.method == 'mds':
            self.decomposer = MDS(**self.parameters)
            def decom_func(data):
                dist_mat = minkowski_pairs(data, sqform=False)
                return self.decomposer.fit(dist_mat)
            self.decom_handle = decom_func
    
    def generate(self, data):
        return self.decom_handle(data)
    
    def show_img(self, split, label):
        N = len(split.keys())
        for i in range(N):
            k = i + 1
            v = split[k]
            print('Epoch: ', k)
            cur_data = v
            cur_label = label[k]
            self.shower.during_hook(cur_data, cur_label, k)
        self.shower.end_hook()
    
    def run(self):
        # fetch data and label
        batch_dict = self.loader.merge_data_label(phase=self.phase)
        data, index = batch_dict['data']
        label = batch_dict['label']
        print('Data loaded！')
        # decompose
        data_ld = self.generate(data)
        split = self.loader.split_data(data_ld, index)
        print('Data decomposed!')
        # visualize
        self.show_img(split, label)
