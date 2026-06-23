# ==========================================
# stt/whisper_engine.py
# ==========================================

import whisper
import numpy as np
import traceback
import torch
from runtime.logger import (
    info,
    error
)

DEVICE:str = "cuda" if torch.cuda.is_available() else "cpu"

info(
    f"WHISPER LOADING ON {DEVICE}"
)

MODEL = whisper.load_model(
    "small.en",
    device=DEVICE
)

info(
    "WHISPER READY"
)

def transcribe_stream(audio_pcm)->str:

    try:

        audio = (
            np.frombuffer(
                audio_pcm,
                dtype=np.int16
            )
            .astype(np.float32)
            / 32768.0
        )

        result:dict[str,str] = MODEL.transcribe(
            audio,
            fp16=False,
            language="en",
            temperature=0
        )

        text:str = (
            result["text"]
            .strip()
        )

        return text

    except Exception:

        error(
            "WHISPER ERROR"
        )

        traceback.print_exc()

        return ""
