from fastapi import FastAPI
import my_preprocessing
import my_training
import pandas as pd
from pydantic import BaseModel
import xgboost as xgb
import uvicorn
import matplotlib

app = FastAPI()


df = pd.read_csv("data/train4.csv")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the model API!"}

@app.post("/hello_world/")
async def preprocess0(city_name: dict):
    return city_name


@app.post("/preprocess/")
async def preprocess(city_name: dict):
    data = df.loc[df['city_name'] == city_name["city_name"]]
    data = data.drop("Unnamed: 0", axis=1)
    data = my_preprocessing.create_dummies(df)
    X_train, X_val, y_train, y_val = my_preprocessing.data_split(data)
    model = my_training.train_model(X_train, y_train)
    rmse, mae = my_training.validate_model(model, X_val, y_val)
    response = {"rmse": rmse, "mae": mae}
    return response

#@app.post("/train/")
#async def train(X_train: pd.DataFrame, y_train: pd.DataFrame):
#    model = my_training.train_model(X_train, y_train)
#    return model

#@app.post("/validate/")
#async def validate(model: xgb.XGBRegressor, X_val: pd.DataFrame, y_val: pd.DataFrame):
#    rmse, mae = my_training.validate_model(model, X_val, y_val)
#    return rmse, mae





