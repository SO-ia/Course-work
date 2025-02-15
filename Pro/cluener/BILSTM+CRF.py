import time
import datetime
from tqdm import tqdm
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from sklearn import metrics
from itertools import chain

from Pro.models.BiLSTM_CRF.data_processor import Mydataset, get_vocab, get_label_map
from Pro.models.BiLSTM_CRF.model import BiLSTM_CRF
from Pro.models.BiLSTM_CRF.predict import predict_chunk

# 设置torch随机种子
torch.manual_seed(3407)
embedding_size = 128
hidden_dim = 768
epochs = 15
batch_size = 32
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# 建立中文词表，扫描训练集所有字符得到，'PAD'在batch填充时使用，'UNK'用于替换字表以外的新字符
vocab = get_vocab(data_path='datasets/train.json', vocab_path='model/vocab.pkl')
# 标签字典保存，扫描训练集所有字符得到
# 包含开头与结尾
# CLUENER数据集实体类型
n_classes = ['address', 'scene', 'name', 'game', 'organization', 'movie',
             'company', 'position', 'government', 'book']
label_map = get_label_map(label_map_path='datasets/label_map.json', n_classes=n_classes)

train_dataset = Mydataset(dataset='cluener', file_path='datasets/train.json', vocab=vocab, label_map=label_map)
valid_dataset = Mydataset(dataset='cluener', file_path='datasets/dev.json', vocab=vocab, label_map=label_map)
print('训练集长度:', len(train_dataset))
print('验证集长度:', len(valid_dataset))

train_dataloader = DataLoader(train_dataset, batch_size=batch_size, num_workers=0, pin_memory=True, shuffle=True,
                              collate_fn=train_dataset.collect_fn)
valid_dataloader = DataLoader(valid_dataset, batch_size=batch_size, num_workers=0, pin_memory=False, shuffle=False,
                              collate_fn=valid_dataset.collect_fn)
model = BiLSTM_CRF(embedding_size, hidden_dim, train_dataset.vocab, train_dataset.label_map, device).to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)


def train():
    total_start = time.time()
    best_score = 0
    for epoch in range(epochs):
        epoch_start = time.time()
        model.train()
        model.state = 'train'
        for step, (text, label, seq_len) in enumerate(train_dataloader, start=1):
            start = time.time()
            text = text.to(device)
            label = label.to(device)
            seq_len = seq_len.to(device)

            loss = model(text, seq_len, label)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            print(f'Epoch: [{epoch + 1}/{epochs}],'
                  f'  cur_epoch_finished: {step * batch_size / len(train_dataset) * 100:2.2f}%,'
                  f'  loss: {loss.item():2.4f},'
                  f'  cur_step_time: {time.time() - start:2.2f}s,'
                  f'  cur_epoch_remaining_time: {datetime.timedelta(seconds=int((len(train_dataloader) - step) / step * (time.time() - epoch_start)))}',
                  f'  total_remaining_time: {datetime.timedelta(seconds=int((len(train_dataloader) * epochs - (len(train_dataloader) * epoch + step)) / (len(train_dataloader) * epoch + step) * (time.time() - total_start)))}')

        # 每周期验证一次，保存最优参数
        score = evaluate()
        if score > best_score:
            print(f'score increase:{best_score} -> {score}')
            best_score = score
            # saved parameters to model directory
            torch.save(model.state_dict(), 'model/model.bin')
        print(f'current best score: {best_score}')


def evaluate():
    # model.load_state_dict(torch.load('model/model.bin'))
    all_label = []
    all_pred = []
    model.eval()
    model.state = 'eval'
    with torch.no_grad():
        for text, label, seq_len in tqdm(valid_dataloader, desc='eval: '):
            text = text.to(device)
            seq_len = seq_len.to(device)
            batch_tag = model(text, seq_len, label)
            all_label.extend([[train_dataset.label_map_inv[t] for t in l[:seq_len[i]].tolist()] for i, l in enumerate(label)])
            all_pred.extend([[train_dataset.label_map_inv[t] for t in l] for l in batch_tag])

    # need_pred = [(index, sublist)
    #              for index, sublist in enumerate(all_pred)
    #              if any(it != 'O' for it in sublist)]
    # print(f"n: {need_pred}")

    all_label = list(chain.from_iterable(all_label))
    all_pred = list(chain.from_iterable(all_pred))
    sort_labels = [k for k in train_dataset.label_map.keys()]
    # 使用sklearn库得到F1分数
    f1 = metrics.f1_score(all_label, all_pred, average='macro', labels=sort_labels[1:])
    print(f"macro f1: {f1}")

    # print evaluation report
    # ignore O-Object
    # ignore 0.0 warning
    print(metrics.classification_report(
        all_label, all_pred, labels=sort_labels[1:], digits=3, zero_division=0.0
    ))

    return f1


# train with parameter showing above
# train()

# test with valid directly
# evaluate()

# test with single chunk
# text = '“商旅业务是我们今年的重点，我们将加强与香港旅游局等组织的合作，扩大信用卡在港优惠商户的数量和范围。'
# predict_chunk(text)
