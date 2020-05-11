import os,sys
import random
import numpy as np
import torch
import torch.nn as nn
import pickle
from CSM import CSM  
from RCM import RCM 
from RGM import RGM 



# 拼成的整个网络
class Net(nn.Module):
    def __init__(self,batch_size,sentence_len,vocab_size,embed_size,hidden_size):
    # 其中hidden_size是三个网络模块所有的隐藏层的维度都一样，取200
        super(Net,self).__init__()
        self.batch_size=batch_size
        self.sentence_len=sentence_len
        self.vocab_size=vocab_size
        self.embed_size=embed_size
        self.hidden_size=hidden_size
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.csm=CSM(vocab_size=vocab_size,embed_size=embed_size,sentence_size=sentence_len)
        self.rcm=RCM(input_size=hidden_size,hidden_size=hidden_size,num_layers=2,output_size=hidden_size,m=sentence_len)
        self.rgm=RGM(batch_size=batch_size,vocab_size=vocab_size,hidden_size=hidden_size,output_size=vocab_size,embed_size=embed_size,context_size=hidden_size)
        self.final_fc = nn.Linear(hidden_size, vocab_size, bias=False)
        
    def forward(self,x,IsTrain): #训练时候IsTrain=True，测试时候IsTrain=False
    # x.shape=batch_size*(4(句)*每句5个字)
        if IsTrain:
            x=x.reshape(self.batch_size,4*self.sentence_len)
            
            xidx=x  #x等会儿变成embedding后的矩阵，因此将初始时的x(每个字的index)放入xidx中，之后要用
            x=self.embedding(torch.LongTensor(x))#x=batch_size*(4(句)*每句5个字)*embed_size
            
            #以下三个模块分别生成二、三、四句
            #生成第二句
            
            #用第一句的字生成第一句的context vector，一句话的context vector形状为batch_size*hidden_size
            sentence_vec1=self.csm(x[:,0:self.sentence_len])
            #这里reshape后dim=1的维度用来之后与后面句子的context vector进行拼接
            sentence_vec1=sentence_vec1.reshape(self.batch_size,1,self.hidden_size)
            #将前面所有的context vector变成context向量
            context1=self.rcm(sentence_vec1)
            
            y=torch.zeros(self.batch_size,3*self.sentence_len,self.vocab_size)
            #y是网络返回的张量，分别是后三句15个位置的概率分布
            
            for i in range(self.sentence_len):  #i=0-4分别代表第二行的五个字
                #这里的cur和prev是RGM模块中的r_{j}和r_{j-1}，迭代实现
                prev=torch.zeros(self.batch_size,self.hidden_size)
                cur=torch.zeros(self.batch_size,self.hidden_size)
                #wj是RGM式子中输入的前一个字的one_hot向量
                wj=torch.zeros(self.batch_size,self.vocab_size)
               
                if i==0:#i=0时直接把要返回的y定为输入的第sentence_len+1个字，也就是第二行第一个字
                    for j in range(self.batch_size):
                        y[j][0][xidx[j][self.sentence_len]]=1
                else:
                    # 前一个字的向量wj用输入的前一个字的one_hot向量，即teacher forcing机制
                    for j in range(self.batch_size):
                        wj[j][xidx[j][i+self.sentence_len-1]]=1
                    #cur为这一轮得到的r_{j}，在下一轮的RGM中用于输入，且用作最后fc层(hidden_size->vocab_size)的输入
                    cur=self.rgm(prev,wj,context1[:,i,:])
                    y[:,i,:]=self.final_fc(cur)
                prev=cur
            
                
                
            # 下面生成三、四句的模块是与前面一样的模块，重复两遍
                
            #生成第三句
            #用第二句的字生成第一句的context vector
            sentence_vec2=self.csm(x[:,self.sentence_len:2*self.sentence_len])
            
            sentence_vec2=sentence_vec2.reshape(self.batch_size,1,self.hidden_size)
            # 将第二句的context vector接在第一句的context vector后面
            sentence_vec2=torch.cat((sentence_vec1,sentence_vec2),1)   
            context2=self.rcm(sentence_vec2)
            
            for i in range(self.sentence_len,2*self.sentence_len):
                prev=torch.zeros(self.batch_size,self.hidden_size)
                cur=torch.zeros(self.batch_size,self.hidden_size)
                wj=torch.zeros(self.batch_size,self.vocab_size)
                
                if i==self.sentence_len:
                    for j in range(self.batch_size):
                        y[j][self.sentence_len][xidx[j][2*self.sentence_len]]=1
                else:
                    for j in range(self.batch_size):
                        wj[j][xidx[j][i+self.sentence_len-1]]=1
                    cur=self.rgm(prev,wj,context2[:,i-self.sentence_len,:])
                    y[:,i,:]=self.final_fc(cur)
                prev=cur
                
                
                
                
            #生成第四句 
            sentence_vec3=self.csm(x[:,2*self.sentence_len:3*self.sentence_len])
            sentence_vec3=sentence_vec3.reshape(self.batch_size,1,self.hidden_size)
            sentence_vec3=torch.cat((sentence_vec2,sentence_vec3),1)   
            context3=self.rcm(sentence_vec3)
 
            for i in range(2*self.sentence_len,3*self.sentence_len):
                prev=torch.zeros(self.batch_size,self.hidden_size)
                cur=torch.zeros(self.batch_size,self.hidden_size)
                wj=torch.zeros(self.batch_size,self.vocab_size)
                
                if i==2*self.sentence_len:
                    for j in range(self.batch_size):
                        y[j][2*self.sentence_len][xidx[j][3*self.sentence_len]]=1
                else:
                    for j in range(self.batch_size):
                        wj[j][xidx[j][i+self.sentence_len-1]]=1
                    cur=self.rgm(prev,wj,context3[:,i-2*self.sentence_len,:])
                    y[:,i,:]=self.final_fc(cur)
                prev=cur
                
        else: #IsTrain=False的情况，即测试集的情况
        
            #以下三个模块分别生成二、三、四句
            #生成第二句
            x=x.reshape(self.batch_size,self.sentence_len+3) #测试时输入每行有sentence_len+3个字
            
            # 将第一句放入x中，第二句首字放入first2中，第三句首字放入first3中，第四句首字放入first4中
            first2=x[:,self.sentence_len]
            first3=x[:,self.sentence_len+1]
            first4=x[:,self.sentence_len+2]
            x=x[:,0:self.sentence_len]
            
            
            x=self.embedding(torch.LongTensor(x))#x.shape=batch_size*sentence_len*embed_size
            #assist在x的后面加入15个字的位置的空向量，以便生成新的字时随时加入
            assist=torch.zeros(self.batch_size,3*self.sentence_len,self.embed_size)
            x=torch.cat((x,assist),dim=1)
            
            
            # 下面关于生成的模块与前面训练时类似
            sentence_vec1=self.csm(x[:,0:self.sentence_len])
            sentence_vec1=sentence_vec1.reshape(self.batch_size,1,self.hidden_size)
            context1=self.rcm(sentence_vec1)
            
            y=torch.zeros(self.batch_size,3*self.sentence_len,self.vocab_size)
            #y是网络的返回张量，分别是后三句15个位置的概率分布
            index=np.zeros((self.batch_size),dtype=int)
            for i in range(self.sentence_len):
                #这里的cur和prev是RGM模块中的r_{j}和r_{j-1}
                prev=torch.zeros(self.batch_size,self.hidden_size)
                cur=torch.zeros(self.batch_size,self.hidden_size)
                wj=torch.zeros(self.batch_size,self.vocab_size)
               
                if i==0:
                    for j in range(self.batch_size):
                        y[j][0][first2[j]]=1
                        index[j]=first2[j]
                else:
                    for j in range(self.batch_size):
                        wj[j][int(index[j])]=1
                    cur=self.rgm(prev,wj,context1[:,i,:])
                    y[:,i,:]=self.final_fc(cur)
                    index=torch.argmax(y[:,i,:],dim=1)
               
                #每生成一个字后就加入x中，为生成后面的context vector做准备
                newembed=self.embedding(torch.LongTensor(index))
                x[:,i+self.sentence_len,:]=newembed
                prev=cur
             
                
                
                
                
            #生成第三句
            sentence_vec2=self.csm(x[:,self.sentence_len:2*self.sentence_len])
            sentence_vec2=sentence_vec2.reshape(self.batch_size,1,self.hidden_size)
            sentence_vec2=torch.cat((sentence_vec1,sentence_vec2),1)   
            context2=self.rcm(sentence_vec2)
            
            index=np.zeros((self.batch_size),dtype=int)
            for i in range(self.sentence_len,2*self.sentence_len):
                prev=torch.zeros(self.batch_size,self.hidden_size)
                cur=torch.zeros(self.batch_size,self.hidden_size)
                wj=torch.zeros(self.batch_size,self.vocab_size)
                
                if i==self.sentence_len:
                    for j in range(self.batch_size):
                        y[j][self.sentence_len][first3[j]]=1
                        index[j]=first3[j]
                else:
                    for j in range(self.batch_size):
                        wj[j][int(index[j])]=1
                    cur=self.rgm(prev,wj,context2[:,i-self.sentence_len,:])
                    y[:,i,:]=self.final_fc(cur)
                    index=torch.argmax(y[:,i,:],dim=1)
                
                newembed=self.embedding(torch.LongTensor(index)) #batchsize*embed_size
                x[:,i+self.sentence_len,:]=newembed
                prev=cur
                        
                
            #生成第四句 
            sentence_vec3=self.csm(x[:,2*self.sentence_len:3*self.sentence_len])
            sentence_vec3=sentence_vec3.reshape(self.batch_size,1,self.hidden_size)
            sentence_vec3=torch.cat((sentence_vec2,sentence_vec3),1)   
            context3=self.rcm(sentence_vec3)
            
            index=np.zeros((self.batch_size),dtype=int)
            for i in range(2*self.sentence_len,3*self.sentence_len):
                
                prev=torch.zeros(self.batch_size,self.hidden_size)
                cur=torch.zeros(self.batch_size,self.hidden_size)
                wj=torch.zeros(self.batch_size,self.vocab_size)
                
                if i==2*self.sentence_len:
                    for j in range(self.batch_size):
                        y[j][2*self.sentence_len][first4[j]]=1
                        index[j]=first4[j]
                else:
                    for j in range(self.batch_size):
                        wj[j][int(index[j])]=1
                    cur=self.rgm(prev,wj,context3[:,i-2*self.sentence_len,:])
                    y[:,i,:]=self.final_fc(cur)
                    index=torch.argmax(y[:,i,:],dim=1)
                    
                newembed=self.embedding(torch.LongTensor(index)) #batchsize*embed_size
                x[:,i+self.sentence_len,:]=newembed
                prev=cur
        return y

