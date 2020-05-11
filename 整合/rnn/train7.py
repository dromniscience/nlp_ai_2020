import os,sys
import random
import numpy as np
import torch
import torch.nn as nn
import pickle
from Net import Net
from get_data import get_batch, get_test_batch, get_train_data, get_test_data


def train(model,loss_func,optim,poem_vec_lst7, num_epochs, model_path):
     global BATCH_SIZE,get_batch,idx2Wd,vocab_size,sentence_len
     for epoch in range(start_epoch,start_epoch+num_epochs):
          print('Starting epoch %d / %d' % (epoch+1,start_epoch+num_epochs))
          model.train()  #设置网络模型为train模式
          #每个epoch取epoch_size//batch_size次，分别使idx取0,1,2,...,epoch_size//batch_size-1
          for idx in range(len(poem_vec_lst7)//BATCH_SIZE):
               print(idx*BATCH_SIZE,"/",len(poem_vec_lst7))
               batch_x,batch_y=get_batch(poem_vec_lst7,BATCH_SIZE,idx, 7)#得到batch_x,batch_y
               batch_x=np.array(batch_x)
               batch_y=np.array(batch_y)
               output=model(batch_x,True)#output为模型预测的向量
            
               #将output变成BATCH_SIZE*3(句)*每句sentence_len个字，每个字有vocab_size种选择的向量
               output=torch.reshape(output,(BATCH_SIZE*3*sentence_len,vocab_size))
               #将output变成BATCH_SIZE*3(句)*每句sentence_len个字，每个位置是ground_truth对应字的index
               batch_y=np.reshape(batch_y,BATCH_SIZE*3*sentence_len)
               batch_y=torch.LongTensor(batch_y)
               #output中选出概率最大的字，这个字的index放到wordidx里
               wordidx=torch.argmax(output,dim=1)
               
               
               loss=loss_func(output,batch_y)#output是每个位置预测每个字的概率分布矩阵，batch_y是一维数组，分别是ground_truth中每个位置字的index
               print('loss is %lf'%(loss.item()))
               
               loss.backward()
               optim.step()
               optim.zero_grad()
          #print('epoch '%) 
          #保存模型
          print("save model in epoch %d "%(epoch))
          torch.save(model.state_dict(), model_path + "\\rnn7_epoch_%d.pth"%(epoch))
           



root_path = os.path.abspath('../') #项目的根目录,这里要保证它是整个项目的根目录

#读入词典
vocab_path = root_path +  '\\Data\\word_vocab_for_rnn.pkl'
with open( vocab_path, 'rb') as f:
     vocab = pickle.load(f)
wd2Idx = {wd: idx for idx, wd in enumerate(vocab)}
idx2Wd = {idx: wd for idx, wd in enumerate(vocab)}

#读取训练数据，这里是七言的古诗
train_data_path = root_path + '\\Data\\qtrain'
poem_line_lst7,  poem_vec_lst7 = get_train_data( train_data_path, wd2Idx, 7)


# 超参数
LR=0.001
BATCH_SIZE=128
vocab_size=6773
embed_size=200
hidden_size=200   

start_epoch=0  #现在是从第start_epoch轮开始训练的
sentence_len=7  #七言
net7=Net(sentence_len=sentence_len,batch_size=BATCH_SIZE,vocab_size=vocab_size,embed_size=embed_size,hidden_size=hidden_size)
loss_function=torch.nn.CrossEntropyLoss()
optimizer=torch.optim.Adam(net7.parameters(),lr = LR)

#读取预训练的词向量
word_vec_net = nn.Sequential(nn.Embedding(vocab_size, embed_size), nn.Embedding(vocab_size, embed_size))
wordVec_path = root_path + '\\Data\\word_vector_for_rnn.pth'
word_vec_net.load_state_dict(torch.load(wordVec_path,map_location=torch.device('cpu')))
net7.embedding.weight.data.copy_(word_vec_net[0].weight.data)

net7.load_state_dict(torch.load(root_path + '\\Models\\rnn\\model7_epoch_1.pth')['model'])
#训练
model_path = root_path + '\\Models\\rnn'
train(net7,loss_function,optimizer,poem_vec_lst7, 5, model_path)

