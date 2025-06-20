
import streamlit as st
from PIL import Image
import numpy as np
import cv2
import base64

st.set_page_config(page_title="Calculadora de Puntadas", layout="centered")

# Fondo negro con logo
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://raw.githubusercontent.com/bordados07/calculadora-puntadas/main/vv56545");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

[data-testid="stHeader"], [data-testid="stToolbar"] {{ background: rgba(0,0,0,0); }}

h1, h2, h3, h4, h5, p, label, div {{
    color: white !important;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("🧵 Calculadora de Puntadas")
st.markdown("Sube tu imagen de bordado. Se eliminará automáticamente el fondo claro y se estimará el número de puntadas en base al área.")

uploaded_file = st.file_uploader("📤 Sube tu imagen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Imagen subida")

    ancho_cm = st.number_input("Ancho del bordado (cm)", min_value=1.0, value=10.0, step=0.1)
    alto_cm = st.number_input("Alto del bordado (cm)", min_value=1.0, value=5.0, step=0.1)

    # Convertir a numpy y quitar fondo claro automáticamente
    img_np = np.array(image)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)  # Quitar fondo blanco
    area_util = cv2.countNonZero(mask)

    # Calcular tamaño real
    total_pixels = mask.shape[0] * mask.shape[1]
    proporcion_area = area_util / total_pixels
    area_cm2 = ancho_cm * alto_cm
    area_util_cm2 = area_cm2 * proporcion_area

    puntadas_estimadas = int(area_util_cm2 * 300)
    precio = round((puntadas_estimadas / 1000) * 1.8, 2)

    st.subheader("🧮 Resultados")
    st.markdown(f"🔹 Puntadas estimadas: **{puntadas_estimadas:,}**")
    st.markdown(f"💲 Precio estimado: **${precio} MXN**")

    st.markdown("---")
    st.markdown("[💬 Contáctanos por WhatsApp](https://wa.me/523328129376)", unsafe_allow_html=True)
