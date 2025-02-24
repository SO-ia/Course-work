import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler


# 处理数据的清洗、平滑、标准化和异常值去除等
def preprocess_dataset(data, freq="D", rolling_window=7, clip_factor=5):
    # Convert date column to datetime format
    data['date'] = pd.to_datetime(data['date'])

    # Sort data by state, sector, and date
    data = data.sort_values(by=["state", "sector", "date"]).reset_index(drop=True)

    # Create a list to store processed DataFrames
    processed_list = []

    # Group data by state and sector
    grouped = data.groupby(["state", "sector"])

    for (state, sector), group in grouped:
        # Set date as the index
        group = group.set_index("date")

        # Resample to ensure daily frequency and fill missing dates
        full_date_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq=freq)
        group = group.reindex(full_date_range)
        group.index.name = "date"

        # Handle missing values (interpolation + small constant for zeroes)
        group["MtCO2 per day"] = group["MtCO2 per day"].interpolate(method='linear')
        group["MtCO2 per day"] = group["MtCO2 per day"].replace(0.0, 1e-5)

        # Apply smoothing using a rolling window
        group["Smoothed_MtCO2"] = group["MtCO2 per day"].rolling(window=rolling_window, min_periods=1).mean()

        # Standardize the smoothed data (robust scaling)
        scaler = RobustScaler()
        group["Standardized_MtCO2"] = scaler.fit_transform(group[["Smoothed_MtCO2"]])

        # Clip outliers
        group["MtCO2 per day"] = group["MtCO2 per day"].clip(upper=group["MtCO2 per day"].mean() + clip_factor * group["MtCO2 per day"].std())

        # Reset index for final structure
        group = group.reset_index()

        # Add state and sector as columns for identification
        group["state"] = state
        group["sector"] = sector

        # Reorder columns to match original dataset
        group = group[["state", "date", "sector", "MtCO2 per day"]]

        # Append to the processed list
        processed_list.append(group)

    # Combine all processed groups into a single DataFrame
    processed_data = pd.concat(processed_list)

    # Reset index to make it easier to work with
    processed_data.reset_index(drop=True, inplace=True)

    # Save the processed data
    # 自行选择是否保存
    # processed_data.to_csv("datasets/processed_carbon.csv", index=False)

    return processed_data


# 生成每周的碳排放量函数
def generate_weekly_emissions(data):
    data['date'] = pd.to_datetime(data['date'])

    # 生成一个新的列表示“周”信息
    data['week'] = data['date'].dt.to_period('W')

    # 按照省份、产业和周进行分组并求和
    weekly_data = data.groupby(['state', 'sector', 'week'], as_index=False)['MtCO2 per day'].sum()

    # 重命名列，以便更容易理解
    weekly_data.rename(columns={'MtCO2 per day': 'MtCO2 per week'}, inplace=True)

    # 输出每周碳排放量到新的 CSV 文件
    weekly_data.to_csv('datasets/weekly_emissions.csv', index=False)


# Load the dataset, skip the first row containing column names
data = pd.read_csv("datasets/carbon.csv")

# 数据预处理：清洗、平滑、标准化、去除异常值
processed_data = preprocess_dataset(data)

# 生成每周的碳排放量
generate_weekly_emissions(processed_data)




