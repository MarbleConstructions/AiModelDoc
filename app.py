import time
from PIL import Image
import numpy as np
import easyocr
import streamlit as st

st.set_page_config(
    page_title="Mirage",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Syne:wght@400;700;800&display=swap');

        /* Фон с эффектом легкого шума */
        .stApp {
            background-color: #0d0d0d;
            background-image: radial-gradient(#2a2a2a 1px, transparent 1px);
            background-size: 15px 15px;
        }

        /* Базовые стили */
        * {
            font-family: 'Syne', sans-serif;
        }

        h1, h2, h3, h4 {
            font-family: 'Bebas Neue', sans-serif !important;
            letter-spacing: 3px;
            color: #ccff00 !important;
        }

        p, span, div, label {
            color: #e0e0e0 !important;
        }

        /* Кастомная сетка */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1100px;
        }


        .mirage-title-container {
            position: relative;
            margin-bottom: 3rem;
            padding-left: 2rem;
            border-left: 8px solid #8a2be2;
        }

        .mirage-title {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 5rem;
            line-height: 0.9;
            color: #ccff00 !important;
            margin: 0;
            text-transform: uppercase;
        }

        .mirage-subtitle {
            font-family: 'Syne', sans-serif;
            font-size: 1.2rem;
            color: #8a2be2 !important;
            font-weight: 700;
            margin-top: 10px;
            letter-spacing: 2px;
        }


        .skewed-panel {
            background: #1a1a1a;
            border: 1px solid #333;
            padding: 2rem;
            /* Асимметричные углы */
            border-radius: 40px 0 40px 0;
            margin-bottom: 2rem;
            box-shadow: 10px 10px 0px #8a2be2;
            transition: transform 0.3s ease;
        }

        .skewed-panel:hover {
            transform: translate(-5px, -5px);
            box-shadow: 15px 15px 0px #8a2be2;
        }

        /* Зона загрузки */
        div[data-testid="stFileUploader"] {
            background: #0d0d0d;
            border: 2px dashed #ccff00;
            border-radius: 20px;
            padding: 1rem;
        }

        div[data-testid="stFileUploader"] button {
            background-color: #ccff00 !important;
            color: #000 !important;
            border-radius: 0 !important;
            font-family: 'Bebas Neue', sans-serif !important;
            font-size: 1.2rem !important;
            letter-spacing: 1px;
            border: none !important;
        }


        .fragment-box {
            margin-bottom: 1rem;
        }
        
        .fragment {
            background: transparent;
            border-bottom: 1px solid #333;
            padding: 0.8rem 0;
            color: #fff !important;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
        }

        .fragment:nth-child(even) {
            padding-left: 2rem;
            color: #ccff00 !important;
        }

        .fragment:nth-child(odd) {
            padding-left: 0.5rem;
            color: #e0e0e0 !important;
        }

        .fragment-marker {
            color: #8a2be2 !important;
            font-weight: bold;
            margin-right: 15px;
            font-size: 1.2rem;
        }

        /* Скрыть стандартные элементы */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Заголовок
st.markdown(
    """
    <div class="mirage-title-container">
        <div class="mirage-title">Mirage</div>
        <div class="mirage-subtitle">НЕЙРОСЕТЕВОЕ ИСКАЖЕНИЕ РЕАЛЬНОСТИ</div>
    </div>
    """,
    unsafe_allow_html=True
)


@st.cache_resource(show_spinner=False)
def init_mirage():

    time.sleep(1.5) 
    return easyocr.Reader(['ru', 'en'], gpu=False)

engine = init_mirage()


col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.markdown('<div class="skewed-panel">', unsafe_allow_html=True)
    st.markdown("### [1] Вход")
    image_file = st.file_uploader(
        "Выберите документ для анализа",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )
    
    if image_file:
        img = Image.open(image_file)
        st.image(img, use_container_width=True, caption="Исходный объект")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    if image_file:
        st.markdown('<div class="skewed-panel" style="box-shadow: -10px 10px 0px #ccff00;">', unsafe_allow_html=True)
        st.markdown("### [2] Искаженный текст")
        
        with st.spinner("Синтез данных..."):
            img_np = np.array(Image.open(image_file))
            text_data = engine.readtext(img_np, detail=0)
            
        if text_data:
            st.markdown('<div class="fragment-box">', unsafe_allow_html=True)
            for i, text in enumerate(text_data):
                st.markdown(
                    f'<div class="fragment"><span class="fragment-marker">/</span> {text}</div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Сохранение файла
            save_name = f"mirage_{image_file.name}.txt"
            with open(save_name, "w", encoding="utf-8") as f:
                f.write("\n".join(text_data))
                
            st.info(f"Фрагменты сохранены: {save_name}")
        else:
            st.warning("Сбой синтеза. Текст не обнаружен.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div style="text-align: center; margin-top: 4rem; opacity: 0.5;">
                <h2>Ожидание сигнала...</h2>
                <p>Загрузите изображение слева</p>
            </div>
            """,
            unsafe_allow_html=True
        )