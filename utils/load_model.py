import os
import json
import requests
from llama_cpp import Llama
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
import torch

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

                yield data

        return f"Model {model_name} downloaded"
    else:
        return f"Model {model_name} download failed"
    
def get_size(model_name:str):
    '''
    Method to get the size of the model. Where:
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
    
    # Get the size of the model
    print(f'Getting size of model {model_name}...')
    response = requests.get(model_url, stream=True)

    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        return total_size
    else:
        return f"Model {model_name} download failed"
    
### GPTQ ADDITIONS WITH TRANSFORMERS ###
    
def load_gen_model(path: str, model_name: str):
    # Carga el modelo y el tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_name,
                                                cache_dir=path,
                                                torch_dtype=torch.float16,
                                                device_map="auto",
                                                revision="main",
                                                #force_download=True, 
                                                #resume_download=False
                                                )

    tokenizer = AutoTokenizer.from_pretrained(model_name,
                                            cache_dir=path,
                                            use_fast=True)
    
    return model, tokenizer

def create_lang_chain(model: AutoModelForCausalLM, buffer: ConversationBufferMemory=None):
    # Crea una cadena de conversación (con memoria opcional) para el modelo cargado
    conversation = ConversationChain(
        llm=model, 
        verbose=True, 
        memory=buffer,
    )
    
    return conversation

def generate_gpu_text(prompt: str, previous_dialogue: str = None, temperature: float = 0.7, max_length: int = 2000, do_sample: bool = True):
    # Reset chache
    torch.cuda.empty_cache()

    #variable=torch.cuda.memory_summary(device=None, abbreviated=False) para ver como tengo ocupada la memoria de la GPU
    #print(variable)

    # Ruta personalizada en el disco local E para almacenar los modelos descargados y cachés
    # ejemplo si queremos ejecutar otro modelo q esta en otra rama revision="gptq-8bit--1g-actorder_True"(modelo descargado pero no funciona)
    #modelos descargados(se colocan en revision)
        #"gptq-8bit-128g-actorder_True" no funciona con transformers solo con AutoGPTQ
        #"gptq-8bit--1g-actorder_True" no funciona con transformers solo con AutoGPTQ
        #"main" funciona con transformers ya q es ExLLaMa
    #Path utilizados(se colocan en ra_personalizada)
        #"TheBloke/vicuna-7B-v1.5-GPTQ" (main,gptq-8bit-128g-actorder_True)
        #"TheBloke/Llama-2-13B-chat-GPTQ"(main,gptq-8bit-128g-actorder_True,gptq-8bit--1g-actorder_True,gptq-4bit-32g-actorder_True)

    # Load name of the model from config.json
    with open('data/config.json', 'r') as f:
        config = json.load(f)
    model_name = config['model']

    # Load model and tokenizer
    model, tokenizer = load_gen_model('./models', model_name)  

    # If model doesnt end with GPTQ, return error
    if not model_name.endswith('GPTQ'):
        raise Exception('Model is not GPTQ')

    if not previous_dialogue:
        previous_dialogue = "Esta es la primera escena a generar. Aún no hay contexto."

    prompt_template = f'''[INST] <<SYS>>
        Sos un guionista con 30 años de experiencia en la escritura de diálogos cinematográficos. Cada conjunto de diálogos tiene un contexto (el diálogo anterior) con el cual debe guardar cierta coherencia y seguir un hilo narrativo. DIÁLOGO PREVIO: {previous_dialogue} #! COREEGIR ---
        <</SYS>>
        {prompt}[/INST]

        '''

    print("\n\n*** Generate:")

    input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
  
    with torch.no_grad():
        output = model.generate(input_ids, temperature=temperature, max_length=max_length, do_sample=do_sample)

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return generated_text