import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

# rnn = nn.RNN(10, 20, 2)
# input = torch.randn(5, 3, 10)
# h0 = torch.randn(2, 3, 20)
# output, hn = rnn(input, h0)

# print(output.size())
# print(hn.size())

input_size = 10
hidden_size = 101
output_size = 102
embed_size = 103
context_size = 104


class RGM(nn.Module):
    def __init__(self):
        super(RGM, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.embed_size = embed_size
        self.context_size = context_size
        self.rnn = nn.RNN(self.input_size, self.hidden_size,
                          batch_first=True, bias=False)
        self.fc1 = nn.Linear(self.embed_size, self.input_size, bias=False)
        self.fc2 = nn.Linear(self.context_size, self.input_size, bias=False)
        self.fc3 = nn.Linear(self.hidden_size, self.output_size, bias=False)

    def forward(self, w, context):
        '''
        w:          batch * seq_len * embed_size
        context:    batch * seq_len * context_size
        generate a sequence of words from word vectors and context vectors
        '''
        word_input = self.fc1(w)
        context_input = self.fc2(context)
        # output shape: batch * seq_len * hidden_size
        output, hn = self.rnn(word_input + context_input)
        # output shape: batch * seq_len * output_size
        output = self.fc3(output)
        return output, hn


rgm = RGM()

input1 = torch.rand(3, 200, embed_size)
input2 = torch.rand(3, 200, context_size)
output, hn = rgm.forward(input1, input2)
print(output.size())
print(hn.size())
