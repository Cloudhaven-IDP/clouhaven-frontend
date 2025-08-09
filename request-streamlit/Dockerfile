# request-streamlit/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# minimal system deps
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt ./
RUN pip install -r requirements.txt

# App code
COPY .streamlit/ ./.streamlit/
COPY src/ ./src/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8501 8080

# One container, two processes:
# - Flask health server on 8080 (background)
# - Streamlit app on 8501 (foreground)
ENTRYPOINT ["/entrypoint.sh"]
CMD ["src/app.py"]
