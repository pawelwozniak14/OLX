import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to my application based on OLX (Otodom) data! 👋")

st.sidebar.success("Select a functionality above.")

st.markdown(
    """
    This is an application built for model training on OLX data for state capital cities of Poland and also for predicting prices of new houses.   
    Data come from **KNUM x GOLEM 2022 Hackathon** sponsored by OLX.   
    Project will be further developed in the future.  
    ### Want to learn more about the project?
    - Check out my [github](https://github.com/pawelwozniak14/OLX)
    ### Do you have any questions? Contact me via:
    - [LinkedIn](www.linkedin.com/in/pawelwozniak14)
    - [s96474@pollub.edu.pl](s96474@pollub.edu.pl)
"""
)