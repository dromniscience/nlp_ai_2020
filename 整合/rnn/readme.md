各文件：
- get_data 读入文件
- CSM 模型的CSM部分
- RCM 模型的RCM部分
- RGM 模型的RGM部分
- Net 将上三个模型部分整合在一起
- train5 训练生成五言的模型
- train7 训练生成七言的模型
- generate_poem5 生成五言诗
- generate_poem7 生成七言诗

如果出现读入路径问题，只需修改root_path变量。保证root_path是整个项目的根目录，即rnn文件夹的上级文件夹。