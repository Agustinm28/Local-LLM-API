# Local-LLM-API
Repository for Local LLM API Server solution.

##🔧Setup:

1. Easy path: Run the setup.py file with sudo:

```bash
sudo python3 setup.py
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

##⚡How to use

1. Create a folder named "models" in the root path of the project.

2. Download a .bin model:
    
    - You can download from here: https://huggingface.co/TheBloke

    - The model has to be GGML for `llama-cpp-python==0.1.65` or GGUF for newer versions.

3. Put the model in the models folder.

4. Run the server:

```bash
python3 main.py
```

##🌐Requests

- The requests has endpoint: `http://localhost:5000/`
- See the example in examples folder.

### POST /models

- This is for see the available models in the models folder.
- Request body: None

### POST /setModel

- This is for set the model to use.
- Request body: `{"model": "model_name.bin"}`

### POST /answer

- This is for get the answer of the model.
- Request body: `{"question": "prompt"}`

### POST /stream

- This is for get the answer of the model in a stream (similar to ChatGPT).
- Request body: `{"question": "prompt"}`

##🖊️Author

Agustín Montaña - [GitHub](https://github.com/Agustinm28)