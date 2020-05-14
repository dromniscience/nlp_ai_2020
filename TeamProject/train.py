"""此模块包含:
训练函数定义
"""

__all__=[]

# %%
from hyperdata_funct import *
from data import *
from models import *
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import time
torch.manual_seed(1)



# %% [markdown]
# ## train 模块

# %%
def train(input_tensor, target_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion, wd2Idx,
          num_topic, is_lreg):
    """
    @params
        input_tensor:batch,seq_len
    """
    encoder.train()
    decoder.train()

    input_tensor = input_tensor.permute(1, 0).contiguous()
    target_tensor = target_tensor.permute(1, 0).contiguous()

    encoder_hidden = encoder.initHidden(input_tensor.size()[1])

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    input_len = input_tensor.size(0)
    target_len = target_tensor.size(0)

    encoder_outputs = torch.zeros(LEN + 2, encoder.hidden_size, device=device)  # 单向、batch=1
    loss = 0

    encoder_outputs, encoder_hidden = encoder(input_tensor, encoder_hidden)
    # encoder_outputs:encode_seq_len,batch,num_dir*hidden_size
    # encoder_hidden:num_layer*num_dir,batch,hidden_size

    decoder_input = torch.tensor([wd2Idx["<S>"]] * BATCH_SIZE, device=device).view(1, BATCH_SIZE)
    zeros_tmp = torch.zeros((encoder.num_layer, BATCH_SIZE, decoder.num_topic), device=device)
    decoder_hidden = torch.cat((encoder_hidden, zeros_tmp), 2)
    if is_lreg:
        decoder_hidden_topic = []
        for i in range(decoder.num_topic):
            longtensor = torch.ones((encoder.num_layer, BATCH_SIZE, num_topic), dtype=torch.long, device=device) * i

            tmp = zeros_tmp.scatter(2, longtensor, 1)
            decoder_hidden_topic_tmp = torch.cat((encoder_hidden, tmp), 2)
            # print("decoder_hidden_topic %d" %(i))
            # print(decoder_hn_topic_tmp.size())
            decoder_hidden_topic.append(decoder_hidden_topic_tmp)

        Q_list = [torch.zeros((BATCH_SIZE, num_topic), device=device) for _ in range(num_topic)]
    # Teacher forcing
    for di in range(target_len):
        decoder_output, decoder_hidden, decoder_attention, Q = decoder(
            decoder_input, decoder_hidden, encoder_outputs
        )
        loss += criterion(decoder_output, target_tensor[di])
        if is_lreg:
            for i in range(decoder.num_topic):
                # print(i)
                # print(decoder_hidden_topic[i][0].size())
                decoder_output_topic, decoder_hidden_topic[i], decoder_attention_topic, Q_topic = decoder(
                    decoder_input, decoder_hidden_topic[i], encoder_outputs
                )
                Q_list[i] = Q_list[i] + Q_topic
        decoder_input = target_tensor[di].view(1, -1)
    if is_lreg:
        for i in range(num_topic):
            # print(Q_list[i].size())
            Q_list[i] /= target_len
            Q_list[i] = F.softmax(Q_list[i], dim=1)
    loss_reg = 0
    # print(Q_list)
    if is_lreg:
        for k in range(num_topic):
            for b in range(BATCH_SIZE):
                loss_reg -= torch.log(Q_list[k][b][k])
    loss_reg = 2 * (loss_reg * target_len / num_topic / BATCH_SIZE)
    print("loss_reg: %f" % (loss_reg / target_len))
    loss += loss_reg
    loss.backward()
    encoder_optimizer.step()
    decoder_optimizer.step()

    return loss.item() / target_len


# %% [markdown]
# ## trainIters 模块

# %%
def trainIters(encoder, decoder, wd2Idx, epoch, num_topic, print_every=100, plot_every=100, learning_rate=0.005):
    global X_batch, Y_batch

    print(X_batch.size())
    start = time.time()
    plot_losses = []
    print_loss_total = 0  # Reset every print_every
    plot_loss_total = 0  # Reset every plot_every

    encoder_optimizer = optim.Adam(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.Adam(decoder.parameters(), lr=learning_rate)

    criterion = nn.CrossEntropyLoss()
    batch_len = len(X_batch)
    for ep in range(epoch):
        # if ep > 0:
        #     _, _ = load_model('checkpoint{:d}.tar'.format(ep - 1), encoder, decoder, encoder_optimizer, decoder_optimizer)
        is_lreg = True if ep < 5 else False
        print("epoch:{}".format(ep))
        for iter in range(0, batch_len):
            input_tensor = X_batch[iter]
            target_tensor = Y_batch[iter]

            loss = train(input_tensor, target_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion,
                         wd2Idx, num_topic, is_lreg)
            print_loss_total += loss
            plot_loss_total += loss

            if iter % print_every == 0:
                print_loss_avg = print_loss_total / print_every
                print_loss_total = 0
                print('%s (%d %d%%) %.4f' % (timeSince(start, (iter + 1) / batch_len),
                                             iter + 1, (iter + 1) / batch_len * 100, print_loss_avg))

            if iter % plot_every == 0:
                plot_loss_avg = plot_loss_total / plot_every
                plot_losses.append(plot_loss_avg)
                plot_loss_total = 0
        print("save model seq2seq_attn_bigru in epoch %d" % (ep))
        torch.save(encoder.state_dict(), "models/wuyan/seq2seq_attn_bigru_encoder.pth")
        torch.save(decoder.state_dict(), "models/wuyan/seq2seq_attn_bigru_decoder.pth")
    # showPlot(plot_losses)

# %% [markdown]
# ## 加载预训练词向量
# %%
word_vec_net = nn.Sequential(nn.Embedding(len(vocab), 200),
                         nn.Embedding(len(vocab), 200))
word_vec_net.load_state_dict(torch.load("../word_vector.pth",map_location=torch.device('cpu')))


# %%
encoder = Encoder(len(wd2Idx), hidden_size,vec_dim,num_layer)
decoder = Decoder(len(wd2Idx), hidden_size,vec_dim,num_layer,num_topic,dropout_p=0.1)
encoder.embedding.weight.data.copy_(word_vec_net[0].weight.data)
decoder.embedding.weight.data.copy_(word_vec_net[0].weight.data)
encoder.load_state_dict(torch.load("models/wuyan/seq2seq_attn_bigru_encoder.pth"))
decoder.load_state_dict(torch.load("models/wuyan/seq2seq_attn_bigru_decoder.pth"))
encoder = encoder.to(device)
decoder = decoder.to(device)

trainIters(encoder, decoder,wd2Idx,epoch=10, num_topic=num_topic,print_every=5,learning_rate=0.001)
