
import streamlit as st
from PIL import Image
import numpy as np
import cv2

st.set_page_config(page_title="Calculadora Inteligente de Puntadas", layout="centered")

st.markdown(
    """
    <style>
        .stApp {
            background-color: #000000;
        }
        h1, h2, h3, label, .stMarkdown, .stTextInput, .stNumberInput label, .stSelectbox label {
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

st.title("🧵 Calculadora de Puntadas con IA (Área Útil Detectada)")

uploaded_file = st.file_uploader("📤 Sube tu logo con fondo blanco o transparente", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Vista previa del diseño", use_container_width=True)

    # Convertir a imagen OpenCV
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Invertir la imagen para que el fondo blanco sea 0 y el diseño sea 1
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Calcular porcentaje de área útil
    area_util = np.count_nonzero(mask)
    total_area = mask.shape[0] * mask.shape[1]
    porcentaje_util = area_util / total_area

    st.markdown(f"🔍 Área útil detectada: **{porcentaje_util*100:.2f}%** del total de la imagen")

    # Entrada de tamaño real
    st.markdown("### 📐 Ingresa el tamaño real del bordado")
    col1, col2 = st.columns(2)
    with col1:
        ancho_cm = st.number_input("Ancho (cm)", min_value=1.0, value=10.0, step=0.1)
    with col2:
        alto_cm = st.number_input("Alto (cm)", min_value=1.0, value=5.0, step=0.1)

    if st.button("🧮 Calcular puntadas"):
        area = ancho_cm * alto_cm

        # Lógica automática según área
        if area < 30:
            tipo = "Solo contorno"
            densidad = 80
        elif area < 70:
            tipo = "Relleno medio"
            densidad = 200
        else:
            tipo = "Relleno completo"
            densidad = 300

        puntadas = int(area * densidad * porcentaje_util)
        precio = round((puntadas / 1000) * 1.8, 2)

        st.markdown(f"### ✨ Resultado estimado con IA:")
        st.success(f"🔢 **{puntadas:,} puntadas** para un área útil de **{porcentaje_util*100:.2f}%**")
        st.info(f"Tipo de cobertura detectada: **{tipo}**")
        st.markdown(f"💰 **Precio estimado del bordado:** ${precio} MXN")

# WhatsApp contacto
st.markdown("---")
st.markdown(
    '<a href="https://wa.me/523328129376" target="_blank" style="color:#00ffe1; text-decoration:none; font-size:18px;">📱 Contáctanos por WhatsApp</a>',
    unsafe_allow_html=True
)
