from itertools import chain
from Pro.models.HMM import HMM_model
from Pro.models.load_classes import load_tag2idx, data_process
from sklearn import metrics


# Yidu-S4K数据集实体类型
n_classes = ['解剖部位', '手术', '疾病和诊断', '药物', '实验室检验', '影像检查']
tag2idx = load_tag2idx(n_classes)

# 数据处理，加载训练集和验证集
train_data = data_process('datasets/train.json')
valid_data = data_process('datasets/dev.json')

print('训练集长度:', len(train_data))
print('验证集长度:', len(valid_data))
print()

# 初始化HMM模型并训练
model = HMM_model(tag2idx, dataset='ccks')
# 首次运行时直接训练模型
model.check_matrix(train_data)
# 否则直接加载训练得到的参数矩阵
"""
    否则直接加载训练得到的参数矩阵
    3 matrix:
    1. A shape: (25, 25) --- (tag, tag)
    2. B shape: (25, 65535) --- (tag, char)
    3. pi shape: (25, ) --- (tag, )
"""
model.load_paramters()

# 测试模型
model.predict(
    "入院前5天患者无明显诱因出现眼黄、尿黄，伴大便不成形，呈黄色糊状便，每日一次。但无黑便、粘液脓血便"
    "、里急后重，无皮肤瘙痒、腹胀、纳差、厌油、恶心、呕吐、呕血、腹痛，无尿频、尿急、尿痛、血尿、腰痛，"
    "无畏寒、发热、心悸、气促、胸闷、胸痛。在外未予诊治。病程中家属发现患者两眼黄染、皮肤黄染较前逐渐加重，"
    "于2017-01-22在***医院就诊，查“肝功示：总胆红素：231umol/L，直接胆红素177.9umol/L，"
    "ALT：923.3U/L，AST：570.4U/L，ALP：236.8u/l，r-GT：177.3U/L。乙肝三对：乙肝表面抗原：27.979，"
    "阳性、乙肝e抗原、乙肝核心抗体阳性。”，今日为进一步就诊，遂来我院要求住院治疗，门诊以“乙型肝炎”收入我科。"
    "病程中精神、饮食可，大便如下述，小便颜色深黄。体重无明显改变。")
print()

# 验证集预测和评估
y_pred = model.valid(valid_data)
# 获取验证集中的真实标签
y_true = [data[1] for data in valid_data]

# 打印详细的分类评估报告
sort_labels = [k for k in tag2idx.keys()]
y_pred = list(chain.from_iterable(y_pred))  # 将y_pred扁平化
y_true = list(chain.from_iterable(y_true))  # 将y_true扁平化

# 打印分类报告
# 忽略'O'标签
# ignore 0 label
print(metrics.classification_report(
    y_true, y_pred, labels=sort_labels[1:], digits=3, zero_division=0.0
))
