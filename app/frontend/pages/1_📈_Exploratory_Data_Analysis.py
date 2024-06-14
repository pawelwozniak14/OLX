import streamlit as st
#import my_training
#import my_preprocessing
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Exploratory Data Analysis", page_icon="📈")

st.header("📈 EDA")
st.markdown("Choose your city")

def get_data_from_api(city_name):
    response_preprocess = requests.post('http://backend:8000/get_data/', json = city_name)
    json_data = response_preprocess.json()["data"]
    if json_data!="":
        df = pd.DataFrame(json_data)
    else:
        df = ""
    return df

with st.form(key = "train"):
    city = st.selectbox(
        "Choose your city",
        ["Białystok", "Bydgoszcz", "Gdańsk", "Gorzów Wielkopolski", "Katowice",
        "Kielce", "Kraków", "Lublin", "Łódź", "Olsztyn", "Opole",
        "Poznań", "Rzeszów", "Szczecin", "Toruń", "Warszawa", "Wrocław",
        "Zielona Góra"],
        label_visibility="collapsed",
        placeholder="Choose an option",
        index = None)
    city_name = {'city_name': city}
    #st.session_state['city_name'] = city_name
    data = get_data_from_api(city_name)
    submit_button = st.form_submit_button("Click here to confirm your choice", type="primary")

st.dataframe(data)