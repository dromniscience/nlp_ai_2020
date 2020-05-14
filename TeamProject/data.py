"""本模块包含:
源数据处理函数
    import本模块时将自动得到处理好的待训练数据
"""
__all__ = ['poem_line_lst5','poem_line_lst7','poem_vec_lst5','poem_vec_lst7', \
           'default_poem_lst','default_poem_vec','X_batch','Y_batch']

# %%
from hyperdata_funct import *
import torch
import random
torch.manual_seed(1)
random.seed(1)

# %%
def get_train_data(fileName, wd2Idx):
    """
    @params:
        fileName:文件名，具体应该为"qtrain"

    @return:
        poem_line_lst5:五言绝句列表
        poem_line_lst7:七言绝句列表
        poem_vec_lst5:映射后的五言绝句列表
        poem_vec_lst7:映射后的七言绝句列表

    其它:
        暂时没有为每句诗加上<S>和<E>
    """
    poem_line_lst5 = []
    poem_line_lst7 = []

    poem_vec_lst5 = []
    poem_vec_lst7 = []

    with open(root_path + fileName, 'r', encoding='utf-8') as fin:
        for line in fin:
            line = (" ".join(line.strip().split("\t"))).split(" ")
            line = ["<S>"] + line + ["<E>"]
            if len(line) == 22:
                line = line[:6]+["，"]+line[6:11]+["。"]+line[11:16]+["，"]+line[16:21]+["。"]+[line[21]]
                poem_line_lst5.append(line)

            elif len(line) == 30:
                line = line[:8]+["，"]+line[8:15]+["。"]+line[15:22]+["，"]+line[22:29]+["。"]+[line[29]]
                poem_line_lst7.append(line)

    random.shuffle(poem_line_lst5)
    random.shuffle(poem_line_lst7)

    poem_vec_lst5 = [[wd2Idx[wd] for wd in line] for line in poem_line_lst5]
    poem_vec_lst7 = [[wd2Idx[wd] for wd in line] for line in poem_line_lst7]

    return poem_line_lst5, poem_line_lst7, poem_vec_lst5, poem_vec_lst7

poem_line_lst5, poem_line_lst7, poem_vec_lst5, poem_vec_lst7 = get_train_data(
    "qtrain", wd2Idx)

if __name__ == '__main__':
    print(poem_vec_lst5[0])

default_poem_lst = poem_line_lst7 if LEN == 7 else poem_line_lst5
default_poem_vec = poem_vec_lst7 if LEN == 7 else poem_vec_lst5


# %%
def get_batch(data, bat, sent_len):
    """
    @params:
        data:待划分的数据集
        bat:BATCH_SIZE
        sent_len:单句长度

    @returns:
        X_batch:shape: len(data)//bat,bat,seq_len,其中seq_len包含四句诗
        Y_batch:shape: len(data)//bat,bat,seq_len,其中seq_len包含后三句诗
    """
    X_batch = []
    Y_batch = []
    for idx in range(len(data) // bat):
        st = idx * bat
        ed = st + bat
        X_batch.append([vec[:sent_len] for vec in data[st:ed]])
        Y_batch.append([vec[sent_len:] for vec in data[st:ed]])
    X_batch = torch.tensor(X_batch, device=device)
    Y_batch = torch.tensor(Y_batch, device=device)

    return X_batch, Y_batch

X_batch,Y_batch = get_batch(default_poem_vec,BATCH_SIZE,LEN+1+1)

if __name__ == '__main__':
    # %%
    print(X_batch.shape)
    print(X_batch.size(0))
    # print(X_batch[0].permute(1,0))
