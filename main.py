from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import fastapi_poe as fp
import json
import uvicorn

app = FastAPI()

DEFAULT_MODEL = "GPT-4"
BOTS_LIST = json.load(open("bots.json", "r"))
RESPONSE_TEMPLATE = {
    "id": "chat-123",
    "object": "chat.completion.chunk",
    "created": 123,
    "model": "",
    "system_fingerprint": "fp_123",
    "choices": [
        {
            "index": 0,
            "delta": {
                "role": "assistant",
                "content": ""
            },
            "logprobs": None,
            "finish_reason": ""
        }
    ]
}


async def get_request_params(request: Request):
    request_body = await request.json()
    request_headers = request.headers
    # fix request body
    for message in request_body["messages"]:
        if isinstance(message["content"], list):
            message["content"] = message["content"][0]["text"]

    def map_message(message):
        return {
            **message,
            "role": "bot" if message["role"] == "assistant" else message["role"]
        }


    return {
        "api_key": request_headers.get("Authorization").split(" ")[1],
        "model": BOTS_LIST.get(request_body["model"], DEFAULT_MODEL),
        "max_tokens": request_body.get("max_tokens", 1024),
        "messages": [
            fp.ProtocolMessage(**map_message(m)) for m in request_body["messages"]
        ],
        "temperature": request_body.get("temperature", 1),
        "top_p": request_body.get("top_p", 1),
        "frequency_penalty": request_body.get("frequency_penalty", 1),
        "presence_penalty": request_body.get("presence_penalty", 1),
        "stream": request_body.get("stream", False),
    }


@app.post("/v1/chat/completions")
@app.post("/openai/chat/completions")
async def chat_completions(request: Request):
    params = await get_request_params(request)

    async def generate():
        async for chunk in fp.get_bot_response(
                messages=params["messages"],
                bot_name=params["model"],
                api_key=params["api_key"],
                temperature=params["temperature"],
        ):
            response = RESPONSE_TEMPLATE.copy()
            response["model"] = params["model"]
            response["choices"][0]["delta"]["content"] = chunk.text
            if not chunk.text:
                response["choices"][0]["finish_reason"] = "stop"
            yield f"data: {json.dumps(response)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8765)
