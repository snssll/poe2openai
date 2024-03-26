# poe2openai🚀

This is a tool that 🛠️converts the POE developer API to the standard OpenAI API format.


## How to Use?🤔

1. Prepare the local 🐳Docker environment;
2. Clone this project to local;
3. Enter the project directory and execute `docker build -t poe2openai .` to 🔧build the image;
4. Execute `docker run -d --name poe2openai -p 8765:8765 poe2openai` to start the container;
5. Replace 🔄 `https://api.openai.com` in your application with `http://localhost:8765`;

## Q&A💬

* How to get a POE API Key? 🔑 Please visit `https://poe.com/api_key`;
* What are the 😄advantages? Unlimited access to Claude3 and GPT4 without worrying about regional restrictions;
* What are the 😥disadvantages? Payment is required, and the first response is relatively slow;

## Disclaimer

This project is for learning and communication purposes only, and should not be used for commercial purposes.