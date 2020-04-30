import torch
import torch.nn
import numpy as np
device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyper-parameters
penalty_rate=0.5
LR=0.01
BATCH_SIZE=128
log_dir="./model.pth"

epoch_finish5=0
epoch_finish7=0
net=Net().to(device)
loss_function=torch.nn.CrossEntropyLoss()
optimizer=torch.optim.SGD(net.parameters(),lr = LR,weight_decay=penalty_rate)

if os.path.exists(log_dir):
    checkpoint = torch.load(log_dir)
    cnn.load_state_dict(checkpoint['model'])
    optimizer.load_state_dict(checkpoint['optimizer'])
    start_epoch = checkpoint['epoch']
    print('加载 epoch {} 成功！'.format(start_epoch))
else:
    start_epoch=0

def train(model,loss_func,optim,num_epochs):
    global poem_vec_lst5,poem_vec_lst7,BATCH_SIZE,epoch_finish5,epoch_finish7
    for epoch in range(start_epoch,start_epoch+num_epochs):
        print('Starting epoch %d / %d' % (epoch+1,start_epoch+num_epochs))
        model.train()
        epoch_finish5=0
        epoch_finish7=0
        while epoch_finish5==1:
            batch_x,batch_y=get_batch(poem_vec_lst5,BATCH_SIZE)
            output=model(batch_x)
            loss=loss_func(output,batch_y)#output是每个位置预测每个字的概率分布矩阵，batch_y是一维数组，分别是ground_truth中每个位置字的index
            
            optim.zero_grad()
            loss.backward()
            optim.step()
            
            state={'model':model.state_dict(),'optimizer':optimizer.state_dict(),'epoch':epoch}
            torch.save(state,log_dir)

        while epoch_finish7==1:
            batch_x,batch_y=get_batch(poem_vec_lst7,BATCH_SIZE)
            output=model(batch_x)
            loss=loss_func(output,batch_y)
            
            optim.zero_grad()
            loss.backward()
            optim.step()
            
            state={'model':model.state_dict(),'optimizer':optimizer.state_dict(),'epoch':epoch}
            torch.save(state,log_dir)

def valid(model,loss_func):
    global val_vec_lst5,val_vec_lst7,BATCH_SIZE,epoch_finish5,epoch_finish7
    model.eval()
    total_loss=0
    
    epoch_finish5=0
    epoch_finish7=0
    while epoch_finish5==1:
        batch_x,batch_y=get_batch(val_vec_lst5,BATCH_SIZE)
        output=model(batch_x)
        loss=loss_func(output,batch_y)
        total_loss+=loss

    while epoch_finish7==1:
        batch_x,batch_y=get_batch(val_vec_lst7,BATCH_SIZE)
        output=model(batch_x)
        loss=loss_func(output,batch_y)
        total_loss+=loss

    return total_loss
    
def test(model):
    global test_vec_lst5,test_vec_lst7,epoch_finish5,epoch_finish7,idx2Wd5,idx2Wd7
    model.eval()
    
    epoch_finish5=0
    epoch_finish7=0
    while epoch_finish5==1:
        batch_x,batch_y=get_batch(test_vec_lst5,BATCH_SIZE)
        output=model(batch_x)
        output=np.argmax(output,axis=0)  # 假设一个列向量为一个位置的预测
        length=len(output)
        for i in range(length):
            print(idx2Wd5[output[i]])
        
    while epoch_finish7==1:
        batch_x,batch_y=get_batch(test_vec_lst7,BATCH_SIZE)
        output=model(batch_x)
        output=np.argmax(output,axis=0)
        length=len(output)
        for i in range(length):
            print(idx2Wd7[output[i]])
    
train(model=net,loss_func=loss_function,optim=optimizer,num_epochs=100)
valid(model=net,loss_func=loss_function)
test(model=net)
