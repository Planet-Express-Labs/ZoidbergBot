
# 8888888888P         d8b      888 888                                    888               888
#       d88P          Y8P      888 888                                    888               888
#      d88P                    888 888                                    888               888
#     d88P    .d88b.  888  .d88888 88888b.   .d88b.  888d888 .d88b.       88888b.   .d88b.  888888
#    d88P    d88""88b 888 d88" 888 888 "88b d8P  Y8b 888P"  d88P"88b      888 "88b d88""88b 888
#   d88P     888  888 888 888  888 888  888 88888888 888    888  888      888  888 888  888 888
#  d88P      Y88..88P 888 Y88b 888 888 d88P Y8b.     888    Y88b 888      888 d88P Y88..88P Y88b.
# d8888888888 "Y88P"  888  "Y88888 88888P"   "Y8888  888     "Y88888      88888P"   "Y88P"   "Y888
# This software is provided free of charge without a warranty.   888
# This Source Code Form is subject to the terms of the      Y8b d88P
# Mozilla Public License, v. 2.0. If a copy of the MPL was   "Y88P"
# this file, You can obtain one at https://mozilla.org/MPL/2.0/.

# This is designed to be used with Zoidberg bot, however I'm sure it could be adapted to work with your own projects.
# If there is an issue that might cause issue on your own bot, feel free to pull request if it will improve something.<3

# This file servers as a library for interfacing with the models we are using with HuggingFace.
# Once OpenAI goes public or when I get a key, many of the models will be transitioned to using GPT3.
import json
import requests
import asyncio

from zoidbergbot.config import HF_API_KEY


class Inferances:
    def __init__(self, headers=None,  use_gpu=False, use_cache=True, wait_for_model=False):
            self.API_URL = None

            self.use_gpu = use_gpu
            self.use_cache = use_cache
            self.wait_for_model = wait_for_model

            if headers is None:
                # Some time down the road, it's probably worth re working how the API keys are handled.
                self.headers = {"Authorization": f"Bearer {HF_API_KEY}"}


class NLP(Inferances):
    
    async def direct_query(self, payload):
        """[summary]
        Args:
            payload (dict): Data to send to API.
        Returns:
            [dict]: [data returned from API]
        """
        data = json.dumps(payload)
        response = requests.request(
            "POST", self.API_URL, headers=self.headers, data=data)
        val  = json.loads(response.content.decode("utf-8"))
        if "error" in val and "is currently loading" in val["error"]:
            await asyncio.sleep(2)
            return await self.direct_query(payload)
        return val


class Gpt2(NLP):
    def __init__(self):
        super().__init__()
        self.API_URL = "https://api-inference.huggingface.co/models/gpt2"
    
    async def expand_text(self, text):
        data = {
            "inputs": text
        }
        data = await self.direct_query(data)
        return data["generated_text"]


class GptNeo(NLP):
    def __init__(self):
        super().__init__()
        self.API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"


class BartMNLI(NLP):
    def __init__(self, API_URL=None, headers=None):
        super().__init__(headers)
        self.API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

    async def catagorize(self, inputs, labels, multi_label=False, use_gpu=False, use_cache=True, wait_for_model=False):
        """Sees how much a label applies to a given input. Coroutine. 
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

    async def summarize(self, inputs: str, min_length=None, max_length=None, top_k=None, top_p=None, temperature=1.0,
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
        resp = await self.direct_query(data)
        try:
            return resp["summary_text"]
        except KeyError:
            return resp


class DialoGPT(NLP):
    def __init__(self):
        super().__init__()
        self.API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"

    async def generate_response(self, input: str, past_input: list, last_responses:list, min_length=None, max_length=None, top_k=None, top_p=None, temperature=1.0,
                repetition_penalty=None, max_time=None):

        data = await self.direct_query(
            {
                "inputs": {
                    "past_user_inputs": past_input, 
                    "generated_responses": last_responses,
                    "text": input
                },
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
                    "use_gpu": self.use_gpu,
                    "use_cache": self.use_cache,
                    "wait_for_model": self.wait_for_model
                }
            }
        )
        conv = data["conversation"]
        return data["generated_text"], conv["generated_responses"], conv["past_user_inputs"]


class distilbert(NLP):
    def __init__(self):
        super().__init__()
        self.API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

    async def classify(self, inputs):
        data = await self.direct_query({
                "inputs": inputs,
                "options": {
                    "use_gpu": self.use_gpu,
                    "use_cache": self.use_cache,
                    "wait_for_model": self.wait_for_model
                }
                })
        return data


class Wav2Vec2(Inferances):
    def __init__(self):
        super().__init__()
        self.API_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"
    
    def convert(self, filename):
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.request("POST", self.API_URL, headers=self.headers, data=data)
        return json.loads(response.content.decode("utf-8"))["text"]
