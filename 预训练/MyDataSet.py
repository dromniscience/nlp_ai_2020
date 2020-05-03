import collections
import torch 
import torch.nn as nn 
import torch.utils.data as data
import sys
import os
import random
import math
import torch.nn.functional as F

class MyDataSet(data.Dataset):
    def __init__(self, centers, contexts, noises):
        self.centers = centers #中心词
        self.contexts = contexts #背景词
        self.noises = noises #噪声词

    def __len__(self):
        return len(self.centers)
    def __getitem__(self, index):
        return (self.centers[index], self.contexts[index], self.noises[index])
