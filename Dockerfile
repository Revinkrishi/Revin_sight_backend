FROM python:3.11-slim

WORKDIR /app

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

