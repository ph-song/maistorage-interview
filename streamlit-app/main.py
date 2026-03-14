import streamlit as st
import httpx
import settings
import time
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Hide Deploy button and position Clear Session button next to the menu
st.markdown("""
    <style>
    /* Hide the Deploy button */
    .stAppDeployButton {
        display: none;
    }
    /* Position the first button (Clear Session) to the top right */
    div[data-testid="stHeader"] {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-end;
        padding-right: 80px;
    }
    /* CSS to move a specific button to the header area */
    .header-btn-container {
        position: fixed;
        top: 12px;
        right: 80px;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# Place the Clear Session button in a fixed container
st.markdown('<div class="header-btn-container">', unsafe_allow_html=True)
if st.button("Clear Session"):
    st.session_state.messages = []
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.title("AI Chatbot")

# Initialize chat history and cookie storage
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_cookies" not in st.session_state:
    st.session_state.api_cookies = {}

# Display chat messages from history on app rerun       
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # 1. Define your configuration separately
            request_kwargs = {
                "url": settings.API_URL + "/chat",
                "params": {"message": prompt},
                "cookies": st.session_state.api_cookies,
                "timeout": 30.0  
            }

            # 2. Use unpacking and a Client for speed
            with httpx.Client() as client:
                with client.stream("POST", **request_kwargs) as response:
                    # Update stored cookies with any new ones from the response
                    if response.cookies:
                        st.session_state.api_cookies.update(dict(response.cookies))
                    
                    if response.status_code == 200:
                        # iter_lines handles the byte-to-string decoding
                        for line in response.iter_lines():
                            if line.startswith("data: "):
                                raw_data = line[6:].strip()
                                
                                # Skip empty lines or completion signals
                                if not raw_data or raw_data == "[DONE]":
                                    continue
                                
                                try:
                                    payload = json.loads(raw_data)
                                    if isinstance(payload, dict) and "text" in payload:
                                        full_response += payload["text"]
                                        message_placeholder.markdown(full_response + "▌")
                                    
                                except json.JSONDecodeError:
                                    continue
                        message_placeholder.markdown(full_response)
                    else:
                        error_msg = f"Error: {response.status_code}"
                        st.error(error_msg)
                        full_response = error_msg
                        message_placeholder.markdown(full_response)
                
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            logger.error(error_msg, exc_info=True)
            st.error(error_msg)
            full_response = error_msg
            message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
