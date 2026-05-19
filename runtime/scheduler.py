from runtime.bus import (
    event_bus
)

from runtime.messages import (
    MessageType
)

from runtime.queues import (
    audio_queue,
    stt_queue,
    tts_queue
)

from runtime.logger import (
    info
)

def scheduler_loop():

    while True:

        message = event_bus.get()

        # =====================
        # AUDIO ROUTING
        # =====================

        if (
            message.type ==
            MessageType.AUDIO_PCM
        ):

            info(
                "ROUTE AUDIO → STT"
            )

            audio_queue.put(
                message.payload
            )

        # =====================
        # TRANSCRIPTION
        # =====================

        elif (
            message.type ==
            MessageType.TRANSCRIPTION
        ):

            info(
                "ROUTE TEXT → LLM"
            )

            stt_queue.put(
                message.payload
            )

        # =====================
        # TTS
        # =====================

        elif (
            message.type ==
            MessageType.TTS_REQUEST
        ):

            info(
                "ROUTE RESPONSE → TTS"
            )

            tts_queue.put(
                message.payload
            )

        # =====================
        # INTERRUPT
        # =====================

        elif (
            message.type ==
            MessageType.INTERRUPT
        ):

            info(
                "GLOBAL INTERRUPT"
            )
