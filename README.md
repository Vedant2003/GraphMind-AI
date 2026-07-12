# 🧠 GraphMind AI

GraphMind AI is a conversational AI chatbot built using **LangGraph**, **Ollama**, and **Streamlit**. It runs a local Large Language Model (LLM) using Ollama and uses LangGraph with SQLite checkpointing to maintain conversation state.

## ✨ Features

* 🤖 Local AI chatbot powered by Ollama
* 🧠 Mistral LLM integration
* 🔗 LangGraph-based conversational workflow
* 💾 Persistent conversation state using SQLite
* ⚡ Streaming AI responses
* 💬 Interactive Streamlit chat interface
* 🔐 No paid API key required
* 🏠 Runs locally on your machine

## 🛠️ Tech Stack

* Python
* LangGraph
* LangChain
* Ollama
* Mistral
* Streamlit
* SQLite

## 📁 Project Structure

```text
GraphMind-AI/
│
├── newcon.py           # LangGraph backend
├── newcon1.py          # Streamlit frontend
├── chatbot.db          # SQLite database (generated automatically)
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└─
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd GraphMind-AI
```

### 2. Create a virtual environment

```bash
python -m venv myenv
```

Activate it on Windows:

```bash
myenv\\Scripts\\activate
```

For Git Bash:

```bash
source myenv/Scripts/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Install Ollama on your system and make sure the Ollama service is running.

### 5. Download the Mistral model

```bash
ollama pull mistral
```

Check the installed models:

```bash
ollama list
```

### 6. Run the application

```bash
streamlit run newcon1.py
```

The Streamlit application will open in your browser.

## 🏗️ How It Works

The application consists of two main components.

### Backend

`newcon.py` creates a LangGraph workflow with a conversational state containing the message history.

The workflow follows this structure:

```text
START
  ↓
Chat Node
  ↓
Mistral via Ollama
  ↓
END
```

The `SqliteSaver` checkpointer stores conversation states in `chatbot.db`, allowing LangGraph to maintain conversations using unique thread IDs.

### Frontend

`newcon1.py` provides the Streamlit user interface. It:

* Accepts user messages
* Maintains the current chat session
* Sends messages to the LangGraph workflow
* Streams responses from the local Mistral model
* Displays the conversation in a chat-style interface

## 🚀 Future Improvements

Planned features include:

* Meaningful AI-generated conversation titles
* Multiple saved conversations in the sidebar
* Load previous conversations
* Rename and delete conversations
* Support for multiple Ollama models
* Document upload and RAG
* Improved user interface
* Docker support

## 🎯 Learning Objectives

This project demonstrates practical experience with:

* Building stateful LLM applications
* LangGraph state management
* Conversation checkpointing
* Local LLM integration with Ollama
* Streaming LLM responses
* Building interactive AI applications with Streamlit

## 👨‍💻 Author

**Vedant Agnihotri**

## 📄 License

This project is intended for learning and portfolio purposes.
