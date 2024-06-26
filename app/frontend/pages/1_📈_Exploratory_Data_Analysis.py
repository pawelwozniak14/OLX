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

def show_data(data):
    st.dataframe(data.head(10))

def plot_price_dist(data):
    fig, ax = plt.subplots()
    sns.histplot(data['price'], kde=True, ax=ax)
    ax.set_xlabel('Price (PLN)')
    ax.set_ylabel('Frequency')
    ax.set_title('Price Distribution')
    # Display the plot in Streamlit
    st.pyplot(fig)

def plot_area_dist(data):
    fig, ax = plt.subplots()
    sns.histplot(data['m'], kde=True, ax=ax)
    ax.set_xlabel('Area (m²)')
    ax.set_ylabel('Frequency')
    ax.set_title('Area Distribution')
    # Display the plot in Streamlit
    st.pyplot(fig)

def plot_price_area(data):
    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x='m', y='price', ax=ax)
    ax.set_xlabel('Area (m²)')
    ax.set_ylabel('Price (PLN)')
    ax.set_title('Price of Flats Based on Area')
    # Display the plot in Streamlit
    st.pyplot(fig)

def plot_business_count(data):
    fig, ax = plt.subplots()
    sns.countplot(data=data, x='is_business', ax=ax)
    ax.set_xlabel('Is Business')
    ax.set_ylabel('Count')
    ax.set_title('Count of Business vs. Non-Business Flats')
    # Display the plot in Streamlit
    st.pyplot(fig)

def plot_balcony_price(data):
    fig, ax = plt.subplots()
    sns.boxplot(data=data, x='balcony', y='price', ax=ax)
    ax.set_xlabel('Has Balcony')
    ax.set_ylabel('Price (PLN)')
    ax.set_title('Price Distribution Based on Balcony Presence')
    # Display the plot in Streamlit
    st.pyplot(fig)

def plot_market_price(data):
    fig, ax = plt.subplots()
    sns.boxplot(data=data, x='market_primary', y='price', ax=ax)
    ax.set_xlabel('Market Primary')
    ax.set_ylabel('Price (PLN)')
    ax.set_title('Price Distribution Based on Market Primary')
    # Display the plot in Streamlit
    st.pyplot(fig)

data = ""

with st.form(key = "data"):
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


if not data.empty:
    show_data(data)
    plot_price_dist(data)
    plot_area_dist(data)
    plot_price_area(data)
    plot_business_count(data)
    plot_balcony_price(data)
    plot_market_price(data)