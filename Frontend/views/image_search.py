"""
Image Search View - Search products by uploading images
"""
import streamlit as st
from utils import add_to_cart
from components import render_order_summary


def image_search_view():
    """Image search view with upload and analysis"""
    main_col, summary_col = st.columns([2.5, 1])
    
    with main_col:
        st.markdown("### Image Search")
        st.markdown("Upload an image to search for similar products or identify materials.")
        
        with st.container(border=True):
            uploaded_file = st.file_uploader(
                "Upload Image",
                type=["png", "jpg", "jpeg"],
                label_visibility="collapsed"
            )
            
            if uploaded_file is not None:
                col_img, col_info = st.columns([1, 1])
                
                with col_img:
                    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
                
                with col_info:
                    st.markdown("### Image Analysis")
                    
                    if st.button("Analyze Image", type="primary", use_container_width=True):
                        with st.spinner("🔍 Analyzing image..."):
                            try:
                                # TODO: Call backend API for image analysis
                                st.session_state.image_search = {
                                    "analyzed": True,
                                    "recommendations": [],
                                    "explanation": "Image analysis coming soon..."
                                }
                                st.success("Image analyzed successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error analyzing image: {e}")
        
        st.markdown("### Search Results")
        
        if st.session_state.image_search and st.session_state.image_search.get("analyzed"):
            results = st.session_state.image_search
            
            st.info(results.get("explanation", "No explanation available"))
            
            recommendations = results.get("recommendations", [])
            if recommendations:
                st.markdown("### Identified Products")
                
                for idx, rec in enumerate(recommendations):
                    with st.container(border=True):
                        c1, c2, c3 = st.columns([0.5, 2.5, 1])
                        
                        with c1:
                            st.markdown("<div style='font-size: 2rem; text-align: center;'>🔩</div>", unsafe_allow_html=True)
                        
                        with c2:
                            st.markdown(f"**{rec['name']}**")
                            st.caption(f"{rec.get('category', 'Unknown')} | {rec.get('supplier', 'Unknown')}")
                        
                        with c3:
                            qty = st.number_input(
                                "Qty",
                                min_value=0,
                                value=rec.get('qty', 1),
                                step=1,
                                key=f"img_qty_{rec['id']}_{idx}",
                                label_visibility="collapsed"
                            )
                            if qty > 0:
                                if st.button("Add", key=f"img_add_{rec['id']}_{idx}", use_container_width=True):
                                    add_to_cart(rec, qty)
                                    st.toast(f"✅ Added {rec['name']} to cart!")
                            st.caption("pcs")
            
            if st.button("Clear Results", type="secondary", key="img_clear_results"):
                st.session_state.image_search = None
                st.rerun()
        else:
            st.info("Upload an image and click 'Analyze Image' to search for matching products.")
    
    with summary_col:
        with st.container(border=True):
            render_order_summary(key_prefix="image_search")

