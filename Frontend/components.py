"""
Reusable UI components: sidebar, order summary, product description
"""
import streamlit as st
from utils import calculate_total, place_order, navigate_to
from config import AUTO_APPROVAL_LIMIT, ADMIN_PASSWORD


def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.markdown("## Procurement Assistant")
        st.markdown("---")
        
        pages = [
            ("🏠", "Dashboard"),
            ("📋", "Orders"),
            ("📊", "Reports")
        ]
        
        for icon, page in pages:
            is_active = st.session_state.current_page == page
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}  {page}", key=f"nav_{page}", use_container_width=True, type=btn_type):
                navigate_to(page)
                st.rerun()
        
        st.markdown("---")
        st.caption("Hackathon Demo v2.0")


def render_order_summary(key_prefix="default"):
    """Render the order summary component"""
    st.markdown("### Order Summary")
    
    if not st.session_state.cart:
        st.markdown("*Your cart is empty*")
        return
    
    for item in st.session_state.cart:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{item['name']}**")
            st.caption(f"{item['qty']} pcs")
        with col2:
            subtotal = item['price'] * item['qty']
            st.markdown(f"€{subtotal:.2f}")
    
    st.markdown("---")
    
    total = calculate_total()
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("**Total**")
    with col2:
        st.markdown(f"**€{total:.2f}**")
    
    # Show approval status
    requires_approval = total > AUTO_APPROVAL_LIMIT
    
    if requires_approval:
        st.warning(f"⚠️ Requires admin approval (over €{AUTO_APPROVAL_LIMIT})")
        admin_password = st.text_input(
            "Admin Password",
            type="password",
            placeholder="Enter admin password to approve",
            key=f"{key_prefix}_admin_password_input_{st.session_state.cart_version}"
        )
    else:
        st.success(f"✓ Auto-approved (under €{AUTO_APPROVAL_LIMIT})")
        admin_password = None
    
    st.markdown("")
    
    if st.button("Place order", type="primary", use_container_width=True, key=f"{key_prefix}_place_order_btn_{st.session_state.cart_version}"):
        if requires_approval:
            if admin_password == ADMIN_PASSWORD:
                status = place_order(custom_status="Admin Approved")
                st.success(f"✅ Order approved by admin!")
                st.rerun()
            elif admin_password:  # Wrong password entered
                status = place_order(custom_status="Order Declined")
                st.error("❌ Invalid password. Order declined.")
                st.rerun()
            else:  # No password entered
                st.warning("⚠️ Please enter admin password to place this order.")
        else:
            status = place_order()
            st.success(f"Order placed successfully!")
            st.rerun()


def render_product_description(product):
    """Render product description card"""
    st.markdown("### Product Description")
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 1rem;">
        <span style="font-size: 2rem;">{product.get('icon', '🔩')}</span>
        <div>
            <div style="font-weight: 600; color: #1E3A5F;">{product['name']}</div>
            <div style="color: #64748B; font-size: 0.9rem;">{product['description']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_chat_message(role, content):
    """Render a single chat message bubble"""
    if role == "user":
        # User message - right aligned, blue
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
            <div style="background-color: #2563EB; color: white; padding: 0.75rem 1rem; border-radius: 12px 12px 0 12px; max-width: 80%;">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Assistant message - left aligned, gray
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
            <div style="background-color: #F1F5F9; color: #1E3A5F; padding: 0.75rem 1rem; border-radius: 12px 12px 12px 0; max-width: 80%; border: 1px solid #E2E8F0;">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_chat_history():
    """Render the full chat history"""
    for msg in st.session_state.voice_chat_messages:
        render_chat_message(msg["role"], msg["content"])

