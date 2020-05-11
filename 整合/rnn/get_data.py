import os,sys
import random
import numpy as np
import torch
import torch.nn as nn
import pickle




def get_train_data(filePath, wd2Idx, sentence_size):  
    #读取训练集中的数据，训练集中有五言和七言的数据，这里现在是全部读入五言的并转化为one_hot向量
    """
    得到训练集
    @params:
        fileName:文件路径
        wd2Idx
        sentence_size:5或7；表示五言或七言
    @return:
        poem_line_lst:古诗列表
        poem_vec_lst:映射成one-hot向量后的古诗列表
        poem_line_lst
    其它:
        没有为每句诗加上<S>和<E>
    """
    poem_line_lst = []
    poem_vec_lst = []
    with open(filePath, 'r', encoding='utf-8') as fin:
        for line in fin:
            line = (" ".join(line.strip().split("\t"))).split(" ")
            if sentence_size == 5 and len(line) == 20:
                poem_line_lst.append(line)
            elif sentence_size == 7 and len(line) == 28:
                poem_line_lst.append(line)
    poem_vec_lst = [[wd2Idx[wd] for wd in line] for line in poem_line_lst]
    return poem_line_lst, poem_vec_lst


def get_test_data(filePath, wd2Idx, sentence_size):  
    """
    读取测试集中的数据，并将其转化为one_hot向量
    五言数据测试集中每行为8个字，前5个为第一句诗歌，后3个字为后面3句诗的开头
    @params:
        fileName:文件路径
        wd2Idx
        sentence_size:5或7,表示五言或七言
    @return:
        poem_line_lst5:五言绝句列表
        poem_vec_lst5:映射后的五言绝句列表
    其它:
        没有为每句诗加上<S>和<E>
    """
    poem_line_lst = []
    poem_vec_lst = []
    
    with open(filePath, 'r', encoding='utf-8') as fin:
        for line in fin:
            line = (" ".join(line.strip().split("\t"))).split(" ")
            if sentence_size == 5 and len(line) == 5+3:
                poem_line_lst.append(line)
            elif sentence_size == 7 and len(line) == 7+3:
                poem_line_lst.append(line)
    poem_vec_lst = [[wd2Idx[wd] for wd in line] for line in poem_line_lst]
    return poem_line_lst, poem_vec_lst



def get_batch(data,bat,idx, sentence_size):
    """
    训练时每个epoch取epoch_size//batch_size次batch，
    分别使idx取0,1,2,3,...,epoch_size//batch_size-1，以取数据集中不同的部分
    @params:
        data:待划分的数据集
        bat:BATCH_SIZE
    
    @returns:
        X_batch:shape: len(data)//bat,bat,seq_len,其中seq_len包含四句诗
        Y_batch:shape: len(data)//bat,bat,seq_len,其中seq_len包含后三句诗
    """
    X_batch = []
    Y_batch = []
    st = idx * bat
    ed = st + bat
    X_batch.append(data[st:ed])
    Y_batch.append([vec[sentence_size:] for vec in data[st:ed]])
    return X_batch,Y_batch


def get_test_batch(data,bat,idx):
# 从测试集中的one_hot向量中取一个batch的数据
    X_batch = []
    
    st = idx * bat
    ed = st + bat
    X_batch.append(data[st:ed])
    

    return X_batch
