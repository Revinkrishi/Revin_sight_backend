FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Pipenv properly (important: system packages required)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir pipenv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Pipenv files first (best practice)
COPY Pipfile Pipfile.lock ./

# Install dependencies into system Python environment
RUN pipenv install --system --deploy

# Copy actual source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload", "--port", "8000"]
