FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG APP_PORT=8765
ENV PORT=${APP_PORT}
ENV OLLAMA_BASE_URL=http://host.docker.internal:11434
EXPOSE ${APP_PORT}

CMD ["python", "launch.py"]
