import json

MEMORY_FILE = "chat_memory.json"

def get_chat_memory():
    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"history": []}

def update_chat_memory(new_history):
    with open(MEMORY_FILE, "w") as file:
        json.dump({"history": new_history}, file)
