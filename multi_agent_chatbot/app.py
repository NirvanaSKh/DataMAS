import streamlit as st
import spacy
import os
import pandas as pd
import json
from agents.query_analysis import detect_intent
from agents.data_query import query_database
from agents.data_analysis import analyze_data
from agents.graph_rules import determine_graph_type
from agents.build_table import build_table
from agents.build_graph import build_graph
from utils.memory import ChatMemory

# ✅ Define the correct model path
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models/en_core_web_md")

# ✅ Load spaCy model from the correct directory
try:
    nlp = spacy.load(MODEL_PATH)
except OSError:
    st.warning("spaCy model not found! Downloading...")
    import spacy.cli
    spacy.cli.download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")

# ✅ Initialize chat memory
memory = ChatMemory()

# ✅ Streamlit UI
st.title("💬 Multi-Agent AI Chatbot")

# ✅ Chat history display
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    st.write(message)

# ✅ User input
user_input = st.text_input("Ask a question:")

if user_input:
    # ✅ Store user query in memory
    memory.store_query(user_input)

    # ✅ Determine user intent
    intent = detect_intent(user_input, nlp)

    # ✅ Handle different intents
    if intent == "database_query":
        query_result = query_database(user_input)
        data_analysis = analyze_data(query_result)
        
        # ✅ Display a table if structured data is detected
        if isinstance(query_result, pd.DataFrame):
            st.write("### 📊 Query Results")
            st.dataframe(query_result)
        
        # ✅ Determine graph type
        graph_type = determine_graph_type(data_analysis)

        # ✅ Generate graph if applicable
        if graph_type:
            st.write("### 📈 Generated Graph")
            fig = build_graph(query_result, graph_type)
            st.pyplot(fig)
    
    elif intent == "chat_memory":
        previous_queries = memory.retrieve_queries()
        st.write("### 🔍 Previous Questions")
        st.write(previous_queries)

    else:
        st.write("🤖 Sorry, I didn’t understand that. Please try again.")

    # ✅ Save response to chat history
    st.session_state.chat_history.append(f"**You:** {user_input}")
    st.session_state.chat_history.append(f"**Bot:** {intent}")

# ✅ Button to clear chat history
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.write("Chat cleared!")
