import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. Page Configuration & Custom CSS for a Flawless Mobile-First Experience
st.set_page_config(page_title="ARPAN AI", page_icon="🤖", layout="centered")

# Mobile-first styling overrides
st.markdown("""
    <style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0B0E14;
        color: #F0F2F6;
    }
    /* Mobile Responsive Chat Container */
    .chat-container {
        padding: 5px;
        max-width: 100%;
    }
    /* User Chat Bubble */
    .user-bubble {
        background: linear-gradient(135deg, #1E293B, #0F172A);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 12px 16px;
        border-radius: 18px 18px 2px 18px;
        margin-bottom: 12px;
        max-width: 85%;
        margin-left: auto;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    /* AI Chat Bubble with Neon Cyberpunk Glow */
    .ai-bubble {
        background: linear-gradient(135deg, #111827, #1F2937);
        border-left: 3px solid #00FFCC;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 2px;
        margin-bottom: 16px;
        max-width: 85%;
        margin-right: auto;
        box-shadow: 0 2px 8px rgba(0, 255, 204, 0.05);
    }
    /* Clean up form elements for small phone screens */
    div[data-testid="stForm"] {
        border: 1px solid rgba(0, 255, 204, 0.2) !important;
        border-radius: 16px !important;
        background-color: #161B22 !important;
        padding: 10px !important;
    }
    /* Custom spacing for mobile headers */
    .main-title {
        font-size: 2rem !important;
        font-weight: 700;
        color: #00FFCC;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.2);
        margin-bottom: 0px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Secure API Key Setup from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Please configure your GEMINI_API_KEY in the Streamlit Secrets manager.")
    st.stop()

# 3. Private Session State Handling
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header UI Layout
st.markdown("<h1 class='main-title'>🤖 ARPAN AI</h1>", unsafe_allow_html=True)
st.caption("First-Year IoT Engineering Project | Mobile Optimized")
st.write("---")

# 4. Render Chat History inside responsive layout
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'><b>You</b><br>{msg['text']}</div>", unsafe_allow_html=True)
        if msg.get("image"):
            st.image(msg["image"], caption="Uploaded Image", use_container_width=True)
    else:
        st.markdown(f"<div class='ai-bubble'><b>ARPAN AI</b><br>{msg['text']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 5. Mobile-Optimized Input Box at the Bottom
with st.form(key="chat_form", clear_on_submit=True):
    user_text = st.text_input("Type a message...", placeholder="Ask ARPAN AI anything...", key="input_field")
    user_image = st.file_uploader("Upload an image (Optional)", type=["jpg", "jpeg", "png"])
    submit_button = st.form_submit_button(label="Send Message")

# 6. Run API request upon clicking send
if submit_button and (user_text or user_image):
    current_msg = {"role": "user", "text": user_text, "image": None}
    
    img_obj = None
    if user_image is not None:
        img_bytes = user_image.read()
        img_obj = Image.open(io.BytesIO(img_bytes))
        current_msg["image"] = img_obj
        
    st.session_state.messages.append(current_msg)
    st.rerun()

# Generate response if the last turn belongs to the user
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_msg = st.session_state.messages[-1]
    
    with st.spinner("Thinking..."):
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            contents = []
            
            if last_msg["text"]:
                contents.append(last_msg["text"])
            if last_msg["image"]:
                contents.append(last_msg["image"])
                
            if not last_msg["text"] and last_msg["image"]:
                contents.append("Describe and analyze this image in detail.")

            response = model.generate_content(contents)
            ai_text = response.text
            
        except Exception as e:
            ai_text = f"Error processing request: {str(e)}"
            
    st.session_state.messages.append({"role": "model", "text": ai_text})
    st.rerun()
