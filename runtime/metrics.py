import time

class Metrics:

    def __init__(self)->None:

        self.start_time = 0

    def start(self)->None:

        self.start_time = time.time()

    def stop(self)->None:

        return (
            time.time()
            - self.start_time
        )

metrics = Metrics()
