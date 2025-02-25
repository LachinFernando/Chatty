import pandas as pd
import streamlit as st
import pandas as pd 

from bot import chatty


IMAGE_ADDRESS = "https://getvoip.com/uploads/State-of-Chatbots-1024x594.png"

# web app
st.title("Chatty")

st.image(IMAGE_ADDRESS, caption = "Your Personal Chat App")

if not st.experimental_user.is_logged_in:
    if st.sidebar.button("Log in with Google", type="primary", icon=":material/login:"):
        st.login()
else:
    if st.sidebar.button("Log out", type="secondary", icon=":material/logout:"):
        st.logout()
    # Display user name
    # chat app
    chatty()