import streamlit as st
from streamlit_js import st_js
import base64
from custom.run_task import import_run_task
from database.db_init import db_users
from lib.general_func import time_to_seconds
from lib.static import TEST_TIMER


def card_2(user_timezone):
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.title("Run Task")

        hours_minutes = st.session_state.hours_minutes
        desc = st.session_state.desc
        priority = st.session_state.priority

        # -------------- short desc
        max_length = 60  # Максимальная длина текста
        short_desc = desc[:max_length] + "..." if len(desc) > max_length else desc
        st.text(short_desc)
        # --------------

        # Укажите лимит таймера в секундах
        if TEST_TIMER:
            limit_timer = 10
        else:
            limit_timer = time_to_seconds(hours_minutes)

        # --- to play MP3 need convert it to base64 to run as url source only.
        # if use source path - it will not work.

        final_sound_user = db_users.get_final_sound_user()
        file_name = final_sound_user if final_sound_user else "sound 8 (default)"

        with open(f'static/{file_name}.mp3', "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode()
            audio_source_done = f"data:audio/mp3;base64,{audio_base64}"

        with open('static/click.mp3', "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode()
            audio_source_click = f"data:audio/mp3;base64,{audio_base64}"

        # HTML + JavaScript таймер с ограничением
        import_run_task(user_timezone, hours_minutes, desc, priority,
                        limit_timer, audio_source_done, audio_source_click)

        if st.button("Cancel"):
            # need full restart page to get cookies update.
            st_js("parent.window.location.reload()")



