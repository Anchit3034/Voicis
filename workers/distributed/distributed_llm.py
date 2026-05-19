import asyncio
import websockets

from llm.ollama_runtime import (
    stream_llm
)

from workers.distributed.worker_protocol import (
    create_message,
    parse_message
)

SERVER = (
    "ws://localhost:8765"
)

async def llm_worker():

    async with websockets.connect(
        SERVER
    ) as websocket:

        print(
            "[LLM WORKER CONNECTED]"
        )

        while True:

            raw = await websocket.recv()

            message = parse_message(
                raw
            )

            if (
                message["type"] !=
                "transcription"
            ):
                continue

            text = message["payload"]

            response = ""

            for token in stream_llm(
                text
            ):

                response += token

            packet = create_message(

                "llm",

                "response",

                response
            )

            await websocket.send(
                packet
            )

asyncio.run(
    llm_worker()
)
