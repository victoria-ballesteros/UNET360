FROM python:3.12

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8000

# Entrypoint runs the initial DB seed (only for empty collections) before starting the app.
# Invoked via `bash` so it works even when the repo is bind-mounted over /app.
ENTRYPOINT ["bash", "/app/entrypoint.sh"]

# Command to run the application
CMD ["uvicorn", "adapter.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
