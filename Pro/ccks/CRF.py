# ccks
import os
import joblib
import sklearn_crfsuite
from sklearn import metrics
from itertools import chain
from Pro.models.load_classes import data_process, sent2features, sent2labels

# 数据预处理
train = data_process('datasets/train.json')
valid = data_process('datasets/dev.json')
print('训练集长度:', len(train))
print('验证集长度:', len(valid))
X_train = [sent2features(s[0]) for s in train]
y_train = [sent2labels(s[1]) for s in train]
X_dev = [sent2features(s[0]) for s in valid]
y_dev = [sent2labels(s[1]) for s in valid]
print(X_train[0][1])


# 初始化CRF模型
crf_model = sklearn_crfsuite.CRF(algorithm='lbfgs', c1=0.1, c2=0.1, max_iterations=50,
                                 all_possible_transitions=True, verbose=True)

# 定义模型保存路径
model_dir = 'model'
model_file = os.path.join(model_dir, 'crf_model.pkl')

# 如果模型目录不存在则创建
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# 检查模型文件是否已存在
if os.path.isfile(model_file):
    try:
        # 如果模型文件已存在，直接加载模型
        crf_model = joblib.load(model_file)
        print("已加载现有的模型！")
    except Exception as e:
        print(f"加载模型时出错: {e}")
else:
    # 训练并保存模型
    try:
        crf_model.fit(X_train, y_train)
        joblib.dump(crf_model, model_file)  # 保存模型
        print("模型训练并保存成功！")
    except Exception as e:
        print(f"训练模型时出错: {e}")


labels = list(crf_model.classes_)
# 移除'O'标签
labels.remove("O")
y_pred = crf_model.predict(X_dev)

# "入院前11年患者于受凉后出现咳嗽、胸闷，伴咳痰，咳嗽呈阵发性发作,咳出白色粘痰，伴喘息、气急，到**某家医院就诊，诊断为“支气管哮喘、慢性支气管炎”，给予抗感染、平喘等对症支持治疗后好转。之后下述症状反复发作，以受凉及春冬季发作较频繁。入院前1年前受凉后再次于我科住院治疗，考虑诊断“1、慢性阻塞性肺病急性发作期 肺源性心脏病 2、慢性胃炎 3、贫血 4、肺结核？”，经抗感染、平喘、止咳化痰、抑酸等治疗后好转，院外长期低流量吸氧。入院前5天前患者受凉后出现下述症状加重，偶有黄白粘痰，量少，不易咳出，伴喘累，伴纳差，无畏寒、寒战，无潮热、盗汗、消瘦，无咯血，无腹痛、腹胀，无头昏、头痛，无尿痛、肉眼血尿，无皮上出血等不适。于今日来我院就诊，为进一步治疗，门诊以\"慢性支气管炎急性发作 \"收入我科住院治疗。自患病以来，患者食欲差，精神、睡眠欠佳，大小便正常，体重无明显上降。"
# print("dev")
# print(f"0: {y_dev[0]}")
# print("pred")
# print(f"0: {y_pred[0]}")


y_dev = list(chain.from_iterable(y_dev))
y_pred = list(chain.from_iterable(y_pred))

# 计算F1分数
print('weighted F1 score:',
      metrics.f1_score(y_dev, y_pred, average='weighted', labels=labels, zero_division=0.0))

# 排好标签顺序输入
sorted_labels = sorted(labels, key=lambda name: (name[1:], name[0]))
# 打印详细分数报告
print(metrics.classification_report(
    y_dev, y_pred, labels=sorted_labels, digits=3, zero_division=0.0
))

# 查看CRF模型的转移概率和发射概率
# print('CRF转移概率：', crf_model.transition_features_)
# print('CRF发射概率：', crf_model.state_features_)