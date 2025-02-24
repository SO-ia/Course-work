## requirements

```python
statsmodels
sklearn
tkinter
pandas
matplotlib
```



## Quick Start

1. 将所有文件放在任意命名的同一个文件夹下

2. 确保所有 `requirements` 内包含的库安装完成

3. 运行 `preprocess.py` 以确保 `datasets ` 文件夹下下有 `weekly_emissions.csv`  文件

4. 运行 `app_week.py`，弹出以下界面

   `Generate Forecast`: 选择 province 和 sector，输入预测周长，点击 `Generate Forecast` 开始预测未来数据，可生成预测结果图，并在 predict results 下方显示预测数值结果

   `Generate Train-Test Forecast`: 选择 province 和 sector，点击 `Generate Train-Test Forecast`开始预测测试集，可生成测试集预测结果图，并在 predict results 下方显示前5周预测数值结果与评测结果

   <img src=".\readme-image\interface.png" alt="interface" style="zoom:38%;" />

   

   > 如果需要提高运行速度，需修改 `arima_model.py` ， `model_selection.py` 和 `app_week.py` 将 SARIMA 修改为 ARIMA，具体见下文文件说明的对应文件说明, 但预测效果很差

   `ARIMA`: 每个省份的每个领域的 ARIMA 模型训练找最优 order 大概需要 15 分钟左右，可通过`app_week.py` 手动调整参数与查找范围
   `SARIMA`: SARIMA 模型训练找最优 order 与 seasonal_order, 时长不明，每个省份的每个行业对应训练时长都不小于40分钟，可通过`app_week.py` 手动调整参数 (`best_order` 与 `best_seasonal_order`) 或查找范围





## 文件说明

### datasets

数据集放在该文件夹下

1. `carbon.csv`: 原始数据集

2. `processed_csv`: (preprocess.py中可选择生成) 预处理 (清洗、平滑、标准化和异常值去除) 后的数据集

3. `weekly_emissions.csv`: 包含按省份、产业和周分组的每周碳排放量数据

   特征列名: state,sector,week,MtCO2 per week



### 数据处理

#### preprocess.py

`preprocess_dataset`

数据预处理：清洗、平滑、标准化、去除异常值

1. 填补缺失值
2. 平滑处理，指定的滚动窗口大小 (默认 7 天) 计算平滑值, 减少噪音
3. 对平滑后的数据标准化，使其适应后续分析
4. 截断法去除离群值，保证数据在合理范围内
5. (可选) 将所有处理后的数据保存到 `processed_csv` 中

`generate_weekly_emissions`

生成每周的碳排放量，并输出到 `weekly_emissions.csv`



#### week_data_loader.py

1. `load_data`: 加载数据为 `DataFrame`
2. `subset_data`: 单变量模型需要选择特征值



### 模型构建

#### arima_model.py

调包完成: **季节性模型 (SARIMA) ** (周期设定为52)

1. `fit_sarimax_model`: 训练 SARIMA
2. `fit_arima_model`: 训练 ARIMA
3. `forecast_arima`: 预测训练集或未来
4. `predict_arima`: 预测训练集

> 可以选择 `fit_arima_model` 函数，修改为 ARIMA 模型



#### model_selection.py

通过5折交叉验证寻找最佳的 SARIMA 模型参数 `(p, d, q)`，并评估该模型的预测性能。

1. `evaluate_arima` : 评估给定 SARIMA 模型的表现，返回模型的均方误差 (MSE) 
2. `cross_validate_arima`: 使用交叉验证方法并通过网格搜索来选择最佳的 SARIMA 模型参数 `(p, d, q)`

> 可以注释 SARIMA 行，修改为 ARIMA 模型
>



#### stationarity.py

检测时间序列数据的平稳性 (stationarity) 并通过差分处理 (differencing) 将其转化为平稳序列

1. `adf_test`: 执行 Augmented Dickey-Fuller (ADF) 检验
2. `apply_differencing`: 差分处理将非平稳序列转换为平稳序列



### 运行文件

#### visualization.py

所有绘图都基于用户选定的 province 和 sector 参数, 可显示最优超参序列

1. `plot_time_series` : 绘制整个训练集的碳排放的时间序列图
2. `plot_acf_pacf`: 绘制时间序列的自相关函数 (ACF) 和偏自相关函数 (PACF)
3. `plot_forecast`: 绘制预测值曲线图
4. `plot_data_forecast`: 绘制原数据后的预测值曲线图
5. `plot_test_fore_comparison`: 绘制测试集真实值与预测值
6. `plot_train_pred_comparison`: 绘制训练集真实值与预测值



#### app_week.py: 

1. 界面设置

   - 省份 (provinces): 中国30个省份选择列表

   - 行业 (sectors): 行业选择 `['Industry', 'Aviation', 'Residential', 'Power', 'Ground Transport']`

   - 输入框 (Entry): 预测**周**数

   - Generate Forecast: 未来碳排放预测

   - Generate Train-Test Comparison: 训练集与测试集预测对比

     

2. `handle_forecast`: 预测未来数据

   - 加载数据

     根据 province 和 sector 从 CSV 文件中加载数据

   - 平稳性检验

     ADF (Augmented Dickey-Fuller) 检验 **已有数据** (由于是预测未来，因此将当前所有的数据都作为训练集) 时间序列平稳性

     平稳则设定 d=0; 非平稳则进行一阶差分 (apply_differencing) 处理, 并设定 d=1

   - ACF 和 PACF 图

     绘制当前省份与行业的数据集 ACF 和 PACF 图，帮助选择适当的 SARIMA 模型参数

   - SARIMA 参数选择

     交叉验证 (cross_validate_arima) 来选择最优的 SARIMA 模型参数 (p, d, q) 和 (P, D, Q)

   - SARIMA 模型拟合

     使用选定的模型参数拟合数据 (fit_sarimax_model) 

     > 可以注释 SARIMA 行，修改为 ARIMA 模型

   - 预测

     根据预测步长对未来的值进行预测 (forecast_sarimax) 

   - 绘制预测图

     当前省份与行业的碳排放未来预测可视化曲线图 (plot_forecast) 

3. `handle_train_test_comparison`: 预测训练集与测试集数据

   - 加载数据

     根据 province 和 sector 从 CSV 文件中加载数据

   - 数据集拆分

     将数据拆分为训练集 (80%) 和测试集 (20%) 

   - 平稳性检验

     ADF (Augmented Dickey-Fuller) 检验 **训练集** 时间序列平稳性

     平稳则设定 d=0; 非平稳则进行一阶差分 (apply_differencing) 处理, 并设定 d=1

   - ACF 和 PACF 图

     绘制当前省份与行业的数据集 ACF 和 PACF 图，帮助选择适当的 SARIMA 模型参数

   - SARIMA 模型参数

     交叉验证 (cross_validate_arima) 来选择最优的 SARIMA 模型参数 (p, d, q) 和 (P, D, Q)

   - SARIMA 模型拟合

     使用训练集数据和选择的 SARIMA 模型参数进行拟合

     > 可以注释 SARIMA 行，修改为 ARIMA 模型

   - 训练集预测

     对训练集进行预测 (predict_sarimax) ，并绘制当前省份与行业的训练集与预测值的对比图 (plot_train_pred_comparison) 

   - 测试集预测

     对测试集进行预测 (forecast_sarimax)，并绘制当前省份与行业的测试集与预测值的对比图 (plot_test_fore_comparison) 



### ARIMA 完整版本

#### ARIMA

`ARIMA.ipynb`

存放本实验模型的的第一个版本使用 ARIMA 模型，包含具体项目说明与运行结果。

