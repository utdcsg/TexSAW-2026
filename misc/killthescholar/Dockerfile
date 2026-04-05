FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends coq && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY src/app.py src/flag.txt ./
COPY src/index.html /app/templates/

EXPOSE 3333

CMD ["gunicorn", "--bind", "0.0.0.0:3333", "--workers", "2", "--timeout", "60", "app:app"]
