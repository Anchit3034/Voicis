from runtime.gpu_registry import (
    gpu_workers
)

from runtime.logger import (
    info,
    error
)

def get_worker(worker_type):

    worker = gpu_workers.get(
        worker_type
    )

    if not worker:

        error(
            f"NO GPU WORKER: "
            f"{worker_type}"
        )

        return None

    return worker
