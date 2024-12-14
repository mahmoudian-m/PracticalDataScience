from exercise_1 import extract_data, calculate_moving_avg, store_data

expected_columns = ['Amount Requested', 'Application Date', 'Loan Title', 'Risk_Score',
                    'Debt-To-Income Ratio', 'Zip Code', 'State', 'Employment Length',
                    'Policy Code']

csv_path = "../../rejected_2007_to_2018Q4.csv"
size_of_chunks = 50

# Code testing to ensure that functions produces the expected outputs for specific inputs.
# Data testing to validate that each county number appears no more than once per date in a dataset.


df = extract_data(csv_path, size_of_chunks)


def test_extract_data_row_counts():
    assert df.shape[0] == 5169


def test_extract_data_column_match() -> None:
    assert df.columns.tolist() == expected_columns


def test_extract_data_no_duplicated() -> None:
    duplicated_df = df.loc[df.duplicated()]
    assert duplicated_df.empty


def test_extract_data_no_nulls() -> None:
    assert df["Risk_Score"].isnull().sum() == 0


ma = calculate_moving_avg(df, 50)


def test_calculate_moving_av_row_counts():
    assert ma.shape[0] == 5169


def test_calculate_moving_av__match() -> None:
    assert df.columns.tolist() == expected_columns.append("RiskScoreMA50")

