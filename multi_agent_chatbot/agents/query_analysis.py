from fuzzywuzzy import process

# Sample intent dictionary
INTENT_DICTIONARY = {
    "sales report": "SELECT * FROM sales_data",
    "customer trends": "SELECT * FROM customer_trends",
    "product performance": "SELECT * FROM product_data"
}

def detect_intent(user_query):
    best_match, score = process.extractOne(user_query, INTENT_DICTIONARY.keys())

    if score > 70:
        return INTENT_DICTIONARY[best_match]
    return None
