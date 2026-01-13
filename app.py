import streamlit as st
import requests
import io
from PIL import Image


st.set_page_config(page_title="IA Image Generator", page_icon="🎨", layout="centered")

# URL del modelo en Hugging Face (FLUX.1 es rápido y gratuito)
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

def query_hugging_face(prompt, api_token):

    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {"inputs": prompt}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code != 200:

        if response.status_code == 503:
            st.warning("El modelo está iniciando en los servidores de Hugging Face. Reintenta en 10-20 segundos.")
        raise Exception(f"Error {response.status_code}: {response.text}")
        
    return response.content

# --- INTERFAZ DE USUARIO ---
st.title("🎨 AI Text-to-Image Generator")
st.write("Convierte tus descripciones en imágenes usando Inteligencia Artificial.")

# Barra lateral para el Token (Seguridad)
with st.sidebar:
    st.header("Configuración de API")
    st.markdown("[Obtén tu Token de Hugging Face aquí](https://huggingface.co/settings/tokens)")
    hf_token = st.text_input("Ingresa tu HF Token (hf_...)", type="password")
    st.divider()

# Ejemplos de prompts para ayudar al usuario
st.subheader("¿Qué quieres crear hoy?")
col1, col2 = st.columns(2)
with col1:
    if st.button("🏙️ Ciudad Cyberpunk"):
        st.session_state.prompt = "A futuristic cyberpunk city with neon signs and rain, 8k resolution, highly detailed"
with col2:
    if st.button("🐱 Gato Astronauta"):
        st.session_state.prompt = "A cute fluffy cat wearing a space suit on Mars, digital art, cinematic lighting"

# Entrada de texto del usuario
user_prompt = st.text_area("Escribe tu descripción en inglés para mejores resultados:", 
                            value=st.session_state.get('prompt', ''),
                            placeholder="Ejemplo: An oil painting of a sunset over a calm lake")

# Botón principal
if st.button("Generar Imagen ✨"):
    if not hf_token:
        st.error("⚠️ Por favor, ingresa tu Token de Hugging Face en la barra lateral.")
    elif not user_prompt:
        st.warning("⚠️ Escribe una descripción antes de generar.")
    else:
        try:
            with st.spinner("La IA está trabajando en tu imagen..."):
                # Llamada a la API
                image_bytes = query_hugging_face(user_prompt, hf_token)
                
                # Procesamiento de la imagen
                image = Image.open(io.BytesIO(image_bytes))
                
                # Mostrar imagen en pantalla
                st.image(image, caption="Imagen generada con éxito", use_container_width=True)
                
                # Preparar descarga
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="Descargar Imagen 💾",
                    data=byte_im,
                    file_name="ai_image.png",
                    mime="image/png"
                )
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

st.divider()
st.caption("Desarrollado con Streamlit y Hugging Face Inference API.")