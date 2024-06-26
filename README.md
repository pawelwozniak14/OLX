# Welcome to my application based on OLX (Otodom) data! 👋
This is an application built for model training on OLX data for state capital cities of Poland and also for predicting prices of new houses.   
Data come from **KNUM x GOLEM 2022 Hackathon** sponsored by OLX.   

## How to use the application
To run this project you need train7.csv and test7.csv which were too large to put them in this repo. I should have already sent you e-mail with the data or you need to contact me to get it.
You have to put train7.csv in the .../app/backend/data/

You should run this project with Docker.

To run prediction you should use test7.csv. Otherwise you need to put a csv with the exact same columns that use the same encodings etc. as original test7.csv.
To use prediction you first need to train a model in the training page. Then in the prediction page it will predict prices for the city you previously trained the model on.

## API methods 
API has 3 post endpoints.
- "/get_data/" where you should send a dictionary with "city_name" key, where value is name of the city of which you want to get data.

- "/train/" where you should send a dictionary with "city_name" key, where value is name of the city you would like to train the model on.
It returns a dictionary consisting of rmse, mae, data, where rmse is Root Mean Squared Error achieved on validation set, mae is Mean Absolute Error achieved on validation set and data is a dataframe with columns consisting of
actual and pred, where actual is actual prices of houses in validation set and pred is the predicted value.

- "/predict/" where you should send a byte file which is turned into a dataframe used to make predictions for your dataset.

## Here is how the application looks like:
- Exploratory Data Analysis:

![image](https://github.com/pawelwozniak14/OLX/assets/73362296/90af558f-8387-4b41-a78a-ca06ba1c4b45)

![image](https://github.com/pawelwozniak14/OLX/assets/73362296/94e9511b-6eaf-4297-9684-9465db8d42a6)

- Training:
![image](https://github.com/pawelwozniak14/OLX/assets/73362296/88c17f7b-d115-4745-8b3a-3c29e69b45db)

- Prediction:
![image](https://github.com/pawelwozniak14/OLX/assets/73362296/05f12126-2667-4466-a813-c2186385383c)









