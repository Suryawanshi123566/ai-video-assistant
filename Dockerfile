# ── InsightFlow — AI Meeting Assistant ───────────────────────────────────────
# Python 3.11 slim base (smaller image, compatible with all deps)
FROM python:3.11-slim

# ── System dependencies ───────────────────────────────────────────────────────
# ffmpeg  : required by pydub / Whisper for audio processing
# git     : needed by some HuggingFace / pip installs
# curl    : general utility
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Install Python dependencies ───────────────────────────────────────────────
# Copy requirements first so Docker can cache this layer
COPY Requirements.txt .

# Upgrade pip, then install all deps
# torch CPU-only variant is used to keep image size manageable (~2 GB vs ~6 GB)
RUN pip install --upgrade pip && \
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install -r Requirements.txt

# ── Copy application source ───────────────────────────────────────────────────
COPY . .

# ── Streamlit configuration ───────────────────────────────────────────────────
# Disable Streamlit's browser-open behaviour and set a fixed port
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# ── Expose port ───────────────────────────────────────────────────────────────
EXPOSE 8501

# ── Health check ─────────────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ── Entrypoint ────────────────────────────────────────────────────────────────
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
