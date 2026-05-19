import asyncio
import websockets

from tts.speaker import (
    speak_stream
)

from workers.distributed.worker_protocol import (
    create_message,
    parse_message
)

SERVER = (
    "ws://localhost:8765"
)

async def tts_worker():

    async with websockets.connect(
        SERVER
    ) as websocket:

        print(
            "[TTS WORKER CONNECTED]"
        )

        while True:

            raw = await websocket.recv()

            message = parse_message(
                raw
            )

            if (
                message["type"] !=
                "tts"
            ):
                continue

            speak_stream(
                message["payload"]
            )

asyncio.run(
    tts_worker()
)
