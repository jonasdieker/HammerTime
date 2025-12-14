"""
Dashboard View - Main dashboard with enhanced UI and features
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import json

# Import components
from components import (
    render_product_card_modern,
    render_metric_card,
    render_progress_bar,
    render_empty_state,
    show_toast,
    render_loading_spinner,
    render_order_status_badge,
    render_chat_interface_modern,
    render_voice_interface,
    render_image_upload
)

# Import utils
from utils import calculate_total, add_to_cart, set_cart_qty
from config import PRODUCTS, API_BASE_URL


def dashboard_view():
    """Main dashboard view with enhanced UI"""
    
    # Dashboard header with hero section
    render_dashboard_header()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📦 Product Search", "🎤 Voice Request", "📷 Image Search"])
    
    with tab1:
        render_product_search()
    
    with tab2:
        render_voice_dashboard()
    
    with tab3:
        render_image_dashboard()


def render_dashboard_header():
    """Render the dashboard hero section"""
    
    # Hero section with gradient background
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 24px;
        padding: 40px;
        color: white;
        margin-bottom: 40px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    ">
        <!-- Animated background elements -->
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 80%, rgba(255,255,255,0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255,255,255,0.05) 0%, transparent 50%);
            animation: gradientShift 15s ease infinite;
        "></div>
        
        <div style="position: relative; z-index: 2;">
            <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 25px;">
                <div style="
                    width: 80px;
                    height: 80px;
                    background: rgba(255, 255, 255, 0.2);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 40px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                ">
                    🔨
                </div>
                <div>
                    <h1 style="
                        margin: 0;
                        font-size: 42px;
                        font-weight: 800;
                        letter-spacing: -0.5px;
                        background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                    ">
                        Welcome to HammerTime
                    </h1>
                    <p style="
                        margin: 10px 0 0 0;
                        font-size: 18px;
                        opacity: 0.9;
                        font-weight: 400;
                    ">
                        Your intelligent procurement assistant for construction sites
                    </p>
                </div>
            </div>
            
            <!-- Quick stats -->
            <div style="
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin-top: 30px;
            ">
                <div style="
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 16px;
                    padding: 20px;
                    text-align: center;
                ">
                    <div style="font-size: 12px; opacity: 0.9; margin-bottom: 8px;">Active Orders</div>
                    <div style="font-size: 32px; font-weight: 800;">12</div>
                    <div style="font-size: 12px; margin-top: 5px; color: #a5b4fc;">+2 this week</div>
                </div>
                
                <div style="
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 16px;
                    padding: 20px;
                    text-align: center;
                ">
                    <div style="font-size: 12px; opacity: 0.9; margin-bottom: 8px;">This Month</div>
                    <div style="font-size: 32px; font-weight: 800;">€2,480</div>
                    <div style="font-size: 12px; margin-top: 5px; color: #a5b4fc;">+15% vs last month</div>
                </div>
                
                <div style="
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 16px;
                    padding: 20px;
                    text-align: center;
                ">
                    <div style="font-size: 12px; opacity: 0.9; margin-bottom: 8px;">Time Saved</div>
                    <div style="font-size: 32px; font-weight: 800;">24h</div>
                    <div style="font-size: 12px; margin-top: 5px; color: #a5b4fc;">Avg. 2h per order</div>
                </div>
                
                <div style="
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 16px;
                    padding: 20px;
                    text-align: center;
                ">
                    <div style="font-size: 12px; opacity: 0.9; margin-bottom: 8px;">AI Accuracy</div>
                    <div style="font-size: 32px; font-weight: 800;">94%</div>
                    <div style="font-size: 12px; margin-top: 5px; color: #a5b4fc;">Correct matches</div>
                </div>
            </div>
        </div>
    </div>
    
    <style>
    @keyframes gradientShift {
        0%, 100% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎤 Voice Order", 
                    use_container_width=True,
                    type="primary",
                    help="Place order using voice commands",
                    key="quick_voice"):
            st.session_state.current_page = "Voice Request"
            st.rerun()
    
    with col2:
        if st.button("📷 Image Scan", 
                    use_container_width=True,
                    type="primary",
                    help="Upload image of materials needed",
                    key="quick_image"):
            st.session_state.current_page = "Image Search"
            st.rerun()
    
    with col3:
        if st.button("📋 View Orders", 
                    use_container_width=True,
                    help="Check order status and history",
                    key="quick_orders"):
            st.session_state.current_page = "Orders"
            st.rerun()
    
    with col4:
        if st.button("📊 Analytics", 
                    use_container_width=True,
                    help="View procurement analytics",
                    key="quick_reports"):
            st.session_state.current_page = "Reports"
            st.rerun()


def render_product_search():
    """Enhanced product search interface"""
    
    # Two column layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Search and filter section
        st.markdown("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            border: 1px solid #e5e7eb;
            margin-bottom: 25px;
        ">
            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 20px;
            ">
                <div>
                    <div style="font-weight: 700; color: #1f2937; font-size: 24px;">🔍 Product Catalog</div>
                    <div style="color: #6b7280; font-size: 14px; margin-top: 5px;">
                        Browse and order construction materials
                    </div>
                </div>
                <div style="
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                    color: #667eea;
                    padding: 8px 16px;
                    border-radius: 12px;
                    font-size: 14px;
                    font-weight: 600;
                ">
                    {count} products
                </div>
            </div>
        </div>
        """.format(count=len(PRODUCTS)), unsafe_allow_html=True)
        
        # Search and filter row
        search_col, filter_col = st.columns([3, 1])
        
        with search_col:
            search_query = st.text_input(
                "Search products...",
                placeholder="Type product name, category, or supplier",
                key="product_search",
                label_visibility="collapsed"
            )
        
        with filter_col:
            categories = ["All", "Fasteners", "PPE", "Tools", "Electrical", "Plumbing"]
            selected_category = st.selectbox(
                "Category",
                categories,
                index=0,
                key="category_filter",
                label_visibility="collapsed"
            )
        
        # Filter products
        filtered_products = PRODUCTS
        if search_query:
            filtered_products = [
                p for p in PRODUCTS 
                if search_query.lower() in p['name'].lower() 
                or search_query.lower() in p['description'].lower()
                or search_query.lower() in p['supplier'].lower()
            ]
        
        if selected_category != "All":
            filtered_products = [p for p in filtered_products if p['category'] == selected_category]
        
        # Display products
        if not filtered_products:
            render_empty_state(
                icon="🔍",
                title="No products found",
                message=f"No products match '{search_query}'. Try a different search term."
            )
        else:
            # Display in grid
            cols = st.columns(2)
            for idx, product in enumerate(filtered_products):
                with cols[idx % 2]:
                    render_product_card_modern(product, card_key=f"search_{idx}")
    
    with col2:
        # Order summary and recommendations
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid #e5e7eb;
            margin-bottom: 25px;
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #f1f5f9;
            ">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 20px;
                ">
                    🛒
                </div>
                <div>
                    <div style="font-weight: 700; color: #1f2937; font-size: 18px;">Your Cart</div>
                    <div style="font-size: 13px; color: #6b7280;">{cart_count} items</div>
                </div>
            </div>
        """.format(cart_count=len(st.session_state.cart)), unsafe_allow_html=True)
        
        if st.session_state.cart:
            total = calculate_total()
            
            # Cart items preview
            for item in st.session_state.cart[:3]:  # Show first 3
                st.markdown(f"""
                <div style="
                    background: white;
                    padding: 12px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    border: 1px solid #e5e7eb;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <div style="font-size: 13px; color: #374151;">{item['name']}</div>
                    <div style="font-size: 13px; font-weight: 600; color: #667eea;">{item['qty']}×</div>
                </div>
                """, unsafe_allow_html=True)
            
            if len(st.session_state.cart) > 3:
                st.markdown(f"""
                <div style="
                    text-align: center;
                    font-size: 12px;
                    color: #6b7280;
                    margin: 10px 0;
                    padding: 8px;
                    background: #f8fafc;
                    border-radius: 8px;
                ">
                    +{len(st.session_state.cart) - 3} more items
                </div>
                """, unsafe_allow_html=True)
            
            # Total
            st.markdown(f"""
            <div style="
                margin-top: 20px;
                padding-top: 15px;
                border-top: 2px solid #f1f5f9;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-weight: 600; color: #374151;">Total</div>
                    <div style="font-size: 24px; font-weight: 800; color: #667eea;">€{total:.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Checkout button
            if st.button("Proceed to Checkout", 
                        type="primary",
                        use_container_width=True,
                        key="checkout_btn"):
                st.session_state.current_page = "Orders"
                st.rerun()
        else:
            st.markdown("""
            <div style="
                text-align: center;
                padding: 30px 20px;
                color: #9ca3af;
            ">
                <div style="font-size: 48px; margin-bottom: 15px;">🛒</div>
                <div style="font-weight: 600; color: #6b7280; margin-bottom: 8px;">Your cart is empty</div>
                <div style="color: #9ca3af; font-size: 14px;">Add products to get started</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick recommendations
        st.markdown("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            border: 1px solid #e5e7eb;
            margin-top: 20px;
        ">
            <div style="
                font-weight: 700;
                color: #1f2937;
                font-size: 18px;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            ">
                <div style="
                    width: 32px;
                    height: 32px;
                    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #10b981;
                    font-size: 16px;
                ">
                    💡
                </div>
                Quick Picks
            </div>
        """, unsafe_allow_html=True)
        
        # Recommended products
        recommended = random.sample(PRODUCTS, min(3, len(PRODUCTS)))
        for product in recommended:
            with st.container():
                st.markdown(f"""
                <div style="
                    background: #f8fafc;
                    padding: 12px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    border: 1px solid #e5e7eb;
                    cursor: pointer;
                    transition: all 0.2s ease;
                "
                onmouseover="this.style.background='#f1f5f9'; this.style.borderColor='#667eea';"
                onmouseout="this.style.background='#f8fafc'; this.style.borderColor='#e5e7eb';">
                    <div style="font-size: 13px; color: #374151; font-weight: 500; margin-bottom: 4px;">
                        {product['name']}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-size: 11px; color: #6b7280;">{product['supplier']}</div>
                        <div style="font-size: 13px; font-weight: 600; color: #667eea;">€{product['price']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_voice_dashboard():
    """Voice request interface in dashboard"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Voice interface
        st.markdown("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            border: 1px solid #e5e7eb;
            margin-bottom: 25px;
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 25px;
            ">
                <div style="
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 15px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 28px;
                ">
                    🎤
                </div>
                <div>
                    <div style="font-weight: 700; color: #1f2937; font-size: 24px;">Voice Procurement</div>
                    <div style="color: #6b7280; font-size: 14px; margin-top: 5px;">
                        Speak naturally about what you need
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice recording section
        st.markdown("""
        <div style="
            text-align: center;
            margin-bottom: 30px;
        ">
            <div id="voice-button" style="
                width: 120px;
                height: 120px;
                margin: 0 auto 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 48px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
                animation: pulse 2s infinite;
            "
            onmouseover="this.style.transform='scale(1.1)'; this.style.boxShadow='0 12px 35px rgba(102, 126, 234, 0.6)';"
            onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 8px 25px rgba(102, 126, 234, 0.4)';">
                🎤
            </div>
            <div style="font-weight: 600; color: #374151; font-size: 20px;">Click to Record</div>
            <div style="color: #6b7280; font-size: 14px; margin-top: 5px;">
                Speak clearly about your material needs
            </div>
        </div>
        
        <style>
        @keyframes pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
            }
            70% {
                box-shadow: 0 0 0 25px rgba(102, 126, 234, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(102, 126, 234, 0);
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Record button
        if st.button("Start Recording", 
                    type="primary",
                    use_container_width=True,
                    key="voice_record_main"):
            
            with st.spinner("🎤 Listening... Speak now..."):
                # Simulate recording
                time.sleep(2)
                
                # Sample transcriptions
                samples = [
                    "I need 25 boxes of 4x40mm screws for drywall installation",
                    "Order 10 pairs of safety gloves size 9 and 5 construction helmets",
                    "Get me materials for painting: brushes, rollers, and paint trays",
                ]
                
                st.session_state.voice_text = random.choice(samples)
                st.session_state.voice_raw_text = st.session_state.voice_text
                show_toast("✅ Voice recording captured!", "success")
                st.rerun()
        
        # Display transcribed text if available
        if st.session_state.get('voice_text'):
            st.markdown("### 📝 Transcribed Request")
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                border-radius: 12px;
                padding: 20px;
                margin: 20px 0;
                border: 1px solid rgba(102, 126, 234, 0.3);
            ">
                <div style="font-weight: 600; color: #4c51bf; margin-bottom: 10px; font-size: 14px;">
                    What you said:
                </div>
                <div style="color: #667eea; font-size: 16px; line-height: 1.6;">
                    "{st.session_state.voice_text}"
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Process button
            if st.button("Process with AI", 
                        type="primary",
                        use_container_width=True,
                        key="process_voice_main"):
                with st.spinner("🤖 AI is processing your request..."):
                    time.sleep(1)
                    show_toast("✅ Request sent to AI assistant!", "success")
    
    with col2:
        # Voice tips
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid #e5e7eb;
            margin-bottom: 25px;
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 20px;
            ">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%);
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #f59e0b;
                    font-size: 20px;
                ">
                    💡
                </div>
                <div style="font-weight: 700; color: #1f2937; font-size: 18px;">Voice Tips</div>
            </div>
        """, unsafe_allow_html=True)
        
        tips = [
            "Speak in complete sentences",
            "Mention quantities clearly",
            "Include specifications like size",
            "Add delivery urgency if needed",
            "Be specific about materials"
        ]
        
        for tip in tips:
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: flex-start;
                gap: 10px;
                margin-bottom: 12px;
                padding: 12px;
                background: white;
                border-radius: 10px;
                border: 1px solid #e5e7eb;
            ">
                <div style="
                    width: 24px;
                    height: 24px;
                    background: rgba(102, 126, 234, 0.1);
                    border-radius: 6px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #667eea;
                    font-size: 12px;
                    flex-shrink: 0;
                ">
                    ✓
                </div>
                <div style="color: #374151; font-size: 14px; line-height: 1.5;">{tip}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Examples
        st.markdown("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            border: 1px solid #e5e7eb;
            margin-top: 20px;
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 20px;
            ">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #10b981;
                    font-size: 20px;
                ">
                    🗣️
                </div>
                <div style="font-weight: 700; color: #1f2937; font-size: 18px;">Examples</div>
            </div>
        """, unsafe_allow_html=True)
        
        examples = [
            "I need 50 wood screws, 3 inches long",
            "Order safety equipment for 3 workers",
            "Get paint supplies for one room"
        ]
        
        for example in examples:
            st.markdown(f"""
            <div style="
                background: #f8fafc;
                padding: 12px;
                border-radius: 10px;
                margin-bottom: 10px;
                border: 1px solid #e5e7eb;
                cursor: pointer;
                transition: all 0.2s ease;
            "
            onmouseover="this.style.background='#f1f5f9'; this.style.borderColor='#667eea';"
            onmouseout="this.style.background='#f8fafc'; this.style.borderColor='#e5e7eb';">
                <div style="color: #374151; font-size: 13px; line-height: 1.5;">"{example}"</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_image_dashboard():
    """Image search interface in dashboard"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Image upload section
        st.markdown("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            border: 1px solid #e5e7eb;
            margin-bottom: 25px;
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 25px;
            ">
                <div style="
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 15px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 28px;
                ">
                    📷
                </div>
                <div>
                    <div style="font-weight: 700; color: #1f2937; font-size: 24px;">Image Analysis</div>
                    <div style="color: #6b7280; font-size: 14px; margin-top: 5px;">
                        Upload photos of materials or handwritten lists
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Upload area
        uploaded_file = st.file_uploader(
            "Drag & drop or click to upload",
            type=['png', 'jpg', 'jpeg', 'heic'],
            help="Upload images of materials, shopping lists, or construction sites",
            key="image_upload_dashboard"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Analyze Image", 
                            type="primary",
                            use_container_width=True,
                            key="analyze_image_dash"):
                    with st.spinner("🔍 AI is analyzing the image..."):
                        time.sleep(2)
                        
                        # Sample analysis
                        analyses = [
                            "I can see construction screws, safety gloves, and measuring tools. Ready to order?",
                            "This appears to be a handwritten shopping list for electrical work.",
                            "I recognize drywall materials and finishing tools in this photo."
                        ]
                        
                        analysis = random.choice(analyses)
                        
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
                            border-radius: 12px;
                            padding: 20px;
                            margin-top: 20px;
                            border: 1px solid rgba(16, 185, 129, 0.3);
                        ">
                            <div style="font-weight: 600; color: #065f46; margin-bottom: 10px;">
                                🤖 AI Analysis:
                            </div>
                            <div style="color: #047857; font-size: 15px; line-height: 1.6;">
                                {analysis}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            with col_b:
                if st.button("Clear Image", 
                            type="secondary",
                            use_container_width=True,
                            key="clear_image_dash"):
                    uploaded_file = None
                    st.rerun()
        
        else:
            # Upload instructions
            st.markdown("""
            <div style="
                border: 2px dashed #667eea;
                border-radius: 20px;
                padding: 60px 40px;
                text-align: center;
                background: rgba(102, 126, 234, 0.05);
                margin: 20px 0;
                cursor: pointer;
                transition: all 0.3s ease;
            "
            onmouseover="this.style.background='rgba(102, 126, 234, 0.1)'; this.style.borderColor='#764ba2';"
            onmouseout="this.style.background='rgba(102, 126, 234, 0.05)'; this.style.borderColor='#667eea';">
                <div style="font-size: 48px; margin-bottom: 20px; color: #667eea;">📤</div>
                <div style="font-weight: 600; color: #374151; font-size: 18px; margin-bottom: 10px;">
                    Upload Construction Images
                </div>
                <div style="color: #6b7280; font-size: 14px; margin-bottom: 30px;">
                    Supports photos, handwritten lists, screenshots
                </div>
                
                <div style="
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 15px;
                    max-width: 400px;
                    margin: 0 auto;
                ">
                    <div style="
                        background: white;
                        padding: 15px;
                        border-radius: 10px;
                        border: 1px solid #e5e7eb;
                    ">
                        <div style="font-size: 24px; margin-bottom: 10px;">📝</div>
                        <div style="font-size: 13px; color: #374151; font-weight: 500;">Handwritten Lists</div>
                    </div>
                    <div style="
                        background: white;
                        padding: 15px;
                        border-radius: 10px;
                        border: 1px solid #e5e7eb;
                    ">
                        <div style="font-size: 24px; margin-bottom: 10px;">🔩</div>
                        <div style="font-size: 13px; color: #374151; font-weight: 500;">Material Photos</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Image analysis benefits
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid #e5e7eb;
            margin-bottom: 25px;
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 20px;
            ">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #667eea;
                    font-size: 20px;
                ">
                    🎯
                </div>
                <div style="font-weight: 700; color: #1f2937; font-size: 18px;">Why Use Images?</div>
            </div>
        """, unsafe_allow_html=True)
        
        benefits = [
            ("🚀 Faster Ordering", "Skip manual entry by snapping a photo"),
            ("✅ Fewer Errors", "AI accurately identifies materials"),
            ("💡 Smart Suggestions", "Get recommendations for similar items"),
            ("📊 Better Pricing", "Find best deals across suppliers")
        ]
        
        for icon, text in benefits:
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 15px;
                padding: 12px;
                background: white;
                border-radius: 10px;
                border: 1px solid #e5e7eb;
            ">
                <div style="
                    width: 32px;
                    height: 32px;
                    background: rgba(102, 126, 234, 0.1);
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #667eea;
                    font-size: 16px;
                    flex-shrink: 0;
                ">
                    {icon}
                </div>
                <div style="color: #374151; font-size: 14px; font-weight: 500;">{text}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Recent analyses
        st.markdown("""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            border: 1px solid #e5e7eb;
            margin-top: 20px;
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 20px;
            ">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #10b981;
                    font-size: 20px;
                ">
                    📋
                </div>
                <div style="font-weight: 700; color: #1f2937; font-size: 18px;">Recent Analyses</div>
            </div>
        """, unsafe_allow_html=True)
        
        recent = [
            ("Construction screws", "2 hours ago", "✅ 95% match"),
            ("Safety equipment", "Yesterday", "✅ 92% match"),
            ("Paint supplies", "Mar 15", "✅ 88% match")
        ]
        
        for item, time, match in recent:
            st.markdown(f"""
            <div style="
                background: #f8fafc;
                padding: 12px;
                border-radius: 10px;
                margin-bottom: 10px;
                border: 1px solid #e5e7eb;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <div style="font-weight: 500; color: #374151; font-size: 13px;">{item}</div>
                    <div style="font-size: 11px; color: #6b7280; background: rgba(102, 126, 234, 0.1); padding: 2px 8px; border-radius: 10px;">
                        {match}
                    </div>
                </div>
                <div style="font-size: 11px; color: #9ca3af;">{time}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_recent_activity():
    """Render recent activity section"""
    st.markdown("### 📈 Recent Activity")
    
    activities = [
        {
            "time": "10:30 AM",
            "action": "Order Placed",
            "item": "50x Screws, 10x Gloves",
            "user": "Site Foreman",
            "status": "approved"
        },
        {
            "time": "09:45 AM",
            "action": "Voice Request",
            "item": "Safety gear for team",
            "user": "Construction Worker",
            "status": "pending"
        },
        {
            "time": "Yesterday",
            "action": "Image Order",
            "item": "Drywall materials",
            "user": "Project Manager",
            "status": "delivered"
        },
        {
            "time": "Mar 12",
            "action": "Contract Signed",
            "item": "Annual supply agreement",
            "user": "Procurement Manager",
            "status": "completed"
        },
    ]
    
    for activity in activities:
        with st.container():
            col1, col2, col3 = st.columns([1, 3, 2])
            
            with col1:
                st.markdown(f"**{activity['time']}**")
            
            with col2:
                st.markdown(f"{activity['action']}: {activity['item']}")
                st.caption(f"By: {activity['user']}")
            
            with col3:
                status_color = {
                    "approved": "#10b981",
                    "pending": "#f59e0b",
                    "delivered": "#3b82f6",
                    "completed": "#8b5cf6"
                }.get(activity['status'], "#6b7280")
                
                st.markdown(f"""
                <span style="
                    background: {status_color};
                    color: white;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 600;
                ">{activity['status'].upper()}</span>
                """, unsafe_allow_html=True)


def render_top_suppliers():
    """Render top suppliers section"""
    st.markdown("### 🏆 Top Suppliers")
    
    suppliers = [
        {"name": "Würth", "orders": 42, "rating": "★★★★★", "category": "Fasteners"},
        {"name": "Fischer", "orders": 28, "rating": "★★★★☆", "category": "Anchors"},
        {"name": "Bosch", "orders": 19, "rating": "★★★★☆", "category": "Tools"},
        {"name": "Uvex", "orders": 15, "rating": "★★★☆☆", "category": "PPE"},
    ]
    
    for supplier in suppliers:
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{supplier['name']}**")
                st.caption(f"{supplier['category']} • {supplier['orders']} orders")
            
            with col2:
                st.markdown(f"<div style='color: #f59e0b;'>{supplier['rating']}</div>", unsafe_allow_html=True)


# Helper function for time simulation
import time as time_module


# Export main function
def main():
    """Main dashboard entry point"""
    dashboard_view()


if __name__ == "__main__":
    main()