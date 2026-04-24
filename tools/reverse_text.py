
TOOL_NAME = "reverse_text"
TOOL_DESCRIPTION = "Reverse input text"

import sys
import json


def execute(input_data):
    text = input_data.get("text", "")
    return {"result": text[::-1]}



if __name__ == "__main__":
    input_json = json.loads(sys.stdin.read())
    output = execute(input_json)
    print(json.dumps(output))
