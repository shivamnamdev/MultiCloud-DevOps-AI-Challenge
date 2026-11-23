FROM python:3.12-slim
COPY --from=alpine/k8s:1.31.2 /usr/bin/kubectl /usr/local/bin/kubectl
RUN pip install --no-cache-dir "mcp[cli]<2" pytest
WORKDIR /app
COPY hatch.py .
