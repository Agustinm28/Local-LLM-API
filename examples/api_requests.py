import requests

class RequestLLM:

    def __init__(self):
        self.url = "http://localhost:5000/"

    def get_answer(self, endpoint="/model", prompt:str=None):

        data = {"question": f"{prompt}"}
        url = self.url + endpoint

        response = requests.post(url, json=data)

        if response.status_code == 200:
            # Request was successful
            result = response.json() # result is a dict
            text = result['result']['choices'][0]['text']

            parts = text.split("Answer:")

            # Verify that the response contains an answer
            if len(parts) > 1:
                answer = parts[1].strip()  # Delete leading and trailing spaces
            else:
                answer = "No answer found"

            return answer
        else:
            # Request encountered an error
            print("Error:", response.status_code)
            print("Response:", response.text)

    def get_models(self, endpoint="models"):

        url = self.url + endpoint
        response = requests.get(url)

        if response.status_code == 200:
            # Request was successful
            result = response.json()
            return result
        else:
            # Request encountered an error
            print("Error:", response.status_code)
            print("Response:", response.text)

    def set_model(self, endpoint="/setModel", model:str=None):

        data = {"model": f"{model}"}
        url = self.url + endpoint

        response = requests.post(url, json=data)

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


if __name__ == '__main__':
    
    rq = RequestLLM()

    prompt = "Who is the president of Canada?"
    answer = rq.get_answer(prompt=prompt)
    print(answer)

    # available_models = rq.get_models()
    # print(available_models)

    # rq.set_model(model="vicuna-7b-v1.5.ggmlv3.q4_0.bin")