
import streamlit as st
from PIL import Image
import numpy as np
import cv2

st.set_page_config(page_title="Calculadora de Puntadas", layout="centered")

st.markdown(
    """
    <style>
        .stApp {
            background-color: black;
            color: white;
            background-image: url("logo_etikreativo.png");
            background-size: 40%;
            background-repeat: no-repeat;
            background-position: center;
        }
        h1, h2, h3, h4, h5, h6, p, label, div {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧵 Calculadora de Puntadas")

st.markdown("Sube tu imagen de bordado, indica el tamaño real y obtendrás una estimación automática de puntadas con base en el área.")

uploaded_file = st.file_uploader("📤 Sube tu logo o imagen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGBA")
    st.image(image, caption="Imagen subida", use_column_width=True)

    st.markdown("## ✂️ Tamaño estimado del bordado")
    col1, col2 = st.columns(2)
    with col1:
        ancho_cm = st.number_input("Ancho del bordado (cm)", min_value=1.0, value=10.0, step=0.1)
    with col2:
        alto_cm = st.number_input("Alto del bordado (cm)", min_value=1.0, value=5.0, step=0.1)

    st.markdown("### 🧶 Selecciona la cantidad de relleno")
    tipo = st.radio("",
        [
            "Bajo (300 puntadas/cm²)",
            "Medio (450 puntadas/cm²)",
            "Alto (650 puntadas/cm²)"
        ]
    )

    tipo_valores = {
        "Bajo (300 puntadas/cm²)": 300,
        "Medio (450 puntadas/cm²)": 450,
        "Alto (650 puntadas/cm²)": 650
    }

    puntadas_por_cm2 = tipo_valores[tipo]
    area_cm2 = ancho_cm * alto_cm
    total_puntadas = int(area_cm2 * puntadas_por_cm2)
    precio = round((total_puntadas / 1000) * 1.8, 2)

    st.markdown("## 📏 Resultado")
    st.success(f"Total estimado de puntadas: {total_puntadas}")
    st.info(f"💰 Precio estimado del bordado: ${precio} MXN")
