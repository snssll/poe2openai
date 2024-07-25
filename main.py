from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import fastapi_poe as fp
import json
import uvicorn

app = FastAPI()

# DEFAULT_MODEL = "GPT-4"
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

RESPONSE_TEMPLATE_NOT_STREAM = {
    "id": "chat-123",
    "object": "chat.completion.chunk",
    "created": 123,
    "model": "",
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": ""
            },
            "logprobs": None,
            "finish_reason": "stop",
            "index": 0
        }
    ]
}


async def get_request_params(request: Request):
    request_body = await request.json()
    request_headers = request.headers
    # print(request_headers)
    # print(request_body)
    # fix request body
    for message in request_body["messages"]:
        if isinstance(message["content"], list):
            message["attachments"] = []
            for i in range(1, len(message["content"])):
                t = message["content"][i]["type"]
                message["attachments"].append(
                    fp.Attachment(
                        url=message["content"][i][t]["url"],
                        content_type=t,
                        name=t,
                        parsed_content='一张图片',
                    )
                )
            message["content"] = message["content"][0]["text"] # remove the attachments
            # print(message)



    def map_message(message):
        return {
            **message,
            "role": "bot" if message["role"] == "assistant" else message["role"]
        }


    return {
        "api_key": request_headers.get("Authorization").split(" ")[1],
        "model": BOTS_LIST.get(request_body["model"], request_body["model"]),
        "max_tokens": request_body.get("max_tokens", 1024),
        "messages": [
            fp.ProtocolMessage(**map_message(m)) for m in request_body["messages"]
        ],
        "temperature": request_body.get("temperature", 0),
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

    if params["stream"]:
        return StreamingResponse(generate(), media_type="text/event-stream")
    else:
        one_res = RESPONSE_TEMPLATE_NOT_STREAM.copy()
        one_res["model"] = params["model"]
        text = ""
        async for chunk in fp.get_bot_response(
                messages=params["messages"],
                bot_name=params["model"],
                api_key=params["api_key"],
                temperature=params["temperature"],
        ):
            text += chunk.text
        one_res["choices"][0]["message"]["content"] = text
        return one_res



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8765)
