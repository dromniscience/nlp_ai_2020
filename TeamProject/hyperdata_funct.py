"""本模块包含:
数据子文件夹路径
模型超参数
功能性函数
"""

__all__ = ['device','root_path','BATCH_SIZE','LEN','wd2Idx','idx2Wd','vocab',
           'hidden_size','vec_dim','num_layer','num_topic',
           'asMinutes','timeSince']

# %%
import torch
import time
import math
import pickle
torch.manual_seed(1)


# %%
# 环境设置
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)


# %% [markdown]
# ## 数据处理

# %%
root_path = "./"  #到数据集的路径，可能根据具体情况修改
BATCH_SIZE = 64
LEN = 5 # 用于决定5言还是7言


# %%
with open('./word_vocab.pkl', 'rb') as f:
     vocab = pickle.load(f)
wd2Idx = {wd: vocab[wd] for wd in vocab.keys()}
idx2Wd = {vocab[wd]: wd for wd in vocab.keys()}

if __name__ == '__main__':
    print(len(vocab))
    print(wd2Idx['水'])
    print(idx2Wd[2447])


# 模型超参数
# %%
hidden_size = 128
vec_dim = 200
num_layer = 1
num_topic = 10


# 功能性函数
def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


def timeSince(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (asMinutes(s), asMinutes(rs))
