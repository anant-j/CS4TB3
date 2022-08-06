# API layer to interface between Front-end (Jupyter Notebook) and Back-end
# (regexNL.py)

# Importing libraries
import json
from regexNL import parse
import base64
from urllib.parse import unquote

globalKeyVal = {}  # Key-val store to cache popular requests and conserve execution time


def lambda_handler(event, context):
    try:
        inputstr = event['body']
        try:
            decodedInput = str(base64.b64decode(inputstr))  # Decode base64 string
            finalInput = unquote(decodedInput.split("input=")[1])[:-1]  # Convert input from URL to Text Format
        except:
            finalInput = json.loads(inputstr)
            finalInput = finalInput["input"]
        print(finalInput)  # For logging
        result = ""
        if(finalInput in globalKeyVal):
            result = globalKeyVal[finalInput]  # Return from cache if present
        else:
            result = parse(finalInput)  # Compute results
            globalKeyVal[finalInput] = result  # Store in cache
        return {
            'statusCode': 200,
            'body': json.dumps(result) # Return result
        }
    except BaseException:
        return {
            'statusCode': 500
        }
