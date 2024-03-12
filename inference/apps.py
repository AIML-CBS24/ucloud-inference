from django.apps import AppConfig
from llama_cpp import Llama
from loguru import logger

from config import REPO_ID, MODEL_FILE_NAME, VERBOSE


class App(AppConfig):
    name = 'inference'
    verbose_name = "AIML24 Inference App"
    llm = None

    def ready(self):

        # Load the model from Hugging Face Hub
        App.llm = Llama.from_pretrained(
            repo_id=REPO_ID,
            filename=MODEL_FILE_NAME,
            n_gpu_layers=-1,  # Use GPU acceleration if available
            local_dir="models",
            cache_dir=".hf_cache",
            n_ctx=4_000,
            verbose=VERBOSE,
            
        )
        logger.debug("Model loaded successfully 🚀")

