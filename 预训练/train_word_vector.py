#In[1]
import collections
import torch 
import torch.nn as nn 
import torch.utils.data as data
import sys
import os
import random
import math
import torch.nn.functional as F
from sample import Sample
from MyDataSet import MyDataSet
import time

#In[2]
#二元交叉熵损失函数
class SigmoidBinCELoss(nn.Module):
    def __init__(self):
        super(SigmoidBinCELoss, self).__init__()
    def forward(self, inputs, targets, mask=None):
        inputs, targets, mask = inputs.float(), targets.float(), mask.float()
        res = F.binary_cross_entropy_with_logits(inputs, targets, reduction="none", weight=mask)
        return res.mean(dim=1)   
#In[3]
#跳字模型的前向计算,其实就是批量矩阵乘法
def skip_gram(center, context_and_negatives, embed_v, embed_u):
    u = embed_u(context_and_negatives)
    v = embed_v(center)
    u = u.permute(0, 2, 1)
    return torch.bmm(v, u)

#In[4]
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

#In[5]
def train(net, lr, loss, epochs):
    #训练模型，得到词向量
    device = torch.device('cuda' if torch.cuda.is_available else 'cpu')
    print('train on', device)
    net = net.to(device)
    optimizer = torch.optim.Adam(net.parameters(), lr=lr) 
    for epoch in range(epochs):
        start_time = time.time()
        loss_sum = 0.0
        n = 0
        for iter, batch in enumerate(data_iter):
            center, context, mask, label = [d.to(device) for d in batch]
            pred = skip_gram(center, context, net[0], net[1]) #跳字模型的前向计算
            #一个batch的平均loss
            ls = (loss(pred.view(label.shape), label, mask) * mask.shape[1] / mask.float().sum(dim=1)).mean()
            #梯度下降
            optimizer.zero_grad()
            ls.backward()
            optimizer.step()
            loss_sum += ls.item()
            n+=1
            if (iter + 1) % 500 == 0:
                print('save model')
                torch.save(net.state_dict(), 'net_epoch_%d_itr_%d.pth' % ( epoch, iter//1000))      
        print('epoch %d, loss %.2f, time %.2fs' % (epoch+1, loss_sum / n, time.time() - start_time))


#In[6]
#读取数据集
data_path = 'ptb.train.txt' #文件路径
with open(data_path) as f:
    lines = f.readlines()  
    #读取数据 raw_data_set就是字符形式的样本 
    raw_data_set = [scentence.split() for scentence in lines]   
    
#In[7]
#进行数据集的处理，构建模型
batch_size = 512
data_set = Sample(raw_data_set, 5, 5) #对raw_data_set进行采样
vocab_size = len(data_set.idx2word)
centers, all_contexts, noises = data_set.get_sample_data()#对raw_data_set进行采样，得到中心词，背景词，噪声词
data_set = MyDataSet(centers, all_contexts, noises)#把得到的词放到MyDataSet中
data_iter = data.DataLoader(data_set, batch_size, shuffle=True, collate_fn=collate_func, num_workers=0)
#构建词词嵌入层，训练其中的词向量
embed_size = 200
net = nn.Sequential(nn.Embedding(vocab_size, embed_size),
                    nn.Embedding(vocab_size, embed_size))
loss = SigmoidBinCELoss()

#In[8]

#训练
epochs = 10        
lr = 0.005     
train(net, lr=lr, loss=loss, epochs=epochs)

#In[9]

#读取训练得到的模型参数
net.load_state_dict(torch.load('net_epoch_9_itr_0.pth'))
#训练完成后，中心词向量net[0]可作为词的表征向量






