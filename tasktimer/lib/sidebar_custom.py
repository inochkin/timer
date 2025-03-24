import streamlit as st


def custom_sidebar():
    """
    Custom menu instead of all pages from 'pages' folder.
    """

    st.logo('./static/logo.png', size="large", link=None, icon_image=None)

    st.sidebar.page_link('main.py', label='Main page', icon=':material/home:')
    st.sidebar.page_link('pages/user_settings.py', label='Settings', icon=':material/garden_cart:')
    st.sidebar.page_link('pages/statistics.py', label='Statistics', icon=':material/cognition:')

