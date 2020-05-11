import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt


# RGM Module
class RGM(nn.Module):
    def __init__(self,batch_size,vocab_size,hidden_size,output_size,embed_size,context_size):
        super(RGM, self).__init__()
        self.batch_size=batch_size
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.embed_size = embed_size
        self.context_size = context_size
        
        self.fc1 = nn.Linear(self.vocab_size, self.hidden_size, bias=False)#矩阵X
        self.fc2 = nn.Linear(self.context_size, self.hidden_size, bias=False)#矩阵H
        self.fc3 = nn.Linear(self.hidden_size, self.hidden_size, bias=False)#矩阵R
        
    def forward(self, r, w, context):#r=batch*1*hidden_size,
                                     #w=batch*1*vocab_size,
                                     #context=batch*1*context_size
        
        r=torch.Tensor(r)
        w=torch.Tensor(w)
        context=torch.Tensor(context)
        torch.reshape(r,(self.batch_size,self.hidden_size))
        torch.reshape(w,(self.batch_size,self.vocab_size))
        torch.reshape(context,(self.batch_size,self.context_size))
        word_input = self.fc1(w)
        context_input = self.fc2(context)
        hidden_input = self.fc3(r)
        temp=hidden_input
        hidden_output= torch.tanh(word_input+context_input+temp)
        return hidden_output #batch*hidden_size

