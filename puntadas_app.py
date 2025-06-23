
import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="Calculadora de Puntadas", layout="centered")

st.markdown("<h1 style='text-align: center; color: white;'>Calculadora de Puntadas para Bordado</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Sube tu diseño, elige si deseas eliminar el fondo automáticamente o no, y obtén un estimado de puntadas y precio.</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("### ¿Duda con la eliminación de fondo?")
st.markdown("[Haz clic aquí para quitar el fondo manualmente](https://www.iloveimg.com/es/eliminar-fondo)", unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("📤 Sube tu imagen", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGBA")
    image_np = np.array(image)

    st.image(image, caption="🖼️ Imagen original", use_column_width=True)

    metodo = st.radio("¿Deseas quitar el fondo?", ["Automático", "Desactivado"])
    if metodo == "Automático":
        image_gray = cv2.cvtColor(image_np, cv2.COLOR_RGBA2GRAY)
        _, alpha = cv2.threshold(image_gray, 250, 255, cv2.THRESH_BINARY_INV)
        image_np[:, :, 3] = alpha
        st.image(image_np, caption="🧽 Fondo eliminado automáticamente", use_column_width=True)

    elif metodo == "Desactivado":
        st.warning("La imagen se procesará con el fondo incluido.")

    st.markdown("### ✏️ Selecciona la cantidad de relleno")
    nivel = st.radio("Seleccione la cantidad de relleno:", ["Bajo", "Medio", "Alto"])

    if nivel == "Bajo":
        densidad = 300
    elif nivel == "Medio":
        densidad = 450
    else:
        densidad = 650

    alpha_channel = image_np[:, :, 3]
    visible_pixels = np.sum(alpha_channel > 0)

    puntadas_estimadas = int((visible_pixels / 100) * (densidad / 100))
    precio_estimado = (puntadas_estimadas / 1000) * 1.8

    st.success(f"🧵 Puntadas estimadas: {puntadas_estimadas}")
    st.info(f"💸 Precio estimado: ${precio_estimado:.2f} MXN")
