from langchain_community.document_loaders import PyPDFLoader 
# only good for text pdf not images containg pdf etc for that we have others
# it convers each page into 1 document
# response is a list which length is no of pages of pdf 
import os

# 1. LOAD THE DOCUMENT 
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "crash_course_on_React.pdf")

if not os.path.exists(file_path):
    print(f"File '{file_path.split('/')[-1]}' does not exist.")
    exit(1)


loader = PyPDFLoader(file_path) 
docs = loader.load()

print("=========== complete docs with pages " + str(len(docs))+" =============")
print(docs)
print("================== page_content pg#1 =======================================================")
print(docs[0].page_content)
print("================== metadata pg#1 =======================================================")
print(docs[0].metadata)
print("================== pg#2 =======================================================")
print(docs[1])

