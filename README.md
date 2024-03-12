This repo contains the code for a Django app that serves as a wrapper for the `llama-cpp-python` library. The app is designed to be deployed on a UCloud server, and it is set up to use a GPU for inference. The point to enable students in the AIML course to interact with a powerful LLM through a simple API call.

## Calling the app

Here is an uncessarily complicated class to make calls against a public URL such as the one we expose from our UCloud server

```python
class UCloudRequester:

    def __init__(self, url : str, email : str) -> None:
        self.url = url
        self.email = email

    def _predict(self, prompt : str, **params) -> dict:

        try:
            query = {
                'email': self.email,
                'prompt': prompt,
                'params': {**params}
            }
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(self.url, headers=headers, json=query)
            return response.json()
        
        except requests.exceptions.JSONDecodeError:
            return f"Failed to decode response as JSON: {response.text}"

        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)
        
    
    def predict(self, prompt : str, return_meta=False, **params) -> dict | str:
        result : dict = self._predict(prompt, **params)
        if return_meta:
            return result
        return result["choices"][0]["text"]
    
requester = UCloudRequester(
    url="<UCLOUD URL>",
    email="ur-emailc@cbs.dk"
)
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

***

## Setup on UCloud
(Make sure you have a DJANGO_SECRET_KEY set in ur environment. See the `.example.env` file)
Assuming you have set up a django app with a GFPU and have accessed the docker container: 

Initialize mamba and refresh the session
```bash
mamba init
bash -l
```

Then, create a conda environment and install requirements.txt
```bash
mambda create -p ./myenv
mambda activate myenv
mambda install --file requirements.txt
```

Install CUDA toolkit 12.2.2. 
```bash
mamba install -y -c 'nvidia/label/cuda-12.2.2' cuda
```

Install `llama-cpp-python` with cuBLAS support, so that we can use the Nvidia GPU
```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install --force-reinstall --upgrade --no-cache-dir llama-cpp-python
```

Fire up the django app. This will download the model from HuggingfaceHub. The default model is "mixtral-8x7b-instruct-v0.1.Q6_K.gguf" from the HF repo "TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF"
```bash
python manage.py runserver
```

### Change the model
Change the model in `config.py`. Note that it has to be supported by llama-cpp-python.