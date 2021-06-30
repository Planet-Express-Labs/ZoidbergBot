import json
import requests
import os

from zoidbergbot.config import HF_API_KEY


class Gpt2:
    def __init__(self, API_URL=None, headers=None):
        if API_URL is None:
            self.API_URL = "https://api-inference.huggingface.co/models/gpt2"
        if headers is None:
            self.headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    def direct_query(self, payload):
        data = json.dumps(payload)
        response = requests.request(
            "POST", self.API_URL, headers=self.headers, data=data)
        return json.loads(response.content.decode("utf-8"))


class GptNeo:
    def __init__(self, API_URL=None, headers=None):
        if API_URL is None:
            self.API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
        if headers is None:
            self.headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    def direct_query(self, payload):
        data = json.dumps(payload)
        response = requests.request(
            "POST", self.API_URL, headers=self.headers, data=data)
        return json.loads(response.content.decode("utf-8"))


class BartMNLI:    
    def __init__(self, API_URL=None, headers=None):
        if API_URL is None:
            self.API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
        if headers is None:
            self.headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    def direct_query(self, payload: dict):
        """[summary]

        Args:
            payload (type): Data to send to API.

        Returns:
            [dict]: [data returned from API]
        """        
        data = json.dumps(payload)
        response = requests.request(
            "POST", self.API_URL, headers=self.headers, data=data)
        return json.loads(response.content.decode("utf-8"))

    def catagorize(self, inputs, labels, multi_label=False, use_gpu=False, use_cache=True, wait_for_model=False):
        """[summary]

        Args:
            inputs (string): String to pass to BART
            labels (list): BART labels to score. 

            Stuff I passed though that I'm not entirely sure what they are for.
            multi_label (bool, optional): Defaults to False.
            use_gpu (bool, optional): Defaults to False.
            use_cache (bool, optional): Defaults to True.
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


class BartCnn:
    def __init__(self, API_URL=None, headers=None):
        if API_URL is None:
            self.API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        if headers is None:
            self.headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    def direct_query(self, payload):
        data = json.dumps(payload)
        response = requests.request("POST", self.API_URL, headers=self.headers, data=data)
        return json.loads(response.content.decode("utf-8"))

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
            "options":{
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

