import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from sklearn.ensemble import RandomForestClassifier

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & ENTERPRISE DARK THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BioSyncAI | Enterprise Intelligence Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force dark theme across header, body, sidebar, and all container components
st.markdown("""
    <style>
    /* Main App Backgrounds */
    .stApp, [data-testid="stHeader"], [data-testid="stSidebar"] {
        background-color: #04080e !important;
        color: #e2e8f0 !important;
    }
    
    /* Sidebar Specific Styling */
    section[data-testid="stSidebar"] {
        background-color: #0d1520 !important;
        border-right: 1px solid #1e293b;
    }

    /* Cards & Container Elements */
    .stMetric, div[data-testid="stExpander"] {
        background-color: #0d1520 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
    }

    /* Inputs, Selectboxes, and Text Areas */
    input, textarea, select, div[data-baseweb="select"] {
        background-color: #0d1520 !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
    }

    /* Primary Buttons (Lime Accent like Cropin) */
    .stButton>button {
        background: linear-gradient(135deg, #84cc16 0%, #65a30d 100%) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 48px !important;
        font-size: 16px !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #a3e635 0%, #84cc16 100%) !important;
        color: #000000 !important;
    }

    /* Custom Header Cards */
    .cropin-header {
        color: #84cc16;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .partner-card {
        background-color: #0d1520;
        border-left: 4px solid #84cc16;
        padding: 20px;
        border-radius: 8px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)
