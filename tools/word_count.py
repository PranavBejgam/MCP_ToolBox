
TOOL_NAME = "word_count"
TOOL_DESCRIPTION = "Count words and characters in text"

import sys
import json

def execute(input_data):
    text = input_data.get('text', '')
    words = text.split()
    return {'word_count': len(words), 'char_count': len(text)}

if __name__ == "__main__":
    input_json = json.loads(sys.stdin.read())
    output = execute(input_json)
    print(json.dumps(output))
