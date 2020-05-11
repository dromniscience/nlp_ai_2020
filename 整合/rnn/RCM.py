import os,sys
import random
import numpy as np
import torch
import torch.nn as nn
import pickle

class RCM(nn.Module):#改成了生成了1<=j<=m的context向量
    def __init__(self, m, input_size, hidden_size, num_layers, output_size):
        super(RCM, self).__init__()
        assert m in (5,7), r'Only 5-char or 7-char quatrain suits RCM model!'

        self.m = m
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_size = output_size

        self.rnn = nn.RNN(input_size,
                          hidden_size,
                          num_layers,
                          bias=False,
                          nonlinearity='tanh',
                          batch_first=True)
        self.linear = []
        for _ in range(m):
            self.linear.append(nn.Linear(hidden_size, output_size, bias=False))
        
    def forward(self, x):
        # x: tensor of shape (batch_size, seq_len, input_size)
        # Set initial hidden and cell states
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        out, _ = self.rnn(x, h0)  # out: tensor of shape (batch_size, seq_length, hidden_size)
        out = out[:,-1,:]         # out: tensor of shape (batch_size, hidden_size)

        # Generate representations
        position = []
        for _ in range(self.m):#这里本来是m-1，改成了m
            position.append(torch.tanh(self.linear[_](out)))
        
        outputs = torch.stack(position, 1)  # outputs: tensor of shape (batch_size, m, output_size)
        return outputs

