import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. Page Configuration & Futuristic UI Architecture
st.set_page_config(page_title="⚡ ARPAN AI MATRIX", page_icon="🔮", layout="centered")

# Master Passcode Configuration
MASTER_PREMIUM_CODE = "IOT_ARPAN_2026"

# Advanced Responsive CSS for Cyberpunk / Premium Mobile Layout
st.markdown("""
    <style>
    /* Dark Sci-Fi Canvas Background */
    .stApp {
        background-color: #05070F;
        background-image: radial-gradient(circle at 50% 10%, #150F30 0%, #05070F 80%);
        color: #E2E8F0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Dynamic Glowing Top Beam */
    .neon-bar {
        height: 4px;
        background: linear-gradient(90deg, #00f2fe 0%, #7928ca 50%, #00ffcc 100%);
        box-shadow: 0 0 20px #00f2fe, 0 0 30px #7928ca;
        border-radius: 10px;
        margin-bottom: 25px;
    }

    /* System Status Badges */
    .status-badge-locked {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        color: #f87171;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1px;
        float: right;
    }
    .status-badge-unlocked {
        background: rgba(0, 255, 204, 0.1);
        border: 1px solid #00ffcc;
        color: #00ffcc;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1px;
        float: right;
        box-shadow: 0 0 10px rgba(0, 255, 204, 0.2);
    }

    /* Chat Elements with Frosted Glassmorphism */
    .user-bubble {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 14px 18px;
        border-radius: 20px 20px 4px 20px;
        margin-bottom: 16px;
        max-width: 88%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    .ai-bubble {
        background: rgba(0, 255, 204, 0.02);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 204, 0.22);
        padding: 14px 18px;
        border-radius: 20px 20px 20px 4px;
        margin-bottom: 20px;
        max-width: 88%;
        margin-right: auto;
        box-shadow: 0 4px 20px rgba(0, 255, 204, 0.04);
    }
    
    .sender-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
        display: block;
    }
    .user-label { color: #38bdf8; font-weight: 600; }
    .ai-label { color: #00ffcc; font-weight: 700; text-shadow: 0 0 8px rgba(0, 255, 204, 0.3); }

    /* Core Control Panels */
    div[data-testid="stForm"] {
        border: 1px solid rgba(121, 40, 202, 0.3) !important;
        border-radius: 24px !important;
        background: rgba(10, 15, 30, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5) !important;
        padding: 18px !important;
    }
    
    /* Cyberpunk Interactive Button */
    button[data-testid="stFormSubmitButton"] {
        background: linear-gradient(90deg, #7928ca 0%, #00f2fe 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        border: none !important;
        border-radius: 14px !important;
        width: 100% !important;
        box-shadow: 0 0 15px rgba(121, 40, 202, 0.4) !important;
        height: 45px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. API Key Deployment Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("SYSTEM CRISIS: API Key is unconfigured in Secrets.")
    st.stop()

# 3. Persistent State Architectures
if "messages" not in st.session_state:
    st.session_state.messages = []
if "premium_unlocked" not in st.session_state:
    st.session_state.premium_unlocked = False

# UI Title Framework
st.markdown("<div class='neon-bar'></div>", unsafe_allow_html=True)

# 4. Premium Code Authorization Panel
with st.expander("🔑 ENTER PREMIUM ACCESS CODE(Get from Arpan)", expanded=not st.session_state.premium_unlocked):
    input_code = st.text_input("Enter code to unlock Multimodal/Matrix protocols:", type="password", placeholder="••••••••")
    if input_code:
        if input_code == MASTER_PREMIUM_CODE:
            st.session_state.premium_unlocked = True
            st.success("⚡ CORE UPGRADED: Premium Multimodal & Variant Engine unlocked!")
            st.toast("Access Granted. All systems online.", icon="🔓")
        else:
            st.session_state.premium_unlocked = False
            st.sidebar.error("ACCESS DENIED: Invalid Authentication Token.")

# Header Status Generation
if st.session_state.premium_unlocked:
    st.markdown("<span class='status-badge-unlocked'>👑 APEX VIP ACTIVE</span>", unsafe_allow_html=True)
else:
    st.markdown("<span class='status-badge-locked'>🔒 STANDARD TEXT MODE</span>", unsafe_allow_html=True)

st.markdown("<h1 style='margin-top:0px; margin-bottom:0px; color:#ffffff; font-weight:800;'>🔮 ARPAN AI <span style='color:#00ffcc;'>PRO</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#475569; font-size:0.8rem; letter-spacing:1px; margin-bottom:20px;'>QUANTUM INTERFACE // CORE V3.5 MULTI-MATRIX</p>", unsafe_allow_html=True)
st.write("---")

# 5. Live Streamlit Chat Feed
st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'><span class='sender-label user-label'>▲ SECURE USER</span>{msg['text']}</div>", unsafe_allow_html=True)
        if msg.get("image"):
            st.image(msg["image"], use_container_width=True)
    else:
        st.markdown(f"<div class='ai-bubble'><span class='sender-label ai-label'>◆ {msg['core_label']}</span>{msg['text']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 6. Dynamic Main Console
with st.form(key="chat_form", clear_on_submit=True):
    user_text = st.text_input("Transmit message stream...", placeholder="Ask something brilliant...", key="input_field")
    
    # The magical gatekeeper logic: Unlocks completely when passcode verified
    user_image = None
    ai_mode = "Standard Assistant" # Default
    
    if st.session_state.premium_unlocked:
        st.markdown("<p style='color:#00ffcc; font-size:0.75rem; font-weight:600; margin-top:10px; margin-bottom: 2px;'>✨ PREMIUM CORE VECTOR MATRIX ACTIVE:</p>", unsafe_allow_html=True)
        
        # 3-Dot Dropdown box simulation for system settings
        ai_mode = st.selectbox(
            "Select AI Processing Core Matrix (⋮)", 
            ["Jarvis Matrix Protocols", "Savage Core (Extreme Roast Mode)", "Standard AI Engine"]
        )
        
        st.markdown("<p style='color:#7928ca; font-size:0.75rem; font-weight:600; margin-top:5px; margin-bottom: -5px;'>📸 INJECT VISUAL DATA STREAM:</p>", unsafe_allow_html=True)
        user_image = st.file_uploader("", type=["jpg", "jpeg", "png"])
    else:
        st.markdown("<p style='color:#64748B; font-size:0.7rem; font-style:italic; text-align:center; margin-top:10px;'>Unlock Premium mode above to activate the 3 Different Engine Selector & Vision Vectoring.</p>", unsafe_allow_html=True)
        
    submit_button = st.form_submit_button(label="EXECUTE TRANS-CODELINK")

# 7. Heavy Computational Request Handlers
if submit_button and (user_text or user_image):
    current_msg = {"role": "user", "text": user_text, "image": None}
    
    if user_image is not None:
        img_bytes = user_image.read()
        img_obj = Image.open(io.BytesIO(img_bytes))
        current_msg["image"] = img_obj
        
    st.session_state.messages.append(current_msg)
    
    # Store the selected AI core mode into session state so processing script remembers it
    st.session_state.active_core = ai_mode
    st.rerun()

# Processing Engine Threads
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_msg = st.session_state.messages[-1]
    
    # Read active processing persona or fallback to Standard
    chosen_engine = st.session_state.get("active_core", "Standard AI Engine")
    
    with st.spinner("Compiling structural vectors..."):
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            contents = []
            
            # System Persona Injection based on chosen core switch
            if chosen_engine == "Jarvis Matrix Protocols":
                display_label = "JARVIS PROTOCOL"
                persona_prompt = "You are JARVIS, an ultra-advanced, brilliant, polite AI assistant. Address the user respectfully as Sir. Keep responses highly technical, efficient, and sophisticated."
            elif chosen_engine == "Savage Core (Extreme Roast Mode)":
                display_label = "SAVAGE ROAST CORE"
                persona_prompt = "You are a savage, highly sarcastic, funny AI. Roast the user's prompt heavily with absolute wits, dark humor, and playful mockery. Do not be generic."
            else:
                display_label = "ARPAN CORE"
                persona_prompt = "You are a premium, highly responsive AI assistant built for Arpan's engineering project."
            
            # Append prompt instructions first to force persona behavior
            contents.append(persona_prompt)

            if last_msg["text"]:
                contents.append(last_msg["text"])
            if last_msg["image"]:
                contents.append(last_msg["image"])
                
            if not last_msg["text"] and last_msg["image"]:
                contents.append("Analyze and map out this visual matrix completely based on your current persona configuration.")

            response = model.generate_content(contents)
            ai_text = response.text
            
        except Exception as e:
            ai_text = f"CRITICAL CONSOLE ERROR: {str(e)}"
            display_label = "ERROR VECTOR"
            
    st.session_state.messages.append({"role": "model", "text": ai_text, "core_label": display_label})
    st.rerun()
            
