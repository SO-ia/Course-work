import os.path

import numpy as np
from tqdm import tqdm

# HMM模型类
class HMM_model:
    def __init__(self, tag2idx, dataset='weibo'):
        if not os.path.exists(f'../{dataset}/matrix'):
            os.makedirs(f'../{dataset}/matrix')
            print('已自动创建matrix文件夹用于存储HMM矩阵\n')

        self.matrix = f'../{dataset}/matrix'
        self.tag2idx = tag2idx  # 标签到ID的映射字典
        self.n_tag = len(self.tag2idx)  # 标签的总数
        self.n_char = 65535  # 所有字符的Unicode编码数量，包括汉字
        self.epsilon = 1e-100  # 为了防止概率归一化时出现除零错误，设置一个极小值
        self.idx2tag = dict(zip(self.tag2idx.values(), self.tag2idx.keys()))  # ID到标签的映射字典
        self.A = np.zeros((self.n_tag, self.n_tag))  # 状态转移概率矩阵 A, shape: (41, 41)
        self.B = np.zeros((self.n_tag, self.n_char))  # 观测概率矩阵 B, shape: (41, 65535)
        self.pi = np.zeros(self.n_tag)  # 初始隐状态概率 pi, shape: (41,)

    def train(self, train_data):
        print('开始训练数据：')
        for i in tqdm(range(len(train_data))):  # 遍历训练数据
            for j in range(len(train_data[i][0])):  # 遍历每组数据中的每个字符
                cur_char = train_data[i][0][j]  # 当前字符
                cur_tag = train_data[i][1][j]  # 当前标签
                self.B[self.tag2idx[cur_tag]][ord(cur_char)] += 1  # 统计B矩阵，标签->字符的观测次数
                if j == 0:
                    # 如果是该文本段的第一个字符，统计初始隐状态概率pi
                    self.pi[self.tag2idx[cur_tag]] += 1
                    continue
                pre_tag = train_data[i][1][j - 1]  # 记录前一个字符的标签
                self.A[self.tag2idx[pre_tag]][self.tag2idx[cur_tag]] += 1  # 统计A矩阵，前一个标签->当前标签的转移次数

        # 防止数据下溢,对数据进行对数归一化
        self.A[self.A == 0] = self.epsilon
        self.A = np.log(self.A) - np.log(np.sum(self.A, axis=1, keepdims=True))
        self.B[self.B == 0] = self.epsilon
        self.B = np.log(self.B) - np.log(np.sum(self.B, axis=1, keepdims=True))
        self.pi[self.pi == 0] = self.epsilon
        self.pi = np.log(self.pi) - np.log(np.sum(self.pi))

        # 将A，B，pi矩阵保存到本地
        np.savetxt(f'{self.matrix}/A.txt', self.A)
        np.savetxt(f'{self.matrix}/B.txt', self.B)
        np.savetxt(f'{self.matrix}/pi.txt', self.pi)
        print('训练完毕！')

    # 载入A，B，pi矩阵参数
    def load_paramters(self):
        self.A = np.loadtxt(f'{self.matrix}/A.txt')
        self.B = np.loadtxt(f'{self.matrix}/B.txt')
        self.pi = np.loadtxt(f'{self.matrix}/pi.txt')

    # 使用维特比算法进行解码
    def viterbi(self, s):
        if not s:  # 如果输入字符串为空，返回空标签列表
            return []

        delta = self.pi + self.B[:, ord(s[0])]  # 初始时刻的delta值
        path = []  # 保存路径
        for i in range(1, len(s)):
            tmp = delta.reshape(-1, 1) + self.A  # 计算每个标签的转移概率
            delta = np.max(tmp, axis=0) + self.B[:, ord(s[i])]  # 计算每个字符的最大概率
            path.append(np.argmax(tmp, axis=0))  # 记录每一时刻的最优路径

        # 回溯得到最优路径
        index = np.argmax(delta)  # 最后一个时刻的标签
        results = [self.idx2tag[index]]  # 结果列表
        while path:
            tmp = path.pop()  # 取出路径中的每一步
            index = tmp[index]  # 回溯到上一时刻的标签
            results.append(self.idx2tag[index])  # 添加到结果中
        results.reverse()  # 因为路径是反向回溯的，所以需要反转
        return results

    # 模型预测函数
    def predict(self, s):
        results = self.viterbi(s)  # 使用维特比算法进行解码
        for i in range(len(s)):
            print(s[i] + results[i], end=' | ')  # 输出字符及其对应的标签

        # print(results)

    # 在验证集上进行评估
    def valid(self, valid_data):
        y_pred = []
        for i in range(len(valid_data)):
            y_pred.append(self.viterbi(valid_data[i][0]))  # 对每条验证数据进行预测
        return y_pred

    # check if matrix has been calculated
    def check_matrix(self, train_data):
        files = [f'{self.matrix}/A.txt', f'{self.matrix}/B.txt', f'{self.matrix}/pi.txt']
        is_found = all(os.path.isfile(file) for file in files)
        # if saved
        if is_found:
            # load it directly
            print('model has been trained already')
            self.load_paramters()
        # if not
        else:
            # calculate it
            print('HMM will be trained')
            self.train(train_data)
