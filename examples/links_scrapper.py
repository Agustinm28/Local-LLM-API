import requests
from bs4 import BeautifulSoup
import os
import json as js

class LinkExtractor:

    def __init__(self, url):
        self.url = url
        self.start = 'https://huggingface.co'
        self.models_json = {}

    def extract_links(self):
        response = requests.get(self.url)

        links = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            list_li = soup.find_all('li')

            for li in list_li:
                link = li.find('a', attrs={'title': 'Download file'})
                if link:
                    download_link = self.start + link.get('href')
                    links.append(download_link)
            return links
        else:
            print('Error: {}'.format(response.status_code))

    def filter_links(self, links):
        filtered_links = []
        for link in links:
            if link.endswith('.bin') or link.endswith('.zip'):
                filtered_links.append(link)
        return filtered_links

    def generate_model_json(self, links):
        json = {}
        for link in links:
            name = os.path.basename(link)
            json[f'{name}'] = link
        return json
    
    def add_models(self, model_name, json):
        self.models_json[f'{model_name}'] = json
        return self.models_json
    
    def dump_json(self, json_file, path):
        if not os.path.exists(path):
            with open(path, 'w') as f:
                js.dump(json_file, f, indent=4)
        else:
            with open(path, 'r') as f:
                data = js.load(f)
            data.update(json_file)
            with open(path, 'w') as f:
                js.dump(data, f, indent=4)

if __name__ == '__main__':
    model_extraction = {
        'Llama-2-7B-GGML': 'https://huggingface.co/TheBloke/Llama-2-7B-GGML/tree/main',
        'Llama-2-13B-GGML': 'https://huggingface.co/TheBloke/Llama-2-13B-GGML/tree/main',
        'Llama-2-70B-GGML': 'https://huggingface.co/TheBloke/Llama-2-70B-GGML/tree/main',
        'Llama-2-7B-Chat-GGML': 'https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main',
        'Llama-2-13B-Chat-GGML': 'https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/tree/main',
        'Llama-2-70B-Chat-GGML': 'https://huggingface.co/TheBloke/Llama-2-70B-Chat-GGML/tree/main',
        'Yarn-Llama-2-7B-64K':'https://huggingface.co/TheBloke/Yarn-Llama-2-7B-64K-GGML/tree/main',
        'Yarn-Llama-2-13B-128K':'https://huggingface.co/TheBloke/Yarn-Llama-2-7B-128K-GGML/tree/main',
        'Vicuna-7B-GGML': 'https://huggingface.co/TheBloke/vicuna-7B-v1.3-GGML/tree/main',
        'Vicuna-13B-GGML': 'https://huggingface.co/TheBloke/vicuna-13B-v1.5-GGML/tree/main',
        'Vicuna-33B-GGML': 'https://huggingface.co/TheBloke/vicuna-33B-GGML/tree/main',
    }

    output_path = 'data/models.json'
    
    for model, url in model_extraction.items():
        print(f'Extracting links for {model}')
        extractor = LinkExtractor(url)
        links = extractor.extract_links()
        links = extractor.filter_links(links)
        json = extractor.generate_model_json(links)
        json = extractor.add_models(model, json)
        extractor.dump_json(json, output_path)
    print('Done!')