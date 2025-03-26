import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")  # Устанавливает широкий макет

from custom.sidebar import custom_sidebar
from custom.main_styles import import_main_styles
from database.db_init import db_users

st.title("All Users")

import_main_styles()
custom_sidebar()

users = db_users.get_all_users()
if users:
    df = pd.DataFrame(users)
    st.dataframe(df)

