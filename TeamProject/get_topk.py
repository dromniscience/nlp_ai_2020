
import torch 
import torch.nn as nn 
import torch.utils.data
import sys
import os
import random
import math
import torch.nn.functional as F
import pickle
def get_similar_word(word, k, W, idx2Wd):
    x = W[wd2Idx[word]]
    cos = torch.matmul(W, x) / (torch.sum(W*W, dim = 1) * torch.sum(x*x) ).sqrt()
    _, topk = torch.topk(cos, k=k+1)
    topk = topk.cpu().numpy()
    lst=[]
    for i in topk[1:]:
        print(cos[i], idx2Wd[i])
        lst.append([cos[i],idx2Wd[i]])
        
    return lst

root_path = os.path.abspath('./')
#读入词典
vocab_path = root_path +  '\\word_vocab.pkl'
with open( vocab_path, 'rb') as f:
     vocab = pickle.load(f)
wd2Idx = {wd: vocab[wd] for wd in vocab.keys()}
idx2Wd = {vocab[wd]: wd for  wd in vocab.keys()}

vocab_size = len(vocab)
embed_size = 200
#读取预训练的词向量
word_vec_net = nn.Sequential(nn.Embedding(vocab_size, embed_size), nn.Embedding(vocab_size, embed_size))
wordVec_path = root_path + '\\word_vector.pth'
word_vec_net.load_state_dict(torch.load(wordVec_path,map_location=torch.device('cpu')))
W = word_vec_net[0].weight.data

def jiekou(word):
    return get_similar_word(word, 5, W, idx2Wd)
