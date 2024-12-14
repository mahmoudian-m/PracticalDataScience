#######################################################################
# Title      :    Calculate moving average
# Author     :    Mostafa Mahmoudian <mahmoudian.m1991@gmail.com>
# Date       :    2022-11-25
# Requires   :    pandas
# Category   :
#######################################################################
# Description
#   Calculate exponential moving average for CSV file based on Risk_Score column for 2007 year
#######################################################################
import pandas as pd
import os.path
import datetime


def extract_data(source: str, chunk_size: int,
                 time_filter: datetime.date = datetime.datetime(2008, 1, 1)) -> pd.DataFrame | str:
    """
    Extract and filter data from CSV file
    :param source: CSV path to read data
    :param chunk_size: Chunk size for reading from each iterator
    :param time_filter: Filtering data by year
    :return: Pandas DataFrame,str
    """
    print('Start extracting data')
    absolute_path = os.path.abspath(source)
    if not os.path.isfile(absolute_path):
        return "CSV file does not exist"
    stored_df = pd.DataFrame()
    with pd.read_csv(absolute_path, chunksize=chunk_size) as reader:
        for chunk in reader:
            selected_df = chunk.loc[
                (pd.to_datetime(chunk['Application Date']) < time_filter)]
            df_size = selected_df.shape[0]
            if df_size > 0:
                stored_df = pd.concat([stored_df, selected_df])
            if df_size < chunk_size:
                break
    if not stored_df.empty:
        return stored_df.dropna(subset=['Risk_Score']).drop_duplicates().reset_index(drop=True)
    else:
        return "Empty DataFrame"


def calculate_exp_moving_avg(extracted_data: pd.DataFrame, moving_average: int) -> pd.DataFrame | str:
    """
    Transform data and calculate Exponential moving average
    :param moving_average: Moving average window
    :param extracted_data: DataFrame
    :return: DataFrame,str
    """
    print('Start Calculating moving average')
    if extracted_data.empty:
        return "Empty DataFrame"
    extracted_data['RiskScoreMA50'] = extracted_data['Risk_Score'].ewm(alpha=0.5, adjust=False, min_periods=50).mean()
    return extracted_data


def store_data(transformed_data: pd.DataFrame, path: str = "../../moving_avg_result/",
               file_name: str = "mv_result.csv", ) -> None | str:
    """
    Save result into CSV file
    :param path: directory to save result
    :param file_name: name of CSV file
    :param transformed_data: DataFrame
    :return: None
    """
    print('Start storing results')
    absolute_path = os.path.abspath(path)
    if not os.path.isdir(absolute_path):
        return "Directory does not exist"
    transformed_data.to_csv(path + file_name, index=False)


if __name__ == "__main__":
    csv_path = "../../calculatedma50.csv"
    size_of_chunks = 50
    df = extract_data(csv_path, size_of_chunks)
    ma = calculate_exp_moving_avg(df, 50)
    store_data(transformed_data=df)
