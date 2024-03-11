from decouple import config


REPO_ID="Qwen/Qwen1.5-0.5B-Chat-GGUF"
MODEL_FILE_NAME="*q8_0.gguf"

VERBOSE=True

DJANGO_SECRET_KEY= config("DJANGO_SECRET_KEY")