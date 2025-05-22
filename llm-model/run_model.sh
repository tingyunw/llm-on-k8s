#!/bin/bash

# Start ollama in background
ollama serve &

# Wait for server to become available
# until curl -s http://localhost:11434 > /dev/null; do
#   echo "Waiting for ollama to be ready..."
#   sleep 2
# done

# Pull the model
ollama pull deepseek-r1:1.5B

# Optionally run it once to warm up
ollama run deepseek-r1:1.5B

# Keep foreground process alive
wait -n