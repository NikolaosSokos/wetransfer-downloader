FROM python:3.12-slim

# Install OS dependencies required by Playwright
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
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project
COPY . .

# Install uv
RUN pip install uv

# Install project dependencies via uv (your choice)
RUN uv sync --no-dev --frozen

# Install Playwright using pip (this installs the CLI)
RUN pip install playwright

# Install Chromium browser for Playwright
RUN playwright install chromium

EXPOSE 8000

CMD ["uvicorn", "src.wetransfer_downloader.api:app", "--host", "0.0.0.0", "--port", "8000"]
