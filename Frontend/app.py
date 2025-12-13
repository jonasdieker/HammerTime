import streamlit as st
import pandas as pd
import random
from datetime import datetime
import requests

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="Comstruct", layout="wide")

# FORCE LIGHT THEME STYLING (Includes Fix for Toast Notifications)
st.markdown("""
    <style>
    /* 1. Force Main Background to White */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 2. Force Sidebar to Light Grey */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }

    /* 3. FORCE ALL TEXT TO DARK BLUE/GREY */
    .stApp, .stMarkdown, p, h1, h2, h3, h4, h5, h6, span, div, label {
        color: #0F172A !important;
    }
    
    /* 4. FIX INPUT FIELDS (Search Bar & Number Inputs) */
    input[type="text"], input[type="number"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
    }
    div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
    }
    
    /* 5. FIX TOAST NOTIFICATIONS (The "Added to cart" popup) */
    div[data-testid="stToast"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #2563EB !important; /* Blue border to make it pop */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    /* 6. Metrics */
    [data-testid="stMetricValue"] {
        color: #2563EB !important; /* Primary Blue */
    }
    
    /* 7. Buttons */
    .stButton button {
        background-color: #FFFFFF;
        color: #2563EB !important;
        border: 1px solid #2563EB !important;
    }
    .stButton button:hover {
        background-color: #EFF6FF !important;
        color: #1D4ED8 !important;
        border-color: #1D4ED8 !important;
    }
    
    /* Primary Buttons (Filled Blue) */
    .stButton button[kind="primary"] {
        background-color: #2563EB !important;
        color: white !important;
        border: none !important;
    }
    .stButton button[kind="primary"]:hover {
        background-color: #1D4ED8 !important;
    }

    /* 8. Tables/Dataframes */
    [data-testid="stDataFrame"] {
        background-color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA (Simulating the CSV) ---
PRODUCTS = [
    {"id": "C001", "name": "Screws TX20 4x40 (Box 500)", "category": "Fasteners", "price": 40.00, "supplier": "Wurth"},
    {"id": "C004", "name": "Wall Plugs 6mm (Box 100)", "category": "Fasteners", "price": 10.00, "supplier": "Fischer"},
    {"id": "C019", "name": "Work Gloves Size 9", "category": "PPE", "price": 2.50, "supplier": "Uvex"},
    {"id": "C025", "name": "Painter Fleece", "category": "Site Supplies", "price": 18.00, "supplier": "Toom"},
    {"id": "C035", "name": "PU Foam Can", "category": "Chemicals", "price": 6.50, "supplier": "Illbruck"},
    {"id": "C056", "name": "LED Site Lamp", "category": "Electronics", "price": 29.00, "supplier": "Brennenstuhl"},
    {"id": "C046", "name": "Trash Bags 120L", "category": "Cleaning", "price": 0.80, "supplier": "Deiss"},
    {"id": "C047", "name": "Duct Tape Silver", "category": "Adhesives", "price": 6.90, "supplier": "Tesa"},
    {"id": "C048", "name": "Drill Bit Set", "category": "Tools", "price": 14.50, "supplier": "Bosch"},
]

# --- 3. SESSION STATE ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'orders' not in st.session_state:
    st.session_state.orders = []

# --- 4. HELPER FUNCTIONS ---
def add_to_cart(product, qty):
    st.session_state.cart.append({**product, "qty": qty})
    # The CSS above fixes this toast to be White background with Blue Text
    st.toast(f"Added {qty}x {product['name']} to cart", icon="✅")

def calculate_total():
    return sum(item['price'] * item['qty'] for item in st.session_state.cart)

def place_order():
    total = calculate_total()
    status = "Pending Approval" if total > 200 else "Auto-Approved"
    
    new_order = {
        "Order ID": f"ORD-{random.randint(1000, 9999)}",
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Requester": "Foreman Hans",
        "Total (EUR)": total,
        "Status": status,
        "Items": ", ".join([i['name'] for i in st.session_state.cart])
    }
    st.session_state.orders.insert(0, new_order) 
    st.session_state.cart = [] 
    return status

# --- 5. VIEW: FOREMAN ---
def foreman_view():
    st.title("Site Supplies | C-Materials")
    st.caption("Project: Munich-West")
    
    # --- Sidebar Cart ---
    with st.sidebar:
        st.header("Order Summary")
        if not st.session_state.cart:
            st.markdown("Your cart is empty.")
        else:
            cart_df = pd.DataFrame(st.session_state.cart)
            st.dataframe(
                cart_df[['name', 'qty', 'price']], 
                hide_index=True,
                column_config={
                    "name": "Item",
                    "qty": "Qty",
                    "price": st.column_config.NumberColumn("Price", format="€%.2f")
                }
            )
            
            total = calculate_total()
            st.divider()
            st.metric("Total Estimate", f"€{total:.2f}")
            
            # Budget Warning
            if total > 200:
                st.info("Notice: Orders over €200 require central approval.")
            
            if st.button("Place Order", type="primary", use_container_width=True):
                status = place_order()
                if status == "Pending Approval":
                    st.info(f"Order sent to procurement. Status: {status}")
                else:
                    st.success(f"Order placed successfully. Status: {status}")
                st.rerun()

    # --- Search / AI Assistant ---
    with st.container():
        st.subheader("Product Search")
        col1, col2 = st.columns([4, 1])
        with col1:
            ai_query = st.text_input("Search", placeholder="Search by product or task (e.g. 'Drywall')", label_visibility="collapsed")
        with col2:
            search_trigger = st.button("Search", use_container_width=True)

        response_data = None
        if ai_query and search_trigger:
            st.info(f"Searching for: {ai_query}")
            try:
                response = requests.post("http://localhost:8000/receive_user_prompt", json={"prompt": ai_query})
                response.raise_for_status()
                response_data = response.json()
                print(f"API Response: {response_data}")

                # Parse the new API response format
                if response_data and "items" in response_data and "explanation" in response_data:
                    import json
                    
                    # Display explanation
                    st.success("✨ AI Recommendation")
                    st.markdown(f"**{response_data['explanation']}**")
                    
                    st.divider()
                    st.subheader("Recommended Materials")
                    
                    # Get items directly from response
                    api_items = response_data["items"]
                    
                    # Create recommendations list - items already have all data from API
                    recommendations = []
                    for api_item in api_items:
                        article_id = api_item.get("artikel_id")
                        article_name = api_item.get("artikelname")
                        count = api_item.get("anzahl")
                        price = api_item.get("preis_stk")
                        categorie = api_item.get("kategorie")
                        supplier = api_item.get("lieferant")
                                                
                        recommendations.append({
                            "product_id": article_id,
                            "name": article_name,
                            "recommended_qty": count,
                            "subtotal": price * count,
                            "category": categorie,
                            "supplier": supplier
                        })

                    # Display recommendations
                    if recommendations:
                        # Add all button
                        col_btn1, col_btn2 = st.columns([3, 1])
                        with col_btn2:
                            if st.button("Add All to Cart", type="primary", use_container_width=True):
                                for rec in recommendations:
                                    add_to_cart(rec, rec["recommended_qty"])
                                st.success(f"Added {len(recommendations)} items to cart!")
                                st.rerun()
                        
                        st.divider()
                        
                        # Display each recommendation
                        for idx, rec in enumerate(recommendations):
                            with st.container(border=True):
                                c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                                with c1:
                                    st.markdown(f"**{rec['name']}**")
                                    st.caption(f"{rec['category']} | {rec['supplier']}")
                                with c2:
                                    st.markdown(f"**Qty: {rec['recommended_qty']}**")
                                with c3:
                                    st.markdown(f"€{rec['subtotal']:.2f}")
                                with c4:
                                    if st.button("Add", key=f"rec_{rec['product_id']}_{idx}", use_container_width=True):
                                        # Add price field for add_to_cart
                                        rec_with_price = {**rec, "id": rec['product_id'], "price": rec['subtotal'] / rec['recommended_qty']}
                                        add_to_cart(rec_with_price, rec["recommended_qty"])
                                        st.rerun()
                        
                        # Total estimate
                        total_estimate = sum(r["subtotal"] for r in recommendations)
                        st.divider()
                        st.metric("Total Estimate", f"€{total_estimate:.2f}")
                        
                        # Show approval status
                        if response_data.get("requireApproval", False):
                            st.info("⚠️ This order will require approval (over budget threshold)")
                    else:
                        st.warning("No matching items found in catalog.")
                else:
                    st.error("Invalid response format from API - missing required fields.")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"API request failed: {str(e)}")
            except json.JSONDecodeError as e:
                st.error(f"Failed to parse JSON: {str(e)}")
            except KeyError as e:
                st.error(f"Missing expected field in response: {str(e)}")
            except Exception as e:
                st.error(f"Error processing request: {str(e)}")
                print(f"Error details: {e}")

    st.divider()


# --- 6. VIEW: PROCUREMENT ADMIN ---
def procurement_view():
    st.title("Procurement Console")
    st.caption("Administration / C-Materials")
    
    st.divider()

    # Metrics
    if st.session_state.orders:
        df_orders = pd.DataFrame(st.session_state.orders)
        total_spend = df_orders["Total (EUR)"].sum()
        pending_count = len(df_orders[df_orders["Status"] == "Pending Approval"])
    else:
        total_spend = 0
        pending_count = 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Spend (Month)", f"€{total_spend:.2f}")
    m2.metric("Pending Approvals", pending_count)
    m3.metric("Active Suppliers", "5")

    st.markdown("### Recent Orders")
    
    if st.session_state.orders:
        df = pd.DataFrame(st.session_state.orders)
        
        # Interactive Table
        st.dataframe(
            df, 
            use_container_width=True,
            column_config={
                "Total (EUR)": st.column_config.NumberColumn(format="€%.2f"),
                "Date": st.column_config.TextColumn("Time")
            }
        )
        
        # Approval Workflow
        pending_orders = [o for o in st.session_state.orders if o["Status"] == "Pending Approval"]
        
        if pending_orders:
            st.divider()
            st.subheader("Approval Queue")
            
            c_select, c_action = st.columns([3, 1])
            with c_select:
                order_to_approve = st.selectbox(
                    "Select Order to Review", 
                    options=[o["Order ID"] for o in pending_orders],
                    format_func=lambda x: f"{x} - {next(o['Requester'] for o in pending_orders if o['Order ID'] == x)}"
                )
            with c_action:
                st.write("") 
                st.write("") 
                if st.button("Approve Order", type="primary", use_container_width=True):
                    for order in st.session_state.orders:
                        if order["Order ID"] == order_to_approve:
                            order["Status"] = "Approved"
                    st.success(f"Order {order_to_approve} successfully approved.")
                    st.rerun()
    else:
        st.info("No orders found in the system.")

# --- 7. MAIN APP ROUTER ---
def main():
    # Sidebar Navigation
    with st.sidebar:
        st.title("comstruct")
        view_mode = st.radio("Select View", ["Foreman (Site)", "Procurement (Office)"])
        st.divider()
        st.caption("Hackathon Demo v1.0")
    
    if "Foreman" in view_mode:
        foreman_view()
    else:
        procurement_view()

if __name__ == "__main__":
    main()