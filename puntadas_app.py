
import streamlit as st
from PIL import Image
import numpy as np
import cv2

st.set_page_config(page_title="Calculadora de Puntadas con Detección Automática", layout="centered")

st.markdown(
    """
    <style>
        .stApp {
            background-color: #000000;
        }
        h1, h2, h3, p, label, div {
            color: #ffffff !important;
        }
        .stButton>button {
            background-color: #00ffe1;
            color: black;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧵 Calculadora de Puntadas con Eliminación Automática de Fondo")

uploaded_file = st.file_uploader("📤 Sube tu imagen de bordado (con fondo blanco)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)
    st.image(image, caption="Imagen original", use_container_width=True)

    # Convertir a HSV para eliminar fondo blanco automáticamente
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    lower_white = np.array([0, 0, 200], dtype=np.uint8)
    upper_white = np.array([180, 40, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    mask_inv = cv2.bitwise_not(mask)

    # Mostrar imagen sin fondo blanco
    result = cv2.bitwise_and(img_np, img_np, mask=mask_inv)
    st.image(result, caption="Fondo eliminado automáticamente", use_container_width=True)

    # Calcular área útil
    area_util = np.count_nonzero(mask_inv)
    total_area = mask.shape[0] * mask.shape[1]
    porcentaje_util = area_util / total_area

    # Ingreso de medidas
    st.subheader("📐 Tamaño real del bordado")
    col1, col2 = st.columns(2)
    with col1:
        ancho_cm = st.number_input("Ancho (cm)", min_value=1.0, value=10.0, step=0.1)
    with col2:
        alto_cm = st.number_input("Alto (cm)", min_value=1.0, value=5.0, step=0.1)

    if st.button("🧮 Calcular puntadas y precio"):
        area_total = ancho_cm * alto_cm
        area_util_real = area_total * porcentaje_util
        puntadas = int(area_util_real * 300)
        precio = round((puntadas / 1000) * 1.8, 2)

        st.markdown(f"### 🔢 Puntadas estimadas: **{puntadas:,}**")
        st.markdown(f"💰 Precio estimado: **${precio} MXN**")
        st.caption(f"Área útil detectada: {porcentaje_util*100:.2f}% del total")

# Enlace de contacto
st.markdown("---")
st.markdown(
    '<a href="https://wa.me/523328129376" target="_blank" style="color:#00ffe1; text-decoration:none; font-size:18px;">📱 Contáctanos por WhatsApp</a>',
    unsafe_allow_html=True
)
