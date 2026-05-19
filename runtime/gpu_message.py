import json

def gpu_registration(

    worker_name,

    gpu_id,

    vram,

    model
):

    return json.dumps({

        "type": "gpu_register",

        "worker": worker_name,

        "gpu_id": gpu_id,

        "vram": vram,

        "model": model
    })
