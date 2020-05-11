import os,sys
import random
import numpy as np
import torch
import torch.nn as nn
import pickle

class CSM(nn.Module):
    def __init__(self, vocab_size, embed_size, sentence_size):
        '''
        @param
        vocab_size: 词表大小
        embed_size:每个词向量的维度，相当于论文中的q
        sentence_size: 诗句的长度，5或7
        '''
        super(CSM, self).__init__()
        self.sentence_size = sentence_size
        self.conv1 = nn.Parameter(torch.randn((2, embed_size)))
        self.conv2 = nn.Parameter(torch.randn((2, embed_size)))
        self.conv3 = nn.Parameter(torch.randn((3, embed_size)))
        if sentence_size == 7:
            self.conv4 = nn.Parameter(torch.randn((3, embed_size))) 
    
    def convolute(self, X, kernel):
        '''
        论文中的卷积操作
        @param
            X 形状是(batch_size, sentence_size, embed_size)
            kernel 形状是(h, embed_size)
        @return
            y 形状是(batch_size, sentence_size - h + 1, embed_size)
        '''
        h = kernel.shape[0]
        y = torch.zeros((X.shape[0], X.shape[1]- h + 1, X.shape[2]))
        for i in range(X.shape[0]):
            for j in range(X.shape[1]- h + 1):
                temp = X[i, j: j+h]
                y[i, j] = (temp * kernel).sum(dim=0)
        return y
    def forward(self, X):#X=batchsize*sentence_len*embed_size
        '''
        @param 
            X :输入形状(batch_size, sentence_size, embed_size)
        @return  
            输出 是一个(batch_size, embed_size)大小的向量
        '''
        X = torch.tanh(self.convolute(X, self.conv1))
        X = torch.tanh(self.convolute(X, self.conv2))
        X = torch.tanh(self.convolute(X, self.conv3))
        if self.sentence_size == 7:
            X = torch.tanh(self.convolute(X, self.conv4))
        return X.view(X.shape[0], -1)  #返回的X的形状：(batch_size, embed_size) 
