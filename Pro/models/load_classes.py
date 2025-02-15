import json
from collections import defaultdict

'''
    该NER任务使用 BIESO 五位标注法，即:
    B-begin：代表实体开头
    I-inside：代表实体内部
    E-end：代表实体结尾
    S-single：代表单个字符实体
    O-outside：代表不属于任何实体

    其后面接实体类型，如'B-name','I-company'
'''


def load_tag2idx(n_classes):
    '''
        tag2idx字典
        键: 标签名称
        值: 标签序号
    '''
    # 设计tag2idx字典，对每个标签设计4种，如B-name、I-name，并设置其ID值
    tag2idx = defaultdict()
    tag2idx['O'] = 0
    count = 1
    for n_class in n_classes:
        tag2idx['B-' + n_class] = count
        count += 1
        tag2idx['I-' + n_class] = count
        count += 1
        tag2idx['E-' + n_class] = count
        count += 1
        tag2idx['S-' + n_class] = count
        count += 1

    return tag2idx


'''
    数据处理函数：将JSON数据转换为适合HMM训练的数据格式
    data_process: 尾下标需-1 (weibo, ccks)
    cluener_process: 开头结尾即字符下标 (cluener)
'''


def data_process(path):
    json_data = []
    # 读取JSON文件中的数据
    with open(path, 'r', encoding='utf-8') as fp:
        for line in fp:
            json_data.append(json.loads(line))

    data = []
    for entry in json_data:
        text = entry.get('text', '')  # 获取文本，如果不存在则设为空字符串
        if not text.strip():  # 跳过空文本
            continue

        label = ['O'] * len(text)  # 初始化标签列表，默认标签为'O'
        # 遍历实体信息，根据实体的起始和结束位置进行标签标注
        for entity in entry.get('entities', []):  # 确保 entities 存在
            start_idx = entity['start_idx']
            # 某些数据集的结尾标注需要-1
            end_idx = entity['end_idx'] - 1
            entity_label = entity['entity_label']
            if start_idx == end_idx:
                label[start_idx] = 'S-' + entity_label
            else:
                # 起始位置标记为'B-实体类型'
                label[start_idx] = 'B-' + entity_label
                # 中间位置标记为'I-实体类型'
                label[start_idx + 1:end_idx] = ['I-' + entity_label] * (end_idx - start_idx - 1)
                # 结束位置标记为'E-实体类型'
                label[end_idx] = 'E-' + entity_label

        # 将文本和标签编成一个列表添加到返回数据中
        data.append([list(text), label])
    return data


def cluener_process(path):
    json_data = []
    # 读取JSON文件中的数据
    with open(path, 'r', encoding='utf-8') as fp:
        for line in fp:
            json_data.append(json.loads(line))

    data = []
    for entry in json_data:
        text = entry.get('text', '')  # 获取文本，如果不存在则设为空字符串
        if not text.strip():  # 跳过空文本
            continue

        label = ['O'] * len(text)  # 初始化标签列表，默认标签为'O'
        # 遍历实体信息，根据实体的起始和结束位置进行标签标注
        for entity in entry.get('entities', []):  # 确保 entities 存在
            start_idx = entity['start_idx']
            end_idx = entity['end_idx']
            entity_label = entity['entity_label']
            if start_idx == end_idx:
                label[start_idx] = 'S-' + entity_label
            else:
                # 起始位置标记为'B-实体类型'
                label[start_idx] = 'B-' + entity_label
                # 中间位置标记为'I-实体类型'
                label[start_idx + 1:end_idx] = ['I-' + entity_label] * (end_idx - start_idx - 1)
                # 结束位置标记为'E-实体类型'
                label[end_idx] = 'E-' + entity_label

        # 将文本和标签编成一个列表添加到返回数据中
        data.append([list(text), label])
    return data


'''
    数据处理函数：将JSON数据转换为适合CRF训练的数据格式
    is_english: 判断字符是否是英文
    word2features: 将文本转换为特征字典
'''


def is_english(c):
    if 97 <= ord(c.lower()) <= 122:
        return True
    else:
        return False

def word2features(sent, i):
    word = sent[i][0]
    features = {
        'bias': 1.0,
        'word': word,
        'word.isdigit()': word.isdigit(),
        'word.is_english()': is_english(word),
    }

    if i > 0:
        word = sent[i - 1][0]
        features.update({
            '-1:word': word,
            '-1:word.isdigit()': word.isdigit(),
            '-1:word.is_english()': is_english(word),
        })
    else:
        features['BOS'] = True

    if i < len(sent) - 1:
        word = sent[i + 1][0]
        features.update({
            '+1:word': word,
            '+1:word.isdigit()': word.isdigit(),
            '+1:word.is_english()': is_english(word),
        })
    else:
        features['EOS'] = True

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for label in sent]
