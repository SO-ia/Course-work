# Requirements

```python
joblib==1.4.2
numpy==1.24.3
scikit_learn==1.5.2
sklearn_crfsuite==0.5.0
torch==2.5.0+cpu
tqdm==4.67.1
```





# Files structure

```powershell
  Pro						# 项目总文件夹
    │  requirements.txt				# 依赖安装
    │
    │
    ├─ccks						# ccks数据集运行、模型及结果文件夹
    │  │  BILSTM+CRF.py					# BILSTM+CRF基线模型运行文件
    │  │  CRF.py					# CRF基线模型运行文件
    │  │  HMM.py					# HMM+viterbi模型运行文件
    │  │
    │  ├─datasets					# ccks数据集运行、模型及结果文件夹
    │  │      ccks2019_task1.json			# ccks数据集源文件
    │  │      dev.json					# ccks验证集
    │  │      label_map.json				# 标签、下标字典 -- BILSTM+CRF
    │  │      train.json				# ccks训练集
    │  │
    │  ├─matrix						# HMM矩阵文件夹
    │  │      A.txt					# 状态转移矩阵
    │  │      B.txt					# 发射概率矩阵
    │  │      pi.txt					# 初始概率矩阵
    │  │
    │  └─model						# 模型参数文件夹
    │          crf_model.pkl				# CRF
    │          model.bin				# BILSTM+CRF
    │          vocab.pkl				# 中文词表 -- BILSTM+CRF
    │
    │
    ├─cluener
    ├─weibo
    ├─每个数据集文件结构一致
    │
    │
    └─models						# 模型文件夹
       │  HMM.py					# HMM类
       │  load_classes.py				# 数据加载文件
       │
       └─BiLSTM_CRF					# BILSTM+CRF模型文件夹
             data_processor.py				# BILSTM+CRF数据加载文件
             model.py					# BILSTM+CRF类
             predict.py					# BILSTM+CRF预测文件
         


```





# Quick Start

- 每类数据集的操作相同
- 确保 `{dataset_name}/datasets` 路径下存在训练集`train.json` 和 验证集`dev.json`

## HMM

1.  `python HMM.py`
2. 生成 `matrix` 文件夹保存HMM所需矩阵
3. 控制台输出验证集得分结果与单句预测结果



## CRF

1.  `python CRF.py`
2. 生成 `model` 文件夹保存模型参数为 `crf_model.pkl` 文件
3. 控制台输出验证集得分结果



## BILSTM+CRF

### 训练

1.  `BILSTM+CRF.py` 中 `train()` 行未注释
2. 运行 `BILSTM+CRF.py`
   可设置 `epochs, batch_size` 等参数
3. 生成 `model` 文件夹保存模型参数为 `model.bin` 文件

### 验证集测试

1. 取消注释 `BILSTM+CRF.py` 中以下代码

   ```python
   # test with valid directly
   evaluate()
   
   def evaluate():
       model.load_state_dict(torch.load('model/model.bin'))
       ...
   ```

2. 运行 `BILSTM+CRF.py`

3. 控制台输出验证集得分结果

### 单句测试

1. 取消注释 `BILSTM+CRF.py` 中以下代码

   ```python
   # test with single chunk
   text = '老百姓心新乡新闻网话说这几天新乡天气还好吧偷笑'
   predict_chunk(text, dataset='weibo')
   ```

2. 运行 `BILSTM+CRF.py`

3. 控制台输出单句预测结果
