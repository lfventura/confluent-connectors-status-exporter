FROM python:3.12-alpine
LABEL org.opencontainers.image.source "https://github.com/lfventura/confluent-connectors-status-exporter"
ENV TZ="GMT"
WORKDIR /app
COPY exporter .
RUN pip install --no-cache-dir -r requirements.txt && chmod u+x status_exporter.py
