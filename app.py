import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage

# --- PAGE CONFIG ---
st.set_page_config(page_title="Local AI Chat", page_icon="🦙")
st.title("🦙 Local Ollama Chat")

# --- INITIALIZE MODEL ---
# Using phi:latest as you have it installed
llm = ChatOllama(model="phi:latest", temperature=0.4)

# --- SESSION STATE (Memory) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.chat_history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# --- CHAT INPUT ---
if prompt := st.chat_input("Type your message here..."):
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Save User Message to History
    st.session_state.chat_history.append(HumanMessage(content=prompt))

    # 3. Generate Assistant Response (Streaming)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Stream the response for a better UI experience
        for chunk in llm.stream(st.session_state.chat_history):
            full_response += chunk.content
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)

    # 4. Save Assistant Message to History
    st.session_state.chat_history.append(AIMessage(content=full_response))