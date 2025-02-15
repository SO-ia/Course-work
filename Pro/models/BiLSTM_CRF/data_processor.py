import os
import json
import pickle
import torch
from torch.utils.data import Dataset
from Pro.models.load_classes import data_process, load_tag2idx, cluener_process


def get_label_map(label_map_path='', n_classes=None):
    if n_classes is None:
        n_classes = ['']
    # label_map_path: 标签字典保存路径
    # 第一次运行需要遍历训练集获取到标签字典，并存储成json文件保存，第二次运行即可直接载入json文件
    if os.path.exists(label_map_path):
        with open(label_map_path, 'r', encoding='utf-8') as fp:
            label_map = json.load(fp)
    else:
        # n_classes: ['address', 'book', 'company', 'game', 'government', 'movie', 'name', 'organization', 'position', 'scene']
        # 设计label_map字典，对每个标签设计两种，如B-name、I-name，并设置其ID值
        label_map = load_tag2idx(n_classes)
        # 对于BiLSTM+CRF网络，需要增加开始和结束标签，以增强其标签约束能力
        START_TAG = "<START>"
        STOP_TAG = "<STOP>"
        label_map[START_TAG] = len(label_map)
        label_map[STOP_TAG] = len(label_map)

        # 将label_map字典存储成json文件
        with open(label_map_path, 'w', encoding='utf-8') as fp:
            json.dump(label_map, fp, indent=4)

    # {0: 'B-address', 1: 'I-address', 2: 'B-book', 3: 'I-book'...}
    label_map_inv = {v: k for k, v in label_map.items()}
    return label_map, label_map_inv


def get_vocab(data_path='', vocab_path=''):
    # 词表保存路径
    # 第一次运行需要遍历训练集获取到标签字典，并存储成pkl文件保存，第二次运行即可直接载入pkl文件
    if os.path.exists(vocab_path):
        with open(vocab_path, 'rb') as fp:
            vocab = pickle.load(fp)
    else:
        json_data = []
        # 加载数据集
        with open(data_path, 'r', encoding='utf-8') as fp:
            for line in fp:
                json_data.append(json.loads(line))
        # 建立词表字典，提前加入'PAD'和'UNK'
        # 'PAD'：在一个batch中不同长度的序列用该字符补齐
        # 'UNK'：当验证集或测试集出现词表以外的词时，用该字符代替
        vocab = {'PAD': 0, 'UNK': 1}
        # 遍历数据集，不重复取出所有字符，并记录索引
        for data in json_data:
            text = data.get('text', '')  # 获取文本，如果不存在则设为空字符串
            if not text.strip():  # 跳过空文本
                continue

            for word in text:
                if word not in vocab:
                    vocab[word] = len(vocab)
        # vocab：{'PAD': 0, 'UNK': 1, '浙': 2, '商': 3, '银': 4, '行': 5...}
        # 保存成pkl文件
        with open(vocab_path, 'wb') as fp:
            pickle.dump(vocab, fp)

    # 翻转字表，预测时输出的序列为索引，方便转换成中文汉字
    # vocab_inv：{0: 'PAD', 1: 'UNK', 2: '浙', 3: '商', 4: '银', 5: '行'...}
    vocab_inv = {v: k for k, v in vocab.items()}
    return vocab, vocab_inv


class Mydataset(Dataset):
    def __init__(self, file_path, vocab, label_map, dataset=''):
        self.file_path = file_path
        # 数据预处理
        if dataset == 'cluener':
            self.data = cluener_process(self.file_path)
        else:
            self.data = data_process(self.file_path)
        self.label_map, self.label_map_inv = label_map
        self.vocab, self.vocab_inv = vocab
        # self.data为中文汉字和英文标签，将其转化为索引形式
        self.examples = []
        for text, label in self.data:
            t = [self.vocab.get(t, self.vocab['UNK']) for t in text]
            l = [self.label_map[l] for l in label]
            self.examples.append([t, l])

    def __getitem__(self, item):
        return self.examples[item]

    def __len__(self):
        return len(self.data)

    def collect_fn(self, batch):
        # 取出一个batch中的文本和标签，将其单独放到变量中处理
        # 长度为batch_size，每个序列长度为原始长度
        text = [t for t, l in batch]
        label = [l for t, l in batch]
        # 获取一个batch内所有序列的长度，长度为batch_size
        seq_len = [len(i) for i in text]
        # 提取出最大长度用于填充
        max_len = max(seq_len)

        # 填充到最大长度，文本用'PAD'补齐，标签用'O'补齐
        text = [t + [self.vocab['PAD']] * (max_len - len(t)) for t in text]
        label = [l + [self.label_map['O']] * (max_len - len(l)) for l in label]

        # 将其转化成tensor，再输入到模型中，这里的dtype必须是long否则报错
        # text 和 label shape：(batch_size, max_len)
        # seq_len shape：(batch_size,)
        text = torch.tensor(text, dtype=torch.long)
        label = torch.tensor(label, dtype=torch.long)
        seq_len = torch.tensor(seq_len, dtype=torch.long)

        return text, label, seq_len
