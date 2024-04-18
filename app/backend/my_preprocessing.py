import numpy as np
import pandas as pd
import csv
from sklearn.model_selection import train_test_split

def data_split(data):
    X = data.drop("price", axis=1) #create X
    y = data["price"] #create y
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size = 0.2, random_state = 14) #split
    return X_train, X_val, y_train, y_val