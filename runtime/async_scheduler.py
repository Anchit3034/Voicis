import asyncio

from runtime.async_bus import (
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

async def scheduler_loop():

    info(
        "ASYNC SCHEDULER STARTED"
    )

    while True:

        message = await event_bus.get()

        # =====================
        # AUDIO
        # =====================

        if (
            message.type ==
            MessageType.AUDIO_PCM
        ):

            info(
                "ASYNC ROUTE AUDIO"
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
                "ASYNC ROUTE TEXT"
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
                "ASYNC ROUTE TTS"
            )

            tts_queue.put(
                message.payload
            )

        await asyncio.sleep(0)
