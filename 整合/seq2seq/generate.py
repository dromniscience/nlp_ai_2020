"""此模块包含:
Beam Search的生成模型实现
"""

__all__ = ['generate']

from hyperdata_funct import *
from data import *
from models import *
import torch
import torch.nn.functional as F
import numpy as np
import os
torch.manual_seed(1)


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--line", help="请输入一句五言诗!")
args = parser.parse_args()
input_verse = args.line

# 检查命令行输入
def str2tensor(input_verse):
    assert isinstance(input_verse, str), "请输入字符串!"
    assert len(input_verse) == 5, "诗句长度应为5!"
    switch = [wd2Idx['<S>']]
    for wd in input_verse:
        assert wd in wd2Idx, "字符'%s'非中文汉字, 或者过于生僻!" % wd
        switch.append(wd2Idx[wd])
    switch.append(wd2Idx['，'])
    return torch.tensor(switch,device=device)

if input_verse:
    input_verse = str2tensor(input_verse)


# %% [markdown]
# ## Generate 模块

# %%
class trace:
    def __init__(self):
        self.poem = ["<S>"]
        self.hidden = None
        self.posb = 0


def generate_prepare(encoder, decoder, wd2Idx, idx2Wd, input_tensor, num_topic):
    """
    @params:
        input_tensor:(1,seq_len)  已经向量化了
    """
    encoder.eval()
    decoder.eval()

    input_tensor = input_tensor.permute(1, 0).contiguous()

    encoder_hidden = encoder.initHidden(1)
    encoder_outputs = torch.zeros(LEN + 2, encoder.hidden_size, device=device)
    encoder_outputs, encoder_hidden = encoder(input_tensor, encoder_hidden)

    zeros_tmp = torch.zeros((encoder.num_layer, 1, decoder.num_topic), device=device)
    decoder_hidden = torch.cat((encoder_hidden, zeros_tmp), 2)

    decoder_hidden_topic = []
    for i in range(decoder.num_topic):
        longtensor = torch.ones((encoder.num_layer, 1, num_topic), dtype=torch.long, device=device) * i
        tmp = zeros_tmp.scatter(2, longtensor, 1)
        # print(tmp)
        decoder_hidden_topic_tmp = torch.cat((encoder_hidden, tmp), 2)
        # print("decoder_hidden_topic %d" %(i))
        # print(decoder_hn_topic_tmp.size())
        decoder_hidden_topic.append(decoder_hidden_topic_tmp)
    # for i in decoder_hidden_topic:
    #     print(i)

    beam = [trace()]
    beam[0].hidden = decoder_hidden

    beam_list = [[trace()] for _ in range(num_topic)]
    for i in range(num_topic):
        beam_list[i][0].hidden = decoder_hidden_topic[i]

    # print("")
    # print(beam[0].hidden)
    # for i in range(num_topic):
    #     print(beam_list[i][0].hidden)

    k = 5
    for _ in range(3 * LEN + 4):
        btmp = []
        for tce in beam:
            inputs = torch.tensor([wd2Idx[tce.poem[-1]]]).view(1, 1).to(device)
            outputs, hidden, attention, Q = decoder(inputs, tce.hidden, encoder_outputs)
            topk = torch.topk(F.softmax(outputs[0]), k)
            for i in range(k):
                nxt = trace()
                nxt.poem = tce.poem + [idx2Wd[topk[1][i].item()]]
                nxt.hidden = hidden
                nxt.posb = tce.posb + np.log(topk[0][i].item())
                btmp.append(nxt)
        beam = []
        for _ in range(k):
            posMax = -1e6
            idxMax = 0
            for idx, tce in enumerate(btmp):
                if tce.posb - posMax > 1e-6:
                    posMax = tce.posb
                    idxMax = idx
            beam.append(btmp[idxMax])
            btmp.remove(btmp[idxMax])

    for i in range(num_topic):
        for _ in range(3 * LEN + 4):
            # for j in beam_list[i]:
            #     print(i, end=" ")
            #     print(j.poem)
            btmp = []
            for tce in beam_list[i]:
                inputs = torch.tensor([wd2Idx[tce.poem[-1]]]).view(1, 1).to(device)
                outputs, hidden, attention, Q = decoder(inputs, tce.hidden, encoder_outputs)
                topk = torch.topk(F.softmax(outputs[0]), k)
                for j in range(k):
                    nxt = trace()
                    nxt.poem = tce.poem + [idx2Wd[topk[1][j].item()]]
                    nxt.hidden = hidden
                    nxt.posb = tce.posb + np.log(topk[0][j].item())
                    btmp.append(nxt)
            beam_list[i] = []
            for _ in range(k):
                posMax = -1e6
                idxMax = 0
                for idx, tce in enumerate(btmp):
                    if tce.posb - posMax > 1e-6:
                        posMax = tce.posb
                        idxMax = idx
                beam_list[i].append(btmp[idxMax])
                btmp.remove(btmp[idxMax])

        # for i in range(decoder.num_topic):
        #     for j in beam_list[i]:
        #         for kk in beam:
        #             print(kk.hidden-j.hidden, end=" ")
        #     print("")

    return beam, beam_list


def generate(encoder, decoder, num_topic):
    global input_verse
    if input_verse == None:
        print("请输入一句五言诗句!")
        while not input_verse:
            input_verse = input().strip()
        input_verse = str2tensor(input_verse)

    input_tensor = input_verse.view(1, -1)
    beam_res, beam_res_list = generate_prepare(encoder, decoder, wd2Idx, idx2Wd, input_tensor, num_topic)
    encoded_words = [idx2Wd[idx.item()] for idx in input_tensor[0]]
    for idx, each in enumerate(beam_res):
        print("No.", idx, sep="")
        poem_lst = each.poem
        print(poem_lst)
        print("".join(encoded_words[1:]))
        for i in range(1,len(poem_lst)):
            print(poem_lst[i], end="")
            if (poem_lst[i] == "，")or (poem_lst[i]=="。"):
                print("")
        print("")
        print("posb:", each.posb)

    for i in range(num_topic):
        print("-" * 40)
        print("topic %d" % (i))
        print("-" * 40)
        for idx, each in enumerate(beam_res_list[i]):
            print("No.", idx, sep="")
            poem_lst = each.poem
            print(poem_lst)

            print("".join(encoded_words[1:]))
            for i in range(1,len(poem_lst)):
                print(poem_lst[i], end="")
                if (poem_lst[i] == "，")or (poem_lst[i]=="。"):
                    print("")
            print("")
            print("posb:", each.posb)


root_path = os.path.abspath('../')
model_path = root_path + '\\Models\\seq'
encoder = Encoder(len(wd2Idx), hidden_size,vec_dim,num_layer)
decoder = Decoder(len(wd2Idx), hidden_size,vec_dim,num_layer,num_topic,dropout_p=0.1)
encoder = encoder.to(device)
decoder = decoder.to(device)

encoder.load_state_dict(torch.load(model_path + '\\seq2seq_encoder.pth'))
decoder.load_state_dict(torch.load(model_path + '\\seq2seq_decoder.pth'))
encoder.eval()
decoder.eval()

generate(encoder, decoder, num_topic)
