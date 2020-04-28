r'''Implement RCM model

    Its input is a tensor of the shape (batch_size, seq_len, input_size), which embeds the previous i lines.
    It generates context representations for every position in the (i+1)-th line, which is a tensor of the shape (batch_size, m-1, output_size).

    According to the paper,
    seq_len = i
    input_size = q
    hidden_size = q
    output_size = q

    Current RCM version uses tanh() as its nonlinear function. (Both in RNN and decoding)
    Both RNN network and decoding part take no bias.
    However these attributes can be easily modified.

    If you want it to run on GPU, please specifically configure it.
'''

import torch
import torch.nn as nn

# Hyper-parameters
r'''
q:          hidden_size, by default 200
V:          set of Chinese characters
L:          a pre-trained word-embedding matrix of the size q*|V|
word2no:    a dict entitling each character to a unique no
m:          the number of characters in every verse
batch_size: recommended to be 2^k
'''

# RCM module
class RCM(nn.Module):
    def __init__(self, m, input_size, hidden_size, num_layers, output_size):
        super().__init__()
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
        for _ in range(m - 1):
            self.linear.append(nn.Linear(hidden_size, output_size, bias=False))

    def forward(self, x):
        # x: tensor of shape (batch_size, seq_len, input_size)

        # Set initial hidden and cell states
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)

        # Forward propagate RNN
        out, _ = self.rnn(x, h0)  # out: tensor of shape (batch_size, seq_length, hidden_size)
        out = out[:,-1,:]         # out: tensor of shape (batch_size, hidden_size)

        # Generate representations
        position = []
        for _ in range(self.m - 1):
            position.append(torch.tanh(self.linear[_](out)))
        outputs = torch.stack(position, 1)  # outputs: tensor of shape (batch_size, m-1, output_size)
        return outputs

# Testing
if __name__ == '__main__':
    model = RCM(5, 10, 10, 2, 10)

    inputs = torch.randn(20,2,10)
    outputs = model(inputs)
    print(outputs.size())
