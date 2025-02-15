# cluener
import os
import joblib
import sklearn_crfsuite
from sklearn import metrics
from itertools import chain
from Pro.models.load_classes import cluener_process, sent2features, sent2labels

# 数据预处理
train = cluener_process('datasets/train.json')
valid = cluener_process('datasets/dev.json')
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

# “商旅业务是我们今年的重点，我们将加强与香港旅游局等组织的合作，扩大信用卡在港优惠商户的数量和范围。
print("dev")
print(f"0: {y_dev[0]}")
print("pred")
print(f"0: {y_pred[0]}")


y_dev = list(chain.from_iterable(y_dev))
y_pred = list(chain.from_iterable(y_pred))

# 计算F1分数
print('weighted F1 score:',
      metrics.f1_score(y_dev, y_pred, average='weighted', labels=labels))

print(labels)
# 排好标签顺序输入
sorted_labels = sorted(labels, key=lambda name: (name[1:], name[0]))
print(sorted_labels)
# 打印详细分数报告
# print(metrics.classification_report(
#     y_dev, y_pred, labels=sorted_labels, digits=3, zero_division=0.0
# ))

# 查看CRF模型的转移概率和发射概率
# print('CRF转移概率：', crf_model.transition_features_)
# print('CRF发射概率：', crf_model.state_features_)