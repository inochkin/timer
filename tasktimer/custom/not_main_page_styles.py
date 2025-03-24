import streamlit as st


def import_not_main_page_styles():
    css = """
        <style>
        div[data-testid="stMarkdownContainer"] > p { color: #101010 !important;}
        [data-testid="stIconMaterial"] { color: #101010 !important;}

        .stMainBlockContainer {background: #aac9e7;}
        .stMain {background: #aac9e7;}
        header {background: #aac9e7 !important;}

        .stSidebar{
            background: #4c78a3;
            transition: background-color 1.5s;
        }
        a[data-testid="stSidebarNavLink"] > span { color: white;}

        button[data-testid="stBaseButton-headerNoPadding"] {color: white;}
        button[data-testid="stBaseButton-headerNoPadding"] > svg {width: 30px; height: 30px;}


        </style>
        """
    st.markdown(css, unsafe_allow_html=True)