FROM python:3.12-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libasound2t64 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    libnss3 \
    libxss1 \
    libxtst6 \
    libdrm2 \
    libxshmfence1 \
    libpci3 \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY . .

# Install uv
RUN pip install uv

# Install project dependencies using uv
RUN uv sync

# Install Playwright and Chromium
RUN uv run playwright install chromium

EXPOSE 8000

ENV PYTHONPATH=/app/src

CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

