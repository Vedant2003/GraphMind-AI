import streamlit as st
from newcon import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid


# **************************************** Utility Functions *************************

def generate_thread_id():
    return str(uuid.uuid4())


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def load_conversation(thread_id):
    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return state.values.get("messages", [])


def get_chat_title(thread_id):
    """
    Get the first user message and use it as the chat title.
    """

    messages = load_conversation(thread_id)

    for msg in messages:

        if isinstance(msg, HumanMessage):

            # Take first 30 characters
            title = msg.content[:30]

            # Add ... if message is longer
            if len(msg.content) > 30:
                title += "..."

            return title

    return "New Chat"


# **************************************** Session Setup ******************************

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()


if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()


# Add current thread
add_thread(st.session_state["thread_id"])


# **************************************** Sidebar UI *********************************

st.sidebar.title("🧠 GraphMind AI")


if st.sidebar.button(
    "➕ New Chat",
    use_container_width=True
):
    reset_chat()
    st.rerun()


st.sidebar.header("My Conversations")


# Show conversations in reverse order
for thread_id in st.session_state["chat_threads"][::-1]:

    # Get meaningful title
    chat_title = get_chat_title(thread_id)

    if st.sidebar.button(
        f"💬 {chat_title}",
        key=f"chat_{thread_id}",
        use_container_width=True
    ):

        # Set selected thread
        st.session_state["thread_id"] = thread_id

        # Load conversation
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:

            if isinstance(msg, HumanMessage):
                role = "user"
            else:
                role = "assistant"

            temp_messages.append(
                {
                    "role": role,
                    "content": msg.content
                }
            )

        # Update UI history
        st.session_state["message_history"] = temp_messages

        st.rerun()


# **************************************** Main UI ************************************

st.title("🧠 GraphMind AI")

st.caption("Powered by LangGraph + Ollama")


# Display conversation history
for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# **************************************** Chat Input *********************************

user_input = st.chat_input(
    "Type your message here..."
)


if user_input:

    # Add user message to UI history
    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # Display user message
    with st.chat_message("user"):

        st.markdown(user_input)


    # LangGraph configuration
    CONFIG = {

        "configurable": {
            "thread_id":
            st.session_state["thread_id"]
        },

        "metadata": {
            "thread_id":
            st.session_state["thread_id"]
        },

        "run_name":
        "chat_turn"
    }


    # **************************************** AI Response *****************************

    with st.chat_message("assistant"):

        ai_message = st.write_stream(

            message_chunk.content

            for message_chunk, metadata

            in chatbot.stream(

                {
                    "messages": [
                        HumanMessage(
                            content=user_input
                        )
                    ]
                },

                config=CONFIG,

                stream_mode="messages"
            )
        )


    # Add AI response to UI history
    st.session_state["message_history"].append(
        {
            "role": "assistant",
            "content": ai_message
        }
    )


    # Refresh sidebar after first message
    # This changes "New Chat" to the first message title
    st.rerun()
