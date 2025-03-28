import streamlit as st


def import_not_main_page_styles():
    css = """
        <style>
        
        [data-testid="stSidebarHeader"]::after  {
                content: "TASK TIMER";
                margin-left: 20px;
                margin-top: 15px;
                font-size: 20px;
                position: absolute;
                top: 10px;
                left: 50px;
                color: #0f3b8f;
                font-weight: bold;
        }
        
        div[data-testid="stMarkdownContainer"] > p { color: #101010 !important;}
        [data-testid="stIconMaterial"] { color: #101010 !important;}

        .stMainBlockContainer {background: #aac9e7;}
        .stMain {background: #aac9e7;}
        
        // hide defualt header
        header {visibility: hidden;}
        [data-testid="stHeader"] {display: none;}

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