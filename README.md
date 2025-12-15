# 영어 음성 → 한국어 음성 변환 파이프라인

본 프로젝트는 **영어 음성을 입력으로 받아 한국어 음성으로 변환하는 End-to-End 음성 처리 파이프라인**을 구현한다.  
음성 인식(STT), 기계 번역(MT), 음성 합성(TTS)을 순차적으로 결합하여 하나의 자동화된 시스템으로 구성하였다.

---

## 1. 프로젝트 개요

### 입력 (Input)
- 영어 음성 파일  
- 지원 형식: `.wav`, `.flac`, `.mp3`

### 출력 (Output)
- 한국어 음성 파일 (`.mp3`)

### 파이프라인 구성
1. **음성 인식 (STT)**  
   - Whisper  
   - 영어 음성 → 영어 텍스트
2. **기계 번역 (MT)**  
   - googletrans  
   - 영어 텍스트 → 한국어 텍스트
3. **음성 합성 (TTS)**  
   - gTTS  
   - 한국어 텍스트 → 한국어 음성

---

## 2. 사용 데이터셋

### LibriSpeech – test-clean

- 데이터셋 이름: **LibriSpeech**
- 사용한 세부 데이터: **test-clean.tar.gz**
- 언어: 영어
- 오디오 형식: FLAC
- 샘플링 레이트: 16 kHz
- 용도: 음성 인식(STT) 입력 데이터

공식 홈페이지:  
https://www.openslr.org/12

---

## 3. 전체 파이프라인 구조

```
영어 음성 파일
        ↓
Whisper (STT)
영어 텍스트
        ↓
googletrans (번역)
한국어 텍스트
        ↓
gTTS (TTS)
한국어 음성 파일
```

---

## 4. 실행 환경 구성

### 요구 사항
- 운영체제: Windows / Linux / macOS
- Python 버전: 3.9 이상
- Conda 사용 권장

### 1) 가상환경 생성
```bash
conda create -n speech_pipeline python=3.9 -y
conda activate speech_pipeline
```

### 2) 필수 라이브러리 설치
```bash
pip install -r requirements.txt
conda install -c conda-forge ffmpeg -y
```

---

## 5. 실행 방법

```bash
python -m src.pipeline --in <입력_음성_파일_경로> --out outputs
```

예시:
```bash
python -m src.pipeline --in 61-70968-0000.flac --out outputs
```

---

## 6. 실행 결과물

```
outputs/
├─ input_16k_mono.wav
├─ stt_en.txt
├─ translated_ko.txt
└─ result_ko.mp3
```

---

## 7. 결론

본 프로젝트에서는 LibriSpeech의 `test-clean` 데이터셋을 사용하여  
영어 음성을 입력으로 받아 한국어 음성으로 변환하는  
완전한 음성 처리 파이프라인을 구현하였다.
