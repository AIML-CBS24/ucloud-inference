This repo contains the code for running a llama-cpp-python server with a nginx reverse proxy on UCloud. The app is designed to be deployed on a UCloud server, and it is set up to use a GPU for inference. The point to enable students in the AIML course to interact with a powerful LLM through a simple API call.

## Calling the app

Here is an uncessarily complicated class to make calls against a public URL such as the one we expose from our UCloud server

```python
class UCloudRequester:
    """ This class is a simple container for the UCloud API 
    request. It is used to send a query to the UCloud API 
    and return the response with or without metadata."""

    def __init__(self, url : str) -> None:
        self.url = url # URL of the UCloud API

    def call_url(self, prompt : str, **params) -> dict:
        """This method handles the call to the UCloud API and
        returns the response as a dictionary"""

        # try:
        query = {'prompt': prompt, **params}
        response = requests.post(
            url=self.url,
            headers={'Content-Type': 'application/json'},
            json=query
        )
        return response.json() # <- Translates JSON to dictionary
        
        # except requests.exceptions.JSONDecodeError:
        #     return f"JSONDecodeError: Failed to decode response as JSON: {response.text}"

        # except requests.exceptions.HTTPError as e:
        #     return "HTTPError: " + str(e)
        
    def predict(self, prompt : str, return_meta=False, **params) -> dict:
        """This method is the main method for sending a request.
        if return_meta is set to True, the method will return the
        full response as a dictionary. Otherwise, it will return
        the text of the first choice in the response."""

        result : dict = self.call_url(prompt, **params)
        if return_meta:
            return result
        return result["choices"][0]["text"]
    

requester = UCloudRequester(url=URL)
```

Then you can call the app like this:

```python
# example model params
params = dict(
    max_tokens=50,
    temperature=0.5,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["\n", "###"],
    # logprobs=2, # note: this is not supported by all models
)

PROMPT = "Once upon a time"

prediction = requester.predict(prompt=PROMPT, return_meta=True, **params)
```
Yields
```json
{
  'id': 'cmpl-b352a635-ef93-4ac8-af24-fb73615c7eca',
  'object': 'text_completion',
  'created': 1710194329,
  'model': 'models/qwen1_5-0_5b-chat-q8_0.gguf',
  'choices': [
    {
      'text': ', there was a young woman named Lily who lived in a small village. She was known for her kindness and gentle nature towards others.',
      'index': 0,
      'logprobs': None,
      'finish_reason': 'stop'
    }
  ],
 'usage': {
    'prompt_tokens': 5, 
    'completion_tokens': 27, 
    'total_tokens': 32
  },
 'timestamp': '2024-03-11T21:58:51.087056',
 'email': 'ur-email@cbs.dk'}
```

### Swagger
The app is also set up with a swagger UI at `/docs`. 

***

## Setup on UCloud
Assuming you have set up an nginx app with a GPU and have accessed the terminal. The `setup.sh` should run on initialization, meaning that conda is installed and ready to go.



create the conda environment with CMAKE_ARGS and FORCE_CMAKE to enable cuBLAS support
```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 conda env create -f environment.yml
```

Fire up the llama.cpp server by running `run.sh` . This will download the model from HuggingfaceHub. The default model is "mixtral-8x7b-instruct-v0.1.Q5_K_M.gguf" from the HF repo "TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF"
```bash

```

### Change the model
Change the model in `config.py`. Note that it has to be supported by llama-cpp-python.