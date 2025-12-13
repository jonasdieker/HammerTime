"""
Dashboard View - Product Search with AI recommendations
"""
import streamlit as st
import requests
from utils import add_to_cart
from components import render_order_summary
from config import API_BASE_URL


def dashboard_view():
    """Main dashboard view with product search"""
    main_col, summary_col = st.columns([2.5, 1])
    
    with main_col:
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
            if st.button("Clear Results", type="secondary", key="dashboard_clear_results"):
                st.session_state.search_results = None
                st.session_state.last_search_query = ""
                st.rerun()
        
        # AI Search Results from Backend
        if search_query and search_clicked:
            st.session_state.last_search_query = search_query
            with st.spinner(f"🔍 Searching for: {search_query}"):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/receive_user_prompt",
                        json={"prompt": search_query}
                    )
                    response.raise_for_status()
                    response_data = response.json()
                    
                    if response_data and "items" in response_data and "explanation" in response_data:
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
        
        # Display stored search results
        if st.session_state.search_results:
            results = st.session_state.search_results
            recommendations = results["recommendations"]
            
            st.success("✨ AI Recommendation")
            st.markdown(f"**{results['explanation']}**")
            
            st.divider()
            st.markdown("### Recommended Materials")
            
            if recommendations:
                col_spacer, col_btn = st.columns([3, 1])
                with col_btn:
                    if st.button("Add All to Cart", type="primary", use_container_width=True):
                        for rec in recommendations:
                            add_to_cart(rec, rec["qty"])
                        st.toast(f"✅ Added {len(recommendations)} items to cart!")
                
                st.divider()
                
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
        with st.container(border=True):
            render_order_summary(key_prefix="dashboard")

