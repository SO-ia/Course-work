import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from week_data_loader import load_data
from stationarity import adf_test, apply_differencing
from visualization import plot_time_series, plot_acf_pacf, plot_forecast, plot_data_forecast, plot_test_fore_comparison, plot_train_pred_comparison
from model_selection import cross_validate_arima
from arima_model import fit_sarimax_model, fit_arima_model, forecast_sarimax, predict_sarimax, evaluate_model

# Initialize the main window
root = tk.Tk()
root.title("SARIMA Forecasting Tool")
root.geometry("600x600")

# Province and sector options
provinces = [
    'Anhui', 'Beijing', 'Chongqing', 'Fujian', 'Gansu', 'Guangdong',
    'Guangxi', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan',
    'Hubei', 'Hunan', 'Inner Mongolia', 'Jiangsu', 'Jiangxi', 'Jilin',
    'Liaoning', 'Ningxia', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanghai',
    'Shanxi', 'Sichuan', 'Tianjin', 'Xinjiang', 'Yunnan', 'Zhejiang'
]

sectors = ['Industry', 'Aviation', 'Residential', 'Power', 'Ground Transport']

# Create labels and dropdowns for province and sector
tk.Label(root, text="Select Province").pack(pady=5)
province_dropdown = ttk.Combobox(root, values=provinces, state="readonly")
province_dropdown.set(provinces[0])  # Default to first province
province_dropdown.pack(pady=5)

tk.Label(root, text="Select Sector").pack(pady=5)
sector_dropdown = ttk.Combobox(root, values=sectors, state="readonly")
sector_dropdown.set(sectors[0])  # Default to first sector
sector_dropdown.pack(pady=5)

# Create input for the forecast steps
tk.Label(root, text="Enter Forecast Steps").pack(pady=5)
forecast_entry = tk.Entry(root)
forecast_entry.pack(pady=5)


# Function to handle forecasting and plotting
def handle_forecast():
    # Step 8: Forecast future values based on input from the text field
    try:
        forecast_steps = int(forecast_entry.get())  # Number of forecast steps entered by the user
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for forecast steps.")
        return

    # Step 1: Load the data
    # Step 2: Get the selected province and sector
    state = province_dropdown.get()
    sector = sector_dropdown.get()
    # Step 3: Subset data based on province and sector
    data_subset = load_data('datasets/weekly_emissions.csv', state, sector)

    # Step 4: Check for stationarity
    is_stationary = adf_test(data_subset['MtCO2 per week'])

    # Step 5: Apply differencing if non-stationary
    if not is_stationary:
        data_subset_diff = apply_differencing(data_subset['MtCO2 per week'], order=1)
        d = 1
    else:
        data_subset_diff = data_subset['MtCO2 per week']
        d = 0

    # Plot ACF and PACF to help with SARIMAX model order selection
    plot_acf_pacf(data_subset_diff)

    # Step 6: Fit the SARIMAX model
    # 在这里设置找最优超参数的范围
    p_range = range(0, 4)
    q_range = range(0, 4)
    # 该函数获取最优超参数
    best_order, best_score = cross_validate_arima(train_data_diff, p_range, d, q_range)
    print(f"Best SARIMA parameters: {best_order} with MSE: {best_score}")

    # 该序列为 Anhui-industry 的最优序列
    # 可在此处人工设置序列
    best_order = (0, 1, 1)
    best_seasonal_order = (1, 0, 0)
    model_fit = fit_sarimax_model(data_subset_diff, best_order, best_seasonal_order)
    # 此处可选择 arima
    # model_fit = fit_arima_model(data_subset_diff, best_order)

    forecast = forecast_sarimax(model_fit, forecast_steps)
    forecast_index = pd.date_range(start=data_subset_diff.index[-1], periods=forecast_steps + 1, freq='D')[1:]

    # show forecast value
    result_label.config(
        text=f"Predict the next {forecast_steps} week(s):\n"
             f"{forecast}"
    )

    plot_time_series(data_subset_diff, title=f"train - {state} - {sector}")
    # Step 9: Plot the forecast
    # 只画预测数据
    plot_forecast(forecast, forecast_index,
                  title=f"Prediction - {state} - {sector} in {forecast_steps} week(s)\n"
                        f"best_order: {best_order}\n"
                        f"best_seasonal_order: {best_seasonal_order}\n"
                  )
    # 接着原始数据画，但有点离谱，就没加了
    # plot_data_forecast(data_subset_diff, forecast, forecast_index,
    #                    title=f"Prediction - {state} - {sector} in {forecast_steps} week(s)\n"
    #                          f"best_order: {best_order}\n"
    #                          f"best_seasonal_order: {best_seasonal_order}\n"
    #                    )


# Button to trigger forecasting
forecast_button = tk.Button(root, text="Generate Forecast", command=handle_forecast)
forecast_button.pack(pady=20)


# Function to handle test set vs training set comparison
def handle_train_test_comparison():
    # Step 1: Load the data
    # Step 2: Get the selected province and sector
    state = province_dropdown.get()
    sector = sector_dropdown.get()
    # Step 3: Subset data based on province and sector
    data_subset = load_data('datasets/weekly_emissions.csv', state, sector)

    # Step 4: Split data into train and test
    train_size = int(len(data_subset) * 0.8)
    train_data, test_data = data_subset[:train_size], data_subset[train_size:]

    # Step 5: Check for stationarity and apply differencing if necessary
    # 检查数据是否平稳
    is_stationary = adf_test(train_data['MtCO2 per week'])
    if not is_stationary:
        # 非平稳：一阶差分去除线性趋势 (不使用二阶或高阶差分)
        train_data_diff = apply_differencing(train_data['MtCO2 per week'], order=1)
        test_data_diff = apply_differencing(test_data['MtCO2 per week'], order=1)
        d = 1
    else:
        # 平稳数据则直接取出排放量
        train_data_diff = train_data['MtCO2 per week']
        test_data_diff = test_data['MtCO2 per week']
        d = 0

    # Plot ACF and PACF to help with SARIMAX model order selection
    plot_acf_pacf(train_data_diff)

    # Step 6: Fit the SARIMAX model
    # 在这里设置找最优超参数的范围
    p_range = range(0, 2)
    q_range = range(0, 2)
    # 该函数获取最优超参数
    best_order, best_score = cross_validate_arima(train_data_diff, p_range, d, q_range)
    print(f"Best SARIMA parameters: {best_order} with MSE: {best_score}")

    # ======================================================================================
    # 该序列为 Anhui-industry 和 Beijing-industry 的最优序列
    best_order = (0, 1, 1)
    best_seasonal_order = (1, 0, 0)
    model_fit = fit_sarimax_model(train_data_diff, best_order, best_seasonal_order)
    # 此处可选择 arima
    # model_fit = fit_arima_model(data_subset_diff, best_order)

    # Step 7: Forecast on the training set
    # 预测训练集
    predict_steps = len(train_data)
    predict = predict_sarimax(model_fit, predict_steps)
    predict_index = train_data.index
    # print(f"train_data['MtCO2 per week']: {train_data['MtCO2 per week']}")
    # # print(f"test_data['MtCO2 per week']: {test_data['MtCO2 per week']}")
    # print(f"forecast: {predict}")

    # Step 8: Forecast on the test set
    # 预测测试集
    forecast_steps = len(test_data)
    forecast = forecast_sarimax(model_fit, forecast_steps)
    forecast_index = test_data.index
    # print(f"train_data['MtCO2 per week']: {train_data['MtCO2 per week']}")
    # print(f"test_data['MtCO2 per week']: {test_data['MtCO2 per week']}")
    # print(f"forecast: {forecast}")

    # evaluation
    # 4项评估指标 mse, rmse, mae 和 mape，改完后都可以正常使用
    print("========== over ==========")
    mse, rmse, mae, mape = evaluate_model(test_data_diff, forecast)
    result_label.config(
        text=f"Predicted Carbon Emission for test set:\n{forecast.head()}\n\n"
             f"Model Evaluation:\nMSE: {mse}\nRMSE: {rmse}\nMAE: {mae}\nMAPE: {mape:.8f}"
    )

    plot_time_series(train_data_diff, title=f"train - {state} - {sector}")

    # Step 9: Plot the comparison between training data predict
    # 可视化训练集与预测值对比
    plot_train_pred_comparison(train_data_diff, predict, predict_index,
                               title=f"Training vs Prediction - {state} - {sector}\n"
                                     f"best_order: {best_order}\n"
                                     f"best_seasonal_order: {best_seasonal_order}\n"
                               )
    # Step 10: Plot the comparison between test data and forecast
    # 可视化测试集与预测值对比
    plot_test_fore_comparison(test_data_diff, forecast, forecast_index,
                              title=f"Testing vs Prediction - {state} - {sector}\n"
                                    f"best_order: {best_order}\n"
                                    f"best_seasonal_order: {best_seasonal_order}\n"
                              )


# Button to generate train-test comparison chart
comparison_button = tk.Button(root, text="Generate Train-Test Comparison", command=handle_train_test_comparison)
comparison_button.pack(pady=20)

# Result label
result_label = tk.Label(root, text="Prediction results")
result_label.pack()

# Start the Tkinter main loop
root.mainloop()
