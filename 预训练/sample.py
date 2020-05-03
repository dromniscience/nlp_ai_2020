import collections
import torch 
import torch.nn as nn 
import torch.utils.data as data
import sys
import os
import random
import math

class Sample(data.Dataset):
    '''
    采样类：用于对原始数据进行采样
    '''
    def __init__(self, raw_data_set, max_window_size, noise_num):
        '''
        raw_data_set 最初的数据集
        max_window_size：最大窗口大小。如果窗口大小是2，那么就在中心词左边采2个，右边采2个
        noise_num ：每一对（中心词，背景词）所对应的要采样的噪声词的个数
        '''
        self.max_window_size = max_window_size
        self.noise_num = noise_num
        self.words_num = sum([len(poem) for poem in raw_data_set]) #总词数。包括重复出现的词
        #counter是一个dict,对应每个word和它的出现次数
        self.counter = collections.Counter([word for poem in raw_data_set for word in poem])
        self.idx2word = [word for word, _ in self.counter.items()]
        self.word2idx = {word: idx for idx, word in enumerate(self.idx2word)}
        #data_set是raw_data_set对应的词索引形式
        self.data_set = [[self.word2idx[word] for word in poem ] for poem in raw_data_set]
        self.center_words = [] #中心词
        self.context_words = [] #背景词
        self.noise_words = [] #噪声词
               
    
    #提取中心词和背景词
    def get_center_and_context(self):
        for x in self.data_set:
            if len(x) >= 2:#如果一个句子的词数大于等于2，才能看出中心词和背景词
                self.center_words += x
                for i in range(len(x)):
                    window_size = random.randint(1, self.max_window_size)
                    indices = list(range(max(0, i- window_size), min(len(x), i + window_size + 1))) #背景词的索引
                    indices.remove(i)#把背景词索引中的中心词索引拿掉
                    self.context_words.append([x[k] for k in indices]) #添加该中心词所对应的背景词

    #负采样，采样噪声词
    def get_negative_samples(self):
        #噪声词采样频率P(w)为w词频与总词频之比的0.75次方
        sampling_weights = [self.counter[word]**0.75 for word in self.idx2word]
        neg_candidates = []#候选的噪声词
        i = 0
        population = list(range(len(sampling_weights)))#每个词的编号,为了一次性生成大量候选词

        for contexts in self.context_words:#遍历每个batch，contexts是该batch下的背景词
            noises = []
            #每个背景词要采样noise_num个噪声词，因此总共要采样这么多背景词
            while len(noises) < len(contexts) * self.noise_num:                
                if i == len(neg_candidates):
                    #一次性生成1e5个候选的噪声词，能加快选择速度
                    i, neg_candidates = 0, random.choices(population, sampling_weights, k=int(1e5))
                neg, i = neg_candidates[i], i + 1
                #采样未出现在背景窗口的噪声词
                if neg not in set(contexts):
                    noises.append(neg)
            self.noise_words.append(noises)

    def get_sample_data(self):
        '''
        得到中心词，背景词，噪声词
        '''
        
        #先对数据集进行二次采样，得到新的数据集
        #二次采样的目的是，让频率过高的词低一些。不进行二次采样其实也可以
        subsample_set = []
        for sample in self.data_set:
            subsample = []
            for idx in sample:
                if random.uniform(0, 1) > 1 - math.sqrt(1e-4/self.counter[self.idx2word[idx]] * self.words_num):
                    subsample.append(idx)
            subsample_set.append(subsample)
        
        #得到中心词，背景词，噪声词
        self.data_set = subsample_set
        self.get_center_and_context()
        self.get_negative_samples()
        return self.center_words, self.context_words, self.noise_words


        