import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# --- Page Configuration ---
st.set_page_config(page_title="Llama 3.2 Streamer", page_icon="⚡", layout="centered")

st.title("⚡ Real-time AI Assistant")
st.caption("Chatting with Llama 3.2:1b via Ollama")
st.markdown("---")

# --- 1. Setup the Model ---
@st.cache_resource
def load_model():
    return ChatOllama(model="llama3.2:1b")

model = load_model()

# --- 2. Initialize Session State ---
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

# --- 3. Build the LangChain Logic ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful and concise AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | model
wrapped_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# --- 4. Sidebar ---
with st.sidebar:
    st.header("Control Panel")
    session_id = st.text_input("Session ID", value="user_123")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.store = {}
        st.session_state.generating = False
        st.rerun()

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
    
    # --- STOP BUTTON LOGIC ---
    # We place the button in a container so it appears above or below the generating text
    stop_button = st.button("Stop Generating", type="primary")
    
    if stop_button:
        st.session_state.generating = False
        st.rerun()

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # We iterate manually through the stream to allow for interruption
            for chunk in wrapped_chain.stream(
                {"input": last_user_prompt},
                config={"configurable": {"session_id": session_id}}
            ):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")
                
                # Check if the user pressed 'Stop' during the loop
                # Note: In Streamlit, a button click triggers a rerun, 
                # so the script usually restarts before this check completes.
                # However, this manual loop is necessary for clean state handling.
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.generating = False
            st.rerun()
            
        except Exception as e:
            st.session_state.generating = False
            st.rerun()