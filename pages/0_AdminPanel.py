import streamlit as st
from google.cloud import firestore
import pandas as pd

from google_integration import get_google_cloud_credentials, get_user_details, update_user_document, get_user_field


ADMIN_LIST = st.secrets["admin"]["ADMIN_LIST"]
COLLECTION_NAME = "history"


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

if not st.experimental_user.is_logged_in:
    st.error("Please Login as Admin to use the service!")
    st.stop()

# get the user email
user_email = st.experimental_user["email"]

if not user_email in ADMIN_LIST:
    st.error("You are not an Admin!")
    st.stop()

# title
st.title('Chat Analysis')

# get credentials
# set up firestore credentials
creds=set_up_credentials()
db = get_db(creds)
doc_ref = db.collection(COLLECTION_NAME)
docs = doc_ref.stream()

# Extract data into a list of dictionaries
data = []
users = []
for doc in docs:
    doc_dict = doc.to_dict()
    email = doc_dict["email"]
    name = doc_dict["name"]
    query_list = doc_dict["queries_log"]
    doc_dict['id'] = doc.id

    # append the users
    users.append(
        {
            "Name": name,
            "Email": email
        }
    )
    
    for log_record in query_list:
        log_record["email"] = email
        log_record["name"] = name
        data.append(log_record)

# Convert list of dictionaries to DataFrame
df_history = pd.DataFrame(data)
df_users = pd.DataFrame(users)

# history
st.subheader("Chat History")
st.dataframe(df_history)

# users
st.subheader("Users")
st.dataframe(df_users)

