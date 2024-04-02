import streamlit as st
#import my_training
#import my_preprocessing
import pandas as pd
import requests

st.set_page_config(page_title="Exploratory Data Analysis", page_icon="📈")

st.markdown("# Exploratory Data Analysis")
st.sidebar.header("EDA parameters")
st.write(
    """In this page you can watch visualisations of the data"""
)


#@st.cache_data
#def load_data():
#    df = pd.read_csv('data/train2.csv', dtype={"district_id": "Int64", "city_id": "Int64", "id": "Int64", "is_business": "string", "region_id": "Int64", "price": "Int64", "created_at_first": "str",
#"params": "str"}, engine="python", encoding="utf-8")
#    districts = pd.read_csv("data/districts.csv", dtype={'id': 'Int64'})
#    cities = pd.read_csv("data/cities.csv", dtype={'id': 'Int64'})
#    return df, districts, cities

#df, districts, cities = load_data()





with st.sidebar.form(key="city_form"):
    st.header("Choose your city 🏙️")
    city = st.selectbox(
        "Choose your city",
        ["Białystok", "Bydgoszcz", "Gdańsk", "Gorzów Wielkopolski", "Katowice",
         "Kielce", "Kraków", "Lublin", "Łódź", "Olsztyn", "Opole",
         "Poznań", "Rzeszów", "Szczecin", "Toruń", "Warszawa", "Wrocław",
         "Zielona Góra"],
        label_visibility="collapsed")
    submit_button = st.form_submit_button("Click here to confirm your choice", type="primary")
    st.write(city)

city_name = {'city_name': city}
response = requests.post('http://backend:8000/hello_world/', json = city_name)
st.write(response.json())
