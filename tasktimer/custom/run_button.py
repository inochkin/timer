import streamlit as st


def import_run_button_style():
    st.markdown("""
            <style>
                /* -------------------- 2
                # Добавляем скрытый элемент перед кнопкой "Run" чтобы кастомизировать Run button.
                    # Добавляем кастомные стили
                ---------------------------*/
                .element-container:has(style) {
                        display: none;
                }
                #button-after3 {
                    display: none;
                }
                .element-container:has(#button-after3) {
                    display: none;
                }
                .element-container:has(#button-after3) + div button {
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

                .element-container:has(#button-after3) + div button p {
                    color: white;
                    font-size: 18px;
                }

                .element-container:has(#button-after3) + div button:hover {
                    background-color: red;
                }
                </style>
                """, unsafe_allow_html=True)
    st.markdown('<span id="button-after3"></span>', unsafe_allow_html=True)

