
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
    for i in topk[1:]:
        print(cos[i], idx2Wd[i])

root_path = os.path.abspath('../')
#读入词典
vocab_path = root_path +  '\\Data\\word_vocab_for_rnn.pkl'
with open( vocab_path, 'rb') as f:
     vocab = pickle.load(f)
wd2Idx = {wd: idx for idx, wd in enumerate(vocab)}
idx2Wd = {idx: wd for idx, wd in enumerate(vocab)}

vocab_size = len(vocab)
embed_size = 200
#读取预训练的词向量
word_vec_net = nn.Sequential(nn.Embedding(vocab_size, embed_size), nn.Embedding(vocab_size, embed_size))
wordVec_path = root_path + '\\Data\\word_vector_for_rnn.pth'
word_vec_net.load_state_dict(torch.load(wordVec_path,map_location=torch.device('cpu')))
W = word_vec_net[0].weight.data

