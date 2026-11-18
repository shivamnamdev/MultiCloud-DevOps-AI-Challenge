FROM python:3.12-slim
RUN useradd -m -u 10001 app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app app.py .
USER app
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "1", "app:app"]
