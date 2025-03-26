import streamlit as st

from lib.cookies import check_cookie_user_is_authorised


def init_session_state_user_auth():
    """
    initialisation of 'st.session_state' works separately on two different files.
    It means will be 2 different calls to the function.
    So if you want to use these 'st.session_state' in a file that has import another file with
    the same 'st.session_state' will be issue with different calls initialisation.
    !! 'st.session_state' keys should be used in one file only. !!
    """
    # ------- init session_state variables.
    for key in ['error_message',
                'success_message',
                'registered',
                'user_is_authorised',
                'username',
                'user_email',
                'user_id'
                ]:
        if key not in st.session_state:
            st.session_state[key] = False

    # ----------------------------------------
    # print('---- call init -------')
    # print('>>>>', st.session_state)

    if not st.session_state['user_is_authorised']:
        """
        if user is not authorised check cookie USER_AUTH_DATA_ENCRYPTED exists or not.
        if cookie exists - update session_state 'user_authorised'.
        in order not to call check_user_is_authorised every time. 
        """

        user_data = check_cookie_user_is_authorised()

        if user_data:
            # print('>>> user is authorised !!!')
            st.session_state['user_is_authorised'] = True
            st.session_state['username'] = user_data[0]
            st.session_state['user_email'] = user_data[1]
            st.session_state['user_id'] = user_data[2]


def user_is_authorised():
    return st.session_state['user_is_authorised']


def user_is_registered_not_active():
    return st.session_state['registered']

