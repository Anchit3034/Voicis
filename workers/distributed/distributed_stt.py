import asyncio
import websockets

from stt.whisper_engine import (
    transcribe_stream
)

from workers.distributed.worker_protocol import (
    create_message,
    parse_message
)

SERVER = (
    "ws://localhost:8765"
)

async def stt_worker():

    async with websockets.connect(
        SERVER
    ) as websocket:

        print(
            "[STT WORKER CONNECTED]"
        )

        while True:

            raw = await websocket.recv()

            message = parse_message(
                raw
            )

            if (
                message["type"] !=
                "audio"
            ):
                continue

            audio_bytes = (
                message["payload"]
                .encode("latin1")
            )

            text = transcribe_stream(
                audio_bytes
            )

            response = create_message(

                "stt",

                "transcription",

                text
            )

            await websocket.send(
                response
            )

asyncio.run(
    stt_worker()
)
