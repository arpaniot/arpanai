import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. Page Configuration & Custom CSS for Neon Theme and Flawless Mobile View
st.set_page_config(page_title="ARPAN AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    /* Chat Bubble Styling */
    .user-bubble {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    .ai-bubble {
        background: rgba(0, 255, 204, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 204, 0.2);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 0 0 10px rgba(0, 255, 204, 0.1);
    }
    /* Mobile responsive adjustments for the bottom input container */
    div[data-testid="stForm"] {
        border: 1px solid rgba(0, 255, 204, 0.3) !important;
        border-radius: 12px !important;
        background-color: #161A24 !important;
    }
    </style>
""", unsafe_allowed_html=True)

# 2. Secure API Key Setup (Configured in Streamlit Secrets later)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Please configure your GEMINI_API_KEY in the Streamlit Secrets manager.")
    st.stop()

# 3. Private Session State Handling (No shared chat history!)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header Layout
st.title("🤖 ARPAN AI")
st.caption("First-Year IoT Engineering Project | Private & Multimodal")
st.write("---")

# 4. Display Chat History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'><b>You:</b><br>{msg['text']}</div>", unsafe_allowed_html=True)
        if msg.get("image"):
            st.image(msg["image"], caption="Uploaded Image", width=250)
    else:
        st.markdown(f"<div class='ai-bubble'><b>ARPAN AI:</b><br>{msg['text']}</div>", unsafe_allowed_html=True)

st.write("") # Spacer

# 5. Fixed Mobile Input Form (Keeps prompt visible on phones)
with st.form(key="chat_form", clear_on_submit=True):
    user_image = st.file_uploader("Upload an image for ARPAN AI to see...", type=["jpg", "jpeg", "png"])
    user_text = st.text_input("Type your message here...", placeholder="Ask me anything...")
    submit_button = st.form_submit_button(label="Send Message")

# 6. Process Input & Call Multimodal Gemini API
if submit_button and (user_text or user_image):
    # Save user message to local private history
    current_msg = {"role": "user", "text": user_text, "image": None}
    
    # Process image if uploaded
    img_obj = None
    if user_image is not None:
        img_bytes = user_image.read()
        img_obj = Image.open(io.BytesIO(img_bytes))
        current_msg["image"] = img_obj
        
    st.session_state.messages.append(current_msg)
    
    # Rerender screen to show user message instantly
    st.rerun()

# Generate AI response if the last message is from user
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_msg = st.session_state.messages[-1]
    
    with st.spinner("ARPAN AI is thinking..."):
        try:
            # Using the fast, multimodal gemini-2.5-flash model
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            # Prepare contents payload
            contents = []
            if last_msg["text"]:
                contents.append(last_msg["text"])
            if last_msg["image"]:
                contents.append(last_msg["image"])
                
            # Default prompt if text is empty but image exists
            if not last_msg["text"] and last_msg["image"]:
                contents.append("Describe and analyze this image in detail.")

            # Request generation
            response = model.generate_content(contents)
            ai_text = response.text
            
        except Exception as e:
            ai_text = f"Error processing request: {str(e)}"
            
    # Save and display AI response privately
    st.session_state.messages.append({"role": "model", "text": ai_text})
    st.rerun()
              
