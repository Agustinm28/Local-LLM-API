from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from promptGen import PromptGenerator
import torch

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

def dialogue_loop(promptGen: PromptGenerator, n_scenes: int = 5):
    previous_scene = None
    
    for i in range(n_scenes):
        print(f"ESCENA {i + 1}".center(40, "_"))
    
        # Genera el prompt
        prompt = promptGen.generate_random_dialogue_prompt(numOfKeyWord=2, numOfCharacters=3, numOfExchanges=5)
        prompt_with_context = promptGen.add_prompt_context(prompt, {"mainFeeling": "Tristeza", "secondaryFeeling": "Desengaño", "setting": "La luna", "time": "Noche", "weather": "Lluvia de meteoritos", "writingStyle": "Stephen King", "genre": "Terror", "plot": "Uno de los personajes es un fantasma y siempre está aterrorizando a los otros", "objective": "Asustar al lector"})
        
        # Genera el diálogo 
        gen_scene = generate_text(
            prompt_with_context,
            previous_scene
            )
        
        # Actualiza la última escena previa
        previous_scene = gen_scene

        print(gen_scene)

def generate_text(prompt: str, previous_dialogue: str = None):
    # Reset chache
    #torch.cuda.empty_cache()

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

    model, tokenizer = load_gen_model('E:/Modelos_Prueba_IA', 'TheBloke/Llama-2-13B-chat-GPTQ')  
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
        output = model.generate(input_ids, temperature=0.7, max_length=2000, do_sample=True)

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return generated_text

if __name__ == '__main__':
    dialogue_loop(PromptGenerator(r"C:\Users\Fran\Desktop\Local-LLM-API\data\topicList.csv", r"C:\Users\Fran\Desktop\Local-LLM-API\data\characterList.json"))