FROM ollama/ollama:0.7.0

WORKDIR /app

COPY run_model.sh run_model.sh
RUN chmod +x run_model.sh

ENTRYPOINT ["./run_model.sh"]