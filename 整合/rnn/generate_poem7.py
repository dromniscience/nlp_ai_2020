import os,sys
import random
import numpy as np
import torch
import torch.nn as nn
import pickle
from Net import Net
from get_data import get_test_data, get_test_batch

BATCH_SIZE = 128
vocab_size = 6773
embed_size = 200
hidden_size = 200  
sentence_len = 7
root_path = os.path.abspath('../')


#读入词典
vocab_path = root_path +  '\\Data\\word_vocab_for_rnn.pkl'
with open( vocab_path, 'rb') as f:
     vocab = pickle.load(f)
wd2Idx = {wd: idx for idx, wd in enumerate(vocab)}
idx2Wd = {idx: wd for idx, wd in enumerate(vocab)}

#读取测试集
test_data_path = root_path + '\\Data\\qtest7'
testline,testvec=get_test_data(test_data_path, wd2Idx, sentence_len)
testbatch=get_test_batch(testvec,BATCH_SIZE,0) #得到一个batch的测试数据

#读取网络
net7=Net(sentence_len=sentence_len,batch_size=BATCH_SIZE,vocab_size=vocab_size,embed_size=embed_size,hidden_size=hidden_size)
net_path = root_path + '\\Models\\rnn\\rnn7_epoch_1.pth'
net7.load_state_dict(torch.load(net_path))
net7.eval() #表示此时网络不在训练
testbatch=np.array(testbatch)
print(testbatch.shape)

output=net7(testbatch,False)  #一个batch测试的输出

output=torch.reshape(output,(BATCH_SIZE*3*sentence_len,vocab_size))  #每个输入的输出是3(句)*sentence_len个字的概率分布

wordidx=torch.argmax(output,dim=1)#取概率最大的

#输出测试集的结果
with open("out7.txt", "w", encoding="utf-8") as f:     
     for i in range(BATCH_SIZE):
          f.write('\n')
          f.write('\n')
          for j in range(7):
               f.write(idx2Wd[testbatch[0][i][j]])
          
          start = i * 21
          for k in range(21):
               if(k % 7)==0:
                    f.write('\n')
               f.write(idx2Wd[int(wordidx[start+k])])

          