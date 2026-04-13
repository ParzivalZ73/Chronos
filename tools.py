import anthropic
import os
import subprocess
from pathlib import Path


client = anthropic.Anthropic(
    base_url="http://localhost:11434",
    api_key="ollama"
)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def create_file(filename: str, content) -> str:
    try:
        # Fix: convert anything to string
        if isinstance(content, list):
            content = "\n".join(str(i) for i in content)
        elif not isinstance(content, str):
            content = str(content)
        filepath = OUTPUT_DIR / filename
        filepath.write_text(content, encoding="utf-8")
        return f"File '{filename}' created successfully at {filepath}"
    except Exception as e:
        return f"Error creating file: {str(e)}"


def write_code(filename: str, description) -> str:
    try:
        if not isinstance(description, str):
            description = str(description)
        response = client.messages.create(
            model="qwen2.5-coder:7b",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"Write Python code for: {description}. Return only the code, no explanation."
                }
            ]
        )
        code = response.content[0].text
        # Strip markdown code blocks if present
        if code.startswith("```"):
            lines = code.split("\n")
        # Remove first line (```python) and last line (```)
            lines = [l for l in lines if not l.strip().startswith("```")]
            code = "\n".join(lines).strip()

        filepath = OUTPUT_DIR / filename
        filepath.write_text(code, encoding="utf-8")
        return code
    except Exception as e:
        return f"Error writing code: {str(e)}"


def summarize(text) -> str:
    try:
        if not text or text is None:
            return "No text provided for summarization."
        if not isinstance(text, str):
            text = str(text)
        response = client.messages.create(
            model="qwen2.5-coder:7b",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"You are a summarizer. Read the following text and write a concise summary in 3-4 sentences. Do not repeat the original text. Write only the summary(short version).\n\nText to summarize:\n{text}\n\nSummary:"
                }
            ]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error summarizing: {str(e)}"


def general_chat(message) -> str:
    try:
        if not message or message is None:
            return "No message provided."
        if not isinstance(message, str):
            message = str(message)
        response = client.messages.create(
            model="qwen2.5-coder:7b",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        if response.content and len(response.content) > 0:
            return response.content[0].text
        return "No response from model."
    except Exception as e:
        return f"Error in chat: {str(e)}"
    

def run_code(filename: str) -> str:
    try:
        filepath = OUTPUT_DIR / filename

        if not filepath.exists():
            return f"❌ File '{filename}' not found in output folder."

        # Open VS Code in output folder
        subprocess.Popen(["code", str(OUTPUT_DIR)])

        # Run file in terminal (cross-platform safe)
        command = f'python "{filepath}"'

        if os.name == "nt":  # Windows
            subprocess.Popen(
                ["cmd", "/k", command],
                cwd=OUTPUT_DIR
            )

        return f" Running '{filename}' in terminal..."

    except Exception as e:
        return f" Error: {str(e)}"
    
def launch_file(filename: str) -> str:
    try:
        filepath = OUTPUT_DIR / filename

        # Create file if not exists
        if not filepath.exists():
            filepath.touch()
            created = True
        else:
            created = False

        # Open file in VS Code
        subprocess.Popen(["code", str(filepath)])

        if created:
            return f" Created and opened '{filename}' in VS Code."
        else:
            return f" Opened existing file '{filename}' in VS Code."

    except Exception as e:
        return f" Error: {str(e)}"