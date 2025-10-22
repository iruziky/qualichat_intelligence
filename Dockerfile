# Dockerfile for Qualichat Intelligence
# TODO: Implement the Docker build stages.

FROM python:3.10-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-dev

# Copy the rest of the application
COPY . .

# Command to run the application
CMD ["poetry", "run", "python", "app/main.py"]
