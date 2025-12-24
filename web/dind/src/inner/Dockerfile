FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y docker.io iputils-ping && rm -rf /var/lib/apt/lists/*

#RUN groupadd -f ctf && useradd -m -g ctf ctfer 

# Create user
RUN groupadd -g 2375 -f docker && \
    groupadd -f ctf && \
    useradd -m -g ctf -G docker ctfer

RUN usermod -aG docker ctfer

RUN pip install flask
COPY app /app

EXPOSE 5000
CMD ["python", "app.py"]
