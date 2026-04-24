
TOOL_NAME = "uppercase_text"
TOOL_DESCRIPTION = "Convert text to uppercase"

import sys
import json


def execute(input_data):
    text = input_data.get("text", "")
    return {"result": text.upper()}


if __name__ == "__main__":
    input_json = json.loads(sys.stdin.read())
    output = execute(input_json)
    print(json.dumps(output))
