import threading
last_tts_time:int =0
interrupt_event = threading.Event()

speaking_event = threading.Event()

processing_event = threading.Event()
