# 🤖 Local Ollama Chatbot with LangChain

A modular Python chatbot that uses **LangChain** to communicate with a local **Ollama** instance. This project is designed to run completely offline on your local machine.

## 📋 Prerequisites

Before running the code, ensure you have **Ollama** installed and the required models pulled:

1. **Install Ollama:** [ollama.com](https://ollama.com)
2. **Start the Service:**
```bash
sudo systemctl start ollama

```


3. **Download Models:**
```bash
ollama pull llama3.2:1b
```



---

## 🚀 Installation & Setup

1. first setup your virtual environment and activate:  
`venv` or `uv` or `any`

2. Install packages from requirements.txt:
```bash
pip install -r requirements.txt
# or
uv add -r requirements.txt
``` 
3. run project:
```bash
streamlit run app.py
```

---

and **Start chatting:** with the `llama3.2:1b` model.



## ⚙️ How it Works

This project uses the `langchain-ollama` partner package to interface with the Ollama generation API. By default, it connects to `http://localhost:11434`.

Models are loaded into system memory (RAM) upon the first request and remain there for 5 minutes of inactivity before being automatically unloaded to save resources.

---
