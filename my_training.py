from GPyOpt.methods import BayesianOptimization
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error
import xgboost as xgb
import pandas as pd


class XGBoostModel:
    def __init__(self):
        self.df = pd.read_csv("data/train7.csv") #read train data

    def set_df(self, df):
        self.df = df

    def set_city(self, city_name: str):
        self.city = city_name
        self.df.loc[self.df['city_name'] == self.city]

    def xgb_cv_score(self, parameters): #scoring function for the model
        parameters = parameters[0]
        score = -cross_val_score(
            	xgb.XGBRegressor(
                	max_depth=int(parameters[0]),
                	min_child_weight=int(parameters[1]),
                	subsample=parameters[2],
                	colsample_bytree=parameters[3],
                	n_estimators=int(parameters[4]),
                	learning_rate=parameters[5]),
            	self.X_train, self.y_train, scoring='neg_mean_squared_error', cv=3).mean()
        return score

    def train_model(self, X, y):
        self.X_train = X
        self.y_train = y
        baysian_opt_bounds = [
	        {'name': 'max_depth', 'type': 'discrete', 'domain': (3, 10, 5, 15)},
	        {'name': 'min_child_weight', 'type': 'discrete', 'domain': (1, 5, 10)},
	        {'name': 'subsample', 'type': 'continuous', 'domain': (0.5, 1.0)},
	        {'name': 'colsample_bytree', 'type': 'continuous', 'domain': (0.5, 1.0)},
	        {'name': 'n_estimators', 'type': 'discrete', 'domain': (100, 200, 300, 400)},
	        {'name': 'learning_rate', 'type': 'continuous', 'domain': (0.01, 0.2)}
        ]
        optimizer = BayesianOptimization(
	        f=self.xgb_cv_score, domain=baysian_opt_bounds, model_type='GP',
	        acquisition_type='EI', max_iter=25
            )
        optimizer.run_optimization()
        best_params_bayesian = optimizer.x_opt #getting best params
        params_bayesian_opt = {
	    'max_depth': int(best_params_bayesian[0]),
	    'min_child_weight': int(best_params_bayesian[1]),
	    'subsample': best_params_bayesian[2],
	    'colsample_bytree': best_params_bayesian[3],
	    'n_estimators': int(best_params_bayesian[4]),
	    'learning_rate': best_params_bayesian[5]
        } #setting a dict of best params
        # Initialize and train the model
        model_bayesian_opt = xgb.XGBRegressor(**params_bayesian_opt) 
        model_bayesian_opt.fit(self.X_train, self.y_train) #training
        self.model = model_bayesian_opt


    def validate_model(self, X_val, y_val):
        self.pred = self.model.predict(X_val) #make predictions on val set
        self.rmse = mean_squared_error(y_val, self.pred, squared = False) #calculate rmse
        self.mae = mean_absolute_error(y_true = y_val, y_pred = self.pred) #calculate mae

    def predict_new(self, X_test):
        self.new_pred = self.model.predict(X_test) #make new preds
