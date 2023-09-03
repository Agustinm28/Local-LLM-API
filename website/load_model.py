from llama_cpp import Llama
import os
import json

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
