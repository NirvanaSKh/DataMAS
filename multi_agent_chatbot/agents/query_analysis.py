import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the spaCy language model
nlp = spacy.load("en_core_web_md")

# Predefined intents and associated SQL queries
INTENT_DICTIONARY = {
    "sales report": "SELECT * FROM sales_data",
    "customer trends": "SELECT * FROM customer_trends",
    "product performance": "SELECT * FROM product_data",
    "monthly revenue": "SELECT month, revenue FROM revenue_data",
    "top customers": "SELECT customer_name, total_spent FROM customers ORDER BY total_spent DESC LIMIT 10"
}

# Convert intent labels into embeddings
intent_embeddings = {intent: nlp(intent).vector for intent in INTENT_DICTIONARY.keys()}

def detect_intent(user_query):
    """Detects intent using NLP-based similarity matching."""
    query_vector = nlp(user_query).vector  # Convert user query into vector
    
    # Compute cosine similarity with each intent
    similarities = {intent: cosine_similarity([query_vector], [vector])[0][0] 
                    for intent, vector in intent_embeddings.items()}
    
    # Get the best match
    best_match = max(similarities, key=similarities.get)
    best_score = similarities[best_match]
    
    # If similarity score is below threshold, return None
    if best_score < 0.6:
        return None  # No confident match found
    
    return INTENT_DICTIONARY[best_match]
