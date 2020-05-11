"""此模块包含:
Encoder和Decoder的类定义
"""

__all__ = ['Encoder','Decoder']

# %%
from hyperdata_funct import *
import torch
import torch.nn as nn
import torch.nn.functional as F
torch.manual_seed(1)

# %% [markdown]
# ## Encoder 模块

# %%
class Encoder(nn.Module):
    def __init__(self, input_size, hidden_size, vec_dim, num_layer):
        super(Encoder, self).__init__()
        self.hidden_size = hidden_size
        self.vec_dim = vec_dim
        self.embedding = nn.Embedding(input_size, vec_dim)
        self.gru = nn.GRU(vec_dim, hidden_size, num_layers=num_layer, bidirectional=True)
        self.num_layer = num_layer
        self.num_dir = 1 if self.gru.bidirectional == False else 2

    def forward(self, input, hidden):
        """
        @params:
            input:(seq_len,batch)
            hidden:(num_layers*num_dirs,batch,hidden_size)
        """
        seq_len, batch = input.size()

        embedded = self.embedding(input).view(seq_len, batch, -1)
        output = embedded  # output:(seq_len,batch,vec_dim)
        output, hidden = self.gru(output, hidden)  # output:(seq_len,batch,num_dir*hidden_size)
        # hidden:(num_layer*num_dir,batch,hidden_size)
        output = output[:, :, :self.hidden_size] + output[:, :, self.hidden_size:]
        hidden = hidden.view(self.num_layer, self.num_dir, batch, self.hidden_size)
        hidden = hidden[:, 0, :, :] + hidden[:, 1, :, :]
        # output:seq_len,batch,hidden_size
        # hidden:num_layer,batch,hidden_size
        return output, hidden

    def initHidden(self, bat):
        """
        @params
            bat:batch参数
        """
        return torch.zeros(self.num_layer * self.num_dir, bat, self.hidden_size, device=device)


# %% [markdown]
# ## 带attention机制的Decoder模块

# %%
class Decoder(nn.Module):
    def __init__(self, input_size, hidden_size, vec_dim, num_layer, num_topic, dropout_p):
        super(Decoder, self).__init__()
        self.encoder_hidden_size = hidden_size
        self.decoder_hidden_size = hidden_size + num_topic
        self.vec_dim = vec_dim
        self.embedding = nn.Embedding(input_size, vec_dim)
        self.encode_seq_len = LEN + 2
        self.dropout_p = dropout_p
        self.input_size = input_size
        self.num_layer = num_layer
        self.num_topic = num_topic
        self.all_word = torch.tensor([i for i in range(input_size)], dtype=torch.long, device=device)

        self.gru = nn.GRU(vec_dim, self.decoder_hidden_size, num_layers=num_layer, bidirectional=False)
        self.attn = nn.Linear(self.decoder_hidden_size + self.vec_dim, self.encode_seq_len)
        self.attn_combine = nn.Linear(self.encoder_hidden_size + self.vec_dim, self.vec_dim)
        self.dropout = nn.Dropout(self.dropout_p)
        self.out = nn.Linear(self.decoder_hidden_size, self.input_size)
        self.W = nn.Linear(self.vec_dim, self.num_topic, bias=False)

        self.num_dir = 1 if self.gru.bidirectional == False else 2

    def forward(self, input, hidden, encoder_outputs):
        """
        @params:
            encoder_outputs:encode_seq_len,batch,num_dir*hidden_size
            hidden:num_layer*num_dir,batch,hidden_size
            input:seq_len,batch
        """
        seq_len, batch = input.size()  # when decoding ,we let seq_len = 1

        embedded = self.embedding(input).view(seq_len, batch, -1)
        embedded = self.dropout(embedded)  # embedded:1,batch,vec_dim

        attn_weights = F.softmax(  # attn_weights:batch,encode_seq_len
            self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)
        attn_applied = torch.bmm(attn_weights.unsqueeze(1),
                                 encoder_outputs.permute(1, 0, 2).contiguous())
        # so far,shape of attn_applied:batch,1,hidden_size
        attn_applied = attn_applied.permute(1, 0, 2).contiguous()

        output = torch.cat((embedded[0], attn_applied[0]), 1)
        output = self.attn_combine(output).unsqueeze(0)
        output = F.relu(output)
        # output:1,batch,vec_dim
        output, hidden = self.gru(output, hidden)
        # output:1,batch,vec_dim
        logits = self.out(output)  # logits:1,batch,input_size
        logits = logits.view(-1, self.input_size)

        word_distribution = F.softmax(logits, dim=1)
        # (batch, word_num)
        # word_distribution = torch.squeeze(word_distribution, 0) # (batch, word_num)
        word_matrix = self.embedding(self.all_word)  # (word_num, vec_dim)
        expected_embedding = torch.mm(word_distribution, word_matrix)  # (batch, vec_dim)
        Q = self.W(expected_embedding)  # (batch, num_topic)

        return logits, hidden, attn_weights, Q

    def initHidden(self, bat):
        return torch.zeros(self.num_dir * self.num_layer, bat, self.hidden_size, device=device)
