import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Prediction", page_icon="🔮")

st.header("🔮 Prediction")
st.markdown("Upload your data")

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def predict_data(file_bytes):
    response_predict = requests.post('http://127.0.0.1:8000/predict/', files={'file': file_bytes})
    json_data = response_predict.json()["data"]
    if json_data!="":
        df = pd.DataFrame(json_data)
    else:
        df = ""
    return df

data = ""

input_file = st.file_uploader("Upload a CSV file", type="csv", accept_multiple_files=False)

if input_file is not None:
    st.info("File uploaded successfully")
    if st.button("Upload to API"):
        st.info("Uploading file to API...")
        file_bytes = input_file.getvalue()
        data = predict_data(file_bytes)
        st.dataframe(data, width=150)
        csv = convert_df(data)
        st.download_button(
        label="Download predictions as CSV",
        data=csv,
        file_name='predictions.csv',
        mime='text/csv',
        )



