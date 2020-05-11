import torch
import numpy as np 
import torch.nn as nn
import torch.nn.functional as F

class CSM(nn.Module):
    def __init__(self, vocab_size, embed_size, scentence_size):
        '''
        @param
        vocab_size: 词表大小
        embed_size:每个词向量的维度，相当于论文中的q
        scentence_size: 诗句的长度，5或7
        '''
        super(CSM, self).__init__()
        self.scentence_size = scentence_size
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.conv1 = nn.Parameter(torch.randn((2, embed_size)))
        self.conv2 = nn.Parameter(torch.randn((2, embed_size)))
        self.conv3 = nn.Parameter(torch.randn((3, embed_size)))
        self.conv4 = nn.Parameter(torch.randn((3, embed_size))) 
        
    
    def convolute(self, X, kernel):
        '''
        论文中的卷积操作，好像pytorch中没有现成的
        @param
            X 形状是(batch_size, scentence_size, embed_size)
            kernel 形状是(h, embed_size)
        @return
            y 形状是(batch_size, scentence_size - h + 1, embed_size)
        '''
        h = kernel.shape[0]
        y = torch.zeros((X.shape[0], X.shape[1]- h + 1, X.shape[2]))
        for i in range(X.shape[0]):
            for j in range(X.shape[1]- h + 1):
                temp = X[i, j: j+h]
                y[i, j] = (temp * kernel).sum(dim=0)
        return y
 
    def forward(self, X):
        '''
        @param 
            X :输入是batch_size*词索引形式的张量，形状是(batch_size, scentence_size)
        @return  
            输出 是一个(batch_size, embed_size)大小的向量
        '''
        X = self.embedding(X) #此时X形状(batch_size, scentence_size, embed_size)
        X = torch.sigmoid(self.convolute(X, self.conv1))
        X = torch.sigmoid(self.convolute(X, self.conv2))
        X = torch.sigmoid(self.convolute(X, self.conv3))
        if self.scentence_size == 7:
            X = torch.sigmoid(self.convolute(X, self.conv4))
        
        return X.view(X.shape[0], -1)  #返回的X的形状：(batch_size, embed_size) 
    
if __name__ == "__main__":
    # 测试
    datas = np.load("tang.npz", allow_pickle=True)
    data = datas['data']
    ix2word = datas['ix2word'].item()
    word2ix = datas['word2ix'].item()
    vocab_size = len(word2ix)
    embedding_size = 256
    scentence_size = 7
    poem = ['遥', '看', '瀑', '布', '挂', '前', '川']
    poem_idx = [word2ix[word] for word in poem]
    print(poem_idx)
    model = CSM(vocab_size, embedding_size, scentence_size)
    X = torch.tensor(poem_idx).view((1, 7))
    x1 = torch.tensor(X)
    y = model(X)
    assert x1.equal(X)
    print(y.shape)
