# ── Stage 1: build deps ────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-shop.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements-shop.txt


# ── Stage 2: runtime image ─────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

LABEL org.opencontainers.image.title="vend-safe-shop"
LABEL org.opencontainers.image.description="Vend-Safe shop MCP server (no guardrails, demo only)"

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy only what the server needs
COPY shop_server.py .
COPY attacks.py .

# Non-root user for security hygiene
RUN useradd --no-create-home --shell /bin/false appuser
USER appuser

EXPOSE 9000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:9000/admin/state')"

CMD ["python", "shop_server.py"]
