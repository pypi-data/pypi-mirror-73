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

# data loader

def load_data(name, root, mask):
    path = os.path.join(root, name)
    data = np.load(path)
    if mask is not None:
        data = data[mask]
    return data
