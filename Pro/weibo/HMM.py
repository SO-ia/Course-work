from itertools import chain
from Pro.models.HMM import HMM_model
from Pro.models.load_classes import load_tag2idx, data_process
from sklearn import metrics


# 微博数据集实体类型
n_classes = ['LOC.NAM', 'LOC.NOM', 'PER.NAM', 'ORG.NOM', 'ORG.NAM', 'GPE.NAM', 'PER.NOM']
tag2idx = load_tag2idx(n_classes)

# 数据处理，加载训练集和验证集
train_data = data_process('datasets/train.json')
valid_data = data_process('datasets/dev.json')

print('训练集长度:', len(train_data))
print('验证集长度:', len(valid_data))

# 初始化HMM模型并训练
model = HMM_model(tag2idx, dataset='weibo')
# 首次运行时直接训练模型
model.check_matrix(train_data)
"""
    否则直接加载训练得到的参数矩阵
    3 matrix:
    1. A shape: (29, 29) --- (tag, tag)
    2. B shape: (29, 65535) --- (tag, char)
    3. pi shape: (29, ) --- (tag, )
"""
model.load_paramters()

# 测试模型
model.predict('老百姓心新乡新闻网话说这几天新乡天气还好吧偷笑')
print()

# 验证集预测和评估
y_pred = model.valid(valid_data)
# 获取验证集中的真实标签
y_true = [data[1] for data in valid_data]

# 打印详细的分类评估报告
sort_labels = [k for k in tag2idx.keys()]
y_pred = list(chain.from_iterable(y_pred))  # 将y_pred扁平化
y_true = list(chain.from_iterable(y_true))  # 将y_true扁平化

# 打印分类报告，忽略'O'标签
print(metrics.classification_report(
    y_true, y_pred, labels=sort_labels[1:], digits=3, zero_division=0.0
))
