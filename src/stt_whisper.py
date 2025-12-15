from __future__ import annotations
import whisper


def transcribe_en(audio_wav_path: str, model_size: str = "base") -> str:
    """
    English speech -> English text
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_wav_path, language="en")
    return (result.get("text") or "").strip()

