from fastapi import FastAPI
import my_preprocessing
import my_training
import pandas as pd
from pydantic import BaseModel
import xgboost as xgb

app = FastAPI()

df = pd.read_csv('data/train2.csv', dtype={"district_id": "Int64", "city_id": "Int64", "id": "Int64", "is_business": "string", "region_id": "Int64", "price": "Int64", "created_at_first": "str",
"params": "str"}, engine="python", encoding="utf-8")
districts = pd.read_csv("data/districts.csv", dtype={'id': 'Int64'})
cities = pd.read_csv("data/cities.csv", dtype={'id': 'Int64'})


@app.post("/hello_world/")
async def preprocess(city_name: str):
    return city_name

@app.post("/preprocess/")
async def preprocess(city_name: str):
    data = my_preprocessing.preprocess_data(df, cities, districts, city_name=city_name)
    X_train, X_val, y_train, y_val = my_preprocessing.data_split(data)
    return X_train, X_val, y_train, y_val

@app.post("/train/")
async def train(X_train: pd.DataFrame, y_train: pd.DataFrame):
    model = my_training.train_model(X_train, y_train)
    return model

@app.post("/validate/")
async def validate(model: xgb.XGBRegressor, X_val: pd.DataFrame, y_val: pd.DataFrame):
    rmse, mae = my_training.validate_model(model, X_val, y_val)
    return rmse, mae





