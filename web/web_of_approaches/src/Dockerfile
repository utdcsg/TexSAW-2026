FROM python:3.11-slim
WORKDIR /app

RUN ls
RUN pip install flask
RUN pip install flask_sqlalchemy

COPY app /app

EXPOSE 5000
CMD ["python", "app/app.py"]
