# poe2openai🚀

This is a tool that 🛠️seamlessly converts the POE developer API to the standard OpenAI API format.

## Models mapping (detail in bots.json)

| Poe Model Name | Mapping Name |
|---------------|--------------|
|GPT-4o-Mini    | gpt-4o-mini |
|GPT-4o         | gpt-4o       |
|GPT-4o-128k    | gpt-4o-128k |
|GPT-4-Turbo     | gpt-4-turbo |
|GPT-4-Turbo-128K | gpt-4-turbo-128k |
|Claude-3.5-Sonnet | claude-3.5-sonnet |
|Claude-3.5-Sonnet-200k | claude-3.5-sonnet-200k |

Note that you can look up and pass in the [model names](https://poe.com/explore?category=Official) supported by the official Poe website.
The above is only an adaptation for when custom model names are not allowed in your client.

## How to Use?🤔

### One-Step Running

```
docker run -d --name poe2openai -p 8765:8765 1ynn/poe2openai:latest
```

### DIY

1. Set up your local 🐳 Docker environment;
2. Clone this project to your local machine;
3. Navigate to the project directory and run `docker build -t poe2openai .` to 🔧build the image;
4. Run `docker run -d --name poe2openai -p 8765:8765 poe2openai` to start the container;
5. Replace 🔄 `https://api.openai.com` in your application with `http://localhost:8765`;

## Q&A💬

* How can I get a POE API Key? 🔑 Please visit `https://poe.com/api_key`;
* What are the 😄advantages? Unlimited access to Claude3 and GPT4 without worrying about regional restrictions;
* What are the 😥disadvantages? Payment is required, and the first response is relatively slow;

## Disclaimer

This project is for learning and communication purposes only, and should not be used for commercial purposes.
