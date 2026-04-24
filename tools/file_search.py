# TOOL_NAME = "file_search"
# TOOL_DESCRIPTION = "Search for a file by name in a base directory and return its full path"

# import sys
# import json
# import subprocess

# BASE_DIR = r"C:\Users\Pranav Bejgam\OneDrive - Xebia\Tasks\mcp_toolbox\tools"


# def execute(input_data): 
#     query = (
#         input_data.get("text") or 
#         input_data.get("file_name") or 
#         ""
#     ).strip()

#     if not query:
#         return {"error": "No filename provided."}

#     result = subprocess.run(
#         ["cmd", "/c", "dir", f"*{query}*", "/s", "/b", "/a-d"],
#         cwd=BASE_DIR,
#         capture_output=True,
#         text=True
#     )

#     matches = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]

#     if not matches:
#         return {"found": False, "query": query, "message": f"No file matching '{query}' found."}

#     return {"found": True, "query": query, "paths": matches}


# if __name__ == "__main__":
#     input_json = json.loads(sys.stdin.read())
#     print(json.dumps(execute(input_json), default=str))

TOOL_NAME = "file_search"
TOOL_DESCRIPTION = "Search for a file by name and return its full path. If it is a PDF, also extract and return its text content."

import sys
import json
import fitz
import camelot
from pathlib import Path

BASE_DIR = Path(r"C:\Users\Pranav Bejgam\OneDrive - Xebia\Tasks\mcp_toolbox\tools")


def find_file(query):
    return [str(p) for p in BASE_DIR.rglob("*") if p.is_file() and query.lower() in p.name.lower()]


def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    combined_text = ""

    for page_num in range(len(doc)):
        combined_text += f"\n--- Page {page_num + 1} Text ---\n"
        page = doc.load_page(page_num)

        tables = []
        try:
            tables = camelot.read_pdf(pdf_path, pages=str(page_num + 1))
        except:
            pass

        table_areas = []
        for table in tables:
            if hasattr(table, "_bbox"):
                table_areas.append(table._bbox)

        clean_text = ""
        for block in page.get_text("blocks"):
            x0, y0, x1, y1, text, *_ = block
            is_table_text = any(
                not (x1 < tx0 or x0 > tx1 or y1 < ty0 or y0 > ty1)
                for tx0, ty0, tx1, ty1 in table_areas
            )
            if not is_table_text:
                clean_text += text + "\n"

        combined_text += clean_text

        for i, table in enumerate(tables):
            combined_text += f"\n--- Table {i + 1} (Page {page_num + 1}) ---\n"
            combined_text += table.df.to_string()
            combined_text += "\n"

    return combined_text


def execute(input_data):
    query = (input_data.get("text") or input_data.get("file_name") or "").strip()

    if not query:
        return {"error": "No filename provided."}

    matches = find_file(query)

    if not matches:
        return {"found": False, "query": query, "message": f"No file matching '{query}' found."}

    path = matches[0]

    if path.lower().endswith(".pdf"):
        try:
            text = extract_text(path)
            return {
                "found": True,
                "query": query,
                "path": path,
                "all_paths": matches,
                "extracted_text": text
            }
        except Exception as e:
            return {
                "found": True,
                "query": query,
                "path": path,
                "all_paths": matches,
                "extraction_error": str(e)
            }

    return {"found": True, "query": query, "path": path, "all_paths": matches}


if __name__ == "__main__":
    input_json = json.loads(sys.stdin.read())
    print(json.dumps(execute(input_json), default=str))