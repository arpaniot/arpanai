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
    
