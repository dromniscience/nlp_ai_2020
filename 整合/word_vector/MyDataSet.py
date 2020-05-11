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

def collate_func(data):
    '''
    这个函数是放到DataLoader里，指定DataLoader选取batch时的方式
    '''
    max_len = max(len(c) + len(n) for _, c, n in data) #得到背景词和噪声词个数和的最大值
    centers, context_noise, masks, labels = [] , [], [], []
    for center, context, noise in data:
        centers.append(center)
        cur_len = len(context) + len(noise) #当前数据背景词和噪声词的个数和
        context_noise.append(context + noise + [0]*(max_len - cur_len)) #不足的地方补零
        #为了防止补零的区域对后续计算交叉熵的影响，这里使用mask掩码。相当于补零的地方权重为0
        masks.append([1]*cur_len + [0] * (max_len - cur_len)) 
        #labels:背景词为1，其余为0
        labels.append([1] * len(context) + [0] * (max_len - len(context)))
    return (torch.tensor(centers).view(-1, 1), torch.tensor(context_noise), torch.tensor(masks), torch.tensor(labels))
