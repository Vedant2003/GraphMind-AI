import sqlite3
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver

llm=ChatOllama(model="mistral",temperature=0.3)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    return {"messages":[llm.invoke(state["messages"])]}

conn=sqlite3.connect("chatbot.db",check_same_thread=False)
checkpointer=SqliteSaver(conn)
g=StateGraph(ChatState)
g.add_node("chat",chat_node)
g.add_edge(START,"chat")
g.add_edge("chat",END)
chatbot=g.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    ids=[]
    for cp in checkpointer.list(None):
        tid=cp.config["configurable"]["thread_id"]
        if tid not in ids:
            ids.append(tid)
    return ids
