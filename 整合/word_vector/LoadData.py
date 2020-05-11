"""
注：考虑到暂不知道具体实现，一些细节未予以处理
    1、每首诗的首尾位加<S>和<E>
    2、默认五言绝句与七言绝句分开训练，两者有两套不同的字典
    3、在实际使用中，为方便起见，可能需要对X_batch，Y_batch进行微调
    
"""

import os,sys
import random
random.seed(1)   #设置随机种子


root_path = ""  #到数据集的路径，可能根据具体情况修改
BATCH_SIZE=128

def get_train_data(fileName, wd2Idx ):
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
                poem_line_lst5.append(line)
               
            elif len(line) == 30:
                poem_line_lst7.append(line)
                

    random.shuffle(poem_line_lst5)
    random.shuffle(poem_line_lst7)

    poem_vec_lst5 = [[wd2Idx[wd] for wd in line] for line in poem_line_lst5]
    poem_vec_lst7 = [[wd2Idx[wd] for wd in line] for line in poem_line_lst7]

    

    return poem_line_lst5, poem_line_lst7,poem_vec_lst5, poem_vec_lst7



def get_eval_data(fileName,wd2Idx):
    """
    得到验证集
    @params:
        fileName:文件名，具体应该为"qtest"/"qvalid"
        wd2Idx:由训练集得到的的wd2Idx映射
       

    @return:
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
            if len(line) == 20:
                poem_line_lst5.append(line)
            elif len(line) == 28:
                poem_line_lst7.append(line)

    random.shuffle(poem_line_lst5)
    random.shuffle(poem_line_lst7)

    poem_vec_lst5 = [[wd2Idx.get(wd, wd2Idx["<unk>"])
                      for wd in line] for line in poem_line_lst5]
    poem_vec_lst7 = [[wd2Idx.get(wd, wd2Idx["<unk>"])
                      for wd in line] for line in poem_line_lst7]

    return poem_vec_lst5, poem_vec_lst7


def get_batch(data,bat):
    """
    @params:
        data:待划分的数据集
        bat:BATCH_SIZE
    
    @returns:
        X_batch:shape: len(data)//bat,bat,seq_len,其中seq_len包含四句诗
        Y_batch:shape: len(data)//bat,bat,seq_len,其中seq_len包含后三句诗
    """
    X_batch = []
    Y_batch = []
    for idx in range(len(data)//bat):
        st = idx * bat
        ed = st + bat
        X_batch.append(data[st:ed])
        Y_batch.append([vec[5:] for vec in data[st:ed]])
    
    return X_batch,Y_batch

if __name__ == "__main__":
    
    # 简单测试 get_train_data
    poem_line_lst5, poem_line_lst7, wd2Idx5, wd2Idx7, idx2Wd5, idx2Wd7, poem_vec_lst5, poem_vec_lst7 = get_train_data( 
        "qtrain")

    print(wd2Idx5.get("好",wd2Idx5["<unk>"]))
    print(wd2Idx5.get("好人",wd2Idx5["<unk>"]))
    print(wd2Idx5["<unk>"])
    print(len(wd2Idx5))
    print(len(wd2Idx7))
    print("______________________________________________________")
    # 简单测试 get_eval_data
    test_vec_lst5,test_vec_lst7 = get_eval_data("qtest",wd2Idx5,wd2Idx7)
    val_vec_lst5,val_vec_lst7 = get_eval_data("qvalid",wd2Idx5,wd2Idx7)

    print(len(test_vec_lst5))
    print(len(test_vec_lst7))
    print(test_vec_lst5[0])
    print(test_vec_lst7[0])

    print(len(val_vec_lst5))
    print(len(val_vec_lst7))
    print(val_vec_lst5[0])
    print(val_vec_lst7[0])
    print("______________________________________________________")
    # 简单测试 get_batch
    X_batch,Y_batch = get_batch(poem_vec_lst5,BATCH_SIZE)

    print(len(X_batch))
    print(len(Y_batch))
    print(X_batch[0][0:2])
    print(Y_batch[0][0:2])
