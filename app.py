import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage

# Page config
st.set_page_config(page_title="Local AI Chat", page_icon="🦙")
st.title("🦙 Local Ollama Chat")

# Initialize model
llm = ChatOllama(model="phi:latest", temperature=0.4)

# Session state (memory)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Save User Message to History
    st.session_state.chat_history.append(HumanMessage(content=prompt))

    # Generate Assistant Response (Streaming)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Stream the response for a better UI experience
        for chunk in llm.stream(st.session_state.chat_history):
            full_response += chunk.content
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)

    # Save Assistant Message to History
    st.session_state.chat_history.append(AIMessage(content=full_response))
