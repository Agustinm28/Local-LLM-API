from llama_cpp import Llama
import os
import json
import requests
from tqdm import tqdm

def load_model():
    '''
    Method to load the model. Gets the model name from config.json.
    '''
    
    print('Loading model...')

    # Read model name from config.json
    with open('data/config.json', 'r') as f:
        config = json.load(f)
    model_name = config['model']

    model_path = f'./models/{model_name}'

    llm = Llama(model_path=model_path)
    print('Model loaded')

    return llm

def get_models():
    '''
    Method to get the models available in the models folder.
    '''
    # Check if models folder exists
    if not os.path.isdir('./models'):
        os.mkdir('./models')

    # Check files in models folder
    print('Getting models...')
    models = []
    for file in os.listdir('./models'):
        if file.endswith('.bin'):
            models.append(file)
    print('Models obtained')

    return models

def set_model(model_name:str):
    '''
    Method to set the model. Where:
        - model_name: name of the model. You can get the models with get_models()
    '''

    print(f'Setting up model {model_name}')
    try:
        # Check if model exists
        if model_name not in get_models():
            return False
        
        # Write the model name in config.json
        with open('data/config.json', 'r') as f:
            config = json.load(f)
        config['model'] = model_name
        with open('data/config.json', 'w') as f:
            json.dump(config, f)
        
        print(f'Model {model_name} set up correctly')

        return True
    except Exception as e:
        print(e)
        return False

def see_models():
    '''
    Method to see the models available for download in the models.json file
    '''
    # Read models.json
    with open('data/models.json', 'r') as f:
        models = json.load(f)

    models_dict = {}
    # Make a dict with the model
    for model_name, sub_dict in models.items():
        # Create key list with sub_dict keys
        keys = list(sub_dict.keys())

        # Add the pair key-value to the dict
        models_dict[model_name] = keys

    return models_dict

def download_model(model_name:str):
    '''
    Method to download the model. Where:
        - model_name: name of the model. You can get the models with see_models()
    '''

    with open('data/models.json', 'r') as f:
        models = json.load(f)

    # Check if model exists
    for model in models:
        if model_name in models[model]:
            model_url = models[model][model_name]
        else:
            pass
    
    download_path = f'models/{model_name}'

    # Download the model
    print(f'Downloading model {model_name}...')
    response = requests.get(model_url, stream=True)

    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        chunk_size = 1024

        with open(download_path, 'wb') as f, tqdm(
            desc=download_path,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=chunk_size):
                f.write(data)
                bar.update(len(data))
                yield bar
        return f"Model {model_name} downloaded"
    else:
        return f"Model {model_name} download failed"
    