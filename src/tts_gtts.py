from __future__ import annotations
from pathlib import Path
from gtts import gTTS


def synthesize_ko_mp3(text_ko: str, out_mp3_path: str) -> str:
    """
    Korean text -> Korean speech (mp3)
    """
    text_ko = (text_ko or "").strip()
    if not text_ko:
        raise ValueError("Korean text is empty; cannot synthesize TTS.")

    out_path = Path(out_mp3_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    tts = gTTS(text=text_ko, lang="ko")
    tts.save(str(out_path))
    return str(out_path)
