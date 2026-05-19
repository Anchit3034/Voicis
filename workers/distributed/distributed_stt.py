import asyncio
import websockets
import torch

from runtime.gpu_message import (
    gpu_registration
)
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
    gpu_name = (

            torch.cuda.get_device_name(0))
            vram = round(torch.cuda.get_device_properties(0).total_memory / 1024**3,2)
            register_packet = gpu_registration(
                    "whisper",0,vram,"small.en")
            await websocket.send(register_packet)
asyncio.run(
    stt_worker()
)
