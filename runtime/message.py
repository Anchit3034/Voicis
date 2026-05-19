import time
class RuntimeMessage:

    def __init__(
        self,
        msg_type,
        payload
    ):

        self.type = msg_type

        self.payload = payload
        self.timestamp = time.time()
