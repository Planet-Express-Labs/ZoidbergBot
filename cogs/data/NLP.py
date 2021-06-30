import json
import requests
import os

from zoidbergbot.config import HF_API_KEY


class NLP:
    def __init__(self, headers=None):
        self.API_URL = None
        if headers is None:
            # Some time down the road, it's probably worth re working how the API keys are handled.
            self.headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    def direct_query(self, payload):
        """[summary]

        Args:
            payload (dict): Data to send to API.

        Returns:
            [dict]: [data returned from API]
        """
        data = json.dumps(payload)
        response = requests.request(
            "POST", self.API_URL, headers=self.headers, data=data)
        return json.loads(response.content.decode("utf-8"))


class Gpt2(NLP):
    def __init__(self):
        super().__init__()
        self.API_URL = "https://api-inference.huggingface.co/models/gpt2"


class GptNeo(NLP):
    def __init__(self):
        super().__init__()
        self.API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"


class BartMNLI(NLP):
    def __init__(self, API_URL=None, headers=None):
        super().__init__(headers)
        self.API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

    def catagorize(self, inputs, labels, multi_label=False, use_gpu=False, use_cache=True, wait_for_model=False):
        """[summary]

        Args:
            inputs (string): String to pass to BART
            labels (list): BART labels to score. 

            multi_label (bool, optional): Boolean that is set to True if classes can overlap. Defaults to False.
            use_gpu (bool, optional): If you are going to be using GPU on HuggingFace. This is only for certain plans. Defaults to False. 
            use_cache (bool, optional): If the HuggingFace cache should be used. This should only be disabled on large models <10 GO. Defaults to True.
            wait_for_model (bool, optional): Defaults to False.

        Returns:
            [type]: [description]
        """
        data = self.direct_query(
            {
                "inputs": inputs,
                "parameters": {
                    "candidate_labels": labels,
                    "multi_label": multi_label
                },
                "options": {
                    "use_gpu": use_gpu,
                    "use_cache": use_cache,
                    "wait_for_model": wait_for_model
                }
            }
        )
        try:
            return data["scores"]
        except KeyError:
            return data


class BartCnn(NLP):
    def __init__(self, API_URL=None, headers=None):
        super().__init__(headers)
        if API_URL is None:
            self.API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

    def summarize(self, inputs: str, min_length=None, max_length=None, top_k=None, top_p=None, temperature=1.0,
                  repetition_penalty=None, max_time=None, use_gpu=False, use_cache=True, wait_for_model=False):
        data = [{
            "inputs": inputs,
            "parameters": {
                "min_length": min_length,
                "max_length": max_length,
                "top_k": top_k,
                "top_p": top_p,
                "temperature": temperature,
                "repetition_penalty": repetition_penalty,
                "max_time": max_time
            },
            "options": {
                "use_gpu": use_gpu,
                "use_cache": use_cache,
                "wait_for_model": wait_for_model
            }
        }]
        resp = self.direct_query(data)
        try:
            return resp["summary_text"]
        except KeyError:
            return resp

