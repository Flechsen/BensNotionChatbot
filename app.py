# app.py

import time
import os
import streamlit as st
from utils import load_chain
company_logo = 'https://upload.wikimedia.org/wikipedia/commons/3/38/161130_CDTM_Logo_blau.svg'

############################################################################## 
################################# Benedikt ################################### 
############################################################################## 
# Header
st.header("🤖 CDTM AI Assistant 🤖")

# Below code used to display the company logo at the very top of page, instead of only for avatar in chat messages
# st.image(company_logo, width=30)  # controls size exactly

# Below is the code is used to adjust proportions of the avatar image in the chat messages
st.markdown("""
    <style>
        .stChatMessage img {
            width: 55px !important;
            height: 32px !important;
            object-fit: contain;
        }
    </style>
""", unsafe_allow_html=True)
############################################################################## 
################################# Benedikt ################################### 
############################################################################## 


# Initialize LLM chain in session_state
if 'chain' not in st.session_state:
    st.session_state['chain']= load_chain()

# Initialize chat history
if 'messages' not in st.session_state:
    # Start with first message from assistant
    st.session_state['messages'] = [{"role": "assistant", 
                                  "content": "Hi there! How can I help you today?"}]


# Display chat messages from history on app rerun
# Custom avatar for the assistant, default avatar for user
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=company_logo):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat logic
if query := st.chat_input("Ask me anything"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant", avatar=company_logo):
        message_placeholder = st.empty()
        # Temporarily blinded for Ben Experiment
        # result = st.session_state['chain']({"question": query})
        # response = result['answer']
        # full_response = ""
        
############################################################################## 
################################# Benedikt ################################### 
############################################################################## 
# use to get soruces
        result = st.session_state['chain']({"question": query})
        response = result["answer"]
        sources = result.get("source_documents", [])
        
        # Approach 1
        # with st.expander("Sources"):
        #     for i, doc in enumerate(sources):
        #         st.markdown(f"**Source {i+1}:** `{doc.metadata.get('source', 'unknown')}`")
        
        # Approach 2        
        # if sources:
        #     st.markdown("#### Sources:")
        #     for i, doc in enumerate(sources, 1):
        #         raw_source = doc.metadata.get("source", "Unknown")
        #         filename = os.path.basename(raw_source)          
        #         clean_name = os.path.splitext(filename)[0]       
        #         st.markdown(f"**Source {i}:** {clean_name}")
                
        # Approach 3                
        # with st.expander("Sources"):
        #     for i, doc in enumerate(sources, 1):
        #         raw_source = doc.metadata.get("source", "Unknown")
        #         filename = os.path.basename(raw_source)          
        #         clean_name = os.path.splitext(filename)[0]       
        #         st.markdown(f"**Source {i}:** {clean_name}")     
                
                
        # Approach 4   
        with st.expander("Sources"):
            unique_sources = set()
            for doc in sources:
                raw_source = doc.metadata.get("source", "Unknown")
                filename = os.path.basename(raw_source)
                clean_name = os.path.splitext(filename)[0]
                unique_sources.add(clean_name)

            for i, source in enumerate(sorted(unique_sources), 1):
                st.markdown(f"**Source {i}:** {source}")

############################################################################## 
################################# Benedikt ################################### 
############################################################################## 

        # Simulate stream of response with milliseconds delay
        full_response = ""
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
