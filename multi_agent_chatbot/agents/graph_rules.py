import json

def select_graph_type(data_type):
    with open("config/graph_rules.json", "r") as file:
        rules = json.load(file)

    return rules.get(data_type, "bar_chart")  # Default to bar chart if no match
