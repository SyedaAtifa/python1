# simple Dockerfile for running the Flask app on any container platform
FROM python:3.12-slim

WORKDIR /app

# copy only requirements first for caching
COPY pyproject.toml requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# ensure the default port is 5000
ENV PORT=5000

# adjust as needed for production
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000"]
