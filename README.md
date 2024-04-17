This is an application built for model training on OLX data for state capital cities of Poland and also for predicting prices of new houses.   
Data come from **KNUM x GOLEM 2022 Hackathon** sponsored by OLX.   

To run this project you need train7.csv and test7.csv which were too large to put them in this repo. I should have already sent you e-mail with the data or you need to contact me to get it.
You have to put train7.csv in the .../app/backend/data/

You should run this project with Docker.

To run prediction you should use test7.csv. Otherwise you need to put a csv this the exact same columns that use the same encodings etc. as original test7.csv.
To use prediction you first need to train a model in the training page. Then in the prediction page it will predict prices for the city you previously trained the model on.




