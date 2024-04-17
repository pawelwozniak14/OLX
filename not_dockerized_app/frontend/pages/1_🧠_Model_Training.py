import streamlit as st
#import my_training
#import my_preprocessing
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Model Training", page_icon="🧠")

st.header("🧠 Model training")
st.markdown("Choose your city")

#st.write("""In this page you can train your own model!""")

#@st.cache_data
def train_model_from_api(city_name):
    response_preprocess = requests.post('http://backend:8000/train/', json = city_name)
    json_data = response_preprocess.json()["data"]
    rmse = response_preprocess.json()["rmse"]
    mae = response_preprocess.json()["mae"]
    if json_data!="":
        df = pd.DataFrame(json_data)
    else:
        df = ""
    return rmse, mae, df

data = ""

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
    rmse, mae, data = train_model_from_api(city_name)
    submit_button = st.form_submit_button("Click here to confirm your choice", type="primary")



if type(data)!=str:
    st.write("RMSE reached on test data:", rmse)
    st.write("MAE reached on test data:", mae)
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    # Scatter plot
    sns.scatterplot(x='actual', y='pred', data=data, ax=ax)
    # Add diagonal line
    ax.plot(data['actual'], data['actual'], color='red', linestyle='--')
    # Add labels and title  
    ax.set_xlabel('Actual Values')
    ax.set_ylabel('Predicted Values')
    ax.set_title('Actual vs Predicted')
    # Show plot
    st.pyplot(fig)