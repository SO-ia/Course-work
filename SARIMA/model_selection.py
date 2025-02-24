# model_selection.py
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX


def evaluate_arima(train, test, order):
    """
    Evaluate an ARIMA/SARIMAX model using cross-validation.
    Args:
        train (pd.Series): The time series data.
        order (tuple): The (p, d, q) order for ARIMA/SARIMAX.
    Returns:
        float: Mean squared error of the model's forecast.
    """

    seasonal_order = order + (52,)
    model = SARIMAX(train, order=order, seasonal_order=seasonal_order)
    # model = ARIMA(train, order=order)
    model_fit = model.fit()
    predictions = model_fit.forecast(steps=len(test))
    mse = mean_squared_error(test, predictions)
    return mse


def cross_validate_arima(data, p_range, d, q_range):
    """
    Perform a grid search using cross-validation to find the best ARIMA/SARIMAX parameters.
    Args:
        data (pd.Series): The time series data.
        p_range (range): Range of p values to search.
        d: if stable 数据是否平稳
        q_range (range): Range of q values to search.
    Returns:
        tuple: Best (p, d, q) parameters and the corresponding MSE.
    """
    best_score, best_order = float("inf"), None
    tscv = TimeSeriesSplit(n_splits=5)

    for p in p_range:
        for q in q_range:
            order = (p, d, q)
            fold_mse = []  # Store the MSE for each fold

            # 使用 5 折交叉验证查找最优参数
            # Perform cross-validation on the time series data
            for train_idx, test_idx in tscv.split(data):
                train, test = data.iloc[train_idx], data.iloc[test_idx]
                mse = evaluate_arima(train, test, order)
                fold_mse.append(mse)

            # mse = evaluate_arima(data, order)
            # Calculate the average MSE across all splits for this (p, d, q)
            avg_mse = np.mean(fold_mse)
            print(f"SARIMAX{order} - MSE: {avg_mse}")
            # print(f"ARIMA{order} - MSE: {mse}")
            if avg_mse < best_score:
                best_score, best_order = avg_mse, order

    return best_order, best_score
