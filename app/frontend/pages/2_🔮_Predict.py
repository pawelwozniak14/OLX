import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Prediction", page_icon="🔮")

st.header("🔮 Prediction")
st.markdown("Upload your data")

def convert_df(df): #convert pandas dataframe to csv
   return df.to_csv(index=False).encode('utf-8') 

def predict_data(file_bytes): #get prediction from api
    response_predict = requests.post('http://backend:8000/predict/', files={'file': file_bytes})
    json_data = response_predict.json()["data"]
    if json_data!="":
        df = pd.DataFrame(json_data)
    else:
        df = ""
    return df

data = ""

input_file = st.file_uploader("Upload a CSV file", type="csv", accept_multiple_files=False) #upload file

if input_file is not None:
    st.info("File uploaded successfully")
    if st.button("Upload to API"):
        st.info("Uploading file to API...")
        file_bytes = input_file.getvalue() #turning file into bytes
        data = predict_data(file_bytes) #get prediction from api
        st.dataframe(data, width=150) #create dataframe of prediction results
        csv = convert_df(data) #convert results to csv
        st.download_button( #download csv with predictions
        label="Download predictions as CSV",
        data=csv,
        file_name='predictions.csv',
        mime='text/csv',
        )



