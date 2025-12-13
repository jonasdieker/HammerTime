import streamlit as st
import pandas as pd
import random
from datetime import datetime
import requests

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="Procurement Assistant", layout="wide")

# Custom CSS for clean, modern UI matching mockups
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background-color: #F1F5F9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
        padding-top: 1rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown h1 {
        color: #1E3A5F !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        padding: 0.5rem 1rem;
    }
    
    /* Navigation Items */
    .nav-item {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0.5rem;
        border-radius: 8px;
        color: #64748B;
        text-decoration: none;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .nav-item:hover {
        background-color: #F1F5F9;
        color: #1E3A5F;
    }
    
    .nav-item.active {
        background-color: #EFF6FF;
        color: #2563EB;
    }
    
    .nav-icon {
        margin-right: 0.75rem;
        font-size: 1.1rem;
    }
    
    /* Main Content Cards */
    .content-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    
    /* Product Cards */
    .product-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        transition: all 0.2s;
    }
    
    .product-card:hover {
        border-color: #2563EB;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.1);
    }
    
    .product-icon {
        width: 48px;
        height: 48px;
        background-color: #F1F5F9;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-size: 1.5rem;
    }
    
    .product-info {
        flex: 1;
    }
    
    .product-name {
        font-weight: 600;
        color: #1E3A5F;
        margin-bottom: 0.25rem;
    }
    
    .product-desc {
        font-size: 0.875rem;
        color: #64748B;
    }
    
    /* Order Summary Card */
    .summary-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .summary-title {
        font-weight: 700;
        color: #1E3A5F;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    
    .summary-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #F1F5F9;
    }
    
    .summary-total {
        display: flex;
        justify-content: space-between;
        padding: 1rem 0 0.5rem;
        font-weight: 700;
        color: #1E3A5F;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s !important;
    }
    
    .stButton button[kind="primary"] {
        background-color: #2563EB !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton button[kind="primary"]:hover {
        background-color: #1D4ED8 !important;
    }
    
    .stButton button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #2563EB !important;
        border: 2px solid #2563EB !important;
    }
    
    /* Search Input */
    .stTextInput input {
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
    }
    
    .stTextInput input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* Number Input */
    .stNumberInput input {
        border-radius: 8px !important;
        text-align: center !important;
    }
    
    /* Section Headers */
    .section-header {
        font-weight: 700;
        color: #1E3A5F;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Text colors */
    .stMarkdown, p, span, label {
        color: #334155 !important;
    }
    
    h1, h2, h3, h4 {
        color: #1E3A5F !important;
    }
    
    /* Recommendation Card */
    .recommendation-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .recommendation-header {
        font-weight: 700;
        color: #1E3A5F;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .supplier-name {
        font-weight: 600;
        color: #2563EB;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    .rec-item {
        color: #334155;
        margin-bottom: 0.5rem;
    }
    
    .lead-time {
        color: #64748B;
        font-size: 0.9rem;
        margin-top: 0.75rem;
    }
    
    .savings-badge {
        background-color: #DCFCE7;
        color: #166534;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    /* Voice Input Button */
    .voice-btn {
        background-color: #EFF6FF;
        border: 2px solid #2563EB;
        border-radius: 50%;
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .voice-btn:hover {
        background-color: #2563EB;
        color: white;
    }
    
    /* Order Details Table */
    .order-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .order-table th {
        text-align: left;
        padding: 0.75rem;
        background-color: #F8FAFC;
        color: #64748B;
        font-weight: 600;
        font-size: 0.85rem;
        border-bottom: 1px solid #E2E8F0;
    }
    
    .order-table td {
        padding: 0.75rem;
        border-bottom: 1px solid #F1F5F9;
        color: #334155;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA (Simulating products from CSV) ---
PRODUCTS = [
    {"id": "C001", "name": "Screw A", "description": "M4×20 stainless", "category": "Fasteners", "price": 0.03, "supplier": "Supplier A", "icon": "🔩"},
    {"id": "C002", "name": "Screw B", "description": "M4×25 stainless", "category": "Fasteners", "price": 0.04, "supplier": "Supplier A", "icon": "🔩"},
    {"id": "C003", "name": "Screw C", "description": "M5×30 zinc", "category": "Fasteners", "price": 0.05, "supplier": "Supplier B", "icon": "🔩"},
    {"id": "C004", "name": "Washer", "description": "for M4", "category": "Fasteners", "price": 0.01, "supplier": "Supplier B", "icon": "⚙️"},
    {"id": "C005", "name": "Wall Plugs", "description": "6mm (Box 100)", "category": "Fasteners", "price": 10.00, "supplier": "Fischer", "icon": "🔧"},
    {"id": "C006", "name": "Work Gloves", "description": "Size 9", "category": "PPE", "price": 2.50, "supplier": "Uvex", "icon": "🧤"},
]

# --- 3. SESSION STATE ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""
if 'recommendation' not in st.session_state:
    st.session_state.recommendation = None
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'last_search_query' not in st.session_state:
    st.session_state.last_search_query = ""
if 'cart_version' not in st.session_state:
    st.session_state.cart_version = 0  # Used to reset number inputs after order

# --- 4. HELPER FUNCTIONS ---
def add_to_cart(product, qty, add_mode=True):
    """Add product to cart. If add_mode=True, adds qty to existing. If False, sets qty."""
    if qty > 0:
        # Check if product already in cart
        for item in st.session_state.cart:
            if item['id'] == product['id']:
                if add_mode:
                    item['qty'] += qty
                else:
                    item['qty'] = qty
                return
        st.session_state.cart.append({**product, "qty": qty})

def set_cart_qty(product, qty):
    """Set the quantity of a product in cart (replaces existing qty)"""
    if qty > 0:
        for item in st.session_state.cart:
            if item['id'] == product['id']:
                item['qty'] = qty
                return
        st.session_state.cart.append({**product, "qty": qty})
    else:
        # If qty is 0, remove from cart
        remove_from_cart(product['id'])

def remove_from_cart(product_id):
    st.session_state.cart = [item for item in st.session_state.cart if item['id'] != product_id]

def calculate_total():
    return sum(item['price'] * item['qty'] for item in st.session_state.cart)

def place_order():
    total = calculate_total()
    status = "Pending Approval" if total > 200 else "Auto-Approved"
    
    new_order = {
        "Order ID": f"ORD-{random.randint(1000, 9999)}",
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Requester": "Site Foreman",
        "Total (EUR)": total,
        "Status": status,
        "Items": st.session_state.cart.copy()
    }
    st.session_state.orders.insert(0, new_order)
    st.session_state.cart = []
    st.session_state.cart_version += 1  # Reset number input widgets
    return status

def navigate_to(page):
    st.session_state.current_page = page

# --- 5. SIDEBAR NAVIGATION ---
def render_sidebar():
    with st.sidebar:
        st.markdown("## Procurement Assistant")
        st.markdown("---")
        
        # Navigation buttons
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

# --- 6. ORDER SUMMARY COMPONENT ---
def render_order_summary():
    st.markdown("### Order Summary")
    
    if not st.session_state.cart:
        st.markdown("*Your cart is empty*")
        return
    
    # Display cart items
    for item in st.session_state.cart:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{item['name']}**")
            st.caption(f"{item['qty']} pcs")
        with col2:
            subtotal = item['price'] * item['qty']
            st.markdown(f"€{subtotal:.2f}")
    
    st.markdown("---")
    
    # Total
    total = calculate_total()
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("**Total**")
    with col2:
        st.markdown(f"**€{total:.2f}**")
    
    st.markdown("")
    
    # Place Order Button
    if st.button("Place order", type="primary", use_container_width=True):
        status = place_order()
        if status == "Pending Approval":
            st.info(f"Order sent for approval")
        else:
            st.success(f"Order placed successfully!")
        st.rerun()

# --- 7. PRODUCT DESCRIPTION COMPONENT ---
def render_product_description(product):
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

# --- 8. DASHBOARD VIEW ---
def dashboard_view():
    # Main content area with two columns
    main_col, summary_col = st.columns([2.5, 1])
    
    with main_col:
        # Product Search Section
        st.markdown("### Product Search")
        
        # Search with button
        search_col, btn_col = st.columns([4, 1])
        with search_col:
            search_query = st.text_input(
                "Search",
                placeholder="Search by product or task (e.g. 'Drywall', '500 screws M4')",
                label_visibility="collapsed",
                value=st.session_state.last_search_query
            )
        with btn_col:
            search_clicked = st.button("Search", use_container_width=True)
        
        # Clear results button
        if st.session_state.search_results:
            if st.button("Clear Results", type="secondary"):
                st.session_state.search_results = None
                st.session_state.last_search_query = ""
                st.rerun()
        
        # AI Search Results from Backend - fetch new results on search click
        if search_query and search_clicked:
            st.session_state.last_search_query = search_query
            with st.spinner(f"🔍 Searching for: {search_query}"):
                try:
                    response = requests.post(
                        "http://localhost:8000/receive_user_prompt",
                        json={"prompt": search_query}
                    )
                    response.raise_for_status()
                    response_data = response.json()
                    
                    if response_data and "items" in response_data and "explanation" in response_data:
                        # Store results in session state
                        api_items = response_data["items"]
                        recommendations = []
                        
                        for api_item in api_items:
                            recommendations.append({
                                "id": api_item.get("artikel_id"),
                                "name": api_item.get("artikelname"),
                                "qty": api_item.get("anzahl"),
                                "price": api_item.get("preis_stk"),
                                "category": api_item.get("kategorie"),
                                "supplier": api_item.get("lieferant"),
                                "subtotal": api_item.get("preis_stk", 0) * api_item.get("anzahl", 0)
                            })
                        
                        st.session_state.search_results = {
                            "explanation": response_data['explanation'],
                            "recommendations": recommendations,
                            "requireApproval": response_data.get("requireApproval", False)
                        }
                    else:
                        st.error("Invalid response format from API.")
                        st.session_state.search_results = None
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"API request failed: {str(e)}")
                    st.session_state.search_results = None
                except Exception as e:
                    st.error(f"Error processing request: {str(e)}")
                    st.session_state.search_results = None
        
        # Display stored search results (persists across reruns)
        if st.session_state.search_results:
            results = st.session_state.search_results
            recommendations = results["recommendations"]
            
            st.success("✨ AI Recommendation")
            st.markdown(f"**{results['explanation']}**")
            
            st.divider()
            st.markdown("### Recommended Materials")
            
            if recommendations:
                # Add All button
                col_spacer, col_btn = st.columns([3, 1])
                with col_btn:
                    if st.button("Add All to Cart", type="primary", use_container_width=True):
                        for rec in recommendations:
                            add_to_cart(rec, rec["qty"])
                        st.toast(f"✅ Added {len(recommendations)} items to cart!")
                
                st.divider()
                
                # Display each recommendation
                for idx, rec in enumerate(recommendations):
                    with st.container(border=True):
                        c1, c2, c3, c4 = st.columns([0.5, 2, 1, 1])
                        with c1:
                            st.markdown("<div style='font-size: 2rem; text-align: center;'>🔩</div>", unsafe_allow_html=True)
                        with c2:
                            st.markdown(f"**{rec['name']}**")
                            st.caption(f"{rec['category']} | {rec['supplier']}")
                        with c3:
                            st.markdown(f"**Qty: {rec['qty']}**")
                            st.caption(f"€{rec['subtotal']:.2f}")
                        with c4:
                            if st.button("Add", key=f"rec_{rec['id']}_{idx}", use_container_width=True):
                                add_to_cart(rec, rec["qty"])
                                st.toast(f"✅ Added {rec['name']} to cart!")
                
                # Total estimate
                total_estimate = sum(r["subtotal"] for r in recommendations)
                st.divider()
                st.metric("Total Estimate", f"€{total_estimate:.2f}")
                
                if results.get("requireApproval", False):
                    st.info("⚠️ This order will require approval (over budget threshold)")
            else:
                st.warning("No matching items found in catalog.")
        
        # Show helpful message when no search yet
        if not st.session_state.search_results:
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem; color: #64748B;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                <h3 style="color: #1E3A5F; margin-bottom: 0.5rem;">Search for materials</h3>
                <p>Describe what you need and our AI will recommend the best products.</p>
                <p style="font-size: 0.9rem; color: #94A3B8;">Try: "500 stainless screws M4×20 with washers"</p>
            </div>
            """, unsafe_allow_html=True)
    
    with summary_col:
        # Order Summary
        with st.container(border=True):
            render_order_summary()

# --- 9. VOICE REQUEST VIEW (Create Request) ---
def voice_request_view():
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        # Voice Input Section
        with st.container(border=True):
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div style="background-color: #EFF6FF; border: 2px solid #2563EB; border-radius: 50%; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.25rem;">🎤</span>
                </div>
                <div style="background-color: #F8FAFC; border-radius: 8px; padding: 0.75rem 1rem; flex: 1;">
                    <span style="color: #64748B;">Click microphone to speak...</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🎤 Start Voice Input", use_container_width=True):
                st.session_state.voice_text = "need 500 stainless screws M4×20 with washers"
                st.rerun()
        
        # Create Request Text Input
        with st.container(border=True):
            st.markdown("### Create Request")
            request_text = st.text_area(
                "Request",
                value=st.session_state.voice_text,
                placeholder="need 500 stainless screws M4×20 with washers",
                height=80,
                label_visibility="collapsed"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("Submit Request", type="primary", use_container_width=True):
                    if request_text:
                        # Call backend API
                        try:
                            response = requests.post(
                                "http://localhost:8000/receive_user_prompt",
                                json={"prompt": request_text}
                            )
                            if response.ok:
                                data = response.json()
                                st.session_state.recommendation = {
                                    "supplier": "Supplier B",
                                    "items": data.get("items", []),
                                    "explanation": data.get("explanation", ""),
                                    "lead_time": "2 days",
                                    "savings": "32%"
                                }
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
    
    with col2:
        # Recommendation Panel
        with st.container(border=True):
            st.markdown("### Recommendation")
            
            if st.session_state.recommendation:
                rec = st.session_state.recommendation
                st.markdown(f"**{rec.get('supplier', 'Supplier B')}**")
                
                # Display items
                for item in rec.get('items', []):
                    name = item.get('artikelname', item.get('name', 'Item'))
                    qty = item.get('anzahl', item.get('qty', 0))
                    price = item.get('preis_stk', item.get('price', 0)) * qty
                    st.markdown(f"{qty} {name} - €{price:.2f}")
                
                st.markdown(f"*Lead time: {rec.get('lead_time', '2 days')}*")
                st.markdown(f"<span style='background-color: #DCFCE7; color: #166534; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem;'>{rec.get('savings', '32%')} less wastage</span>", unsafe_allow_html=True)
                
                st.markdown("")
                col_a, col_m = st.columns(2)
                with col_a:
                    if st.button("Approve", type="primary", use_container_width=True):
                        # Add items to cart
                        for item in rec.get('items', []):
                            product = {
                                'id': item.get('artikel_id', item.get('id')),
                                'name': item.get('artikelname', item.get('name')),
                                'price': item.get('preis_stk', item.get('price', 0)),
                                'qty': item.get('anzahl', item.get('qty', 0))
                            }
                            st.session_state.cart.append(product)
                        st.session_state.recommendation = None
                        navigate_to("Dashboard")
                        st.rerun()
                with col_m:
                    if st.button("Modify", use_container_width=True):
                        navigate_to("Dashboard")
                        st.rerun()
            else:
                st.markdown("*Submit a request to get AI recommendations*")
    
    # Order Details Table
    if st.session_state.recommendation and st.session_state.recommendation.get('items'):
        st.markdown("### Order Details")
        items = st.session_state.recommendation['items']
        
        table_data = []
        for item in items:
            table_data.append({
                "Item": item.get('artikelname', item.get('name', '')),
                "Description": item.get('kategorie', item.get('description', '')),
                "Quantity": f"{item.get('anzahl', item.get('qty', 0))} pcs",
                "Subtotal": f"€{item.get('preis_stk', item.get('price', 0)) * item.get('anzahl', item.get('qty', 0)):.2f}"
            })
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

# --- 10. ORDERS VIEW ---
def orders_view():
    st.markdown("### Order History")
    
    if st.session_state.orders:
        for order in st.session_state.orders:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"**{order['Order ID']}**")
                    st.caption(f"{order['Date']} • {order['Requester']}")
                with col2:
                    st.markdown(f"€{order['Total (EUR)']:.2f}")
                with col3:
                    status = order['Status']
                    if status == "Pending Approval":
                        st.warning(status)
                    elif status == "Auto-Approved" or status == "Approved":
                        st.success(status)
                    else:
                        st.info(status)
    else:
        st.info("No orders yet. Create a request or add products to your cart.")

# --- 11. REPORTS VIEW ---
def reports_view():
    st.markdown("### Reports & Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_orders = len(st.session_state.orders)
        st.metric("Total Orders", total_orders)
    
    with col2:
        total_spend = sum(o['Total (EUR)'] for o in st.session_state.orders) if st.session_state.orders else 0
        st.metric("Total Spend", f"€{total_spend:.2f}")
    
    with col3:
        pending = len([o for o in st.session_state.orders if o['Status'] == 'Pending Approval'])
        st.metric("Pending Approvals", pending)
    
    st.markdown("---")
    st.info("Detailed reports and analytics coming soon...")

# --- 12. MAIN APP ---
def main():
    render_sidebar()
    
    # Page Title based on current page
    if st.session_state.current_page == "Dashboard":
        # Add tabs for Dashboard and Create Request
        tab1, tab2 = st.tabs(["📦 Product Search", "🎤 Create Request"])
        
        with tab1:
            dashboard_view()
        
        with tab2:
            voice_request_view()
    
    elif st.session_state.current_page == "Orders":
        orders_view()
    
    elif st.session_state.current_page == "Reports":
        reports_view()

if __name__ == "__main__":
    main()
