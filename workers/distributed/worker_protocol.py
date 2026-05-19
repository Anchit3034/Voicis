import json

def create_message(

    worker,

    msg_type,

    payload
):

    return json.dumps({

        "worker": worker,

        "type": msg_type,

        "payload": payload
    })

def parse_message(message):

    return json.loads(
        message
    )
