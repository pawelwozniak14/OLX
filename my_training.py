from GPyOpt.methods import BayesianOptimization
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error
import xgboost as xgb


def train_model(X, y):
    global X_train
    global y_train
    X_train = X
    y_train = y
    baysian_opt_bounds = [
	{'name': 'max_depth', 'type': 'discrete', 'domain': (3, 10, 5, 15)},
	{'name': 'min_child_weight', 'type': 'discrete', 'domain': (1, 5, 10)},
	{'name': 'subsample', 'type': 'continuous', 'domain': (0.5, 1.0)},
	{'name': 'colsample_bytree', 'type': 'continuous', 'domain': (0.5, 1.0)},
	{'name': 'n_estimators', 'type': 'discrete', 'domain': (100, 200, 300, 400)},
	{'name': 'learning_rate', 'type': 'continuous', 'domain': (0.01, 0.2)}
    ]
    optimizer = BayesianOptimization(
	    f=xgb_cv_score, domain=baysian_opt_bounds, model_type='GP',
	    acquisition_type='EI', max_iter=25
        )
    optimizer.run_optimization()
    best_params_bayesian = optimizer.x_opt
    params_bayesian_opt = {
	'max_depth': int(best_params_bayesian[0]),
	'min_child_weight': int(best_params_bayesian[1]),
	'subsample': best_params_bayesian[2],
	'colsample_bytree': best_params_bayesian[3],
	'n_estimators': int(best_params_bayesian[4]),
	'learning_rate': best_params_bayesian[5]
    }
    # Initialize and train the model
    model_bayesian_opt = xgb.XGBRegressor(**params_bayesian_opt)
    model_bayesian_opt.fit(X_train, y_train)
    return model_bayesian_opt


def validate_model(model, X_val, y_val):
    predictions_bayesian_opt = model.predict(X_val)
    rmse_bayesian_opt = mean_squared_error(y_val, predictions_bayesian_opt, squared = False)
    mae = mean_absolute_error(y_true = y_val, y_pred = predictions_bayesian_opt)
    print("RMSE for Bayesian Optimization: ", rmse_bayesian_opt)
    print("MAE for Bayesian Optimization: ", mae)


def xgb_cv_score(parameters):
    parameters = parameters[0]
    score = -cross_val_score(
            	xgb.XGBRegressor(
                	max_depth=int(parameters[0]),
                	min_child_weight=int(parameters[1]),
                	subsample=parameters[2],
                	colsample_bytree=parameters[3],
                	n_estimators=int(parameters[4]),
                	learning_rate=parameters[5]),
            	X_train, y_train, scoring='neg_mean_squared_error', cv=3).mean()
    return score