# arima_model.py
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error


# 季节性模型 SARIMAX
def fit_sarimax_model(data, order, seasonal_order):
    """
    Fit an ARIMA model with the given order.
    Args:
        data (pd.Series): The time series data.
        order (tuple): The (p, d, q) order for ARIMA.
        seasonal_order (tuple): (P, D, Q, T), 其中 T 为周期，本模型设周期为 52
    Returns:
        ARIMAResults: Fitted ARIMA model.
    """
    print("training with SARIMA...")
    seasonal_order = seasonal_order + (52,)
    # 实际为 SARIMA 模型，无外界因素X
    model = SARIMAX(data, order=order, seasonal_order=seasonal_order)
    model_fit = model.fit()
    return model_fit


# 非季节性模型 ARIMA
def fit_arima_model(data, order):
    """
    Fit an ARIMA model with the given order.
    Args:
        data (pd.Series): The time series data.
        order (tuple): The (p, d, q) order for ARIMA.
    Returns:
        ARIMAResults: Fitted ARIMA model.
    """
    print("training with ARIMA...")
    model = ARIMA(data, order=order)
    model_fit = model.fit()
    return model_fit


# 测试集与未来预测
def forecast_sarimax(model_fit, steps):
    """
    Generate forecast from a fitted SARIMAX model.
    Args:
        model_fit (ARIMAResults): Fitted ARIMA model.
        steps (int): Number of periods to forecast.
    Returns:
        np.array: Forecasted values.
    """
    print("forecasting...")
    forecast = model_fit.forecast(steps=steps)
    return forecast


# 训练集预测
def predict_sarimax(model_fit, steps):
    """
    Generate forecast from a fitted SARIMAX model.
    Args:
        model_fit (ARIMAResults): Fitted ARIMA model.
        steps (int): Number of periods to forecast.
    Returns:
        np.array: Forecasted values.
    """
    print("predicting...")
    predict = model_fit.predict(steps=steps)
    return predict



# 评估指标计算
def evaluate_model(test_true, forecast):
    """
    Evaluate the performance of the model using MSE, RMSE, and MAE.
    """
    # Forecast the training data itself to evaluate performance

    # Calculate performance metrics
    mse = mean_squared_error(test_true, forecast)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(test_true, forecast)
    mape = np.mean(np.abs((test_true - forecast) / test_true)) * 100

    # Print out the evaluation metrics
    # print(f'Mean Squared Error (MSE): {mse}')
    # print(f'Root Mean Squared Error (RMSE): {rmse}')
    # print(f'Mean Absolute Error (MAE): {mae}')

    # Return metrics for further use
    return mse, rmse, mae, mape