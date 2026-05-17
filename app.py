import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. Page Configuration & Cyberpunk Header Injection
st.set_page_config(page_title="⚡ ARPAN AI PRO", page_icon="🔮", layout="centered")

# Advanced Responsive CSS for Premium Mobile UI
st.markdown("""
    <style>
    /* Dark Sci-Fi Background */
    .stApp {
        background-color: #060814;
        background-image: radial-gradient(circle at 50% 0%, #1a103c 0%, #060814 70%);
        color: #E2E8F0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Top Neon Laser Line */
    .neon-bar {
        height: 4px;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #00ffcc 100%);
        box-shadow: 0 0 15px #00f2fe, 0 0 25px #00ffcc;
        border-radius: 10px;
        margin-bottom: 25px;
    }

    /* Glassmorphism Container for Chat */
    .chat-wrapper {
        padding: 5px;
        width: 100%;
    }

    /* User Chat Bubble: Deep Space Blue */
    .user-bubble {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 14px 18px;
        border-radius: 20px 20px 4px 20px;
        margin-bottom: 16px;
        max-width: 88%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        animation: fadeIn 0.3s ease-in-out;
    }

    /* AI Chat Bubble: Glowing Cyan Matrix */
    .ai-bubble {
        background: rgba(0, 255, 204, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 204, 0.25);
        padding: 14px 18px;
        border-radius: 20px 20px 20px 4px;
        margin-bottom: 20px;
        max-width: 88%;
        margin-right: auto;
        box-shadow: 0 4px 20px rgba(0, 255, 204, 0.05), inset 0 0 10px rgba(0, 255, 204, 0.02);
        animation: fadeIn 0.3s ease-in-out;
    }
    
    .sender-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 4px;
        display: block;
    }
    
    .user-label { color: #38bdf8; font-weight: 600; }
    .ai-label { color: #00ffcc; font-weight: 700; text-shadow: 0 0 8px rgba(0, 255, 204, 0.4); }

    /* Premium High-Tech Bottom Input Form */
    div[data-testid="stForm"] {
        border: 1px solid rgba(0, 242, 254, 0.25) !important;
        border-radius: 22px !important;
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
        padding: 15px !important;
        margin-top: 20px;
    }
    
    /* Submit Button Neon Glow styling */
    button[data-testid="stFormSubmitButton"] {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #060814 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        width: 100% !important;
        box-shadow: 0 0 12px rgba(0, 242, 254, 0.4) !important;
        transition: all 0.2s ease !important;
    }
    
    button[data-testid="stFormSubmitButton"]:hover {
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.7) !important;
        transform: scale(1.02);
    }

    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# 2. Secure API Key Setup from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key! Please configure your GEMINI_API_KEY in the Streamlit Secrets manager.")
    st.stop()

# 3. Private Session State Handling
if "messages" not in st.session_state:
    st.session_state.messages = []

# Glowing Header Layout
st.markdown("<div class='neon-bar'></div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-bottom: 0px; color:#ffffff; font-weight:800; letter-spacing: 1px;'>🔮 ARPAN AI <span style='color:#00ffcc;'>PRO</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color:#64748B; font-size:0.85rem; margin-bottom: 25px;'>QUANTUM INTERFACE // CORE V2.5 FLASH</p>", unsafe_allow_html=True)

# 4. Render Chat History inside responsive layout
st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'><span class='sender-label user-label'>▲ SECURE USER</span>{msg['text']}</div>", unsafe_allow_html=True)
        if msg.get("image"):
            st.image(msg["image"], use_container_width=True)
    else:
        st.markdown(f"<div class='ai-bubble'><span class='sender-label ai-label'>◆ ARPAN CORE</span>{msg['text']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 5. Mobile-Optimized Input System at the Bottom
with st.form(key="chat_form", clear_on_submit=True):
    user_text = st.text_input("Execute prompt...", placeholder="Ask something brilliant...", key="input_field")
    user_image = st.file_uploader("Inject Visual Data (Optional)", type=["jpg", "jpeg", "png"])
    submit_button = st.form_submit_button(label="INITIALIZE RESPONSE")

# 6. Run Multimodal API request upon clicking send
if submit_button and (user_text or user_image):
    current_msg = {"role": "user", "text": user_text, "image": None}
    
    if user_image is not None:
        img_bytes = user_image.read()
        img_obj = Image.open(io.BytesIO(img_bytes))
        current_msg["image"] = img_obj
        
    st.session_state.messages.append(current_msg)
    st.rerun()

# Generate response if the last turn belongs to the user
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_msg = st.session_state.messages[-1]
    
    with st.spinner("Decoding quantum vectors..."):
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            contents = []
            
            if last_msg["text"]:
                contents.append(last_msg["text"])
            if last_msg["image"]:
                contents.append(last_msg["image"])
                
            if not last_msg["text"] and last_msg["image"]:
                contents.append("Analyze and map out this visual matrix completely.")

            response = model.generate_content(contents)
            ai_text = response.text
            
        except Exception as e:
            ai_text = f"SYSTEM ERROR: Failed to process request vector. Details: {str(e)}"
            
    st.session_state.messages.append({"role": "model", "text": ai_text})
    st.rerun()
    
