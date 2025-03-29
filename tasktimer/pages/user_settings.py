import streamlit as st
st.set_page_config(layout="centered")

from custom.sidebar import custom_sidebar
from custom.not_main_page_styles import import_not_main_page_styles
from database.db_init import db_users

import_not_main_page_styles()
custom_sidebar()

st.title("User settings")


# --- 1 Min minutes to select for user.
list_min_options = ("", "02", "05", "10", "15")
min_time_user = db_users.get_min_time_user()
default_index = list_min_options.index(min_time_user) if min_time_user in list_min_options else 0

min_minutes = st.selectbox("Set your min task time in minutes.", list_min_options, index=default_index)
if min_minutes:
    db_users.save_user_min_time(min_minutes)


# ---- 2 set sound complete
final_sounds = ["sound 1", "sound 2", "sound 3", "sound 4",
                "sound 5", "sound 6", "sound 7", "sound 8 (default)"]
final_sound_user = db_users.get_final_sound_user()

default_index = final_sounds.index(final_sound_user) if final_sound_user in final_sounds else 7
final_sound = st.selectbox("Set final sound", final_sounds, index=default_index)
if final_sound:
    db_users.save_final_sound(final_sound)











