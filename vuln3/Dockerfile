FROM python:3.11-slim

WORKDIR /app
COPY src/ .
COPY init/ /app/init/

RUN pip install flask pymongo

EXPOSE 5003
CMD ["python", "app.py"]
