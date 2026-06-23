

DEBUG:bool = False

def debug(message:str)->None:

    if DEBUG:

        print(
            f"[DEBUG] {message}"
        )

def info(message:str)->None:

    print(
        f"[INFO] {message}"
    )

def error(message:str)->None:

    print(
        f"[ERROR] {message}"
    )
