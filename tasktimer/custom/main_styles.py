import streamlit as st


def import_main_styles():
    css = """
    <style>
    
    /* Скрываем пустые контейнеры от CookieController после рефреша */
    .stElementContainer:has(iframe[height="0"]) {
        display: none !important;
    }
        
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
    
    button[data-testid="stBaseButton-headerNoPadding"] {color: white;}
    button[data-testid="stBaseButton-headerNoPadding"] > svg {width: 30px; height: 30px;}
    
    label[data-baseweb="radio"] {padding: 5px;}
    
    /* ----------------------- */
    
     /* ---- on loading page  -- */
    .stMainBlockContainer {
        opacity: 0;
        animation: fadeIn 0.3s ease-in forwards;
        animation-delay: 0.6s; /* Задержка в 2 секунды перед запуском анимации */
    }
    
    header{
        opacity: 0;
        animation: fadeIn 0.3s ease-in forwards;
        animation-delay: 0.6s; /* Задержка в 2 секунды перед запуском анимации */
    }
    
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    } 
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)