import streamlit as st


def import_not_main_page_styles():
    css = """
    <style>
    .stMainBlockContainer {background: #aac9e7;}
    .stMain {background: #aac9e7;}
    header {background: #aac9e7 !important;}

    .stSidebar{
        background: #4c78a3;
        transition: background-color 0.1s;
    }
    a[data-testid="stSidebarNavLink"] > span { color: white;}

    button[data-testid="stBaseButton-secondary"] {border: 2px solid rgb(231 154 149);}

    /* popup styles   */
    button[aria-label="Close"] {
        display: none !important;
    }

    div[data-testid="stDialog"] {
            background-image: linear-gradient(234deg, #aac9e7, #346389);
        color: black !important;
        padding: 10px !important;
    }

     /* Устанавливаем белый фон для внутреннего div в модальном окне */
    div[data-testid="stDialog"] > div {
            background-image: linear-gradient(234deg, #aac9e7, #346389);
        border-radius: 10px !important;
        padding: 20px !important;
    }

     div[aria-label="dialog"] {
             background-image: linear-gradient(234deg, #9ac1e7, #4d7597);
    }

    button[data-testid="stBaseButton-headerNoPadding"] {color: white;}
    button[data-testid="stBaseButton-headerNoPadding"] > svg {width: 30px; height: 30px;}

    label[data-baseweb="radio"] {padding: 5px;}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)