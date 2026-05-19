import asyncio

event_bus = asyncio.Queue(
    maxsize=256
)
