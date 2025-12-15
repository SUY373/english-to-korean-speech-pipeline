from __future__ import annotations
from pathlib import Path
from pydub import AudioSegment


def ensure_wav_16k_mono(input_path: str | Path, out_path: str | Path) -> str:
    """
    Convert any audio file to 16kHz mono WAV (PCM).
    Requires ffmpeg installed (pydub backend).
    """
    input_path = Path(input_path)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(out_path, format="wav")
    return str(out_path)
