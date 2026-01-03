import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# --- Page Configuration ---
st.set_page_config(page_title="Ollama Multi-Model Streamer", page_icon="⚡", layout="centered")

st.title("⚡ Real-time AI Assistant")

# --- 1. Sidebar (Model Selection & Controls) ---
with st.sidebar:
    st.header("Control Panel")
    
    # Model Selection Dropdown
    # Note: Ensure these models are already pulled in your Ollama instance
    model_options = ["llama3.2:1b","qwen2.5-coder:1.5b","qwen2.5-coder:3b","qwen2.5:3b"]
    selected_model = st.selectbox("Choose a Model", options=model_options, index=0)
    
    st.caption(f"Currently using: **{selected_model}**")
    st.markdown("---")
    
    session_id = st.text_input("Session ID", value="user_123")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.store = {}
        st.session_state.generating = False
        st.rerun()

# --- 2. Setup the Model ---
# We use the selected_model as a cache key so it reloads only when changed
@st.cache_resource
def load_model(model_name):
    return ChatOllama(model=model_name)

model = load_model(selected_model)

# --- 3. Initialize Session State ---
if "store" not in st.session_state:
    st.session_state.store = {}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "generating" not in st.session_state:
    st.session_state.generating = False

def get_session_history(session_id: str):
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]

# --- 4. Build the LangChain Logic ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful and concise AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

# The chain now uses the model instance derived from the sidebar selection
chain = prompt | model
wrapped_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# --- 5. Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. Chat Input & Streaming Logic ---
user_input = st.chat_input("What is on your mind?", disabled=st.session_state.generating)

if user_input:
    st.session_state.generating = True
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

if st.session_state.generating:
    last_user_prompt = st.session_state.messages[-1]["content"]
    
    stop_button = st.button("Stop Generating", type="primary")
    
    if stop_button:
        st.session_state.generating = False
        st.rerun()

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            for chunk in wrapped_chain.stream(
                {"input": last_user_prompt},
                config={"configurable": {"session_id": session_id}}
            ):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.generating = False
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.session_state.generating = False