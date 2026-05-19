# ==========================================
# workers/audio_worker.py
# ==========================================
import time
import ctypes
import threading
import asyncio

from runtime.async_bus import (
    event_bus
)
from runtime.events import Event


from runtime.message import (
    RuntimeMessage
)
from runtime.loop import (
    runtime_loop
)
from runtime.messages import (
    MessageType
)
from runtime.queues import (
    audio_queue,
    event_queue
)
from runtime.signals import (
    interrupt_event
)
CHUNK_SIZE = 480

# ==========================================
# LOAD C LIB
# ==========================================

lib = ctypes.CDLL(
    "./audio/libsegmenter.so"
)

lib.init_audio()

lib.read_audio.argtypes = [
    ctypes.POINTER(ctypes.c_short)
]

buffer = (
    ctypes.c_short * CHUNK_SIZE
)()

# ==========================================
# GLOBAL FLAGS
# ==========================================

recording_event = threading.Event()

shutdown_event = threading.Event()

# ==========================================
# INPUT THREAD
# ==========================================

def input_loop():
    
    while True:

        cmd = input(
            "\n[ENTER=start/stop | q=quit] > "
        )

        # =====================
        # QUIT
        # =====================

        if cmd.lower() == "q":

            print(
                "\n[SHUTDOWN]"
            )

            shutdown_event.set()

            recording_event.clear()

            break

        # =====================
        # TOGGLE RECORDING
        # =====================

        if recording_event.is_set():

            recording_event.clear()

        else:

            recording_event.set()

# ==========================================
# AUDIO LOOP
# ==========================================

def audio_loop():

    threading.Thread(
        target=input_loop,
        daemon=True
    ).start()

    while not shutdown_event.is_set():

        # =====================
        # WAIT FOR RECORD
        # =====================

        recording_event.wait()

        if shutdown_event.is_set():
            break

        print(
            "\n[RECORDING STARTED]"
        )
        interrupt_event.set()
        time.sleep(0.1)
        interrupt_event.clear()
        event_queue.put(
            Event.SPEECH_STARTED
        )

        frames = []

        while recording_event.is_set():
            
            result = lib.read_audio(
                buffer
            )

            if result <= 0:
                continue

            pcm_bytes = memoryview(
                buffer
            ).cast("B").tobytes()

            frames.append(
                pcm_bytes
            )

            print(
                ".",
                end="",
                flush=True
            )

            if shutdown_event.is_set():

                recording_event.clear()

                break

        # =====================
        # RECORDING STOPPED
        # =====================

        if not frames:
            continue

        print(
            "\n[RECORDING STOPPED]"
        )

        audio_pcm = b"".join(
            frames
        )

        print(
            f"[AUDIO BYTES] {len(audio_pcm)}"
        )

        try:

            asyncio.run_coroutine_threadsafe(
                    event_bus.put(RuntimeMessage(MessageType.AUDIO_PCM,audio_pcm)
                                  ),runtime_loop
                    )

        except Exception as e:

            print(
                f"[AUDIO QUEUE ERROR] {e}"
            )

        event_queue.put(
            Event.SPEECH_FINISHED
        )

    print(
        "\n[AUDIO WORKER EXITED]"
    )
