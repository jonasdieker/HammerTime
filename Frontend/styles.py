"""
CSS Styles for the Procurement Assistant UI - Enhanced Version
"""

ENHANCED_CSS = """
    <style>
    /* ============================================================================
       BASE STYLES & RESETS
    ============================================================================ */
    
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body {
        font-family: 'Inter', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* ============================================================================
       STREAMLIT APP CONTAINER
    ============================================================================ */
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        font-family: 'Inter', sans-serif !important;
        min-height: 100vh;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }
    
    /* ============================================================================
       SIDEBAR ENHANCEMENTS
    ============================================================================ */
    
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.08) !important;
        padding-top: 1rem !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    
    /* ============================================================================
       NAVIGATION & BUTTONS
    ============================================================================ */
    
    /* Main navigation buttons */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: none !important;
        position: relative;
        overflow: hidden;
        font-size: 0.95rem !important;
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(255, 255, 255, 0.5);
        opacity: 0;
        border-radius: 100%;
        transform: scale(1, 1) translate(-50%);
        transform-origin: 50% 50%;
    }
    
    .stButton > button:focus:not(:active)::after {
        animation: ripple 1s ease-out;
    }
    
    @keyframes ripple {
        0% {
            transform: scale(0, 0);
            opacity: 0.5;
        }
        100% {
            transform: scale(20, 20);
            opacity: 0;
        }
    }
    
    /* Primary buttons - Gradient */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(0) !important;
    }
    
    /* Secondary buttons */
    .stButton > button[kind="secondary"] {
        background: white !important;
        color: #667eea !important;
        border: 2px solid #667eea !important;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: rgba(102, 126, 234, 0.05) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* ============================================================================
       CARD DESIGNS
    ============================================================================ */
    
    /* Modern card base */
    .modern-card {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-bottom: 1rem !important;
    }
    
    .modern-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.12) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Product cards */
    .product-card-modern {
        background: white !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        margin-bottom: 0.75rem !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid #e5e7eb !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .product-card-modern:hover {
        border-color: #667eea !important;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15) !important;
        transform: translateY(-2px) !important;
    }
    
    .product-card-modern::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 3px !important;
        background: linear-gradient(90deg, transparent, #667eea, transparent) !important;
        transition: left 0.5s ease !important;
    }
    
    .product-card-modern:hover::before {
        left: 100% !important;
    }
    
    /* ============================================================================
       TYPOGRAPHY & TEXT
    ============================================================================ */
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        margin-bottom: 1rem !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 1.5rem !important;
    }
    
    h2 {
        font-size: 1.75rem !important;
        margin-bottom: 1.25rem !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
    }
    
    /* Paragraphs and text */
    .stMarkdown, p, span, label, div {
        color: #374151 !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.6 !important;
    }
    
    /* Section headers */
    .section-header {
        font-weight: 700 !important;
        color: #1f2937 !important;
        font-size: 1.1rem !important;
        margin-bottom: 1rem !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }
    
    /* ============================================================================
       INPUT FIELDS & FORMS
    ============================================================================ */
    
    /* Text inputs */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #e5e7eb !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* Number inputs */
    .stNumberInput > div > div > input {
        border-radius: 12px !important;
        text-align: center !important;
        border: 2px solid #e5e7eb !important;
        padding: 0.5rem !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Text areas */
    .stTextArea > div > div > textarea {
        border-radius: 12px !important;
        border: 2px solid #e5e7eb !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div > div {
        border-radius: 12px !important;
        border: 2px solid #e5e7eb !important;
    }
    
    .stSelectbox > div > div > div:hover {
        border-color: #667eea !important;
    }
    
    /* File uploader */
    .stFileUploader > div {
        border-radius: 12px !important;
        border: 2px dashed #667eea !important;
        background: rgba(102, 126, 234, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div:hover {
        background: rgba(102, 126, 234, 0.1) !important;
        border-color: #764ba2 !important;
    }
    
    /* ============================================================================
       TABS ENHANCEMENT
    ============================================================================ */
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: transparent !important;
        border-bottom: none !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px !important;
        white-space: pre-wrap !important;
        background-color: white !important;
        border-radius: 12px 12px 0 0 !important;
        gap: 1rem !important;
        padding: 12px 24px !important;
        border: 1px solid #e5e7eb !important;
        border-bottom: none !important;
        font-weight: 600 !important;
        color: #6b7280 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f8fafc !important;
        color: #667eea !important;
        border-color: #667eea !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: #667eea !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* ============================================================================
       CHAT INTERFACE
    ============================================================================ */
    
    /* Chat bubbles */
    .chat-bubble-user {
        margin-left: auto !important;
        margin-right: 0 !important;
        max-width: 75% !important;
        animation: slideInRight 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .chat-bubble-ai {
        margin-right: auto !important;
        margin-left: 0 !important;
        max-width: 75% !important;
        animation: slideInLeft 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(30px) !important;
            opacity: 0 !important;
        }
        to {
            transform: translateX(0) !important;
            opacity: 1 !important;
        }
    }
    
    @keyframes slideInLeft {
        from {
            transform: translateX(-30px) !important;
            opacity: 0 !important;
        }
        to {
            transform: translateX(0) !important;
            opacity: 1 !important;
        }
    }
    
    /* ============================================================================
       VOICE INTERFACE
    ============================================================================ */
    
    .voice-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        color: white !important;
        text-align: center !important;
        margin: 20px 0 !important;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3) !important;
    }
    
    .voice-pulse {
        animation: pulse 2s infinite !important;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7) !important;
        }
        70% {
            box-shadow: 0 0 0 20px rgba(102, 126, 234, 0) !important;
        }
        100% {
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0) !important;
        }
    }
    
    /* ============================================================================
       STATUS INDICATORS & BADGES
    ============================================================================ */
    
    .status-badge {
        display: inline-block !important;
        padding: 4px 12px !important;
        border-radius: 20px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
    }
    
    .status-approved {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
    }
    
    .status-pending {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: white !important;
    }
    
    .status-declined {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
    }
    
    .status-shipped {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: white !important;
    }
    
    /* ============================================================================
       LOADING & PROGRESS
    ============================================================================ */
    
    .loading-spinner {
        display: inline-block !important;
        width: 50px !important;
        height: 50px !important;
        border: 3px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 50% !important;
        border-top-color: #667eea !important;
        animation: spin 1s ease-in-out infinite !important;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg) !important; }
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 4px !important;
    }
    
    /* ============================================================================
       TABLES & DATA DISPLAY
    ============================================================================ */
    
    /* Order tables */
    .order-table {
        width: 100% !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
    }
    
    .order-table th {
        text-align: left !important;
        padding: 1rem !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        border: none !important;
    }
    
    .order-table td {
        padding: 1rem !important;
        border-bottom: 1px solid #f1f5f9 !important;
        color: #374151 !important;
        background: white !important;
        transition: all 0.2s ease !important;
    }
    
    .order-table tr:hover td {
        background: #f8fafc !important;
    }
    
    /* ============================================================================
       METRIC CARDS
    ============================================================================ */
    
    .metric-card {
        background: white !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        border: 1px solid #e5e7eb !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.3s ease !important;
    }
    
    .metric-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08) !important;
        border-color: #667eea !important;
    }
    
    /* ============================================================================
       ANIMATIONS & EFFECTS
    ============================================================================ */
    
    /* Floating animation */
    .float-animation {
        animation: float 3s ease-in-out infinite !important;
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px) !important;
        }
        50% {
            transform: translateY(-10px) !important;
        }
    }
    
    /* Shimmer effect */
    .shimmer {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%) !important;
        background-size: 200% 100% !important;
        animation: shimmer 1.5s infinite !important;
    }
    
    @keyframes shimmer {
        0% {
            background-position: -200% 0 !important;
        }
        100% {
            background-position: 200% 0 !important;
        }
    }
    
    /* Bounce animation */
    .bounce {
        animation: bounce 0.5s !important;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0) !important;
        }
        40% {
            transform: translateY(-10px) !important;
        }
        60% {
            transform: translateY(-5px) !important;
        }
    }
    
    /* Fade in animation */
    .fade-in {
        animation: fadeIn 0.5s ease-in !important;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0 !important;
        }
        to {
            opacity: 1 !important;
        }
    }
    
    /* ============================================================================
       UPLOAD AREAS
    ============================================================================ */
    
    .upload-area {
        border: 2px dashed #667eea !important;
        border-radius: 20px !important;
        padding: 40px !important;
        text-align: center !important;
        background: rgba(102, 126, 234, 0.05) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    
    .upload-area:hover {
        background: rgba(102, 126, 234, 0.1) !important;
        border-color: #764ba2 !important;
        transform: translateY(-2px) !important;
    }
    
    /* ============================================================================
       EXPANDERS & ACCORDIONS
    ============================================================================ */
    
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        color: #374151 !important;
        background: #f8fafc !important;
        border-radius: 12px !important;
        border: 1px solid #e5e7eb !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f1f5f9 !important;
        border-color: #667eea !important;
    }
    
    .streamlit-expanderContent {
        background: white !important;
        border-radius: 0 0 12px 12px !important;
        border: 1px solid #e5e7eb !important;
        border-top: none !important;
        padding: 1.5rem !important;
        margin-top: 0 !important;
    }
    
    /* ============================================================================
       SCROLLBAR STYLING
    ============================================================================ */
    
    ::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1 !important;
        border-radius: 4px !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 4px !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    /* ============================================================================
       HIDE STREAMLIT BRANDING
    ============================================================================ */
    
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    
    /* ============================================================================
       CUSTOM UTILITY CLASSES
    ============================================================================ */
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    /* Glass effect */
    .glass-effect {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Shadow utilities */
    .shadow-sm {
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04) !important;
    }
    
    .shadow-md {
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
    }
    
    .shadow-lg {
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12) !important;
    }
    
    /* Border utilities */
    .border-gradient {
        border: 2px solid transparent !important;
        background: linear-gradient(white, white) padding-box,
                    linear-gradient(135deg, #667eea 0%, #764ba2 100%) border-box !important;
    }
    
    /* ============================================================================
       MOBILE RESPONSIVENESS
    ============================================================================ */
    
    @media (max-width: 768px) {
        .stApp {
            padding: 10px !important;
        }
        
        [data-testid="stSidebar"] {
            width: 100% !important;
            max-width: 100% !important;
            transform: translateX(-100%) !important;
        }
        
        .product-card-modern {
            flex-direction: column !important;
            text-align: center !important;
            gap: 1rem !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            flex-direction: column !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            width: 100% !important;
            border-radius: 12px !important;
            margin-bottom: 8px !important;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
        
        .modern-card {
            padding: 1rem !important;
        }
    }
    
    /* ============================================================================
       DARK MODE SUPPORT
    ============================================================================ */
    
    @media (prefers-color-scheme: dark) {
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
        }
        
        [data-testid="stSidebar"] {
            background: rgba(30, 41, 59, 0.95) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        .modern-card, .product-card-modern, .metric-card {
            background: rgba(30, 41, 59, 0.8) !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
            color: #e2e8f0 !important;
        }
        
        h1, h2, h3, h4, h5, h6, .stMarkdown, p, span, label, div {
            color: #e2e8f0 !important;
        }
        
        .stButton > button[kind="secondary"] {
            background: rgba(30, 41, 59, 0.8) !important;
            color: #cbd5e1 !important;
            border-color: #475569 !important;
        }
        
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: rgba(30, 41, 59, 0.8) !important;
            border-color: #475569 !important;
            color: #e2e8f0 !important;
        }
        
        .order-table td {
            background: rgba(30, 41, 59, 0.8) !important;
            color: #e2e8f0 !important;
            border-color: #475569 !important;
        }
        
        .streamlit-expanderHeader {
            background: rgba(30, 41, 59, 0.8) !important;
            border-color: #475569 !important;
            color: #e2e8f0 !important;
        }
        
        .streamlit-expanderContent {
            background: rgba(30, 41, 59, 0.8) !important;
            border-color: #475569 !important;
            color: #e2e8f0 !important;
        }
        
        ::-webkit-scrollbar-track {
            background: #1e293b !important;
        }
    }
    
    /* ============================================================================
       PRINT STYLES
    ============================================================================ */
    
    @media print {
        [data-testid="stSidebar"],
        .stButton,
        .stFileUploader,
        .stTabs {
            display: none !important;
        }
        
        .stApp {
            background: white !important;
        }
        
        .modern-card, .product-card-modern {
            box-shadow: none !important;
            border: 1px solid #e5e7eb !important;
            break-inside: avoid !important;
        }
    }
    
    /* ============================================================================
       ACCESSIBILITY
    ============================================================================ */
    
    /* Focus styles for keyboard navigation */
    *:focus {
        outline: 2px solid #667eea !important;
        outline-offset: 2px !important;
    }
    
    /* High contrast mode */
    @media (prefers-contrast: high) {
        .stButton > button[kind="primary"] {
            border: 2px solid white !important;
        }
        
        .modern-card, .product-card-modern {
            border: 2px solid #667eea !important;
        }
    }
    
    /* Reduced motion */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* ============================================================================
       ICON ANIMATIONS
    ============================================================================ */
    
    .icon-spin {
        animation: icon-spin 2s linear infinite !important;
    }
    
    @keyframes icon-spin {
        0% {
            transform: rotate(0deg) !important;
        }
        100% {
            transform: rotate(360deg) !important;
        }
    }
    
    .icon-pulse {
        animation: icon-pulse 1.5s ease-in-out infinite !important;
    }
    
    @keyframes icon-pulse {
        0%, 100% {
            transform: scale(1) !important;
        }
        50% {
            transform: scale(1.1) !important;
        }
    }
    
    /* ============================================================================
       GRID LAYOUTS
    ============================================================================ */
    
    .grid-2 {
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 1rem !important;
    }
    
    .grid-3 {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 1rem !important;
    }
    
    .grid-4 {
        display: grid !important;
        grid-template-columns: repeat(4, 1fr) !important;
        gap: 1rem !important;
    }
    
    @media (max-width: 768px) {
        .grid-2, .grid-3, .grid-4 {
            grid-template-columns: 1fr !important;
        }
    }
    
    /* ============================================================================
       CUSTOM SPACING
    ============================================================================ */
    
    .space-y-2 > * + * {
        margin-top: 0.5rem !important;
    }
    
    .space-y-4 > * + * {
        margin-top: 1rem !important;
    }
    
    .space-y-6 > * + * {
        margin-top: 1.5rem !important;
    }
    
    .space-y-8 > * + * {
        margin-top: 2rem !important;
    }
    
    .space-x-2 > * + * {
        margin-left: 0.5rem !important;
    }
    
    .space-x-4 > * + * {
        margin-left: 1rem !important;
    }
    
    .space-x-6 > * + * {
        margin-left: 1.5rem !important;
    }
    
    /* ============================================================================
       FINAL UTILITIES
    ============================================================================ */
    
    .rounded-xl {
        border-radius: 12px !important;
    }
    
    .rounded-2xl {
        border-radius: 16px !important;
    }
    
    .rounded-3xl {
        border-radius: 20px !important;
    }
    
    .bg-gradient-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    .bg-gradient-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    }
    
    .bg-gradient-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
    }
    
    .bg-gradient-danger {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    }
    
    .text-primary {
        color: #667eea !important;
    }
    
    .text-success {
        color: #10b981 !important;
    }
    
    .text-warning {
        color: #f59e0b !important;
    }
    
    .text-danger {
        color: #ef4444 !important;
    }
    
    .border-primary {
        border-color: #667eea !important;
    }
    
    .border-success {
        border-color: #10b981 !important;
    }
    
    .border-warning {
        border-color: #f59e0b !important;
    }
    
    .border-danger {
        border-color: #ef4444 !important;
    }
    
    </style>
"""

ANIMATIONS_CSS = """
    <style>
    /* Confetti effect for celebrations */
    .confetti {
        position: relative;
        overflow: hidden;
    }
    
    .confetti::after {
        content: '🎉';
        position: absolute;
        top: -20px;
        left: 50%;
        transform: translateX(-50%);
        animation: confetti 1s ease-out;
        opacity: 0;
    }
    
    @keyframes confetti {
        0% {
            opacity: 1;
            transform: translateX(-50%) translateY(0) rotate(0deg);
        }
        100% {
            opacity: 0;
            transform: translateX(-50%) translateY(100px) rotate(360deg);
        }
    }
    
    /* Typewriter effect */
    .typewriter {
        overflow: hidden;
        border-right: 3px solid #667eea;
        white-space: nowrap;
        margin: 0 auto;
        animation: typing 