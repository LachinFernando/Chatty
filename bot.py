import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from google.cloud import firestore

from llm import streaming_question_answering, LLM_MODELS
from google_integration import get_google_cloud_credentials, update_user_document


def set_up_credentials():
    if 'credentials' not in st.session_state:
        service_account_info = st.secrets["gcp_service_account"]
        credentials = get_google_cloud_credentials(service_account_info)
        st.session_state['credentials'] = credentials
    return st.session_state['credentials']


def get_db(credentials):
    # Initialize the Firestore client using credentials
    #credentials = set_up_credentials()
    db = firestore.Client(credentials=credentials)
    return db


def message_creator(list_of_messages: list) -> list:
    prompt_messages = []
    for message in list_of_messages:
        if message["role"] == "user":
            prompt_messages.append(HumanMessage(content = message["content"]))
        else:
            prompt_messages.append(AIMessage(content = message["content"]))

    return prompt_messages

def chatty():

    # set up firestore credentials
    creds=set_up_credentials()
    db = get_db(creds)
    
    # Assuming 'st.experimental_user' is a valid object with user details
    user_email = st.experimental_user["email"]
    user_name = st.experimental_user["name"]
    # web app

    st.title("Welcome to Chatty")

    with st.sidebar:
        # chose the model
        st.title("Choose Your Model")
        llm_option = st.selectbox(
            "Please select a LLM model you would like to interact?",
            LLM_MODELS,
            index = None
        )

        # selected model
        st.markdown("**Selected Model**: {}".format(llm_option))

    if not llm_option:
        st.error("Please Select a Model to Proceed!")
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_list = message_creator(st.session_state.messages)
            response = st.write_stream(streaming_question_answering(message_list, llm_option))
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Assuming user_email and user_name are set correctly in session
        update_user_document(db, user_email, user_name, prompt, response)