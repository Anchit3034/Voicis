from enum import Enum

class MessageType(Enum):

    AUDIO_PCM = 1

    TRANSCRIPTION = 2

    LLM_RESPONSE = 3

    TTS_REQUEST = 4

    INTERRUPT = 5

    STATE_CHANGE = 6
