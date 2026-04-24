from pathlib import Path
import importlib.util
import subprocess
import json
import sys
from fastmcp import FastMCP

TOOLS_DIR = Path(__file__).parent / "tools"

mcp = FastMCP("Dynamic MCP Toolbox Server")


def load_module(file_path: Path):
    try:
        spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
        if spec is None or spec.loader is None:
            return None

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    except Exception as e:
        print(f"❌ Failed to load module {file_path.name}: {e}")
        return None


def run_tool(file_path, input_data):
    try:
        result = subprocess.run(
            [sys.executable, str(file_path)],
            input=json.dumps(input_data),
            text=True,
            capture_output=True,
            timeout=20
        )

        if result.returncode != 0:
            return {"error": result.stderr}

        try:
            return json.loads(result.stdout)
        except:
            return {"error": "Invalid JSON output from tool"}

    except Exception as e:
        return {"error": str(e)}


def make_tool_runner(file_path):
    def wrapper(input_data: dict):
        return run_tool(file_path, input_data)
    return wrapper


def register_all_tools():
    for file_path in TOOLS_DIR.glob("*.py"):
        if file_path.name.startswith("_"):
            continue

        try:
            module = load_module(file_path)

            if module and hasattr(module, "TOOL_NAME"):
                print(f"Registering tool: {module.TOOL_NAME}")

                mcp.tool(
                    name=module.TOOL_NAME,
                    description=getattr(module, "TOOL_DESCRIPTION", module.TOOL_NAME)
                )(make_tool_runner(file_path))

        except Exception as e:
            print(f"❌ Error registering tool {file_path.name}: {e}")
            continue


# Initial registration
register_all_tools()


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8011
    )