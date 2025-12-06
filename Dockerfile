FROM python:3.11-slim

# set work directory
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile + Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies via pipenv
RUN pipenv install --system --deploy

# Copy entire project
COPY . .

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
