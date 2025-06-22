
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2

st.set_page_config(page_title="Eliminador de Fondo por Color Seleccionado", layout="centered")

st.title("🎯 Elimina el fondo seleccionando un color")
st.markdown("Haz clic en la imagen sobre el color de fondo que quieras eliminar. El sistema detectará ese color y eliminará todos los píxeles similares.")

uploaded_file = st.file_uploader("📤 Sube tu imagen (PNG o JPG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    st.subheader("🖱 Haz clic en el fondo")
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)", 
        stroke_width=1,
        stroke_color="#000000",
        background_image=image,
        update_streamlit=True,
        height=image_np.shape[0],
        width=image_np.shape[1],
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data and canvas_result.json_data["objects"]:
        point = canvas_result.json_data["objects"][-1]  # Último punto marcado
        x = int(point["left"])
        y = int(point["top"])

        st.markdown(f"📍 Coordenada seleccionada: ({x}, {y})")

        selected_color = image_np[y, x]  # RGB
        st.markdown(f"🎨 Color seleccionado: RGB {tuple(selected_color)}")

        # Tolerancia (ajustable)
        tolerance = st.slider("🎚 Tolerancia de color", 5, 100, 30)

        # Crear máscara para eliminar fondo
        lower = np.clip(selected_color - tolerance, 0, 255)
        upper = np.clip(selected_color + tolerance, 0, 255)

        mask = cv2.inRange(image_np, lower, upper)
        mask_inv = cv2.bitwise_not(mask)
        result = cv2.bitwise_and(image_np, image_np, mask=mask_inv)

        st.image(result, caption="🧼 Imagen con fondo eliminado", use_container_width=True)

        # Calcular área útil
        area_util = np.count_nonzero(mask_inv)
        total_area = mask.shape[0] * mask.shape[1]
        porcentaje_util = area_util / total_area

        # Medidas reales
        ancho_cm = st.number_input("Ancho del bordado (cm)", 1.0, 100.0, 10.0, step=0.1)
        alto_cm = st.number_input("Alto del bordado (cm)", 1.0, 100.0, 5.0, step=0.1)

        # Densidad fija o seleccionable
        densidad = st.selectbox("Densidad del bordado (puntadas/cm²)", [300, 450, 650])
        puntadas = int((ancho_cm * alto_cm * porcentaje_util) * densidad)
        precio = round((puntadas / 1000) * 1.8, 2)

        st.markdown(f"### 🔢 Puntadas estimadas: **{puntadas:,}**")
        st.markdown(f"💰 Precio estimado: **${precio} MXN**")
