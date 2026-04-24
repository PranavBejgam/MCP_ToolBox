
TOOL_NAME = "calculator_subtract"
TOOL_DESCRIPTION = "Subtract two numbers"

import sys
import json

def execute(input_data):
    a = input_data.get("a", 0)
    b = input_data.get("b", 0)
    return {
        "result": a - b
    }

if __name__ == "__main__":
    input_json = json.loads(sys.stdin.read())
    output = execute(input_json)
    print(json.dumps(output))
