
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Calculadora de Puntadas", layout="centered")

st.title("🧵 Estimador de Puntadas para Bordado")
st.markdown("Sube tu imagen de bordado, indica el tamaño real y selecciona el tipo de cobertura.")

uploaded_file = st.file_uploader("📤 Sube tu logo o imagen", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen subida", use_column_width=True)

col1, col2 = st.columns(2)
with col1:
    ancho_cm = st.number_input("Ancho del bordado (cm)", min_value=1.0, value=10.0, step=0.1)
with col2:
    alto_cm = st.number_input("Alto del bordado (cm)", min_value=1.0, value=5.0, step=0.1)

tipo = st.selectbox("Tipo de cobertura del bordado", [
    "Relleno completo (300 puntadas/cm²)",
    "Relleno medio (200 puntadas/cm²)",
    "Solo contorno (80 puntadas/cm²)"
])

if st.button("Calcular puntadas"):
    area = ancho_cm * alto_cm
    densidad = 300 if "completo" in tipo else 200 if "medio" in tipo else 80
    puntadas = int(area * densidad)

    st.success(f"🧮 Estimación: **{puntadas:,} puntadas** para un área de {area:.2f} cm².")
    st.markdown("---")
    st.markdown("Este es un valor aproximado. Para resultados precisos, usar software como Wilcom.")
