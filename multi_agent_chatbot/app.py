import os
import streamlit as st
import psycopg2
import pandas as pd
import logging
import spacy

# Define the local model path
MODEL_PATH = "multi_agent_chatbot/models/en_core_web_md"

# Load spaCy model from local directory
try:
    nlp = spacy.load(MODEL_PATH)
except OSError:
    st.error("spaCy model not found! Please ensure en_core_web_md is stored locally.")
    raise SystemExit("Critical Error: spaCy model is missing.")

# Import agents
from config.db_config import get_db_connection
from agents.query_analysis import detect_intent
from agents.data_query import query_database
from agents.data_analysis import analyze_data
from agents.graph_rules import select_graph_type
from agents.build_table import build_table
from agents.build_graph import generate_graph
from utils.memory import get_chat_memory, update_chat_memory

# Configure logging
logging.basicConfig(filename="logs/error.log", level=logging.ERROR)

# Initialize Streamlit UI
st.title("Multi-Agent Chatbot with NLP Memory")

# Load chat memory
chat_memory = get_chat_memory()

# User Input
user_query = st.text_input("Ask me something about the database:")

if user_query:
    try:
        # Update chat memory
        previous_queries = chat_memory.get("history", [])
        previous_queries.append(user_query)
        update_chat_memory(previous_queries)

        # Step 1: Detect Intent
        intent = detect_intent(user_query)

        if not intent:
            st.write("I'm not sure what you're asking. Could you clarify?")
        else:
            # Step 2: Query Database
            query_result = query_database(intent)

            if query_result is None:
                st.write("I couldn't find relevant data. Can you rephrase?")
            else:
                # Step 3: Analyze Data
                data_type = analyze_data(query_result)

                # Step 4: Determine Graph Type
                graph_type = select_graph_type(data_type)

                # Step 5: Build Table
                table = build_table(query_result)
                st.write("### Data Table")
                st.write(table)

                # Step 6: Generate Graph
                if graph_type:
                    st.write("### Visualization")
                    generate_graph(query_result, graph_type)

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        st.write("Oops! Something went wrong. Please try again.")
