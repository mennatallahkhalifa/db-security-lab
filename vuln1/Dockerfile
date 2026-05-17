FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install flask psycopg2-binary

# Plant the flag (Member 2 can change this)
RUN echo "FLAG{cve_2019_9193_pg_rce_pwned}" > /flag.txt

EXPOSE 5001
CMD ["python", "app.py"]
