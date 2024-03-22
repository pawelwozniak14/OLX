import numpy as np
import pandas as pd
import csv

def preprocess_data(df, cities, districts, threshold=30):
    data = pd.merge(df, cities, left_on="city_id", right_on="id")
    data = data.drop("id_y", axis=1)
    districts = districts.rename(columns={"id": "district_id"})
    data = pd.merge(data, districts, on="district_id", how="left")
    data = data.drop(columns = {"Unnamed: 0", "id_x", "created_at_first", "region_id", "lon_x", "lat_x"})
    data = data.rename(columns = {"name_pl_x": "city_name", "name_pl_y": "disctrict_name"})
    data = data.loc[data['city_name'] == "Lublin"]
    parsed_data = data['params'].apply(parse_values).apply(pd.Series)
    parsed_data = drop_nans(data, threshold)

def merge_drop_rename(df, cities, districts):
    data = pd.merge(df, cities, left_on="city_id", right_on="id")
    data = data.drop("id_y", axis=1)
    districts = districts.rename(columns={"id": "district_id"})
    data = pd.merge(data, districts, on="district_id", how="left")
    data = data.drop(columns = {"Unnamed: 0", "id_x", "created_at_first", "region_id", "lon_x", "lat_x"})
    data = data.rename(columns = {"name_pl_x": "city_name", "name_pl_y": "disctrict_name"})

def parse_values(row):
    pairs = row.split('<br>')
    values = {}
    for pair in pairs:
        if pair.strip() != '':
            col, val = pair.split('<=>')
            if val.strip() == '' or val.strip().lower() == 'nan':
                val = np.nan
            values[col] = val
    return pd.Series(values)

def drop_nans(data, threshold):
    missing_percentages = data.isna().sum() / len(data) * 100
    columns_to_drop = missing_percentages[missing_percentages > threshold].index
    data_dropped = data.drop(columns=columns_to_drop)
    return data_dropped
