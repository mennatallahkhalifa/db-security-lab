FROM python:3.11-slim

WORKDIR /app
COPY app/ .

RUN pip install flask pymongo

EXPOSE 5003
CMD ["python", "app.py"]
