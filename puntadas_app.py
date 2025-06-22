
import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: white;'>🧵 Calculadora de Puntadas</h1>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Sube tu imagen de bordado", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    # Convertimos a espacio de color HSV
    hsv = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)

    # Definimos rango para eliminar fondo blanco
    lower_white = np.array([0, 0, 200], dtype=np.uint8)
    upper_white = np.array([180, 40, 255], dtype=np.uint8)

    # Crear máscara y eliminar fondo
    mask = cv2.inRange(hsv, lower_white, upper_white)
    result = cv2.bitwise_and(image_np, image_np, mask=cv2.bitwise_not(mask))

    st.image(result, caption="Imagen sin fondo blanco", use_container_width=True)

    # Escala de relleno
    st.subheader("Seleccione la cantidad de relleno")
    relleno = st.radio(
        "", 
        ["Bajo (300)", "Medio (450)", "Alto (650)"],
        horizontal=True
    )

    if relleno == "Bajo (300)":
        puntadas_por_cm2 = 300
    elif relleno == "Medio (450)":
        puntadas_por_cm2 = 450
    else:
        puntadas_por_cm2 = 650

    ancho = st.number_input("Ancho (cm)", min_value=1.0, value=10.0)
    alto = st.number_input("Alto (cm)", min_value=1.0, value=5.0)

    if st.button("Calcular puntadas"):
        area = ancho * alto
        puntadas = int(area * puntadas_por_cm2)
        precio = round((puntadas / 1000) * 1.8, 2)

        st.success(f"🔢 Puntadas estimadas: {puntadas}")
        st.info(f"💲 Precio estimado del bordado: ${precio}")
