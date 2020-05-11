预训练词向量的部分

和github上的代码不同。这里已经封装好了，只需要打开train_and_generate.ipynb文件就可以看到训练和使用词向量的步骤

每个文件的具体功能：
    - sample.py 负责采样，提取中心词，背景词，噪声词
    - MyDataSet.py 负责把以上的三组词封装到一个dataset里
    - word_vector_train.py 负责训练词向量。如果你想更改模型的存储路径，可以去这里面更改。
    - LoadData.py 负责读入数据
    - CSM.py 只是为了展示如何使用词向量的例子。并不重要
请看train_and_generate.ipynb的“重要"部分。并适当修改部分代码，从而保证加入分隔符后不出错。