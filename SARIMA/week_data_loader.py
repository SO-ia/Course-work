# week_data_loader.py
import pandas as pd


def load_data(file_path, state, sector):
    """
    Load the processed carbon emission data from a CSV file.
    Args:
        file_path (str): Path to the CSV file.
        state, sector: 指定省份与行业
    Returns:
        pd.DataFrame: Processed carbon emission data.
    """
    data = pd.read_csv(file_path)
    # data['date'] = pd.to_datetime(data['date'])

    # 提取 week 列中的开始日期部分（week 列格式为 "2020-01-20/2020-01-26"）
    data['week_start'] = data['week'].str.split('/').str[0]
    data['date'] = pd.to_datetime(data['week_start'], format='%Y-%m-%d')
    data.set_index('date', inplace=True)

    data = subset_data(data, state, sector)

    return data


def subset_data(data, state, sector):
    """
    Filter data for a specific state and sector.
    Args:
        data (pd.DataFrame): The full dataset.
        state (str): The state to filter.
        sector (str): The sector to filter.
    Returns:
        pd.DataFrame: The filtered data for the specified state and sector.
    """
    return data[(data['state'] == state) & (data['sector'] == sector)]
