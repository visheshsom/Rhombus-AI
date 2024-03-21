import pandas as pd
import os
from dateutil.parser import parse


def is_date(string):
    try:
        parse(string)
        return True
    except ValueError:
        return False


def infer_categorical(series, threshold=0.05):
    if series.dtype == object and (series.nunique() / len(series) < threshold):
        return True
    return False


def infer_and_convert_dtypes(df):
    for column in df.columns:
        col_data = df[column]

        if col_data.dtype == object:
            # Check if the column contains dates
            if all(is_date(val) for val in col_data.dropna().unique()):
                # Specify the format to avoid the warning and improve performance
                datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
                try:
                    temp_col_data = pd.to_datetime(
                        col_data, format=datetime_format, errors="raise"
                    )
                    # If successful, check if time is all zeros and decide the format accordingly
                    if all(
                        item.time() == pd.Timestamp(0).time() for item in temp_col_data
                    ):
                        df[column] = temp_col_data.dt.date
                    else:
                        df[column] = temp_col_data
                except (ValueError, TypeError):
                    pass  # If conversion with the specific format fails, do not convert

            # Infer categoricals and numerics
            elif infer_categorical(col_data):
                df[column] = col_data.astype("category")
            else:
                df[column] = pd.to_numeric(col_data, errors="coerce").fillna(col_data)
    return df


def process_file(file):
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    file_name = file.name
    file_extension = os.path.splitext(file_name)[1].lower()
    temp_file_path = os.path.join(temp_dir, file_name)

    with open(temp_file_path, "wb+") as temp_file:
        for chunk in file.chunks():
            temp_file.write(chunk)

    # Determine file type and read file accordingly
    if file_extension in [".csv"]:
        df = pd.read_csv(temp_file_path)
    elif file_extension in [".xls", ".xlsx"]:
        df = pd.read_excel(temp_file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")

    df = infer_and_convert_dtypes(df)

    result = df.to_json(orient="records", date_format="iso")
    return result
