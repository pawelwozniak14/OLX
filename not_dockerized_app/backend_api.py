from fastapi import FastAPI
import my_preprocessing
import my_training
import pandas as pd
from pydantic import BaseModel
import xgboost as xgb
import uvicorn
import matplotlib as plt
import numpy as np
import jsonpickle.ext.pandas as jsonpickle_pandas
from jsonpickle.pickler import Pickler
from jsonpickle.unpickler import Unpickler
from fastapi.responses import StreamingResponse
import joblib
import os

jsonpickle_pandas.register_handlers()

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
    if city_name["city_name"]!=None:
        data = df.loc[df['city_name'] == city_name["city_name"]]
        data = data.drop("Unnamed: 0", axis=1)
        data = my_preprocessing.create_dummies(data)
        X_train, X_val, y_train, y_val = my_preprocessing.data_split(data)
        model = my_training.train_model(X_train, y_train)
        rmse, mae, pred = my_training.validate_model(model, X_val, y_val)
        act_pred = {'actual': y_val, 'pred': pred}
        data = pd.DataFrame(act_pred)
        response = {"rmse": rmse, "mae": mae, "data": data.to_dict(orient="records")}
        if not os.path.exists("models"):
            os.makedirs("models")
        #joblib.dump(model, 'models/xgb_model.pkl')
        try:
            joblib.dump(model, 'models/xgb_model.pkl')
        except Exception as e:
            print("Error saving the model:", e)
        return response
    else:
        response = {"rmse": "", "mae": "", "data": ""}
        return response
    

"""
@app.post("/train/")
async def train(df_in: dict):
    #data = df["df_in"]
    #data = pd.DataFrame(df)
    data = pd.DataFrame.read_json(df_in)
    answer = data["price"][0]
    response = {"rmse": answer, "mae": "xd3"}
    return response
    X_train, X_val, y_train, y_val = my_preprocessing.data_split(data)
    model = my_training.train_model(X_train, y_train)
    rmse, mae = my_training.validate_model(model, X_val, y_val)
    response = {"rmse": rmse, "mae": mae}
    return response
"""
#@app.post("/train/")
#async def train(X_train: pd.DataFrame, y_train: pd.DataFrame):
#    model = my_training.train_model(X_train, y_train)
#    return model

#@app.post("/validate/")
#async def validate(model: xgb.XGBRegressor, X_val: pd.DataFrame, y_val: pd.DataFrame):
#    rmse, mae = my_training.validate_model(model, X_val, y_val)
#    return rmse, mae





