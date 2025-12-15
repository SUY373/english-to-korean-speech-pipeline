from __future__ import annotations

import argparse
from pathlib import Path

import whisper
from googletrans import Translator

from src.audio_utils import ensure_wav_16k_mono
from src.tts_gtts import synthesize_ko_mp3


def stt_whisper_en(audio_wav_path: str, model_size: str = "base") -> str:
    """
    English speech -> English text (STT)
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(
        audio_wav_path,
        language="en",
        task="transcribe"
    )
    return (result.get("text") or "").strip()


def translate_en_to_ko(text_en: str) -> str:
    """
    English text -> Korean text using googletrans
    """
    text_en = (text_en or "").strip()
    if not text_en:
        return ""

    translator = Translator()
    result = translator.translate(text_en, src="en", dest="ko")
    return result.text.strip()


def run_pipeline(
    audio_in: str,
    out_dir: str = "outputs",
    whisper_model: str = "base",
    keep_converted_wav: bool = True,
) -> dict:
    out_dir_p = Path(out_dir)
    out_dir_p.mkdir(parents=True, exist_ok=True)

    audio_in_p = Path(audio_in)
    if not audio_in_p.exists():
        raise FileNotFoundError(f"Input audio not found: {audio_in}")

    # 0) Convert to 16kHz mono WAV
    converted_wav = out_dir_p / "input_16k_mono.wav"
    wav_path = ensure_wav_16k_mono(audio_in_p, converted_wav)

    # 1) STT (EN)
    text_en = stt_whisper_en(wav_path, model_size=whisper_model)
    (out_dir_p / "stt_en.txt").write_text(text_en, encoding="utf-8")

    # 2) Translation (EN -> KO)
    text_ko = translate_en_to_ko(text_en)
    (out_dir_p / "translated_ko.txt").write_text(text_ko, encoding="utf-8")

    # 3) TTS (KO)
    out_mp3 = str(out_dir_p / "result_ko.mp3")
    synthesize_ko_mp3(text_ko, out_mp3)

    if not keep_converted_wav:
        try:
            Path(wav_path).unlink(missing_ok=True)
        except Exception:
            pass

    return {
        "input_audio": str(audio_in_p),
        "converted_wav": wav_path,
        "stt_en": text_en,
        "translated_ko": text_ko,
        "tts_out": out_mp3,
        "out_dir": str(out_dir_p),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="audio_in", required=True, help="Input English audio (flac/wav/mp3).")
    parser.add_argument("--out", dest="out_dir", default="outputs", help="Output directory.")
    parser.add_argument("--whisper_model", default="base", help="Whisper model size.")
    parser.add_argument("--rm_wav", action="store_true", help="Remove intermediate wav.")
    args = parser.parse_args()

    result = run_pipeline(
        audio_in=args.audio_in,
        out_dir=args.out_dir,
        whisper_model=args.whisper_model,
        keep_converted_wav=not args.rm_wav,
    )

    print("\n=== PIPELINE RESULT ===")
    print(f"[INPUT]  {result['input_audio']}")
    print(f"[WAV]    {result['converted_wav']}")
    print("\n[1) STT - English]")
    print(result["stt_en"])
    print("\n[2) Translation - Korean]")
    print(result["translated_ko"])
    print(f"\n[3) TTS - Korean Audio]\n{result['tts_out']}")
    print(f"\n[FILES SAVED IN]\n{result['out_dir']}")


if __name__ == "__main__":
    main()
