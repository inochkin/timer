from custom.not_main_page_styles import import_not_main_page_styles
from custom.sidebar import *
# from sidebar_custom import custom_sidebar  # ! need import not from *
# from check_user_is_auth import init_session_state_user_auth  # ! need import not from *
import time


import_not_main_page_styles()
custom_sidebar()  # -- sidebar custom


# -------------- get request  (?token=1111&email=2222).
if st.query_params:

    st.title("Confirmation Email")
    error_mess = None
    # print('all >>>>>>>', st.query_params)

    token = st.query_params["token"]
    email = st.query_params["email"]

    if not all([email, token]):
        st.error("- email or token was not send.")

    user = db_users.is_user_exist(email)
    if not user:
        st.error(f"- no user with email = {email}")
    else:
        token_expected = user.token_confirm
        if not db_users.verify_token(token, token_expected):
            st.error("- wrong token key.")
        else:
            if not user.status:
                db_users.activate_user(email)  # activate user.

            # save cookie.
            username = user.username
            user_id = str(user.id)  # object UUID to str.
            save_cookies_user_creds_encrypted(username, email, user_id)

            st.session_state["user_is_authorised"] = True
            st.session_state['username'] = username
            st.session_state['user_id'] = user_id
            st.session_state['user_email'] = email

            st.success("- Your account activated.")

            time.sleep(3)
            st.switch_page("main.py")  # redirect without full update page.

