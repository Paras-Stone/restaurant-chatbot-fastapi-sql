"""
import re

def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(1) #1 gives group 2 of regex output
        #(testing) print(extracted_string)
        return extracted_string
    return ""

def get_str_from_food_dict(food_dict: dict):
    #(testing) result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
    #(testing) print(result)
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])


#(testing) extract_session_id("projects/foo/agent/sessions/123456789/contexts/context1")
#(testing) get_str_from_food_dict({"pizza":3,"burger":2})

#both function working
"""

import re

def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(1)
        print("📎 Extracted session_id:", extracted_string)
        return extracted_string
    return ""

def get_str_from_food_dict(food_dict: dict):
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
