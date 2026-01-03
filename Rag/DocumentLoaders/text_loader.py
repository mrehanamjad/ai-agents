# """
# # Document Loaders
# Use to load documents of differeny formate i.e `.docx`,`.pdf`,`.md`, etc
# in langchange
# """
# # - **TextLoader**

# import os
# from langchain_community.document_loaders import TextLoader

# current_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(current_dir, "crash_course_on_React.txt")

# loader = TextLoader(file_path,encoding="utf8")

# docs = loader.load()

# # print(docs) # type list
# # print(docs[0].page_content)
# print(docs[0].metadata)
# # print(docs[1]) # IndexError: list index out of range



import os
from langchain_community.document_loaders import TextLoader
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. LOAD THE DOCUMENT 
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "crash_course_on_React.txt")

# Ensure the file exists before loading
if not os.path.exists(file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Artificial Intelligence is transforming the world. Local LLMs like Ollama allow for private data processing.")

loader = TextLoader(file_path, encoding="utf8")
docs = loader.load()

# 2. INITIALIZE THE MODEL
# We use the llama3.2:1b model you have installed
llm = ChatOllama(model="llama3.2:1b", temperature=0.3)

# 3. CREATE THE PROMPT
# We create a template that accepts 'context' (the file content)
prompt = ChatPromptTemplate.from_template(
    """Answer the following question based ONLY on the provided context:
    
    Context: {context}
    
    Question: {question}
    """
)

# 4. BUILD THE CHAIN
# The pipe operator (|) links the prompt, the model, and the string parser
chain = prompt | llm | StrOutputParser()

# 5. EXECUTE
# We pass the content from docs[0] as the context
question = input("Enter your question: ") #"What is the main topic of the document?"
print("AI is thinking...", flush=True)
# Not Streaming
# response = chain.invoke({
#     "context": docs[0].page_content,
#     "question": question
# })
# print(f"--- Document Metadata ---\n{docs[0].metadata}")
# print(f"\n--- AI Response ---\n{response}")


# Streaming
for chunk in  chain.stream({
    "context": docs[0].page_content,
    "question": question
}):
    print(chunk, end="", flush=True)

print("\n\n--- Done ---")
print(f"--- Document Metadata ---\n{docs[0].metadata}")