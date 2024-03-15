#!/bin/bash

# activate conda environment    
conda activate ./aiml24

# Define the model path
export repo="TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF"
export model="mixtral-8x7b-instruct-v0.1.Q5_K_M.gguf"

# Check if the model exists
if [ ! -f "models/$model" ]; then
    echo "Model does not exist. Downloading now..."
    # Download the model using huggingface_hub CLI
    huggingface-cli download $repo $model --local-dir models/ --cache-dir .hf_cache
else
    echo "Model exists."
fi  

# start llama.cpp server
python -m llama_cpp.server \
    --model models/$model \
    --port 8000 \
    --n_gpu_layers 50 \
    --offload_kqv True
