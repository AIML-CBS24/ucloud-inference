from decouple import config


REPO_ID="TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF"
MODEL_FILE_NAME="mixtral-8x7b-instruct-v0.1.Q6_K.gguf"

VERBOSE=True

DJANGO_SECRET_KEY= config("DJANGO_SECRET_KEY")
