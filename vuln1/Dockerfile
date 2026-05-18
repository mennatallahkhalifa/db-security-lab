FROM python:3.11-slim
WORKDIR /app
COPY src/ .
RUN pip install flask psycopg2-binary
RUN echo "FLAG{pg_superuser_copy_to_program_rce_9193}" > /tmp/flag.txt
EXPOSE 5001
CMD ["python", "-u", "app.py"]
