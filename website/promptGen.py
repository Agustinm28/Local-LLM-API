from random import sample, randrange
from json import load as jload

class PromptGenerator():
    
    def __init__(self, topicFilePath: str, characterFilePath: str):
        self.topicList: list = self.load_from_csv(topicFilePath)
        self.characterDict: dict = self.load_from_json(characterFilePath)
    
    def load_from_csv(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().splitlines()[1::]
    
    def load_from_json(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            return jload(f)
       
    def generate_deterministic_dialogue_prompt(self, *, characterList: 'list[str]', topicList: 'list[str]', numOfExchanges: int = None):
        for character in characterList:
            if not (character in list(self.characterDict.keys())):
                raise ValueError(f"Unknown characters specified. characterDict must be a subset of self.characterDict")
        
        characters = {c: self.characterDict[c] for c in characterList}
        exchangeNum = numOfExchanges if numOfExchanges else randrange(5, 11)

        basePrompt = f"Genera un diálogo corto de {exchangeNum} intercambios entre {len(characters)} personajes ({', '.join(c for c in characters.keys())}), con temática relacionada a las siguientes palabras clave: {', '.join(k for k in topicList)}."

        return basePrompt
    
    def generate_random_dialogue_prompt(self, *, numOfKeyWord: int = None, numOfCharacters: int = None, numOfExchanges: int = None):       
        keyWords = sample(self.topicList, numOfKeyWord if numOfKeyWord else randrange(1,4))
        characters = sample(list(self.characterDict), numOfCharacters if numOfCharacters else randrange(2,4))
        exchangeNum = numOfExchanges if numOfExchanges else randrange(5, 11)

        basePrompt = f"Genera un diálogo corto de {exchangeNum} intercambios entre {len(characters)} personajes ({', '.join(c for c in characters)}), con temática relacionada a las siguientes palabras clave: {', '.join(k for k in keyWords)}."
        
        return basePrompt
    
    def add_prompt_context(self, basePrompt: str, promptOptions: 'dict[str, str]'):
        '''Method for adding context to a prompt. Where:
            - basePrompt: The base prompt to be used.
            - promptOptions: The options to be used for adding context to the prompt.
                - mainFeeling: The main feeling to be evoked in the scene, for adding context to the prompt.
                - secondaryFeeling: A secondary feeling to be evoked in the scene, for adding context to the prompt.
                - setting: The setting in which the scene takes place, for adding context to the prompt.
                - time: The time of day at which the scene happens, for adding context to the prompt.
                - weather: The weather at the moment of the scene, for adding context to the prompt.
                - writingStyle: The writing style of the scene (of a particular writer, for example), for adding context to the prompt.
                - genre: The genre of the scene, for adding context to the prompt.
                - plot: The plot of the scene, for adding context to the prompt.
                - objective: What the scene must accomplish in general, for adding context to the prompt.
        '''
        prompt = basePrompt
        context = {
            "mainFeeling": " El sentimiento principal del diálogo es {}.",
            "secondaryFeeling": " El sentimiento secundario del diálogo es {}.",
            "setting": " El diálogo se desarrolla en {}.",
            "time": " En cuanto al tiempo, el diálogo tiene lugar al/ a la {}.",
            "weather": " El clima del diálogo es {}.",
            "writingStyle": " El diálogo debe estar escrita al estilo de {}.",
            "genre": " El diálogo debe ser del género {}.",
            "plot": " El argumento principal del diálogo es el siguiente: {}.",
            "objective": " El objetivo del diálogo (lo que se pretende lograr con el mismo dentro de la historia) es {}."
        }        
        
        for option in promptOptions.keys():
            if option in context.keys():
                prompt += context[option].format(promptOptions[option])
            else:
                raise ValueError(f"Unknown prompt option specified. '{option}' is not a valid prompt option.")

        return prompt       

if __name__ == "__main__":
    promptGen = PromptGenerator("data/topicList.csv", "data/characterList.json")
    print(promptGen.generate_random_dialogue_prompt(numOfKeyWord=4, numOfCharacters=5, numOfExchanges=6))
    basePrompt = promptGen.generate_deterministic_dialogue_prompt(characterList=["Cosmo", "Coscu (Streamer, Latin American Spanish)"], topicList=["Economía", "Anime"], numOfExchanges=6)
    print(promptGen.add_prompt_context(basePrompt, {"mainFeeling": "Tristeza", "secondaryFeeling": "Desengaño", "setting": "La luna", "time": "Noche", "weather": "Lluvia de meteoritos", "writingStyle": "Stephen King", "genre": "Terror", "plot": "Cosmo se encuentra con el fantasma de Coscu", "objective": "Asustar al lector"}))