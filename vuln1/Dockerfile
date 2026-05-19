FROM python:3.11-slim
WORKDIR /app
COPY src/ .
RUN pip install flask psycopg2-binary
EXPOSE 5001
CMD ["python", "-u", "app.py"]