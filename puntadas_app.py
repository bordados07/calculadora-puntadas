
import streamlit as st
from PIL import Image

st.set_page_config(page_title="GDL Bordados - Calculadora de Puntadas", layout="centered")

# CSS personalizado para estilos elegantes
st.markdown(
    """
    <style>
        body {
            background-color: #111111;
            color: #ffffff;
        }
        .stApp {
            background-color: #111111;
        }
        h1, h2, h3, .stMarkdown {
            color: #FFCC00;
        }
        .stButton>button {
            background-color: #FFCC00;
            color: black;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Mostrar el logo centrado
st.image("https://raw.githubusercontent.com/bordados07/calculadora-puntadas/main/logo_etikreativo.png", width=150)

st.title("🧵 Calculadora de Puntadas")
st.markdown("Sube tu imagen de bordado, indica el tamaño real y obtendrás una estimación automática de puntadas con base en el área.")

# Subir imagen
uploaded_file = st.file_uploader("📤 Sube tu logo o imagen", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Vista previa del diseño", use_column_width=True)

# Tamaño del bordado
st.markdown("### 📐 Tamaño estimado del bordado")
col1, col2 = st.columns(2)
with col1:
    ancho_cm = st.number_input("Ancho (cm)", min_value=1.0, value=10.0, step=0.1)
with col2:
    alto_cm = st.number_input("Alto (cm)", min_value=1.0, value=5.0, step=0.1)

if st.button("🧮 Calcular puntadas"):
    area = ancho_cm * alto_cm

    # Lógica automática según el tamaño
    if area < 30:
        tipo = "Solo contorno"
        densidad = 80
    elif area < 70:
        tipo = "Relleno medio"
        densidad = 200
    else:
        tipo = "Relleno completo"
        densidad = 300

    puntadas = int(area * densidad)

    st.markdown(f"### ✨ Resultado estimado:")
    st.success(f"🔢 **{puntadas:,} puntadas** para un área de **{area:.2f} cm²**")
    st.info(f"Tipo de cobertura detectada automáticamente: **{tipo}**")

# WhatsApp contacto
st.markdown("---")
st.markdown(
    '<a href="https://wa.me/523328129376" target="_blank" style="color:#FFCC00; text-decoration:none; font-size:18px;">📱 Contáctanos por WhatsApp</a>',
    unsafe_allow_html=True
)
