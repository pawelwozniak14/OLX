import numpy as np
import pandas as pd
import csv

def preprocess_data(df, cities, districts, city_name="Lublin", threshold=30):
    data = merge_drop_rename(df, cities, districts) #combining dataframes
    data = data.loc[data['city_name'] == city_name] #filtering data for a given city
    parsed_data = data['params'].apply(parse_values).apply(pd.Series) #extracting params
    parsed_data = drop_nans(parsed_data, threshold) #dropping NaNs for a given threshold
    parsed_data = parsed_data.loc[parsed_data["build_year"].astype("Int16")>=1900] #selecting only instances of
    data = data.drop("params", axis=1) #dropping column params (parsed params stay)
    data = pd.concat([data, parsed_data], axis=1) #combining data with extracted params
    parsed_data = data['extras_types'].apply(parse_extras).apply(pd.Series) # for parsing extras_types 
    parsed_data = parsed_data.drop(["trash"], axis=1) #droping trash column from extras_type
    parsed_data = parsed_data.replace(np.nan, False)
    data = pd.concat([data, parsed_data], axis=1) #combining extras with data
    data = data.drop(["extras_types", "price[currency]", "rent[currency]"], axis=1)
    data["category"] = data["category"].str.replace(' ','_').str.lower().str.replace('ż', 'z') #change category into lower letters, with underscore instead of space and "z" instead of "ż"

    return data

def merge_drop_rename(df, cities, districts):
    data = pd.merge(df, cities, left_on="city_id", right_on="id") #merging data with cities
    data = data.drop("id_y", axis=1) #dropping trash column
    districts = districts.rename(columns={"id": "district_id"})
    data = pd.merge(data, districts, on="district_id", how="left") #merging data (now data with cities) with districts
    data = data.drop(columns = {"Unnamed: 0", "id_x", "created_at_first", "region_id", "lon_x", "lat_x", "city_id"}) #dropping trash columns
    data = data.rename(columns = {"name_pl_x": "city_name", "name_pl_y": "disctrict_name"})
    return data

def parse_values(row):
    pairs = row.split('<br>') #creating a pair of col_name and value
    values = {}
    for pair in pairs: #going through pairs of col_name and value
        if pair.strip() != '': 
            col, val = pair.split('<=>') #splitting a pair for col_name and value
            if val.strip() == '' or val.strip().lower() == 'nan':
                val = np.nan #filling with NaNs
            values[col] = val #putting values into columns
    return pd.Series(values)

def parse_extras(row):
    row = str(row) #for some reason it wasn't a string
    pairs = row.split('<->') #splitting extras
    values = {}
    for pair in pairs:
        if pair.strip() != '' and pair.strip() != 'nan' and pair.strip() != "0":
            col = pair
            val = True #assigning value
        else:
            col = "trash"
            val = np.nan
        values[col] = val #putting values into columns
    return pd.Series(values)

def drop_nans(data, threshold):
    missing_percentages = data.isna().sum() / len(data) * 100
    columns_to_drop = missing_percentages[missing_percentages > threshold].index
    data_dropped = data.drop(columns=columns_to_drop)
    return data_dropped

def transform_build_year(data):
    data["build_year"] = data["build_year"].astype("Int16")
    data = data.loc[data['build_year'] >= 1800]
    bins = [1800, 1900, 1945, 1989, 2000, 2011, 2021]
    labels = ['1800-1900', '1901-1945', '1946-1989', '1990-2000', '2001-2011', '2011-2021']
    data['build_year_category'] = pd.cut(data['build_year'], bins=bins, labels=labels, right=False)
    dummy = pd.get_dummies(data["build_year_category"])
    data = pd.concat([data, dummy], axis=1)   
    data = data.drop(["build_year", "build_year_category"], axis=1)
