import whisper
import torch

def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("medium", device=device)
    return model

def transcribe(model, audio_path: str) -> str:
    try:
        result = model.transcribe(audio_path)
        return result["text"].strip()
    except Exception as e:
        return f"Error transcribing: {str(e)}"