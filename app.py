import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import json

# 1. Page Configuration & Advanced Cyberpunk Sidebar UI Architecture
st.set_page_config(page_title="⚡ ARPAN AI OMNI", page_icon="🔮", layout="centered", initial_sidebar_state="collapsed")

# Master Passcode Configuration
MASTER_PREMIUM_CODE = "IOT_ARPAN_2026"

# Advanced Responsive CSS for Sidebar Navigation and Glassmorphism
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

    /* Cyberpunk Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #090D1A !important;
        border-right: 1px solid rgba(0, 255, 204, 0.15) !important;
        box-shadow: 5px 0 25px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Sliding History Item Styling */
    .history-item {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s ease;
    }
    .history-item:hover {
        background: rgba(0, 255, 204, 0.05);
        border-color: rgba(0, 255, 204, 0.3);
        transform: translateX(4px);
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

# 3. Persistent LocalStorage State Handling (Simulated Session Architecture)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "premium_unlocked" not in st.session_state:
    st.session_state.premium_unlocked = False

# Load history structure from Streamlit's internal cache framework acting as local cache
if "global_history" not in st.session_state:
    st.session_state.global_history = {}

# 4. SIDEBAR CHAT MATRIX (Left sliding panel like ChatGPT/Gemini)
with st.sidebar:
    st.markdown("<h3 style='color:#00ffcc; font-weight:800; letter-spacing:1px; margin-bottom:5px;'>🔮 TIME MATRIX</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#475569; font-size:0.75rem; margin-bottom:20px;'>CHRONOLOGICAL PROMPT VECTORS</p>", unsafe_allow_html=True)
    st.write("---")
    
    if st.button("➕ CLEAR ACTIVE TERMINAL STREAM", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.write("")
    st.markdown("<p style='color:#64748B; font-size:0.8rem; font-weight:600;'>PAST ENCRYPTED LOGS:</p>", unsafe_allow_html=True)
    
    # Render saved prompt links with sliding animated list styling
    keys_to_delete = []
    for idx, old_msg in enumerate(st.session_state.messages):
        if old_msg["role"] == "user":
            short_text = old_msg["text"][:18] + "..." if len(old_msg["text"]) > 18 else old_msg["text"]
            if not short_text.strip(): short_text = "Visual Data Vector"
            
            # Sidebar container layout for text alignment and custom button deletion
            col_text, col_del = st.columns([4, 1])
            with col_text:
                st.markdown(f"<div class='history-item'>💬 {short_text}</div>", unsafe_allow_html=True)
            with col_del:
                if st.button("🗑️", key=f"del_{idx}"):
                    keys_to_delete.append(idx)
                    
    # Execute deletion logic instantly if trash icon triggered
    if keys_to_delete:
        for index in sorted(keys_to_delete, reverse=True):
            # Remove the user message and corresponding AI response block right after it
            if index < len(st.session_state.messages):
                st.session_state.messages.pop(index)
                if index < len(st.session_state.messages) and st.session_state.messages[index]["role"] == "model":
                    st.session_state.messages.pop(index)
        st.rerun()

# UI Main Title Framework
st.markdown("<div class='neon-bar'></div>", unsafe_allow_html=True)

# 5. Premium Code Authorization Panel
with st.expander("🔑 ENTER APEX PREMIUM ACCESS CODE(Get from Arpan)", expanded=not st.session_state.premium_unlocked):
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

st.markdown("<h1 style='margin-top:0px; margin-bottom:0px; color:#ffffff; font-weight:800;'>🔮 ARPAN AI <span style='color:#00ffcc;'>OMNI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#475569; font-size:0.8rem; letter-spacing:1px; margin-bottom:20px;'>QUANTUM INTERFACE // PERSISTENT OMNI-CORE v4.0</p>", unsafe_allow_html=True)
st.write("---")

# Inform user about the new sliding history panel
st.caption("💡 Click the small arrow icon ( ＞ ) at the top-left of your phone screen to toggle your sliding History Panel & individual log removal systems.")

# 6. Live Streamlit Chat Feed
st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'><span class='sender-label user-label'>▲ SECURE USER</span>{msg['text']}</div>", unsafe_allow_html=True)
        if msg.get("image"):
            st.image(msg["image"], use_container_width=True)
    else:
        st.markdown(f"<div class='ai-bubble'><span class='sender-label ai-label'>◆ {msg['core_label']}</span>{msg['text']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 7. Dynamic Main Console Input
with st.form(key="chat_form", clear_on_submit=True):
    user_text = st.text_input("Transmit message stream...", placeholder="Ask something brilliant...", key="input_field")
    
    user_image = None
    ai_mode = "Standard Assistant"
    
    if st.session_state.premium_unlocked:
        st.markdown("<p style='color:#00ffcc; font-size:0.75rem; font-weight:600; margin-top
                
