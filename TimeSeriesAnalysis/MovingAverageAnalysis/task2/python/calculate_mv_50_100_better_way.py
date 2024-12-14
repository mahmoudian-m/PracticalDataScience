from csv import reader
import datetime
import pandas as pd
import itertools
import os

source = "../../rejected_2007_to_2018Q4.csv"
output_result = "../../moving_avg_result/mv_result.csv"
destination_source = "../../moving_avg_result/""mv_result.csv"
columns = ['Amount Requested', 'Application Date', 'Loan Title', 'Risk_Score',
           'Debt-To-Income Ratio', 'Zip Code', 'State', 'Employment Length',
           'Policy Code']

stored_array = []
df = pd.DataFrame(columns=columns)


def calculate_moving_avg(extracted_data: pd.DataFrame, moving_average: int, column_name: str) -> pd.DataFrame | str:
    """
    Transform data and calculate moving average
    :param column_name: Name of new column
    :param moving_average: Moving average window
    :param extracted_data: DataFrame
    :return: DataFrame,str
    """
    if extracted_data.empty:
        return "Empty DataFrame"
    extracted_data = extracted_data.drop_duplicates().reset_index(drop=True)
    extracted_data[column_name] = extracted_data['Risk_Score'].rolling(moving_average).mean()
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
    absolute_path = os.path.abspath(path)
    if not os.path.isdir(absolute_path):
        return "Directory does not exist"
    transformed_data.to_csv(path + file_name, index=False, mode='a', header=False)


def processing(offset, time_filter):
    """
    Read CSV file from specific offset
    :param offset: from this line to read
    :param time_filter: filter based on year
    :return: last line number, filtered DataFrame
    """
    count = offset
    absolute_path = os.path.abspath(source)
    with open(absolute_path, 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in itertools.islice(csv_reader, offset, None):
            count += 1
            if datetime.datetime.strptime(row[1], "%Y-%m-%d").year == time_filter:
                if row[3]:
                    df.loc[len(df)] = row
            else:
                break
    return count, df


years = [2007, 2008, 2009, 2010, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

line_number = 1
for year in years:
    print("processing year: {}".format(year))
    line_number, selected_df = processing(line_number, year)
    if year == 2007:
        calculated_moving_avg = calculate_moving_avg(selected_df, 50, "RiskScoreMA50")
        print(store_data(calculated_moving_avg))
        df.drop(df.index, inplace=True)
    elif year == 2008:
        print(store_data(df))
        df.drop(df.index, inplace=True)
    else:
        calculated_moving_avg = calculate_moving_avg(selected_df, 100, "MA100")
        print(store_data(calculated_moving_avg))
        df.drop(df.index[:-100], axis=0, inplace=True)
        df.reset_index(inplace=True, drop=True)
