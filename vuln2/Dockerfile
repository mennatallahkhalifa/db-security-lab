FROM python:3.11-slim

WORKDIR /app
COPY src/ .

RUN pip install flask mysql-connector-python

EXPOSE 5002
CMD ["python", "app.py"]
