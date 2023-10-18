# Local-LLM-API
Repository for Local LLM API Server solution.

This project aims to facilitate the local deployment of LLM model APIs for various purposes, with a primary focus on optimized CPU execution.

## 🔧 Setup:

**Suported OS**: Linux

1. Easy path: Run the setup.sh file with sudo:

```bash
source setup.sh
```
and then:
```bash
sudo ./setup.sh
```

**NOTE**: Remember to activate the virtual environment before running the server if it's not already activated.

```bash
source .venv/bin/activate
```

2. Manual installation:

- Setup a virtual environment:

```bash
sudo apt install python3.10-venv
```
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```

- Install the dependencies:

```bash
sudo apt-get install gcc
```
```bash
export CC=gcc
```
```bash
sudo apt-get install g++
```
```bash
export CXX=g++
```
```bash
sudo apt-get install make
```

- Install the requirements:

```bash
pip install -r requirements.txt
```

- Create a models folder in path:

```bash
mkdir models
```

## ⚡How to use

1. Create a folder named "models" in the root path of the project if not exists.

2. Download a .gguf model (last supported for LlamaCPP):
    
    - Recomended repository: https://huggingface.co/TheBloke
        **Credit**: Tom Jobbins (TheBloke)

    - The model has to be GGML for `llama-cpp-python==0.1.65` ans lesser or GGUF for newer versions.

3. Put the model in the models folder.

    **NOTE**: Download a model direct in the folder throug console with `wget [download_model url]`

4. Configure a profile for a model:

    a. Go to `data/config.json` file
    b. A profile contains the configuration values of a particular LLM, allowing you to have different profiles set up for various purposes. For instance, a profile for a chatbot looks like:

    ```json
    {
    "SelectedModel": "Vicuna-13b",
    "Vicuna-13b": {
        "model": "vicuna-13b-v1.5.Q5_K_M.gguf",
        "n_ctx": 4096,
        "temperature": 0.7,
        "max_tokens": 16000,
        "top_p": 0.8,
        "top_k": 40,
        "verbose": true,
        "repeat_penalty": 1.1,
        "template": "You are a chatbot. \n\n{chat_history} \n\nPROMPT: {input} \n\nBOT:"
        }
    }
    ```

    Where:

        - **SelectedModel** is the profile in use
        - **Vicuna-13b** is the name of the profile
            - **model** is the name of the model .gguf file in models folder
            - **n_ctx** determines the maximum context length for the model.
            - **temperature** controls the randomness of the model's output. Higher values make the output more random, while lower values make it more deterministic.
            - **max_tokens** sets a limit on the number of tokens in the model's response.
            - **top_p** is used for nucleus sampling, where the model only considers the most likely tokens that make up a certain portion of the cumulative probability distribution.
            - **top_k** limits the number of the most likely tokens to consider during response generation. Higher values result in more diversity, but excessive values may lead to incoherent output.
            - **verbose**: indicates that the model will provide detailed or additional information alongside the responses.
            - **repeat_penalty** discourages the model from repeating the same tokens in the response.
            - **template** It's where the system prompt (LLM's mission and features) and variables are located. You can modify this parameter in order to achieve a specific goal for your LLM.

    **NOTE**: Learn more of quantized LLMs here [What are Quantized LLMs?](https://www.tensorops.ai/post/what-are-quantized-llms#:~:text=Updated%3A%20Oct%201,the%20precision%20of%20their%20weights.)

    c. To add a new profile, put a new key-value segment after "SelectedModel" or after other profile:

    ```json
    {
    "SelectedModel": "Vicuna-13b",
    "Vicuna-13b": {
        "model": "vicuna-13b-v1.5.Q5_K_M.gguf",
        "n_ctx": 4096,
        "temperature": 0.7,
        "max_tokens": 16000,
        "top_p": 0.8,
        "top_k": 40,
        "verbose": true,
        "repeat_penalty": 1.1,
        "template": "You are a chatbot. \n\n{chat_history} \n\nPROMPT: {input} \n\nBOT:"
        },
    "Other-profile": {
        "Your configuration here ..."
        }
    }
    ```

5. Configure Master-Key

    In order to make requests to the api, you need to configure a Master Key. This master key will help you make API calls and generate new API keys.

    - Go to data/api_keys.json and put a secure api key there. Another option we recommend is to use the `generate_api_key()` function within `auth/authentication.py` to generate a secure key and then place it in the `api_keys.json` file. 

5. Run the server:

```bash
python3 main.py
```

## 📖 Sessions

Sessions are used to store the history of interactions in a conversation locally for later resumption. Some considerations include:

    - Sessions will store the number of interactions specified in the `k` parameter of the `ConversationBufferWindowMemory` in the `memory` variable in `services/answer_services.py` in the post function for the `Answer` class. This parameter will cause the last k interactions to be stored in memory.

    ```python
    session = load_session(session_id=session_id)
    memory = ConversationBufferWindowMemory(
            k=5, # Number of interactions to store in memory
            memory_key="chat_history", 
            chat_memory=session
            )
    ```

    - If no session is specified in the body of the request, the session will be taken as `None`, and will not be saved locally, so the session will only live the k interactions specified above in memory.

    - The session_id can take any numerical value, if it does not exist in `data/sessions.json` on the server side a new session will be generated, if it does exist, it will continue and update that existing session.

## 🌐 Requests

- The requests has endpoint: `http://localhost:5000/` by default
- See the example in examples folder.

### POST /answer

- Get an answer from the LLM in the LLM Local API Server.
- Request body: `{"prompt": "YOUR-PROMPT-HERE", "session_id": id(int)}`
- Request header: {"Authorization": api_key}
- Where:
    - `prompt` is the prompt to be sended to the LLM
    - `session_id` is an optional parameter to use an existent session or create a new one.
    - `Authorization` is the master key or an api key generated by the master key.

### GET /answer

- Get a dict of the existing sessions from the LLM Local API Server.
- Request header: {"Authorization": api_key}

### GET /models

- Get a dict of the available models in the models folder in LLM Local API Server.
- Request header: {"Authorization": api_key}

### POST /models/model

- Set the model and profile to be used in the LLM Local API Server.
- Request body: `{"model": "gguf_model", "model_config": "profile_name"}`
- Request header: {"Authorization": api_key}
- Where:
    - `model` is the name of the model .gguf file in models folder
    - `model_config` is the name of the profile in config.json
    - `Authorization` is the master key or an api key generated by the master key.

### GET /auth

- Check the authorization (api key) of the LLM Local API Server.
- Request header: {"Authorization": api_key}

### POST /auth/key

- Generate a new api key for the LLM Local API Server. Requires master key.
- Request header: {"Authorization": master_api_key}

## 🖊️ Author

Agustín Montaña - [GitHub](https://github.com/Agustinm28)
Bruno Orbelli - [GitHub](https://github.com/Bruno-Orbelli)
Francisco Espinola - [GitHub](https://github.com/franespinola)