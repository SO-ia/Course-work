# visualization.py
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


def plot_time_series(data, title):
    """
    Plot the time series data.
    Args:
        data (pd.Series): The time series data to plot.
        title (str): The title for the plot.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data.values, label='Data')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('MtCO2 per day')
    plt.legend()
    plt.show()


def plot_acf_pacf(series):
    """
    Plot the ACF and PACF for model order selection.
    Args:
        series (pd.Series): The time series data.
    """
    plt.figure(figsize=(12, 6))

    plt.subplot(121)
    plot_acf(series, ax=plt.gca(), lags=50)
    plt.title('ACF')

    plt.subplot(122)
    plot_pacf(series, ax=plt.gca(), lags=50)
    plt.title('PACF')

    plt.show()


# 预测未来
def plot_forecast(forecast, forecast_index, title):
    """
    Plot forecast.
    Args:
        forecast (np.array): Forecast values.
        forecast_index (pd.DatetimeIndex): Index for forecasted values.
        title (str): Title for the plot.
    """
    plt.figure(figsize=(12, 9))
    plt.plot(forecast_index, forecast, label='Forecast', color='red')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('MtCO2 per day')
    plt.legend()
    plt.grid(True)
    plt.show()


# 训练加预测未来
def plot_data_forecast(data, forecast, forecast_index, title):
    """
    Plot forecast.
    Args:
        forecast (np.array): Forecast values.
        forecast_index (pd.DatetimeIndex): Index for forecasted values.
        title (str): Title for the plot.
    """
    plt.figure(figsize=(12, 9))
    plt.plot(data.index, data.values, label='Historical Data', color='blue')
    plt.plot(forecast_index, forecast, label='Forecast', color='red')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('MtCO2 per day')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_test_fore_comparison(test_data, forecast, forecast_index, title="Train vs Test Prediction", figsize=(10, 9)):
    """
    Plot true test data, and forecasted data.

    :param test_data: The test dataset (true values for validation)
    :param forecast: The forecasted values from the ARIMA model
    :param forecast_index: Date index for the forecasted values
    :param title: Title for the plot
    :param figsize: Size of the plot
    """
    plt.figure(figsize=figsize)

    # Plot true test data
    plt.plot(test_data.index, test_data.values, label='True Test Data', color='green', linewidth=2)

    # Plot forecasted data
    plt.plot(forecast_index, forecast, label='Forecasted Data', color='red', linewidth=2)

    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_train_pred_comparison(train_data, predict, predict_index, title="Train vs Test Prediction", figsize=(10, 9)):
    """
    Plot training data, and predicted data.

    :param train_data: The training dataset (train set)
    :param predict: The forecasted values from the ARIMA model
    :param predict_index: Date index for the forecasted values
    :param title: Title for the plot
    :param figsize: Size of the plot
    """
    plt.figure(figsize=figsize)

    # Plot training data
    plt.plot(train_data.index, train_data.values, label='Training Data', linewidth=2)

    # Plot forecasted data
    plt.plot(predict_index, predict, label='predicted Data', linewidth=2)

    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()

