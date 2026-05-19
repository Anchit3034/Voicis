import asyncio
import json
import websockets

from runtime.async_bus import (
    event_bus
)

from runtime.message import (
    RuntimeMessage
)

from runtime.messages import (
    MessageType
)

from runtime.logger import (
    info,
    error
)

clients = set()
workers={}
# ==========================================
# CLIENT HANDLER
# ==========================================

async def handle_client(
    websocket
):

    clients.add(websocket)

    info(
        "CLIENT CONNECTED"
    )
    worker_name = data.get(
    "worker")
    if worker_name:
        workers[worker_name] = websocket
    try:

        async for message in websocket:

            data = json.loads(
                message
            )

            msg_type = data.get(
                "type"
            )

            payload = data.get(
                "payload"
            )

            # =====================
            # AUDIO INPUT
            # =====================

            if msg_type == "audio":

                await event_bus.put(

                    RuntimeMessage(
                        MessageType.AUDIO_PCM,
                        payload.encode(
                            "latin1"
                        )
                    )
                )

            # =====================
            # INTERRUPT
            # =====================

            elif msg_type == "interrupt":

                await event_bus.put(

                    RuntimeMessage(
                        MessageType.INTERRUPT,
                        None
                    )
                )

    except Exception as e:

        error(
            f"CLIENT ERROR: {e}"
        )

    finally:

        clients.remove(
            websocket
        )

        info(
            "CLIENT DISCONNECTED"
        )

# ==========================================
# BROADCAST
# ==========================================
async def broadcast_message(
    msg_type,
    payload
):

    if not clients:
        return

    dead_clients = set()

    packet = json.dumps({

        "type": msg_type,

        "payload": payload
    })

    for client in clients:

        try:

            await client.send(
                packet
            )

        except:

            dead_clients.add(
                client
            )

    for dead in dead_clients:

        clients.remove(dead)

# ==========================================
# SERVER LOOP
# ==========================================

async def websocket_server():

    info(
        "WEBSOCKET SERVER STARTED"
    )

    async with websockets.serve(

        handle_client,

        "0.0.0.0",

        8765

    ):

        await asyncio.Future()
