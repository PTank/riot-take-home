FROM ghcr.io/astral-sh/uv:python3.14-alpine

# Install runtime dependencies for Alpine
RUN apk add --no-cache \
    ca-certificates \
    && rm -rf /var/cache/apk/*

# Create non-root user for security
RUN addgroup -g 1000 -S appgroup && \
    adduser -u 1000 -S appuser -G appgroup

# Set working directory
WORKDIR /app

# Copy project configuration files
COPY pyproject.toml uv.lock README.md ./

# Copy application code
COPY app/ ./app/

# Create virtual environment and install dependencies
# Use --frozen to ensure reproducible builds with locked dependencies
RUN uv sync --frozen --no-dev

# Set permissions for non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8000

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
