import ollama
import traceback
from typing import Iterator
from memory.context_manager import (
    build_context,
    add_response
)

MODEL:str = "tinyllama"

def stream_llm(prompt:str)->Iterator[str] | None:

    try:

        context:list[dict[str,str]] = build_context(
            prompt
        )

        response_text:str = ""

        stream: Iterator[ollama.ChatResponse] = ollama.chat(
            model=MODEL,
            messages=context,
            stream=True
        )

        for chunk in stream:

            try:

                token:str = (
                    chunk["message"]
                    ["content"]
                )

                response_text += token

                yield token

            except Exception:

                print(
                    "\n[OLLAMA TOKEN ERROR]"
                )

                traceback.print_exc()

        add_response(response_text)

    except Exception:

        print(
            "\n[OLLAMA ERROR]"
        )

        traceback.print_exc()
