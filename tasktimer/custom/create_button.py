import streamlit as st

def import_create_button_styles():
    # Добавляем кастомные стили
    st.markdown("""
            <style>
            .element-container:has(style) {
                display: none;
            }
            #button-create {
                display: none;
            }
            .element-container:has(#button-create) {
                display: none;
            }
            .element-container:has(#button-create) + div button {
                background-color: orange;
                width: 100px;
                height: 100px;
                border-radius: 50%;
                border: none;
                cursor: pointer;
                transition: background 0.3s ease;
    
                /* Анимация пульсации */
                animation: pulse 1.5s infinite ease-in-out;
            }
    
            /* Анимация пульсации */
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); } /* Увеличение на 15% */
                100% { transform: scale(1); }
            }
    
            .element-container:has(#button-create) + div button p {
                color: white !important;
                font-size: 18px;
            }
    
            .element-container:has(#button-create) + div button:hover {
                background-color: red;
            }
            </style> """, unsafe_allow_html=True)

    # Добавляем скрытый элемент перед кнопкой
    st.markdown('<span id="button-create"></span>', unsafe_allow_html=True)