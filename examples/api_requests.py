import requests
from dotenv import load_dotenv
import os

class LLMRequests:

    def __init__(self, url: str, api_key: str = None):
        self.url = 'http://127.0.0.1:5000'
        self.api_key = api_key

class AnswerRequest(LLMRequests):
    '''
    Class to make requests to the LLM Local API Server. This class agrupates the methods to get an answer.
    '''

    def get_answer(self, endpoint="/answer", prompt: str = None, session_id: int = None):
        '''
        Method to get an answer from the LLM Local API Server. Where:
            - prompt: is the question to be answered.
        '''

        data = {"prompt": f"{prompt}", "session_id": session_id}
        headers = {"Authorization": self.api_key, "charset": "UTF-8", "pageEncoding": "UTF-8"}
        url = self.url + endpoint

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            # Request was successful
            result = response.json()  # result is a dict
            text = result['result']

            return text
        else:
            # Request encountered an error
            print("Error:", response.status_code)
            print("Response:", response.text)

    def get_raw_answer(self, endpoint="/answer", prompt: str = None, session_id: int = None):
        '''
        Method to get an answer from the LLM Local API Server. Where:
            - prompt: is the question to be answered.
        '''

        data = {"prompt": f"{prompt}", "session_id": session_id}
        headers = {"Authorization": self.api_key}
        url = self.url + endpoint

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            # Request was successful
            result = response.json()

            return result
        else:
            # Request encountered an error
            print("Error:", response.status_code)
            print("Response:", response.text)

    def get_sessions(self, endpoint="/answer"):
        '''
        Method to get the sessions from the LLM Local API Server. Where:
            - prompt: is the question to be answered.
        '''

        headers = {"Authorization": self.api_key}
        url = self.url + endpoint

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Request was successful
            result = response.json()
            return result
        
        else:
            # Request encountered an error
            print("Error:", response.status_code)
            print("Response:", response.text)


class ModelRequest(LLMRequests):
    '''
    This class agrupates the methods to set and see the available models in the LLM Local API Server.
    '''

    def get_models(self, endpoint="/models"):
        '''
        Method to get the available models in the LLM Local API Server.
        '''

        url = self.url + endpoint
        headers = {"Authorization": self.api_key}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Request was successful
            result = response.json()
            return result
        else:
            # Request encountered an error
            print("Error:", response.status_code)
            print("Response:", response.text)

    def set_model(self, endpoint="/models/model", model: str = None, model_config: str = None):
        '''
        Method to set the model to be used in the LLM Local API Server. Where:
            - model: is the name of the model to be used.
            - model_config: is the name of the model profile to be used.
        '''

        data = {"model": f"{model}", "model_config": f"{model_config}"}
        headers = {"Authorization": self.api_key}
        url = self.url + endpoint

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            # Request was successful
            result = response.json()

            if result['model_status'] == True:
                print(f"Model {model} set successfully")
            else:
                print(f"Model {model} not set")
                print("Error:", response.status_code)
                print("Response:", response.text)
        else:
            # Request encountered an error
            print("Error:", response.status_code)
            print("Response:", response.text)


class AuthRequest(LLMRequests):
    '''
    This class agrupates the methods to check the authorization (api key) of the LLM Local API Server.
    '''

    def check_auth(self, endpoint="/auth"):
        '''
        Method to check the authorization (api key) of the LLM Local API Server.
        '''
        url = self.url + endpoint
        headers = {"Authorization": self.api_key}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Request was successful
            result = response.json()
            return result
        else:
            # Request encountered an error
            print("Error:", response.status_code)
            print("Response:", response.text)

    def gen_key(self, endpoint="/auth/key"):
        '''
        Method to generate a new api key for the LLM Local API Server. Requires master key.
        '''

        url = self.url + endpoint
        headers = {"Authorization": self.api_key}  # Only with master key

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Request was successful
            result = response.json()
            return result
        else:
            # Request encountered an error
            print("Error:", response.status_code)
            print("Response:", response.text)


if __name__ == '__main__':

    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    ans = AnswerRequest(API_KEY)
    mo = ModelRequest(API_KEY)
    au = AuthRequest(API_KEY)

    # Get answer from the model throug API
    # prompt = "Genera un diálogo corto de 6 intercambios entre 2 personajes (Cosmo, Coscu (Streamer, Latin American Spanish)), con temática relacionada a las siguientes palabras clave: Economía, Anime. El sentimiento principal del diálogo es Tristeza. El sentimiento secundario del diálogo es Desengaño. El diálogo se desarrolla en La luna. En cuanto al tiempo, el diálogo tiene lugar al/ a la Noche. El clima del diálogo es Lluvia de meteoritos. El diálogo debe estar escrita al estilo de Stephen King. El diálogo debe ser del género Terror. El argumento principal del diálogo es el siguiente: Cosmo se encuentra con el fantasma de Coscu. El objetivo del diálogo (lo que se pretende lograr con el mismo dentro de la historia) es Asustar al lector."
    # prompt = 'Podes continuar el dialogo anterior? Pero esta vez, Cosmo le cuenta a Goku (Saiyan de Dragon Ball Z) lo sucedido con Coscu.'
    # prompt = 'Resumime el dialogo anterior.'
    prompt = "Genera el boceto de un episodio de una serie 5 escenas, donde los siguientes personajes intervengan en el orden que consideres más conveniente (Cosmo, Coscu, Goku). La temática del episodio debe ser 'El valor de la amistad'. Tienes absoluta libertad respecto a los lugares, la ambientación y el entramado de la historia, siempre y cuando las escenas sean coherentes y cohesivas entre sí. Cada escena debe estar limitada al siguiente formato: ESCENA <número de escena>: <doble salto de línea> - TÓPICOS: <lista de tópicos principales de la escena, separados por coma; cada tópico debe ser una sola palabra> <doble salto de línea> - GÉNERO: <género principal de la escena: terror, comedia, etc...> <doble salto de línea> - ARGUMENTO: <frase breve describiendo el argumento principal de la escena> <doble salto de línea> - OBJETIVO: <frase breve describiendo lo que escena pretende lograr argumentalmente hablando, lo que busca evocar en el televidente> <doble salto de línea>."
    answer = ans.get_answer(prompt=prompt, session_id=1)
    print(answer)

    ## Get answer from the model through API
    # prompt = "Genera un diálogo corto de 6 intercambios entre 2 personajes (Cosmo, Wanda), que continúe con los diálogos anteriores (presentes en 'CURRENT CONVERSATION'), con temática relacionada a las siguientes palabras clave: Amor, Anime. El sentimiento principal del diálogo es Esperanza. El sentimiento secundario del diálogo es Angustia. El diálogo se desarrolla en La luna. En cuanto al tiempo, el diálogo tiene lugar al/ a la Noche. El clima del diálogo es Lluvia de meteoritos. El diálogo debe estar escrito al estilo de Stephen King. El diálogo debe ser del género Terror. El argumento principal del diálogo es el siguiente: Cosmo le cuenta a Wanda lo sucedido con Coscu. El objetivo del diálogo (lo que se pretende lograr con el mismo dentro de la historia) es Avanzar la trama principal. Debes cumplir con las siguientes pautas:\n - Las anotaciones o acotaciones respecto a expresiones, entradas o salidas de personajes deben escribirse entre paréntesis.\n - Las líneas de los personajes deben responder al siguiente formato: <nombre del personaje>: (<acotaciones, si las hubiese>) <línea de diálogo>.\n - Las líneas de los personajes deben estar separadas por dos saltos de línea."
    # answer = ans.get_answer(prompt=prompt)
    # print(answer)

    # Get raw answer from the model throug API (dict format with extra info)
    # prompt = "Genera un diálogo corto de 6 intercambios entre 2 personajes (Cosmo, Coscu (Streamer, Latin American Spanish)), con temática relacionada a las siguientes palabras clave: Economía, Anime. El sentimiento principal del diálogo es Tristeza. El sentimiento secundario del diálogo es Desengaño. El diálogo se desarrolla en La luna. En cuanto al tiempo, el diálogo tiene lugar al/ a la Noche. El clima del diálogo es Lluvia de meteoritos. El diálogo debe estar escrita al estilo de Stephen King. El diálogo debe ser del género Terror. El argumento principal del diálogo es el siguiente: Cosmo se encuentra con el fantasma de Coscu. El objetivo del diálogo (lo que se pretende lograr con el mismo dentro de la historia) es Asustar al lector."
    # answer = ans.get_raw_answer(prompt=prompt)
    # print(answer)

    # Get sessions
    # sessions = ans.get_sessions()
    # sessions = json.dumps(sessions, indent=4)
    # print(sessions)

    # Get available models
    # available_models = mo.get_models()
    # print(available_models)

    # Set model to be used
    # mo.set_model(model="vicuna-13b-v1.5.Q5_K_M.gguf", model_config="Vicuna-13b")

    # Check authorization
    # auth = au.check_auth()
    # print(auth)

    # Generate new api key (requires master key)
    # key = au.gen_key()
    # print(key)
