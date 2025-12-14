"""
Reusable UI components: sidebar, order summary, product description, and enhanced UI elements
"""
import streamlit as st
import time
import random
from datetime import datetime, timedelta
from utils import calculate_total, place_order, navigate_to, add_to_cart, remove_from_cart, set_cart_qty
from config import AUTO_APPROVAL_LIMIT, ADMIN_PASSWORD, API_BASE_URL, PRODUCTS
import requests
import json


# ============================================================================
# ENHANCED SIDEBAR COMPONENT
# ============================================================================

def render_sidebar():
    """Enhanced sidebar with modern design and user profile"""
    with st.sidebar:
        # Logo and Title with gradient
        st.markdown("""
        <div style="text-align: center; padding: 20px 0 30px 0;">
            <div style="
                font-size: 36px;
                font-weight: 800;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 5px;
            ">
                🔨 HammerTime
            </div>
            <div style="
                color: #6b7280;
                font-size: 14px;
                margin-top: 5px;
                letter-spacing: 1px;
                text-transform: uppercase;
            ">
                Procurement Assistant
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent); margin: 0 10px 25px 10px;'></div>", unsafe_allow_html=True)
        
        # Navigation with enhanced styling
        pages = [
            ("🏠", "Dashboard", "Main dashboard with all features"),
            ("🎤", "Voice Request", "Order using voice commands"),
            ("📷", "Image Search", "Upload images of materials"),
            ("📋", "Orders", "View and manage orders"),
            ("📊", "Reports", "Analytics and insights"),
        ]
        
        current_page = st.session_state.get('current_page', 'Dashboard')
        
        for icon, page, description in pages:
            is_active = current_page == page
            
            # Create a custom button with hover effects
            button_html = f"""
            <div style="
                margin: 8px 12px;
                padding: 12px 16px;
                background: {'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if is_active else 'transparent'};
                color: {'white' if is_active else '#4b5563'};
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                border: 1px solid {'transparent' if is_active else '#e5e7eb'};
                display: flex;
                align-items: center;
                gap: 12px;
                {'box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);' if is_active else ''}
            "
            onmouseover="this.style.transform='translateX(5px)'; this.style.background='{'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if not is_active else '#5a67d8'}; this.style.color='white';"
            onmouseout="this.style.transform='translateX(0)'; this.style.background='{'transparent' if not is_active else 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'}; this.style.color='{'#4b5563' if not is_active else 'white'}';"
            onclick="window.location.href='?page={page.lower().replace(' ', '_')}'">
                <div style="font-size: 20px;">{icon}</div>
                <div>
                    <div style="font-weight: 600; font-size: 15px;">{page}</div>
                    <div style="font-size: 11px; opacity: 0.8; margin-top: 2px;">{description}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Use markdown with HTML and JavaScript for navigation
            st.markdown(button_html, unsafe_allow_html=True)
            
            # Add Streamlit button for actual navigation
            if st.button(f"{icon} {page}", key=f"nav_{page}", 
                        help=description, 
                        use_container_width=True,
                        type="primary" if is_active else "secondary",
                        label_visibility="collapsed"):
                navigate_to(page)
                st.rerun()
        
        st.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent); margin: 25px 10px;'></div>", unsafe_allow_html=True)
        
        # User profile section
        st.markdown("""
        <div style="
            padding: 20px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border-radius: 16px;
            margin: 0 10px 20px 10px;
            border: 1px solid rgba(102, 126, 234, 0.2);
        ">
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                <div style="
                    width: 50px;
                    height: 50px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    font-size: 20px;
                    box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
                ">
                    👷
                </div>
                <div>
                    <div style="font-weight: 700; color: #374151; font-size: 16px;">Site Foreman</div>
                    <div style="font-size: 13px; color: #6b7280;">Construction Site #42</div>
                    <div style="font-size: 12px; color: #10b981; margin-top: 3px;">
                        <span style="background: rgba(16, 185, 129, 0.1); padding: 2px 8px; border-radius: 10px;">🟢 Active</span>
                    </div>
                </div>
            </div>
            
            <div style="
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-top: 15px;
            ">
                <div style="
                    background: white;
                    padding: 10px;
                    border-radius: 10px;
                    text-align: center;
                    border: 1px solid #e5e7eb;
                ">
                    <div style="font-size: 11px; color: #6b7280;">Today's Orders</div>
                    <div style="font-size: 18px; font-weight: 700; color: #667eea;">3</div>
                </div>
                <div style="
                    background: white;
                    padding: 10px;
                    border-radius: 10px;
                    text-align: center;
                    border: 1px solid #e5e7eb;
                ">
                    <div style="font-size: 11px; color: #6b7280;">Pending</div>
                    <div style="font-size: 18px; font-weight: 700; color: #f59e0b;">2</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick cart preview
        if st.session_state.cart:
            st.markdown("<div style='margin: 0 10px 15px 10px; font-weight: 600; color: #374151; font-size: 14px;'>🛒 Current Cart</div>", unsafe_allow_html=True)
            for item in st.session_state.cart[:2]:  # Show first 2 items
                st.markdown(f"""
                <div style="
                    background: white;
                    padding: 8px 12px;
                    border-radius: 8px;
                    margin: 5px 10px;
                    border: 1px solid #e5e7eb;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <div style="font-size: 13px; color: #374151;">{item['name']}</div>
                    <div style="font-size: 13px; font-weight: 600; color: #667eea;">{item['qty']}×</div>
                </div>
                """, unsafe_allow_html=True)
            
            if len(st.session_state.cart) > 2:
                st.markdown(f"<div style='text-align: center; font-size: 12px; color: #6b7280; margin: 5px 10px;'>+{len(st.session_state.cart) - 2} more items</div>", unsafe_allow_html=True)
            
            total = calculate_total()
            st.markdown(f"""
            <div style="
                margin: 10px;
                padding: 12px;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                border-radius: 10px;
                text-align: center;
                border: 1px solid rgba(102, 126, 234, 0.2);
            ">
                <div style="font-size: 12px; color: #6b7280;">Cart Total</div>
                <div style="font-size: 22px; font-weight: 700; color: #667eea;">€{total:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent); margin: 20px 10px;'></div>", unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
        <div style="
            text-align: center;
            padding: 15px 10px;
            color: #9ca3af;
            font-size: 11px;
        ">
            <div style="margin-bottom: 5px;">⚡ Powered by Claude AI</div>
            <div style="
                display: flex;
                justify-content: center;
                gap: 10px;
                margin-top: 10px;
            ">
                <span style="background: rgba(102, 126, 234, 0.1); padding: 3px 10px; border-radius: 20px; font-size: 10px;">v2.0</span>
                <span style="background: rgba(118, 75, 162, 0.1); padding: 3px 10px; border-radius: 20px; font-size: 10px;">TUM.ai</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# MODERN PRODUCT CARD COMPONENT
# ============================================================================

def render_product_card_modern(product, show_add=True, card_key=""):
    """Modern product card with enhanced interactions and animations"""
    
    # Generate random stock for demo
    stock = random.randint(0, 100)
    if stock > 50:
        stock_color = "#10b981"
        stock_text = "In Stock"
    elif stock > 20:
        stock_color = "#f59e0b"
        stock_text = "Low Stock"
    else:
        stock_color = "#ef4444"
        stock_text = "Out of Stock"
    
    # Calculate delivery time (1-3 days)
    delivery_days = random.randint(1, 3)
    
    with st.container():
        st.markdown(f"""
        <div class="modern-card" style="
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: 0;
                right: 0;
                width: 0;
                height: 0;
                border-style: solid;
                border-width: 0 40px 40px 0;
                border-color: transparent rgba(102, 126, 234, 0.1) transparent transparent;
            "></div>
            
            <div style="display: flex; align-items: flex-start; gap: 15px;">
                <!-- Product Icon -->
                <div style="
                    width: 70px;
                    height: 70px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 28px;
                    flex-shrink: 0;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                ">
                    {product.get('icon', '🔩')}
                </div>
                
                <!-- Product Info -->
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div style="
                                font-weight: 700;
                                color: #1f2937;
                                font-size: 16px;
                                margin-bottom: 4px;
                            ">{product['name']}</div>
                            <div style="
                                color: #6b7280;
                                font-size: 13px;
                                margin-bottom: 8px;
                                line-height: 1.4;
                            ">{product['description']}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="
                                font-size: 24px;
                                font-weight: 800;
                                color: #667eea;
                                margin-bottom: 2px;
                            ">€{product['price']}</div>
                            <div style="font-size: 11px; color: #9ca3af;">per unit</div>
                        </div>
                    </div>
                    
                    <!-- Product Details -->
                    <div style="
                        display: flex;
                        gap: 15px;
                        margin-top: 10px;
                        padding-top: 10px;
                        border-top: 1px solid #f3f4f6;
                    ">
                        <div style="display: flex; align-items: center; gap: 5px;">
                            <div style="
                                width: 8px;
                                height: 8px;
                                background: {stock_color};
                                border-radius: 50%;
                            "></div>
                            <div style="font-size: 12px; color: #6b7280;">{stock_text}</div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 5px;">
                            <div style="font-size: 12px; color: #6b7280;">🚚 {delivery_days} days</div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 5px;">
                            <div style="font-size: 12px; color: #6b7280;">🏢 {product['supplier']}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quantity selector and add button
        if show_add:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Find current quantity in cart
                current_qty = 0
                for item in st.session_state.cart:
                    if item['id'] == product['id']:
                        current_qty = item['qty']
                
                qty = st.number_input(
                    "Quantity",
                    min_value=0,
                    max_value=100,
                    value=current_qty if current_qty > 0 else 1,
                    key=f"qty_{product['id']}_{card_key}",
                    label_visibility="collapsed"
                )
            
            with col2:
                button_text = "Update" if current_qty > 0 else "Add to Cart"
                button_type = "primary" if qty > 0 else "secondary"
                
                if st.button(
                    f"🛒 {button_text}",
                    key=f"add_{product['id']}_{card_key}",
                    type=button_type,
                    use_container_width=True,
                    help=f"Add {qty} units to cart" if qty > 0 else "Set quantity first"
                ):
                    if qty > 0:
                        set_cart_qty(product, qty)
                        show_toast(f"✅ {qty}x {product['name']} added to cart!", "success")
                        time.sleep(0.3)  # Brief pause for toast visibility
                        st.rerun()
                    else:
                        remove_from_cart(product['id'])
                        show_toast(f"🗑️ {product['name']} removed from cart", "info")
                        time.sleep(0.3)
                        st.rerun()


# ============================================================================
# ENHANCED ORDER SUMMARY COMPONENT
# ============================================================================

def render_order_summary(key_prefix="default"):
    """Enhanced order summary with animations and approval workflow"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    ">
        <div style="
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f1f5f9;
        ">
            <div style="display: flex; align-items: center; gap: 10px;">
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
                    📦
                </div>
                <div>
                    <div style="font-weight: 700; color: #1f2937; font-size: 18px;">Order Summary</div>
                    <div style="font-size: 13px; color: #6b7280;">Review items before checkout</div>
                </div>
            </div>
            <div style="
                background: rgba(102, 126, 234, 0.1);
                color: #667eea;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 13px;
                font-weight: 600;
            ">
                {items} items
            </div>
        </div>
    """.format(items=len(st.session_state.cart)), unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 40px 20px;
            color: #9ca3af;
        ">
            <div style="font-size: 48px; margin-bottom: 15px;">🛒</div>
            <div style="font-weight: 600; color: #6b7280; margin-bottom: 8px;">Your cart is empty</div>
            <div style="font-size: 14px; color: #9ca3af;">Add products from the search or voice request</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    # Cart items with animations
    for idx, item in enumerate(st.session_state.cart):
        subtotal = item['price'] * item['qty']
        
        st.markdown(f"""
        <div class="fade-in" style="
            animation-delay: {idx * 0.1}s;
            background: white;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 10px;
            border: 1px solid #e5e7eb;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.3s ease;
        ">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #667eea;
                    font-size: 18px;
                ">
                    {item.get('icon', '📦')}
                </div>
                <div>
                    <div style="font-weight: 600; color: #374151; font-size: 14px;">{item['name']}</div>
                    <div style="display: flex; align-items: center; gap: 10px; margin-top: 4px;">
                        <div style="font-size: 12px; color: #6b7280;">{item['supplier']}</div>
                        <div style="font-size: 12px; color: #667eea; background: rgba(102, 126, 234, 0.1); padding: 2px 8px; border-radius: 10px;">
                            €{item['price']} each
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    background: #f8fafc;
                    padding: 6px 12px;
                    border-radius: 10px;
                ">
                    <div style="
                        font-weight: 700;
                        color: #374151;
                        min-width: 30px;
                        text-align: center;
                    ">{item['qty']}</div>
                </div>
                
                <div style="text-align: right;">
                    <div style="font-weight: 700; color: #1f2937; font-size: 16px;">€{subtotal:.2f}</div>
                    <div style="font-size: 11px; color: #9ca3af;">total</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Total and approval section
    total = calculate_total()
    requires_approval = total > AUTO_APPROVAL_LIMIT
    
    st.markdown("""
        <div style="
            margin-top: 25px;
            padding-top: 20px;
            border-top: 2px solid #f1f5f9;
        ">
    """, unsafe_allow_html=True)
    
    # Summary rows
    summary_items = [
        ("Subtotal", f"€{total:.2f}"),
        ("Shipping", "€0.00"),
        ("Tax (19%)", f"€{total * 0.19:.2f}")
    ]
    
    for label, value in summary_items:
        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            color: #6b7280;
            font-size: 14px;
        ">
            <div>{label}</div>
            <div>{value}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Grand Total
    grand_total = total * 1.19
    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: space-between;
        padding: 15px 0;
        margin: 15px 0;
        border-top: 2px solid #e5e7eb;
        border-bottom: 2px solid #e5e7eb;
    ">
        <div style="font-weight: 700; color: #1f2937; font-size: 18px;">Total</div>
        <div style="
            font-weight: 800;
            color: #667eea;
            font-size: 24px;
        ">€{grand_total:.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Approval status
    if requires_approval:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        ">
            <div style="font-size: 36px; margin-bottom: 10px;">⚠️</div>
            <div style="font-weight: 700; color: #92400e; margin-bottom: 8px;">
                Admin Approval Required
            </div>
            <div style="color: #b45309; font-size: 14px; margin-bottom: 15px;">
                Orders over €{AUTO_APPROVAL_LIMIT} need manual approval
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Admin password input
        admin_password = st.text_input(
            "🔐 Admin Password",
            type="password",
            placeholder="Enter admin password to approve",
            key=f"{key_prefix}_admin_password",
            help="Enter 'admin123' to approve this order"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚫 Cancel Order", 
                        use_container_width=True,
                        type="secondary",
                        key=f"{key_prefix}_cancel"):
                st.session_state.cart = []
                show_toast("Order cancelled", "info")
                st.rerun()
        
        with col2:
            if st.button("✅ Approve & Place Order", 
                        use_container_width=True,
                        type="primary",
                        key=f"{key_prefix}_approve",
                        disabled=not admin_password):
                if admin_password == ADMIN_PASSWORD:
                    status = place_order(custom_status="Admin Approved")
                    show_toast("✅ Order approved and placed successfully!", "success")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    show_toast("❌ Invalid password. Please try again.", "error")
    
    else:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        ">
            <div style="font-size: 36px; margin-bottom: 10px;">✅</div>
            <div style="font-weight: 700; color: #065f46; margin-bottom: 8px;">
                Auto-Approval Granted
            </div>
            <div style="color: #047857; font-size: 14px;">
                Orders under €{AUTO_APPROVAL_LIMIT} are auto-approved
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Place Order Now", 
                    type="primary",
                    use_container_width=True,
                    key=f"{key_prefix}_place_order"):
            status = place_order()
            show_toast(f"✅ Order placed successfully! Status: {status}", "success")
            time.sleep(0.5)
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)


# ============================================================================
# ENHANCED CHAT COMPONENTS
# ============================================================================

def render_chat_message(role, content):
    """Render a modern chat message bubble with animations"""
    
    # Process content for display
    if isinstance(content, dict):
        content_str = json.dumps(content, indent=2)
    else:
        content_str = str(content)
    
    # Format bullet points and newlines
    formatted_content = content_str
    for char in ['•', '-', '*']:
        formatted_content = formatted_content.replace(f'{char} ', f'<br>{char} ')
    formatted_content = formatted_content.replace('\n', '<br>')
    
    if role == "user":
        # User message - right aligned with gradient
        st.markdown(f"""
        <div class="chat-bubble-user" style="
            margin-left: auto;
            margin-right: 0;
            max-width: 75%;
            animation: slideInRight 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        ">
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 14px 18px;
                border-radius: 18px 18px 4px 18px;
                line-height: 1.5;
                font-size: 14px;
                box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
            ">
                {formatted_content}
            </div>
            <div style="
                font-size: 11px;
                color: #9ca3af;
                text-align: right;
                margin-top: 5px;
                padding-right: 5px;
            ">
                <span style="background: rgba(255, 255, 255, 0.2); padding: 2px 8px; border-radius: 10px;">You</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Assistant message - left aligned
        st.markdown(f"""
        <div class="chat-bubble-ai" style="
            margin-right: auto;
            margin-left: 0;
            max-width: 75%;
            animation: slideInLeft 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        ">
            <div style="
                background: white;
                color: #374151;
                padding: 14px 18px;
                border-radius: 18px 18px 18px 4px;
                line-height: 1.5;
                font-size: 14px;
                border: 1px solid #e5e7eb;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            ">
                {formatted_content}
            </div>
            <div style="
                font-size: 11px;
                color: #9ca3af;
                text-align: left;
                margin-top: 5px;
                padding-left: 5px;
            ">
                <span style="background: rgba(102, 126, 234, 0.1); padding: 2px 8px; border-radius: 10px; color: #667eea;">🤖 AI Assistant</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_chat_history():
    """Render the full chat history with animations"""
    for idx, msg in enumerate(st.session_state.voice_chat_messages):
        render_chat_message(msg["role"], msg["content"])


def render_chat_interface_modern():
    """Modern chat interface for voice and text conversations"""
    
    # Chat header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px 20px 0 0;
        padding: 20px;
        color: white;
        margin-bottom: 0;
    ">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 5px;">
            <div style="font-size: 24px;">💬</div>
            <div>
                <div style="font-weight: 700; font-size: 18px;">AI Procurement Assistant</div>
                <div style="font-size: 13px; opacity: 0.9;">Ask for materials in plain English</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat messages container
    st.markdown("""
    <div style="
        background: white;
        border-radius: 0 0 20px 20px;
        padding: 25px;
        height: 400px;
        overflow-y: auto;
        border: 1px solid #e5e7eb;
        border-top: none;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    ">
    """, unsafe_allow_html=True)
    
    if not st.session_state.voice_chat_messages:
        # Welcome message
        st.markdown("""
        <div style="
            text-align: center;
            padding: 40px 20px;
            color: #9ca3af;
        ">
            <div style="font-size: 48px; margin-bottom: 15px;">🤖</div>
            <div style="font-weight: 700; color: #374151; margin-bottom: 8px; font-size: 18px;">
                Hi! I'm your Procurement Assistant
            </div>
            <div style="color: #6b7280; font-size: 14px; margin-bottom: 20px;">
                Describe what you need and I'll find the best products
            </div>
            <div style="
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                max-width: 400px;
                margin: 0 auto;
            ">
                <div style="
                    background: rgba(102, 126, 234, 0.1);
                    padding: 12px;
                    border-radius: 10px;
                    font-size: 13px;
                    color: #667eea;
                ">
                    <div style="font-weight: 600;">"I need 50 screws"</div>
                </div>
                <div style="
                    background: rgba(118, 75, 162, 0.1);
                    padding: 12px;
                    border-radius: 10px;
                    font-size: 13px;
                    color: #764ba2;
                ">
                    <div style="font-weight: 600;">"Safety gear for 5 workers"</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Render chat messages
        for idx, msg in enumerate(st.session_state.voice_chat_messages):
            render_chat_message(msg["role"], msg["content"])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    with col1:
        chat_input = st.chat_input("💬 Describe what materials you need...", key="chat_input_main")
        if chat_input:
            # Add user message
            st.session_state.voice_chat_messages.append({
                "role": "user",
                "content": chat_input
            })
            
            # Show typing indicator
            with st.spinner("🤔 AI is thinking..."):
                # Simulate AI processing
                time.sleep(1)
                
                # Add AI response (in real app, this would call the API)
                sample_responses = [
                    "I understand you need screws. What size and quantity are you looking for?",
                    "For safety gear, I recommend helmets, gloves, and safety glasses. How many of each?",
                    "I found several options for that. Do you have a preferred supplier or budget range?",
                    "Great! I'll help you order those materials. Any specific delivery requirements?"
                ]
                ai_response = random.choice(sample_responses)
                
                st.session_state.voice_chat_messages.append({
                    "role": "assistant",
                    "content": ai_response
                })
            
            st.rerun()
    
    with col2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("🗑️", help="Clear chat history", key="clear_chat"):
            st.session_state.voice_chat_messages = []
            st.rerun()


# ============================================================================
# VOICE INTERFACE COMPONENT
# ============================================================================

def render_voice_interface():
    """Enhanced voice input interface with animations"""
    
    # Voice interface header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 30px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    ">
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="none" stroke="white" stroke-width="1" opacity="0.1"/></svg>');"></div>
        
        <div style="position: relative; z-index: 1;">
            <div style="font-size: 64px; margin-bottom: 20px; animation: pulse 2s infinite;">🎤</div>
            <h2 style="margin: 0 0 10px 0; font-size: 28px;">Voice Procurement</h2>
            <p style="opacity: 0.9; font-size: 16px; margin-bottom: 25px;">
                Speak naturally about what you need. Our AI will understand and help you order.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Voice recording section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Voice recording button with animation
        st.markdown("""
        <div style="
            text-align: center;
            margin-bottom: 30px;
        ">
            <div id="voice-button" style="
                width: 100px;
                height: 100px;
                margin: 0 auto 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 36px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            "
            onmouseover="this.style.transform='scale(1.1)'; this.style.boxShadow='0 12px 35px rgba(102, 126, 234, 0.6)';"
            onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 8px 25px rgba(102, 126, 234, 0.4)';">
                🎤
            </div>
            <div style="font-weight: 600; color: #374151; font-size: 18px;">Click to Record</div>
            <div style="color: #6b7280; font-size: 14px; margin-top: 5px;">
                Speak clearly about your material needs
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Record button
        if st.button("🎤 Start Recording", 
                    use_container_width=True, 
                    type="primary",
                    key="voice_record_btn"):
            
            with st.spinner("🎤 Listening... Speak now..."):
                # Simulate recording
                time.sleep(3)
                
                # Sample voice transcriptions
                sample_transcriptions = [
                    "I need 25 boxes of 4x40mm screws for drywall installation",
                    "Order 10 pairs of safety gloves size 9 and 5 construction helmets",
                    "Get me materials for painting: brushes, rollers, and paint trays",
                    "Need electrical supplies: wire, connectors, and circuit breakers"
                ]
                
                st.session_state.voice_text = random.choice(sample_transcriptions)
                st.session_state.voice_raw_text = st.session_state.voice_text
            
            # Show success message
            show_toast("✅ Voice recording captured!", "success")
            st.rerun()
    
    # Voice tips
    with st.expander("💡 Voice Tips & Examples", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Speak clearly and include:**
            - Item names (screws, gloves, helmets)
            - Quantities (10 boxes, 5 pairs)
            - Specifications (size 9, 4x40mm)
            - Purpose (for drywall, painting)
            
            **Good Examples:**
            • "I need 50 wood screws, 3 inches long"
            • "Order safety equipment for 3 workers"
            • "Get paint supplies for one room"
            """)
        
        with col2:
            st.markdown("""
            **For best results:**
            1. Speak in complete sentences
            2. Mention quantities clearly
            3. Include any special requirements
            4. Specify delivery urgency if needed
            
            **Try saying:**
            • "Need materials for bathroom renovation"
            • "Order 100 concrete blocks"
            • "Get tools for electrical work"
            """)
    
    # Display transcribed text if available
    if st.session_state.voice_text:
        st.markdown("### 🎯 Transcribed Request")
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <div style="font-weight: 600; color: #065f46; margin-bottom: 10px;">
                📝 What you said:
            </div>
            <div style="color: #047857; font-size: 16px; line-height: 1.6;">
                "{st.session_state.voice_text}"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Process button
        if st.button("🤖 Process with AI", 
                    type="primary",
                    use_container_width=True,
                    key="process_voice"):
            
            with st.spinner("🔍 Analyzing your request..."):
                time.sleep(2)
                
                # Add to chat history
                st.session_state.voice_chat_messages.append({
                    "role": "user",
                    "content": st.session_state.voice_text
                })
                
                # Add AI response
                st.session_state.voice_chat_messages.append({
                    "role": "assistant",
                    "content": "I understand you need construction materials. Let me find the best options for you from our suppliers. Do you have any preferred brands or budget constraints?"
                })
                
                # Clear voice text
                st.session_state.voice_text = ""
            
            show_toast("✅ Request sent to AI assistant!", "success")
            st.rerun()


# ============================================================================
# IMAGE UPLOAD COMPONENT
# ============================================================================

def render_image_upload():
    """Modern image upload interface for construction materials"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 30px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    ">
        <div style="font-size: 64px; margin-bottom: 20px;">📷</div>
        <h2 style="margin: 0 0 10px 0; font-size: 28px;">Image-Based Procurement</h2>
        <p style="opacity: 0.9; font-size: 16px;">
            Upload photos of materials, handwritten lists, or construction sites
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload area
    uploaded_file = st.file_uploader(
        "Drag & drop or click to upload",
        type=['png', 'jpg', 'jpeg', 'heic'],
        help="Upload images of materials, shopping lists, or construction sites",
        key="image_uploader"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            st.markdown("""
            <div style="
                background: white;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #e5e7eb;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            ">
                <div style="font-weight: 600; color: #374151; margin-bottom: 15px;">
                    Image Details
                </div>
                <div style="color: #6b7280; font-size: 13px;">
                    <div style="margin-bottom: 8px;">📁 {filename}</div>
                    <div style="margin-bottom: 8px;">📏 {size} KB</div>
                    <div style="margin-bottom: 8px;">🖼️ {type}</div>
                </div>
            </div>
            """.format(
                filename=uploaded_file.name,
                size=uploaded_file.size // 1024,
                type=uploaded_file.type.split('/')[-1].upper()
            ), unsafe_allow_html=True)
        
        # Analyze button
        if st.button("🔍 Analyze Image with AI", 
                    type="primary",
                    use_container_width=True,
                    key="analyze_image"):
            
            with st.spinner("👀 AI is analyzing the image..."):
                time.sleep(3)
                
                # Sample analysis results
                sample_analyses = [
                    "I can see construction screws, safety gloves, and measuring tools in this image. Would you like me to order these items?",
                    "This appears to be a handwritten shopping list for electrical work. I can identify wire connectors, circuit breakers, and cable ties.",
                    "I recognize drywall materials, joint compound, and finishing tools in this photo. Need help ordering these?",
                    "This looks like a photo of plumbing supplies. I see pipes, fittings, and sealants. Shall I find suppliers for these?"
                ]
                
                analysis = random.choice(sample_analyses)
                
                # Add to chat history
                st.session_state.image_chat_messages.append({
                    "role": "user",
                    "content": "I uploaded an image of materials needed"
                })
                
                st.session_state.image_chat_messages.append({
                    "role": "assistant",
                    "content": analysis
                })
            
            show_toast("✅ Image analysis complete!", "success")
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
        ">
            <div style="font-size: 48px; margin-bottom: 20px; color: #667eea;">📤</div>
            <div style="font-weight: 600; color: #374151; font-size: 18px; margin-bottom: 10px;">
                Upload Construction Images
            </div>
            <div style="color: #6b7280; font-size: 14px; margin-bottom: 30px;">
                Supports photos, handwritten lists, screenshots, and material catalogs
            </div>
            
            <div style="
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                max-width: 500px;
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
                <div style="
                    background: white;
                    padding: 15px;
                    border-radius: 10px;
                    border: 1px solid #e5e7eb;
                ">
                    <div style="font-size: 24px; margin-bottom: 10px;">🏗️</div>
                    <div style="font-size: 13px; color: #374151; font-weight: 500;">Site Photos</div>
                </div>
                <div style="
                    background: white;
                    padding: 15px;
                    border-radius: 10px;
                    border: 1px solid #e5e7eb;
                ">
                    <div style="font-size: 24px; margin-bottom: 10px;">📋</div>
                    <div style="font-size: 13px; color: #374151; font-weight: 500;">Catalogs</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# FEEDBACK AND NOTIFICATION COMPONENTS
# ============================================================================

def show_toast(message, type="success"):
    """Show toast notification with animations"""
    colors = {
        "success": {"bg": "#10b981", "icon": "✅"},
        "error": {"bg": "#ef4444", "icon": "❌"},
        "warning": {"bg": "#f59e0b", "icon": "⚠️"},
        "info": {"bg": "#3b82f6", "icon": "ℹ️"}
    }
    
    toast_type = colors.get(type, colors["info"])
    
    # JavaScript for auto-dismiss
    js = f"""
    <script>
    function showToast() {{
        var toast = document.getElementById('toast-{type}');
        toast.style.display = 'block';
        setTimeout(function() {{
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-20px)';
            setTimeout(function() {{
                toast.style.display = 'none';
            }}, 300);
        }}, 3000);
    }}
    setTimeout(showToast, 100);
    </script>
    """
    
    # Toast HTML
    toast_html = f"""
    <div id="toast-{type}" style="
        position: fixed;
        top: 20px;
        right: 20px;
        background: {toast_type['bg']};
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        display: none;
        animation: slideInRight 0.3s ease;
        transition: all 0.3s ease;
        max-width: 350px;
        display: flex;
        align-items: center;
        gap: 12px;
    ">
        <div style="font-size: 20px;">{toast_type['icon']}</div>
        <div style="font-size: 14px; line-height: 1.4;">{message}</div>
    </div>
    {js}
    """
    
    st.markdown(toast_html, unsafe_allow_html=True)


def render_loading_spinner(message="Loading..."):
    """Render an animated loading spinner"""
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 40px;
    ">
        <div class="loading-spinner" style="
            display: inline-block;
            width: 50px;
            height: 50px;
            border: 3px solid rgba(102, 126, 234, 0.3);
            border-radius: 50%;
            border-top-color: #667eea;
            animation: spin 1s ease-in-out infinite;
            margin-bottom: 20px;
        "></div>
        <div style="
            color: #667eea;
            font-weight: 600;
            font-size: 16px;
            margin-top: 15px;
        ">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def render_empty_state(icon="📦", title="No items found", message="Try adding some items to get started"):
    """Render empty state component"""
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 60px 40px;
        color: #9ca3af;
    ">
        <div style="font-size: 64px; margin-bottom: 20px;">{icon}</div>
        <div style="font-weight: 700; color: #6b7280; font-size: 20px; margin-bottom: 10px;">
            {title}
        </div>
        <div style="color: #9ca3af; font-size: 15px; max-width: 400px; margin: 0 auto;">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# STATISTICS AND METRICS COMPONENTS
# ============================================================================

def render_metric_card(title, value, change=None, icon="📊", color="#667eea"):
    """Render a modern metric card"""
    change_html = ""
    if change is not None:
        change_color = "#10b981" if change >= 0 else "#ef4444"
        change_icon = "↗️" if change >= 0 else "↘️"
        change_html = f"""
        <div style="
            font-size: 12px;
            color: {change_color};
            margin-top: 5px;
            display: flex;
            align-items: center;
            gap: 4px;
        ">
            {change_icon} {abs(change)}%
        </div>
        """
    
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    "
    onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 8px 25px rgba(0, 0, 0, 0.08)';"
    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 10px rgba(0, 0, 0, 0.04)';">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
            <div style="
                width: 40px;
                height: 40px;
                background: {color}20;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: {color};
                font-size: 20px;
            ">
                {icon}
            </div>
        </div>
        <div style="font-size: 12px; color: #6b7280; margin-bottom: 8px;">{title}</div>
        <div style="font-size: 28px; font-weight: 700; color: #1f2937;">{value}</div>
        {change_html}
    </div>
    """, unsafe_allow_html=True)


def render_progress_bar(label, value, max_value=100, color="#667eea"):
    """Render animated progress bar"""
    percentage = (value / max_value) * 100
    
    st.markdown(f"""
    <div style="margin: 20px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="font-size: 14px; color: #374151;">{label}</span>
            <span style="font-weight: 600; color: {color}; font-size: 14px;">{value}/{max_value}</span>
        </div>
        <div style="
            width: 100%;
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
        ">
            <div style="
                width: {percentage}%;
                height: 100%;
                background: linear-gradient(90deg, {color}, {color}80);
                border-radius: 4px;
                transition: width 0.5s ease;
                animation: shimmer 2s infinite;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# ORDER STATUS COMPONENTS
# ============================================================================

def render_order_status_badge(status):
    """Render order status badge with colors"""
    status_config = {
        "pending": {"color": "#f59e0b", "bg": "#fef3c7", "icon": "⏳"},
        "approved": {"color": "#10b981", "bg": "#d1fae5", "icon": "✅"},
        "shipped": {"color": "#3b82f6", "bg": "#dbeafe", "icon": "🚚"},
        "delivered": {"color": "#8b5cf6", "bg": "#ede9fe", "icon": "📦"},
        "cancelled": {"color": "#ef4444", "bg": "#fee2e2", "icon": "❌"}
    }
    
    config = status_config.get(status.lower(), status_config["pending"])
    
    return f"""
    <span style="
        background: {config['bg']};
        color: {config['color']};
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    ">
        {config['icon']} {status.title()}
    </span>
    """


def render_timeline_step(step, title, description, is_active=False, is_completed=False):
    """Render a timeline step for order tracking"""
    icon = "✅" if is_completed else "⏳" if is_active else "⚪"
    color = "#10b981" if is_completed else "#667eea" if is_active else "#9ca3af"
    
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: flex-start;
        gap: 15px;
        margin-bottom: 20px;
        position: relative;
    ">
        <div style="
            width: 32px;
            height: 32px;
            background: {color};
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 14px;
            flex-shrink: 0;
            z-index: 2;
        ">
            {icon}
        </div>
        <div style="flex: 1;">
            <div style="
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 5px;
            ">
                <div style="font-weight: 600; color: #374151; font-size: 14px;">Step {step}</div>
                <div style="font-weight: 700; color: #1f2937; font-size: 15px;">{title}</div>
            </div>
            <div style="color: #6b7280; font-size: 13px; line-height: 1.5;">
                {description}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# PRODUCT DESCRIPTION COMPONENT
# ============================================================================

def render_product_description(product):
    """Render product description card"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
        ">
            <div style="
                width: 80px;
                height: 80px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 36px;
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
            ">
                {product.get('icon', '🔩')}
            </div>
            <div>
                <div style="
                    font-weight: 800;
                    color: #1f2937;
                    font-size: 24px;
                    margin-bottom: 5px;
                ">{product['name']}</div>
                <div style="
                    color: #6b7280;
                    font-size: 14px;
                    margin-bottom: 10px;
                ">{product['description']}</div>
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 15px;
                ">
                    <div style="
                        background: rgba(102, 126, 234, 0.1);
                        color: #667eea;
                        padding: 6px 12px;
                        border-radius: 20px;
                        font-size: 13px;
                        font-weight: 600;
                    ">
                        🏢 {product['supplier']}
                    </div>
                    <div style="
                        background: rgba(16, 185, 129, 0.1);
                        color: #10b981;
                        padding: 6px 12px;
                        border-radius: 20px;
                        font-size: 13px;
                        font-weight: 600;
                    ">
                        📦 {product['category']}
                    </div>
                </div>
            </div>
        </div>
        
        <div style="
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
        ">
            <div style="
                background: white;
                padding: 15px;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            ">
                <div style="font-size: 12px; color: #6b7280; margin-bottom: 5px;">Unit Price</div>
                <div style="font-size: 24px; font-weight: 800; color: #667eea;">€{product['price']}</div>
            </div>
            <div style="
                background: white;
                padding: 15px;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            ">
                <div style="font-size: 12px; color: #6b7280; margin-bottom: 5px;">Availability</div>
                <div style="font-size: 18px; font-weight: 700; color: #10b981;">In Stock</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN EXPORTS
# ============================================================================

__all__ = [
    'render_sidebar',
    'render_product_card_modern',
    'render_order_summary',
    'render_chat_message',
    'render_chat_history',
    'render_chat_interface_modern',
    'render_voice_interface',
    'render_image_upload',
    'show_toast',
    'render_loading_spinner',
    'render_empty_state',
    'render_metric_card',
    'render_progress_bar',
    'render_order_status_badge',
    'render_timeline_step',
    'render_product_description'
]