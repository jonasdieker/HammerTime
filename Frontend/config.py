"""
Configuration, constants, and session state initialization
"""
import streamlit as st

# Product data (simulating CSV)
PRODUCTS = [
    {"id": "C001", "name": "Screw A", "description": "M4×20 stainless", "category": "Fasteners", "price": 0.03, "supplier": "Supplier A", "icon": "🔩"},
    {"id": "C002", "name": "Screw B", "description": "M4×25 stainless", "category": "Fasteners", "price": 0.04, "supplier": "Supplier A", "icon": "🔩"},
    {"id": "C003", "name": "Screw C", "description": "M5×30 zinc", "category": "Fasteners", "price": 0.05, "supplier": "Supplier B", "icon": "🔩"},
    {"id": "C004", "name": "Washer", "description": "for M4", "category": "Fasteners", "price": 0.01, "supplier": "Supplier B", "icon": "⚙️"},
    {"id": "C005", "name": "Wall Plugs", "description": "6mm (Box 100)", "category": "Fasteners", "price": 10.00, "supplier": "Fischer", "icon": "🔧"},
    {"id": "C006", "name": "Work Gloves", "description": "Size 9", "category": "PPE", "price": 2.50, "supplier": "Uvex", "icon": "🧤"},
]

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Order Settings
AUTO_APPROVAL_LIMIT = 1000  # Orders above this amount (EUR) require manual approval
ADMIN_PASSWORD = "admin123"  # Password required for orders over limit


def init_session_state():
    """Initialize all session state variables"""
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'orders' not in st.session_state:
        st.session_state.orders = []
    if 'reports' not in st.session_state:
        st.session_state.reports = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if 'voice_text' not in st.session_state:
        st.session_state.voice_text = ""
    if 'voice_raw_text' not in st.session_state:
        st.session_state.voice_raw_text = ""
    if 'voice_recommendation' not in st.session_state:
        st.session_state.voice_recommendation = None
    if 'image_search' not in st.session_state:
        st.session_state.image_search = None
    if 'recommendation' not in st.session_state:
        st.session_state.recommendation = None
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'last_search_query' not in st.session_state:
        st.session_state.last_search_query = ""
    if 'cart_version' not in st.session_state:
        st.session_state.cart_version = 0
    # Voice Chat Flow state
    if 'voice_chat_messages' not in st.session_state:
        st.session_state.voice_chat_messages = []  # List of {"role": "user"|"assistant", "content": "..."}
    if 'voice_chat_recommendations' not in st.session_state:
        st.session_state.voice_chat_recommendations = None  # Final recommendations from AI

