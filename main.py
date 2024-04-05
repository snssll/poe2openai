from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import fastapi_poe as fp
import json
import uvicorn

app = FastAPI()


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):

    response_template = {
        "id": "chatcmpl-123",
        "object": "chat.completion.chunk",
        "created": 123,
        "model": "Claude-3-Opus",
        "system_fingerprint": "fp_123",
        "choices": [
            {
                "index": 0,
                "delta": {"role": "assistant", "content": ""},
                "logprobs": None,
                "finish_reason": None
            }
        ]
    }

    request_body = await request.json()

    api_key = request.headers.get("Authorization").split(" ")[1]
    bot_name = request_body["model"]

    def map_message(message):
        return {**message, "role": "bot" if message["role"] == "assistant" else message["role"]}

    messages = [fp.ProtocolMessage(**map_message(m)) for m in request_body["messages"]]

    async def generate():
        async for chunk in fp.get_bot_response(messages=messages, bot_name=bot_name, api_key=api_key, temperature=0.2):
            response = response_template.copy()
            response["choices"][0]["delta"]["content"] = chunk.text
            if not chunk.text:
                response["choices"][0]["finish_reason"] = "stop"
            yield f"data: {json.dumps(response)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8765)
