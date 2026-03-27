import json
import os

CASE_FILE = "cases.json"

def save_cases(user_id,query):
    data={}

    if os.path.exists(CASE_FILE):
        with open(CASE_FILE,"r") as f:
            data=json.load(f)

    if user_id not in data:
        data[user_id] = []

    data[user_id].append(query)

    with open(CASE_FILE,"w") as f:
        json.dump(data,f,indent=4)


def get_user_cases(user_id):
    if not os.path.exists(CASE_FILE):
        return []

    with open(CASE_FILE, "r") as f:
        data = json.load(f)

    return data.get(user_id, [])