FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_NO_INTERACTION=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl build-essential libpq-dev git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy only dependency files first (for caching)
COPY pyproject.toml poetry.lock ./

# Disable venvs and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-ansi --no-root

# Copy rest of the application
COPY . .

# Expose port
EXPOSE 8000

# Default startup will be overridden by docker-compose command
CMD ["uvicorn", "main:app", "--port", "8000", "--reload"]
