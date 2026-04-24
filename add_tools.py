from pathlib import Path
import subprocess
import sys
import time


TOOLS_DIR = Path(__file__).parent / "tools"


def restart_server(server_path: str, port: int = 8011) -> dict:
    try:
        kill_cmd = (
            f'for /f "tokens=5" %a in (\'netstat -aon ^| findstr :{port} '
            f'^| findstr LISTENING\') do taskkill /F /PID %a'
        )
        subprocess.run(kill_cmd, shell=True)

        time.sleep(1)

        subprocess.Popen([sys.executable, server_path])

        return {"status": "Server restarted successfully"}

    except Exception as e:
        return {"error": str(e)}


def add_tool(name: str, description: str, code: str, server_path: str) -> dict:
    """
    Creates tool file + restarts MCP server
    """

    try:
        file_path = TOOLS_DIR / f"{name}.py"

        content = f"""
TOOL_NAME = "{name}"
TOOL_DESCRIPTION = "{description}"

import sys
import json

{code}

if __name__ == "__main__":
    input_json = json.loads(sys.stdin.read())
    output = execute(input_json)
    print(json.dumps(output))
"""

        #  Write tool file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        #  Restart server
        restart_result = restart_server(server_path)

        if "error" in restart_result:
            return restart_result

        return {
            "message": "Tool added successfully",
            "tool_file": str(file_path),
            "server_status": restart_result
        }

    except Exception as e:
        return {"error": str(e)}