"""
Voice Request View - Conversational chat with voice input
"""
import streamlit as st
import requests
import speech_recognition as sr
from config import API_BASE_URL
from components import render_chat_message, render_chat_history, render_order_summary
from utils import add_to_cart


def send_message_to_chat(user_message: str):
    """Send a message to the chat API and handle the response"""
    # Add user message to chat history
    st.session_state.voice_chat_messages.append({
        "role": "user",
        "content": user_message
    })
    
    # Send to backend
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat_request",
            json={"messages": st.session_state.voice_chat_messages}
        )
        
        if response.ok:
            result = response.json()
            
            if result["type"] == "question":
                # AI is asking a clarifying question
                st.session_state.voice_chat_messages.append({
                    "role": "assistant",
                    "content": result["content"]
                })
            elif result["type"] == "recommendations":
                # AI has provided final recommendations
                st.session_state.voice_chat_recommendations = result["content"]
                explanation = result["content"].get("explanation", "Here are my recommendations:")
                st.session_state.voice_chat_messages.append({
                    "role": "assistant",
                    "content": f"✅ {explanation}"
                })
            elif result["type"] == "error":
                st.session_state.voice_chat_messages.append({
                    "role": "assistant",
                    "content": f"❌ Error: {result['content']}"
                })
        else:
            st.error(f"Backend Error: {response.status_code}")
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")


def voice_request_view():
    """Voice request view with conversational chat"""
    
    # Two column layout: main content + order summary
    main_col, summary_col = st.columns([3, 1])
    
    with main_col:
        st.markdown("### 🎤 Create Request")
        st.caption("Speak or type your material request. I'll ask clarifying questions if needed.")
        
        # Chat History Container
        chat_container = st.container()
        
        with chat_container:
            if st.session_state.voice_chat_messages:
                st.markdown("---")
                render_chat_history()
            else:
                st.info("💡 Start by clicking the microphone button or typing your request below.")
        
        # Voice Input Section
        st.markdown("---")
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("🎤 Speak", key="voice_chat_record", use_container_width=True, type="primary"):
                r = sr.Recognizer()
                r.energy_threshold = 300
                
                try:
                    with sr.Microphone() as source:
                        with st.spinner("🤫 Calibrating..."):
                            r.adjust_for_ambient_noise(source, duration=1)
                        
                        with st.spinner("🎙️ Listening..."):
                            audio = r.listen(source, timeout=5, phrase_time_limit=10)
                        
                        # Google Speech to Text
                        raw_text = r.recognize_google(audio)
                        st.toast(f"Heard: '{raw_text}'")
                        
                        # Send to chat
                        send_message_to_chat(raw_text)
                        st.rerun()
                        
                except sr.WaitTimeoutError:
                    st.warning("⚠️ No speech detected. Try speaking louder.")
                except sr.UnknownValueError:
                    st.warning("🤔 Could not understand audio. Try again.")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        with col2:
            # Text input for follow-up
            user_input = st.text_input(
                "Type your message",
                placeholder="e.g., 'I need 10 M4 screws and 2 pairs of gloves'",
                key="voice_chat_text_input",
                label_visibility="collapsed"
            )
        
        # Send button for text input
        col_send, col_clear = st.columns([1, 1])
        
        with col_send:
            if st.button("📤 Send", key="voice_chat_send", use_container_width=True):
                if user_input and user_input.strip():
                    send_message_to_chat(user_input.strip())
                    st.rerun()
        
        with col_clear:
            if st.button("🗑️ Clear Chat", key="voice_chat_clear", use_container_width=True):
                st.session_state.voice_chat_messages = []
                st.session_state.voice_chat_recommendations = None
                st.rerun()
        
        # Show Recommendations if available
        if st.session_state.voice_chat_recommendations:
            st.markdown("---")
            st.markdown("### 📦 Recommended Materials")
            
            recommendations = st.session_state.voice_chat_recommendations
            items = recommendations.get("items", [])
            
            if items:
                # Display items in a nice format
                for item in items:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{item.get('artikelname', item.get('artikel_id', 'Unknown'))}**")
                        st.caption(f"{item.get('kategorie', '')} | {item.get('lieferant', '')}")
                    
                    with col2:
                        st.markdown(f"Qty: **{item.get('anzahl', 0)}**")
                        st.caption(f"€{item.get('preis_stk', 0):.2f}/pc")
                    
                    with col3:
                        st.markdown(f"**€{item.get('preis_gesamt', 0):.2f}**")
                        if st.button("➕", key=f"add_chat_{item.get('artikel_id', '')}"):
                            product = {
                                'id': item.get('artikel_id', ''),
                                'name': item.get('artikelname', item.get('artikel_id', '')),
                                'price': item.get('preis_stk', 0),
                                'description': item.get('kategorie', ''),
                                'supplier': item.get('lieferant', ''),
                                'icon': '🔩'
                            }
                            add_to_cart(product, item.get('anzahl', 1))
                            st.toast(f"Added {item.get('artikelname', '')} to cart!")
                
                # Total and Add All button
                st.markdown("---")
                total = recommendations.get("total", 0)
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"### Total: €{total:.2f}")
                with col2:
                    if st.button("🛒 Add All to Cart", key="add_all_chat", type="primary", use_container_width=True):
                        for item in items:
                            product = {
                                'id': item.get('artikel_id', ''),
                                'name': item.get('artikelname', item.get('artikel_id', '')),
                                'price': item.get('preis_stk', 0),
                                'description': item.get('kategorie', ''),
                                'supplier': item.get('lieferant', ''),
                                'icon': '🔩'
                            }
                            add_to_cart(product, item.get('anzahl', 1))
                        st.success("✅ All items added to cart!")
                        st.session_state.voice_chat_recommendations = None
                        st.rerun()
    
    # Order Summary on the right
    with summary_col:
        with st.container(border=True):
            render_order_summary(key_prefix="voice_request")
