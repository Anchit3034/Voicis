import asyncio
import websockets
import json

async def client():

    uri = "ws://localhost:8765"

    async with websockets.connect(
        uri
    ) as websocket:

        print(
            "CONNECTED"
        )

        while True:

            message = await websocket.recv()

            data = json.loads(
                message
            )

            print(
                f"\n[{data['type']}]"
            )

            print(
                data['payload']
            )

asyncio.run(
    client()
)
