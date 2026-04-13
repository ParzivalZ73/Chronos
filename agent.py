import anthropic
import json

client = anthropic.Anthropic(
    base_url="http://localhost:11434",
    api_key="ollama"
)

SYSTEM_PROMPT = """You are an intent classifier. Respond ONLY with a JSON object. No explanation. No markdown. No extra text.

Rules:
- If user mentions creating/making a file with content → intent: create_file
- If user mentions writing/creating code, a script, a function, a program → intent: write_code
- If user mentions summarize/summary/summarizing → intent: summarize
- If user mentions run/execute → intent: run_code
- If user mentions open/launch a file → intent: launch_file
- Everything else → intent: general_chat

JSON format:
{"intent": "write_code", "filename": "zenin.py", "content": null, "description": "hello function"}

User: "run the calculator file"
Response: {"intent": "run_code", "filename": "calculator.py", "content": null, "description": null}
User command:"""

def detect_intent(transcribed_text: str) -> dict:
    try:
        response = client.messages.create(
            model="qwen2.5-coder:7b",
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": transcribed_text
                }
            ]
        )
        
        raw = response.content[0].text.strip()
        result = json.loads(raw)
        return result
    
    except json.JSONDecodeError:
        return {
            "intent": "general_chat",
            "filename": None,
            "content": transcribed_text,
            "description": None
        }
    except Exception as e:
        return {
            "intent": "error",
            "filename": None,
            "content": str(e),
            "description": None
        }


def run_agent(transcribed_text: str) -> dict:
    from tools import create_file, write_code, summarize, general_chat
    
    intent_data = detect_intent(transcribed_text)
    intent = intent_data.get("intent")
    
    if intent == "create_file":
        filename = intent_data.get("filename") or "output.txt"
        if "." not in filename:
            filename = filename + ".txt"
        result = create_file(filename=filename, content=intent_data.get("content", ""))

    elif intent == "write_code":
        result = write_code(
            filename=intent_data.get("filename", "code.py"),
            description=intent_data.get("description", "")
        )
    elif intent == "summarize":
        text = intent_data.get("content") or transcribed_text
        result = summarize(text=text)
    elif intent == "general_chat":
        message = intent_data.get("content") or transcribed_text
        result = general_chat(message=message)

    elif intent == "run_code":
        from tools import run_code

        filename = intent_data.get("filename") or ""

    # Normalize filename
        if filename and "." not in filename:
            filename += ".py"

        if not filename:
            result = " No filename provided to run."
        else:
            result = run_code(filename=filename)


    elif intent == "launch_file":
            from tools import launch_file

            filename = intent_data.get("filename") or ""

    # Normalize filename
            if filename and "." not in filename:
                filename += ".py"

            if not filename:
                result = " No filename provided to open."
            else:
                result = launch_file(filename=filename)   

    else:
        result = f"Unknown intent or error: {intent_data.get('content')}"

    
    return {
        "intent": intent,
        "intent_data": intent_data,
        "result": result
    }