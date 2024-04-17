from fastapi import FastAPI, File, UploadFile
import my_preprocessing
import my_training
import pandas as pd
from pydantic import BaseModel
import xgboost as xgb
import uvicorn
import matplotlib as plt
import numpy as np
import io



app = FastAPI()

model_xgb = my_training.XGBoostModel()

class city:
    def __init__(self):
        self.city = ""
    def set_city(self, city):
         self.city = city

city_filter = city()


@app.get("/")
async def read_root():
    return {"message": "Welcome to application's API!"}


@app.post("/train/")
async def train(city_name: dict):
    if city_name["city_name"] is not None:
        city_filter.set_city(city_name["city_name"])
        data = model_xgb.df.loc[model_xgb.df['city_name'] == city_filter.city]
        data = data.drop(["Unnamed: 0", "city_name"], axis=1)
        X_train, X_val, y_train, y_val = my_preprocessing.data_split(data)
        model_xgb.train_model(X_train, y_train)
        model_xgb.validate_model(X_val, y_val)
        act_pred = {'actual': y_val, 'pred': model_xgb.pred}
        data = pd.DataFrame(act_pred)
        response = {"rmse": model_xgb.rmse, "mae": model_xgb.mae, "data": data.to_dict(orient="records")}
        return response
    else:
        response = {"rmse": "", "mae": "", "data": ""}
        return response
    


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
        """
        data = model_xgb.df.loc[model_xgb.df['city_name'] == "Lublin"]
        data = data.drop("Unnamed: 0", axis=1)
        data = my_preprocessing.create_dummies(data)
        X_train, X_val, y_train, y_val = my_preprocessing.data_split(data)
        model_xgb.train_model(X_train, y_train)
        """
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        df = df.loc[df['city_name'] == city_filter.city]
        df = df.drop(["Unnamed: 0", "city_name"], axis=1)
        model_xgb.predict_new(df)
        pred = pd.DataFrame(model_xgb.new_pred, columns = ["pred"])
        pred["pred"] = pred['pred'].astype(int)
        #data = pd.concat([df, pred])
        #data.fillna(value=np.nan, inplace=True)
        response = {"data": pred.to_dict(orient = "records")}
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





