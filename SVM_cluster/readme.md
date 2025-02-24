# 环境配置

```python
pip install -r requirements.txt
```

### requirements内容如下

```python
matplotlib==3.8.4
numpy==2.0.2
pandas==2.2.3
scikit_learn==1.4.2
seaborn==0.13.2
```



# 文件说明

## SVM_cluster

存放项目主要运行文件与数据集文件

`001` — `adult`

`002` — `winequality-red`

`003` — `winequality-white`



### `dataset`

存放数据集文件 `(adult.csv, winequality-white.csv, winequality-red.csv, filtered_winequality-white.csv)`

`filtered_winequality-white.csv`: 通过 `feature_selection.py` 对 `winequality-white.csv` 进行特征选择后的数据集



### `images`

用于存放生成结果可视化的图片文件，若不存在可自动创建



### `SVM_class`

自定义 `SVM` 模型

`svm_binary_model.py`: 二分类模型

`svm_multi_model.py`: 多分类模型

`svm_kernels.py`: 核函数计算 (最终由于自主计算过慢，使用了 `sklearn.metrics.pairwise` 的 `
pairwise_kernels` 库实现)

`utils.py`: 判断实际标签与预测标签是否相同



### `requirements.txt`

环境依赖配置文件



## 运行文件

`001_process.py`: 通过自定义的二分类模型，随机选取 `adult.csv` 的 6000 条数据进行测试与训练

`001_process_sklearn.py`: 调用 `sklearn` 内的 `SVM` 模型，并以完整的 `adult.csv` 进行测试与训练

`002_process.py`: 通过自定义的多分类模型，对 `winequality-red.csv` 进行测试与训练

`003_process.py`: 通过自定义的多分类模型，对 `filtered_winequality-white.csv` 进行测试与训练





## 数据预处理文件

`data_loader.py`: 读取数据集，清洗数据，选取数据，划分训练集与测试集等操作

`feature_selection.py`: 对 `winequality-white.csv` 进行特征选择生成`filtered_winequality-white.csv` 文件



## 可视化文件

`visualization_adult.py`: 可视化 `001_process.py` 与 `001_process_sklearn.py` 的分类结果

`visualization_red.py`: 可视化 `002_process.py` 的分类结果

`visualization_white.py`: 可视化 `003_process.py` 的分类结果

