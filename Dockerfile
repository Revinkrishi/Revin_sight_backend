FROM python:3.11-slim

WORKDIR /app

# Install Pipenv properly (important: system packages required)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir pipenv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# Install pipenv only (no GCC required)
RUN pip install pipenv

# Copy required files
COPY Pipfile Pipfile.lock ./

# Install deps inside system (no compile)
RUN pipenv install --system --deploy --skip-lock

# Copy project
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

