import os
import json
import requests
import config
import re

def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def add_comment(ci_tool, data):
    # Determine build tool
    if ci_tool == "bitbucket":
        bb_config = "BITBUCKET_PR_COMMENT_API"
    else:
        print("The CI Tool isn't configured")

    # Build the URL from the config.py file
    api_config = getattr(config, bb_config)
    api_url = ""
    pattern = r'\$'

    for value in api_config.values():    
        if value.startswith('$'):
            value = re.sub(pattern, '', value)
            value = os.environ[value]
            api_url += value
        else:
            api_url += value

    pr_comment_token = os.environ["PR_COMMENT_TOKEN"]
    
    json_string = json.dumps({"content": {"raw": data}})

    # Send the JSON string to the specified API URL
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + pr_comment_token, "Accept": "application/json" }
    response = requests.post(api_url, data=json_string, headers=headers)
    print(response.text)    