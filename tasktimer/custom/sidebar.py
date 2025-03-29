import streamlit as st
from streamlit_js import st_js
from components.check_user_is_auth import init_session_state_user_auth, user_is_authorised, \
    user_is_registered_not_active, set_current_date_user_to_session_state
from validate_email_address import validate_email
import secrets
from database.db_init import db_users
from lib.cookies import delete_cookie, save_cookies_user_creds_encrypted
from lib.send_email import send_confirmation_email
from lib.static import USER_AUTH_DATA_ENCRYPTED


def custom_sidebar():
    """
    Custom menu instead of all pages from 'pages' folder.
    """

    # -- init session_state
    init_session_state_user_auth()

    st.logo('./static/logo.png', size="large", link=None, icon_image=None)

    with st.sidebar:

        if user_is_authorised():
            username = st.session_state['username']
            # user_email = st.session_state['user_email']
            # user_id = st.session_state['user_id']
            st.success(f"Hello - {username}")

            set_current_date_user_to_session_state()
        else:
            st.button("Login", key='open_modal_login', on_click=modal_login, icon=':material/login:')
            st.button("Registration", key='open_modal_registration', on_click=modal_registration,
                      icon=':material/person_add:')

        if user_is_registered_not_active():
            st.success("Please check your mailbox to confirm your email")
            st.toast("Please check your mailbox to confirm your email", icon="✅")
            st.session_state["registered"] = False

        st.sidebar.page_link('main.py', label='Create Task', icon=':material/notifications_active:')

        # -- logout and pages.
        if user_is_authorised():
            st.sidebar.page_link('pages/statistics.py', label='Statistics', icon=':material/monitoring:')
            st.sidebar.page_link('pages/user_settings.py', label='Settings', icon=':material/settings:')

            # TODO for admin oly
            st.sidebar.page_link('pages/users.py', label='All Users (for admin)', icon=':material/person_search:')

            st.button("Logout", key='Logout', on_click=logout, icon=':material/logout:')


# ---------------------------------------------------------------------------
# registration
# ---------------------------------------------------------------------------

def _generate_token() -> str:
    # Generate a confirmation token
    return secrets.token_urlsafe(16)


def _is_valid_email(email):
    return validate_email(email)


def _validation_user_data(user_email: str, password: str, is_registration: bool, username: str = None):
    error_mess = None
    if is_registration:
        if db_users.is_user_exist(user_email):
            error_mess = f"- {user_email} is already exists."
        if not username:
            error_mess = "- user name is empty."

    if not user_email:
        error_mess = "- email is empty."
    if len(password) <= 6:
        error_mess = f"- password should be more that 6 simbols."
    if not _is_valid_email(user_email):
        error_mess = f"- email address is not valid."

    if error_mess:
        st.session_state["error_message"] = error_mess

        return False

    return True


def registrate_user():
    # -- get submitted values
    username = st.session_state.get("username", "")
    email = st.session_state.get("email", "")
    password = st.session_state.get("password", "")

    if _validation_user_data(email, password, is_registration=True, username=username):
        with st.spinner('Processing ...'):  # show spinner

            # create token.
            token = _generate_token()

            # Send confirmation email
            if not send_confirmation_email(email, token):
                st.session_state["error_message"] = "- Error during send confirmation email."
                return False

            # save user to db.
            db_users.register_user(username, email, password, token)

            if not st.session_state["error_message"]:
                st.session_state["registered"] = True
                st.session_state["success_message"] = True

            st.rerun()
    # else False


@st.dialog("User registration")
def modal_registration():
    st.write("Please enter your credentials.")

    with st.form("my_modal", clear_on_submit=True):
        # Input fields
        st.text_input("Username", key="username")
        st.text_input("Email", key="email")
        st.text_input("Password", type="password", key="password")

        # show error
        if st.session_state["error_message"]:
            st.error(st.session_state["error_message"])

        # Submit button logic
        if st.form_submit_button("Save"):   # or on_click=registrate_user but cannot use st.rerun().
            registrate_user()               # in order to use st.rerun()

# ---------------------------------------------------------------------------
# login
# ---------------------------------------------------------------------------

def login_user():
    # -- get submitted values
    email = st.session_state.get("email", "")
    password = st.session_state.get("password", "")

    if _validation_user_data(email, password, is_registration=False):
        status_authentication = db_users.authenticate_user(email, password)

        # print(email)
        # print(password)
        # print('status', status_authentication)

        if isinstance(status_authentication, tuple):
            user_id = status_authentication[1]
            username = status_authentication[2]

            # сохраняем данные в куки
            save_cookies_user_creds_encrypted(username, email, user_id)
            st_js("parent.window.location.reload()", key='refresh')
        else:
            # errors authenticate_user
            st.session_state["error_message"] = status_authentication

            return False


@st.dialog("User Login")
def modal_login():
    st.write("Please enter your credentials.")
    with st.form("my_modal", clear_on_submit=True):
        # Input fields
        st.text_input("Email", key="email")
        st.text_input("Password", type="password", key="password")

        # show error
        if st.session_state["error_message"]:
            st.error(st.session_state["error_message"])

        # Submit button logic
        if st.form_submit_button("Login"):   # or on_click=login_user but cannot use st.rerun().
            login_user()                     # in order to use st.rerun()


def logout():
    delete_cookie(USER_AUTH_DATA_ENCRYPTED, '13')
    st_js("parent.window.location.reload()", key='refresh')
    # time.sleep(1)
    # st.switch_page("main.py")  # redirect without full update page.




