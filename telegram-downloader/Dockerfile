FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates tzdata \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir -U pip \
  && pip install --no-cache-dir telethon==1.36.0

COPY tg_channel_downloader.py /app/tg_channel_downloader.py

CMD ["python", "/app/tg_channel_downloader.py"]
