from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. Setup the Model
model = ChatOllama(model="llama3.2:1b")

# 2. Create the Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful and concise AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

# 3. Combine into a Chain
chain = prompt | model

# 4. Manage History (In-memory for this example)
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 5. Wrap with History Logic
wrapped_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 6. Start the Chat Loop
session_id = "user_123"
print("Chatbot started! (Type 'exit' to stop)")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
        
    response = wrapped_chain.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"AI: {response.content}")