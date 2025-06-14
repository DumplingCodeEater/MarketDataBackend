# -------- Stage 1: Build & Install Dependencies --------
FROM python:3.12-slim AS builder

# Set environment variables
ENV POETRY_VERSION=1.8.2
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
    
WORKDIR /app
    
# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc curl && \
    pip install --upgrade pip && \
    pip install poetry==$POETRY_VERSION
    
# Copy requirements and install to /root/.local
COPY requirements/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
    
# -------- Stage 2: Runtime Image --------
FROM python:3.12-slim

# Set working directory
WORKDIR /app
    
# Copy project code
COPY --from=builder /usr/local /usr/local
COPY . .
    
# Expose port 8000
EXPOSE 8000
    
# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    