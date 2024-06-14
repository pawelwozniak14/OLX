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

model_xgb = my_training.XGBoostModel() #init model

class city:
    def __init__(self):
        self.city = ""
    def set_city(self, city):
         self.city = city

city_filter = city() #init city


@app.get("/")
async def read_root():
    return {"message": "Welcome to application's API!"}

@app.post("/get_data/")
async def get_data(city_name: dict):
    city_filter.set_city(city_name["city_name"]) #set city to user's choice
    data = model_xgb.df.loc[model_xgb.df['city_name'] == city_filter.city] #filter dataframe to user's city choice
    data = data.drop(["Unnamed: 0", "city_name"], axis=1) #drop trash column and city_name
    response = {"data": data.to_dict(orient="records")}
    return response


@app.post("/train/")
async def train(city_name: dict):
    if city_name["city_name"] is not None:
        city_filter.set_city(city_name["city_name"]) #set city to user's choice
        data = model_xgb.df.loc[model_xgb.df['city_name'] == city_filter.city] #filter dataframe to user's city choice
        data = data.drop(["Unnamed: 0", "city_name"], axis=1) #drop trash column and city_name so the model doesn't learn it
        X_train, X_val, y_train, y_val = my_preprocessing.data_split(data) #train, val split
        model_xgb.train_model(X_train, y_train) #model training
        model_xgb.validate_model(X_val, y_val) #getting metrics on val set
        act_pred = {'actual': y_val, 'pred': model_xgb.pred} 
        data = pd.DataFrame(act_pred) #actual vs pred dataframe
        response = {"rmse": model_xgb.rmse, "mae": model_xgb.mae, "data": data.to_dict(orient="records")}
        return response
    else:
        response = {"rmse": "", "mae": "", "data": ""}
        return response
    


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
        content = await file.read() #read the file
        df = pd.read_csv(io.BytesIO(content)) #read the file into csv
        df = df.loc[df['city_name'] == city_filter.city] #filter to previously chosen city in train
        df = df.drop(["Unnamed: 0", "city_name"], axis=1) #drop trash column and city_name
        model_xgb.predict_new(df) #make prediction
        pred = pd.DataFrame(model_xgb.new_pred, columns = ["pred"]) #create a dataframe with results
        pred["pred"] = pred['pred'].astype(int) #turn it into ints so it isnt float
        #data = pd.concat([df, pred])
        #data.fillna(value=np.nan, inplace=True)
        response = {"data": pred.to_dict(orient = "records")} 
        return response





