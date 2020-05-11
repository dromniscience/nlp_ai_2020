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

#In[5]
def train_word_vector(net, data_iter, lr, loss, epochs):
    #训练模型，得到词向量
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
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
        #每个epoch做完，保存一下模型
        print('save word vector model,in epoch %d' %(epoch))
        torch.save(net.state_dict(), 'word_vec_epoch_%d.pth' % ( epoch))      
        print('epoch %d, loss %.2f, time %.2fs' % (epoch, loss_sum / n, time.time() - start_time))




